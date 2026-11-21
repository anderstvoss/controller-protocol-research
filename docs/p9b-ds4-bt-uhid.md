# DualShock 4 Bluetooth-bus UHID: source-only gap brief

**Scope:** consumer source review only. No real-device capture, host run, pairing, radio, or Bluetooth stack. Every proposed test is **not run**.

## Ranked evidence gaps

| Rank | Gap | Goal | Evidence ceiling | Claim |
| --- | --- | --- | --- | --- |
| 1 | Bluetooth input report modes, CRC and offsets | playable | pinned kernel/SDL consumer behavior; physical fidelity unknown | pending |
| 2 | Bluetooth output flags and CRC | playable | pinned kernel/SDL consumer behavior; physical actuation unknown | pending |
| 3 | Calibration and open-time feature requests | playable | pinned kernel/SDL consumer behavior; calibration contents unknown | pending |
| 4 | Identity and descriptor | faithful | pinned kernel consumer expectation; physical descriptor unknown | pending |

Further details and source-backed claims follow in this brief.
