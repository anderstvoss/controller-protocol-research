# Changelog

All notable changes to the corpus are recorded here. The format follows
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Consumers pin
corpus commits by full SHA; schema changes that alter record shape bump the
affected schema's `schema_version`.

## Unreleased

- Add source-only Xbox 360 Wireless Receiver xpad v7.3-rc1 and SDL Linux lifecycle research: slot presence, evdev recreation, per-interface feedback and USB-level realization requirements; no host or hardware run.
- Pin an externally reported physical DualShock 4 v2 USB feature 0x12 read and its source code; advance only the scoped device-layout claim while retaining other DS4 gaps as unknown or conflicted (source-only review; no agent hardware test).

- Add six source-only Joy-Con (L) protocol and consumer claims for left-half identity, button bits, kernel evdev stick/IMU normalization and SDL3 sideways/vertical presentation; no hardware or host tests.

- Add published GameCube USB adapter descriptor and bInterval evidence, explicitly preserve conflicting EP0 sizes and HID-model limits, and distinguish WaveBird status consumer policies; source-only, no physical or host tests.

- Record the D9 virtual Steam Controller 2026 kernel evdev run from virtualgamepad #304 (mode-switch gate, per-control decoding and ABS ioctl attributes for UHID and reduced uinput) as a virtual-host experiment with consumer claims.

- Document source-only Puck receiver slot presence, attach/detach, SDL status 0x46/0x79, kernel native node recreation, per-slot output/lizard, and teardown against ADR-0022; physical and host validation remain unrun.

- Add pinned DualSense LED consumer mappings: mute pulse and player instant semantics become source-supported while conflicting brightness 0–2 versus 1–3 remains unresolved; no hardware or host tests.

- Record a reviewed physical Xbox Series Bluetooth descriptor, wired xpad
  input/reconnect fixtures, bounded xone headset duplex, and separate Linux
  UHID/xpadneo consumer observations. Add descriptor structural review
  without promoting universal firmware or motor-actuation claims.

- Extend Xbox Series Bluetooth consumer research with an xpadneo deep dive and correct the Share mapping to keyboard KEY_F12; document multi-node evdev topology, Guide modifier, udev hidraw restrictions, FF initialization, UHID request/replies and firmware/quirk limits.

- Record Xbox Series Bluetooth-bus UHID consumer gaps against pinned Linux hid-microsoft, xpadneo and existing SDL/BlueZ: descriptor/firmware applicability, driver binding, post-driver identity, Guide/Share/battery and independent-versus-derived trigger rumble; no device or virtual acceptance claimed.

- Record pinned out-of-tree xone as Xbox Series wired GIP and Xbox Wireless Adapter consumer evidence: source-scoped startup, ACK/chunking, evdev comparison, main-only Linux FF, conditional headset ALSA, and receiver client lifecycle; retain device-side unknowns and not-run physical tests.

- Pin Linux v7.3, SDL Triton, BlueZ HOGP/UHID/GATT/ATT transport framing and Valve public Linux rules for Steam Controller 2026 BLE; record source-only consumer claims, bounded codec/identity implications and an owner-only physical/scratch validation plan.

- Record pinned SDL, PipeWire/WirePlumber, udev, ALSA UCM and Wine/Proton consumer-audio association boundaries, preserving Steam and UHID-sidecar auto-discovery as unknown.

- Record the source-only Switch Pro NFC/MCU report-path scope gap, distinguishing a potential wireless-native feature from Nintendo-documented wired NFC restrictions; no hardware test or implementation change.

- Record the Linux hid-nintendo Switch Pro HOME-button light (subcommand 0x38) as a consumer gap, with a ranked Switch Pro gap brief.

- Record pinned SDL, PipeWire/WirePlumber, udev, ALSA UCM and Wine/Proton consumer-audio association boundaries, preserving Steam and UHID-sidecar auto-discovery as unknown.

- Record the stock Xbox Series xpad evdev shape with a synthetic capability fixture and pinned memoryless force-feedback evidence.

- Record the byte order SDL uses to decode the Switch Pro USB status address.

- Record the Wii MotionPlus cached-mode gate and open-time response races in local logging-only SDL 3.2.10 and 3.4.20 builds across Original and TR virtual host arms.

