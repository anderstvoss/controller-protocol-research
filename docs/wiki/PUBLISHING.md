# Wiki maintenance, review and publishing

The wiki lives in **docs/wiki/pages/** and is manually authored. It is
deliberately a **reviewed snapshot** of the evidence corpus rather than a
continuously synchronized database.

## Authority and update steps

1. Record the target corpus **full Git commit SHA** and the last reviewed
   snapshot (wiki home and editorial changelog).
2. Read added/changed claim JSON, source records, experiments, fixtures and
   original research notes. Group by controller, transport and behavior.
3. Write or revise the technical explanation; include raw report tables,
   consumer/driver distinctions, open questions and implementation constraints
   only where they are actually supported.
4. Directly cite the **individual corpus claim records** with full-SHA
   permalinks. Cite source records for provenance when useful; do not copy
   upstream code, private captures, serials or identifiers.
5. Preserve conflict, supersession, uncertainty and device/consumer evidence
   roles. A source-only parser cannot be promoted to physically verified.
6. Run read-only wiki link checking, publication guard, normal corpus
   validation and tests. Review every rendered page for accuracy, privacy
   and meaningful interpretation.
7. Update the reviewed SHA and document chapter-level changes in the wiki
   changelog only **after** the editorial review. Open a documentation PR.

Do not run an automatic page generator. No wiki update is implied merely by
merging a new corpus claim. Historical docs and source records remain intact.

## Reading and preview

On GitHub, start at [wiki home](pages/index.md).

To preview a searchable site with the optional MkDocs Material package:

~~~sh
python -m mkdocs serve -f docs/wiki/mkdocs.yml
python -m mkdocs build -f docs/wiki/mkdocs.yml --strict
~~~

No dependency or publishing workflow is introduced for MkDocs by this PR.
The static website, if eventually enabled, must be built from an explicitly
reviewed commit and should display that commit's reviewed **corpus revision**
prominently. GitHub Pages is appropriate; a separate GitHub Wiki repository
is not, since it would weaken atomic PR review and provenance.

## What can be validated automatically

A link checker can establish that local pages exist and citations point to
existing corpus records. It cannot decide whether prose correctly interprets
raw reports, whether a source lineage is independent, or whether a physical
experiment genuinely establishes hardware behavior. Those remain **manual
review responsibilities**.

## Privacy and licensing

The existing publication and history guards remain mandatory. This wiki
only cites the corpus's reviewed materials and outside public documentation.
Never introduce raw private captures, device-specific MAC addresses,
serials, calibration images, account metadata or firmware contents here.
