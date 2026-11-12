# OpenPuck versus the genuine receiver

[← OpenPuck overview](index.md)

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

| Question | OpenPuck pinned source | Genuine Puck / consumer evidence |
| --- | --- | --- |
| Identity | External mode chooses `28de:1304`: [`puck-current`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/puck-current.json) | Retained operator note also records `1304`, but with limited source status: [`sc2-july-puck-identity-descriptor`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-july-puck-identity-descriptor.json) |
| Slots | Four HID interfaces/objects in this firmware: [`sc2-migration-openpuck-slots`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-migration-openpuck-slots.json) | Kernel/SDL expect receiver slot interfaces **2–5** inside a seven-interface source-described USB device: [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json) |
| USB total topology | Firmware's own descriptors and callbacks | Actual physical device/config/endpoint/pogo descriptions are not completely captured: [`sc2-gap-puck-usb-descriptors`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-puck-usb-descriptors.json) |
| Connection events | Firmware synthesizes per-slot state and input | Source parsing exists, but physical multi-controller packet ordering is unverified: [`sc2-gap-puck-slots`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-puck-slots.json) |
| Prior compatibility PID `1142` | Historic mention not supported by the current pinned mode | Preserve the unresolved historical provenance: [`puck-historical-compat`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/puck-historical-compat.json), [`puck-historical-physical`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/puck-historical-physical.json) |

## Porting principles

1. Use OpenPuck as a **known working design candidate** only for behavior actually supported by its pinned source; retain its revision and licensing.
2. Recreate the correct consumer-facing **USB interface ancestry** if receiver mode is the target. Do not conflate HID top-level collections, HID objects and USB interface numbers.
3. Introduce feature and state adapters with tests that compare against **both** a real Puck and fixed kernel/SDL consumers.
4. Preserve unknown slots, errors and timing as unknown; physical tests must control which claim gets promoted.

**Primary external implementation source, pinned by the corpus:** [`openpuck`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/source/openpuck.json). **Research context:** [migration analysis](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/steam-controller-migration.md).
