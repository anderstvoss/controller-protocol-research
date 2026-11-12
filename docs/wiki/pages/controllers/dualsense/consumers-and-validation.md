# DualSense — host acceptance, contention and verification

[← DualSense overview](index.md)

> **Evidence snapshot:** corpus `ab74f662…` (2026-11-09); source-only versus physical and device versus consumer evidence are kept distinct.

## Consumers differ

At the pinned Linux `hid-playstation` revision, host probe, calibration and multiple input/sensor nodes are kernel responsibilities. SDL PS5 HIDAPI can directly open hidraw, perform its own feature reads, expose touch and motion and send output; Steam and Wine may select still different routes. A supported VID/PID and matching SDL name are **not** proof of native report compatibility. See [`ds-l0-kernel-input-evdev`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-kernel-input-evdev.json), [`ds-l0-sdl-input-and-sensor-modes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-sdl-input-and-sensor-modes.json), [kernel/raw-application contention matrix](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/sony-consumer-contention.md).

HHD produces a compatible virtual DualSense using UHID, synthetic feature replies and scheduled sensor/touch packets. It is important compatibility evidence, **not** retail protocol validation: [`ds-l0-hhd-uhid-identity`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-hhd-uhid-identity.json), [`ds-l0-hhd-feature-replies`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-hhd-feature-replies.json).

## USB gadget versus UHID historical result

The corpus preserves a reported Steam gyro difference between a `dummy_hcd` virtual USB gadget and a UHID realization. The association with UHID bus/node topology is **inferred**, not a confirmed root cause. A proper differential trial must pin kernel/SDL/Steam versions and enumerate driver bindings, HID interface ancestry, hidraw/evdev/sensor ownership and permissions: [`ds-l0-dummy-hcd-steam-gyro-contrast`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-dummy-hcd-steam-gyro-contrast.json), [`ds-l0-uhid-gyro-association-hypothesis`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-uhid-gyro-association-hypothesis.json).

## Physical and consumer gates

1. Genuine reference USB descriptor/feature inventory and revision; redact private identifiers.
2. Separate USB and Bluetooth report/CRC/feature-response captures.
3. Same-host neutral and isolated control/touch/IMU tests, with explicit selected SDL backend.
4. Safe output LED/rumble/trigger tests and real audio interface routing.
5. Long-run open/close and concurrent/raw-app ownership tests with cleanup.
6. Repeat gadget-versus-UHID Steam gyro experiments with controlled virtual bus/USB differences.

Source-backed details: [L0 lab gates](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/dualsense-l0.md), [compatibility/fidelity and calibration policy](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/dualsense-decision-table.md).
