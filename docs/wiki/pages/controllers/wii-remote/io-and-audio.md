# Wii Remote — infrared, LEDs, rumble and speaker

[← Wii overview](index.md)

> **Scope:** reviewed corpus 2026-11-09; source and virtual-host evidence do not establish a retail Wii Remote physical capture.

## Infrared camera and pointer

The protocol exposes **IR point coordinates and modes**, not a video camera frame. Linux's source-derived evdev exposure has up to four IR coordinates via `ABS_HAT0X/Y` through `ABS_HAT3X/Y`, nominal X 0–1023 and Y 0–767 at that driver revision. Camera configuration, sensitivity and reporting mode writes are separate from the actual geometry of infrared emitters: [`wii-kernel-ir-mode-policy`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-kernel-ir-mode-policy.json), [`wii-c5-camera-no-points`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-c5-camera-no-points.json).

Dolphin expects a multi-step IR register setup (sensitivity `B00000`/9 and `B0001A`/2, `B00033` mode, `B00030` tracking) before treating IR as initialized. A virtual device can acknowledge this configuration while *not* having a physical sensor; consumer acceptance must distinguish ACKs from real pointer tracking. [`wii-gap-dolphin-attach-controller-task-order-and-failure`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-gap-dolphin-attach-controller-task-order-and-failure.json).

## LED, vibration and battery

The kernel source maps remote player LEDs, battery/power status and base-device `FF_RUMBLE` separately from extension evdev nodes. User-visible `FF_RUMBLE` does not mean a generic uinput device responds to actual Wii remote `0x10` output with accurate motor behavior. [`wii-kernel-outputs-battery`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-kernel-outputs-battery.json). Test controls and rumble side effects during report-mode changes and shutdown, as multiple outputs share report/rumble bits.

## Speaker and audio reports

The remote includes a low-rate speaker stream and register-controlled playback. Dolphin source inspection distinguishes speaker enable/mute, rate/config registers, PCM/ADPCM formatting and paced packet output. Codec nibble order, host playback pacing and sound generation require their own evidence; **Linux `hid-wiimote` not sending speaker output** does not imply the remote lacks a speaker.

Relevant source-scoped claims: [`audio-wii-dolphin-pcm-adpcm-rate`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/audio-wii-dolphin-pcm-adpcm-rate.json), [`audio-wii-dolphin-yamaha-adpcm-nibbles`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/audio-wii-dolphin-yamaha-adpcm-nibbles.json), [`audio-wii-dolphin-real-speaker-pacing`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/audio-wii-dolphin-real-speaker-pacing.json), [`audio-wii-linux-hid-driver-does-not-send-speaker`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/audio-wii-linux-hid-driver-does-not-send-speaker.json), [`audio-wii-speaker-physical-acceptance-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/audio-wii-speaker-physical-acceptance-unknown.json). See [initialization and audio ACK gates](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-dolphin-attachment-technical.md).

## Emulation implications

Treat IR, speaker and rumble as **bidirectional protocol features**, not extra SDL buttons. Reserve independent state for speaker sample queues, output rate, IR point population and power/LED reports. A missing real IR or speaker reference should be explicitly flagged rather than silently synthesized as physically calibrated.
