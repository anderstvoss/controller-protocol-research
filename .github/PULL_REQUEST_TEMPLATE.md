## Summary

<!-- What evidence or tooling changed and why. -->

## Checklist

- [ ] No secrets, credentials, tokens, private IPs, or local paths in the diff
- [ ] No device serials, Bluetooth/MAC addresses, evdev `phys`/`uniq` strings, or raw captures
- [ ] New sources are cited by URL, revision and hash; no upstream code or vendor documents copied
- [ ] Claim status matches its evidence (no promotion without the required experiment and fixture)
- [ ] `tools/publication_guard.py`, `tools/validate.py` and `python -m unittest discover -s tests` pass locally
- [ ] If touching `.github/`, `.pre-commit-config.yaml`, `schemas/` or `tools/`, intent documented above
