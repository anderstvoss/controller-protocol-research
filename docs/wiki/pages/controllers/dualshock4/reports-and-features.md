# DualShock 4 — USB/BT framing and feature semantics

[← DS4 overview](index.md) · [Consumers and lab](consumers-and-validation.md)

> **Evidence snapshot:** corpus `ab74f662…` (2026-11-09); source-only versus physical and device versus consumer evidence are kept distinct.

| Role | Source-described format | Limitation |
| --- | --- | --- |
| USB full input | `0x01`, 64 wire bytes; sticks, buttons/hat, analog triggers, motion/timestamp, battery and touch history | Source-backed, not a physical per-revision trace: [`ds4-l0-device-usb01-input`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-device-usb01-input.json) |
| Bluetooth simple/full | Simple `0x01` (~10 bytes) versus enhanced `0x11` (78 bytes); shifted prefix and CRC32 on full reports | BT negotiation/CRC and physical pairing not tested: [`ds4-l0-device-bt01-11-input-modes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-device-bt01-11-input-modes.json) |
| USB output | `0x05`, 32 bytes with rumble/lightbar | Motor and LED physical response unvalidated: [`ds4-l0-device-usb05-output`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-device-usb05-output.json) |
| Bluetooth output | `0x11`, 78 bytes with transport header and CRC | Distinct from USB: [`ds4-l0-device-bt11-output`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-device-bt11-output.json) |

## Feature handling is version-dependent

- **Calibration:** USB feature `0x02` (37 bytes) versus Bluetooth feature `0x05` (41 bytes with CRC) in inspected drivers. The kernel and SDL have different default/fatal-failure policies. A synthetic calibration stub is not measured retail scale: [`ds4-l0-device-feature02-calibration-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-device-feature02-calibration-unknown.json), [`ds4-l0-consumer-kernel-calibration-fallback`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-consumer-kernel-calibration-fallback.json), [`ds4-l0-consumer-sdl-calibration-fallback`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-consumer-sdl-calibration-fallback.json).
- **Device identity:** current Linux USB feature `0x12` versus historical `hid-sony` feature `0x81`. This is a **consumer version difference**, not proof that every retail DS4 answers both: [`ds4-l0-consumer-kernel-pairing12`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-consumer-kernel-pairing12.json), [`ds4-l0-consumer-hidsony-feature81`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-consumer-hidsony-feature81.json).
- **Firmware:** feature `0xA3` request was a fatal gate in historical Linux `hid-sony` but is nonfatal in newer `hid-playstation`. That does not make fabricated all-zero firmware fields physically faithful: [`ds4-l0-consumer-hidsony-a3-probe-gate`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-consumer-hidsony-a3-probe-gate.json), [`ds4-l0-consumer-kernel-a3-optional`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-consumer-kernel-a3-optional.json).

## Report-level practical distinction

A host may first see a limited simple BT report and only later enable enhanced full input. Encoding USB `0x01` bytes inside the Bluetooth report envelope is not enough; offset shifts and CRC are protocol, and the consumer may select a different feature/initialization path. See [`ds4-l0-consumer-sdl-enhanced-switch`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-consumer-sdl-enhanced-switch.json).

Source pins: [`audio-sdl-ps4`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/source/audio-sdl-ps4.json), [`ds4-linux-hid-sony-v61`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/source/ds4-linux-hid-sony-v61.json).
