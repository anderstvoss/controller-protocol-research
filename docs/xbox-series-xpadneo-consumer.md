# xpadneo as a Bluetooth HID consumer: Xbox Series deep dive

**Scope:** Host-side source inspection only of [atar-axis/xpadneo](https://github.com/atar-axis/xpadneo/tree/56b538d951300bf804f6631738603c5eb14c04f0) at `56b538d951300bf804f6631738603c5eb14c04f0`. No host, controller, pairing, packet captures or HID/UHID tests were available. The repository's driver files carry GPL-2.0-only; its documentation is generally GPL-3.0-or-later. All findings are paraphrased and cited by pinned files and line ranges. No upstream source, descriptor bytes or physical identifiers are added to this corpus.

This extends [Bluetooth research PR #124](https://github.com/anderstvoss/controller-protocol-research/pull/124) without duplicating [stock xpad evdev PR #116](https://github.com/anderstvoss/controller-protocol-research/pull/116), [xone wired/receiver PR #123](https://github.com/anderstvoss/controller-protocol-research/pull/123), or the prior SDL Bluetooth report claims. All new `xbox-cgap-*` records are consumer evidence and contain no experiments. The existing Series Bluetooth *device-side* gap remains unknown.

## Ranked conclusions

| Rank | Surface | What the pinned xpadneo implementation actually does | Evidence ceiling / unknown |
| ---: | --- | --- | --- |
| 1 | Share and Guide | Share becomes a separate keyboard `KEY_F12`, not the xpad gamepad `KEY_RECORD`. Guide (`BTN_MODE`) is a shift modifier by default: press may be held until release, or consumed for profiles/mouse. | Driver output semantics only; not hardware report truth. |
| 2 | Devices and identity | Bluetooth HID probe matches Series `045e:0b13`, normalizes HID product/version to `045e:028e` / `0x1130`, and can expose distinct gamepad, keyboard, consumer-control and mouse input nodes. | Exact effective nodes/identity depend on descriptor, configuration and probe. |
| 3 | Kernel and SDL ownership | Its packaged udev rules rebind compatible Bluetooth HID devices and restrict ordinary `hidraw` access, steering consumers toward evdev. | No actual permission or SDL backend-selection test. |
| 4 | Input axis topology | Sticks are signed 16-bit in the evdev projection, triggers are 0..1023, and `ABS_PROFILE` is an additional axis; deadzones, fuzz and layout differ from stock xpad. | Do not copy PR #116's 26-control evdev fixture as xpadneo truth. |
| 5 | Impulse rumble | Nine-byte Bluetooth output report 0x03 has four motor amplitudes; FF playback derives trigger magnitudes from trigger pressure and main FF. Connection-notification test can address triggers before application rumble is enabled. | Neither independent four-motor evdev FF nor physical actuator confirmation. |
| 6 | BLE output | The driver's HOGP branch uses acknowledged `HID_REQ_SET_REPORT` and requires a synchronous UHID reply. Version/bus heuristics determine which output route is selected. | No `UHID_SET_REPORT_REPLY` host validation, real-radio pairing or duty-cycle measurement. |
| 7 | Battery and accessories | Descriptor-discovered battery usage feeds a Linux `power_supply` node. Profiles and optional mouse/keyboard/consumer nodes are driver-managed. | Battery reporting cadence, exact device status and consumer discovery unmeasured. |
| 8 | Models and firmware | Bluetooth identifiers cover older One S, Elite 2 and standard Series; descriptor correction and quirks are conditional. USB GIP/receiver do not bind to this Bluetooth-only HID driver. | No supported Series firmware matrix or special Nano variant assertion. |
| 9 | Audio/LED/diagnostics | No headset ALSA PCM or independent LED-class endpoint in the reviewed driver; xpadneo docs disclaim Bluetooth headset audio. Debug mode can emit complete unpatched descriptors and identifying metadata. | Software-scope absence only; do not publish raw logs. |

## 1. Driver scope, model table, and attach sequence

Source: `hid-xpadneo/src/xpadneo/core.c:34-71,146-320` and `hid-xpadneo/src/xpadneo/xpadneo.h:26-105`.

| Bluetooth HID identity (vendor `045e`) | xpadneo's classification | Applicability |
| --- | --- | --- |
| `02e0`, `02fd`, `0b20` | Xbox One S / 1708-family classic and BLE presentation variants | Comparator; **not** a Series 1914 descriptor. |
| `0b05`, `0b22` | Xbox Elite Series 2 family | Distinct paddle/firmware/HID-BPF considerations. |
| `0b13` | Xbox Series X/S wireless controller | Target reference only for matching Series identity. |

Some third-party controllers are also matched explicitly; shared identifiers are not conclusive evidence of genuine Microsoft hardware. The pinned xpadneo driver matches `HID_BLUETOOTH_DEVICE`; it does **not** supply a wired Xbox USB GIP or proprietary receiver implementation. Unlike xone, it does not make the controller a GIP client.

The probe allocates per-device state, marks `HID_QUIRK_INPUT_PER_APP` and `HID_QUIRK_NO_INPUT_SYNC`, preserves the original identity and then changes the HID-visible vendor/product/version before parsing. The normalized fields are `045e:028e` and `0x1130` across its matched controller types. It calls HID parse/start, initializes consumer-control and keyboard subdevices, then optional mouse, power, quirks and FF. A failure can unwind those stages, and removal closes HID, restores original identity, cancels work and destroys auxiliary nodes. Pinned `core.c:68-138,169-319`. This is a **specific xpadneo interface**, not the native Series Bluetooth descriptor.

## 2. Input devices and non-parity with stock xpad

Sources: `events.c:186-375`, `xpadneo.h:26-205`, `mappings.c:32-66`, `synthetic.c:11-82`, `keyboard.c:11-47`, `consumer.c:11-35`, `mouse.c:17-90,230-279`.

- **Share correction to PR #124:** `BTN_SHARE` is a *source alias* for `KEY_F12` declared in `xpadneo.h:26-28`. The mapping then gives Share that key code, `events.c:239-251` routes it to the keyboard device, and `events.c:343-353` removes it from the gamepad. The xpadneo README also says F12. There was **no code-versus-documentation contradiction**; the earlier research incorrectly treated an alias name as a normal gamepad button.
- **Guide:** `BTN_XBOX` aliases `BTN_MODE`; the default Guide modifier holds its press and replays a synthetic press/release on release if unused. Guide plus A/B/X/Y can change an emulated profile; Guide plus View can toggle mouse mode. Setting `disable_shift_mode=1` changes that policy; Guide timing and combination semantics are not raw firmware cadence.
- **Axis surface:** default stick axes are signed `-32768..32767` with fuzz `32` and flat `3072`, trigger axes `0..1023` with fuzz `4`, plus `ABS_PROFILE` range `0..3`. Module options can change deadzones, and Elite paddles add more keys when applicable. This differs from the exact xpad evdev fixture established by PR #116.
- **Multiple devices:** `HID_QUIRK_INPUT_PER_APP` splits HID application collections, while synthetic helpers can add Consumer Control, Keyboard and Mouse nodes when absent from the descriptor. The optional Mouse node can exist while mouse mode is inactive. Each synthetic input device inherits the post-normalization parent bus, vendor, product and version; thus one Bluetooth HID device can have multiple evdev children. No exact node count is asserted without actual probe.

Mouse mode has a 10 ms timer to emit relative movements, uses triggers for mouse clicks and redirects some buttons to keyboard/consumer events. The timer starts after initialization, stops on remove and is not a HID report-rate specification. `mouse.c:17-90,105-228,232-279`.

## 3. Descriptor handling and firmware/clone scope

Source: `device.c:143-262`, `events.c:63-137`, `quirks.c:45-200`, and the previously pinned Series/One S/Elite descriptor documentation.

A successful probe depends on an interpretable HID report descriptor. xpadneo repairs selected malformed or differently labelled descriptors (including an Xbox One S truncated legacy example, axis usage remapping and older Linux-style button layouts). It can split Elite 2 paddle usages into gamepad buttons. `events.c` also suppresses unchanged report 0x01 packets and can remap sparse Linux-mode button positions conditionally. These **fixups do not establish universal Xbox Series firmware bytes**.

xpadneo's newer BLE documentation describes shared layouts; the actual pinned descriptor examples are still model/firmware scoped: one 283-byte Series example, older One S legacy variants and a distinct 464-byte Elite Series 2 BLE 5.23 example. Avoid using a One S or Elite descriptor as a Series 1914 fixture. Some compatible clones share Xbox-style identifiers; xpadneo uses descriptor length and device metadata to select quirk policies, including different motor masks and no-trigger-rumble. Do not publish Bluetooth identifying metadata or imitate an unrelated product identity.

## 4. HID output, FF, impulse triggers, and probe side effects

Sources: `xpadneo.h:54-105`, `rumble.c:18-41,56-219,229-482`, `device.c:14-36`.

The driver assembles a nine-byte HID output report with **report ID 0x03**, four motor-enable bits, independent output amplitude *fields* for left and right triggers and weak/strong main motors, and sustain/release/loop parameters. This is Bluetooth HID framing, **not GIP**. The primary Linux API is still `EV_FF` `FF_RUMBLE`: the callback receives two usual FF magnitudes and calculates each trigger output based on the larger main magnitude, current left/right trigger pressure, attenuation and quirks. Neither the application nor evdev supplies four independent motor magnitudes by this path. The driver can filter repeated commands and suppress disabled/masked motors.

The default `ff_connect_notify` setting also runs a welcome/test sequence, addressing weak, strong and optionally trigger motors before normal streaming is advertised ready; a real host may therefore receive unsolicited rumble requests on attach. This is an *initialization consumer behavior*, not an application FF request. The source contains delays between test stages; do not derive a firmware keep-alive or runtime packet cadence from them. `rumble.c:229-351,418-482`.

Once initialized, the driver creates an FF effect store with upload, erase and playback callbacks; it refuses unsupported effect types rather than routing arbitrary FF effects to GIP. It can disable FF readiness and drain its worker queues during removal. `rumble.c:354-482`.

## 5. Bluetooth version, request/reply and UHID acceptance

Sources: `core.c:173-194`, `device.c:14-36`, existing kernel source `uhid`.

xpadneo derives its HOGP flag from both **Bluetooth bus** and supplied HID version `>=0x0500`. For that path it uses a HID output `SET_REPORT` request requiring an acknowledged completion. In non-HOGP mode it submits an output report and waits briefly before the next send. For an emulated Bluetooth-bus UHID device, a host can therefore emit `UHID_SET_REPORT` and require `UHID_SET_REPORT_REPLY`; a backend that only listens for `UHID_OUTPUT` will be insufficient in such a branch. This is supported by the Linux UHID interface contract, but no real xpadneo-to-UHID exchange was executed.

An actual BLE HID-over-GATT peer has *additional* advertisement, pairing, ATT/GATT and radio behavior. A local `BUS_BLUETOOTH` UHID object does **not** make the host discoverable over Bluetooth. Those separate tasks remain virtualgamepad #164.

## 6. Desktop/SDL access and permissions

Source: the two pinned xpadneo udev rule files.

The packaged `60-xpadneo.rules` recognizes supported Bluetooth HID IDs, may unbind a previously attached driver and bind xpadneo, and gives the **gamepad input device** active-session `uaccess` permissions. The packaged `70-xpadneo-disable-hidraw.rules` explicitly restricts ordinary `hidraw` file access by setting mode 0000 and removing `uaccess` from associated nodes. This may prevent an ordinary application from opening xpadneo's HIDAPI raw path, causing SDL to consume the **evdev** surface instead. A privileged application, customized rules or a device not processed by these rules can differ. No permission or SDL selection was measured.

This creates a real consumer acceptance distinction:
- Test **SDL with default installed xpadneo rules** for evdev child-device topology and F12 keyboard behavior.
- Test **SDL HIDAPI with consciously permitted hidraw access** only as a separate diagnostic, reporting whether the HID backend actually opens and how it parses a normalized post-driver identity.
- Do **not** equate either result with the one-node xpad fixture or with native hardware BLE pairing.

## 7. Battery, audio, LED and diagnostics

The driver discovers a battery report from its HID descriptor and creates a Linux power-supply surface only when its runtime conditions are satisfied; status and approximate capacity are reconstructed from flags (`mappings.c:130-155`, `power.c:12-167`). This differs from SDL's fallback battery state processing; neither provides a measured physical polling cadence.

The reviewed code has no ALSA headset PCM or independent LED-class implementation. The upstream xpadneo README specifically excludes Bluetooth headset audio. Do not reuse xone's wired/receiver audio findings as Bluetooth evidence. No hardware-wide LED, audio or battery impossibility is established by absence of an xpadneo feature.

The debug subsystem logs a descriptor size and CRC16 and may dump **unpatched descriptor bytes** to kernel logs based on module settings or a locally administered device identity. Raw logs, device identifiers and descriptors from a private owner session must undergo source-lineage and redaction review before publication; they are not supplied here. `debug.c:20-41,130-186`.

## 8. Virtualgamepad disposition and unrun test plan

**Recommendation — inference:** xpadneo is a valuable *acceptance consumer* for a future, explicitly evidence-backed `linux.uhid.bluetooth` realization. It is not a source of authoritative physical Series HID packets, nor a reason to emulate a special xpadneo-only device rather than a real firmware-scoped Series descriptor. No GIP is involved. Leave the realization at **No evidence for physical fidelity**.

Physical tests — **not run**:
1. Privately pair a known standard Series model 1914 reference. Log firmware/model, descriptor length and a hash without copying raw descriptor data, Bluetooth identifiers or host paths into the public repo. Check whether the documented 283-byte example is applicable.
2. In separate experiments, identify which driver actually binds under stock `hid-microsoft`, installed xpadneo with its udev rules, and generic HID fallback; capture only sanitized structural results.
3. Enumerate all evdev children and their advertised keys/axes, including Share as keyboard F12, delayed Guide behavior, 0..3 profile axis and optional mouse node. Do not impose the 26-capability xpad baseline.
4. Test a locally created **evidence-derived** Bluetooth-bus UHID device with appropriate identity, HID descriptor and version. Exercise `UHID_SET_REPORT` replies, failure/timeout, and output ordering. Synthetic success is not physical success.
5. Compare application FF, xpadneo's attach-time welcome rumble, a trigger-only output request from an independent HIDAPI client if permitted, and native physical actuation as distinct experiments.
6. Verify that SDL and Steam/Input choose evdev or HIDAPI as expected under actual udev rules and that all created nodes and event workers disappear after close/reconnect.

**No tests executed** in this research; no vendor firmware analyzed, no raw captures retained, no code ported. Owner decisions on Bluetooth UHID and radio/pairing remain separate.
