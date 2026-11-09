# Nintendo Switch Joy-Con (R)

> Reviewed corpus revision: `ab74f662…` (2026-11-09). Most Switch 1 claims below are **source-only**, not physical captures.

**Registry:** [Joy-Con (R)](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/switch-joycon-right.json), parent [Switch 1 family](../switch-joycon-family/index.md). Native Bluetooth-facing identity is typically `057e:2007`; pinned source device-info type byte `0x02`. [`joycon-a-device-info-type`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-device-info-type.json).

## Right-half-specific controls

This half supplies A/B/X/Y, R/ZR, SL/SR rail buttons, right stick/IMU and the **Home LED**. Linux and SDL can expose different per-half mappings; source code negates Y/Z of the right IMU for a common consumer coordinate convention, without asserting that raw right gyro uses the normalized sign. [`joycon-a-home-led-and-rail-buttons`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-home-led-and-rail-buttons.json), [`joycon-a-right-imu-signs`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-right-imu-signs.json).

## NFC and IR are independent MCU functions

Right Joy-Con's IR camera and NFC controller do not emerge automatically from a standard `0x30` gamepad stream. Their state, reset, report mode `0x31`, output `0x11`, fragment retries and target transitions require a separate codec and lifecycle. See [family MCU chapter](../switch-joycon-family/protocol-and-mcu.md) and [`joycon-b-nfc-state-machine`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-b-nfc-state-machine.json) / [`joycon-b-ir-image-ack-retry`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-b-ir-image-ack-retry.json).

## Qualification

Test right-specific control/LED behavior, right-stick/IMU mapping, a real or safely emulated MCU handshake, bounded infrared data fragments and reconnect. **No physical right-half or NFC/IR capture is asserted**; do not use user NFC tag dumps as corpus fixtures.
