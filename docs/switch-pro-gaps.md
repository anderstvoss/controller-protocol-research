# Switch Pro realization accuracy gaps

**Evidence level:** Source-only Linux consumer inspection. No retail controller hardware test or virtual-host test was run for this contribution. No existing source, experiment or L0 claim record was modified.

## Ranked actionable gaps

| Rank | Gap and virtualgamepad impact | Playable versus faithful | Evidence ceiling | Existing records and issues |
| --- | --- | --- | --- | --- |
| **1** | **HOME-button illumination is not a distinct retained native output.** The Switch Pro implementation has four player indicators, but does not retain HOME brightness. It handles subcommand `0x38` with a generic `0x80` ACK instead of a HOME-light-specific state transition. | Ordinary buttons, axes and gamepad playability are unaffected. Native reverse-output fidelity is incomplete: a host's separately addressed HOME LED cannot be inspected or represented as its own function. Do **not** inflate the four player indicators to five. | **Consumer source-supported** for the Linux command, brightness domain and registration behavior; **no measured retail** brightness, fade, ACK, physical lighting, or firmware-dependent behavior. | New [`swpro-cgap-home-led-consumer`](../records/claim/swpro-cgap-home-led-consumer.json); reuse [`swpro-l0-linux-led-battery-consumer`](../records/claim/swpro-l0-linux-led-battery-consumer.json), [`swpro-l0-device-subcmd-ack-byte`](../records/claim/swpro-l0-device-subcmd-ack-byte.json). Implementation/acceptance [virtualgamepad #156](https://github.com/anderstvoss/virtualgamepad/issues/156); physical ACK and reply [#276](https://github.com/anderstvoss/virtualgamepad/issues/276). |

## Source-backed detail for rank 1

The existing, unchanged [`audio-linux-hid-nintendo`](../records/source/audio-linux-hid-nintendo.json) source pins Linux `hid-nintendo.c` at commit `4056b3c9d3c92ea45955641dbafeb9b960e146ef` with its reviewed SHA-256 digest. Its [command definitions](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-nintendo.c#L72-L75) assign subcommand `0x30` to player lights and `0x38` to HOME illumination. The Pro's right-capable classification is in lines 659–678. Lines 1030–1046 show a five-byte HOME-light payload with a brightness field; lines 2356–2385 show a separately registered HOME LED class with maximum brightness `0x0F`.

Of particular importance, [lines 2373–2380](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-nintendo.c#L2373-L2380) show that an unsuccessful initial HOME-light command results in a warning and no HOME LED registration, **not** a failed controller probe. Consequently, the current realization's generic ACK can permit host LED registration without having modeled HOME illumination. This is a statement about the inspected Linux consumer and current virtual implementation, **not** evidence of how retail hardware acknowledges subcommand `0x38`.

### Narrow remediation contract for virtualgamepad

Track independent HOME light *intent* and brightness in controller-owned retained output, separate from the existing four player lights. Decode subcommand `0x38` without silently changing its identity to a fifth player indicator. Keep original reply and ACK behavior bounded by the [`swpro-l0-device-subcmd-ack-byte`](../records/claim/swpro-l0-device-subcmd-ack-byte.json) source evidence and [#276](https://github.com/anderstvoss/virtualgamepad/issues/276); do not claim exact physical ACK bytes or animation semantics. Check the Linux LED class and retained state with a disposable virtual-host instance before promoting any acceptance cell. No implementation change is part of this PR.

## Existing gaps — cross-references only

The current L0 ledger, decision table, consumer survey and citation map remain authoritative; this document does not duplicate their claims:

- [#276](https://github.com/anderstvoss/virtualgamepad/issues/276): physical subcommand ACK, NACK and reply behavior, including HOME `0x38`; existing `swpro-l0-device-subcmd-ack-byte`.
- [#277](https://github.com/anderstvoss/virtualgamepad/issues/277): wired battery and power reporting; existing `swpro-l0-device-battery-connection-bits`.
- [#278](https://github.com/anderstvoss/virtualgamepad/issues/278): IMU gating and three-sample timing; existing `swpro-l0-device-report30-full` and `swpro-l0-consumer-imu-rumble-ack-gates`.
- [#279](https://github.com/anderstvoss/virtualgamepad/issues/279): factory/user SPI calibration and colors; existing `swpro-l0-device-factory-spi-map`.
- [#280](https://github.com/anderstvoss/virtualgamepad/issues/280): physical USB report cadence; existing `swpro-l0-device-usb-cadence-conflict`.

See [L0 ledger](ledgers/switch-pro-l0.md), [decision table](switch-pro-decision-table.md), [consumer survey](switch-pro-consumer-survey.md) and [citation map](switch-pro-citation-map.md) for technical background and existing source/consumer evidence.

## Proposed physical gate: not run

With prior owner approval and a real reference controller, test separately varied HOME brightness, off/reset, and player-indicator commands. Record sanitized host requests, exact reply success/failure and visible light behavior; distinguish Linux LED-class registration from actual hardware illumination. Include an initial HOME `0x38` failure case on an isolated disposable virtual-host reference where safe. **No hardware, host-side injection, or physical observation occurred in this research pass.**
