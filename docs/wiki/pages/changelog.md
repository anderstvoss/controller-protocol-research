# Wiki editorial changelog

## 2026-11-10 — corpus catch-up and editorial review

**Latest reviewed corpus:** [`ce6b8d3b70fd0957135eb921ef6098988f355cb1`](https://github.com/anderstvoss/controller-protocol-research/commit/ce6b8d3b70fd0957135eb921ef6098988f355cb1) (8 commits after the initial November 9 baseline).

- Merged the eight follow-up corpus commits into the wiki review branch without changing evidence records.
- Added authored chapters for direct Steam Controller BLE/HOGP and conditional ATT MTU; Xbox Series xone wired/receiver and Bluetooth/xpadneo; Switch Pro independent HOME LED and NFC applicability; and HID-to-ALSA/PipeWire audio association.
- Updated chapter indices, protocol cautions, consumer comparisons, research priorities, original-ledger links and MkDocs navigation.
- Retained immutable November 9 claim citations for older paragraphs whose source claims did not change; newer research cites the later full-SHA corpus tree.
- Correctly distinguished xpadneo keyboard F12 Share from stock xpad Record; preserved four Switch Pro player indicators with a separate HOME LED.
- No external radio, Steam UI, hardware-output or synthesized UHID acceptance was performed.

**Editorial limit:** the wiki summarizes reviewed corpus evidence, rather than replacing its records or attesting implementation/hardware fidelity. Some chapters explicitly retain their older individual evidence-snapshot labels because those sections did not acquire new research.

## 2026-11-09 — initial manual consolidation

**Reviewed corpus:** ab74f66274589a7229633f0fe8654490c3d19a12.

- Authored chapters for every controller, family, emulator and host-interface
  registry entry (19 total).
- Added detailed report, feature, input, output, memory, accessory, consumer,
  ownership, virtualization and lab pages where backed by the corpus.
- Distinguished physical D9 wired Steam Controller 2026 results from retained
  Puck source notes, kernel/SDL source descriptions and OpenPuck emulation.
- Retained the existing Sony, Wii, Nintendo, Xbox and GameCube research
  narratives as linked historical documents; no existing records altered.
- Added methodology, an explicit manual-refresh workflow, research priorities
  and separately labeled supplemental external references.
- Chose Markdown-first with optional MkDocs; no scheduled generation or Pages
  publishing was enabled.

**Limitations:** This snapshot is a curated technical narrative, not an
exhaustive row-for-row recitation of all corpus claims. Newer evidence requires
an explicit reviewed update; unverified physical behavior remains unverified.
