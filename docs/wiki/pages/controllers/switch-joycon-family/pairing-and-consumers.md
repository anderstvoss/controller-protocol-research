# Joy-Con — two halves, one logical gamepad?

[← Joy-Con family](index.md)

> Reviewed corpus revision: `ab74f662…` (2026-11-09). Most Switch 1 claims below are **source-only**, not physical captures.

## Physical transport and consumer-created pair

| Arrangement | Physical / USB layout | Who combines |
| --- | --- | --- |
| One Bluetooth Joy-Con (L) | One HID `057e:2006` | No combination |
| One Bluetooth Joy-Con (R) | One HID `057e:2007` | No combination |
| Two Bluetooth halves | Two independent HID devices | SDL in-process or joycond virtual uinput device, policy-dependent |
| USB Charging Grip | One USB `057e:200e` with per-half interfaces | Host selection depends on interface and device-info type |

Support: [`joycon-sdl-hidapi-pair-combination`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-sdl-hidapi-pair-combination.json), [`joycon-joycond-pair-combination`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-joycond-pair-combination.json), [`joycon-hid-nintendo-bus-binding`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-hid-nintendo-bus-binding.json). The synthetic combined `057e:2008` identity is **not** a third physical Bluetooth device.

## Linux, SDL and Steam

Linux creates per-half main evdev and IMU nodes, plus LED management, without combining. SDL HIDAPI can pair halves automatically using its configured policy, often selecting the right IMU as primary. joycond operates on kernel evdev, hides selected physical main nodes and creates a separate uinput pair; it does **not** parse native Bluetooth HID packets like SDL. See [`joycon-hid-nintendo-identity-and-nodes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-hid-nintendo-identity-and-nodes.json), [`joycon-sdl-hidapi-pair-combination`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-sdl-hidapi-pair-combination.json).

Steam's udev rule grants device access, **not** a guarantee that its closed client chooses any specific pairing, gyro or output backend. SDL2 and SDL3 also differ in the strictness of required startup ACKs, so pin exact versions. See [`joycon-e-steam-hidraw-grants`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-e-steam-hidraw-grants.json), [`joycon-c-sdl3-bt-open-gates`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-c-sdl3-bt-open-gates.json), [`joycon-d-sdl2-strict-open`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-d-sdl2-strict-open.json).

## Virtualgamepad implication

Model **two independently identified halves** and optionally a coordinated *create/remove convenience operation*. Let the chosen consumer combine when appropriate. Avoid exposing a third 2008 physical-HID personality by default, since doing so can duplicate inputs and confuse binding. For USB Charging Grip a separate USB composite realization must be researched, rather than relabeling the Bluetooth pair.

**Decision and open questions:** [pair-shape research](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/switch-joycon-pair-shape.md), [identity and calibration decisions](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/switch-joycon-decision-table.md).

## SDL3 standalone left-half mini-mode (November 11)

Pinned SDL3 source presents an unparented Joy-Con Left **sideways** by default, rotating stick and sensor coordinates and mapping directional controls to face buttons. Once paired or configured vertically it exposes a conventional left stick and D-pad hat. Linux `hid-nintendo`, separately, exposes D-pad key events and does **not** automatically combine halves. This is a host mapping distinction, not evidence that the physical half changes its report bytes. See [left-half wire and consumers](../switch-joycon-left/source-and-consumers.md); [`joycon-cgap-left-sdl3-modes`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/joycon-cgap-left-sdl3-modes.json).
