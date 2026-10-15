# Controller protocol research

Independent, versioned evidence corpus for reviewed controller implementations
(public successor of the private `controller-protocol-corpus`). JSON records use Draft 2020-12 schemas. Runtime libraries do not interpret these records.

Consumers such as virtualgamepad and gamepadcapture pin a corpus commit by its
full SHA (for example in a `protocol-corpus.rev` file), copy the fixtures they
need and check them against that revision in CI. The repository is public, so
the checkout needs no credentials.

```sh
python3 -m venv .venv
.venv/bin/pip install --require-hashes --no-deps -r requirements-dev.txt
.venv/bin/python tools/publication_guard.py
.venv/bin/python tools/validate.py
.venv/bin/python -m unittest discover -s tests
```

## Controllers and evidence categories

Every claim names a controller from `records/controller/` (for example
`dualsense`, `wii-remote`, `steam-controller-2026-puck`) and one transport:
`usb`, `bluetooth`, `receiver`, `source_only` (evidence read from source code or
documentation, not a connected device) or `not_measured`. Put finer transport
detail, such as an SDL backend, in the claim's `scope`. Add a controller record
before filing its first claim; each record links its tracking issue.

`tools/status.py` prints each controller's evidence category from its claims:

| Category | Strongest claim status |
| --- | --- |
| No evidence | no claims |
| Evidence in progress | `unknown`, `inferred`, `conflicted` or `rejected` only |
| Source evidence | `source_supported` or `independently_corroborated` |
| Physical evidence | `physically_observed` or `physically_validated` |

These are evidence levels only. Whether a controller is implemented or in
progress in a consuming project is tracked there, not here.

Sources are pinned and hashed, not redistributed. Source lineage is explicit. Synthetic fixtures are manually constructed host-structure examples, not captures and not proof of physical fidelity. Historical OpenPuck/physical identity claims remain conflicted and scoped to unrecovered evidence; current inspected OpenPuck code uses 28de:1304.

Claims may be promoted to physical validation only by a passed controlled physical experiment with a physical fixture and semantic outcome. Unknown firmware, coordinates, and report fields stay explicit. Contradictions are retained rather than resolved by source count.

Use `tools/sanitize.py` for an explicit byte-range replacement on a hex fixture. It records parent hashes and transformation lineage; redaction alone does not establish capture safety or protocol validity. Review output before committing. Raw private captures never belong here.

Corpus commits must be published to a retained branch before a consuming project pins them. Generation is limited to reviewed constants and fixtures; mutable protocol behavior remains handwritten and tested independently.

Fixture transformations accept existing fixture IDs as parents, reject path-like identifiers before reading them, and retain the original fixture unchanged. Invalid parents produce no derived output.

Pinned OpenPuck DS4 and HHD DualSense source inspections now supplement the seed.
Their synthetic active-contact fixtures describe selected field layouts, not
captured packets or claims that source-device mapping conventions are canonical.
OpenPuck feature sizes cite Linux host drivers; shared lineage is not independent
physical corroboration. Its zero-count no-contact packet and trigger thresholds
remain explicit comparison limits. HHD axis-map labels must be interpreted in its
mapping layer before adopting controller-native trigger semantics. No upstream
source code, device serials, calibration captures or private lab records are
redistributed. No DS4 physical reference was available for this inspection.

Post-106 exposure research pins SDL 3.2.0 PS5 decoding separately from a newer
Switch 2 decoder. Those source claims are not consumer observations or physical
validation. The Pro 2 FAQ is a research lead for macro functionality only; raw
visibility and exact Linux/firmware behavior remain unknown. One short vendor
excerpt is retained under `evidence/source-excerpts/`; its hash covers only that
excerpt, explicitly not the full HTML document. Tests preserve these distinctions.

Follow-up research pins SDL's generated Edge default mapping and Linux/HIDAPI
GUID construction. The backend interpretation is source-derived and limited to
reviewed builds and unambiguous identities. Default mapping is distinct from a
user override or observed mapping. The existing kernel parser source provides a
comparison of auxiliary-bit handling, without asserting an attached device's
binding or events. All physical/Linux observation unknowns remain in place.

## Fixture formats

Fixture records declare a `format`. `hid_report_hex` is a hex-encoded HID
report and is the only format `tools/sanitize.py` can transform.
`evdev_trace_json` is a gamepadcapture-style native evdev observation
(manifest, advertised controls, synchronized frames); its manifest's
`synthetic` flag must agree with the fixture kind.

## Publication safety and licensing

`tools/publication_guard.py` runs in CI before validation. It rejects host
paths, MAC/Bluetooth addresses, evdev `phys` strings, private IP and email
addresses, credentials, identifying JSON keys, binary or oversized files and
unexpected top-level entries. It is a backstop, not a substitute for review;
see CONTRIBUTING.md for the capture-safety steps. Repository hardening
(hooks, CI, server-side settings) is described in `docs/REPO-SETUP.md`.

Evidence data (`records/`, `fixtures/`, `schemas/`, `evidence/`) is CC-BY-4.0
(LICENSE-DATA). Tooling and tests are AGPL-3.0-only (LICENSE). NOTICE lists the
third-party excerpt and how upstream sources are cited.
