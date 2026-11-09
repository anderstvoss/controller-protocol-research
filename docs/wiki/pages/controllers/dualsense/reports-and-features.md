# DualSense — USB, Bluetooth, feature reports

[← DualSense overview](index.md) · [Control fields](controls-and-sensors.md)

> **Evidence snapshot:** corpus `ab74f662…` (2026-11-09); source-only versus physical and device versus consumer evidence are kept distinct.

## Input report roles

| Transport | Source-described path | Evidence / limit |
| --- | --- | --- |
| USB | Input `0x01`, **64 wire bytes** including ID | Device-side community mapping [`ds-l0-device-usb01-full-fields`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-usb01-full-fields.json); Linux parser [`ds-l0-kernel-usb-bt-input-shape`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-kernel-usb-bt-input-shape.json) |
| Bluetooth | Enhanced input `0x31`, **78 wire bytes** with transport framing and CRC | Linux/SDL source expectation only for the stated revision; physical BT session not included [`ds-l0-kernel-usb-bt-input-shape`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-kernel-usb-bt-input-shape.json) |
| Other/simple | Consumer fallback and enhanced-mode gating vary | Do not assume a 0x31 layout without negotiated mode and consumer selection [`ds-l0-sdl-input-and-sensor-modes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-sdl-input-and-sensor-modes.json) |

The USB full-state report includes sticks, triggers, hat/buttons, signed IMU samples, timestamps, two touch contacts and status fields. The report ID **is part of the wire count**; avoid shifting all field offsets when calling into HIDAPI, which may distinguish body and report-ID bytes. [`ds-l0-device-usb01-full-fields`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-usb01-full-fields.json).

## Output path is transport-specific

USB commonly uses output `0x02`; Bluetooth output `0x31` has a transport prefix and CRC under the inspected SDL/Linux policies. Both carry versions of a common effect block. Treat Bluetooth output header and CRC as separate protocol logic rather than assuming only the report ID differs: [`ds-l0-device-usb02-valid-flags`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-usb02-valid-flags.json), [`ds-l0-kernel-output-usb-bt`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-kernel-output-usb-bt.json), [`ds-l0-sdl-output-transport`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-sdl-output-transport.json).

## Feature reports that matter to host initialization

| Feature | Shape from source | Why the consumer asks |
| --- | --- | --- |
| `0x05` | 41-byte calibration reply | Gyro/accelerometer bias and sensitivity estimation [`ds-l0-device-feature05-shape`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-feature05-shape.json) |
| `0x09` | 20-byte device/pairing identity shape | Host identity; never publish a device's actual pairing identifiers [`ds-l0-device-feature09-identity-shape`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-feature09-identity-shape.json) |
| `0x20` | 64-byte firmware/version shape | Firmware/feature-version-dependent rumble policy [`ds-l0-device-feature20-firmware-shape`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-feature20-firmware-shape.json) |
| `0x03` | SDL third-party capabilities path in selected conditions | **No evidence** that the exact OpenPuck synthetic reply is required for a Sony-identified retail DualSense [`ds-l0-consumer-feature03-capabilities`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-consumer-feature03-capabilities.json) |

**Important disagreement:** SDL at its pinned revision uses LE16 feature-version cutoff `0x0224` in rumble selection, while Linux has a different version policy. A fixed synthetic firmware response is **compatibility configuration**, not measured Sony firmware: [`ds-l0-consumer-firmware0224-branch`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-consumer-firmware0224-branch.json). If feature GET fails, Linux and SDL have different calibration fallback/attach conditions ([`ds-l0-sdl-calibration-fallback`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-sdl-calibration-fallback.json)).

## Implementer checklist

Capture the chosen HIDAPI backend, initial/short/malformed GET handling, exact report ID/length and effect-valid bits, teardown, and USB/BT profiles **separately**. Do not copy model-specific identities into public fixtures. See [source pin and offset citations](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/dualsense-citation-map.md).
