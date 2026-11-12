# Nintendo Switch 2 GameCube USB Controller

> Reviewed corpus: 2026-11-09. Unless stated otherwise this chapter describes inspected *consumer source code*, not a physical retail capture.

**Registry:** [Switch 2 GameCube](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/controller/switch2-gamecube.json), a distinct device from both [Switch 2 Pro](../switch2-pro/index.md) and the [four-port WUP-028 adapter](../gamecube-usb-adapter/index.md).

## Core distinction

Although the Switch 2 GameCube shares a Nintendo Switch 2 host-command **family**, its USB controller is a single native device with **GameCube-specific C, analog trigger travel and separate full-travel/click controls**. It has its own `0x0a` input report parser and **binary/simple rather than HD rumble** in inspected Linux/SDL sources: [`switch2-gc-distinct-controls`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-distinct-controls.json), [`switch2-gc-report0a-linux`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-report0a-linux.json), [`switch2-gc-rumble-binary`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-rumble-binary.json).

Source code qualifies these **consumer interpretations**; a bounded physical capture plan exists, but has **not run** ([`switch2-gc-retail-physical-unknown`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/switch2-gc-retail-physical-unknown.json)).

## Read next

- [USB topology, reports, analog controls and consumer integration](usb-and-controls.md).
- [Owner-run physical capture plan](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/switch2-gamecube-physical-capture-plan.md).
- [Source-only consumer survey](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/switch2-gamecube-consumer-survey.md).

A previous Switch 1 GameCube controller with a WUP-028 four-port adapter **cannot** be used as a report-shape reference for this product.
