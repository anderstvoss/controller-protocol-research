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

## Bounded virtual USB-bus host observations

P5a USB-bus UHID bound stock playstation and delivered four face-button transitions and stick endpoints via hidraw in an exact-path sweep despite broad diagnostics failing. Steam listing differed between attempts, so gyro availability remains inconclusive. The uinput comparison delivered the bounded event-node sweep and Steam listed it with sticks, individual triggers and a ping pulse/stop. SDL 3.4.20 was outside the diagnostic backend classifier; the privileged comparison stopped on the first sysfs write. Neither run qualifies radio, timing or retail fidelity. [`vg-p5a-stock-dualsense-linux-uhid-usb-bound-ed8065b4be2c`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-p5a-stock-dualsense-linux-uhid-usb-bound-ed8065b4be2c.json), [`vg-p5a-stock-dualsense-linux-uinput-bound-ed8065b4be2c`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-p5a-stock-dualsense-linux-uinput-bound-ed8065b4be2c.json).

## P5a follow-up timing and discovery

USB/IP N1/N3 runs created, appeared, became SDL-ready and removed all 50/150 slots; direct evdev opens initially failed in all slots. An ACL-wait repeat verified all stages in all slots. A separate stock USB-bus UHID discovery run logged Steam HIDAPI selection and SDL opened the owned hidraw path; isolated visible listing and motion were unavailable. Neither discovery nor lifecycle establishes physical fidelity. [`vg-p5a-followup-dualsense-usbip-timing`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-p5a-followup-dualsense-usbip-timing.json), [`vg-p5a-followup-dualsense-usb-uhid-discovery`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/vg-p5a-followup-dualsense-usb-uhid-discovery.json).
