# Security Policy

## Reporting a problem

Do not open public issues for suspected vulnerabilities or for data that
should not have been published (device serials, Bluetooth addresses, host
paths, personal information or raw captures).

Use this repository's **Private Vulnerability Reporting** form:
`https://github.com/anderstvoss/controller-protocol-research/security/advisories/new`.
Include the affected commit and file. The maintainer aims to acknowledge
reports within seven days. Published history is permanent once cloned, so
reports of exposed personal data are handled by removal from `main` and, where
needed, rotation of whatever the data identifies.

## Security controls

- GitHub Actions use commit-SHA-pinned third-party actions, read-only token
  permissions and `step-security/harden-runner` egress auditing against documented allowlists.
- CI runs `tools/publication_guard.py`, offline record validation and the test
  suite on every change, plus a gitleaks scan across every branch and tag on
  every pull request, every push to `main` and weekly.
- A disclosure job scans every file version and commit email reachable from
  any branch, tag or pull-request ref (`tools/history_guard.py`), and runs the
  local-path, private-IP, key and raw-capture blockers, on every change.
- The pre-commit policy replay on Ubuntu, macOS and Windows,
  dependency review on pull requests, CodeQL (Python and Actions workflows)
  and OpenSSF Scorecard.
- pip installs are hash-locked; Dependabot monitors pip and GitHub Actions
  dependencies weekly.
- Committed `.githooks` run gitleaks, credential/local-path/private-IP
  blockers and corpus validation before commits and pushes.
- Server-side controls (secret scanning with push protection, private
  vulnerability reporting, branch protection, tag ruleset) are documented in
  `docs/REPO-SETUP.md`.
