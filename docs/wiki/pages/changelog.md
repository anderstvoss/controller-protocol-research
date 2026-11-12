# Wiki editorial changelog

## 2026-11-11 — four merged research PRs incorporated

**Latest reviewed corpus:** [`e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7`](https://github.com/anderstvoss/controller-protocol-research/commit/e8cca52c51f76c95b72c3bf6d27a9c04d854e9e7); previous snapshot `ce6b8d3b70`.

- Added [scoped Xbox Series physical and virtual observations](controllers/xbox-series/physical-observations.md) from #125: one physical wired xpad input/reconnect reference, bounded main rumble and xone headset audio, a physical 283-byte Bluetooth HID descriptor, and separate scratch-UHID and xpadneo consumer tests. The device-descriptor and post-driver input claims are `physically_validated` in their stated scopes; raw GIP framing and isolated trigger motors are not.
- Added [Puck receiver lifecycle](controllers/steam-controller-2026-puck/receiver-lifecycle.md) from #127: per-interface Linux/SDL presence, `0x46`/`0x79` status decoding, native node teardown and output routing. **Source-only**; slot epochs are inferred.
- Added [Steam virtual kernel-evdev](controllers/steam-controller-2026/virtual-kernel-evdev.md) from #122: mode-gated evdev/sensor events and UHID/uinput differences. A virtual host test, **not a retail device capture**.
- Added [Joy-Con Left protocol and consumer interpretation](controllers/switch-joycon-left/source-and-consumers.md) from #126: native left-half button/stick fields, Linux transforms and SDL sideways versus vertical mappings. **Source-only**, no physical test.
- Integrated original PR records, fixtures and ledgers unchanged; updated manual prose, chapter navigation, research notes, gaps, and host/audio cross-references.

**Scope limit:** no retail Puck or Joy-Con tests; no Steam BLE pairing; the Xbox physical reference does not qualify every firmware, raw USB/BT report or independent motor.

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
