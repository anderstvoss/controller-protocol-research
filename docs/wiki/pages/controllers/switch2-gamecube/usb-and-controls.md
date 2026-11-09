# Switch 2 GameCube — USB protocol and realization

[← Switch 2 GameCube](index.md)

> Reviewed corpus: 2026-11-09. Unless stated otherwise this chapter describes inspected *consumer source code*, not a physical retail capture.

## USB host binding

The source-described device `057e:2073` is matched by SDL's direct libusb path and by Linux's Nintendo Switch 2 vendor USB/HID logic. SDL inspects **interface 1**, discovers bulk IN/OUT endpoints **dynamically**, then sends staged command/configuration/identity/calibration exchanges. A true USB implementation must expose the relevant interfaces and endpoints; **no captured endpoint numbers or actual retail descriptors** were qualified. [`switch2-gc-direct-libusb-identity`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-direct-libusb-identity.json), [`switch2-gc-dynamic-bulk-endpoints`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-dynamic-bulk-endpoints.json), [`switch2-gc-command-handshake`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-command-handshake.json).

## Report and input semantics

The Linux decoder specifically registers input `0x0a`, with support for a distinct unified report `0x05` depending on selected mode. SDL and Linux both decode:
- Unique **C** control;
- separate **analog** left and right trigger values;
- independent end-travel digital **click/shoulder** controls;
- two sticks and gamepad button data.

Do not derive click bits from an arbitrary analog threshold as a claim of physical behavior. The kernel's source map exposes trigger channels `0..4095` at its evdev interface, but that is consumer scaling, not a measured physical ADC resolution: [`switch2-gc-report0a-linux`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-report0a-linux.json), [`switch2-gc-distinct-controls`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-distinct-controls.json), [`switch2-gc-trigger-zero-calibration`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-trigger-zero-calibration.json), [`switch2-gc-linux-evdev-presentation`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-linux-evdev-presentation.json).

## Outputs and calibration

Both SDL and Linux choose a GameCube-specific simple `0x03` rumble path (on/off/duty modulation), in contrast to the different encoded Switch 2 HD-rumble path. USB completion is not tactile confirmation. Host startup also probes firmware/device type and calibration. [`switch2-gc-rumble-binary`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-rumble-binary.json), [`switch2-gc-identity-calibration-consumer`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-identity-calibration-consumer.json).

## Physical capture boundary

The proposed sessions separately cover descriptors, initialization, every control, trigger travel/click, safe rumble and identity. They are **not run** and must be recorded as new controlled experiments before being treated as physical evidence: [owner capture matrix](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/switch2-gamecube-physical-capture-plan.md).
