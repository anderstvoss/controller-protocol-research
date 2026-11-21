# DualSense Bluetooth-bus UHID — source gap pass (p9a)

## Ranked gaps

| Rank | Gap | Playable or faithful | Evidence ceiling | Claim ID |
| --- | --- | --- | --- | --- |
| 1 | Simple `0x01` versus enhanced `0x31` input and host mode switch | Playable controls and probe | Linux/SDL consumer code only | `ds-bt-consumer-input-modes` |
| 2 | Input/output/feature CRC seeds, framing and report lengths | Playable report acceptance | Linux/SDL consumer code only | `ds-bt-consumer-crc-contract` |
| 3 | Required Bluetooth feature replies on probe | Playable kernel initialization | Linux/SDL consumer code only; no private field contents | `ds-bt-consumer-feature-probe` |
| 4 | Bluetooth common payload offsets: output, touch, IMU and battery | Faithful *format*, not actuation | Linux/SDL consumer code only | `ds-bt-consumer-payload-offsets`; `ds-l0-led-bt31-offsets` |
| 5 | Exact retail Bluetooth HID descriptor bytes, physical mode transition, pairing/reconnect, timing and actuator response | Physical fidelity | **Unknown** without owner-controlled reference capture | `ds-l0-physical-bt-protocol-unknown` |

## Implementation decision

Target `linux.uhid.bluetooth` means a local Linux UHID device advertising Bluetooth bus metadata, **not** Bluetooth radio, BlueZ pairing or the deferred `linux.btvirt.bluetooth` work ([virtualgamepad #164](https://github.com/anderstvoss/virtualgamepad/issues/164)). Never treat `wip/btvirt` as protocol evidence.

- The [Linux DualSense parser](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L1436-L1477) expects full `0x31` Bluetooth input, 78 bytes with a Bluetooth prefix and CRC. The [SDL mode recognizer](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps5.c#L399-L416) also supports the short `0x01` state; [SDL effects transitions](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps5.c#L778-L843) can initiate enhanced mode. The source does **not** prove a universal retail mode-switch sequence.
- [Linux CRC validation](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L742-L751) uses seed `0xA1` for input, `0xA2` for output, `0xA3` for feature; the last four bytes hold little-endian CRC32. [Feature validation](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L799-L833) checks exact length, report ID and Bluetooth CRC. SDL's [Bluetooth output](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps5.c#L1044-L1068) uses an alternate header from Linux; do not require a single producer sequence/tag policy.
- [Linux probe](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L1783-L1820) requires successful `0x09`, `0x20` and `0x05` feature replies. This says nothing about a retail controller's identifying or calibration data, which must not be committed or invented. SDL's [feature handling](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps5.c#L418-L445) is more tolerant for enhanced devices.
- The [Linux common input/output shapes](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L244-L316) place enhanced Bluetooth input's 63-byte common body at byte 2 and output's 47-byte common body at byte 3. Existing `ds-l0-led-bt31-offsets` describes output LED positions; `ds-l0-kernel-usb-bt-input-shape` covers the shared input.
- A precise retail Bluetooth HID descriptor **is not established** by these two consumer source files. Do not silently copy the USB descriptor into a Bluetooth realization and claim fidelity. Use a separately pinned compatible descriptor with provenance or restrict the realization until one is available.

## Relationship to existing research

These four new `ds-bt-consumer-*` claims narrow the existing `ds-l0-kernel-usb-bt-input-shape`, `ds-l0-kernel-output-usb-bt`, `ds-l0-led-bt31-offsets`, `ds-l0-consumer-probe-feature-failure-tolerance` and `ds-l0-physical-bt-protocol-unknown` records without changing, superseding or promoting any. All new claims use `transport: source_only`, `evidence_role: consumer` and `experiments: []`.

## Qualification boundaries — not run

- Synthetic unit tests should cover descriptor report declarations, initial neutral input, mode switch, exact full input bytes/CRC, all feature-response lengths and CRCs, invalid host output CRC, full output decoding and separate per-instance identity.
- Linux host checks should establish the selected driver, feature/probe results, evdev/Sensor/SDL exposure, output routing, cleanup and independent instances (P5b). **Not run** in this cloud pass.
- Physical comparison, timings, pairing, radio and adaptive-trigger/heating/audio effects require owner-approved hardware observations. No reference-device run or firmware examination was performed.
