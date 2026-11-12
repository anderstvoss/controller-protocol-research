# Sony DualSense

> **Evidence snapshot:** corpus `ab74f662…` (2026-11-09); source-only versus physical and device versus consumer evidence are kept distinct.

**Registry:** [DualSense](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/dualsense.json), within the [DualSense family](../sony-dualsense-family/index.md). The [Edge](../dualsense-edge/index.md) is separately registered and cannot be treated as this model merely because most reports are similar.

## Pages

- [USB/Bluetooth report and feature contract](reports-and-features.md)
- [Controls, touch, motion and calibration](controls-and-sensors.md)
- [Output, adaptive triggers, LEDs and audio](outputs-and-audio.md)
- [Linux/SDL/Steam consumer acceptance and lab gates](consumers-and-validation.md)

## Overview

Community protocol documents, pinned Linux `hid-playstation`, SDL PS5 HIDAPI and HHD compatible-device implementations describe USB `0x01` input, Bluetooth enhanced `0x31`, selected output and calibration/identity/version features. Those views have **different evidence roles**: community source descriptions can support a device report hypothesis; Linux/SDL code defines *consumer expectations*; HHD is evidence of a compatible synthetic implementation, not Sony firmware. See [`ds-l0-device-usb01-full-fields`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-usb01-full-fields.json), [`ds-l0-kernel-usb-bt-input-shape`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-kernel-usb-bt-input-shape.json) and [`ds-l0-hhd-uhid-identity`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-hhd-uhid-identity.json).

A small maintainer-reported physical USB investigation and historical virtual-host tests exist, but their conditions do not certify all fields, physical adaptive trigger performance, Bluetooth transport or Steam gyro acceptance. The known `dummy_hcd` versus UHID Steam gyro contrast has an **inferred cause only**: [`ds-l0-dummy-hcd-steam-gyro-contrast`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-dummy-hcd-steam-gyro-contrast.json), [`ds-l0-uhid-gyro-association-hypothesis`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-uhid-gyro-association-hypothesis.json).

## Important separations

- **USB versus Bluetooth:** headers, output, report length and checksum differ.
- **Native hardware versus evdev/SDL:** axis scaling, touch normalization and sensor exposure are host policy.
- **Input versus outputs:** recognizing sticks does not prove LED, motor, audio, trigger or reverse-feature handling.
- **Calibration:** synthetic 0x05 replies may satisfy a parser but cannot impersonate an unknown retail factory calibration.

**Research source:** [DualSense L0 ledger](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/dualsense-l0.md), [compatibility versus fidelity decisions](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/dualsense-decision-table.md).