- Register the Switch 2 GameCube USB controller with source-only SDL/Linux protocol records and a not-run physical capture plan.

- Record owner-guided wired lizard desktop mappings, reconnect setup, normal SDL transitions and bounded pad scaling.

- Correct D9 #106 claim prose spacing; audit #105 without changing its statements, preserving all numeric tokens and
  evidence meaning. Missing boundaries were present in manually authored claim
  strings, not introduced by the packet reducer, JSON serialization or Markdown
  reflow. Audit the final serialized prose and applicability text as part of the
  contribution checklist so exporters cannot silently preserve this authoring
  mistake.

- Record supervised D9 MIDI-to-haptics and PCM playback through pinned upstream players, exact padded/short framing, configuration feedback, generated waveform correspondence and qualitative audibility limits.

- Clarify wired Steam Controller raw-HID versus physical HIDINPUT mouse/keyboard coexistence, separate Puck-path restoration latency from a stock watchdog measurement, and distinguish Steam discovery, managed activation and virtual output in the D9 matrix/checklist.

- Record labelled D9 wired native inputs, configuration-dependent pad/stick lockout, SDL-enabled motion, Steam Ping and separate brief rumble channels; retain selected non-identifying payloads and operator caveats.
- Research Steam Controller 2026 lizard firmware, kernel native/raw handoff, SDL HIDAPI arbitration and Steam virtual-device routing; add evidence-labeled visibility matrix and owner-only D9 observation checklist (source-only; no retail watchdog claim).

- Record D9 wired Steam Controller 2026 kernel/Steam feature exchanges, model attribute values and accepted setting writes; add opt-in model-field reduction while preserving serial/identifier withholding. Review follow-up corrects the three ED lengths, records only the safe one-byte value and serial character classes, and withholds all opaque tails.

- Survey GameCube adapter consumers, per-port uinput compatibility decisions and source-only libusb/udev grants for #258.

- Source-pin out-of-tree and user-space GameCube USB adapter bridges, Android USB manager and emulator backends; record source-only evdev and USB gaps.

- Document Joy-Con (R) source-only NFC/IR MCU state, NFC polling/read/write flow and IR register/image fragment policy; five scoped claims, no tag contents or host tests.

- Add Joy-Con single/pair consumer survey, SDL2 2.30.12 open and pair differences, kernel v5.16 history and compat/faithful identity decisions; five source-only claims, no host measurements.

- Research Joy-Con L/R Bluetooth-bus kernel and SDL3 open paths, USB Charging Grip probe, and steam-devices/joycond permissions for #258; nine source-only consumer claims, no host tests.

- Add Switch 1 Joy-Con source-only L/R device ledger (A1–A7), nine A1–A7 claims and an independently pinned joycontrol/nxbt emulator comparison (three G claims); no hardware or host tests.

- Pin the wired Steam Controller 2026 gamepad and sensor evdev capability shapes from Linux v7.3-rc1; these are consumer source claims, not observed virtual-device events.

- Add Switch 1 Joy-Con registry IDs (family, left, right) and a source-only survey of how hid-nintendo, joycond and SDL3 present single halves and pairs; four consumer claims, no device-protocol or host evidence.

- Register the GameCube USB adapter (WUP-028) and add a source-only survey: pinned SDL, Dolphin and Linux sources, corroborated report/init/rumble claims, single-lineage power and brake claims, and the finding that both native consumers need a USB-level device rather than hidraw. No physical or host evidence claimed.

- Record the D9 x86-64 Steam UHID host probe: separate SDL/Steam phases, corrected raw feature types and reply framing, verified node access and cleanup; preserve negative discovery and unknown delivery evidence.

- Add a source-only direct-wired Steam Controller 2026 physical-capture plan, bounded USBmon sessions and a fail-closed review-only transfer reducer with tests; no physical or virtual-host execution claimed.
- Extend the Steam capture plan for an owner-reported transient USB bootloader, paired bare-metal/VM pre-attach enumeration, passive host-command discrimination, version markers per session, and the already merged S3 physical descriptor evidence; no extra hardware observation claimed.

- Capture fresh direct-wired Steam Controller 2026 report descriptor and reduced USB configuration; record physical report declarations, the SDL-only 0x47 deployment mismatch and feature-2 declaration versus unknown wired exchange. No field semantics, consumer acceptance or output effects promoted.

