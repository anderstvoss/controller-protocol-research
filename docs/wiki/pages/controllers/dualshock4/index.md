# Sony DualShock 4

> **Evidence snapshot:** corpus `ab74f662…` (2026-11-09); source-only versus physical and device versus consumer evidence are kept distinct.

**Registry:** [DualShock 4](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/dualshock4.json). This is a **separate controller family** from DualSense; report IDs, touch history, calibration and feature queries differ.

## Pages

- [USB/BT reports, feature replies, calibration](reports-and-features.md)
- [Touch history, host consumer behavior and lab plan](consumers-and-validation.md)

The inspected sources describe wired USB input `0x01` (64 bytes), simple versus enhanced Bluetooth input, output `0x05` USB / `0x11` Bluetooth, firmware and calibration features. These are primarily **source-only**, and the corpus explicitly does not hold a genuine DS4 reference capture for the detailed L0 study. OpenPuck and historic virtualgamepad runs are *compatibility evidence*, not an independent retail DS4 recording. [`ds4-l0-device-usb01-input`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-device-usb01-input.json), [`ds4-l0-device-bt01-11-input-modes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-device-bt01-11-input-modes.json).

Do not combine revisions `054c:05c4`, `054c:09cc` and wireless adapter `054c:0ba0` into a universal USB descriptor or firmware policy. [`ds4-l0-consumer-revision-and-dongle-routing`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-consumer-revision-and-dongle-routing.json).

Full source ledger: [DS4 L0 protocol/consumer ledger](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/dualshock4-l0.md); [compatibility versus faithful decisions](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/dualshock4-decision-table.md).
