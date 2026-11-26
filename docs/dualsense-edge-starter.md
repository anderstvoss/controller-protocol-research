# DualSense Edge — post-Alpha 2 starter research

| Decision | Pinned source finding | Decision / evidence limit |
| --- | --- | --- |
| Identity | Sony DualSense Edge uses the distinct Edge product selector (reported as PID `0x0df2` in existing `dsedge-l0-consumer-identity-separation`); standard DualSense is PID `0x0ce6`. Linux v7.3 matches Edge on both HID buses ([K](https://github.com/torvalds/linux/blob/v7.3/drivers/hid/hid-playstation.c#L2937-L2958)). | **Distinct controller-owned variant/package**, reusing DualSense framing, not extra controls on the standard DualSense API. Identity is software-source evidence. |
| Kernel driver and evdev | Linux **v7.3** `hid-playstation` sets `is_edge`, advertises four `EV_KEY` capabilities, and emits `BTN_TRIGGER_HAPPY1` / `2` (Fn1 / Fn2), `3` / `4` (left / right paddle) ([K](https://github.com/torvalds/linux/blob/v7.3/drivers/hid/hid-playstation.c#L1499-L1508), [K](https://github.com/torvalds/linux/blob/v7.3/drivers/hid/hid-playstation.c#L1804-L1834)). Common controls include `BTN_SOUTH/EAST/WEST/NORTH`, `BTN_MODE`, two stick axes each, analog triggers and D-pad hat ([K](https://github.com/torvalds/linux/blob/v7.3/drivers/hid/hid-playstation.c#L1472-L1497)). | These are **declared/emitted in source**, not verified event delivery on a host; distribution kernel/backports may differ. |
| SDL driver and mapping | Pinned SDL PS5 HIDAPI source at `535d80badefc83c5c527ec5748f2a20d6a9310fe` creates **17** raw joystick buttons for Edge and decodes left/right Fn, left/right paddle in slots **13/14/15/16** ([S](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps5.c#L52-L60), [S](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps5.c#L941-L950), [S](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps5.c#L1273-L1282)). Its generated default Gamepad map is `paddle1:b16,paddle2:b15,paddle3:b14,paddle4:b13` ([G](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/SDL_gamepad.c#L817-L824)). | Mapping means right paddle, left paddle, right Fn, left Fn respectively; default mapping is **not** proof of live evdev events or an active user mapping. |
| USB versus Bluetooth | Linux v7.3 consumes USB full input `0x01` (64 bytes), versus Bluetooth full input `0x31` (78 bytes with CRC). Both reach the same Edge-aware parser. USB output `0x02` (63 bytes) differs from Bluetooth output `0x31` (78 bytes, CRC) ([K](https://github.com/torvalds/linux/blob/v7.3/drivers/hid/hid-playstation.c#L81-L95), [K](https://github.com/torvalds/linux/blob/v7.3/drivers/hid/hid-playstation.c#L1251-L1288), [K](https://github.com/torvalds/linux/blob/v7.3/drivers/hid/hid-playstation.c#L1436-L1469)). | Transport framing differs; no physical transport-specific behavior has been measured. |
| Difference from standard DualSense | Product selection gates four Edge-only keys; Edge opts into compatible vibration v2 without the base model's firmware-version condition ([K](https://github.com/torvalds/linux/blob/v7.3/drivers/hid/hid-playstation.c#L1796-L1810)). Inspected kernel output worker uses shared rumble/LED/mic paths ([K](https://github.com/torvalds/linux/blob/v7.3/drivers/hid/hid-playstation.c#L1322-L1428)). | Kernel source has **no Edge-specific profile handler** in this file. That does not establish absence of a native profile protocol. |
| First realization | **Propose `linux.uhid.bluetooth`**, with a distinct Edge identity and descriptor, shared DualSense Bluetooth codec and a typed four-control extension. Then `linux.uhid.usb` using its separate framing; `linux.uinput` can provide an evdev-only compatibility shape. | HID-family consumer path is preferable to evdev-only for report-aware SDL/Linux, but **unvalidated**. UHID Bluetooth metadata does not provide pairing/radio. |
| Playable vs faithful | Playable: ordinary controls plus independent Fn/paddle events where a selected kernel/backend supports them. Faithful: exact native descriptors and reports, identity and firmware features, profile/remap semantics, output and lifecycle. | Do **not** claim faithful Edge or output/profile parity from base DualSense. uinput cannot answer native HID feature requests. |
| Open unknowns | Actual host binding and SDL backend; physical USB/BT descriptor/packet layouts; firmware/version-specific reports; profile and remap transitions; audio and advanced output behavior. | Source-only, no hardware or host test. See ledger and proposed tests below. |

## Decision rationale

The newer, pinned Linux v7.3 implementation resolves the **source-level** evdev code mapping that earlier corpus claim `dualsense-kernel-aux-parser` could not establish: `FN1 → BTN_TRIGGER_HAPPY1`, `FN2 → BTN_TRIGGER_HAPPY2`, `left paddle → BTN_TRIGGER_HAPPY3`, and `right paddle → BTN_TRIGGER_HAPPY4`. The existing `edge-linux-exposure-unknown` still correctly describes **missing runtime observation**, so it is **not edited or superseded**. Do not confuse the Linux codes with SDL's independent joystick slots or with the order of SDL's standardized Gamepad mapping.

Treat Edge as a **separately curated DualSense variant/package** with shared framing and a typed Edge-specific control surface. The independent Edge identity must be selectable at creation; the standard DualSense's 13-control surface stays intact. Use target restrictions for unavailable Fn/paddles on older kernels or backends rather than fabricated keys, silent aliases, or any GIP emulation.

For the first implementation experiment, `linux.uhid.bluetooth` exercises the native HID consumer path and common state parser with four new bits while retaining Bluetooth report framing/CRC. This is a conditional priority, not a claim of a passing host or paired device. A USB-bus UHID path is an independent second target and may have easier report debugging; a reduced `linux.uinput` profile can expose the four Linux v7.3 keys but cannot impersonate the HID feature/output surface. Track all three separately.

## Evidence ledger (new items)

| Claim ID | Evidence | Interpretation |
| --- | --- | --- |
| `edge-pa2-kernel-identity-buses` | Linux v7.3 source | Edge HID USB/BT matching, Edge-only capability registration |
| `edge-pa2-kernel-extra-evdev` | Linux v7.3 source | Four exact Fn/paddle `EV_KEY` mappings |
| `edge-pa2-kernel-usb-bt-framing` | Linux v7.3 source | Distinct USB and BT report IDs, lengths, and CRC policies |
| `edge-pa2-kernel-output-boundary` | Linux v7.3 source | Shared output implementation; no Edge-profile path observed in file |
| `edge-pa2-kernel-revision-difference` | Earlier pinned Linux source and v7.3 | Old parser limitation must not be universalized |
| `edge-pa2-first-realization` | Inference from pinned consumers | Bluetooth-bus UHID first; unverified |
| `edge-pa2-backend-acceptance-unknown` | No host test | Live kernel/SDL acceptance open |
| `edge-pa2-native-profiles-unknown` | No device evidence | Profiles/remap and Edge reports open |
| `edge-pa2-physical-fidelity-unknown` | No physical evidence | Descriptor/firmware/protocol fidelity open |

The existing `edge-independent-raw`, `edge-sdl-decoder`, `edge-sdl-default-mapping`, `dsedge-l0-consumer-identity-separation`, `edge-linux-exposure-unknown`, and `edge-physical-corroboration-unknown` are reused without modifying their records. All new `source_supported` claims have `evidence_role: consumer`; **device evidence remains "Evidence in progress"**, so no registry category test update is needed. Detailed provenance is in [the Edge ledger](ledgers/dualsense-edge-l0.md).

## Proposed tests — not run

1. On owner-controlled Linux v7.3 and a chosen older baseline, record sanitized driver binding, `EV_KEY` capabilities and separate Fn/paddle press/release transitions for an Edge virtual HID node; repeat for USB-bus and Bluetooth-bus UHID.
2. Exercise SDL at the pinned revision with selected HIDAPI and Linux-event backends, recording 17-button raw joystick visibility versus standardized Gamepad four auxiliary positions, including configuration/user overrides.
3. Probe valid/invalid HID feature replies, idle/neutral input, transport CRC, re-enumeration and teardown; require source-backed outputs and never manufacture profile reports.
4. With separately authorized physical evidence, compare exact Edge identity, descriptor and independent controls under multiple profile/remap states over USB and Bluetooth without publishing identifiers or private captures.
5. Verify `linux.uinput` reduced evdev restrictions and `linux.uhid.usb` report-path parity independently; include negative cases for unavailable controls.

**All tests above are proposals, not results. No host/hardware executions or firmware analysis were performed.**
