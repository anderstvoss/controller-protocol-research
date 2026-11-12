# DualSense Edge L0 — post-Alpha 2 consumer-source ledger

**Scope:** `dualsense-edge`, tracking `anderstvoss/virtualgamepad#170`. This is new **source-only** evidence, not a hardware observation, SDL acceptance test or validated controller protocol. The earlier DualSense source ledger and Edge claims remain immutable.

## Pinned provenance

| Source record | Pinned file and revision | Locator / license | Scope |
| --- | --- | --- | --- |
| `edge-pa2-linux-v73-hid-playstation` | [Linux `v7.3` `hid-playstation.c`](https://github.com/torvalds/linux/blob/v7.3/drivers/hid/hid-playstation.c) | Lines 81–119, 1251–1320, 1322–1428, 1436–1508, 1737–1834, 2937–2958; GPL-2.0-or-later | Linux HID match, report/evdev/output consumer |
| `kernel` (existing) | [Earlier Linux pinned commit](https://github.com/torvalds/linux/blob/adc218676eef25575469234709c2d87185ca223a/drivers/hid/hid-playstation.c) | Parser; GPL-2.0-or-later | Historical auxiliary-bit contrast; no distribution inference |
| `sdl-ps5-baseline` (existing) | [SDL PS5 HIDAPI `535d80b`](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps5.c) | Lines 52–60, 941–950, 1273–1282; zlib | Raw Edge joystick slots and bit masks |
| `sdl-gamepad-baseline` (existing) | [SDL gamepad mapping `535d80b`](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/SDL_gamepad.c) | Lines 817–824; zlib | Generated Edge default Gamepad mapping |

Linux `v7.3` `hid-playstation.c` was retrieved as the exact pinned file and hashed SHA-256 `48a08dddf8d276a611195311a29cd4f113a949a1f5431ecc84b0396b106ec896`. The same byte hash exists under a different existing kernel commit source record; the new record is justified by the **requested tagged revision**, not a claim of different bytes or independent lineage. Neither a second pin nor SDL are independent physical corroboration.

## Consumer evidence and limits

| Claim | Status / role | Source result and boundary |
| --- | --- | --- |
| `edge-pa2-kernel-identity-buses` | source_supported / consumer | USB and Bluetooth Edge selectors use a shared DualSense driver and Edge-only capabilities |
| `edge-pa2-kernel-extra-evdev` | source_supported / consumer | Fn1 = `BTN_TRIGGER_HAPPY1`, Fn2 = `BTN_TRIGGER_HAPPY2`, left paddle = `BTN_TRIGGER_HAPPY3`, right paddle = `BTN_TRIGGER_HAPPY4` |
| `edge-pa2-kernel-usb-bt-framing` | source_supported / consumer | USB `0x01` input and `0x02` output versus Bluetooth `0x31` input/output with CRC |
| `edge-pa2-kernel-output-boundary` | source_supported / consumer | Shared rumble, LEDs and mic output; no Edge-specific profile branch in inspected file |
| `edge-pa2-kernel-revision-difference` | source_supported / consumer | Earlier kernel parser omits auxiliary evdev forwarding; v7.3 exposes it |
| `edge-pa2-first-realization` | inferred / consumer | Propose Bluetooth-bus UHID plus distinct typed Edge variant; not a passing host test |
| `edge-pa2-backend-acceptance-unknown` | unknown / consumer | Physical/virtual host bound driver and selected SDL backend not measured |
| `edge-pa2-native-profiles-unknown` | unknown / device | Profile selection, remap, native feature/output reports unresolved |
| `edge-pa2-physical-fidelity-unknown` | unknown / device | Physical descriptor, firmware, USB/BT packet details and acceptance unmeasured |

## Reconciliation with existing corpus

- `dsedge-l0-consumer-identity-separation` already tracks Edge versus standard DualSense software identity. New claims add tagged kernel and exact event-code resolution without changing old records.
- `edge-independent-raw`, `edge-sdl-decoder` and `edge-sdl-default-mapping` already cover SDL source-only raw and Gamepad mapping; no duplicate SDL claim is needed.
- `dualsense-kernel-aux-parser` reflects an earlier pinned Linux source, not the v7.3 code path; source evolution is not a contradiction about one revision.
- `edge-linux-exposure-unknown` and `edge-physical-corroboration-unknown` retain their valid **observational** limitations. Source-backed event registration resolves an implementation question, not a controlled host result.
- New records are consumer-only when `source_supported`; the controller's device category remains **Evidence in progress** and `tests/test_controller_registry.py` requires no modification.

## Design disposition and proposed tests, not run

Prefer a separate Edge package/variant with a shared DualSense wire codec and four independent native controls. Rank `linux.uhid.bluetooth` first for HID-driver compatibility, with independently qualified `linux.uhid.usb` and reduced `linux.uinput`; the first is a local UHID Bluetooth-bus representation, **not** radio or pairing.

**Not run:** check host driver binding and exact evdev code events on both UHID buses; compare SDL HIDAPI 17 raw buttons against default standardized mapping and evdev backend; perform negative feature/output and teardown cases; obtain owner-controlled physical validation before making descriptor, profile or firmware-specific claims. Do not run or publish vendor firmware analysis; a gap requiring it **needs private analysis**.
