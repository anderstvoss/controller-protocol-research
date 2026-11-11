# Steam Controller 2026 — implementation acceptance and gaps

[← Controller overview](index.md)

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

## Recommended independent gates

| Gate | Method and evidence | Current constraint |
| --- | --- | --- |
| USB identity | Exact device/configuration/HID descriptor with interface and endpoint topology | S3 physical wired observation exists ([`steam-s3-1302-usb-interface`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-s3-1302-usb-interface.json)) |
| Feature exchange | Host GET/SET transcript under pinned SDL/kernel/Steam, safe malformed/optional cases | D9 bounds some feature results ([`steam-d9-feature-response-framing`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-feature-response-framing.json)) |
| Inputs | Neutral → isolated control → release with raw packet/SDL semantic correspondence | D9 reports 22 digital mappings and sensor-contact caveats ([`steam-d9-native-digital-correspondence`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-native-digital-correspondence.json)) |
| Lizard/ownership | Native/desktop paths on kernel-only, SDL-only, Steam-only and coexistence sessions | Exact firmware watchdog unproven ([`sc2-gap-physical-lizard-watchdog`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-physical-lizard-watchdog.json)) |
| IMU | Controlled orientation/angular-rate baseline with clock/axis comparisons | D9 motion is qualitative ([`steam-d9-sdl-enabled-motion`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-sdl-enabled-motion.json)) |
| Output | Intensity/duration and motor-specific pulses, PCM configure/status/stop | D9 bounded streams observed; no universal transfer function ([`steam-d9-pcm-framing-feedback`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-pcm-framing-feedback.json)) |
| Bluetooth | Independent advertising/pairing, report framing, security and reconnect | USB evidence does not qualify BLE ([`sc2-gap-ble-identity`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-ble-identity.json)) |
| Lifecycle | Cold/warm opening, stolen/restored raw client, unplug and rollback | Treat consumer identity, button state and auxiliary desktop nodes together |

## Virtualgamepad contract

A **compatible** implementation can prioritize an observed host parser path; a **faithful** implementation must be grounded in the corresponding physical report and command behavior. Record this policy explicitly per feature. Do not substitute OpenPuck's receiver behavior for a direct `1302` reference.

See [compatibility-versus-fidelity disputes](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-c6-decision-table.md) and [source/physical capture plan](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-physical-capture-plan.md). The next acceptance decision should be made from exact host captures, not just an SDL gamepad appearing.

## Bluetooth-specific research gates (source-only)

The [new BLE chapter](bluetooth-and-uhid.md) adds BlueZ HOGP report routing, a *conditional* ATT feature-write MTU ≥66 requirement, kernel identity `28de:1303` and version-specific SDL trigger/haptic handling. No physical BLE report descriptor, pairing, capture or Steam UI result was obtained. These remain independent owner tests; do not reuse wired/Puck acceptance. [`steam-ble-bluez-att-mtu-feature-constraint`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/steam-ble-bluez-att-mtu-feature-constraint.json).
