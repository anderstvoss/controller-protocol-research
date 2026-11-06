# D9 wired MIDI-to-haptics and PCM reference, 2026-11-05

These are supervised physical observations, built on research PR #105 and the
separate virtualgamepad PR #305. See the [capture plan](steam-d9-audio-midi-capture-plan.md).
Only direct-wired `28de:1302` was used. Steam, Dolphin and SDL were closed.
The owner operated bounded full-snaplen usbmon; the agent never ran sudo or
changed host policy. No firmware update, bootloader, Puck/receiver/Bluetooth or
feature command `0x90`/`0x9f` was used. Each capture records `bcdDevice=0404`
as a version marker; a firmware attribute was not observed by this reduction.

## Reference clients and stimuli

- [SteamHapticsSinger](https://github.com/CrazyCritic89/SteamHapticsSinger/blob/d809a28acb1e4f5aeb92fe50ef06869eb7b07060/main.cpp)
  `d809a28`: unmodified player, all gain modifiers -20, no looping or direct
  velocity. Generated SMF0, 480 PPQN, tempo 500000 us, MIDI notes 57/69 held
  192 ticks (200 ms) each, with silence. First channel 0, then separately
  labelled channels 0,1,2,3. MIDI is host-side input; no USB MIDI endpoint.
- [SteamHapticsPlayer](https://github.com/Pixel1011/SteamHapticsPlayer/blob/e06e48d1570eab51a19c933dfaac1dfcb5157b9c/playPCMSrc/main.cpp)
  `e06e48d`, TritonLib `d470e0d`: unmodified wired 8-kHz s16le stereo player.
  Initial two-second generated WAV: peak 1024/32767, left 220 Hz and right
  440 Hz for 250 ms each, fades and silence. The owner noted that this low
  level limited audibility. The separate moderate repeat used peak 4096/32767,
  equal 440-Hz 500-ms windows on left/right, same holding condition requested.
- [iczero PCM client](https://github.com/iczero/steam-controller-stuff/blob/83c46d7c5711f7497f83336526755fbf50d0c5af/hid-sctrl/src/bin/audio-test.rs)
  `83c46d7`: same moderate waveform as raw PCM, with its own float32 0.9
  scaling, per-target packets and status handling. A reviewed companion sends
  only output `86 01 02 00` and `86 01 05 00` after each PCM client, including
  the error path, because EOF alone does not establish an explicit stream stop.

No new system packages were needed. Client revisions/binary hashes, stimulus
hashes and capture hashes are retained in the linked evidence. The players and
iczero share implementation knowledge; they are not independent corroborating
source lineages. The physical captures are the additional observations.

## MIDI observations

| Capture | Output | Completion | Feedback | Owner observation |
| --- | --- | --- | --- | --- |
| Pilot | 12 `0x83`, 64 wire bytes | all status 0 / 64 bytes | no `0x44` | first mainly felt; second more audible and higher |
| Four channels | 48 `0x83`, 64 wire bytes | all status 0 / 64 bytes | no `0x44` | grip pairs somewhat audible; pad pairs mainly felt |

Each `0x83` has its declared nine-byte body followed by **54 zero padding
bytes**. The app maps MIDI channels 0/1/2/3 to selectors 4/3/1/0. Its note-on
frequency fields are 226/450 for the grip channels and 220/440 for pads, gain
-20 and duration field 32767. Note-off uses gain -128, frequency 0, duration
field 32768. Final and process-exit cleanup repeat all-channel note-offs.
These raw fields are preserved; duration-bit meaning, calibrated tuning and
independently localized left/right actuators are not inferred.

Records: `steam-d9-midi-lfo-framing`, `steam-d9-midi-channel-routing`, experiments
`steam-d9-midi-pilot` / `steam-d9-midi-channels`.
[Evidence](../evidence/steam-d9-midi-pilot.json),
[four-channel evidence](../evidence/steam-d9-midi-channels.json),
[60 selected complete packets](../fixtures/steam-d9-midi-lfo-reference.hex).

## PCM framing, feedback and byte correspondence

| Capture | Data packets | Bytes per channel | All output completions | Owner observation |
| --- | --- | --- | --- | --- |
| Low-level Pixel | 1066 `0x88`, 64 wire bytes | 31980 | status 0 | left felt/quiet; right felt/audible |
| Moderate Pixel | 1333 `0x88`, 64 wire bytes | 39990 | status 0 | both clean, clearly felt/heard, same tone |
| Moderate iczero | 1290 `0x87` at 64 bytes + two at 12 bytes | 40000 | status 0 | both clean, clearly felt/heard, same tone |

All meaningful bytes match the generated waveform after the clients' known
transformations. Pixel skips the first 60 stereo bytes and pads its last chunk;
each `0x88` declares length 30 in two 31-byte slots. The two unused bytes were
zero throughout both captures. iczero splits channels, scales by float32 0.9,
and writes selectors 0/4, including ten-data-byte final chunks. Byte hashes and
selection ordinals are in [PCM evidence](../evidence/steam-d9-pcm-playback.json).

Pixel sends output `0x86` stop group 2/5, then configure group 2/5 in mode 0.
Input `0x44` shows status `0x20` for IDs 1/0 and `0x10` for IDs 4/3: the
internal 8-kHz configuration is accepted, the pad configuration rejected.
**Successful USB completion is not configuration acceptance.** Explicit final
stops again target groups 2/5. All observed host writes paired with completions;
no pending observed write remained.

Each captured `0x44` has six wire bytes: target, status, three zero bytes after
the ID. Status bytes 01/02/04/08/10/20 occur; source labels describe overrun,
stopped, low/high buffering, rejection and acceptance. Two `01` indications
occurred on feedback ID 1 in the iczero trial. This does not establish lost
sample counts, a native FIFO capacity, exact thresholds, or one ACK per write.
No malformed physical traffic was injected to manufacture error cases.

Records: `steam-d9-pcm-framing-feedback`, `steam-d9-pcm-stimulus-correspondence`,
experiment `steam-d9-pcm-playback`.
[80 selected complete input/output packets](../fixtures/steam-d9-pcm-stream-reference.hex).
Raw captures, opaque feature contents, serials, paths/accounts, addresses/URBs
and absolute marker clocks remain outside both repositories. Selected packets
are unmodified known report selections, not byte-replaced reconstructions.
Capture-drop counters were not supplied; do not infer zero loss.

## Scope limits

This demonstrates MIDI rendered as haptic tone requests and PCM delivered to
internal haptics. It establishes no USB Audio Class/MIDI interface, separate
speaker/microphone, calibrated pitch/loudness, output `0x89`, other stream
formats, retail FIFO capacity, or wireless behavior. Virtual compatibility is
checked separately with the same clients and stimuli; it does not promote a
compat buffering model into physical truth.
