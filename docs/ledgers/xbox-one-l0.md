# Xbox One L0 evidence ledger — post-Alpha 2

**Scope:** controller `xbox-one`; virtualgamepad tracking `#355`; source-only review at Linux `4056b3c9d3c92ea45955641dbafeb9b960e146ef`, SDL `d4557c1511c721485dc4960f7149730afc9a73a0` and xpadneo `56b538d951300bf804f6631738603c5eb14c04f0`. No host or physical experiment was performed. The [starter brief](../xbox-one-starter.md) contains the decision table, source lines, implementation proposal, and proposed tests.

| Evidence area | New claim | Status / role | Pinned supporting records | Boundary |
| --- | --- | --- | --- | --- |
| usb id matrix | `xboxone-pa2-usb-id-matrix` | `source_supported` / `consumer` | `xbox-series-linux-xpad` | source_only; no host or device acceptance |
| xpad evdev no share | `xboxone-pa2-xpad-evdev-no-share` | `source_supported` / `consumer` | `xbox-series-linux-xpad`, `xbox-series-xpad-ff-memless` | source_only; no host or device acceptance |
| xpad wired gip boundary | `xboxone-pa2-xpad-wired-gip-boundary` | `source_supported` / `consumer` | `xbox-series-linux-xpad`, `xbox-xone-wired` | source_only; no host or device acceptance |
| linux bt model1708 | `xboxone-pa2-linux-bt-model1708` | `source_supported` / `consumer` | `xbox-cgap-kernel-hid-ids`, `xbox-cgap-kernel-hid-microsoft` | bluetooth; no host or device acceptance |
| sdl legacy bt reports | `xboxone-pa2-sdl-legacy-bt-reports` | `source_supported` / `consumer` | `xbox-series-sdl-xboxone` | bluetooth; no host or device acceptance |
| sdl share exceptions | `xboxone-pa2-sdl-share-exceptions` | `source_supported` / `consumer` | `xboxone-pa2-sdl-joystick`, `xbox-series-sdl-xboxone` | source_only; no host or device acceptance |
| ble descriptor ambiguity | `xboxone-pa2-ble-descriptor-ambiguity` | `source_supported` / `consumer` | `xbox-cgap-xpadneo-docs`, `xbox-cgap-xpadneo-legacy-desc` | bluetooth; no host or device acceptance |
| own family decision | `xboxone-pa2-own-family-decision` | `inferred` / `consumer` | `xbox-series-linux-xpad`, `xboxone-pa2-sdl-joystick`, `xbox-series-sdl-xboxone`, `xbox-cgap-kernel-hid-microsoft` | source_only; no host or device acceptance |
| first uinput | `xboxone-pa2-first-uinput` | `inferred` / `consumer` | `xbox-series-linux-xpad`, `xbox-series-sdl-xboxone`, `xbox-cgap-kernel-hid-microsoft` | source_only; no host or device acceptance |
| physical reference gaps | `xboxone-pa2-physical-reference-gaps` | `unknown` / `device` | None | not_measured; no host or device acceptance |

## Existing evidence reused, not duplicated

- `xbox-series-xpad-identity-share`, `xbox-series-xpad-axis-domains`, `xbox-series-xpad-evdev-shape` and `xbox-series-xpad-trigger-rumble-limitation` establish the *common Linux xpad consumer* and are not separate One device observations.
- `xbox-cgap-linux-binding`, `xbox-cgap-descriptor-variants`, `xbox-cgap-sdl-firmware-buttons` and the detailed xpadneo consumer claims contain Series-focused comparisons with older model 1708, but do not independently register Xbox One variants.
- `xbox-xone-*` describes an out-of-tree GIP/receiver *consumer* and is not evidence of a real USB GIP or receiver realization in virtualgamepad.
- All new consumer claims have empty `experiments`. The single new source record `xboxone-pa2-sdl-joystick` hashes an otherwise unrecorded pinned SDL core file; kernel, SDL HIDAPI and xpadneo source files reuse existing revision-and-file hashes.

## Unresolved gates

- **First realization:** `linux.uinput` with standard Xbox One no-Share xpad evdev, caller-selected identity; not implemented or tested here.
- **Family:** distinct `xbox-one` family (`parent: null`), with explicit model/firmware variants; this is an architectural recommendation, not completed runtime work.
- **Bluetooth UHID:** deferred until independent revision-specific reference report/descriptor and host tests; physical pairing remains out of scope for local UHID.
- **Faithful wired USB:** blocked on real GIP feasibility, never fake GIP. Conventional evdev playability does not constitute USB protocol identity.
- **Physical evidence:** `xboxone-pa2-physical-reference-gaps` stays unknown. No hardware capture, enumeration, battery, motor, audio or consumer acceptance was performed.

## Provenance

Kernel xpad/hid-microsoft and their HID identifiers are GPL-2.0-or-later; SDL source is zlib-licensed; xpadneo documentation is GPL-3.0-or-later. All observations are paraphrased and source-pinned in the brief and source records. No third-party code, HID descriptor bytes, private device identifiers or firmware are copied.
