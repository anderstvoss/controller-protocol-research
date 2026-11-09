# Wiki publishing and maintenance

## Policy

- **One authoritative corpus.** Do not move, delete, rewrite or merge source,
  claim, experiment, fixture or report records to make documentation tidier.
  Existing research documents remain intact.
- **Additive documentation.** The generator produces only an auxiliary
  `docs/wiki/generated/` tree; the existing corpus is read-only.
- **Status is evidence-specific.** Never infer physical device support from
  a host-driver code path, a virtual-host fixture, a synthetic trace, or a
  source-only comparison.
- **Pinned citations.** Every individual claim links to its original JSON;
  source entries link to their pinned URL, revision, digest and lineage.
  Generated links use a Git commit SHA when available.
- **Contradictions are first-class.** Preserve `conflicts_with`, `supersedes`
  and `rejection_scope`; do not resolve by claim count or recency alone.
- **No confidential material.** Publishing a generated page is subject to
  the same privacy and publication guard as the corpus itself.

## Local regeneration and review

Run from the repository root:

~~~sh
python tools/publication_guard.py
python tools/validate.py
python -m unittest discover -s tests
python tools/build_wiki.py
python tools/build_wiki.py --check
~~~

Review the diff in `docs/wiki/generated/` before publishing. The content is
generated solely from existing reviewed JSON and the research-document file
listing. It does **not** fetch upstream code, access physical controllers or
interpret fixture packet bytes. Re-run the publication guard after generation.

For an immutable published snapshot, check out the intended corpus commit and
run the generator with `--ref` set to that full SHA. Record that SHA in release
notes; do not link source claims to a moving branch for a published version.

## Local website preview (optional dependency)

MkDocs Material is **not** required for the corpus validator or Markdown
generation. Install it in an isolated documentation environment and run:

~~~sh
python -m mkdocs serve -f docs/wiki/mkdocs.yml
python -m mkdocs build -f docs/wiki/mkdocs.yml --strict
~~~

The `docs/wiki/mkdocs.yml` file points at the generated Markdown. The site is a
searchable representation of existing records; it does not host external
source blobs, firmware or private captures.

## Deployment choices

**Recommended:** use GitHub Pages from an owner-reviewed, SHA-pinned GitHub
Actions workflow. On every approved `main` change, validate the corpus, run the
publication guard, regenerate the wiki from that same commit, build MkDocs and
publish the static output. Keep Actions read-only by default and give only the
specific Pages job the minimum permissions required.

**Simplest:** commit the generated Markdown to the research repository, link to
its `generated/index.md`, and review these files in the same PR as the evidence
that changes them. No separate wiki repository or deployment is required.

**Do not** enable a new public publishing pipeline without reviewing the repo's
existing branch, disclosure, dependency and GitHub Pages protections.

## Suggested future information architecture

- Controller page: family/parent, identity, evidence categories by transport,
  claims grouped by role and transport, gaps and contradictions.
- Claim drill-down: exact statement and scope, status, source pins, experiments,
  opposing claims and source-document pointers.
- Source lineage: code/document revision, hash and locator, shared ancestry.
- Experiment drill-down: protocol, physical/synthetic/virtual-host distinction,
  status, semantic outcome and fixture hashes.
- Research narrative: existing corpus-backed guides and decision tables,
  linked rather than duplicated.

A generated wiki should never become an alternate evidence ingestion interface.
New findings must first be added to validated corpus records.
