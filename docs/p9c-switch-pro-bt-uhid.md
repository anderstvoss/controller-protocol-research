# Switch Pro Bluetooth-bus UHID source gap checkpoint (p9c)

**Scope:** local `linux.uhid.bluetooth` with Bluetooth-bus metadata, not a Bluetooth radio, discovery, pairing, BlueZ or transport validation. Research is limited to pinned Linux/SDL consumer code and pinned community notes. No host or physical device was used. All proposed lab tests below are **not run**.

## Ranked gaps (source-evidence ceiling)

| Rank | Gap | Playable or faithful | Evidence ceiling | Claim ID |
| --- | --- | --- | --- | --- |
| 1 | Bluetooth startup, excluding USB-only proprietary handshake | Playable | Source-only Linux/SDL consumer | `swpro-bt-consumer-open-gate` |
| 2 | Simple-mode input before full-report selection | Playable | Community research lead; no physical capture | `swpro-bt-simple-report-mode` |
| 3 | Simple-mode signed stick semantics and 0x8000 neutral code | Playable | Pinned SDL consumer parser, no physical capture | `swpro-bt-simple-axis-neutral` |
| 4 | Subcommand/rumble output and synchronous reply framing | Playable | Linux/SDL consumer plus community lead | `swpro-bt-subcommand-report-framing` |
| 5 | Full-mode battery, connection, controls and IMU layout | Playable | Linux consumer plus community lead | `swpro-bt-full-mode-input-layout` |
| 6 | Consumer-requested LEDs, IMU, vibration and SPI read replies | Playable | Source-only consumer | `swpro-bt-consumer-reply-coverage` |
| 7 | Exact retail Bluetooth SDP/report descriptor and transport behavior | Faithful | Unknown; needs physical capture | `swpro-bt-retail-descriptor-unknown` |
| 8 | Switch Pro-specific NFC/IR MCU exchange and failure semantics | Faithful | Unknown; family notes alone insufficient | `swpro-bt-pro-nfc-exchange-unknown` |

## Pinned evidence

- Linux hid-nintendo [`4056b3c`](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-nintendo.c#L2477-L2637): Bluetooth transport bypasses the USB-only proprietary handshake, then requests device information, calibration, mode, IMU and vibration.
- SDL Switch HIDAPI [`535d80b`](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_switch.c#L629-L685): Bluetooth queries device info via subcommand and avoids USB-only setup at open. The [simple input struct and calibrator](https://github.com/libsdl-org/SDL/blob/535d80badefc83c5c527ec5748f2a20d6a9310fe/src/joystick/hidapi/SDL_hidapi_switch.c#L1107-L1122) use the raw neutral stick code 0x8000, not zero.
- Community Bluetooth HID notes [`b354f21`](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/b354f21ae81f7b0d1d060b2b61e66ad0d9bc1756/bluetooth_hid_notes.md#L3-L25) and [report layouts](https://github.com/dekuNukem/Nintendo_Switch_Reverse_Engineering/blob/b354f21ae81f7b0d1d060b2b61e66ad0d9bc1756/bluetooth_hid_notes.md#L110-L181) are research leads, not retail captures.

## Scope boundaries

The local UHID identity and descriptor are an emulation interface, not proof of retail SDP bytes. No vendor firmware analysis, physical observations or connection/radio assertions are made. The USB SPI map may be reused semantically; per-device private content is out of scope. Bluetooth-only NFC/MCU modes are explicitly restricted until a Pro-specific exchange is supported by evidence. Proposed hardware comparison and host checks: **not run**.
