# Research gaps and priorities

These are **editorially selected** open questions at the reviewed corpus commit, not new `unknown` records or proof of unresolved implementation work.

| Family | Highest-value boundary to test | Corpus evidence |
| --- | --- | --- |
| Steam 2026 Puck | Full composite USB descriptors, receiver slot ownership, link lifecycle and output routing compared with real Puck | [`sc2-gap-puck-usb-descriptors`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-puck-usb-descriptors.json), [`sc2-gap-puck-slots`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-puck-slots.json) |
| Steam 2026 BLE | Physical 1303 HID descriptor, GATT Report Map/MTU, kernel/SDL feature replies, Steam acceptance and output response | [`steam-ble-bluez-att-mtu-feature-constraint`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/steam-ble-bluez-att-mtu-feature-constraint.json), [`steam-ble-kernel-v73-binding`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/steam-ble-kernel-v73-binding.json) — **source-only** |
| Steam 2026 wired | Cross-version lizard/watchdog interpretation, consumer ownership, haptic output semantics | [`sc2-gap-physical-lizard-watchdog`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-physical-lizard-watchdog.json), [`sc2-gap-haptic-ack`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-haptic-ack.json) |
| Wii Remote | Real Bluetooth pairing versus UHID metadata, extension/MotionPlus activation and EEPROM identity | [`wii-extension-encryption-gap`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-extension-encryption-gap.json), [`wii-memory-size-hypothesis`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-memory-size-hypothesis.json) |
| DualSense | USB/BT physical reference per firmware, actual trigger actuation, Steam gyro routing | [`ds-l0-uhid-gyro-association-hypothesis`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-uhid-gyro-association-hypothesis.json) |
| DualShock 4 | Revision-specific GET features, enhanced BT, touch-history decoding | [`ds4-l0-device-touch-count-conflict`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds4-l0-device-touch-count-conflict.json) |
| Switch Pro/Joy-Con | Physical USB/BT timing, calibration fallbacks, rumble feedback, distinct HOME LED brightness, and wireless NFC/MCU applicability | [`swpro-l0-device-physical-usb-period-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/swpro-l0-device-physical-usb-period-unknown.json) |
| Switch 2 Pro | Device-side raw packets and actual Linux/SDL selected backend | [`switch2-physical-corroboration-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-physical-corroboration-unknown.json) |
| Switch 2 GameCube USB | Retail descriptor and packet/rumble validation, separate from Switch 2 Pro | [`switch2-gc-retail-physical-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-retail-physical-unknown.json) |
| GameCube WUP-028 | Physical four-port status layout, USB ownership and rumble power | [`gc-adapter-descriptor-details-unconfirmed`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-descriptor-details-unconfirmed.json) |
| Xbox 360 | Native XUSB interface comparison versus generic standard-HID implementation | [`x360-l0-device-physical-wired-usb-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/x360-l0-device-physical-wired-usb-unknown.json) |
| Xbox Series | Separate USB GIP and Bluetooth HID device truth, xone versus xpad audio/receiver paths, xpadneo Share/Guide and trigger-output semantics | [`xbox-series-usb-device-gaps`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/xbox-series-usb-device-gaps.json) |
| 8BitDo Pro 2 / Edge | Firmware-specific independent paddle/macro exposure | [`dsedge-l0-consumer-identity-separation`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/dsedge-l0-consumer-identity-separation.json) |

## How to close a gap

File a specific claim/experiment with controlled procedure and privacy-reviewed fixtures in the corpus, then request a **manual wiki refresh**. Do not amend a wiki page first and later retroactively promote a claim. See [updating](updating.md).

## Recently documented source-only distinctions

- [Steam Controller BLE](controllers/steam-controller-2026/bluetooth-and-uhid.md) — consumer evidence only; the ATT MTU arithmetic is conditional, not a measured radio link.
- [Switch Pro HOME and NFC](controllers/switch-pro/home-light-and-nfc.md) — four player indicators plus one distinct HOME LED; NFC/MCU report codes remain controller-family context.
- [Xbox Series wired GIP](controllers/xbox-series/wired-gip-and-receiver.md) and [Bluetooth/xpadneo](controllers/xbox-series/bluetooth-and-xpadneo.md) — distinguish GIP headset, Bluetooth HID, xpad and keyboard F12 Share.
- [Controller/audio association](audio-association.md) — no demonstrated automatic pairing of a UHID-only controller with unrelated ALSA/PipeWire nodes.

All of these are *research follow-ups*, not newly completed device acceptance tests.
