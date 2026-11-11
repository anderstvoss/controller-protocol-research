# Switch Pro — HOME light and NFC/MCU boundaries

[← Switch Pro overview](index.md) · [Report protocol](protocol.md) · [Output/calibration](calibration-and-consumers.md)

> **2026-11-10 research addition.** These are source-derived feature distinctions, not tests of retail controller hardware or claims of implemented support.

## HOME light is not a fifth player LED

The Switch Pro has **four player indicators** and a distinct HOME-button light. The pinned Linux `hid-nintendo` consumer uses subcommand `0x30` for player indicators and `0x38` for HOME illumination. Linux exports HOME as an additional LED-class object with brightness **0–15**; although it may label that object with a fifth player-function name, **the hardware purpose is HOME illumination**. If the initial `0x38` exchange fails, Linux may omit that auxiliary LED object without failing controller attachment. [swpro-cgap-home-led-consumer](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/swpro-cgap-home-led-consumer.json).

A realization that advertises a generic ACK but discards HOME brightness can appear operational while lacking output fidelity. The right model is *four player lights plus independent HOME brightness*, not five player lights. Actual HOME intensity, patterns and ACK payloads are still unmeasured. [switch-pro-gaps.md](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/docs/switch-pro-gaps.md).

## NFC/MCU is a different transport-dependent question

Pinned community Nintendo controller-**family** notes describe output `0x11`, input `0x31` and MCU subcommands `0x20`–`0x22`. That establishes a possible family protocol path, **not** an observed Switch Pro-specific NFC transaction. The Joy-Con Right's separate NFC state machine must not be transplanted into a Switch Pro realization. [swpro-cgap-nfc-mcu-family-context](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/records/claim/swpro-cgap-nfc-mcu-family-context.json).

Nintendo product documentation (supplementary, **not** a pinned wire capture) describes an NFC touchpoint and states that NFC does **not** operate while *Pro Controller Wired Communication* is enabled. Consequently, the missing NFC path in a USB/wired virtual Switch Pro is **not by itself a failure of expected wired operation**. A wireless/native NFC realization would require separate transport, host workflows, report exchanges and hardware evidence. See [switch-pro-nfc-gaps.md](https://github.com/anderstvoss/controller-protocol-research/blob/ce6b8d3b70fd0957135eb921ef6098988f355cb1/docs/switch-pro-nfc-gaps.md).

## Research gates

Test HOME-light output independently from the player indicators, recording host command, reply and visible behavior. For NFC, first establish a real Pro-specific **wireless** consumer/transaction path, without recording tag contents or transplanting sibling Joy-Con behavior. No such physical tests are recorded in this addition.
