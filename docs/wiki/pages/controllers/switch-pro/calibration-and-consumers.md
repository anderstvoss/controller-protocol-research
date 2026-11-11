# Switch Pro — flash, IMU, rumble and host selection

[← Switch Pro overview](index.md) · [Protocol](protocol.md)

> Reviewed corpus revision: `ab74f662…` (2026-11-09). Most Switch 1 claims below are **source-only**, not physical captures.

## SPI and calibration are active parts of initialization

Pinned SDL/kernel readers probe user and factory calibration over subcommand `0x10` (SPI read). Community map:

| Region | Source-described purpose |
| --- | --- |
| `0x6020`–`0x6037` | Factory IMU calibration |
| `0x603D` / `0x6046` | Left/right factory stick calibration |
| `0x8010`, `0x801B`, `0x8026` | User calibration markers/blocks, including `B2 A1` magic |
| `0x6050` onward | Body/button/grip colour fields |

The kernel and SDL have **different fallback policies** for invalid, absent or all-`FF` user/factory calibration. SDL's source requires some factory stick reads where kernel can substitute defaults. A fabricated all-FF SPI image is therefore not guaranteed to attach. [`swpro-l0-device-factory-spi-map`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-factory-spi-map.json), [`swpro-l0-device-user-spi-magic`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-user-spi-magic.json), [`swpro-l0-consumer-kernel-calibration-fallback`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-consumer-kernel-calibration-fallback.json), [`swpro-l0-consumer-sdl-calibration-fallback`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-consumer-sdl-calibration-fallback.json).

## IMU

`0x30` input contains three accelerometer/gyro sample sets, interpreted/calibrated by each host. Kernel additionally exports a sensor evdev sibling. Subcommand `0x40` enables IMU; the kernel may request it in initialization while SDL enables conditionally on sensor use: [`swpro-l0-linux-imu-evdev-consumer`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-linux-imu-evdev-consumer.json), [`swpro-l0-consumer-imu-rumble-ack-gates`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-consumer-imu-rumble-ack-gates.json).

## HD rumble and player LEDs

Left/right motor words are encoded using frequency/amplitude tables and sent in `0x01`/`0x10`. Source formula/table knowledge is not proof of force response or tactile equivalence. SDL has specific write pacing, including ~30-ms limiting and refresh policy. Player LEDs use subcommand `0x30` with host-controlled settings; kernel battery/LED exposure is an additional surface: [`swpro-l0-device-rumble-word-tables`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-rumble-word-tables.json), [`swpro-l0-sdl-rumble-rate-policy`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-sdl-rumble-rate-policy.json), [`swpro-l0-linux-led-battery-consumer`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-linux-led-battery-consumer.json).

## HOME LED is separate from four player LEDs

The Linux consumer also sends subcommand `0x38` for HOME-button brightness (0–15), independently of the four-player-light `0x30` command. This is an auxiliary LED output, **not** a fifth player indicator; source-only, without measured retail brightness or ACK. [Details](home-light-and-nfc.md), [`swpro-cgap-home-led-consumer`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/swpro-cgap-home-led-consumer.json).

## Discovery, identity and consumer questions

The kernel and SDL choose different open sequences for device info, user/factory SPI, IMU and rumble setup. SDL can derive serial from a device-info identity without using it unchanged as GUID content; Linux exports MAC-derived uniq. Both claims concern **consumer** behavior, not licence to fake a static real address. [`swpro-l0-consumer-kernel-open-order`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-consumer-kernel-open-order.json), [`swpro-l0-consumer-sdl-open-order`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-consumer-sdl-open-order.json), [`swpro-l0-consumer-sdl-mac-serial-guid`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-consumer-sdl-mac-serial-guid.json).

A later SDL fix reverses six bytes of USB status address order relative to its stored representation; the Bluetooth device-info path has a different byte treatment: [`swpro-l0-consumer-sdl-usb-status-address-order`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-consumer-sdl-usb-status-address-order.json). Do not promote this into a universal raw packet-order statement.
