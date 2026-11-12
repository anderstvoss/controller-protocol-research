# Switch Pro cadence conflict and colour SPI — gap pass 2

Source-only findings for [virtualgamepad #156](https://github.com/anderstvoss/virtualgamepad/issues/156), limited to USB cadence and colour SPI. New evidence narrows the implementation decision **without** validating retail hardware. No host or controller test was performed in this research session.

## Ranked gaps

| Rank | Gap | Playable or faithful | Evidence ceiling | Related record or issue |
| --- | --- | --- | --- | --- |
| 1 | Colour SPI requested by a Switch 2 console against a Pro-compatible emulator, despite absence of colour reads in the reviewed Linux/SDL open paths | Faithful presentation and identity; not required for basic controls | Source-supported **Switch 2 consumer report** and compatibility implementation; retail Pro/all-0xFF behavior unknown | `swpro-cgap-switch2-colour-spi-requests`, `swpro-cgap-pro-colour-spi-boundary`; `swpro-l0-consumer-colour-spi-no-evidence`; [#156](https://github.com/anderstvoss/virtualgamepad/issues/156), [#279](https://github.com/anderstvoss/virtualgamepad/issues/279), [#161](https://github.com/anderstvoss/virtualgamepad/issues/161) |
| 2 | USB input cadence conflated with Bluetooth timing and a compatible emulator schedule | Faithful timing; basic gamepad playability does not require asserting a retail period | Source-supported **Linux driver expectation** of approximately 15 ms on USB, not an independently measured retail USB distribution | `swpro-cgap-linux-usb-report-period-source`; `swpro-l0-device-usb-cadence-conflict`, `swpro-l0-device-physical-usb-period-unknown`; [#280](https://github.com/anderstvoss/virtualgamepad/issues/280) |

## Evidence and decision table

| Question | Pinned evidence | Decision for virtualgamepad | Remaining limit |
| --- | --- | --- | --- |
| Nominal Pro USB report interval | [Linux hid-nintendo at 79eb6679](https://github.com/torvalds/linux/blob/79eb6679ef6a0d5ea68da53a8321fb1dc72299b9/drivers/hid/hid-nintendo.c#L1437-L1497) comments describe approximately 15 ms for USB, 8 ms for Bluetooth, 11/15 ms observed in the author's unspecified setup; kernel begins at 15 ms and estimates moving average. Same lineage as previously pinned `audio-linux-hid-nintendo`. | Treat 15 ms as a **source-grounded USB comparison target**, not a mandated universal report scheduler. Do not equate it to Bluetooth 120 Hz notes or OpenPuck's 4 ms emulation loop. | Neither Linux source revision is a newly reproduced USB reference trace; the original conflict stays documented, and #280 remains physical. |
| Does a console request colour SPI? | [pcble2gamepad README at 97084db](https://github.com/wozt/pcble2gamepad/blob/97084dbdc6f83d16663b32a0721ec6b713e2bbe6/README.md#L109-L135) reports the Switch 2 requesting offset 0x6050 length 13 and later offset 0x603D length 25, and displaying four adjustable colour fields from the emulator. | Include these exact **read ranges and overlap behavior** as source-backed console compatibility test cases when this consumer is in scope. Keep colour identity optional and provenance-labelled; never fabricate a retail colour. | It is a maintainer account of a real console against an emulator, not a public, independently reviewed capture, not original Switch console proof, and not a physical retail Pro observation. |
| What must not be overwritten by calibration data? | [Emulator implementation](https://github.com/wozt/pcble2gamepad/blob/97084dbdc6f83d16663b32a0721ec6b713e2bbe6/poc/protocol.c#L137-L232) and [emulator regression](https://github.com/wozt/pcble2gamepad/blob/97084dbdc6f83d16663b32a0721ec6b713e2bbe6/poc/test-protocol.c#L19-L92) reserve the 0x6050 boundary after 0x603D..0x604F; colour layout is four groups of 3 bytes over 0x6050..0x605B, followed by a design byte at 0x605C. | When responding to requested SPI ranges, resolve requested offset and length precisely rather than using an overly broad synthetic calibration table that masks colour fields. Test both request windows. | The implementation's factory marker and colour values are compatibility choices, not proof of actual retail flash contents, firmware variants or all-0xFF reactions. |

## Relationship to existing records

- `swpro-l0-device-usb-cadence-conflict` remains a correct account of conflicting **source models**. The more specific Linux USB estimate is not an independent retail measurement. `swpro-l0-device-physical-usb-period-unknown` remains unknown. Neither record is superseded.
- `swpro-l0-consumer-colour-spi-no-evidence` remains true **for the inspected Linux hid-nintendo and SDL 3.2.0 initialization paths**. The new console observation changes the broader consumer evidence ceiling, not those consumers' behavior, and it does not establish handling of an unavailable/all-0xFF colour block. Do not supersede that scoped claim.
- The existing `swpro-dekunukem-spi-flash-notes` pins the related layout, but the newly pinned pcble2gamepad sources add a separately authored emulator and a reported real-console consumer request. Its implementation and README share one lineage, not independent retail-device corroboration.
- Related physical checks [#279](https://github.com/anderstvoss/virtualgamepad/issues/279) and [#280](https://github.com/anderstvoss/virtualgamepad/issues/280) remain unresolved. [#161](https://github.com/anderstvoss/virtualgamepad/issues/161) owns the broader identity/variant metadata policy.

## Proposed physical gates — not run

**#280 cadence:** With owner-approved reference Switch Pro, record the active USB transport/backend and full-report mode, then timestamps for a sustained 0x30 stream during idle and motion. Report median, spread, outliers and lost/duplicated report counts, separately from Bluetooth and virtual-emulator reports. Compare to 15 ms, 8 ms and 4 ms **as hypotheses**, not hard acceptance thresholds.

**#279 colour:** On approved reference hardware and compatible console/host, capture only sanitized request metadata (offset, requested length, reply length, ACK/error class and outcome; no payload, identifying fields, serials or calibration). Compare 0x6050 length 13 and 0x603D length 25 and a documented unavailable-colour response. Determine whether the consumer actually requests, ignores, or rejects a colour response before declaring any universal fallback. No writes to reference SPI.

## Publication boundary

No firmware analysis, real-device dumps, packet bytes, identifiers or copyrighted source excerpts are included. All source files are cited through pinned revisions and SHA-256 source records. The owner must validate any proposed physical or console acceptance on hardware; this pass changes only the research corpus.
