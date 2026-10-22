# Wii Remote — cloud research checkpoint 1

**Snapshot:** `anderstvoss/controller-protocol-research` main at `36bc9947180c8118c0702571b71e5eeb9354832d` (after WiiBrew-2 PR #24). **85 Wii claims**, **7 claims with status `unknown`**, **7 unique pairs appearing in `conflicts_with`**, and 10 C5/W1 virtual-host experiment records. This is an inventory and source-evidence decision aid; **not** a C5 implementation specification, API freeze, physical device capture, or declaration of retail compatibility. New research records: **none**.

This follows [`wii-remote-l0.md`](wii-remote-l0.md) and retains its separation among pinned consumer source, emulator source, synthetic C5 expectations and physical acceptance. Each identifier below resolves to `records/claim/<id>.json`, except the explicitly identified experiment IDs, which resolve to `records/experiment/<id>.json`. Source-only claims are **not** automatically firmware or hardware facts. Do not change any existing `wii-c5-*` or `wii-w1-*` record based on this checkpoint.

**Source role legend:** **Kernel** = pinned Linux hid-wiimote host interpretation; **SDL** = SDL3 HIDAPI client; **Dolphin** = emulator/active HID consumer; **rnconrad** = historical emulator, with undocumented retail provenance and no identified repository license; **WiiBrew** = community protocol documentation pinned to original oldids (Wiimote 123257, Extension Controllers 121955, Wii Motion Plus 120079); **C5** = curated synthetic source-modeled claim or fixture; **W1/C5 host run** = bounded Linux virtual-host experiment, *not a physical controller test*; **Unknown** = distinct unvalidated physical/reference claim. Omitted roles have no record supporting that particular topic.

## 1. Evidence inventory by area

### Revision, Bluetooth identity and authentication
- **Kernel:** `wii-kernel-bluetooth-match`, `wii-original-remote-consumer-revision`, `wii-tr-consumer-revision`, `wii-gap-early-plus-kernel-name-ambiguity`
- **rnconrad:** `wii-gap-rnconrad-l2cap-psms`
- **WiiBrew:** `wii-gap-wiibrew-wiimote-plus-bluetooth-identity`, `wii-gap-wiibrew-tr-authentication-order`
- **Unknown:** `wii-early-plus-revision-gap`
- **Virtual-host experiment:** `wii-c5-bt-host-binding`

Nintendo Bluetooth names, VID/PIDs and TR channel-authentication sequence are sourced transport/consumer facts. UHID bus-5 binding does **not** demonstrate radio pairing or establish an early non-TR Plus physical discriminator.

### Input/output report IDs, modes and HID/SDP descriptor
- **Kernel:** `wii-kernel-report-modes`
- **SDL:** `wii-sdl-extension-modes`
- **rnconrad:** `wii-gap-rnconrad-candidate-sdp-descriptor-structure`
- **WiiBrew:** `wii-gap-wiibrew-data-report-powerup-default`, `wii-gap-wiibrew-continuous-versus-change-reports`
- **C5/Dolphin-derived:** `wii-c5-report-layouts`, `wii-c5-synthetic-fixtures`
- **Unknown:** `wii-gap-retail-hid-descriptor-capture-unknown`
- **Virtual-host experiment:** `wii-w1-sdl-host-run`

Report IDs and payload lengths have multiple source counterparts. The C5 authored vendor-page descriptor is *synthetic*, while rnconrad's 217-byte SDP candidate is a Game Pad top-level descriptor with separate speaker output IDs; retail origin/licensing remain unproven. WiiBrew describes mode `0x30` at power-up, with accelerometer LSBs embedded in core-button bits **only for modes carrying accelerometer data**; interleaved `0x3e/0x3f` use button-byte space for Z-axis information. Neither source yields a measured cadence.

### Status 0x20, command acknowledgement 0x22, memory response 0x21
- **Kernel:** `wii-kernel-status-ack-flow`
- **Dolphin:** `wii-gap-dolphin-out-of-range-write-ack`
- **rnconrad:** `wii-gap-rnconrad-out-of-range-write-reply`
- **WiiBrew:** `wii-gap-wiibrew-status-20-resend`
- **C5/Dolphin-derived:** `wii-c5-memory-errors`, `wii-c5-report-layouts`
- **Virtual-host experiment:** `wii-w1-battery-rumble-led-host-run`

WiiBrew documents unsolicited attach/detach statuses and the need to reissue output mode request `0x12` after a status transition. Historical emulators disagree on whether an invalid-address **write** produces `0x21` or `0x22`, even when they agree on error 8. C5 follows its declared compatibility source, not an authenticated retail error trace.

### Memory, EEPROM and address boundaries
- **Dolphin:** `wii-dolphin-memory-routing`, `wii-gap-dolphin-eeprom-inclusive-bound`
- **rnconrad:** `wii-gap-rnconrad-eeprom-exclusive-upper-bound`, `wii-gap-rnconrad-eeprom-host-filesystem`
- **WiiBrew:** `wii-gap-wiibrew-host-eeprom-visible-range`, `wii-gap-wiibrew-eeprom-address-mirroring`
- **C5/Dolphin-derived:** `wii-c5-memory-errors`
- **Unknown:** `wii-memory-size-hypothesis`

The community host-facing range is `0x0000..0x16ff`; high-address mirroring is documented for host EEPROM **reads**. Dolphin permits access ending at `0x16ff`; rnconrad's `>0x16ff` check appears off by one. rnconrad also ACKs some attempted EEPROM writes despite using a read-only host file mode. Physical EEPROM size and writable extents are **not** thereby proven. The C5 import path deliberately uses caller-provided extent.

### Extension identifiers, initialization, encryption and data-format selector
- **Kernel:** `wii-kernel-extension-init`, `wii-gap-linux-plaintext-extension-init`
- **SDL:** `wii-gap-classic-pro-host-classifier-tail`
- **Dolphin:** `wii-gap-dolphin-encrypted-extension-lazy-key`
- **rnconrad:** `wii-gap-rnconrad-encrypted-extension-toggle`, `wii-gap-rnconrad-encryption-key-trigger`
- **WiiBrew:** `wii-gap-wiibrew-classic-pro-identity`, `wii-gap-wiibrew-extension-new-init`, `wii-gap-wiibrew-extension-encrypted-setup`, `wii-gap-wiibrew-extension-data-format-selector`, `wii-gap-wiibrew-additional-accessory-identities`
- **C5/Dolphin-derived:** `wii-c5-extension-identifiers`
- **Unknown:** `wii-extension-encryption-gap`, `wii-gap-classic-pro-full-id-physical-unknown`
- **Virtual-host experiment:** `wii-c5-bt-host-binding`

Linux commonly requests plaintext setup using F0/FB. WiiBrew documents encrypted sessions, three-part key writes and mutable `0xA400FE` format selection (Classic format codes 01/02/03). Classic Pro's complete ID now has **documentary** evidence, but physical OEM/third-party revisions remain unverified. Additional Guitar/Drums/Turntable/TaTaCon/tablet/Balance Board/Densha de GO identities are **outside current C5 support**; Classic Pro itself is enumerated as **not-supported** by the acceptance manifest.

### MotionPlus: activation, pass-through, deactivation, identity and calibration
- **Kernel:** `wii-kernel-motionplus-pass-through`, `wii-gap-tr-motionplus-register-host-negotiation`, `wii-gap-linux-external-motionplus-poll-interval`
- **SDL:** `wii-gap-sdl-linux-motionplus-kernel-ownership`
- **Dolphin:** `wii-gap-dolphin-motionplus-crc32-calibration`
- **rnconrad:** `wii-gap-rnconrad-encrypted-extension-toggle`
- **WiiBrew:** `wii-gap-wiibrew-builtin-motionplus-inactive-id`, `wii-gap-wiibrew-motionplus-id-and-activation`, `wii-gap-wiibrew-motionplus-deactivation`, `wii-gap-wiibrew-motionplus-passthrough-field-moves`, `wii-gap-wiibrew-motionplus-crc32-calibration`, `wii-gap-wiibrew-motionplus-host-reprobe`
- **C5/Dolphin-derived:** `wii-c5-extension-packing`
- **Virtual-host experiments:** `wii-c5-bt-host-binding`, `wii-w1-numeric-bt-host-run`

Modes `04/05/07` and six-byte active/inactive suffix differences are documented. WiiBrew reports single-write `0x55` initiation at `0xA600F0` (a second FB write is not necessary in that description), and deactivation via `0x55` at `0xA400F0` returns control to the downstream accessory with unplug/plug statuses. Pass-through packs lossy data and uses byte-5 bit 1 as gyro-versus-extension discriminator. Distinguish external, built-in and early-Plus identity claims; source algorithms do not prove physical gyro scale.

### IR: basic/extended/full, sensitivity, initialization and intensity
- **Kernel:** `wii-kernel-ir-mode-policy`, `wii-kernel-evdev-ir`, `wii-gap-linux-ir-output-metadata-loss`
- **Dolphin:** `wii-gap-dolphin-ir-extended-point-format`, `wii-gap-dolphin-ir-full-point-approximation`
- **WiiBrew:** `wii-gap-wiibrew-ir-extended-full-metadata`, `wii-gap-wiibrew-ir-sensitivity-configuration`, `wii-gap-wiibrew-ir-initialization-uncertainty`
- **C5/Dolphin-derived:** `wii-c5-camera-no-points`
- **Unknown:** `wii-gap-ir-full-mode-intensity-unknown`
- **Virtual-host experiments:** `wii-w1-numeric-bt-host-run`, `wii-w1-numeric-uinput-host-run`

The evdev open path requests **basic** IR, not extended/full; full blob metadata is therefore absent there. WiiBrew documents three- and nine-byte point fields, sensitivity blocks and uncertain camera initialization. Dolphin's full-mode intensity uses an approximation derived from truncated bounds, not a validated optical scale. A documented 50-ms interbyte workaround is not a proven requirement.

### Wii Remote, Nunchuk, Classic and MotionPlus calibration
- **Kernel:** `wii-gap-linux-accelerometer-raw-evdev`
- **SDL:** `wii-gap-sdl-stick-runtime-calibration`
- **Dolphin:** `wii-gap-dolphin-calibration-additive-checksums`, `wii-gap-dolphin-eeprom-accel-calibration-layout`, `wii-gap-dolphin-eeprom-ir-calibration-layout`, `wii-gap-dolphin-nunchuk-calibration-layout`, `wii-gap-dolphin-classic-calibration-layout`, `wii-gap-dolphin-motionplus-crc32-calibration`
- **rnconrad:** `wii-gap-rnconrad-calibration-duplicate-registers`
- **WiiBrew:** `wii-gap-wiibrew-calibration-redundancy-fallback`, `wii-gap-wiibrew-motionplus-crc32-calibration`
- **Unknown:** `wii-gap-extension-calibration-checksum-unknown`
- **Virtual-host experiments:** `wii-w1-numeric-bt-host-run`, `wii-w1-numeric-uinput-host-run`

Dolphin generates synthetic fallback calibration *only if no per-controller saved EEPROM image is loaded*. Source checksum rules and layouts do not license fabricated OEM values. rnconrad mirrors a 16-byte extension block into 0x20 and 0x30, while Dolphin leaves 0x30 zero on reset. Linux evdev subtracts a fixed acceleration bias; SDL learns initial stick center from the first sample instead of consuming these register blocks. W1 host runs test numerical conversions, **not** calibration integrity.

### Outputs: keys, LEDs, rumble, battery and speaker exclusion
- **Kernel:** `wii-kernel-outputs-battery`
- **rnconrad:** `wii-gap-rnconrad-candidate-sdp-descriptor-structure`
- **WiiBrew:** `wii-gap-wiibrew-status-20-resend`
- **C5/Dolphin-derived:** `wii-c5-evdev-consumer-shape`, `wii-c5-evdev-native-values`
- **Virtual-host experiments:** `wii-w1-battery-rumble-led-host-run`, `wii-w1-sdl-host-run`

Kernel devices distinguish LED-class, FF_RUMBLE and power_supply. W1 observed rumble upload/play/erase and battery conversion (raw 192 → 75%); **LED brightness writes returned EACCES**, so LED acceptance remains blocked. Speaker report IDs are found in an unlicensed historical candidate SDP descriptor; speaker is explicitly refused by C5.

### Evdev native mappings, absinfo and companion nodes
- **Kernel:** `wii-kernel-evdev-base-keys`, `wii-kernel-evdev-accelerometer`, `wii-kernel-evdev-ir`, `wii-kernel-evdev-nunchuk`, `wii-kernel-evdev-classic`, `wii-kernel-evdev-motionplus`, `wii-gap-linux-accelerometer-raw-evdev`
- **C5/Dolphin-derived:** `wii-c5-evdev-consumer-shape`, `wii-c5-evdev-native-values`
- **Virtual-host experiments:** `wii-w1-numeric-bt-host-run`, `wii-w1-numeric-uinput-host-run`

Selected-value W1 probes found the six expected role shapes and native event translations; missing IR `1023/1023` and out-of-advertised-range acceleration are intentionally preserved. UHID showed kernel fuzz, while uinput could not carry that field. These are bounded software observations, not complete domain/initial-neutral or physical acceptance.

### Cadence, host timeouts, hotplug and lifecycle
- **Kernel:** `wii-gap-linux-command-wait-timeout`, `wii-gap-linux-external-motionplus-poll-interval`
- **SDL:** `wii-gap-sdl-constant-input-inactivity-timeout`
- **WiiBrew:** `wii-gap-wiibrew-motionplus-host-reprobe`, `wii-gap-wiibrew-continuous-versus-change-reports`, `wii-gap-wiibrew-ir-initialization-uncertainty`
- **Virtual-host experiments:** `wii-c5-uinput-n1-host-run`, `wii-c5-uinput-n4-host-run`, `wii-c5-bt-n1-host-run`, `wii-c5-bt-n4-host-run`

Linux's ~one-second command completion wait, four-second external-MotionPlus poll, SDL's three-second inactivity disconnect and community-documented ~eight-second host discovery are **different host policies**. None is a measured Wii sensor-report period. N1/N4 C5 lifecycle runs restored resources and removed nodes on the tested host; there is **no accepted latency budget**.

### SDL3/Dolphin consumer adoption
- **SDL:** `wii-sdl-extension-modes`, `wii-gap-sdl-linux-motionplus-kernel-ownership`
- **Dolphin:** `wii-dolphin-hidapi-probe`
- **Virtual-host experiments:** `wii-w1-sdl-host-run`, `wii-w1-dolphin-host-run`, `wii-c5-bt-host-binding`

W1 could not open the exact owned hidraw handle (`EACCES`), blocking SDL Wii HIDAPI and Dolphin real-controller acceptance conclusions. SDL's fallback evdev path recognized **11 core buttons, zero axes/hats/sensors**. Dolphin app launch did not establish backend adoption; kernel driver binding alone does not make a full consumer-ready Wii Remote.

## 2. Host experiment ledger (virtual software only)

| Experiment ID | Outcome | What it establishes / does not establish |
| --- | --- | --- |
| `wii-c5-bt-host-binding` | passed | Linux wiimote driver bound to exact owned UHID bus-5 object; six input roles and shapes, rumble and power_supply present; LED writes EACCES; no physical Bluetooth |
| `wii-c5-uinput-n1-host-run` | passed | 10 creation/removal cycles at concurrency 1; missing consumer-open and first-neutral oracles |
| `wii-c5-uinput-n4-host-run` | passed | 40 creations/removals in 10 cycles at concurrency 4; no latency target |
| `wii-c5-bt-n1-host-run` | passed | 10 cycles at concurrency 1 on UHID; initialization-related close delays not performance acceptance |
| `wii-c5-bt-n4-host-run` | passed | 40 creations/removals at concurrency 4; resource restoration, not physical/gameplay acceptance |
| `wii-w1-numeric-uinput-host-run` | passed | Selected live values and ABS metadata; uinput cannot preserve fuzz; not full-domain measurement |
| `wii-w1-numeric-bt-host-run` | passed | Selected live Bluetooth-bus UHID values and kernel fuzz; not calibrated hardware |
| `wii-w1-battery-rumble-led-host-run` | blocked | Battery conversion and rumble succeeded, but LED brightness write permissions blocked the complete probe |
| `wii-w1-sdl-host-run` | blocked | SDL direct hidraw EACCES; fallback evdev core buttons only; no SDL HIDAPI device adoption demonstrated |
| `wii-w1-dolphin-host-run` | blocked | Offscreen Dolphin launched but sandbox hidraw EACCES; no confirmed real-controller connection |

All C5/W1 experiment statuses refer to the stored experiment records as authored. Do not relabel a partially successful **blocked** experiment as passed or a successful virtual-run as hardware validation. Host-policy/permissions require a separate owner decision.

## 3. Explicit conflicts (`conflicts_with` audit)

These are **all seven unique recorded relationships** on this snapshot (including one-way links to pre-existing claims). An arrow says who currently *records* the link; it does not mean the reverse file was edited or that the conflict is resolved.

| Source A | Source B | Link state | Documentary preference / remaining uncertainty |
| --- | --- | --- | --- |
| `wii-gap-rnconrad-eeprom-exclusive-upper-bound` | `wii-gap-dolphin-eeprom-inclusive-bound` | reciprocal | WiiBrew's inclusive host-visible last byte agrees with Dolphin, not rnconrad's likely off-by-one. Not a physical boundary test. |
| `wii-gap-rnconrad-eeprom-exclusive-upper-bound` | `wii-gap-wiibrew-host-eeprom-visible-range` | reciprocal | WiiBrew documentation favours host access ending at 0x16ff; keep `wii-memory-size-hypothesis` unknown. |
| `wii-gap-rnconrad-calibration-duplicate-registers` | `wii-gap-dolphin-nunchuk-calibration-layout` | reciprocal | rnconrad duplicates 0x20 at 0x30; Dolphin zeros separate 0x30 field. Pinned community sources do not settle retail register readback. |
| `wii-gap-rnconrad-calibration-duplicate-registers` | `wii-gap-dolphin-classic-calibration-layout` | reciprocal | Same disagreement for Classic; neither synthetic template is factory evidence. |
| `wii-gap-rnconrad-out-of-range-write-reply` | `wii-gap-dolphin-out-of-range-write-ack` | reciprocal | rnconrad replies with 0x21, Dolphin ACKs on 0x22. The independent WiiBrew records here do not arbitrate the failing-write **report type**. |
| `wii-gap-rnconrad-out-of-range-write-reply` | `wii-c5-memory-errors` | rnconrad → C5 only | C5 sources agree with Dolphin's write-ACK model. Candidate implementation deviation/review; no authenticated retail error response. |
| `wii-gap-dolphin-encrypted-extension-lazy-key` | `wii-gap-rnconrad-encryption-key-trigger` | Dolphin → rnconrad only | Dolphin marks any 0x40–0x4f key write dirty and regenerates upon encrypted read; rnconrad triggers immediately at 0x4c. WiiBrew's documented 6/6/4 writes do not settle execution order. |

No reverse `conflicts_with` relationship is fabricated in this document. Unlisted comparisons are not asserted as corpus conflicts. Resolve a pair only with independently attributable evidence; do not silently choose a software model.

## 4. Every claim still marked `unknown`

| Exact claim ID | What has narrowed the question | Resolution evidence / cloud-only limit |
| --- | --- | --- |
| `wii-early-plus-revision-gap` | WiiBrew documents pre-TR and -TR Bluetooth names, optional built-in MotionPlus IDs; Linux name classifier conflates original and early integrated non-TR units. | Physical **early non-TR Plus** and comparison original/TR: SDP/name, inactive/active MP register IDs, startup/extension and calibration observations. Cloud can research more sources but **cannot close physical revision identity**. |
| `wii-extension-encryption-gap` | WiiBrew documents encrypted enable and key write pattern; Dolphin/rnconrad disagree on regeneration; Linux/SDL mainly use plaintext initialization. | Reference Nunchuk/Classic and MotionPlus-pass-through host write/read traces for encrypted initialization plus checkable decoded response, preserving legal provenance. **Requires measured device or controlled host run**; cloud cannot authenticate retail key timing. |
| `wii-memory-size-hypothesis` | WiiBrew describes 0x1700 host-visible bytes and mirrored high address for reads; Dolphin agrees, rnconrad has likely off-by-one. | Model/revision-scoped physical reads at 0x16ff, 0x1700, straddling lengths and mirrored high-byte requests; safe write testing only with explicit owner consent. **Cloud cannot establish actual retail chip bounds**. |
| `wii-gap-classic-pro-full-id-physical-unknown` | WiiBrew provides six-byte Classic Pro ID; Linux/SDL classify by shared 0x0101 suffix, Dolphin models ordinary Classic. | Actual OEM Classic Pro, normal Classic and representative third-party accessory: full `0xA400FA` readback, selector `0xA400FE` behavior. **Documentation is not a capture**. |
| `wii-gap-extension-calibration-checksum-unknown` | Dolphin models Nunchuk/Classic fields with additive checksum, MotionPlus CRC; WiiBrew describes Wii Remote fallback; rnconrad mirrors extension block differently. | Physical Nunchuk, Classic, Classic Pro and MotionPlus calibration reads with independent checksum/field validation and fallback response; retain raw private. **Cloud cannot validate factory values or EEPROM provenance**. |
| `wii-gap-ir-full-mode-intensity-unknown` | WiiBrew identifies full-mode 9-byte fields; Dolphin derives intensity from approximate/clipped bounds, while kernel evdev exposes basic coordinates only. | Reference remote camera reports 0x3e/0x3f under controlled IR LED geometry/brightness/distance and a known sensor sensitivity configuration; correlate raw intensity/size/bounds. **Cannot be settled by software emulator inspection**. |
| `wii-gap-retail-hid-descriptor-capture-unknown` | rnconrad SDP embeds a 217-byte candidate with known SHA; C5 uses a different synthetic descriptor; SDL HIDAPI run blocked by hidraw access. | Authenticated, revision-labeled original/+/-TR SDP/HID descriptor read or a licensable verified primary source; compare collection, Array/Var and speaker IDs. **Cloud cannot infer provenance from an unlicensed historical repo**. |

The status of each listed record remains **`unknown`** in `main`. Source-backed checksum algorithms, layout definitions and published hex IDs may narrow how to design an experiment without promoting physical truth or implying that unknowns have been solved.

## 5. Candidate C5 impact audit — for implementing agent to decide

Read-only inspection of `anderstvoss/virtualgamepad` main: `crates/gr-curated-controllers/src/wii_remote/` and `acceptance/virtualgamepad.wii-remote.toml`. **Every entry below is candidate, for the implementer to decide**—not a requested code change, proposed patch, acceptance waiver or instruction to copy source-model defaults.

| Candidate question / documented deviation to revisit | Corpus evidence IDs | Current C5 file(s) or manifest | Disposition |
| --- | --- | --- | --- |
| On unsolicited extension-change status, is the documented host `0x12` resend/paused-stream handshake modeled and distinguished from C5's queued disconnect/reconnect status? | `wii-gap-wiibrew-status-20-resend`, `wii-kernel-status-ack-flow`, `wii-c5-report-layouts` | `codec.rs`, `controller.rs`, `lifecycle_tests.rs` | Candidate, for the implementer to decide; no retail status trace. |
| Does MotionPlus deactivation via `0x55` at `0xA400F0` expose the downstream extension and post-deactivation `0xA600FA` suffixes 04/05/07–05 in the documented order? | `wii-gap-wiibrew-motionplus-deactivation`, `wii-gap-wiibrew-motionplus-id-and-activation`, `wii-gap-tr-motionplus-register-host-negotiation` | `memory.rs`, `codec.rs`, `lifecycle_tests.rs` | Candidate, for the implementer to decide; do not collapse inactive external/built-in identities. |
| Are Nunchuk/Classic MotionPlus pass-through lossy field moves, record alternation and byte-5 bit-1 discriminator represented with the documented constraints? | `wii-gap-wiibrew-motionplus-passthrough-field-moves`, `wii-c5-extension-packing`, `wii-kernel-motionplus-pass-through` | `extensions.rs`, `memory.rs`, `codec/tests.rs` | Candidate, for the implementer to decide; software-packed units are not calibrated gyro measurements. |
| Is `0xA400FE` modeled/explicitly refused as a mutable extension **data-format** byte for applicable Classic variants rather than always a fixed read-only identity field? | `wii-gap-wiibrew-extension-data-format-selector`, `wii-c5-extension-identifiers` | `memory.rs`, `extensions.rs` | Candidate, for the implementer to decide; not universal for third-party units. |
| Are unsupported/invalid EEPROM addresses, final-byte bounds, high-address mirroring, and bad-write `0x21` vs `0x22` report paths clearly source-qualified? | `wii-gap-wiibrew-eeprom-address-mirroring`, `wii-gap-wiibrew-host-eeprom-visible-range`, `wii-gap-rnconrad-eeprom-exclusive-upper-bound`, `wii-gap-dolphin-out-of-range-write-ack`, `wii-gap-rnconrad-out-of-range-write-reply`, `wii-memory-size-hypothesis` | `memory.rs`, `codec.rs`, `acceptance/virtualgamepad.wii-remote.toml` | Candidate, for the implementer to decide; preserve caller-imported image extent rather than claim physical chip size. |
| Do acceleration LSBs appear only in reporting modes with accelerometer payload, and are 0x3e/0x3f interleaved Z-axis button bits treated distinctly? | `wii-gap-wiibrew-data-report-powerup-default`, `wii-c5-report-layouts`, `wii-kernel-report-modes` | `codec.rs`, `codec/tests.rs` | Candidate, for the implementer to decide; startup 0x30 is documented, not a periodic rate contract. |
| Does the synthetic vendor-page HID descriptor need a documented SDL HIDAPI compatibility decision relative to the unverified Game Pad top-level SDP candidate (with speaker report IDs)? | `wii-c5-synthetic-fixtures`, `wii-gap-rnconrad-candidate-sdp-descriptor-structure`, `wii-gap-retail-hid-descriptor-capture-unknown`, `wii-dolphin-hidapi-probe` | `realizations.rs`, `acceptance/virtualgamepad.wii-remote.toml` | Candidate, for the implementer to decide; W1 hidraw EACCES blocked definitive SDL/Dolphin acceptance, and retail descriptor remains unknown. |
| Should IR enable/ACK semantics and sensitivity/initialization alternatives be tested separately from physical full-blob fidelity? | `wii-gap-wiibrew-ir-initialization-uncertainty`, `wii-gap-wiibrew-ir-sensitivity-configuration`, `wii-gap-ir-full-mode-intensity-unknown`, `wii-gap-linux-ir-output-metadata-loss` | `codec.rs`, `memory.rs`, `acceptance/virtualgamepad.wii-remote.toml` | Candidate, for the implementer to decide; no promotion of 50-ms wiki workaround or full-intensity equivalence. |
| Does extension encryption remain explicitly refused unless verified, despite source-level enabled-path algorithms? | `wii-extension-encryption-gap`, `wii-gap-wiibrew-extension-encrypted-setup`, `wii-gap-dolphin-encrypted-extension-lazy-key`, `wii-gap-rnconrad-encryption-key-trigger` | `memory.rs`, `definition.rs`, `acceptance/virtualgamepad.wii-remote.toml` | Candidate, for the implementer to decide; preserve explicit unsupported path. |
| Do source-side additive/CRC calibration layouts justify only validation of *imported* images rather than inventing per-device values? | `wii-gap-dolphin-eeprom-accel-calibration-layout`, `wii-gap-dolphin-nunchuk-calibration-layout`, `wii-gap-wiibrew-calibration-redundancy-fallback`, `wii-gap-extension-calibration-checksum-unknown` | `memory.rs`, `controller.rs`, `acceptance/virtualgamepad.wii-remote.toml` | Candidate, for the implementer to decide; no fabricated factory calibration. |
| Should documented Classic Pro six-byte identity change the present **not-supported** manifest policy only after a reference-device discriminator check? | `wii-gap-wiibrew-classic-pro-identity`, `wii-gap-classic-pro-full-id-physical-unknown`, `wii-gap-classic-pro-host-classifier-tail` | `definition.rs`, `memory.rs`, `acceptance/virtualgamepad.wii-remote.toml` | Candidate, for the implementer to decide; not an authorization to implement or silently fall back to Classic. |
| Are LED permission failures, SDL/Dolphin hidraw permissions and uinput fuzz gaps tracked separately from codec semantics and physical protocol acceptance? | `wii-kernel-outputs-battery`, `wii-c5-evdev-consumer-shape`, `wii-gap-sdl-constant-input-inactivity-timeout` | `native.rs`, `realizations.rs`, `live_tests.rs`, `acceptance/virtualgamepad.wii-remote.toml` | Candidate, for the implementer to decide; W1 experiment IDs: `wii-w1-battery-rumble-led-host-run`, `wii-w1-sdl-host-run`, `wii-w1-dolphin-host-run`, `wii-w1-numeric-uinput-host-run`. |

The currently read acceptance manifest still describes several W1 live-axis and SDL/Dolphin cells as not-run/wip; the **newer W1 experiment records** report bounded probes and access blockers. This is an evidence/release-ledger reconciliation **candidate**, not grounds to change the manifest in this docs-only PR. Similarly `codec.rs` explicitly avoids advertising an invented firmware cadence; the host timeout claims do not change that constraint.

## 6. Remaining research **not** performed at this checkpoint

| Priority | Missing work and appropriate evidence type | Why not closed in cloud |
| --- | --- | --- |
| 1 | Obtain revision-pinned, license-aware WiiBrew **Nunchuk**, **Classic Controller** and **Balance Board** subpages, with independent hashes, section locators and delta claims. | Only the three pinned parent WiiBrew revisions above are included in the present corpus; no new source is asserted here. |
| 2 | Physical original / early non-TR Plus / RVL-CNT-01-TR, Classic Pro and third-party extension identity & encrypted setup captures; controlled address-edge tests. | Software sources cannot certify per-SKU physical behavior. |
| 3 | Retail SDP/HID report descriptor captured with model, revision, permissions and provenance; distinguish vendor/Game Pad collections and speaker IDs. | rnconrad candidate is historically unlicensed and unauthenticated; C5 descriptor is synthetic. |
| 4 | Wii Remote speaker report semantics, audio stream pacing and actual host/audio endpoint acceptance as a separately scoped feature. | C5 explicitly excludes speaker; candidate descriptor speaker IDs are not functional proof. |
| 5 | Calibrated IR brightness/size/bounds and sensor-mode initialization experiments; factory calibration fallback tests across accessories. | WiiBrew and Dolphin supply structure/approximations, not calibrated sensor transfer data. |
| 6 | SDL3 HIDAPI and Dolphin active consumer acceptance after an owner-approved hidraw policy/access resolution, plus full neutral/evdev numeric and lifecycle performance budgets. | W1 observed EACCES and deliberate environment restrictions; no permission modification authorized. |
| 7 | Wii host protocol cadence and state transition latency measured from a reference device; safe Bluetooth-radio pairing trials on permitted hardware. | Host polling/timeout values and virtual UHID are not physical timing or radio evidence. |

## 7. Handoff and decision gates

- **Corpus snapshot and review:** This checkpoint is docs-only. Do not add or modify claim, source, experiment, test, fixture or virtualgamepad files. Re-evaluate inventory after any subsequent corpus merge.
- **Source-to-implementation boundary:** Kernel, SDL, Dolphin, rnconrad, WiiBrew and W1 observations are distinct evidence classes; no controller semantics, descriptor authenticity or acceptance level follows from a string of matching software sources alone.
- **For the C5 implementer:** Treat section 5 solely as **candidate, for the implementer to decide**. Prefer independent consumer-oracle or model-labeled physical probes to adjudicate disagreements; keep unsupported operations refused until the project explicitly revisits them.
- **Cloud limits:** It is feasible to locate and pin more public sources and compare software behavior in cloud research. It is not feasible here to authenticate hardware calibration, descriptor provenance, encrypted timing, radio behavior, IR intensity or host permissions without the specified external evidence/host decision.
- **Release gate:** Publication guard, validator and Python unittests must pass on the **PR head**. No performance, whole-game/controller or physical acceptance is asserted by a docs-only green CI run.

_No upstream WiiBrew prose/tables, GPL source excerpts, raw captures, device serials or emulator arrays are included in this ledger._
