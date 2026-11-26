# Wii U Pro Controller — post-Alpha 2 starter research

**Disposition:** source-only research, no host or controller hardware test. Pinned Linux **v6.12**, SDL Wii HIDAPI **877399b2b2cf21e67554ed9046410f268ce1d1b2**, and Cemu **29f2f1fae4631e2317977debd9eacd55cc28dd7d**.

| Decision area | Evidence-backed answer | Confidence / limit |
| --- | --- | --- |
| Identity | Kernel explicitly classifies `Nintendo RVL-CNT-01-UC` and extension type `0x0120` as Wii U Pro. hid-wiimote's Bluetooth Nintendo table covers `0x057e:0x0306` and `0x057e:0x0330`, without a dedicated Pro PID. | Pinned consumer source; retail Pro VID/PID, SDP and revisions unmeasured |
| Kernel driver | `hid-wiimote` via **Bluetooth-bus HID only**; Pro identity selects a separate module/device category, not the Wii Remote extension-port layout. | Linux v6.12 code, not host proof |
| Kernel evdev shape | Dedicated Pro input node: **17 keys**, four `ABS_X/Y/RX/RY` axes, `FF_RUMBLE`; axes `-1024..1024`, fuzz `4`, flat `100`; LED and battery infrastructure on HID parent. | Driver declarations, not captured events |
| Wire-facing parser | Pro-like extension ID suffix `0x01 0x20`; extension-only report `0x3d`, **21 extension bytes**, first 11 used for analog sticks, active-low buttons and status bits. | Kernel/SDL decoding assumptions, not hardware validation |
| SDL driver and mapping | Wii HIDAPI accepts the Wii VID and the two Wii PIDs, discovers Pro through extension type `0x0120`, then emits **15 buttons, six axes**: four sticks plus digital ZL/ZR triggers; special battery decoding. | Pinned SDL source; availability depends on HIDAPI settings/access |
| Other consumers | Cemu's **native Wiimote HIDAPI path deliberately excludes** the Pro product string. Dolphin Pro-specific behavior and Cemu generic gamepad routes remain unverified. | Cemu pinned negative result; no blanket emulator-support claim |
| Differences from Wii Remote | Built-in Pro gamepad controls and dual analog sticks, no external accessory port, no Pro MotionPlus or Wii Remote IR/accel modules in Linux. It shares Wii report/control infrastructure, not native input topology. | Pinned kernel and SDL implementation |
| Recommended first realization | **`linux.uhid.bluetooth`** to engage `hid-wiimote` and preserve raw HID/sysfs/evdev semantics; `linux.uinput` is a later explicitly reduced playable fallback. | Architectural inference, **not** real Bluetooth pairing |
| Family model | Register **`wii-u-pro` with parent `null`**. Implement distinct curated native state on reusable Wii report/transport primitives, not as a Wii Remote extension attached to a logical Remote. | Recommendation to #361; no implementation |
| Playable versus faithful | Playable = correctly enumerated and mapped basic inputs in at least one tested consumer. Faithful = Pro-specific identity, reports, host commands, outputs, timing, battery/charging, creation/removal and ideally reference-device parity. Neither status is earned. | No host or physical tests |
| Open unknowns | Exact physical SDP/VID/PID, calibration/EEPROM policy, startup/reconnect, charge semantics, identity metadata, Pro acceptance under UHID, and Dolphin/Cemu alternative inputs. | Explicit gaps below |

## Pinned implementation evidence

