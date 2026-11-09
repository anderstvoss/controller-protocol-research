# Controller protocol knowledge base

**Reviewed corpus revision:** [`ab74f66274589a7229633f0fe8654490c3d19a12`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12) (2026-11-09).

This is a **curated engineering interpretation**, not a live rendering of every JSON record. The [evidence corpus](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller) remains authoritative; this wiki explains the protocols, host behavior, implementation constraints and unresolved questions. Pages are updated **on request**, after reviewing additions and changes in the corpus.

## Start here

- [Controller library](controllers.md) — all 19 registered controller/family/interface entries.
- [How to interpret evidence](methodology.md) — evidence roles, standards of proof, provenance and conflicts.
- [Host exposure and transport layers](transports-and-consumers.md) — USB, Bluetooth, HID, evdev, SDL, kernel, Steam and virtual realizations.
- [Protocol lifecycle](report-lifecycle.md) — discovery, feature negotiation, state, output, teardown.
- [Outstanding research priorities](gaps.md) — distinguish physical research, source interpretation and consumer acceptance.
- [Original research documents](research-notes.md) — the existing detailed ledgers and experiments, preserved without replacement.
- [External reference shelf](external-references.md) — supplementary material not yet incorporated into corpus claims.
- [Editorial update procedure](updating.md) — deliberate snapshot refreshes and checks.

## Reading a controller chapter

Each primary controller has a landing page. Subpages describe **protocol/wire structure**, **host consumer behavior**, and where appropriate **attachments, outputs and verification**. A precise statement is followed by a link to the specific claim ID. Claim JSON names its pinned sources, experiments, scope and status. The text can summarize evidence, but **never changes its status**.

For example, source code expecting a packet is not proof a retail unit emits it. A successful virtual-host run is not a controlled physical comparison. A hardware observation may be constrained to one firmware, transport and test.

> Scope: this is the November 9, 2026 research snapshot. Newly merged evidence is not automatically reflected here.
