# Switch 1 Joy-Con (R) — NFC/IR MCU source ledger (B)

**Joy-Con research, prep for virtualgamepad #297.** This is **source-only** research. No Joy-Con (R), NFC tag, infrared camera, Linux host, on-air packet or virtualgamepad runtime was tested. NFC/IR belongs specifically to the right Joy-Con. No NFC tag dumps, authentication keys, real identifiers, raw captures, firmware or upstream code are included.

The shared Nintendo subcommand wrapper and full input prefix are already covered by `swpro-l0-device-subcmd-ack-byte` and `swpro-l0-device-report30-full`; this ledger records only the distinct MCU extension. The two independent consumer implementations examined—Yamakaky's `joy` MIT Rust code and Eden's GPL Joy-Con code (derived in part from yuzu, CTCaer, and dekuNukem)—are **source lineage**, not independently observed retail behavior. dekuNukem's pinned reverse-engineering notes are research leads rather than retail captures in this corpus.

## B1. MCU activation and packet framing

| Stage | Protocol-oriented consumer source evidence | Limit |
| --- | --- | --- |
| Enter MCU report mode | Send ordinary controller subcommand `0x03` selecting `0x31`, rather than standard `0x30`. The `0x31` input retains the controller prefix and three IMU samples, then appends the MCU region at report byte 49, up to byte 361 inclusive (313 bytes). | `swpro-dekunukem-bluetooth-hid-notes`, `joycon-b-yamakaky-mcu`. Exact controller report length may depend on HID transport framing; no hardware read. |
| MCU power/state | Ordinary subcommand `0x22` distinguishes suspend (0), resume (1) and update mode (2). Consumer sequence enables MCU, waits for standby, configures a target mode (NFC or IR), waits for target status, and then issues mode-specific requests. | `swpro-dekunukem-bluetooth-hid-subcommands-notes`, `joycon-b-eden-nfc`, `joycon-b-eden-irs`. |
| MCU configuration | Controller subcommand `0x21` passes an MCU configuration envelope; subcommand `0x20` resets MCU. Consumer code differentiates nested mode selection and IR register commands; CRC-8 with polynomial `0x07` protects command envelopes. | `joycon-b-yamakaky-mcu`, `joycon-b-eden-types`. Do not conflate outer controller subcommand `0x21` with nested MCU command ID or input report `0x21`. |
| MCU request / reply | MCU output report `0x11` carries request subtype and packet/check data after rumble field. MCU input `0x31` region includes status/read-data classes (e.g. IR frame class, NFC state/read class) as well as potential busy/empty states. | `joycon-b-yamakaky-mcu`, `joycon-b-yamakaky-ir`. Retail sequence timing and all error statuses unverified. |

**Critical distinction:** entering report mode `0x31` does not by itself initialize the MCU for IR or NFC. The source notes warn that MCU region can remain zero until configuration and explicit MCU requests. Standard controller `0x30` reports do not carry the MCU payload.

## B2. NFC detect/read/write flow (no tag contents or keys)

Eden's pinned Joy-Con input consumer `joycon-b-eden-nfc` implements the following *source-described* stateful protocol:

1. Enter mode `0x31`, enable MCU, transition through standby, configure NFC mode and wait for NFC ready. Request stop-polling initially to establish a known state.
2. **Detect:** start polling; await polling state and inspect NFC-state responses indicating a tag present. Extract only the *field format* (tag type and length of opaque identifier), not any actual identifier value.
3. **Read:** request a tag data transfer; pull successive indexed MCU packet fragments, assemble blocks in order, and require a terminal completion state. A lost-tag status interrupts the transfer. Consumer implementation can also issue MIFARE read operations; corresponding authentication material must not be recorded.
4. **Write:** detect the target; compare the opaque tag identity to intended target; stop polling, return to ready, restart in write-ready mode; send indexed write payload fragments, require write-done status, then stop polling. This does **not** imply any arbitrary tag or operation is supported.
5. Timeouts, state retries, tag-loss behavior and application-visible errors are explicit in the consumer. A permission-granted HIDAPI node alone does not prove NFC works.

**No evidence:** retail NFC keys/secure data (deliberately out of scope), exact behavior for unsupported tags and all firmware revisions, physical field strength, RF timing or verified successful tag write. No tag content was read or published.

## B3. IR image transfer and configuration

Yamakaky's MIT-licensed parser and Eden's GPL consumer describe MCU IR modes including pointing, clustering (`0x06`) and image transfer (`0x07`). The camera configuration programs MCU mode plus paged registers: resolution on page 0, register `0x2e`; exposure/digital-gain on page 1; near/far LEDs, exposure mode, filtering, flip, denoise, pixel threshold and finalization are separate register operations. Source-listed resolutions:

| Pixel size | Image-transfer fragment index range | Derived count at 300 pixels/fragment |
| --- | --- | --- |
| 320 × 240 | 0 through 255 | 256 |
| 160 × 120 | 0 through 63 | 64 |
| 80 × 60 | 0 through 15 | 16 |
| 40 × 30 | 0 through 3 | 4 |
| 20 × 15 | single fragment | 1 |

In the pinned image-transfer implementation, the `0x31` MCU subregion's IR data class identifies a **fragment number**; an image fragment carries **300 grayscale bytes** starting at report offset 59. The consumer accepts the expected next fragment, acknowledges its index, repeats acknowledgment for a duplicate, or requests retransmission of a missing fragment. A frame buffer is assembled from these fragments; CRC-8 guards outbound MCU request/configuration data. This is more than recognizing report `0x31`; loss and retry handling matter.

**Evidence split:** the Yamakaky source lists resolutions through 40×30 but not 20×15; Eden adds 20×15, and 20×15 support is **single-implementation** at this research pin. Exact register defaults, optical fidelity, exposure limits, buffering and timing across actual firmware revisions are **No evidence** until physical testing. No actual camera images were collected.

## Proposed local acceptance — not run

- Establish a right-only Joy-Con MCU-capable UHID instance with ordinary input and `0x31` report framing; observe correct `0x20`/`0x21`/`0x22` responses and nested status transitions without real MCU hardware.
- Use bounded synthetic, nonpersonal NFC state transitions (not a tag dump, identifier or key). Verify detect → read terminal state, tag-loss recovery and write-ready/write-done errors as *protocol simulations*, clearly separated from NFC hardware emulation.
- Simulate 160×120 grayscale frame fragments, deliberately drop and duplicate fragments, and verify re-request, ACK, 64-fragment assembly, CRC and clean cancellation. Synthetic images are not a camera fidelity claim.
- On authorized hardware later, privately validate MCU version negotiation, actual tag/IR output behavior and latency. Do not ingest NFC contents or identifying bytes into the public corpus.

**Status:** B1–B3 have source-described flow and fields. Physical parity, complete NFC payload semantics and all MCU error cases remain **No evidence**.

**Cloud agent (Joy-Con research)**
