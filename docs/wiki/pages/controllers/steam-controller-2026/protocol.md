# Steam Controller 2026 — USB identity and report framing

[← Controller overview](index.md) · [Controls](controls.md) · [Consumers](modes-and-consumers.md)

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

## Wired enumeration: what a USB emulator must realize

The retained **physical wired** `28de:1302` S3 reference reports one configuration, one HID interface **0**, interrupt IN `0x81` and OUT `0x01`, 64-byte endpoint max packets and a 372-byte HID report descriptor. The three HID application collections live **inside one interface**. Therefore three collections must not be translated into three USB interfaces. See [`steam-s3-1302-usb-interface`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-s3-1302-usb-interface.json) and [`steam-s3-1302-report-shapes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-s3-1302-report-shapes.json).

## Descriptor-declared report inventory

The following is the **physical descriptor declaration**, not a claim that all report IDs were observed at runtime. Values are hexadecimal IDs; lengths are body bytes *excluding* the one-byte report ID.

| Direction | Report IDs → body length |
| --- | --- |
| Input | `40:5`, `41:8`, `42:53`, `43:14`, `44:5`, `45:45`, `79:1`, `7b:12` |
| Output | `80:9`, `81:7`, `82:3`, `83:9`, `84:8`, `85:3`, `86:3`, `87:63`, `88:63`, `89:63` |
| Feature | `01:63`, `02:63` |

Source: [`steam-s3-1302-report-shapes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-s3-1302-report-shapes.json). Do not confuse the HID report descriptor's declared sizes with short USB control transfers, feature payload trimming or application-level completion semantics.

## Native packet formats

The source-backed common input family includes:
- `0x42` — 54 wire bytes, `0x45` — 46, and `0x47` — 46 in SDL's alternative timestamp interpretation.
- Sequence and 32-bit button bitfield; signed 16-bit analog triggers/sticks, signed pad coordinates and pressure fields; IMU timestamp, signed accelerometer and gyro fields.
- `0x47` is **not** decoded in the inspected Linux IBEX raw event switch, whereas SDL explicitly supports it. This is a consumer difference, not proof that `0x47` physically occurs on a given link.

See the explicitly opposed [`steam-c6-disagreement-47-kernel`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-c6-disagreement-47-kernel.json) / [`steam-c6-disagreement-47-sdl`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-c6-disagreement-47-sdl.json) claims and [C6 report-field table](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-c6-decision-table.md).

## Feature and output handling

Linux and SDL issue command-shaped feature exchanges for attributes, settings, lizard configuration and rumble. The exact shape, optionality and timing differ by consumer; do not enforce a single universal initialization transcript. The D9 wired feature reductions constrain supported values and statuses ([`steam-d9-feature-response-framing`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-feature-response-framing.json), [`steam-d9-1302-model-attributes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-1302-model-attributes.json)), but redacted serial and unknown feature-body material must not be reproduced.

The S3 descriptor declares `0x86`–`0x89` outputs; their semantics are **not** established merely by kernel source or declaration. Later bounded D9 haptic tests supply selected evidence on `0x83`, `0x86`, `0x87`, `0x88` and `0x44`, with limits described in [haptics](haptics-and-audio.md).

## Separate receiver transport

The Puck USB identity `28de:1304` has *different interface topology*. Copying this wired descriptor into a single simulated Puck interface will not reproduce SDL's receiver interface-number selection. See [receiver interfaces](../steam-controller-2026-puck/interfaces-and-slots.md).
