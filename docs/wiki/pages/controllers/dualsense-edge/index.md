# Sony DualSense Edge

> **Evidence snapshot:** corpus `ab74f662…` (2026-11-09); source-only versus physical and device versus consumer evidence are kept distinct.

**Registry:** [DualSense Edge](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/dualsense-edge.json), a separate member of the [DualSense family](../sony-dualsense-family/index.md). Read the [base DualSense chapter](../dualsense/index.md) for common input/feature concepts, but **do not automatically inherit** its USB ID, firmware profile or auxiliary-button semantics.

## What distinguishes this scope

Pinned Linux and SDL sources explicitly distinguish the Edge model (`054c:0df2`) from the standard `054c:0ce6`. Source-described additional control mappings and model-specific output behavior make **identity separation a consumer requirement**: [`dsedge-l0-consumer-identity-separation`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/dsedge-l0-consumer-identity-separation.json).

The cited source establishes what the inspected host understands; it does **not** settle the actual physical rear-button/macro assignment, whether all controls are exposed independently over every transport, or whether user profiles/mapping can suppress their visibility. No Edge physical fixture or controlled Edge session is established by this chapter.

## Research and implementation questions

- Which extra controls are present in native HID packets, and which are forwarded only after the controller's onboard mapping?
- How do firmware, profiles and SDL HIDAPI/evdev/Steam Input paths affect rear-button exposure?
- Are trigger-effect, lighting and sensor interfaces byte-compatible with a particular base DualSense firmware, or model-specific?
- What physical input and output tests can safely validate those fields?

Keep Edge source-specific claims under its own registry identity; record shared facts at the [family page](../sony-dualsense-family/index.md) only when genuinely applicable. Source narrative: [DualSense family/Edge comparison](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/ledgers/dualsense-l0.md), [consumer ownership](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/sony-consumer-contention.md).
