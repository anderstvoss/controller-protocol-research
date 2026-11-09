# Evidence wiki

This is the human-readable **index** over the controller protocol corpus. It is
not a replacement for the original evidence, a new source of protocol truth, or
an implementation roadmap. All source, claim, experiment, fixture, controller
and report records remain in their existing directories, unchanged.

**Browse now:** [controller evidence navigator](INDEX.md).
**Authoritative evidence:** [records](../../records/) and [fixtures](../../fixtures/).
**Existing research narrative:** [docs](../).
**Generated controller and evidence indexes:** [open the complete generated wiki](generated/index.md)
after running the command below.

## Build the complete wiki

From the repository root, with the existing validation dependencies installed:

~~~sh
python tools/build_wiki.py
python tools/build_wiki.py --check
~~~

The generator reads the **entire validated corpus**, including every registered
controller, claim, pinned source, experiment, fixture, report shape and existing
research document. It writes Markdown under `docs/wiki/generated/` and does not
modify source material. Pass `--ref` with a full commit SHA to pin every GitHub
record link to a specific snapshot; otherwise it uses local Git HEAD.
`--check` detects missing, modified or unexpected generated pages.

The records are linked individually, and the generator retains the original
statement, status, role, revision, firmware, transport, scope, conflict and
supersession references. Source pages preserve the URL, pinned revision,
SHA-256, lineage and locator. Existing retained evidence artifacts are linked
without new interpretation. Experiment pages preserve the procedure, run
status, semantic outcome and fixture links. Fixture pages preserve their kind,
format, hash, ancestry and transformation descriptions. Existing narrative
documents are **linked, never consolidated by rewriting**.

## How to read an evidence entry

- **Device** and **consumer** roles are separate. A host driver recognizing
  a device is not proof the corresponding physical hardware behaves that way.
- **Transport** is explicit: USB, Bluetooth, receiver, source-only or
  not-measured. A source-only comparison cannot prove physical behavior.
- **Status** is retained verbatim. `source_supported`, `physically_observed`,
  `physically_validated`, `inferred`, `unknown`, `conflicted`, `rejected` and
  `independently_corroborated` are *not* interchangeable.
- **Lineage** is part of source provenance. Two records ultimately derived
  from the same implementation are not independent corroboration.
- **Conflicts** remain as separate referenced claims. The wiki does not
  silently vote them away or promote one source over another.
- **Experiments** reference separately documented procedures and fixtures.
  A passed virtual-host run is not a controlled test of physical equivalence.
- **Unknowns** remain unknown until added evidence passes the corpus rules.

For the canonical validation semantics see
[the repository README](../../README.md) and
[the validator](../../tools/validate.py).

## A worked example: Steam Controller 2026 Puck

The source-backed observations are distinct:

| Question | Existing claim record | What is established |
| --- | --- | --- |
| Official receiver identity and HID descriptor length in retained operator notes | [sc2-july-puck-identity-descriptor](../../records/claim/sc2-july-puck-identity-descriptor.json) | Notes record `28de:1304` and a 372-byte HID descriptor. No complete physical USB interface topology was verified. |
| Native receiver input `0x42` | [sc2-july-puck-input-42](../../records/claim/sc2-july-puck-input-42.json) | Retained operator notes record the report shape and sample counts, not physical byte-level semantics or timing. |
| Host interface expectations | [steam-puck-interface-selection](../../records/claim/steam-puck-interface-selection.json) | Pinned kernel and SDL sources describe interface selection; this is consumer/source evidence, not a physical descriptor capture. |
| Current OpenPuck identity | [puck-current](../../records/claim/puck-current.json) | Pinned compatibility implementation selects `28de:1304`; not proof of retail USB layout. |
| Historical contradictory Puck identity | [puck-historical-physical](../../records/claim/puck-historical-physical.json) | Historical source remains explicitly `conflicted`, with original capture unrecovered. |

The [pinned OpenPuck source record](../../records/source/openpuck.json),
[pinned kernel source record](../../records/source/steam-ibex-linux-driver.json)
and [Puck evidence gaps](../steam-controller-2026-research-gaps.md)
are linked separately. The example is a **navigation sample**; the generated
Puck page includes all applicable claims rather than selecting only these.

## Recommended presentation

1. **GitHub Markdown** — minimal maintenance, familiar diffs and direct
   record links. Good for reviewing the source-backed text inside a PR.
2. **MkDocs Material + GitHub Pages** — recommended reader experience:
   full-text search, collapsible navigation, mobile layout, permalinks and
   copyable links. The optional [MkDocs configuration](mkdocs.yml) uses
   only the generated Markdown. Pages publishing needs a separate owner-reviewed
   deployment workflow and GitHub Pages configuration.
3. **GitHub Wiki** — possible but not the preferred source of truth: it is a
   separate Git repository, making evidence/PR provenance and atomic changes
   harder to review and pin.
4. **Future faceted browser** — filters for controller, role, transport,
   status, source lineage and experiment kind; views should always link to the
   canonical JSON and never overwrite it.

See [publishing and maintenance](PUBLISHING.md) for the build and update policy.
