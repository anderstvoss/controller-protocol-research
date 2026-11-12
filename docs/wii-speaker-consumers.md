# Wii Remote speaker: protocol and consumers beyond Dolphin

**Scope:** source-only evidence for the original Wii Remote speaker and software consumers; tracking anderstvoss/virtualgamepad#158. This is not a Wii Remote Plus, MotionPlus topology, ADR-0024 audio architecture or physical-fidelity decision. **No host, Bluetooth or physical hardware tests were run.** All suggested experiments are **not run**.

## Consumer decision table

| Consumer, pinned revision and licence | Enable 0x14, mute 0x19, stream 0x18 | Register sequence, format / divisor / volume | Pacing and response gates | Outcome |
| --- | --- | --- | --- | --- |
| libogc WPAD/wiiuse `ef718e2d7df5e5b1750a9e1a67c17350bdd30d3e`; wiiuse GPL-3.0 with libogc independent-module linking exception | All three originated | Mute → enable → A20009=01 → A20001=08 → 7-byte A20001 config → A20008=01 → unmute → status; config format 0x00 ADPCM, divisor 0x07d0 LE, volume 0x40; disable mutes then clears A2 and enable | 20 encoded bytes each 6,666,667 ns alarm; queue advances on matching 0x22 ACK; 0x20 status speaker bit used | **Positive audio producer; potential unrequested data-ACK queue dependency** |
| CWiid `fadf11e89b579bcc0336a0692ac15c93785f3f82`; GPL-2.0-or-later | All three originated by beep | Enable → mute → A20009=01 → A20001=08 → 7-byte A20001 config → A20008=01 → unmute; format 0x00 ADPCM, divisor 0x0c00 LE, volume 0x40; disable mutes then disables | 100 fixed 20-byte blocks, nominal 10,204,081 ns interval; HID transaction handshake per control-socket send and synchronous write completion | **Positive fixed-beep producer**, not a generic PCM stream |
| Upstream wiiuse/wiiuse `e769bd73860a4f941bd110ebae5a790f968b71e3`; GPL-3.0-or-later | No speaker command API or speaker sends in inspected public header/main source | None shown in inspected source | Speaker-state flag alone is not a send path | **Not established as speaker originator**; distinct lineage from libogc |
| WiimoteLib `34516b59818d068f1fdf2925d07b7a70ad95c514`; MIT | No 0x14/0x18/0x19 sender in pinned Wiimote.cs | No speaker A2 configuration | Generic input 0x22 ACK handling and 0x20 status wait apply to other functions | **No positive speaker sender** in inspected file |
| Cemu `29f2f1fae4631e2317977debd9eacd55cc28dd7d`; MPL-2.0 | Header names all three IDs; provider does not send them | No speaker A2 configuration in inspected provider | Status/LED/IR/extension state machine does not establish an audio stream | **Constants only; no positive audio sender** |
| Dolphin `e1d35f666cc35f6ead55d32ea2679df44d04da72`; GPL-2.0-or-later | Existing source-backed enable/mute/data, passthrough and mixer | Existing source-backed formats 0x00 ADPCM and 0x40 signed 8-bit PCM, divisor and volume interpretation | Real transport gated by app preference; host-time scheduled sends, not a fixed audio rate | **Existing** `audio-wii-dolphin-*` claims, not duplicated |
| Linux hid-wiimote `734bef548a96e8774d6eef5dfa2026c6edc4e80b`; kernel GPL-2.0 | None originated in inspected driver files | No driver speaker configuration | Other userspace can still use HID/raw | Existing `audio-wii-linux-hid-driver-does-not-send-speaker` |

The selected consumers implement **different speakers of the protocol**: a game/runtime producer (libogc WPAD), a test beep (CWiid), emulator passthrough (Dolphin), and libraries which either parse only inputs/status or merely define the speaker constants. An absent sender in one inspected source file is not a universal statement about all applications using that library.

## Pinned source reading and agreements

