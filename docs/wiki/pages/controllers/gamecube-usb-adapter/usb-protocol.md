# GameCube adapter — four-port packet layout

[← Adapter overview](index.md)

> Reviewed corpus: 2026-11-09. Unless stated otherwise this chapter describes inspected *consumer source code*, not a physical retail capture.

## USB input report

The adapter's `0x21` input is **37 bytes**: one report prefix plus four consecutive **nine-byte port blocks**. For each port the source-described block fields are:

| Byte within port block | Meaning |
| --- | --- |
| 0 | status/presence/power-related bits |
| 1–2 | button bitfields (including face, D-pad, Start, Z and digital L/R clicks) |
| 3–4 | main stick X/Y |
| 5–6 | C-stick X/Y |
| 7–8 | analog L/R trigger travel |

This layout is independently corroborated by distinct consumer source paths: [`gc-adapter-input-report-layout`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-input-report-layout.json), [`gc-adapter-button-bits`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-button-bits.json).

## Per-port presence

Status `0x10` means wired controller present and `0x20` a WaveBird receiver present; neither means empty. Power bit `0x04` is interpreted by some software as enabling rumble via the second USB cable. Unspecified bits remain unknown; do not advertise their exact firmware meaning without capture. [`gc-adapter-port-type-bits`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-port-type-bits.json), [`gc-adapter-port-power-bit`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-port-power-bit.json), [`gc-adapter-remaining-status-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-remaining-status-unknown.json).

## Output

Initialization: interrupt OUT **`0x13`**; SDL waits for a reply/ready path while Dolphin tolerates an initial failure differently. Rumble: **`0x11` + four port bytes**, typically 1=run and 0=stop for wired controllers; SDL also describes 2=hard brake, but physical effect/clone compatibility is unmeasured. Both SDL and Dolphin avoid sending effective rumble to WaveBird ports. [`gc-adapter-init-command`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-init-command.json), [`gc-adapter-rumble-output`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-rumble-output.json), [`gc-adapter-rumble-brake-value`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-rumble-brake-value.json).

## Timing and topology gaps

Do not hardcode ToadKing adapter endpoint numbers into a faithful USB realization without the source device's descriptor. Some consumers enumerate interface/endpoint dynamically, and kernel bridge drivers derive polling interval from `bInterval`, which was **not** independently captured here: [`gc-adapter-descriptor-details-unconfirmed`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/gc-adapter-descriptor-details-unconfirmed.json).

## Published descriptor observations and consumer divergence

Two published third-party USB dumps agree on one configuration, one HID interface, an advertised 214-byte HID descriptor, and interrupt IN endpoint `0x81` (37 bytes) and OUT `0x02` (5 bytes), with interval 8 at full speed. This nominal interval is not measured cadence. EP0 packet sizes disagree (8 versus 64); descriptor bytes and provenance differences remain unresolved. [`gc-cgap-published-usb-interface`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/gc-cgap-published-usb-interface.json), [`gc-cgap-published-interrupt-endpoints`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/gc-cgap-published-interrupt-endpoints.json), [`gc-cgap-control-endpoint-packet-size-variance`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/gc-cgap-control-endpoint-packet-size-variance.json).

The HIDMaestro emulated descriptor advertises a 37-byte payload for report `0x21`, in tension with the 37-byte transfer including the report ID; no parser experiment resolves this. [`gc-cgap-emulated-hid-descriptor-model`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/gc-cgap-emulated-hid-descriptor-model.json), [`gc-cgap-hid-report-length-tension`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/gc-cgap-hid-report-length-tension.json). WaveBird status is consumer-dependent: Nintendont accepts `0x22` as communicating, not `0x20`; RetroArch's generic presence test accepts the latter, whereas the emulator models it as disconnected. No physical status capture settles the divergence. [`gc-cgap-wavebird-status-consumer-divergence`](https://github.com/anderstvoss/controller-protocol-research/blob/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/claim/gc-cgap-wavebird-status-consumer-divergence.json).
