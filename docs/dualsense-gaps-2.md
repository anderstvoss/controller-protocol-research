# DualSense LED source gaps — controller gaps 2

**Scope:** source-only examination of LED brightness, mute LED pulse and player LED instant-change control. No host, physical controller or vendor firmware analysis was performed. New source hashes cover the exact pinned files; no source contents are redistributed.

## Ranked gap decisions

| Rank | Gap / prior record | Playable or faithful | Source evidence ceiling | New claim / virtualgamepad issue | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | Brightness byte and value range — `ds-l0-led-led-brightness-levels` (`unknown`) | Faithful: LED intensity and target LEDs | Conflicting consumer encodings; not a physical validation | `ds-cgap-led-brightness-encoding-disagreement` / #154 | **conflicted**: 0–2 vs 1–3; no universal LED brightness behavior established |
| 2 | Mute LED pulse mode — `ds-l0-led-mute-led-pulse-mode` (`inferred`) | Faithful: mute LED animation | Two separately maintained source implementations agree on mode 2, but no physical observation | `ds-cgap-mute-led-pulse-source-mapping` / #154 | **source_supported**, source convention only |
| 3 | Player LED instant-change bit — `ds-l0-led-player-led-instant-bit` (`inferred`) | Faithful: transition timing | Two separately maintained source implementations use bit 5 for instant change, no timing measurement | `ds-cgap-player-led-instant-source-mapping` / #154 | **source_supported**, source convention only |

All three are fidelity gaps rather than core gameplay input blockers. Their new claims supersede the named older records **without editing the original JSON**. No claim is physically observed, independently physically validated or sufficient to promote an acceptance cell.

## Pinned source lineage

| New source record | Revision / reviewed lines | Role and caution |
| --- | --- | --- |
| `ds-cgap-nowrep-dualsensectl-main` | `d3ae2fa272e1bf9a5c08a0ded3f374b40f7c73ac`, `main.c` 71–81, 591–639, 661–680 | GPL-2.0 Linux command utility: encodes brightness 0–2 with valid_flag2 bit 0, pulse mode 2, instant bit 5. Host software intent, not retained controller observations |
| `ds-cgap-xinput-hid-dualsense` | `11cf2eac369134e74af8ebef4f502c7b7b2160fc`, `dualsense.cpp` 23–43, 90–94, 162–198 | MIT compatibility mapping: brightness 0/1/2 (bright/mid/dim), mute breathing mode 2, player bit 5 fade/instant. The source itself attributes its interface map to a 2024 community wiki snapshot; independent maintenance is **not** independent primary measurement |
| `ds-cgap-yesbotics-brightness-notes` | `24203b8ebe0bf6bd8d123bc02174b9735f811f6a`, `README_PROTOCOL.md` 310–327 | MIT protocol notes: brightness 1/2/3 (full/medium/low), claims mute plus player LED scope and a mute-flag constraint. Documentary counterevidence, not a hardware capture |

Reused sources: `audio-sdl-ps5` (SDL comment and player bit use) and `audio-linux-hid-playstation` (kernel output field). New pinned files are hashed in their source records. These independent *code repositories* may share community protocol ancestry, so count them as new consumers, not independent retail tests. No third-party code is copied into this brief.

## Decision table: implications for virtualgamepad

| Question | Source-derived result | What may be implemented as compatibility behavior | Faithful answer / open physical test |
| --- | --- | --- | --- |
| LED brightness value range | `nowrep` accepts 0–2 and enables valid_flag2 bit 0; XInput_HID labels 0 high, 1 mid, 2 dim; yesbotics instead documents 1 high, 2 medium, 3 low. Physical target scope is also not reconciled. | An **explicitly labeled compatibility policy**, if desired, may use the `nowrep` 0–2 encoding and gate bit 0; do not require it for every device or silently treat it as retail truth. | **Unknown/conflicted** physical levels, target LEDs and firmware behavior; compare outputs on a reference with revisions controlled. **Not run** |
| Mute LED pulse | `nowrep` writes mode 2, flag1 bit 0; XInput_HID names enum value 2 Breathing; SDL previously documented 0 off / 1 solid / 2 pulse. | Expose output mode 2 as a source-supported, opt-in compatibility command distinct from a host microphone-mute state. | **Unknown** physical blink period, availability and firmware acceptance. LED-only 0, 1 and 2 trial (existing inventory L6). **Not run** |
| Player LED instant bit | `nowrep` sets player LED bit 5 when the instant option is requested; XInput_HID describes bit 5 as fading when unset and immediate when set; SDL previously used 0x20. | Model bit 5 as an explicit player LED transition option, separately from the five pattern bits. | **Unknown** actual fade timing and revision dependence. Compare identical player masks with bit 5 clear/set (existing inventory L5). **Not run** |

Field indexing follows `docs/dualsense-led-inventory.md`: `led_brightness` is common byte 42 (USB report 0x02 byte 43; Bluetooth report 0x31 byte 45); `player_leds` is common byte 43; `mute_button_led` is common byte 8. The brightness-enable bit is valid_flag2 bit 0 (common byte 38), distinct from the lightbar-setup bit 1. Preserve USB/Bluetooth framing and valid-bit gating in any implementation.

## Evidence ceiling and next actions

1. Keep all physical LED responses `unknown` until owner-authorized, reproducible, revision-scoped USB and Bluetooth tests document actual transitions and brightness. Do not use the physical DualSense's broken trigger modules to infer unrelated LED results.
2. Resolve 0–2 versus 1–3 *as a source discrepancy*, not by source count. Confirm whether one source uses an API-level index and another a raw report byte; the pinned yesbotics document does not establish that distinction.
3. When authorized, run a bounded LED-only test with one LED field family per report: brightness with explicit enable flag, mute modes 0–2, and same player mask with bit 5 clear/set. Record transport, device revision, firmware revision and visual outcome **privately and without identifying raw data**. This plan is **not run**.
4. For virtualgamepad #154, treat source-supported bits as candidate compatibility semantics only. No support matrix promotion, consumer success, or hardware fidelity was demonstrated.

**Checks:** Cloud GitHub connector session only; repository-wide publication guard, validator, unit tests and pre-commit are not runnable in this session without a checked-out repository. CI on the draft PR must supply those checks.
