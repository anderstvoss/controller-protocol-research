# Going public checklist

Do these steps in order. Everything before step 6 happens while the repository
is still private. Once it's public, every reachable commit on every branch and
tag is public.

## 1. Land the hardening

- [x] Merge the publication-hardening PR and the blueprint layer on top of it
      in the private repository first, so they're part of the copy.
- [ ] Decide what happens to the other open PRs and branches. Any branch that
      still exists at the flip becomes public along with its history. Merge,
      close or delete each one.

## 2. History and data hygiene (hard gate)

- [ ] `scripts/deep-scan.sh` passes: gitleaks over every branch and tag.
- [ ] `python tools/publication_guard.py` passes on `main`.
- [ ] `python tools/history_guard.py` passes with no warnings after fetching
      every ref, including `refs/pull/*/head`. It scans every file version
      ever committed and every commit email.
- [ ] Review the full history, not just `main`, for raw captures, serials,
      Bluetooth or MAC addresses, host paths and private lab notes:
      `git log --all --stat` and `git log --all -p -- fixtures evidence`.
- [ ] If anything sensitive turns up, remove it, start again from a new flat
      copy before the flip, and rotate or retire whatever it identifies.
- [ ] Confirm that no upstream source code or vendor documents are committed
      beyond the excerpt listed in NOTICE.

## 3. Metadata and licensing

- [ ] Set the repo description and topics (for example: game-controller, hid,
      evdev, protocol, dualsense).
- [ ] Confirm LICENSE (AGPL-3.0-only, tooling), LICENSE-DATA (CC-BY-4.0, data)
      and NOTICE, including the copyright holder and year.
- [ ] Make sure README, CONTRIBUTING, SECURITY and CHANGELOG are current.
- [ ] Turn off Wiki and Projects if you won't maintain them. Decide whether
      to keep Issues on (the templates assume they're on).

## 4. Start the fresh repository from a flat copy

GitHub keeps every pull request's original commits under `refs/pull/*`, and
only GitHub Support can purge them. So the public repository is a new one that
has never had pull requests, started from a flat copy of the private
repository's `main` rather than its history. This private repository keeps its
current name.

- [x] Create an empty private repository `anderstvoss/controller-protocol-research`
      (no README, license or .gitignore).
- [x] Copy the tracked files of the private `main` (`git archive main`) into it
      as a single first commit authored with your GitHub noreply address
      (Settings → Emails). No earlier commits, branches, tags or pull-request
      refs come across.
- [x] `python tools/history_guard.py --identities fail` passes on the new
      repository.
- [ ] Keep `controller-protocol-corpus` private under its current name; archive
      it once nothing is left to land there. Remove its deploy key
      once consumers have moved.
- [ ] Locally: `git remote set-url origin https://github.com/anderstvoss/controller-protocol-research.git`
      in a fresh clone; an old clone's history does not belong here.
- [ ] Commit SHAs do not carry over. Repin consumers to the new `main`
      (step 8).

## 5. Local hooks

- [ ] `git config core.hooksPath .githooks`
- [ ] `pre-commit run --all-files` and
      `pre-commit run --all-files --hook-stage pre-push` both pass.

## 6. The flip

- [ ] Settings → General → Danger Zone → Change repository visibility → Public.

## 7. Right after the flip

- [ ] Apply the server-side controls in `docs/REPO-SETUP.md` Step 2. Some
      settings reset when visibility changes.
- [ ] Run the checks in Step 3: open a draft PR, confirm all required contexts
      go green, and confirm Scorecard results appear in the Security tab.
- [ ] Tag a baseline (for example `corpus-2026.10.0`) on the commit that
      consumers will pin first.

## 8. Consumers

- [ ] virtualgamepad: point the `protocol-corpus` CI job's checkout at
      `anderstvoss/controller-protocol-research`, move `protocol-corpus.rev`
      to the new repository's commit and regenerate its fixture manifest; it can now
      check out anonymously. Drop the `PROTOCOL_CORPUS_SSH_KEY` requirement and its
      secret, update the "private corpus" wording (ci.yml, dependabot.yml,
      docs/CORE_ARCHITECTURE.md, docs/ALPHA_RELEASE_NOTES.md,
      scripts/check-protocol-corpus.py) and add CC-BY-4.0 attribution for the
      fixtures it copies into `tests/fixtures/protocol-corpus/`.
- [ ] Delete the read-only deploy key from this repository once
      virtualgamepad no longer uses it.
- [ ] gamepadcapture: add the same pin pattern (`protocol-corpus.rev`, a check
      script and a CI job) when it starts consuming corpus formats.

## 9. Afterwards

- [ ] Watch the Security tab for the first few days.
- [ ] Review dependencies, advisories and stale issues every quarter.
