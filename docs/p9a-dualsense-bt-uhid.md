# DualSense Bluetooth-bus UHID — source gap pass (p9a)

## Ranked gaps

| Rank | Gap | Playable or faithful | Evidence ceiling | Claim ID |
| --- | --- | --- | --- | --- |
| 1 | Bluetooth descriptor/report IDs and simple-to-enhanced mode transition | Playable host probe and controls | Linux/SDL consumer source; no retail Bluetooth capture | `ds-l0-kernel-usb-bt-input-shape`; new claim pending |
| 2 | Bluetooth CRC32 seeds, report lengths and rejection policy | Playable host exchange | Linux/SDL consumer source only | new claim pending |
| 3 | Bluetooth feature replies and calibration handling at probe | Playable host probe | Linux/SDL consumer source only | `ds-l0-consumer-probe-feature-failure-tolerance`; new claim pending |
| 4 | Bluetooth output, LED and adaptive-trigger block offsets | Faithful report parsing, not actuator fidelity | Linux/SDL consumer source only | `ds-l0-led-bt31-offsets`; new claim pending |
| 5 | Retail descriptor fidelity, pairing, timing and actuation | Faithful physical-device behavior | Unknown; needs owner-controlled physical evidence | `ds-l0-physical-bt-protocol-unknown` |

## Scope

This is the local `linux.uhid.bluetooth` HID representation, not pairing, radio, BlueZ or `linux.btvirt.bluetooth`. All implementation tests derived from upstream consumers are synthetic, not host/device observations.

## Source anchors

- [Linux hid-playstation, pinned](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-playstation.c#L81-L95)
- [SDL DualSense HIDAPI, pinned](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_ps5.c#L297-L320)

## Execution boundary

Source-backed protocol shapes can guide a draft implementation; Bluetooth-specific host behavior is **not run**. Physical fidelity remains unknown. No vendor firmware or private controller data is used.
