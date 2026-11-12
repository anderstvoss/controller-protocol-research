# GameCube adapter — direct USB consumers versus evdev bridges

[← Adapter overview](index.md) · [Native packet contract](usb-protocol.md)

> Reviewed corpus: 2026-11-09. Unless stated otherwise this chapter describes inspected *consumer source code*, not a physical retail capture.

## Why four uinput pads are not a WUP-028 adapter

A userspace bridge such as ToadKing can parse `0x21` reports and create up to four uinput pads. It is an excellent route for **application compatibility** but does not expose one native USB `057e:0337` device, direct libusb control path, adapter status report or `0x13` initialization. [`gc-adapter-toadking-four-uinput-pads`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-toadking-four-uinput-pads.json), [`gc-adapter-consumers-require-usb-device`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-consumers-require-usb-device.json).

In contrast, SDL HIDAPI GameCube, Dolphin, Eden and Cemu code paths may expect **direct USB/libusb access**, including ownership/permission for the actual USB device node. An evdev node that resembles a GameCube controller can be ignored by their *native adapter* selection. [`gc-adapter-eden-direct-libusb`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-eden-direct-libusb.json), [`gc-adapter-cemu-direct-libusb`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-cemu-direct-libusb.json), [`gc-adapter-consumers-require-usb-device`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-consumers-require-usb-device.json).

## Semantic traps in bridge mode

- A GameCube stick is a raw byte-domain value; consumers may invert Y or calibrate from the first sample. Do not assume one universal neutral offset or signedness: [`gc-adapter-consumer-neutral-calibration`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-consumer-neutral-calibration.json), [`gc-adapter-toadking-evdev-range`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-toadking-evdev-range.json).
- Analog L/R travel and digital bottom-out **must stay independent**; do not manufacture trigger clicks solely by a generic threshold.
- Native port rumble is binary, while uinput FF_RUMBLE amplitude can be converted into duty-cycle policy. The conversion is **not device physics**: [`gc-adapter-toadking-rumble-power`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-toadking-rumble-power.json).
- WaveBird and second-cable power semantics must survive the routing layer, or consumers may believe a disconnected/unpowered rumble call succeeded.

## Implementation choice

For a transparent native adapter substitute, emulate a single **USB device with four port slots** using a USB-capable realization (such as `dummy_hcd`) and implement its interrupt setup/status/output contract. For a generic four-pad application demo, uinput is smaller and intentionally **not** native adapter fidelity. Record the chosen target; do not mix acceptance outcomes.
