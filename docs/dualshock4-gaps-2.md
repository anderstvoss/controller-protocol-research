# DualShock 4 conflicts and unknowns — controller gaps 2

**Scope:** source-only follow-up to the L0 device ledger for #155. No host run, physical device operation, pairing write, firmware analysis, or virtualgamepad code change was performed in this research session. The physical observation below is **reported by a third party**, not executed or independently reproduced here.

## Ranked gap decision table

| Rank | Gap and decision | Playable or faithful | Evidence ceiling | Existing claim / tracking |
| --- | --- | --- | --- | --- |
| 1 | Feature report 0x12: **narrow source-evidence advancement** for a reported v2 USB read and field positions; all other variants remain unknown | **Playable** for driver identity/probe compatibility; **faithful** device layout only within the reported v2 scope | `source_supported` **external self-report**, not corpus physical validation | New `ds4-cgap-feature12-v2-usb-read` supersedes the broad unknown only in its stated scope; `ds4-l0-device-feature12-pairing-unknown`; #155 |
| 2 | Feature report 0x81: **no new pinned device observation** resolves its actual revision coverage or coexistence with 0x12 | Playable: older hid-sony probe; faithful: variant matrix | Existing consumer-source expectations only; retail unknown | `ds4-l0-device-feature81-mac-unknown`; #155 |
| 3 | Touch-history count: **conflict retained** between community wording and kernel struct's historical sample slots | Faithful touch behavior, not basic buttons | Kernel consumer parser and secondary summary; no new retail capture | `ds4-l0-device-touch-count-conflict`; #155, physical #283–#286 |
| 4 | SDL feature 0xA3 request: **existing no-evidence finding unchanged**; the pinned SDL version has no proven request gate | Playable host acceptance, consumer side | Source-scoped negative finding, no host trace or new call-path proof | `ds4-l0-consumer-sdl-a3-no-evidence`; #155 |

## Pinned-source review and actual advancement

A new pinned [ControlDeck research note](https://github.com/ViniZap4/ControlDeck/blob/46151468605ba4d9e5c6378079bb56cd3c934333/DS4_PAIRING_SCOPE.md#L92-L107) states that a read-only macOS HID feature request for report 0x12 succeeded against **one physical DualShock 4 v2 over USB**, Sony product 0x09CC. The reported response length is 16 bytes, with controller identity fields at positions **1 through 6** and stored peer identity fields at **10 through 15**, both interpreted little-endian. These are positions within the complete feature report, including its report-ID field. **No address contents, captured report bytes, key material, or personal identifiers are reproduced here.**

The corresponding [read-only probe source](https://github.com/ViniZap4/ControlDeck/blob/46151468605ba4d9e5c6378079bb56cd3c934333/spikes/DS4PairSpike/Sources/DS4PairSpike/DS4PairSpike.swift#L55-L105) selects a Sony device on USB, requests feature report 0x12, checks success and interprets those positions. The code corroborates the *method used*, **not** the independently observed result; both files come from the same ControlDeck project. The report of successful physical contact is self-reported in its research note and has not been verified by this agent.

The sources are recorded once each in `records/source/ds4-cgap-controldeck-pairing-scope.json` and `records/source/ds4-cgap-controldeck-pairing-spike.json`. Both cite immutable revision `46151468605ba4d9e5c6378079bb56cd3c934333`, exact-file SHA-256 values, upstream MIT licence and line locators. Neither file is redistributed.

### Claim-level decision

- **`ds4-cgap-feature12-v2-usb-read`** is `source_supported`, `device`, `source_only`. It narrowly supersedes `ds4-l0-device-feature12-pairing-unknown` for the externally reported DS4 v2 USB read only. This is stronger than previous kernel-consumer expectations alone, but it does **not** promote any physical validation in this corpus.
- The existing broad unknown still applies to DS4 v1, other firmwares and wireless-adapter paths, and to a write or reconnection handshake; no write was observed. Driver choice (historical 0x81 versus newer 0x12) remains consumer- and revision-sensitive. Do not infer that the two reports are universally interchangeable or that one report is absent when the other is present.
- **`ds4-l0-device-feature81-mac-unknown`** is unchanged. The older kernel's seven-byte 0x81 expectation is not a newly verified retail v2 response, and the newly inspected v2 source does not probe 0x81.
- **`ds4-l0-device-touch-count-conflict`** is unchanged. Three USB or four Bluetooth nine-byte *history samples* can each hold two touch-contact slots; that does not imply three or four simultaneous fingers. A fresh, independently pinned retail source is still needed to resolve the community wording.
- **`ds4-l0-consumer-sdl-a3-no-evidence`** is unchanged. No newly pinned evidence demonstrates SDL's PS4 HIDAPI driver requests 0xA3; Linux drivers differ in their treatment of that report.

## Virtualgamepad consequence

For a **compatibility** implementation of the DS4 v2 USB personality, the source now supports checking the sixteen-byte report 0x12 reply and the positional identity fields against the existing pinned newer-kernel consumer expectations. Do not hard-code a copied physical identity or treat the reported peer field as a replacement for caller-supplied pairing identity. There is no new evidence that virtualgamepad's current reply fails; **no implementation change is claimed necessary**.

For **faithfulness**, do not upgrade the support matrix on this source-only evidence. Maintain unknown device-side revision differences, pairing writes, 0x81/0x12 coexistence, touch-history behavior, and SDL runtime gating until independent evidence exists.

## Future owner-only physical validation — proposed, not run

On an authorized DS4 v1 and v2 reference, privately log sanitized success/failure, returned length and report structure for read-only feature reports 0x81 and 0x12; compare to the pinned consumer drivers. Do not publish device identities or payloads containing identities. Use separate USB and Bluetooth sessions to investigate touch-history sample counts and release sequences. Run version-pinned SDL discovery and optional 0xA3 request traces in an isolated environment, without touch injection into the active desktop. Physical validation issues #283–#286 remain physical; lightbar blink #287 is parked and excluded.

**Evidence classification:** external source review only; no hardware test by this agent.
