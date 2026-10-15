# Changelog

All notable changes to the corpus are recorded here. The format follows
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Consumers pin
corpus commits by full SHA; schema changes that alter record shape bump the
affected schema's `schema_version`.

## Unreleased

- Add Wii L0 pinned consumer/emulator ledger, separate original/early-Plus/TR revision scopes, source-derived evdev shape and explicit memory/encryption gaps.

### Added

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
