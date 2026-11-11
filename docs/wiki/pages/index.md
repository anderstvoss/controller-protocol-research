# Controller protocol knowledge base

**Latest reviewed corpus revision:** [`ce6b8d3b70fd0957135eb921ef6098988f355cb1`](https://github.com/anderstvoss/controller-protocol-research/commit/ce6b8d3b70fd0957135eb921ef6098988f355cb1) (2026-11-10, local). The initial chapters were reviewed at [`ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12); their original claim citations remain pinned to that immutable revision unless a newer claim is explicitly cited. The eight subsequent main-branch commits are interpreted in the added/updated chapters.

This is a **curated engineering interpretation**, not a live rendering of every JSON record. The [evidence corpus](https://github.com/anderstvoss/controller-protocol-research/tree/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/controller) remains authoritative; this wiki explains the protocols, host behavior, implementation constraints and unresolved questions. Pages are updated **on request**, after reviewing additions and changes in the corpus.

## Start here

- [Controller library](controllers.md) — all 19 registered controller/family/interface entries.
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

> Editorial coverage: the original November 9 baseline plus eight follow-up commits through `ce6b8d3b70`. The additions are Steam Controller BLE, Xbox Series xpad/xone/xpadneo/Bluetooth, Switch Pro HOME/NFC, and audio association. This is not a new physical-device validation.
