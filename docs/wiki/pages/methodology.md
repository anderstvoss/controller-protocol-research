# Evidence interpretation and citation rules

## Authority and scope

A wiki statement should point to the **smallest applicable claim record** (for example [`steam-puck-interface-selection`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/steam-puck-interface-selection.json)), not just a long narrative ledger or an unpinned upstream page. Each claim specifies controller, revision, firmware, transport, scope, status, source IDs, experiment IDs, conflicts and supersessions. Follow those links before using a claim to implement byte-level behavior.

The registry is an evidence catalogue, **not a controller support matrix**. Features existing in source code are not necessarily implemented in virtualgamepad, accepted by SDL, or observed on hardware.

## Evidence statuses

| Status | Use in prose |
| --- | --- |
| `unknown` | No qualified answer for the stated question; retain the gap. |
| `inferred` | A hypothesis derived from other evidence, not a direct observation. |
| `source_supported` | A claim grounded in pinned source/documentation at its stated revision. |
| `independently_corroborated` | Distinct source lineages support the stated claim; still not automatically physical. |
| `physically_observed` | A controlled physical experiment supports the scoped observation; not comprehensive fidelity. |
| `physically_validated` | Controlled physical experiment, physical fixture and semantic outcome support the specific validation. |
| `conflicted` | Competing evidence remains unresolved; preserve both interpretations. |
| `rejected` | Evidence rejects the claim in the explicitly recorded rejection scope. |

See [source validator](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/tools/validate.py) and [evidence-status documentation](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/README.md). **Source-only** is a *transport/acquisition scope*, not a third role. `evidence_role=device` and `evidence_role=consumer` are separate and must not be conflated.

## Distinguish the layers

| Layer | What a record can establish | What it cannot establish alone |
| --- | --- | --- |
| Device protocol research | Report encoding or behavior as described by pinned community/device implementations | Physical identity, byte-exact retail parity |
| Kernel/SDL source inspection | What a fixed driver version expects, sends, exposes and rejects | That a real controller replied, or that Steam selected the same backend |
| Virtual-host experiment | Which virtual node/shape a measured host accepted | Retail physical behavior |
| Physical controlled experiment | The particular observed controller/session/result | Universal behavior across firmwares or transports |
| Historical notes | Leads and retained operator evidence within their stated provenance | Missing original trace details or stronger evidence than the record status |

**Examples:** the Puck [`puck-historical-physical`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/puck-historical-physical.json) historical claim remains conflicted despite a current OpenPuck `1304` mode ([`puck-current`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/puck-current.json)). The Sony gyro association after `dummy_hcd` is a hypothesis ([`ds-l0-uhid-gyro-association-hypothesis`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/ds-l0-uhid-gyro-association-hypothesis.json)), not an established causal mechanism.

## Source and experiment provenance

Open a claim's `sources` and `experiments` fields. The [source record](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/source) pins URL, revision, SHA-256, lineage and locator; sources derived from the same code are *not* independent confirmation. The [experiment](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/experiment) describes procedure and semantic outcome; [fixture metadata](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/fixture) contains hashes and transformations. Sensitive raw captures intentionally are **not** republished.

## Citation and editorial policy

- Quote or paraphrase the source accurately, then link the applicable claim ID. For multi-part assertions use multiple claims.
- Include applicability when it affects interpretation: USB versus Bluetooth, firmware, driver version, test environment and whether hardware was operated.
- Present source-vs-physical conflicts and unconfirmed flags prominently. Do not infer negative behavior from absence of decoder branches.
- Supplemental external reading must be explicitly labeled **not yet corpus-reviewed** and must not upgrade a claim.
- On every requested refresh, identify the exact reviewed corpus commit; changes to the wiki are separate reviewed commits.
