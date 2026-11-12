# Xbox Elite Series 1 L0 evidence ledger

**Scope:** source-only post-Alpha 2 starter for `anderstvoss/virtualgamepad#359`. No physical device, receiver, Linux host, SDL runtime, or virtual acceptance test was run. No original USB descriptor, raw report or vendor firmware material was captured.

| Question | Claims | Evidence level / boundary |
| --- | --- | --- |
| Original USB identity | `elite1-pa2-xpad-usb-identity` | Source-supported consumer; Linux v7.3 xpad original Elite 0x045e:0x02e3, not Elite 2 or Series |
| Post-driver event capabilities | `elite1-pa2-xpad-event-surface` | Source-supported consumer; fifteen keys including four grip paddles, eight axes and conditional FF |
| Paddle suppression on remap | `elite1-pa2-xpad-paddle-guard` | Source-supported consumer; original fixed packet branch and custom-mapping guard |
| SDL USB HIDAPI decoder | `elite1-pa2-sdl-gip-paddle-parser` | Source-supported consumer; newer pinned decoder, not measured active Linux path |
| SDL Linux evdev paddles | `elite1-pa2-sdl-linux-evdev-paddles` | Source-supported consumer; conditional automatic mapping; no SDL execution |
| SDL built-in default mapping | `elite1-pa2-sdl-base-db-entry` | Source-supported consumer; ordinary original Elite USB mapping, no explicit paddles |
| Transport assumption | `elite1-pa2-transport-no-bluetooth-inference` | Inferred device scope; wired USB/Xbox Wireless, not verified non-Bluetooth hardware |
| Priority recommendation | `elite1-pa2-uinput-first` | Inferred consumer design; `linux.uinput` compatibility is not USB-GIP fidelity |
| Outstanding evidence | `elite1-pa2-unmeasured-reference-gaps` | Unknown device scope; all proposed tests not run |

## Source provenance

- `elite1-pa2-linux-v7-3-xpad`: Linux `v7.3`, exact xpad file SHA-256 `b47281151829fc382c4bcb5f466865f476a6f4ebfacd617ee49393f99c1e3950`, GPL-2.0-or-later. Its bytes also match the existing `xbox-series-linux-xpad` snapshot, which is not modified.
- Reused SDL sources: `sdl-linux-joystick-baseline` and `x360-l0-sdl-gamepad-db` at `release-3.2.0`, plus `xbox-series-sdl-xboxone` at a different pinned SDL commit. SDL licence: zlib. `xbox-series-xpad-ff-memless` and `xbox-xone-receiver` are existing consumer-only comparators.
- Existing `xbox-series-*`, `xbox-cgap-*` and `xbox-xone-*` claims are cited, not copied. No Elite Series 2 PR was open when surveyed.

The brief [records the decision and unrun tests](../xbox-elite-series-1-starter.md). Device transport absence and application paddle visibility are not physically validated, and the first proposed realization does not fake GIP.
