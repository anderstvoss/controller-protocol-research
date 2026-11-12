# Nintendo Switch Pro Controller (Switch 1)

> Reviewed corpus revision: `ab74f662…` (2026-11-09). Most Switch 1 claims below are **source-only**, not physical captures.

**Registry:** [Switch Pro](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/switch-pro.json). This is not [Switch 2 Pro](../switch2-pro/index.md) and must not inherit its new consumer decoder or Bluetooth interface.

## Pages

- [USB/BT commands, reports and subcommands](protocol.md)
- [Calibration, IMU, HD rumble and host consumers](calibration-and-consumers.md)
- [Physical validation and emulation boundaries](validation.md)
- [Independent HOME-button illumination and NFC/MCU limits](home-light-and-nfc.md) — source-only additions.

## What sources establish

The corpus draws on pinned Linux `hid-nintendo`, SDL3 Switch HIDAPI, independent dekuNukem community notes and OpenPuck compatibility code. Their evidence roles are not interchangeable. USB initialization uses command `0x80` / response `0x81`, while the controller's state/rumble/feature exchanges also use subcommand output `0x01` and input response `0x21`. Full state with IMU commonly uses `0x30`; `0x3F` is a simpler input mode: [`swpro-l0-linux-usb-handshake`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-linux-usb-handshake.json), [`swpro-l0-device-report30-full`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-report30-full.json).

**Unknown:** exact retail physical USB configuration, firmware-specific calibration, the Pro's definitive physical USB report period and motor transfer function remain unmeasured. In particular, source estimates of ~60/120 Hz and a 4-ms OpenPuck scheduler are **not** a validated retail USB rate: [`swpro-l0-device-usb-cadence-conflict`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-usb-cadence-conflict.json), [`swpro-l0-device-physical-usb-period-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-physical-usb-period-unknown.json).

Study [Switch Pro L0 ledger](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/switch-pro-l0.md) and [compatibility/faithfulness decisions](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/switch-pro-decision-table.md).

## Two independent output boundaries, added November 10

Linux's HOME LED class output uses subcommand `0x38` and must **not** be counted as a fifth physical player indicator. Player light count remains four. The existing source-only NFC/MCU family notes mention `0x11/0x31`, but a wired USB realization need not invent Pro NFC functionality; product documentation explicitly restricts NFC while Pro Controller Wired Communication is active. Both questions are detailed in [HOME light and NFC/MCU](home-light-and-nfc.md). [`swpro-cgap-home-led-consumer`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/swpro-cgap-home-led-consumer.json), [`swpro-cgap-nfc-mcu-family-context`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/swpro-cgap-nfc-mcu-family-context.json).
