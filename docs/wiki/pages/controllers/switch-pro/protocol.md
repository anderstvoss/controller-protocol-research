# Switch Pro — USB handshake and HID report protocol

[← Switch Pro overview](index.md)

> Reviewed corpus revision: `ab74f662…` (2026-11-09). Most Switch 1 claims below are **source-only**, not physical captures.

## Startup on USB

Community and kernel source describe `0x80` USB command framing, with status `01`, handshake `02`, baudrate change `03`, repeated handshake and no-timeout `04`, acknowledged by `0x81`. SDL has a related but separately programmed initialization path. Do **not** assume the sequence or timings are identical for Bluetooth; they are separate transports: [`swpro-l0-device-usb-cmd-sequence`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-usb-cmd-sequence.json), [`swpro-l0-sdl-usb-initialization`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-sdl-usb-initialization.json).

## Report role table

| ID | Direction | Content |
| --- | --- | --- |
| `0x01` | Host → controller | Rumble words, packet counter, subcommand ID and arguments |
| `0x10` | Host → controller | Rumble-only packet |
| `0x21` | Controller → host | Subcommand reply, ACK state, echoed subcommand ID and data |
| `0x30` | Controller → host | Full input state and three IMU sample sets |
| `0x3F` | Controller → host | Simplified button/hat report |
| `0x81` | Controller → host | USB command acknowledgement |
| `0x31` | Controller → host | **Controller-family** MCU-capable extended input described in source notes; Switch Pro-specific NFC operation remains unverified |

Report role citations: [`swpro-l0-linux-report-id-routing`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-linux-report-id-routing.json), [`swpro-l0-device-subcmd-ack-byte`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-subcmd-ack-byte.json), [`swpro-l0-device-report30-full`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-report30-full.json).

A `0x01` subcommand generally follows a packet counter and **eight rumble bytes**. Linux waits for a corresponding `0x21` reply and retries according to its consumer timeout. A synthetic OpenPuck ACK is compatibility behavior, not evidence of every hardware NACK/error path: [`swpro-l0-linux-subcmd-retry-ack`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-linux-subcmd-retry-ack.json), [`swpro-l0-openpuck-output-accept`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-openpuck-output-accept.json).

## Full report structure

Source-described `0x30` includes timestamp/timer, battery/connection, three button bytes, two packed 12-bit stick values, vibration status and **three consecutive six-axis IMU samples**. Linux maps the Pro d-pad to `ABS_HAT0` and sticks to `ABS_X/Y` + `ABS_RX/RY` in its evdev exposure. These are a wire-candidate and a **host mapping**, respectively: [`swpro-l0-device-report30-full`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-report30-full.json), [`swpro-l0-linux-pro-button-mapping`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-linux-pro-button-mapping.json).

## Device information

Subcommand `0x02` returns firmware/type and identity fields. The source-described type for Pro is `0x03`. Never publish real MAC values; generated per-instance identity for an emulator is not measured physical firmware: [`swpro-l0-device-info02-fields`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-info02-fields.json).

**Source reference:** [individual source locators](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/switch-pro-citation-map.md).

## MCU report caution (follow-up research)

The family-level `0x11` output and `0x31` input, together with MCU subcommands `0x20`–`0x22`, are **not a measured Switch Pro-specific command/reply sequence**. Do not copy Joy-Con Right NFC assumptions into the Pro. See [HOME light / NFC scope](home-light-and-nfc.md) and [`swpro-cgap-nfc-mcu-family-context`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/swpro-cgap-nfc-mcu-family-context.json).
