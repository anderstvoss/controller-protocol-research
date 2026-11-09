# Puck — physical validation and laboratory plan

[← Puck overview](index.md)

> **Evidence snapshot:** [corpus `ab74f662…`](https://github.com/anderstvoss/controller-protocol-research/commit/ab74f66274589a7229633f0fe8654490c3d19a12), 2026-11-09. This is an editorial account; the linked records control confidence and applicability.

## Distinct evidence gates

| Gate | Task | Required output |
| --- | --- | --- |
| P1 | Record authentic Puck `28de:1304` device, configuration, interface, endpoint and HID descriptors | Full topology by firmware, safely sanitized/hashed; compare seven-interface source model |
| P2 | Observe one controlled controller slot attach, steady native input, loss, reconnect and unplug | Timestamped report histogram, slot identity, connection ordering; avoid unsupported cadence claims |
| P3 | Probe host feature and output paths on that slot | Source-backed commands, GET/SET lengths, successful/failed return semantics; exclude identifiers |
| P4 | Compare real Puck with OpenPuck mode | Enumerated interfaces, report content, lifecycle; treat differences as source-vs-device findings |
| P5 | Compare simulated USB composite with physical Puck | Fixed Linux/SDL/Steam builds, selected consumer backend, all slot/open/close transitions |
| P6 | Deliberate teardown | Neutral each slot, cancel pending effects, remove all interfaces, verify no orphan evdev/hidraw nodes |

The current physical provenance is **retained operator notes** rather than a complete raw configuration capture: [`sc2-july-puck-identity-descriptor`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-july-puck-identity-descriptor.json). The source model for slots is [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json); unresolved report cadence and non-HID/pogo semantics are [`sc2-cadence`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-cadence.json) and [`sc2-gap-puck-usb-descriptors`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/sc2-gap-puck-usb-descriptors.json).

## Practical scope

Only one Puck and one controller are currently available. **Do not** claim four simultaneous physical slots have been validated from one-device connect/disconnect tests. Internal Steam Machine `1305` is excluded, notwithstanding source comparisons of its identity. Preserve original captures privately and publish only reviewed non-identifying evidence.

See [original lab plan](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-physical-capture-plan.md) and [evidence gaps](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/steam-controller-2026-research-gaps.md).
