# Steam Controller 2026 — haptic commands, MIDI and PCM

[← Controller overview](index.md) · [Protocol](protocol.md)

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

## Why output report declarations are not enough

The physical wired HID descriptor declares `0x80`–`0x89`, but a declaration does not prove an effect, sign convention, motor or stream-ack protocol. Linux interprets certain `0x80` gain bytes as unsigned, while SDL packed structures interpret them as signed. Neither establishes how a retail motor handles encoded negative gain; preserve both positions and test in their common nonnegative range: [`steam-c6-disagreement-gain-kernel`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-c6-disagreement-gain-kernel.json) / [`steam-c6-disagreement-gain-sdl`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-c6-disagreement-gain-sdl.json).

## Bounded D9 observations

The owner's supervised **wired** sessions on 2026-11-05 distinguish MIDI input to a host app, USB haptic output and subjective physical sensation. MIDI is **not a USB MIDI interface**. Pinned SteamHapticsSinger generated `0x83` 64-byte outputs; labelled MIDI channels 0–3 mapped to differing internal motor selectors, and grip versus pad sensations differed. Frequency bytes and routing are recorded, but exact left/right actuator identities remain partially source-named rather than independently qualified. See [`steam-d9-midi-channel-routing`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-midi-channel-routing.json), [`steam-d9-midi-lfo-framing`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-midi-lfo-framing.json) and [capture conditions](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-d9-audio-midi-2026-11-05.md).

Two pinned PCM clients supplied 8-kHz, signed 16-bit stereo streams, one via `0x88` and another via `0x87`. The supervised runs recorded configuration through `0x86`, status-bearing `0x44` input and selected framed output lengths; USB transfer status 0 means a write completed, **not** that the controller accepted every configuration. `0x88` data packets were 64 wire bytes with 30 meaningful bytes per channel slot. The `0x87` path included short terminal packets. See [`steam-d9-pcm-framing-feedback`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-pcm-framing-feedback.json) and [`steam-d9-pcm-stimulus-correspondence`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-d9-pcm-stimulus-correspondence.json).

## Audio versus haptic semantics

The owner described both palpable and audible sensations at different signal levels. That does **not** establish a conventional independent USB Audio Class speaker or calibrated acoustic response. Keep haptic pulse/rumble, PCM-to-actuator streaming, unrelated host audio devices and consumer mappings separate. Physical playback was direct-wired only; nothing here proves Puck per-slot audio transport.

## Implementation priorities

Preserve exact report ID/length, motor selector, command ordering, completion and `0x44` feedback without misreporting it as an ACK unless proven. Make stop/neutral and underrun recovery deterministic. Test selected waveform equivalence and each actuator independently before claiming fidelity. See [`sc2-gap-haptic-ack`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-haptic-ack.json) and [`sc2-gap-audio`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-audio.json).
