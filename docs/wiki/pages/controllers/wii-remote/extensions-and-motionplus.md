# Wii Remote — Nunchuk, Classic, MotionPlus and hotplug

[← Wii overview](index.md) · [Base protocol](protocol-and-memory.md)

> **Scope:** reviewed corpus 2026-11-09; source and virtual-host evidence do not establish a retail Wii Remote physical capture.

## Topology

An accessory is **not just an extra button map**. The remote must expose changes in extension status and internal register identity, change report mode/packing where relevant, and return calibrated data after consumer initialization. Core extension types in the corpus include Nunchuk (stick, C/Z, accelerometer), Classic Controller (buttons, analog sticks, triggers), and external/integrated MotionPlus (gyro plus optional downstream Nunchuk/Classic). The state model should allow adding further extensions without rewriting the remote transport.

Kernel and SDL source behavior: [`wii-kernel-extension-init`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-kernel-extension-init.json), [`wii-sdl-extension-modes`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-sdl-extension-modes.json).

## MotionPlus activation and routing

| State/procedure | Source-described role |
| --- | --- |
| Inactive MP | Probe ID in `A600FA`; read/register map around `A600` |
| Activate external MP | Write `A600F0=55`, then `A600FE` mode `04` (MP-only), `05` (Nunchuk pass-through) or `07` (Classic pass-through) |
| Active MP identity | Read `A400FA` as part of mapped/activated state |
| Motion data | Six extension bytes in selected report modes; discriminator distinguishes gyro from downstream accessory samples |
| Downstream ID in Dolphin | When pass-through attached, **`A400F6/4`** conditional identity mirror |
| Calibration in Dolphin | MP `A40020/32`; downstream calibration **`A40040/16`** after identity/mode gates |

These are specific **consumer/source** expectations, not all physically verified registers. The A400F6 and A40040 addresses are particularly important to Dolphin's current ControllerInterface task chain; the research explicitly distinguishes likely hardware-derived meaning from Dolphin-specific compatibility accommodation: [`wii-gap-dolphin-attach-passthrough-four-byte-id-f6`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-gap-dolphin-attach-passthrough-four-byte-id-f6.json), [`wii-gap-dolphin-attach-report-calibration-and-later-gates`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-gap-dolphin-attach-report-calibration-and-later-gates.json), [Dolphin sequence and limits](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-dolphin-attachment.md).

## Hotplug and status edges

A status `0x20` extension bit change may force SDL/Dolphin/kernel to reset cached extension identity, reporting mode, calibration or MotionPlus mode and retry. That makes spurious toggles a real compatibility hazard. The source research recommends **opt-in, creation-time compatibility transitions** for external MP until physical status-edge behavior is measured, not asserting every activation sends a disconnect event. [activation status decision](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-motionplus-activation-status.md).

## Integrated Remote Plus

The original Remote and later `TR` do not have identical discovery rules, while early non-TR Plus identities overlap the original. Integrated MotionPlus cannot physically hot-unplug; it may still be **logically inactive**. Avoid advertising an identity-only `0330` virtual device with no gyro capability as faithful Remote Plus. [`wii-early-plus-revision-gap`](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/records/claim/wii-early-plus-revision-gap.json), [model variants and implementation choice](https://github.com/anderstvoss/controller-protocol-research/blob/ab74f66274589a7229633f0fe8654490c3d19a12/docs/wii-remote-plus.md).

## Extension roadmap

Keep report shape generation, accessory-specific register/memory providers, calibration source and hotplug state as independently replaceable modules. This permits future Classic Pro, guitar/percussion/balance-board or other adapters without reworking the base codec. No unmeasured exotic accessory should be claimed implemented just because the topology supports plugins.
