# Nintendo Switch Joy-Con (L)

> Reviewed corpus revision: `ab74f662…` (2026-11-09). Most Switch 1 claims below are **source-only**, not physical captures.

**Registry:** [Joy-Con (L)](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/switch-joycon-left.json), parent [Switch 1 family](../switch-joycon-family/index.md). Native Bluetooth-facing identity is typically `057e:2006`; the `0x02` device-info type byte is `0x01` in the pinned source interpretation. [`joycon-a-device-info-type`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-device-info-type.json).

## Left-half-specific controls

**New dedicated analysis:** [left wire fields and kernel/SDL presentation](source-and-consumers.md), reviewed through November 11. It remains **source-only**.

The source-described left half includes the D-pad, L/ZL, SL/SR rail buttons, one packed left stick and its IMU. Its absence of right-side ABXY is **not** a reason to invent a full Pro controller on-wire. The `0x30` report still has common slots; the missing stick and unused rumble slot must be handled according to the supported device/consumer semantics rather than silently inferred. [`joycon-a-full-report-per-side`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-full-report-per-side.json), [`joycon-a-rumble-slot-framing`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-rumble-slot-framing.json).

Factory left-stick calibration differs in address from right-stick calibration and should be read or supplied per-device rather than mirrored. [`joycon-a-calibration-per-side`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-calibration-per-side.json).

## Pairing and transport

Bluetooth left and right halves are independent devices. A program may present them as a combined controller, but this is outside the physical left-half protocol: [pairing chapter](../switch-joycon-family/pairing-and-consumers.md). The Charging Grip has its own USB interfaces. [`joycon-hid-nintendo-bus-binding`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-hid-nintendo-bus-binding.json).

## Qualification

Reference probes: left-specific `0x02` type, isolated SL/SR events, left stick neutral/endpoints, IMU axes, calibration fallbacks, rumble and disconnect/reconnect. **No physical left-half capture is asserted.**

## November 11 left-specific source follow-up

Pinned source narrows the left-half identity to `057e:2006` / device-info type `0x01`, specifies Minus/Capture/SL/SR/L/ZL bits in full `0x30` reports, and describes Linux `BTN_DPAD` rather than hat output, left-stick calibration/Y inversion and left-IMU axes without right-half sign reversal. SDL3 changes the *presentation* of the same raw fields between sideways mini-mode and parented/vertical mode. The unused right-stick bytes remain physically unknown. Details: [left-specific wire and consumer chapter](source-and-consumers.md), [`joycon-cgap-left-wire-fields`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/joycon-cgap-left-wire-fields.json), [`joycon-cgap-left-sdl3-modes`](https://github.com/anderstvoss/controller-protocol-research/blob/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7/records/claim/joycon-cgap-left-sdl3-modes.json).
