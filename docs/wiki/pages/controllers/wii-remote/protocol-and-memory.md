# Wii Remote — native report lifecycle and memory

[← Wii overview](index.md) · [Extensions](extensions-and-motionplus.md)

> **Scope:** reviewed corpus 2026-11-09; source and virtual-host evidence do not establish a retail Wii Remote physical capture.

## Transport and reports

The original remote's protocol is Bluetooth HID with an output/control report exchange. In Linux, `BUS_BLUETOOTH` on **UHID** can be enough for `hid-wiimote` to bind and expose native hidraw/evdev interfaces, but **does not implement radio discovery, L2CAP channels or pairing**. The corpus explicitly distinguishes these: [`wii-kernel-bluetooth-match`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-kernel-bluetooth-match.json); [consumer transport matrix](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-consumer-survey.md).

Important report classes in the pinned source:
- **`0x15`** status request → **`0x20`** status report; extension flags/LED/battery may trigger reinitialization.
- **`0x11`** LEDs, **`0x12`** report-mode selection, **`0x13/0x1a`** infrared enable, **`0x14/0x19`** speaker enable/mute controls.
- **`0x16`** memory/register write, **`0x17`** memory/register read; **`0x21`** reply and ACK/error exchange. Other continuous input report modes combine buttons, acceleration, IR and extension bytes.
- **`0x37`** is a frequent full-state mode with extension payload used in Dolphin MotionPlus sequences; it is not universal across consumers.

The exact required ACK/status/order is consumer-dependent: [`wii-kernel-report-modes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-kernel-report-modes.json), [`wii-kernel-status-ack-flow`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-kernel-status-ack-flow.json), [`wii-c5-report-layouts`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-c5-report-layouts.json) and [`wii-gap-dolphin-attach-controller-task-order-and-failure`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-gap-dolphin-attach-controller-task-order-and-failure.json).

## Memory is part of the controller personality

Do **not** conflate EEPROM-like persistent calibration with I²C/register space. Dolphin and other consumers read base calibration from EEPROM address `0x0016`; extension ID and calibration are accessed through register regions around `A400`, active/inactive MotionPlus controls around `A600`, and IR registers around `B000`. The corpus's `0x1700` memory size is explicitly a **hypothesis**, not a frozen device capacity: [`wii-dolphin-memory-routing`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-dolphin-memory-routing.json), [`wii-memory-size-hypothesis`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-memory-size-hypothesis.json).

A safe virtual memory design supports a known reference image or caller-supplied calibration, mutable **ephemeral default** state, explicit optional import/export on clean shutdown and opt-in persistence. Never publish a real pairing/identity image, and do not fabricate factory calibration checksums as hardware truth. Test inclusive read bounds, partial/failed reads, multiple register banks and reset semantics separately.

## Extension security and failures

The pinned consumer code frequently disables extension encryption before normal reads. That does **not** establish full encrypted-mode operation or every challenge response. Preserve [`wii-extension-encryption-gap`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-extension-encryption-gap.json) as an open device-protocol question. Refused register reads and ACK errors can leave Dolphin or the kernel waiting rather than proceeding to gyro decoding.

See [Dolphin read/write sequence](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-dolphin-attachment-technical.md) and [security and challenge provenance](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-motionplus-challenge.md).

## Retail descriptor evidence (P6)

One RVL-036 Plus advertising Nintendo RVL-CNT-01 returned the same 217-byte HID report descriptor in two SDP queries and a bound Linux hidraw read. This is a physical observation scoped to that unit and Bluetooth identity. The retained descriptor matches the published rnconrad candidate digest. Retail and interim synthetic descriptors share the Game Pad application collection and declared report IDs/lengths, but retail vendor-page main items are Array rather than Variable. Both declare speaker output IDs `0x14`, `0x18`, `0x19` with payload lengths 1, 21, 1 excluding report ID, and no Feature reports; the older C5 synthetic descriptor lacks the speaker outputs. [`wii-p6-retail-plus-rvl-cnt-01-descriptor-observed`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/wii-p6-retail-plus-rvl-cnt-01-descriptor-observed.json), [`wii-p6-retail-plus-rvl-cnt-01-descriptor-comparison`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/wii-p6-retail-plus-rvl-cnt-01-descriptor-comparison.json), [`wii-p6-retail-hid-descriptor-run`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/experiment/wii-p6-retail-hid-descriptor-run.json), [`wii-p6-retail-plus-rvl-cnt-01-descriptor`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/fixture/wii-p6-retail-plus-rvl-cnt-01-descriptor.json). Other revisions, on-air framing, speaker behavior and virtual acceptance remain separate questions.
