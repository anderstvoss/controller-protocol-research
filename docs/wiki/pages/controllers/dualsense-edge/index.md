# Sony DualSense Edge

> **Reviewed corpus:** 2026-11-09. A source parser, compatibility shim or virtual-host acceptance does not establish native physical hardware fidelity.

**Registry:** [DualSense Edge](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/dualsense-edge.json), a separate member of the [DualSense family](../sony-dualsense-family/index.md). The [base DualSense chapter](../dualsense/index.md) describes overlapping report structures, not automatically inherited Edge firmware or independent controls.

## What the pinned SDL source exposes

SDL PS5 HIDAPI at the pinned 3.2.0 revision decodes separate **left/right function** bits `0x10/0x20` and **left/right paddle** bits `0x40/0x80` from buttons byte 2. These are **consumer-source** decoder results, not a retail Edge capture: [`edge-independent-raw`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/edge-independent-raw.json), [`edge-sdl-decoder`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/edge-sdl-decoder.json).

The generated SDL **default mapping** uses `paddle1:b16,paddle2:b15,paddle3:b14,paddle4:b13`, corresponding in that decoder to right paddle, left paddle, right function and left function. This describes the default mapping rather than an observed active user mapping; user profiles can override it. [`edge-sdl-default-mapping`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/edge-sdl-default-mapping.json).

The Edge is separately recognized as Sony `054c:0df2` (versus base `054c:0ce6`) in inspected Linux/SDL source: [`dsedge-l0-consumer-identity-separation`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/dsedge-l0-consumer-identity-separation.json).

## Missing physical and Linux evidence

No exact Edge kernel/evdev exposure or controlled physical trace of those independent controls is established: [`edge-linux-exposure-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/edge-linux-exposure-unknown.json), [`edge-physical-corroboration-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/edge-physical-corroboration-unknown.json). Firmware, onboard profiles and transport settings may change which event reaches an application.

## Next tests

Use isolated extra-button presses under fixed firmware/transport; compare raw HID bits, SDL HIDAPI output, SDL mapping override, Linux evdev events and Steam Input. Check whether using controller-side reassignment changes independent report bits or just ordinary mapped button activations. Track adaptive triggers, touch, IMU and LEDs separately rather than presuming complete base-model parity.

Existing source narrative: [DualSense and Edge L0 source evidence](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/dualsense-l0.md).

## Linux v7.3 source revision update

Edge is a distinct product on USB and Bluetooth HID buses. Unlike the earlier pinned parser, Linux v7.3 advertises and emits four extra keys: Fn1/Fn2 as BTN_TRIGGER_HAPPY1/2, left/right paddles as BTN_TRIGGER_HAPPY3/4. These are source-defined controls, not live host events. [`edge-pa2-kernel-identity-buses`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/edge-pa2-kernel-identity-buses.json), [`edge-pa2-kernel-extra-evdev`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/edge-pa2-kernel-extra-evdev.json), [`edge-pa2-kernel-revision-difference`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/edge-pa2-kernel-revision-difference.json).

USB 0x01 input (64 bytes) and BT 0x31 (78 bytes with CRC) feed the shared parser; USB output 0x02 (63 bytes) and BT output 0x31 (78 bytes) differ in framing. The inspected kernel shares output paths and selects compatible vibration v2 for Edge but does not show an Edge-specific profile handler. [`edge-pa2-kernel-usb-bt-framing`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/edge-pa2-kernel-usb-bt-framing.json), [`edge-pa2-kernel-output-boundary`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/edge-pa2-kernel-output-boundary.json).

Physical descriptors, independent Fn/paddle behavior, onboard profiles and remapping, actual driver binding and SDL backend acceptance remain unmeasured. Bluetooth-bus UHID is not radio pairing. [`edge-pa2-native-profiles-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/edge-pa2-native-profiles-unknown.json), [`edge-pa2-physical-fidelity-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/edge-pa2-physical-fidelity-unknown.json), [`edge-pa2-backend-acceptance-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/edge-pa2-backend-acceptance-unknown.json).
