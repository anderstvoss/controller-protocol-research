# Changelog

All notable changes to the corpus are recorded here. The format follows
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Consumers pin
corpus commits by full SHA; schema changes that alter record shape bump the
affected schema's `schema_version`.

## Unreleased

- Record W9h kernel-bound Plus regression, isolated Original Nunchuk copy-off
  calibration gate, Original Classic mode 07 and separate Plus default/external
  ID native Dolphin passes. Preserve decoded UI versus raw data, preliminary
  sampling limits, synthetic caller provenance and generic-binding release gate.

- CI: harden-runner uses `audit` instead of `block` on the macOS and Windows
  policy-check legs; its pre-step ignores the step-level `if` and block mode
  broke Windows DNS and revocation lookups (anderstvoss/virtualgamepad#260).
  Linux jobs stay in `block`.

- Document MotionPlus activation/deactivation 0x20 status transitions, Dolphin
  emulator versus documented device evidence, conditional F6 and Linux/SDL/
  Cemu/wiiuse/xwiimote re-probes. Rank creation-time compat, retain W9f
  reporting distinction and defer physical comparison to #52.
- CI: bump `step-security/harden-runner` to v2.22.3, which fixes block mode
  dropping allowed connections on GitHub-hosted Linux runners (the cause of
  stuck CodeQL jobs, anderstvoss/virtualgamepad#260). Egress policy stays `block`.

- Record W9g kernel-first gyro regressions and generic-bound native Dolphin
  MP+Nunchuk decoding with the activation re-attach compat edge. Isolate the
  edge-off reporting pause and F6-off calibration gate; keep raw frames separate
  from the UI oracle, and preserve #258 release and physical-fidelity limits.

- Record W9f counted stimulus: sustained commits, no post-map MP+Nunchuk
  data without a new report-mode request, and a passing MP-only gyro control.
  Separate pre-map frames and producer/consumer rate denominators; no model fix.
- Record Plus P1 kernel/xwiimote gyro, SDL 3.2.10 gyro limits and bound
  Dolphin MP-only UI observations, all scoped to Tr with default built-in ID.
  Keep absent kernel ID logging and physical/status limits explicit.

- Record the W9e owner-window generic-binding retry: MP and child calibration
  transport succeeds, MP+Nunchuk changing decoded motion remains unestablished,
  the MP-only gyro control passes, and loss of kernel Wii input/xwiimote access
  is observed. Preserve the earlier bind refusal and the release policy gate.

- Separate device and consumer evidence with an optional `evidence_role` claim marker, independent status columns and transport categories, and validator regression coverage. Historical consumer-only claims are being reclassified without changing their provenance or evidence strength.
- Record the W9e per-device hid-generic bind refusal, verified wiimote restoration
  and cleanup; pin version-matched stable HID source, preserving both Dolphin
  arms and the kernel-node trade-off as unmeasured.

- Extend Steam C6 wired research with six distinct-field synthetic haptic fixtures, offset-level assertions, SDL and Linux consumer timing assumptions, and kernel mid-session lizard/hidraw ownership claims; physical timing and replies remain unverified.

- Record four W9 compat controls: bound-kernel MP+Nunchuk on/off stops at F6,
  MP-only native Dolphin mapped gyro, and fresh kernel evdev axis delivery.
  Separate native from combined output, preserve missing-node/pilot limits,
  and do not promote unreached mirrors or calibration copies.

- Pin the W9 owner-selected fixed F7 value 0x02 as compat, paraphrasing the
  Dolphin enum, activation/update path and hardware-description comment. Keep
  challenge data at 0x50 refused and distinguish policy from physical readback.

- Diagnose W8 Cemu setup order: distinguish MP status/report-mode polling from
  MP+Nunchuk IR reconfiguration after successful replies. Preserve missing
  timestamp/internal-state limits; do not invent an ACK timeout or model fix.

- Add two clean W8 Cemu imported-resource comparisons after the browser holder
  closes. All 18 MP+Nunchuk calibration reads succeed, including 17 Nunchuk
  payload matches; decoded motion remains unobserved. Preserve coexistence arms
  and distinguish transport delivery from application interpretation.

- Add four post-merge W8 imported-block consumer arm sets: changing native
  Dolphin MP mapping indicators, the MP+Nunchuk F6 identity boundary, and Cemu
  coexistence limits. Keep clean no-holder and decoded-state unknowns explicit;
  retain the factory, physical, rate, audio and game acceptance gaps.

- Record seven bounded W8 caller-image Cemu and native Dolphin baseline arms.
  Separate successful base EEPROM reads, Nunchuk extension calibration error 7,
  native discovery and the speaker-mute ACK boundary from unobserved decoded
  motion. Retain raw artifacts privately and preserve the physical evidence gap.

- Fix W7 Cemu test imports when corpus discovery runs from a parent or unrelated working directory. Load the original reducer by a path relative to the test file and add an external-directory regression. Evidence records and runtime helpers are unchanged.

- Correct the incomplete W7 Cemu availability lookup with an installed ARM64 AppImage native-Wiimote run: four holder/profile comparisons and byte-capture repeats, native register attribution and calibration error 8 with the default empty caller EEPROM. Raw transport works; decoded gyro remains unobserved. Add reduced evidence, original trace reducer/guard and deterministic boundary tests; retain prior records unchanged.

- Record W7 independent Wii consumers: bounded libxwiimote gyro/normalization and evtest passes, RetroArch UHID/uinput generic controls with version-specific sensor limitations, ARM64 Cemu availability blocker and unresolved Dolphin direct-scanner checkpoint. Add original owned-device probes and reduced semantic evidence; preserve survey and physical claims.

- Research Wii Remote in-band speaker for post-alpha planning: pin Dolphin real-Wiimote forwarding/pacing, emulated speaker control/registers, signed PCM/Yamaha ADPCM decoder and rate, plus Linux hid-wiimote consumer exclusion. Cross-reference the three existing WiiBrew claims, record Dolphin/WiiBrew ADPCM volume-range discrepancy and maintain an explicitly not-run physical lab plan. No wii-* claims edited, no implementation, no physical promotion.

- Document source-scoped controller audio exclusions: xpad Xbox 360 no headset PCM path, Xbox Series xpad explicitly disabling GIP audio interface, Nintendo/SDL Switch Pro rumble distinct from audio, and Steam Controller 2026 audio endpoint unknown. No claims about physical absence and no existing SC2 gap record changes.

- Add pinned Sony audio consumer research: DualSense HID route/levels/mute/preamp fields and USB/BT framing, ALSA UCM routing, maintainer-documented physical UAC1 and headphone/grip observations, DS4 SDL/kernel distinctions, explicit unanswered Bluetooth/DS4 audio questions, and the kernel's USB jack-detect driven routing. No controller implementation or physical-status promotion.

- Add W5 unchanged-model MotionPlus gyro diagnosis: verified active packet decoding/pass-through and kernel ABS gyro delivery before fresh SDL holder/control comparisons. Retain zero SDL gyro and disconnects, actor/readback ambiguity and private-mode instrumentation limits. Add original probes, semantic evidence reducers and deterministic tests; no prior records or protocol model changes.

- Add pinned W4 SDL consumer-source no-reattach claims for3.2.10, latest3.4.18 and main; correct the MotionPlus-active downstream-change disconnect distinction. Record five60-second fixed-extension claim-held runs, selected controls/acceleration and LED intent; retain blocked zero gyro in both MotionPlus profiles. Add original probes and evidence-boundary tests without protocol or historical-record changes.

- Record W3 unchanged-model SDL extension reinitialization diagnosis with timestamped virtual reports and explicit blocked sustained HIDAPI acceptance; attribute the W2 N1 global count delta to unrelated USB input entries while preserving its historical blocked status. Add original reproducible tracing tools and deterministic evidence tests; no claim promotion.

- Record W2 authored interim Game Pad descriptor, default SDL enumeration and bounded initial Wii HIDAPI claim with later disconnect, plus clean-head UHID N1/N4 timing; preserve N1 global input-count discrepancy and all historical evidence.

- Add separate human-granted W1 LED, SDL and Dolphin virtual-host follow-ups: LED intent succeeds, hidraw access succeeds, Wii HIDAPI/backend acceptance remains unobserved. Historical blocked records and all wii-gap claims remain unchanged.

- Clear repository-local Git environment in both hook wrappers so nested cache/fixture commands cannot mutate the active worktree; cover inherited hook context deterministically.

- Record W1 bounded Wii numeric delivery on UHID/uinput, battery/rumble observations and explicit SDL HIDAPI/Dolphin/LED permission blocks, with original reproducible probes; no physical promotion or wii-gap claim changes.

- Add reproducible hash-checked Wii consumer-shape extraction and a six-node synthetic evdev golden; record source extension register tails and pass-through packing without promoting physical calibration.

- Add C5 source-only report layout/error/camera/extension locators and explicitly synthetic neutral packets and functional HID framing; preserve retail descriptor, calibration and physical-evidence limits.

- Migrate pinned Steam kernel/OpenPuck identity,interface,report and lizard findings; retain historical1142/current1304 distinction and unmeasured cadence.
- Add Wii L0 pinned consumer/emulator ledger, separate original/early-Plus/TR revision scopes, source-derived evdev shape and explicit memory/encryption gaps.
- Add Xbox Series L0 source-only xpad/SDL ledger and linked observed-evdev artifact, preserving USB-GIP/Bluetooth/device-evidence separation.
- Record500 measured DualSense/Xbox360 uinput lifecycle samples with virtual-host-only format/validation, sanitized paths/time and explicit missing consumer measurements; no physical promotion.

### Added

- Added a source-backed wired Steam Controller 2026 (C6) report field map, conditional feature/settings exchange claims, synthetic input/output/GET fixtures, source discrepancies and strict fixture regression checks; no physical acceptance claimed.


- Pinned Steam Controller 2026 P0 consumer evidence: kernel introduction and
  v7.3-rc1 selection, SDL Triton direct/receiver filters, and provisional UHID
  feasibility. Live P1 and all physical observations remain unmeasured.
- Source-reviewed Steam Controller 2026/Puck earlier-research gap audit, with revision-pinned independent Triton sources and unresolved gap claim records; no physical or live acceptance claimed.

- `records/controller/` registry (schema `controller.schema.json`). Every
  claim's `applicability.controller` must name a registered controller, and
  each record links its tracking issue.
- `tools/status.py`, which prints each controller's evidence category (no
  evidence, evidence in progress, source evidence, physical evidence) overall
  and per transport.

### Changed

- Claim `applicability.transport` is a fixed vocabulary: `usb`, `bluetooth`,
  `receiver`, `source_only`, `not_measured`. Existing free-text transports
  became `source_only` with the original detail moved into `scope`; existing
  controller names became registry IDs. Record shape is unchanged, so
  `schema_version` stays 1.

### Changed

- Visibility gates removed from CI now that the repository is public: the
  policy matrix, dependency review, CodeQL and Scorecard run on every change,
  and the history guard fails on any personal commit email.

- Published as `controller-protocol-research`, a fresh repository started
  from a flat copy of the private `controller-protocol-corpus` `main` as a
  single first commit, with no earlier history; the private repository keeps
  its name.

### Added

- `tools/history_guard.py` and a `Disclosure checks` CI job: publication
  checks over every reachable file version and commit identity, including
  pull-request refs.

- Public-release hardening from the reference blueprint: committed git hooks,
  pre-commit policy (gitleaks, file hygiene, local-path/IP/credential
  blockers, ruff), CodeQL for Python and Actions workflows, OpenSSF Scorecard,
  dependency review, harden-runner egress allowlists, hash-locked pip installs,
  `scripts/deep-scan.sh`, and issue and PR templates.
- Publication guard, split licensing (CC-BY-4.0 data, AGPL-3.0-only tooling),
  SECURITY.md and CONTRIBUTING.md.

- C5: source-only native evdev conversion/no-clamp evidence; bounded virtual-host binding/swap/rumble/battery-presence and four timing runs. LED permission failures and missing consumer/physical cells remain explicit.
