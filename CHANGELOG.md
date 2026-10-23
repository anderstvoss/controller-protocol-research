# Changelog

All notable changes to the corpus are recorded here. The format follows
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Consumers pin
corpus commits by full SHA; schema changes that alter record shape bump the
affected schema's `schema_version`.

## Unreleased

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
