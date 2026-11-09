# Xbox 360 — wired XUSB packets and wireless receiver

[← Xbox 360 overview](index.md)

> **Reviewed corpus:** 2026-11-09. A source parser, compatibility shim or virtual-host acceptance does not establish native physical hardware fidelity.

## Wired report candidate

Community reference and independently developed USB-host readers describe a **20-byte** wired input report beginning `00 14`. Its candidate field map:

| Byte indices | Description |
| --- | --- |
| 0–1 | report type `00`, length `14` |
| 2–3 | digital button/D-pad bitfield |
| 4–5 | LT / RT, unsigned 8-bit |
| 6–13 | LX, LY, RX, RY signed **little-endian 16-bit** |
| 14–19 | reserved or source-uninterpreted tail |

This is **source-supported device-protocol research**, not independently recorded retail packet bytes: [`x360-l0-device-xusb-wired20`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-xusb-wired20.json), [`x360-l0-device-xusb-wired-buttons`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-xusb-wired-buttons.json).

## Output

Source writers send an 8-byte rumble command of the form `00 08 00 strong weak 00 00 00` and an LED command `01 03 mode`. Per-motor physical intensity, output rate and LED actuation were not measured in a controlled retail experiment: [`x360-l0-device-xusb-output-ff-led`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-xusb-output-ff-led.json).

## Native USB interface

The wired model uses a **vendor-specific USB interface**, not a standard HID descriptor carrying gamepad usages; USB device identity by VID/PID alone is insufficient to qualify native virtualization. See [`x360-l0-device-xusb-nonhid-interface`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-xusb-nonhid-interface.json).

## Wireless receiver is another protocol

The `045e:0719` proprietary 2.4-GHz USB receiver has slot presence/state, connection and distinct receiver packet framing. A wired `00 14` parser or generic Bluetooth HID connection must not be asserted to match receiver traffic. This remains a source lead, not physical qualification: [`x360-l0-device-wireless-receiver0719-lead`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-wireless-receiver0719-lead.json), [`x360-l0-device-physical-receiver-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-physical-receiver-unknown.json).

**Comparison:** [source and host decoder citations](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/xbox360-l0.md).
