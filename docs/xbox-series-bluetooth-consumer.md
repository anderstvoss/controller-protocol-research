# Xbox Series Bluetooth-bus UHID: consumer-evidence gap review

**Status: source-only research, no host or hardware tests.** This brief assesses whether the existing `linux.uhid.bluetooth` realization can represent a Series **Bluetooth HID** device to Linux and SDL. It does not assert real Bluetooth pairing or physical-controller fidelity. All new claims use `xbox-cgap-*`, `evidence_role: consumer` and `experiments: []`.

## Prior research and non-duplication

- [Research PR #116](https://github.com/anderstvoss/controller-protocol-research/pull/116) is the stock **wired xpad evdev** 26-capability reference. It is not a native Bluetooth HID descriptor or a guarantee about xpadneo's output.
- [Research PR #123](https://github.com/anderstvoss/controller-protocol-research/pull/123) concerns USB **GIP and the proprietary wireless receiver**, not Bluetooth HID. Its claims need not be re-pinned or edited.
- Existing `xbox-series-sdl-bluetooth-rumble` and `xbox-series-sdl-bluetooth-report-roles` already establish SDL's fallback Bluetooth report 0x03 and state/Guide/battery report dispatcher. Below we investigate **decoder selection, firmware scope, Linux identity, driver ownership and output delivery**, rather than reasserting those packet templates in new claims.
- Existing `xbox-series-bluetooth-device-gaps` remains **unknown**: this study does not measure reference hardware, firmware identity, canonical descriptor bytes, physical battery telemetry or actual four-motor effects.

## Ranked consumer findings

| Rank | Surface | Pinned source finding | Evidence ceiling and remaining gap |
| ---: | --- | --- | --- |
| 1 | Linux driver binding | Kernel `hid-microsoft` explicitly matches Bluetooth Microsoft model 1914 (`045e:0b13`), with main-motor FF; optional `hid_xpadneo` matches the same bus/identity; unmatched HID may reach `hid-generic`. | Consumer source only; no binding-order or virtual-HID open experiment. |
| 2 | Descriptor and firmware | xpadneo documents a **283-byte Series BLE** descriptor sample (input ID 0x01, output ID 0x03). Legacy 1708 Linux-mode and Elite 2 BLE have other, model-specific descriptors. | No definitive Series descriptor matrix by firmware; do not transplant the legacy/Elite examples. |
| 3 | SDL HIDAPI ownership | SDL's Linux descriptor parser takes precedence when it accepts axes and 12/15 buttons. Otherwise Bluetooth-specific state/Guide/battery dispatch is used; Xbox-type classification and HIDAPI enablement are separate gates. | Consumer source only; no proof that SDL opens or prefers a given virtual `hidraw` node. |
| 4 | Identity mutation | xpadneo maps `045e:0b13` to a normalized `045e:028e` with version `0x1130` before HID parsing. | Exposed post-driver identity is not native hardware identity; downstream SDL behavior needs measurement. |
| 5 | Input/Guide/Share/battery | SDL has firmware-scoped fallback button layouts; xpadneo rewrites some button mappings and exposes a `power_supply` battery surface. | Do not assume wired xpad's exact 26 capabilities or a universal Guide/battery cadence. |
| 6 | Rumble and impulse triggers | Kernel `hid-microsoft` FF handles main motors. xpadneo fills four Bluetooth motor fields but **derives trigger values from main FF and trigger pressure**. SDL can explicitly request trigger amplitudes in its HIDAPI path (already recorded). | No independent four-channel evdev FF API; firmware output acknowledgment and physical effects remain untested. |
| 7 | UHID/BlueZ distinction | BlueZ's HID-over-GATT route creates a Bluetooth-bus HID device through UHID; xpadneo BLE output uses an acknowledged `SET_REPORT` path rather than only a raw output write. | Host-local virtual UHID is not Bluetooth advertising, pairing or a remote device. No acceptance run. |
| 8 | Audio and lifecycle | xpadneo documentation excludes headset audio in Bluetooth mode; tested consumer attach, reconnect, shutdown and sidecar behavior are absent. | No physical audio claim or implementation plan. |

## Pinned sources

- Linux kernel `4056b3c9d3c92ea45955641dbafeb9b960e146ef`: `drivers/hid/hid-microsoft.c:275-350,391-444`, `hid-ids.h:1056-1060` and `hid-generic.c:82-90`. These are recorded as `xbox-cgap-kernel-*` sources, with full-file SHA-256. The stock driver has a real Bluetooth match for `045e:0b13`, and its FF callback supplies the main motors only.
- xpadneo `56b538d951300bf804f6631738603c5eb14c04f0`: `core.c:48-71,169-241`, `device.c:14-36,143-262`, `events.c:60-137`, `mappings.c:32-66,130-155`, `rumble.c:56-137,150-219`, `power.c:12-167`. Kernel module files are GPL-2.0-only. Upstream documentation is cited and paraphrased, not copied; its README and descriptor references are licensed separately.
- Reused existing SDL source `xbox-series-sdl-xboxone` at `d4557c1511c721485dc4960f7149730afc9a73a0`, specifically `SDL_hidapi_xboxone.c:355-475,564-630,669-695,714-980,1257-1311,1377-1464,1942-2012`.
- Reused existing BlueZ `steam-ble-bluez-hog-profile` and `steam-ble-bluez-uhid` source records. This is generic HOGP host plumbing; it is not an Xbox-specific field dump.

## Firmware and descriptor applicability

| Family / evidence example | Transport and identifier | Descriptor/report notes | Limitation |
| --- | --- | --- | --- |
| **Xbox Series model 1914** | Bluetooth LE, typical Microsoft `045e:0b13` | xpadneo cites one 283-byte descriptor with input 0x01 and output 0x03. SDL fallback source cites Series firmware **5.5.2641** and a 17-byte state with Share at the final byte. | These are **separate upstream evidentiary examples**, not a demonstrated paired descriptor-and-packet capture on the same firmware. The example is not universal. |
| Xbox One S model 1708 | Classic Bluetooth on older firmware and BLE on newer firmware; several PIDs | SDL source describes firmware 3.1.1221 16-byte state with separate Guide; firmware 4.8.1923 17-byte state with Windows/Linux Guide differences. xpadneo describes 306-byte truncated/334-byte Linux-mode descriptors. | A **comparator**, not a native Xbox Series model 1914 profile. |
| Xbox Elite Series 2 model 1797 | Different classic/BLE variants; BLE `045e:0b22` | xpadneo documents a 464-byte BLE **5.23** descriptor and possible HID-BPF rewrite; SDL source documents older paddle and Guide variants. | A **comparator**. Do not infer the Elite descriptor for Series model 1914. |

The xpadneo README says BLE-era controllers share a unified layout, but the same pinned repository contains longer Elite 2 and legacy examples and conditional descriptor repairs. Interpret the README as a model-generation generalization, **not byte-for-byte identity across all firmware and variants**. The source description of a 283-byte Series descriptor does not by itself establish which physical firmware versions use exactly those bytes.

No upstream source excerpts, HID descriptor bytes, Bluetooth addresses or raw captures are committed in this PR.

## Consumer path, report dispatch and mapping

**Linux bind path.** A Bluetooth-bus HID identity with Microsoft VID `0x045e`, PID `0x0b13` is eligible for the pinned kernel's `hid-microsoft` driver and for the optional out-of-tree xpadneo driver. Module availability, driver matching order, actual HID descriptor validity and HID-BPF rules determine which probe succeeds. Generic HID is fallback, not proof of a functional gamepad. This differs from the USB `xpad` implementation in PR #116.

**SDL path.** Pinned SDL enables its Xbox One HIDAPI backend through configuration and Xbox-type classification. On Linux it attempts to parse the report descriptor. If X and Y axes plus an expected 12- or 15-button field are found, the descriptor-driven usage decoder handles reports. If parsing is rejected, the Bluetooth fallback examines input ID `0x01` as state, `0x02` as a potentially separate Guide report, and `0x04` as battery. This last set of IDs **reuses existing corpus claims**. The fallback is not a guarantee that IDs 0x02/0x04 are physically present in the 283-byte Series descriptor example.

**Firmware-scoped behavior.** The fallback has distinct 16-byte and longer state formats. It only reads Guide from the inline state when no separate Guide report has been recognized. For the documented Series 5.5.2641 layout, it reads Share separately from View. Battery levels are approximate quartile-like 10/40/70/100 percent with additional flags for charging/battery; they are SDL policy, not a calibrated gas gauge.

**xpadneo path (corrected after deeper review).** xpadneo's kernel driver normalizes identity to `045e:028e` and version `0x1130`. It fixes HID usages and sometimes the button bitmap before creating Linux input events. Its header defines `BTN_XBOX` as `BTN_MODE` and `BTN_SHARE` as **`KEY_F12`**, and the event handler routes Share to a separate keyboard device, removing it from the gamepad key capability set. The README's F12 description **agrees** with the code. Guide also serves as a shift modifier by default. Its optional synthetic mouse/keyboard/consumer devices and extra `ABS_PROFILE` axis make its evdev topology materially different from xpad's 26-capability fixture. Battery report ID is learned from HID usage, and a `power_supply` interface may be registered. See the [full xpadneo consumer deep dive](xbox-series-xpadneo-consumer.md).

**SDL/hidraw permission caveat:** the packaged xpadneo udev rules actively rebind supported devices and restrict ordinary users' hidraw access, so SDL's direct HIDAPI consumer cannot be assumed to open alongside xpadneo. Evdev acceptance and explicitly permitted HIDAPI tests need separate evidence. See the [xpadneo deep dive](xbox-series-xpadneo-consumer.md).

## Rumble and output ownership

The kernel `hid-microsoft` source maps Linux `FF_RUMBLE` to the two main actuator fields. xpadneo's output report supports four amplitude fields, but it applies a **controller-driver policy**: each trigger gets an intensity based on current trigger pressure and the larger main FF magnitude. A quirk can disable those fields. Therefore a user may observe impulse-trigger activity with xpadneo while **no application has separate evdev control of each trigger**. SDL's HIDAPI trigger-rumble method is a different application API, already pinned by the prior claims.

For BLE output, the pinned xpadneo uses an acknowledged HID output `SET_REPORT` request; for non-HOGP connections it uses output-report write with delay. A virtual UHID backend must correctly answer any host-to-device requests that actually occur. Merely accepting input reports or matching `hid-microsoft` is insufficient to mark reverse-output acceptance.

## Implications for virtualgamepad

**Source-backed feasibility, not a realization promotion.** A `linux.uhid.bluetooth` realization is plausible because Linux consumer drivers match Bluetooth HID identities and BlueZ exposes BLE HID through UHID. However, the required **firmware-specific descriptor**, native report contents, SDL selection, HID/output request behavior, battery, Guide/Share, concurrency and cleanup are not verified together. Keep the realization at **No evidence for fidelity** until a bounded host run establishes a consumer path and an owner reference establishes physical parity; using a guessed report descriptor would violate the standing no-fake-protocol requirement. Real BLE radio, pairing and advertising remain [virtualgamepad #164](https://github.com/anderstvoss/virtualgamepad/issues/164), separate from host-local Bluetooth-bus UHID.

### Proposed acceptance experiments — not run

1. **Owner physical reference:** privately collect a standard Series model 1914 BLE identity, firmware version and HID descriptor hash/length; use a safe, non-identifying summary only. Compare 283-byte upstream example if appropriate; do not assume it.
2. **Consumer binding:** on a declared kernel/build, compare actual driver/module selection under stock `hid-microsoft`, explicit xpadneo and `hid-generic` fallback, recording failures as failures rather than switching without notice.
3. **UHID-only synthetic probe:** create a test-profile Bluetooth-bus UHID using an independently validated descriptor, then verify kernel bind, input device(s), hidraw ownership, SDL HIDAPI-versus-evdev selection, zero/neutral input and deterministic removal. A synthetic descriptor fixture alone is not a physical test.
4. **Input correctness:** press/release Guide, Share, View/Menu, axes and triggers; check report layout, evdev mapping and SDL semantics against the same firmware reference. Include descriptor-driven and fallback decoding separately.
5. **Output:** test main rumble and the two trigger fields through SDL, kernel FF and xpadneo, including the acknowledged HOGP `SET_REPORT` path, feature/output replies, output ownership and intentional no-response cases.
6. **Life cycle:** repeat create/remove and failed-open/partial-probe cases; verify no leaked nodes, handle rebind and stereo/audio expectations separately. Actual remote pairing/radio tests belong to #164.

No device, Bluetooth controller or Linux-host test was available to this research agent. The PR makes **no protocol implementation recommendation** and does not modify prior records.
