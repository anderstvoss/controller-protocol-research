# Nintendo Switch 1 Joy-Con family

> Reviewed corpus revision: `ab74f662…` (2026-11-09). Most Switch 1 claims below are **source-only**, not physical captures.

**Registry:** [Switch 1 Joy-Con family](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/switch-joycon-family.json), with separately represented [left](../switch-joycon-left/index.md) and [right](../switch-joycon-right/index.md) halves. Do not treat Switch 2 Joy-Con as members of this family.

## Pages

- [Reports, subcommands, calibration, Motion and MCU](protocol-and-mcu.md)
- [Singles, pairing as a consumer policy, and host paths](pairing-and-consumers.md)

## The central architectural fact

A Bluetooth left/right "pair" remains **two separate HID devices** at the transport level. Combining them is a **consumer policy**, not an additional physical `057e:2008` Bluetooth personality. SDL HIDAPI may combine in-process; joycond creates a **uinput** combined gamepad after its own gesture logic; Linux `hid-nintendo` keeps independent kernel devices. See [`joycon-sdl-hidapi-pair-combination`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-sdl-hidapi-pair-combination.json), [`joycon-joycond-pair-combination`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-joycond-pair-combination.json) and [`joycon-hid-nintendo-identity-and-nodes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-hid-nintendo-identity-and-nodes.json).

Native half identities are `057e:2006` left and `057e:2007` right; a USB Charging Grip `057e:200e` is a **separate USB container**. Device-info reply type bytes identify the half independently of transport. [`joycon-hid-nintendo-bus-binding`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-hid-nintendo-bus-binding.json), [`joycon-a-device-info-type`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-device-info-type.json).

The report family overlaps with Switch Pro, but this is a *shared protocol starting point*, not separate physical Joy-Con corroboration. In particular, right Joy-Con has its own IR/NFC MCU behavior and both halves have side-specific rail/SL/SR buttons. [`joycon-a-home-led-and-rail-buttons`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/joycon-a-home-led-and-rail-buttons.json).

**Primary source:** [Joy-Con device ledger](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/switch-joycon-l0.md), [pair identity survey](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/switch-joycon-pair-shape.md).
