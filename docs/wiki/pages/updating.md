# Manual wiki refresh workflow

The wiki is **not generated** from the corpus. It is maintained editorially, and only updated when requested.

1. Identify the wiki's current **reviewed corpus SHA** on [home](index.md); compare with target corpus SHA. Review new and changed records, experiments, fixtures, conflicts and supersessions. Never delete historical evidence.
2. Read relevant source and experiment records, original research ledgers and any external sources actually needed. Keep source-supported interpretations distinct from observations and editor inference.
3. Update each affected **controller chapter**, associated protocol/consumer subpages, comparison notes and [research gaps](gaps.md). Do not paste a wall of claim JSON into the wiki.
4. Link each substantive technical claim directly to existing record(s) in the reviewed corpus; preserve firmware, transport, status, counterexamples and source lineage.
5. Run [link checks](../README.md) and the repository's original `tools/publication_guard.py`, `tools/validate.py` and tests. A passed guard is only a backstop; manually inspect privacy-sensitive prose.
6. Update the reviewed SHA **after** the editorial changes have been evaluated; include a brief changelog and scope in the wiki PR. Readers must be able to tell that later corpus changes have not yet been incorporated.

## What not to do

- No wiki text generator, automated replacement of human summaries or silent continuous synchronization.
- No changes to `records/`, `fixtures/` or existing research documents merely to make wiki prose cleaner.
- No automatic evidence promotion based on driver version, external blog, synthetic fixture or source count.
- Do not treat metadata for Bluetooth bus/UHID as an actual radio discoverability test.

## Presentation

These Markdown pages are reviewable directly on GitHub. An **optional** MkDocs Material build can publish exactly the same authored pages, without rewriting any text or requiring a new evidence database.
