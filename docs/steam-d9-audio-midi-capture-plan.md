# D9 wired haptic audio and MIDI capture plan

Status: physical trials completed; see the dated evidence report. Builds on research PR #105 and
virtualgamepad PR #305. The owner explicitly requested supervised audio/MIDI
capture, implementation and automated virtual-device end-to-end tests. This is
a separate active-output study, beyond the earlier passive Session 3 scope.

## Meaning and scope

Use only the real direct-wired Steam Controller 2026 (`28de:1302`). MIDI files
are host-side input to SteamHapticsSinger; capture its resulting HID requests.
Do not invent a USB MIDI or Audio Class interface. PCM is the haptic streaming
path exercised by SteamHapticsPlayer, not desktop audio-device enumeration.
No Puck, receiver, Bluetooth, bootloader, firmware update or host-policy changes.
Never send feature commands `0x90` or `0x9f`.

Reference clients are source-reviewed and built outside both repositories:

- SteamHapticsSinger `d809a28acb1e4f5aeb92fe50ef06869eb7b07060`.
- SteamHapticsPlayer `e06e48d1570eab51a19c933dfaac1dfcb5157b9c` with
  TritonLib `d470e0d3bb6309505a201561278b72d1a9dc16f2`.
- Existing iczero pin `83c46d7` supplies hypotheses, not physical truth.

## Ordered physical trials

1. **MIDI pilot:** generated SMF format 0, 480 PPQN, tempo 500000 us/quarter,
   channel 0 notes 57 then 69, velocity 32, 192 ticks (200 ms) each, separated
   by silence. All four player gain modifiers are -20; no direct-velocity gain
   and no looping. The upstream app maps channel 0 to the right internal
   haptic; actual location/pitch/stop are owner observations, not assumed.
2. **MIDI correspondence:** after the pilot, repeat separated note pairs on
   each of the four MIDI channels, with clear preparation/countdown windows.
   Capture note-on/off, exact report size and padding, frequency/gain/duration,
   successful writes and any return reports. No overlapping notes.
3. **PCM pilot:** generated short, low-amplitude stereo waveform, with silence
   before/after and distinct left/right windows, through the unmodified pinned
   player. Record its configure/disable operations and full data framing,
   including any rejection or underrun. Explicitly disable the configured
   stream targets after playback, including on error/interrupt.
4. **Framing/flow follow-up:** only after clean pilots, test the remaining
   source-declared data forms and bounded start/data/stop/restart sequences.
   Distinguish successful USB completion from accepted configuration and
   actuator feedback. Do not fabricate malformed physical traffic to populate
   an error table; use fake-provider tests for speculative invalid cases.

For each trial the owner starts a bounded full-snaplen bus-scoped usbmon capture
with root; the agent never runs sudo. The helper logs relative boundaries for
later reduction; full logs/absolute markers and raw pcaps remain private.
Keep Steam, Dolphin and other SDL clients closed. Check exactly one intended
wired target and record the USB version marker; firmware attributes must be
passively observed and safely identified or recorded as not observed. Stop on
an update prompt or unexpected persistent output; do not accept an update.

## Reduction and evidence

Pair USB requests/completions using private metadata. Publish only reviewed
non-identifying report selections, generated stimulus descriptions/hashes,
relative timing, statuses and owner feedback. Serial/attribute identifiers,
addresses/URBs, host paths, accounts, absolute clocks and opaque unrelated
feature data remain withheld. Preserve unclassified `0x44` bytes privately
until their meaning and identification risk are reviewed. Record the playback
client and binary hashes, configuration, final stops and device cleanup.

## Implementation and virtual end-to-end tests

Implement only captured semantics in the Steam package, refresh its API snapshot
with any API delta, and preserve the existing synthetic serial and default
profile. Make provider limits explicit: uinput cannot carry HID streaming data.
Expose stream data/state without unbounded history or silently dropped chunks.
Do not add a USB audio/MIDI interface unsupported by the wired descriptor.

Run the same upstream clients with the same generated stimuli against one
owned virtual UHID device, physical hardware disconnected. Verify discovery,
exact outputs, bytes/channel routing, measured feedback, stop/restart, repeated
polling, per-controller removal, application shutdown and idempotent cleanup.
Use deterministic fake transport tests for all declared report types, precise
request acknowledgements, queue bounds and error paths; no host request may be
left pending. Preserve prior regressions. Run the complete required repository,
API, script, research and leak checks before PR publication.
