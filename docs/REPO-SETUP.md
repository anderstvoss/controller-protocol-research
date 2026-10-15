# Repository setup

How this repository's hardening is applied. It follows
`anderstvoss/baseline-hardened-repo`, adapted from that blueprint's Rust
library to a Python-tooled data corpus. Rust-only pieces (cargo gates, MSRV,
cargo-deny/audit, Cargo SBOM) are omitted; the validator's single runtime
dependency is hash-locked instead.

## Controls

| Control | Mechanism |
|---|---|
| Pre-commit gitleaks, file hygiene, ruff, publication guard, record validation; blockers for env files, keys, raw captures, local paths, private IPs, cloud URIs, binaries | `.pre-commit-config.yaml`, via committed `.githooks/pre-commit` |
| Pre-push gitleaks, tracked-file blocker, local-paths guard, history disclosure scan, corpus tests | `.githooks/pre-push` |
| Corpus validation (guard, schemas, integrity, tests) on every change | `ci.yml` `Validate corpus` |
| Disclosure scan of every file version and commit identity on every branch, tag and pull-request ref, plus the path/IP/key/capture blockers | `ci.yml` `Disclosure checks` via `tools/history_guard.py` (fails on any personal commit email) |
| Full pre-commit replay on Ubuntu, macOS and Windows | `ci.yml` `Policy checks (…)` |
| Dependency review on pull requests, `fail-on-severity: moderate` | `ci.yml` `Dependency review` |
| Full-history gitleaks across every branch, tag and pull-request ref, weekly and per change | `gitleaks.yml` `Gitleaks (full history)` |
| CodeQL `security-extended` for Python tooling and Actions workflows | `codeql.yml` |
| OpenSSF Scorecard with SARIF publish | `scorecard.yml` |
| SHA-pinned actions; `harden-runner` egress block on every Linux job | every workflow |
| Hash-locked pip installs | `requirements-dev.txt`, `.github/requirements/pre-commit.txt` |
| Ad hoc deep secret scan | `scripts/deep-scan.sh` |
| Secret scanning, push protection, private vulnerability reporting, Dependabot alerts, branch protection, read-only Actions token, tag ruleset | server-side, Step 2 below |


## Step 1: local clone

```bash
pipx install pre-commit          # or: pip install --user pre-commit
git config core.hooksPath .githooks
rm -f .git/hooks/pre-commit .git/hooks/pre-push   # stale wrappers, if any

pre-commit run --all-files
pre-commit run --all-files --hook-stage pre-push
scripts/deep-scan.sh             # needs gitleaks on PATH
```

## Step 2: server-side controls (applied 2026-10-15)

```bash
REPO=anderstvoss/controller-protocol-research

# Secret scanning + push protection
gh api --method PATCH /repos/$REPO --input - <<'EOF'
{"security_and_analysis":{"secret_scanning":{"status":"enabled"},"secret_scanning_push_protection":{"status":"enabled"}}}
EOF

# Private vulnerability reporting (SECURITY.md points here)
gh api -X PUT /repos/$REPO/private-vulnerability-reporting

# Dependabot alerts + automated security updates
gh api -X PUT /repos/$REPO/vulnerability-alerts
gh api -X PUT /repos/$REPO/automated-security-fixes

# Branch protection. Contexts must match job names exactly.
gh api -X PUT /repos/$REPO/branches/main/protection --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "Validate corpus",
      "Disclosure checks",
      "Policy checks (ubuntu-latest)",
      "Policy checks (macos-latest)",
      "Policy checks (windows-latest)",
      "CodeQL (python)",
      "CodeQL (actions)",
      "Gitleaks (full history)"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0,
    "require_code_owner_reviews": false,
    "dismiss_stale_reviews": false
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true
}
EOF

# Actions: read-only default token, workflows cannot approve PRs
gh api -X PUT /repos/$REPO/actions/permissions/workflow \
  -f default_workflow_permissions=read -F can_approve_pull_request_reviews=false

# First-time fork contributors need approval before workflows run
gh api -X PUT /repos/$REPO/actions/permissions/fork-pr-contributor-approval \
  -f approval_policy=first_time_contributors

# Protect release tags (corpus-* and v*) from update and deletion
gh api -X POST /repos/$REPO/rulesets --input - <<'JSON'
{"name":"release-tags","target":"tag","enforcement":"active",
 "conditions":{"ref_name":{"include":["refs/tags/v*","refs/tags/corpus-*"],"exclude":[]}},
 "rules":[{"type":"deletion"},{"type":"update"},{"type":"non_fast_forward"}]}
JSON
```

For community contributions, raise `required_approving_review_count` to 1 and
set `require_code_owner_reviews` to true.

## Step 3: verify

```bash
gh api /repos/$REPO | jq '.security_and_analysis'
gh api /repos/$REPO/branches/main/protection | jq '.required_status_checks.contexts'
gh workflow run scorecard.yml --repo $REPO
gh workflow run gitleaks.yml --repo $REPO
```

Then open a draft PR and confirm every required context goes green. As a
push-protection check, push a fake AWS key on a scratch branch: GitHub should
reject it.

## Maintenance

- If you add, rename or remove a CI job, update the branch-protection
  contexts at the same time.
- `required_linear_history` means PRs are squashed or rebased.
- If a job fails with a blocked egress, add the endpoint to that job's
  `harden-runner` allowlist.
- Regenerate hash locks after editing an `.in` file:
  `uv pip compile requirements-dev.in --generate-hashes --python-version 3.12 --output-file requirements-dev.txt`
  (and likewise for `.github/requirements/pre-commit.in`).