- **libogc init and fields:** [speaker.c](https://github.com/devkitPro/libogc/blob/ef718e2d7df5e5b1750a9e1a67c17350bdd30d3e/wiiuse/speaker.c#L65-L136) and [wiiuse_internal.h](https://github.com/devkitPro/libogc/blob/ef718e2d7df5e5b1750a9e1a67c17350bdd30d3e/wiiuse/wiiuse_internal.h#L73-L127). Speaker state is recovered from [events.c](https://github.com/devkitPro/libogc/blob/ef718e2d7df5e5b1750a9e1a67c17350bdd30d3e/wiiuse/events.c#L118-L159). Its controller-front API and alarm are [wpad.c](https://github.com/devkitPro/libogc/blob/ef718e2d7df5e5b1750a9e1a67c17350bdd30d3e/wiiuse/wpad.c#L1866-L1969) and [wpad.c](https://github.com/devkitPro/libogc/blob/ef718e2d7df5e5b1750a9e1a67c17350bdd30d3e/wiiuse/wpad.c#L198-L220). PCM input is converted to Yamaha 4-bit ADPCM **high nibble first**; that is not a claim that wire-format 8-bit PCM was transmitted.
- **libogc ACK hazard:** [wiiuse.c](https://github.com/devkitPro/libogc/blob/ef718e2d7df5e5b1750a9e1a67c17350bdd30d3e/wiiuse/wiiuse.c#L17-L52) and [wiiuse.c](https://github.com/devkitPro/libogc/blob/ef718e2d7df5e5b1750a9e1a67c17350bdd30d3e/wiiuse/wiiuse.c#L295-L360) enqueue one command at a time. [events.c](https://github.com/devkitPro/libogc/blob/ef718e2d7df5e5b1750a9e1a67c17350bdd30d3e/wiiuse/events.c#L79-L115) dequeues a matched input ACK. For report 0x18 the builder encodes length but does not set ACK-request bit 1, unlike the simple 0x14 and 0x19 control sender. **Inference:** absent input 0x22 for speaker data, that particular queue may stall. Test with a synthetic endpoint; do not assume retail always ACKs report 0x18.
- **CWiid:** [command.c](https://github.com/abstrakraft/cwiid/blob/fadf11e89b579bcc0336a0692ac15c93785f3f82/libcwiid/command.c#L285-L347) gives the complete fixed-beep order and timing; [cwiid_internal.h](https://github.com/abstrakraft/cwiid/blob/fadf11e89b579bcc0336a0692ac15c93785f3f82/libcwiid/cwiid_internal.h#L61-L75) identifies the report IDs. [command.c](https://github.com/abstrakraft/cwiid/blob/fadf11e89b579bcc0336a0692ac15c93785f3f82/libcwiid/command.c#L53-L80) and [util.c](https://github.com/abstrakraft/cwiid/blob/fadf11e89b579bcc0336a0692ac15c93785f3f82/libcwiid/util.c#L59-L100) enforce HID control handshakes and ordered scripts; [command.c](https://github.com/abstrakraft/cwiid/blob/fadf11e89b579bcc0336a0692ac15c93785f3f82/libcwiid/command.c#L207-L281) blocks for memory-write completion.
- **Negative consumer boundaries:** [wiiuse.h](https://github.com/wiiuse/wiiuse/blob/e769bd73860a4f941bd110ebae5a790f968b71e3/src/wiiuse.h#L130-L155) and [wiiuse.c](https://github.com/wiiuse/wiiuse/blob/e769bd73860a4f941bd110ebae5a790f968b71e3/src/wiiuse.c#L535-L805) do not supply the libogc speaker producer. The already recorded `wii-gap-consumer-wiimotelib-windows`, `wii-gap-consumer-cemu-provider` and `wii-gap-consumer-cemu-messages` pin the WiimoteLib and Cemu inspected files; Cemu has constants in WiimoteMessages.h but no speaker producer in its provider. Existing `audio-wii-dolphin-control-and-stream-reports`, `audio-wii-dolphin-pcm-adpcm-rate`, `audio-wii-dolphin-real-speaker-pacing`, `audio-wii-dolphin-real-speaker-gate`, `audio-wii-dolphin-speaker-register-model`, `audio-wii-dolphin-yamaha-adpcm-nibbles` and `audio-wii-dolphin-volume-range-discrepancy` remain unmodified.

### Cross-consumer distinctions (not contradictory hardware evidence)

Both positive non-Dolphin senders use report 0x14 enable, report 0x19 mute, report 0x18 data, memory write 0x16, 4-bit ADPCM selector 0x00, and volume 0x40. Libogc mutes **before** enabling; CWiid enables **before** muting. Libogc's divisor is 0x07d0 and CWiid's is 0x0c00. Under the **existing Dolphin model** only, these map to nominal ADPCM rates of 3,000 Hz and 1,953.125 Hz respectively (6,000,000/divisor); neither software-selected rate is a physical measurement. Their 20-byte send schedules (6.667 ms and 10.204 ms nominal) are not the same as sample rates, and neither demonstrates how the real hardware buffers or handles overrun. No new `conflicts_with` links are justified: these are different consumer choices, not refutations of another claim. Dolphin's 0x40 PCM decoding remains a decoder capability, without proof that these two non-Dolphin senders use PCM.

Libogc's Yamaha nibble order agrees with `audio-wii-dolphin-yamaha-adpcm-nibbles`. Its volume 0x40 is compatible with the existing `audio-wii-dolphin-volume-range-discrepancy` caveat; it does not resolve the existing 0x40 versus 0x7f ADPCM volume limit dispute. These forks and emulator paths are not independent physical corroboration.

## Virtual Wiimote compatibility requirements

| Consumer | Accept / retain | Replies required by inspected source | Proposed synthetic check (not run) |
| --- | --- | --- | --- |
| libogc WPAD | Ordered report 0x14/0x19 state; 0x16 A2 memory writes; report 0x18 with five-bit length at most 20 bytes and rumble bit; decoder format, divisor, volume fields | Status report 0x20 with speaker-enabled bit for `WPAD_IsSpeakerEnabled` and initialization; matched input 0x22 ACKs for queue progression, **especially risk of ACK missing on 0x18** | Replay enable/config/status and sequential 0x18 blocks; compare ACK requested/omitted and queue drain |
| CWiid beep | Same three report IDs and ordered 0x16 A2 writes; 20-byte fixed payload | Success HID-control handshake after each report; memory-write completion and errors through normal write response path; not a demonstrated per-data 0x22 wait | Emulate transaction handshakes and write replies, then send 100 timed blocks |
| Dolphin | Reuse already accepted 0x14/0x19 control ACK expectations; parse 0x18 data and A2 configuration; preserve real/emulated path distinction | Existing `audio-wii-dolphin-control-and-stream-reports` and W8 speaker-mute ACK acceptance requirements | Existing emulator and host checks; no test here |
| WiimoteLib / Cemu / upstream wiiuse | No special speaker behavior established beyond base Wii status/report support from inspected sources | None audio-specific established | Do not claim audio acceptance from their non-audio probes |

**Implementation boundary:** This is a protocol/consumer checklist only. Decoder/playback architecture and audio routing remain in virtualgamepad ADR-0024 and issue #344, not in this evidence PR. Retain unknown response behavior rather than invent an unconditional device-side report 0x18 ACK policy.

## Unresolved gaps and experiments — all not run

- **WiiBrew Speaker source gap:** The recorded `wii-gap-wiibrew-wiimote-oldid123257` locator does **not** contain the Speaker section. Direct wiibrew.org is unreachable in this cloud research setting; no fetched-and-hashed pinned web.archive.org Speaker section was available here. Do not use that existing locator as independent proof of register semantics.
- **Physical device:** Whether 0x18 succeeds with or without input ACK, FIFO size/overrun, error code behavior, actual ADPCM sample clock, volume 0x40/0x7f boundary, decoder reset on mute/enable and effect of final config write remain `unknown` in `wii-gap-speaker-physical-decoder-behavior-unknown`, building on `audio-wii-speaker-physical-acceptance-unknown`.
- **Owner-controlled future test (not run):** On a physical original Wii Remote and an explicitly authorized virtual endpoint, capture the ordered control/register/status exchanges, compare speaker enable state and error replies, vary 0x18 ACK behavior, sweep non-sensitive rate/volume fields, measure packet timing/overruns with bounded stimuli, and compare audible output. Do not collect radio identities, serials, keys, memory dumps or firmware.
- **Out-of-scope:** Early integrated Plus, external MotionPlus, remote identity, native Bluetooth feasibility, and generalized audio routing. No host, physical, or software simulator experiment was run.

## New claim IDs

- `wii-gap-speaker-libogc-startup-status` — `source_supported`, `consumer`
- `wii-gap-speaker-libogc-frames-pacing` — `source_supported`, `consumer`
- `wii-gap-speaker-libogc-stream-ack-queue-risk` — `inferred`, `consumer`
- `wii-gap-speaker-cwiid-beep-sequence` — `source_supported`, `consumer`
- `wii-gap-speaker-cwiid-ack-gates` — `source_supported`, `consumer`
- `wii-gap-speaker-cemu-wiimotelib-no-speaker-origin` — `source_supported`, `consumer`
- `wii-gap-speaker-upstream-wiiuse-not-originating` — `source_supported`, `consumer`
- `wii-gap-speaker-cross-consumer-compatibility` — `inferred`, `consumer`
- `wii-gap-speaker-physical-decoder-behavior-unknown` — `unknown`, `device`

New inventory: **248** `wii-*.json` claims (239 on the source main snapshot + 9 new speaker claims); existing `audio-wii-*` claims are not included in `tests/test_wii_ledger.py`'s `wii-*.json` assertion.
