# 8BitDo Pro 2 — macro buttons and visibility

> **Reviewed corpus:** 2026-11-09. A source parser, compatibility shim or virtual-host acceptance does not establish native physical hardware fidelity.

**Registry:** [8BitDo Pro 2](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/8bitdo-pro-2.json). This chapter intentionally remains small because the corpus contains **limited direct protocol evidence**; adding invented USB packet tables would reduce its utility.

## What the source supports

A vendor FAQ describes **P1/P2** as programmable macro buttons managed through Ultimate Software. It does **not** establish that P1/P2 create independent raw HID button fields in every controller mode, nor that they are absent. The controller's current firmware, switch mode, transport and selected application mapping matter. [`pro2-physical-macro-controls`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/pro2-physical-macro-controls.json).

Corpus records explicitly preserve **unknown** independent P1/P2 raw-field behavior and exact Linux backend/evdev exposure: [`pro2-independent-raw-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/pro2-independent-raw-unknown.json), [`pro2-linux-exposure-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/pro2-linux-exposure-unknown.json), [`pro2-physical-corroboration-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/pro2-physical-corroboration-unknown.json).

## What would justify adding protocol pages

1. Pin model, firmware, hardware switch position and connection transport.
2. Read descriptor and report IDs independently for USB and Bluetooth/receiver modes.
3. In a neutral capture, press P1/P2 one at a time before and after changing onboard macro assignments.
4. Test whether the device emits independent flags, mapped ordinary button sequences, or no separate report at all.
5. Repeat under kernel evdev and SDL HIDAPI with active decoder and user profiles recorded.
6. Add new claim and controlled experiment records before updating this wiki.

Source record: [pinned FAQ](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/source/8bitdo-pro2-faq.json). This should not be interpreted as an endorsement of any particular button exposure strategy.
