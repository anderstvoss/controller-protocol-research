# DualSense — rumble, adaptive triggers, LEDs and audio

[← DualSense overview](index.md)

> **Evidence snapshot:** corpus `ab74f662…` (2026-11-09); source-only versus physical and device versus consumer evidence are kept distinct.

## Common output effect block

USB output `0x02` includes bit-gated motor/effect fields, speaker/microphone volumes and routes, mute LED, player indicators, lightbar and trigger effects. A host must set the appropriate valid flags; writing plausible bytes to unset fields does not demonstrate actuation. The equivalent Bluetooth effect is framed differently. See [`ds-l0-device-usb02-valid-flags`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-usb02-valid-flags.json) and [`ds-l0-sdl-output-transport`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-sdl-output-transport.json).

## Adaptive triggers

Separate **11-byte** effect blocks describe left and right triggers. Community encoders distinguish Off `0x05`, Feedback `0x21`, Weapon `0x25` and Vibration `0x26`, with mode-specific zone masks/strengths and vibration frequency. These are **source-backed encodings**, not physically measured resistance, friction, force or safe operating limits. See [`ds-l0-device-adaptive-trigger-mode-block`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-adaptive-trigger-mode-block.json) and [`ds-l0-device-adaptive-trigger-mode-parameters`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-device-adaptive-trigger-mode-parameters.json).

Do not take an SDL `rumble` call as evidence that it exercises adaptive trigger motors. They require separate reverse-output probes and bounded physical actuation trials.

## LED channels

The common effect layout separates RGB lightbar, five player LEDs and microphone-mute LED. Valid-flag semantics and offsets differ in the wrapped USB and Bluetooth packets. Lightbar RGB, player-bit patterns and mic LED off/on are source-supported; **pulse and brightness details remain inferred or unknown**, not physical. Source records [`ds-l0-led-inventory`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-led-inventory.json), [`ds-l0-led-player-led-bits`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-led-player-led-bits.json), [`ds-l0-led-mute-led-off-on`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-led-mute-led-off-on.json); detailed [LED table and proposed test order](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/dualsense-led-inventory.md).

## Bidirectional audio and tactile transducers

DualSense USB audio and HID effects are **separate interfaces and software stacks**. The pinned ALSA UCM profile describes four playback and two capture hardware channels, including headphone/internal-speaker/microphone/headset logical routes; it does **not** establish that channels 2/3 are physically verified grip/haptic actuators. This is expressly consumer-scoped evidence: [`audio-dualsense-alsa-ucm-roles`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/audio-dualsense-alsa-ucm-roles.json). A prior owner's EXP-0023 reports selective physical USB audio routing, bounded by that experiment's scope. See [Sony audio and consumer survey](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/dualsense-consumer-survey.md).

The proper virtual audio device requires realistic USB Audio Class topology, stream descriptors, clocks/feedback as needed and host ALSA/PipeWire integration; a stand-alone evdev or UHID gamepad cannot manufacture audio endpoints. Report separate outcomes for playback, capture, channel assignment and physical sound/actuation.

## Verification

Test LEDs and adaptive triggers at bounded intensity with explicit stop/reset; use guarded audio amplitudes and validate channel routing independently. Avoid claiming that output USB transfer completion equals physical effect acceptance.

## November 10 host association survey

The newer [controller/audio association chapter](../../audio-association.md) separates SDL's Sony **HID** effect support from **USB sound-card** discovery. ALSA UCM selects the Sony DualSense profile for audio IDs `054c:0ce6` and `054c:0df2`; PipeWire/WirePlumber and ALSA persistent rules use their own udev-derived audio identity. No source establishes automatic Steam/Proton association when UHID controller and sound nodes are unrelated by USB topology. This unknown cannot be closed by merely matching a VID/PID string. [`audio-consumer-dualsense-ucm-usb-ids`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/audio-consumer-dualsense-ucm-usb-ids.json), [`audio-consumer-sidecar-hid-sound-association-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/audio-consumer-sidecar-hid-sound-association-unknown.json).