- Linux [hid-wiimote core](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-core.c#L432-L455) classifies Pro extension data; [name/type decision](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-core.c#L809-L855), [Pro-only module policy](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-core.c#L594-L621), [input report dispatcher](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-core.c#L1594-L1618), [Bluetooth HID table](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-core.c#L1869-L1889) and [HID IDs](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-ids.h#L985-L987). The driver table is Bluetooth-bus-only; it does not implement radio discovery or pairing. GPL-2.0-or-later, paraphrased without code excerpts. Corpus sources: `wii-gap-dolphin-attach-kernel-core-v612`, `wiiupro-pa2-linux-hid-ids-v612`.
- Linux [Pro 11-byte fields and stick decoding](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-modules.c#L1572-L1705), [active-low key map](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-modules.c#L1707-L1761), [event open/report-mode switch](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-modules.c#L1764-L1786), [calibration sysfs](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-modules.c#L1813-L1860), [evdev setup](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-modules.c#L1862-L1929), [Pro force feedback](https://github.com/torvalds/linux/blob/v6.12/drivers/hid/hid-wiimote-modules.c#L1788-L1810). The 12-bit sticks are centered/inverted and optionally auto-corrected on the first packet, rather than populated with known physical calibration. Source: `wii-gap-dolphin-attach-kernel-modules-v612`; GPL-2.0-or-later.
- SDL [device VID/PID gate](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L182-L190), [extension type](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L354-L367), [Pro MotionPlus exclusion](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L385-L443), [report mode](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L550-L589), [stick calibration defaults](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L592-L603), [identity/name](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L712-L733), [button/axis counts](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L809-L817), [packed button map and six-axis output](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L926-L1054), [input report 0x3d dispatch](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L1439-L1491) and [charging/battery heuristics](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L509-L548). SDL zlib licence; source `wiiupro-pa2-sdl-wii-877399b2`.
- Cemu [native Wiimote HIDAPI product filter](https://github.com/cemu-project/Cemu/blob/29f2f1fae4631e2317977debd9eacd55cc28dd7d/src/input/api/Wiimote/hidapi/HidapiWiimote.cpp#L5-L48) explicitly skips `Nintendo RVL-CNT-01-UC`. This does **not** rule out the emulator's SDL/general input APIs. MPL-2.0; reused source `wii-gap-consumer-cemu-hidapi`.

**Scope protection:** The existing [Wii Remote ledger](ledgers/wii-remote-l0.md) explicitly excludes Pro. Its `wii-` claim prefix and `tests/test_wii_ledger.py` count remain unchanged; all new claims use controller `wii-u-pro` and prefix `wiiupro-pa2-`. Existing WiiBrew source records describe other Wii-family devices; no unrecorded WiiBrew claim or page content is assumed.

## Recommended construction boundaries

Keep a distinct Wii U Pro curated family with a full digital gamepad topology and two sticks. Reuse Wii-family transport framing, host report/command machinery, rumble/LED handling and shared lifecycle logic where source-backed, but do not inherit Wii Remote-specific IR, accelerometer, removable Nunchuk/Classic/MotionPlus topology or Wii Remote identity. Treat the kernel's Pro **internal extension module** as a decoding mechanism, not evidence of a physical expansion connector.

Prototype `linux.uhid.bluetooth` first: its Bluetooth **bus metadata** is sufficient to exercise Linux HID driver selection when the descriptor and identity are correct. It is **not** a Bluetooth advertising, pairing or radio-backed realization. A later `linux.uinput` option could expose basic buttons/sticks; it would lack the native HID parent, hidraw commands, sysfs LED/battery semantics and driver-specific behavior. Creation accepts caller-selected identity metadata, defaulting per instance, but never stores or publishes real address-like data in this corpus.

## Gaps and qualification boundaries

The actual retail Pro product metadata, exact initialization requirements, calibration persistence, charge/battery variants, output effects and timings, host reconnection, and Bluetooth-radio behavior need separate owner-authorized validation. A physical gap that requires firmware investigation is **needs private analysis** and must not be pursued here. The absence of a local host/controller means no consumer-acceptance or device-fidelity promotion. Dolphin's Pro-specific path is an **open unknown**, not inferred from its Wiimote support.

## Proposed tests — **not run**

1. On an authorized Linux host, create a Bluetooth-bus UHID Pro candidate with caller-controlled, non-published identity metadata. Observe which HID driver binds and inspect the distinct Pro input node, parent, evdev keys/axis ioctl limits, LED sysfs, power supply and `pro_calib` interface; fail if no driver bind.
2. Send neutral and boundary report 0x3d samples and verify both Linux events and report-mode requests, active-low buttons, 12-bit stick ordering and first-packet calibration behavior; close/recreate and test concurrent instances.
3. With reviewed SDL HIDAPI enabled, verify Pro name, 15 buttons, four stick axes plus ZL/ZR trigger axes, charging classification, LED and rumble responses. Test missing or invalid extension IDs as negative controls.
4. Probe Cemu's native Wiimote entrypoint as an **expected exclusion**; separately examine Cemu's generic gamepad path and Dolphin's joystick bindings only after obtaining independent pinned code for those paths.
5. Measure creation, cleanup, repeated pairing/reconnect expectations and failure rollback separately. Real Bluetooth over-the-air discovery/pairing needs a distinct radio-backed provider and authorized hardware evidence; UHID alone cannot establish it.

## Claim inventory

- `wiiupro-pa2-kernel-bluetooth-match`
- `wiiupro-pa2-kernel-pro-classification`
- `wiiupro-pa2-kernel-pro-mode`
- `wiiupro-pa2-kernel-pro-input`
- `wiiupro-pa2-kernel-pro-stick-calibration`
- `wiiupro-pa2-kernel-pro-output-power`
- `wiiupro-pa2-sdl-pro-detection`
- `wiiupro-pa2-sdl-pro-report`
- `wiiupro-pa2-sdl-pro-mapping`
- `wiiupro-pa2-sdl-pro-power`
- `wiiupro-pa2-cemu-native-pro-exclusion`
- `wiiupro-pa2-separate-family-shared-code`
- `wiiupro-pa2-first-uhid-bluetooth`
- `wiiupro-pa2-physical-identity-gap`
- `wiiupro-pa2-physical-calibration-gap`
- `wiiupro-pa2-virtual-acceptance-gap`
