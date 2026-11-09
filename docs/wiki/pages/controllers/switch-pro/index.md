# Nintendo Switch Pro Controller (Switch 1)

> Reviewed corpus revision: `ab74f662…` (2026-11-09). Most Switch 1 claims below are **source-only**, not physical captures.

**Registry:** [Switch Pro](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/switch-pro.json). This is not [Switch 2 Pro](../switch2-pro/index.md) and must not inherit its new consumer decoder or Bluetooth interface.

## Pages

- [USB/BT commands, reports and subcommands](protocol.md)
- [Calibration, IMU, HD rumble and host consumers](calibration-and-consumers.md)
- [Physical validation and emulation boundaries](validation.md)

## What sources establish

The corpus draws on pinned Linux `hid-nintendo`, SDL3 Switch HIDAPI, independent dekuNukem community notes and OpenPuck compatibility code. Their evidence roles are not interchangeable. USB initialization uses command `0x80` / response `0x81`, while the controller's state/rumble/feature exchanges also use subcommand output `0x01` and input response `0x21`. Full state with IMU commonly uses `0x30`; `0x3F` is a simpler input mode: [`swpro-l0-linux-usb-handshake`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-linux-usb-handshake.json), [`swpro-l0-device-report30-full`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-report30-full.json).

**Unknown:** exact retail physical USB configuration, firmware-specific calibration, the Pro's definitive physical USB report period and motor transfer function remain unmeasured. In particular, source estimates of ~60/120 Hz and a 4-ms OpenPuck scheduler are **not** a validated retail USB rate: [`swpro-l0-device-usb-cadence-conflict`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-usb-cadence-conflict.json), [`swpro-l0-device-physical-usb-period-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-physical-usb-period-unknown.json).

Study [Switch Pro L0 ledger](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/switch-pro-l0.md) and [compatibility/faithfulness decisions](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/switch-pro-decision-table.md).
