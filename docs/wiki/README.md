# Controller protocol research wiki

**[Read the technical wiki](pages/index.md)** · **[Browse controllers](pages/controllers.md)**

This is an **authored technical reference**, not a generated claim dump. It
integrates the research corpus into readable explanations of controller
interfaces, report formats, state machines, consumer behavior and implementation
tests. Source-supported facts, physical observations, hypotheses and unresolved
conflicts remain distinguished.

## Authority

- [Evidence records](../../records/) and [fixture records](../../fixtures/)
  are the **canonical** source of claims, source pins and experiments.
- [Prior research documents](../) remain intact, available and cited.
- Wiki articles link to **specific claim records at the reviewed corpus SHA**.
- The [wiki home](pages/index.md) states the current manually reviewed corpus
  revision. A later corpus commit does **not** automatically update the wiki.
- External references not yet pinned in the corpus are labeled as supplemental.

## How updates happen

The wiki is updated **only on request**. A reviewer compares the target corpus
revision with the last reviewed revision; reads new and changed claims,
experiments, fixtures and disagreements; edits the affected pages as a technical
narrative; then records the new reviewed SHA in a PR. Nothing overwrites source
evidence or generates prose from JSON.

See [update procedure](pages/updating.md) and
[evidence interpretation](pages/methodology.md).

## Validation (not generation)

~~~sh
python tools/check_wiki_links.py
python tools/publication_guard.py
python tools/validate.py
python -m unittest discover -s tests
~~~

The optional link checker is **read-only**. It checks local Markdown links and
repository-file citations. It does not update the wiki, fetch external websites
or change any evidence status.

## Presentation

- **GitHub Markdown:** direct reading and versioned PR diffs, no build needed.
- **MkDocs Material:** optional full-text-search static website using the same
  hand-written Markdown. The configuration is
  [mkdocs.yml](mkdocs.yml); run from repository root:

~~~sh
python -m mkdocs serve -f docs/wiki/mkdocs.yml
python -m mkdocs build -f docs/wiki/mkdocs.yml --strict
~~~

MkDocs is an optional local documentation dependency, **not** part of the
corpus validator's pinned runtime dependency set. GitHub Pages deployment is
not enabled by this PR. See [publishing](PUBLISHING.md).
