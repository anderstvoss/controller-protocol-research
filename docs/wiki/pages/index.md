# Controller protocol knowledge base

**Latest reviewed corpus revision:** [`eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e`](https://github.com/anderstvoss/controller-protocol-research/commit/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e) (2026-11-25 review). The Alpha 2 preparation refresh incorporates registry/hygiene, receiver, Sony, Nintendo, Wii, Xbox, Steam, USB audio and virtual-host polish evidence. Earlier sections retain their historical pinned citations.

This is a **curated engineering interpretation**, not a live rendering of every JSON record. The [evidence corpus](https://github.com/anderstvoss/controller-protocol-research/tree/eb7887bf1aacc1b0baf6f5e973cac2ee41090c4e/records/controller) remains authoritative; this wiki explains the protocols, host behavior, implementation constraints and unresolved questions. Pages are updated **on request**, after reviewing additions and changes in the corpus.

## Start here

- [Controller library](controllers.md) — registered controller/family/interface entries.
- [Latest research additions](changelog.md) — chapter updates, evidence scope and snapshot history.
- [How to interpret evidence](methodology.md) — evidence roles, standards of proof, provenance and conflicts.
- [Controller/audio association](audio-association.md) — separate HID and sound-card discovery, USB ancestry, unknown Steam/Proton association.
- [Host exposure and transport layers](transports-and-consumers.md) — USB, Bluetooth, HID, evdev, SDL, kernel, Steam and virtual realizations.
- [Protocol lifecycle](report-lifecycle.md) — discovery, feature negotiation, state, output, teardown.
- [Outstanding research priorities](gaps.md) — distinguish physical research, source interpretation and consumer acceptance.
- [Original research documents](research-notes.md) — the existing detailed ledgers and experiments, preserved without replacement.
- [External reference shelf](external-references.md) — supplementary material not yet incorporated into corpus claims.
- [Editorial update procedure](updating.md) — deliberate snapshot refreshes and checks.

## Reading a controller chapter

Each primary controller has a landing page. Subpages describe **protocol/wire structure**, **host consumer behavior**, and where appropriate **attachments, outputs and verification**. A precise statement is followed by a link to the specific claim ID. Claim JSON names its pinned sources, experiments, scope and status. The text can summarize evidence, but **never changes its status**.

For example, source code expecting a packet is not proof a retail unit emits it. A successful virtual-host run is not a controlled physical comparison. A hardware observation may be constrained to one firmware, transport and test.

> **Editorial coverage:** See the [editorial changelog](changelog.md) for the PR groups reviewed. Source-only, virtual-host and physical-device findings remain separately scoped.
