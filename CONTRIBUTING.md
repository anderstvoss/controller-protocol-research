# Contributing to controller protocol research

The corpus records evidence about controller protocols. Every record must say
where its claim comes from and how strong that evidence is; see README.md for
the evidence rules.

## Setup

```sh
pipx install pre-commit          # or: pip install --user pre-commit
git config core.hooksPath .githooks
```

The committed hooks run gitleaks, file hygiene, ruff, credential and
local-path blockers, the publication guard and record validation on commit,
and the test suite on push. See `docs/REPO-SETUP.md` for the full posture.

## Checks

```sh
python3 -m venv .venv
.venv/bin/pip install --require-hashes --no-deps -r requirements-dev.txt
.venv/bin/python tools/publication_guard.py
.venv/bin/python tools/validate.py
.venv/bin/python -m unittest discover -s tests
```

Record notable changes in `CHANGELOG.md` under `Unreleased`. To change the
validator's dependencies, edit `requirements-dev.in` and regenerate the hash
lock with `uv pip compile requirements-dev.in --generate-hashes --python-version 3.12 --output-file requirements-dev.txt`.

## Capture safety

This repository is intended to be public. Before adding a physical or
sanitized fixture:

1. Capture privately (for example with gamepadcapture's `capture-lab`) and
   keep the raw bundle outside this repository.
2. Remove or replace serial numbers, Bluetooth and MAC addresses, host paths,
   evdev `phys`/`uniq` strings, usernames, hostnames and wall-clock timestamps.
   Record the transformation with `tools/sanitize.py` so lineage is explicit.
3. Run `tools/publication_guard.py`. It is a backstop for structural leaks, not
   proof that a fixture is safe; review the bytes yourself.
4. Do not commit upstream source code, vendor documents or firmware. Cite them
   in `records/source/` by URL, revision and hash instead.

## Licensing

By contributing, you agree that data you add under `records/`, `fixtures/`,
`schemas/` and `evidence/` is licensed under CC-BY-4.0 (LICENSE-DATA) and that
code under `tools/` and `tests/` is licensed under AGPL-3.0-only (LICENSE).
Third-party excerpts keep their own terms and must be listed in NOTICE.
