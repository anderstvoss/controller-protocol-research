# Switch Pro — faithful-versus-compatible lab gates

[← Switch Pro overview](index.md)

> Reviewed corpus revision: `ab74f662…` (2026-11-09). Most Switch 1 claims below are **source-only**, not physical captures.

## Required comparisons

1. Physical USB inventory (descriptor, interface, bus and source/scope) and independent BT pairing/SDP/HIDP characterization.
2. Reproduce `0x80/0x81` USB initialization and `0x01/0x21` ACK/retry/error paths; do not extrapolate from a single consumer.
3. One-control-at-a-time state decode, neutral/stick endpoint, full `0x30` and simple `0x3F` fields.
4. Factory/user SPI calibration read coverage, markers, invalid-value fallbacks and safe nonwrite policy.
5. IMU sample timing, axis signs, output routing and consistent measured reference motion.
6. Bounded dual-motor HD rumble tests, player LEDs and neutral stop, with captured reverse commands.
7. SDL evdev/HIDAPI, kernel evdev/sensor, Steam/Eden and USB/Bluetooth path selection independently.

Unresolved USB period remains **conflicted/unknown** ([`swpro-l0-device-usb-cadence-conflict`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-usb-cadence-conflict.json)); mere OpenPuck report pacing does not settle it. Steam/Eden reported neutral-axis behavior is a **consumer case** without fully pinned causal backend evidence ([`swpro-l0-consumer-steam-neutral-causation-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-consumer-steam-neutral-causation-unknown.json)).

**Original gate table:** [C-P1 through C-P8](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/switch-pro-l0.md).

## Follow-up gates: HOME and wireless NFC

Measure the HOME LED via `0x38` separately from four player LEDs, including host ACK and real brightness response. Do **not** classify it as player LED five. Validate NFC/MCU only against **Pro-specific wireless** behavior; the controller-family `0x11/0x31` codes and Joy-Con NFC work do not establish wired Pro operation. See [new output distinctions](home-light-and-nfc.md) and [`swpro-cgap-home-led-consumer`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/swpro-cgap-home-led-consumer.json).
