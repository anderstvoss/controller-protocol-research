# Switch Pro controller gaps

Source-only gap pass for the Switch Pro realization (virtualgamepad #156), reviewed against research `main` e1a0591 and virtualgamepad `main` 4ac4232. No hardware was used and no physical test was run.

Most open Switch Pro questions are already tracked and are not restated here: subcommand ACKs (#276), wired battery byte (#277), IMU gating (#278), SPI calibration and colours (#279) and USB report period (#280), with the `swpro-l0-*` claims in `docs/ledgers/switch-pro-l0.md`. This pass found one gap that no existing record or issue covers.

## Ranked gaps

| Rank | Gap | Playable or faithful | Evidence ceiling now | Related |
| --- | --- | --- | --- | --- |
| 1 | HOME-button light (subcommand 0x38) is not modelled | Faithful only; inputs and the four player lights are unaffected | Source evidence (Linux consumer) | `swpro-cgap-home-led-consumer`, #156, #276 |

## 1. HOME-button light

The Switch Pro has four player-indicator lights and a separately controlled HOME-button light. Pinned Linux `hid-nintendo` (`audio-linux-hid-nintendo`, commit 4056b3c) defines subcommand 0x38 for the HOME light separately from player lights (0x30), and for right-capable controller types, which include the Pro, registers a separate HOME LED class device with brightness 0 to 15. Each brightness change sends 0x38 with five payload bytes. The kernel names that LED class device after a fifth player function, but the hardware is the HOME button light, not a fifth player indicator.

At probe time the kernel sends 0x38 once to set brightness 0. If that send fails, it logs a warning and skips registering the HOME LED, without failing the probe. A virtual device that does not acknowledge 0x38 therefore loses the Linux HOME LED quietly.

**virtualgamepad today:** `switch_pro.rs` declares `OutputKind::PlayerIndicator { count: 4 }`, and the retained output state has `player_lights` but no HOME-light field. `switch_subcommand_reply()` has no 0x38 case and answers it with the generic 0x80 acknowledgement. That generic ACK is what keeps the Linux HOME LED registered today; the requested brightness is accepted and discarded.

**Implication:** keep the player indicator count at 4. A faithful realization would retain HOME-light brightness as its own output rather than widening the player count.

**Not established:** retail brightness response, fade or pattern behaviour, the real ACK bytes for 0x38, and how the five payload bytes map to light behaviour beyond what Linux sends.

**Proposed physical gate (not run):** on owner-approved reference hardware, step HOME-light brightness independently of the player lights, and record the host requests, ACKs, visible behaviour and Linux LED class side effects. This fits the #276 capture scope.
