# Joy-Con — native HID, calibration, right-side MCU

[← Joy-Con family](index.md) · [Pairing and host selection](pairing-and-consumers.md)

> Reviewed corpus revision: `ab74f662…` (2026-11-09). Most Switch 1 claims below are **source-only**, not physical captures.

## Common report structure with side-specific meaning

| Report | Source-described use |
| --- | --- |
| `0x3F` | Simple state report with button/hat and Joy-Con filler |
| `0x30` | Full state: battery, buttons, two packed stick slots, vibration field and three IMU samples |
| `0x21` | Subcommand ACK + response |
| `0x01` | Rumble/subcommand request |
| `0x10` | Rumble-only |
| `0x31` | MCU-extended input (when enabled, right-side NFC/IR contexts) |
| `0x11` | MCU request/output envelope |

Citations: [`joycon-a-full-report-per-side`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-full-report-per-side.json), [`joycon-a-simple-report-joycon`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-simple-report-joycon.json), [`joycon-a-subcommand-matrix`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-subcommand-matrix.json).

A full `0x30` report includes **left and right 12-bit stick slots**, even for a single half; what a compatibility emulator populates in the absent half is its own policy, not a native hardware measurement. Linux's right-half IMU Y/Z sign inversions are a **consumer coordinate transformation**, not proof of native right sensor polarity: [`joycon-a-right-imu-signs`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-right-imu-signs.json).

## Calibration and configuration

The shared `0x02` device-info, `0x03` report-mode, `0x10` SPI read, `0x30` player LED, `0x40` IMU, `0x48` vibration, and MCU `0x20`–`0x22` subcommand families are source-described. Factory/user stick calibration areas differ by half; byte/marker interpretations must respect side. See [`joycon-a-device-info-type`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-device-info-type.json), [`joycon-a-calibration-per-side`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-calibration-per-side.json), [`joycon-a-subcommand-matrix`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-subcommand-matrix.json).

Rumble envelopes still reserve **eight bytes** for both motor slots even though one half has only its own physical actuator. Encoding both slots is not evidence one half actuates another half: [`joycon-a-rumble-slot-framing`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-rumble-slot-framing.json).

## Right-half NFC/IR MCU

The right Joy-Con has a separate MCU state machine beyond ordinary buttons/gyro:
- Select report mode `0x31` using regular `0x03` subcommand.
- Power/configure MCU through `0x20`, `0x21`, `0x22`.
- Use output `0x11` for MCU requests; reports append MCU content after the normal state/IMU prefix.
- IR image transfer is fragmented; mode/register setup and missing/out-of-order-fragment ACKs are meaningful.
- NFC requires a target detection/read/write state machine; *no tag bytes, keys or identity data* are included.

Source-only MCU records: [`joycon-b-mcu-config-state-sequence`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-b-mcu-config-state-sequence.json), [`joycon-b-mcu-mode-and-prefix`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-b-mcu-mode-and-prefix.json), [`joycon-b-ir-image-ack-retry`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-b-ir-image-ack-retry.json), [`joycon-b-nfc-state-machine`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-b-nfc-state-machine.json). **No physical right-half NFC/IR experiment** is claimed. [MCU protocol ledger](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/switch-joycon-mcu-l0.md).

## Physical gaps

No connected Joy-Con lab result exists at this source stage. Full Bluetooth discovery/pairing, exact independent HID descriptors, real MCU timings and actuator responses require controlled references. Do not elevate compatible emulator code such as joycontrol/nxbt to physical proof.
