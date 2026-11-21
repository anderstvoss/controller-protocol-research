# DualShock 4 Bluetooth-bus UHID — source-only gap check (p9b)

| Rank | Gap | Goal | Evidence ceiling | New claim ID |
| --- | --- | --- | --- | --- |
| 1 | Minimal/full input framing, CRC, motion/touch offsets | playable | pinned Linux/SDL consumer implementation only | `ds4-bt-consumer-input-envelope` |
| 2 | Output rumble, RGB, blink masks and CRC | playable | pinned Linux/SDL consumer implementation only | `ds4-bt-consumer-output-effects` |
| 3 | Calibration and feature-report requests on open | playable | pinned Linux/SDL consumer requests; data content unknown | `ds4-bt-consumer-calibration-open` |
| 4 | Per-instance identity and transport gating | playable | pinned Linux/SDL consumer routing only | `ds4-bt-consumer-identity-uniq` |
| 5 | Exact retail BT HID descriptor, pairing, physical transition and timing | faithful | **unknown**; owner-authorized physical evidence needed | none |

**Scope:** no host, no real controller, no Bluetooth radio/BlueZ/pairing, no private firmware work, no captured packets. Proposed test cases below are **not run**. `linux.uhid.bluetooth` is a local HID node advertised on Bluetooth bus 5, not an over-the-air emulation.

## Sources and exact gaps

- [Linux DS4 input layouts](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L335-L539) and [CRC/input decoder](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L2389-L2454): Bluetooth 0x01 is 10 bytes and full 0x11 is 78, with two extra leading bytes, up to four touch samples and trailing input CRC. [SDL PS4 full-mode routing](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps4.c#L1166-L1243) accepts additional 0x11–0x19 IDs and conditionally tolerates bad input CRC; strict CRC in our synthetic output is a conservative choice, not proof of device behavior.
- [Linux output semantics](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L507-L539), [output worker/CRC](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L2277-L2386), [SDL output](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps4.c#L924-L973): report 0x11 is 78 bytes, carries validity flags for motors/LED/blink and an output CRC. Host output formatting cannot establish device actuation, including blink timing.
- [Linux calibration](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L1938-L2033) and [probe](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L2784-L2805): Bluetooth feature 0x05/41 bytes with CRC checking; firmware 0xA3 failure is nonfatal. [SDL official calibration path](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps4.c#L462-L647) reads 0x02 then 0x05 and falls back on invalid calibration. No per-device calibration bytes were measured.
- [Linux transport identity](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L2148-L2181): Bluetooth derives its identity from UHID uniq, whereas USB asks for 0x12. [SDL USB preference](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps4.c#L442-L454) is an application/host policy; don't build implicit USB fallback into virtualgamepad.

These claims are `evidence_role: consumer` and `transport: source_only`. Existing `ds4-l0-device-bt01-11-input-modes` and `ds4-l0-device-bt11-output` cite a community protocol summary. That secondary source is a research lead, **not** a physical observation. This brief does not promote either existing claim or acceptance status.

## Unresolved faithful-device questions

Exact Bluetooth HID descriptor identity and revision mapping, on-air state changes, per-device feature contents, real touch history cadence, output acceptance, audible output and physical timing are **unknown**. Bluetooth audio is out of scope. Any question requiring vendor firmware inspection is **needs private analysis**; do not conduct it in this public research.

## Proposed validation (not run)

Test synthetic neutral 0x01/10 and 0x11/78 input encodings, valid CRC and corrupt CRC, offsets for buttons, touch, battery and IMU, and mode change following supported feature access. Decode synthetic 0x11 output including blink and reject malformed CRC; keep USB 0x05 unchanged. Exercise feature 0x02/0x05/0xA3, distinct caller-provided identities, neutral first report, explicit selection only and Bluetooth audio restriction. Real enumeration, SDL/Steam validation and measured latency remain P5b local-host work.