- Add iczero Steam 2026 streaming, feedback, periodic-status and feature research leads plus two July-capture review follow-ups; preserve single-lineage/source-only evidence limits.

- Ingest sanitized July–August 2026 direct/Puck Steam Controller input campaigns, descriptor shapes and historical encoder as provenance-limited research leads; narrow physical gaps without inventing packet fixtures or physical validation.

- Record W9i independent fresh Tr default/external-style native Dolphin runs:
  consumer pre-map FE byte 00, bounded decoded gyro/stick, exact calibration
  and zero native post-map reinitialisation. Close the retained-mode sampling
  gap without physical, whole-controller or release promotion.

- Record W9h kernel-bound Plus regression, isolated Original Nunchuk copy-off
  calibration gate, Original Classic mode 07 and separate Plus default/external
  ID native Dolphin passes. Preserve decoded UI versus raw data, preliminary
  sampling limits, synthetic caller provenance and generic-binding release gate.

- CI: harden-runner uses `audit` instead of `block` on the macOS and Windows
  policy-check legs; its pre-step ignores the step-level `if` and block mode
  broke Windows DNS and revocation lookups (anderstvoss/virtualgamepad#260).
  Linux jobs stay in `block`.

- Document MotionPlus activation/deactivation 0x20 status transitions, Dolphin
  emulator versus documented device evidence, conditional F6 and Linux/SDL/
  Cemu/wiiuse/xwiimote re-probes. Rank creation-time compat, retain W9f
  reporting distinction and defer physical comparison to #52.
- CI: bump `step-security/harden-runner` to v2.22.3, which fixes block mode
  dropping allowed connections on GitHub-hosted Linux runners (the cause of
  stuck CodeQL jobs, anderstvoss/virtualgamepad#260). Egress policy stays `block`.

- Record W9g kernel-first gyro regressions and generic-bound native Dolphin
  MP+Nunchuk decoding with the activation re-attach compat edge. Isolate the
  edge-off reporting pause and F6-off calibration gate; keep raw frames separate
  from the UI oracle, and preserve #258 release and physical-fidelity limits.

- Record W9f counted stimulus: sustained commits, no post-map MP+Nunchuk
  data without a new report-mode request, and a passing MP-only gyro control.
  Separate pre-map frames and producer/consumer rate denominators; no model fix.
- Record Plus P1 kernel/xwiimote gyro, SDL 3.2.10 gyro limits and bound
  Dolphin MP-only UI observations, all scoped to Tr with default built-in ID.
  Keep absent kernel ID logging and physical/status limits explicit.

- Record the W9e owner-window generic-binding retry: MP and child calibration
  transport succeeds, MP+Nunchuk changing decoded motion remains unestablished,
  the MP-only gyro control passes, and loss of kernel Wii input/xwiimote access
  is observed. Preserve the earlier bind refusal and the release policy gate.

- Separate device and consumer evidence with an optional `evidence_role` claim marker, independent status columns and transport categories, and validator regression coverage. Historical consumer-only claims are being reclassified without changing their provenance or evidence strength.
- Record the W9e per-device hid-generic bind refusal, verified wiimote restoration
  and cleanup; pin version-matched stable HID source, preserving both Dolphin
  arms and the kernel-node trade-off as unmeasured.

- Extend Steam C6 wired research with six distinct-field synthetic haptic fixtures, offset-level assertions, SDL and Linux consumer timing assumptions, and kernel mid-session lizard/hidraw ownership claims; physical timing and replies remain unverified.

- Record four W9 compat controls: bound-kernel MP+Nunchuk on/off stops at F6,
  MP-only native Dolphin mapped gyro, and fresh kernel evdev axis delivery.
  Separate native from combined output, preserve missing-node/pilot limits,
  and do not promote unreached mirrors or calibration copies.

- Pin the W9 owner-selected fixed F7 value 0x02 as compat, paraphrasing the
  Dolphin enum, activation/update path and hardware-description comment. Keep
  challenge data at 0x50 refused and distinguish policy from physical readback.

- Diagnose W8 Cemu setup order: distinguish MP status/report-mode polling from
  MP+Nunchuk IR reconfiguration after successful replies. Preserve missing
  timestamp/internal-state limits; do not invent an ACK timeout or model fix.

- Add two clean W8 Cemu imported-resource comparisons after the browser holder
  closes. All 18 MP+Nunchuk calibration reads succeed, including 17 Nunchuk
  payload matches; decoded motion remains unobserved. Preserve coexistence arms
  and distinguish transport delivery from application interpretation.

- Add four post-merge W8 imported-block consumer arm sets: changing native
  Dolphin MP mapping indicators, the MP+Nunchuk F6 identity boundary, and Cemu
  coexistence limits. Keep clean no-holder and decoded-state unknowns explicit;
  retain the factory, physical, rate, audio and game acceptance gaps.

- Record seven bounded W8 caller-image Cemu and native Dolphin baseline arms.
  Separate successful base EEPROM reads, Nunchuk extension calibration error 7,
  native discovery and the speaker-mute ACK boundary from unobserved decoded
  motion. Retain raw artifacts privately and preserve the physical evidence gap.

- Fix W7 Cemu test imports when corpus discovery runs from a parent or unrelated working directory. Load the original reducer by a path relative to the test file and add an external-directory regression. Evidence records and runtime helpers are unchanged.

- Correct the incomplete W7 Cemu availability lookup with an installed ARM64 AppImage native-Wiimote run: four holder/profile comparisons and byte-capture repeats, native register attribution and calibration error 8 with the default empty caller EEPROM. Raw transport works; decoded gyro remains unobserved. Add reduced evidence, original trace reducer/guard and deterministic boundary tests; retain prior records unchanged.

- Record W7 independent Wii consumers: bounded libxwiimote gyro/normalization and evtest passes, RetroArch UHID/uinput generic controls with version-specific sensor limitations, ARM64 Cemu availability blocker and unresolved Dolphin direct-scanner checkpoint. Add original owned-device probes and reduced semantic evidence; preserve survey and physical claims.

- Research Wii Remote in-band speaker for post-alpha planning: pin Dolphin real-Wiimote forwarding/pacing, emulated speaker control/registers, signed PCM/Yamaha ADPCM decoder and rate, plus Linux hid-wiimote consumer exclusion. Cross-reference the three existing WiiBrew claims, record Dolphin/WiiBrew ADPCM volume-range discrepancy and maintain an explicitly not-run physical lab plan. No wii-* claims edited, no implementation, no physical promotion.

- Document source-scoped controller audio exclusions: xpad Xbox 360 no headset PCM path, Xbox Series xpad explicitly disabling GIP audio interface, Nintendo/SDL Switch Pro rumble distinct from audio, and Steam Controller 2026 audio endpoint unknown. No claims about physical absence and no existing SC2 gap record changes.

- Add pinned Sony audio consumer research: DualSense HID route/levels/mute/preamp fields and USB/BT framing, ALSA UCM routing, maintainer-documented physical UAC1 and headphone/grip observations, DS4 SDL/kernel distinctions, explicit unanswered Bluetooth/DS4 audio questions, and the kernel's USB jack-detect driven routing. No controller implementation or physical-status promotion.

- Add W5 unchanged-model MotionPlus gyro diagnosis: verified active packet decoding/pass-through and kernel ABS gyro delivery before fresh SDL holder/control comparisons. Retain zero SDL gyro and disconnects, actor/readback ambiguity and private-mode instrumentation limits. Add original probes, semantic evidence reducers and deterministic tests; no prior records or protocol model changes.

- Add pinned W4 SDL consumer-source no-reattach claims for3.2.10, latest3.4.18 and main; correct the MotionPlus-active downstream-change disconnect distinction. Record five60-second fixed-extension claim-held runs, selected controls/acceleration and LED intent; retain blocked zero gyro in both MotionPlus profiles. Add original probes and evidence-boundary tests without protocol or historical-record changes.

- Record W3 unchanged-model SDL extension reinitialization diagnosis with timestamped virtual reports and explicit blocked sustained HIDAPI acceptance; attribute the W2 N1 global count delta to unrelated USB input entries while preserving its historical blocked status. Add original reproducible tracing tools and deterministic evidence tests; no claim promotion.

- Record W2 authored interim Game Pad descriptor, default SDL enumeration and bounded initial Wii HIDAPI claim with later disconnect, plus clean-head UHID N1/N4 timing; preserve N1 global input-count discrepancy and all historical evidence.

- Add separate human-granted W1 LED, SDL and Dolphin virtual-host follow-ups: LED intent succeeds, hidraw access succeeds, Wii HIDAPI/backend acceptance remains unobserved. Historical blocked records and all wii-gap claims remain unchanged.

- Clear repository-local Git environment in both hook wrappers so nested cache/fixture commands cannot mutate the active worktree; cover inherited hook context deterministically.

- Record W1 bounded Wii numeric delivery on UHID/uinput, battery/rumble observations and explicit SDL HIDAPI/Dolphin/LED permission blocks, with original reproducible probes; no physical promotion or wii-gap claim changes.

- Add reproducible hash-checked Wii consumer-shape extraction and a six-node synthetic evdev golden; record source extension register tails and pass-through packing without promoting physical calibration.

- Add C5 source-only report layout/error/camera/extension locators and explicitly synthetic neutral packets and functional HID framing; preserve retail descriptor, calibration and physical-evidence limits.

- Migrate pinned Steam kernel/OpenPuck identity,interface,report and lizard findings; retain historical1142/current1304 distinction and unmeasured cadence.
- Add Wii L0 pinned consumer/emulator ledger, separate original/early-Plus/TR revision scopes, source-derived evdev shape and explicit memory/encryption gaps.
- Add Xbox Series L0 source-only xpad/SDL ledger and linked observed-evdev artifact, preserving USB-GIP/Bluetooth/device-evidence separation.
- Record500 measured DualSense/Xbox360 uinput lifecycle samples with virtual-host-only format/validation, sanitized paths/time and explicit missing consumer measurements; no physical promotion.

### Added

- Added a source-backed wired Steam Controller 2026 (C6) report field map, conditional feature/settings exchange claims, synthetic input/output/GET fixtures, source discrepancies and strict fixture regression checks; no physical acceptance claimed.


- Pinned Steam Controller 2026 P0 consumer evidence: kernel introduction and
  v7.3-rc1 selection, SDL Triton direct/receiver filters, and provisional UHID
  feasibility. Live P1 and all physical observations remain unmeasured.
- Source-reviewed Steam Controller 2026/Puck earlier-research gap audit, with revision-pinned independent Triton sources and unresolved gap claim records; no physical or live acceptance claimed.

- `records/controller/` registry (schema `controller.schema.json`). Every
  claim's `applicability.controller` must name a registered controller, and
  each record links its tracking issue.
- `tools/status.py`, which prints each controller's evidence category (no
  evidence, evidence in progress, source evidence, physical evidence) overall
  and per transport.

### Changed

- Claim `applicability.transport` is a fixed vocabulary: `usb`, `bluetooth`,
  `receiver`, `source_only`, `not_measured`. Existing free-text transports
  became `source_only` with the original detail moved into `scope`; existing
  controller names became registry IDs. Record shape is unchanged, so
  `schema_version` stays 1.

### Changed

- Visibility gates removed from CI now that the repository is public: the
  policy matrix, dependency review, CodeQL and Scorecard run on every change,
  and the history guard fails on any personal commit email.

- Published as `controller-protocol-research`, a fresh repository started
  from a flat copy of the private `controller-protocol-corpus` `main` as a
  single first commit, with no earlier history; the private repository keeps
  its name.

### Added

- `tools/history_guard.py` and a `Disclosure checks` CI job: publication
  checks over every reachable file version and commit identity, including
  pull-request refs.

- Public-release hardening from the reference blueprint: committed git hooks,
  pre-commit policy (gitleaks, file hygiene, local-path/IP/credential
  blockers, ruff), CodeQL for Python and Actions workflows, OpenSSF Scorecard,
  dependency review, harden-runner egress allowlists, hash-locked pip installs,
  `scripts/deep-scan.sh`, and issue and PR templates.
- Publication guard, split licensing (CC-BY-4.0 data, AGPL-3.0-only tooling),
  SECURITY.md and CONTRIBUTING.md.

- C5: source-only native evdev conversion/no-clamp evidence; bounded virtual-host binding/swap/rumble/battery-presence and four timing runs. LED permission failures and missing consumer/physical cells remain explicit.
