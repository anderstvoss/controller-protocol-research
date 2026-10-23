# Coordinator handoff — W5 Wii gyro diagnosis, SDL/kernel/Dolphin boundaries

**Audience:** coordinating agent managing Wii Remote W5; this is a *research handoff*, not an instruction to write protocol code or change host configuration.  
**Research repo:** `anderstvoss/controller-protocol-research`; parent source analysis [wii-gyro-investigation.md](wii-gyro-investigation.md); new follow-up [wii-gyro-consumer-paths-and-variants.md](wii-gyro-consumer-paths-and-variants.md).  
**Virtualgamepad:** `anderstvoss/virtualgamepad` is **read-only for this cloud research lane**. W5's authoritative [issue #158 coordinator instruction](https://github.com/anderstvoss/virtualgamepad/issues/158#issuecomment-6373947878) already exists; **do not replace, overwrite or broaden it**. Anders controls merging code and research PRs.  
**Evidence status:** source-backed consumer findings only; W4 zero readings are an observation, W5 root cause remains **unproven**. Source pins SDL 3.2.10 `877399b`, SDL 3.4.18 `829a65d`, Linux v6.12 and mainline `734bef5`, Dolphin `e1d35f666cc35f6ead55d32ea2679df44d04da72`.

## 1. Prior results, current question

W4 maintained a fixed-before-open SDL 3.2.10 HIDAPI Wii joystick for **60 seconds** in five topologies: no extension, Nunchuk, Classic01, external/available MotionPlus, and MotionPlus+Nunchuk. Buttons and applicable axes worked; acceleration was observed except where SDL did not advertise it. Both MP topologies **registered and enabled** gyro, but observed polled gyro min=max=0 despite driven 14-bit vector changes `9000/7000/8500` ↔ `7000/9000/7800`. These data **do not** prove a virtualgamepad packing bug, native kernel gyro delivery or physical fidelity. W4 did not exercise optional active hotplug.

**Question:** Which of (a) virtual packet encoding, (b) kernel `MP_USED` activation/mapping, (c) SDL's unconditional A400F0 reset plus Linux no-op reactivation, or (d) consumer-specific report dispatch/sampling causes all-zero SDL gyro? Separate each with an oracle. Do not equate sensor enumeration with actual events.

## 2. Driver and consumer model — communicate this accurately

- **SDL Wii HIDAPI** consumes *native reports through hidraw*. It does **not** read the MotionPlus evdev node to produce its `SDL_SENSOR_GYRO`. On Linux, its activation function leaves A600FE and `m_ucMotionPlusMode` untouched; another component (typically kernel `hid-wiimote`) must maintain the mapped sensor state.
- **Kernel hid-wiimote** detects the MP node but maps into extension registers only after **someone opens** the MP evdev input device (`MP_USED`). A separate SDL hidraw FD does not itself cause this. The kernel exposes its own gyro through evdev, a valuable independent oracle.
- **SDL initialization conflict:** SDL `OpenJoystick` always calls `InitializeExtension` (A400F0 reset) before `GetMotionPlusState`; on Linux it does not immediately restore MotionPlus. Even holding evdev first can fail because mapping is cleared before SDL caches its mode. Periodic presence polling does not repair an already-present mode NONE.
- **Dolphin Real Wii Remote / emulated Bluetooth console:** forwards native reports via real BT L2CAP or a compatible HIDAPI backend; it is not automatically a host-calibrated gyro reader. Dolphin's **ControllerInterface** mode is different: it actively initializes MotionPlus and reads calibration, so Dolphin CI success/failure tests a different application state machine.
- **Dolphin USB Bluetooth passthrough** needs actual adapter topology. A UHID device with `BUS_BLUETOOTH` does not become an RF Bluetooth device. Dolphin HIDAPI warns that `hid-wiimote` can fight its direct register management and prefers `hid-generic`; **do not unbind or reconfigure a host merely based on this finding**.
- **No dummy_hcd requirement follows from Wii gyro.** HHD's DualSense UHID path and project UHID sensor acceptance refute a blanket limitation. SDL Wii gyro's activation state is a protocol/consumer question, distinct from Sony feature reports and USB topology.

## 3. Four hardware presentations: required distinctions

| Case | Consumer name/class | Gyro provenance | Implication for W5 |
| --- | --- | --- | --- |
| Base original Wii Remote | `RVL-CNT-01`, kernel Gen10 | No gyro without accessory | Negative control; accel is not gyro |
| Base + **external** MotionPlus | Same Gen10 remote identity | Physically detachable accessory | External MP detection/polling, MP_USED and mode 04/05/07; W4 test family |
| **Early integrated** Wii Remote Plus | May still appear `RVL-CNT-01` / Gen10 | Built-in but not guaranteed `-TR` identity | Do not infer absence from older name; retain early-revision uncertainty; may use Gen10 polling path |
| Later integrated `RVL-CNT-01-TR` | Gen20 and built-in MP kernel flag | Built-in | No external polling but **still requires mapping**; do not treat identity as gyro proof |

Do not silently merge early integrated and later TR identities, physical calibration, status sequences or attach behavior. Preserve existing `wii-early-plus-revision-gap` as unknown. The initial W5 lab should explicitly identify which *virtual personality* was used; its current observed gyro failures are in MotionPlus topologies, not necessarily every retail revision.

## 4. Execution sequence — defer to existing W5 brief

**H3, encoder first:** Generate and independently decode the 6-byte MP data as emitted by the virtual implementation; record proper byte-5 bit-1 gyro marker, clear bit-0 invalid flag, three 14-bit values, slow/fast flags, report mode `0x35`, and interleaving with Nunchuk instead of concatenation. Compare WiiBrew motionplus records and a pure Rust test. If H3 fails, **report virtualgamepad bug on #158 before editing code**; no silent workaround.

**Kernel evdev gyro independently:** Have an authorized local process open and hold exactly the `Nintendo Wii Remote Motion Plus` input node of the owned virtual HID. Correlate `MP_USED`, actual A600FE mode 04 (MP alone) or 05 (Nunchuk), and *varying evdev ABS_RX/RY/RZ*. A created node without changing events is not sufficient.

**H1/H4 combined:** For a fresh SDL process on each arm, compare **MP evdev holder open first** against **no holder**. Record every A400F0 and A600FE write/read, A400FA/A600FA identities, SDL initial open and `GetMotionPlusState` mode, decoded report type/length, sensor **event count**, extrema, removal/reconnect and cleanup. Attribute actors when possible. Check the decisive sequence: kernel MP mapped → SDL A400F0 reset → late kernel remap → SDL cached NONE → all-zero gyro. If observed and H3/kernel gyro pass, classify as **SDL-on-Linux consumer state limitation under the tested host tuple**, *not* proof that all physical Wii hardware or all SDL versions fail.

**H2 optional:** Repeat identical inputs on a scoped SDL 3.4.18 binary (no system-wide install), only if local and cheap. At the reviewed pins the relevant Wii source branches remain the same; do not assume a version bump solves it.

**Dolphin optional, separately authorized:** Do not perform a Dolphin run as part of W5 automatically. If Anders requests it, choose explicit test axis: (1) Dolphin ControllerInterface real-Wiimote HIDAPI on the same owned virtual HID to test *Dolphin-driven* register writes and calibration-gated decoding; (2) Dolphin Real Wii Remote path to test report pass-through/game interaction; (3) actual Bluetooth adapter passthrough (not possible through UHID alone). Capture driver binding and expected GET/WRITE register transactions. A Dolphin emulator-generated MotionPlus packet is only software cross-check, not an independent physical oracle.

## 5. Verdict matrix for coordinator

| Source/host observation | Supported disposition |
| --- | --- |
| H3 encoded gyro bytes wrong while active | Local virtual codec/model defect lead; report on #158, fix only after coordination and add regression |
| H3 valid, kernel MP evdev shows changing gyro, SDL zero | SDL mode/activation/packet selection/consumer path lead; isolate SDL cached mode and reset |
| MP evdev node present but unopened, no A600FE mapping | Kernel not asked to consume gyro yet; test holder; **not** an encoder verdict |
| Holder maps MP then SDL reset deactivates it, no timely restore | Supports H4 ordering cause; no guaranteed fix from holder alone |
| SDL cached active mode and has valid gyro-marked input, but SDL events absent | Instrument SDL dispatch/sensor enable, report length/format and consumer samples; potentially SDL issue |
| SDL valid nonzero readings for 60s, kernel evdev also changes | Bounded gyro success under exact runtime tuple; still no physical equivalence |
| Dolphin CI can decode with calibration while SDL fails | Consumer divergence; *not* confirmation SDL needs a Dolphin-style calibration feature report |
| External MP vs early integrated/TR differ | Preserve model-specific evidence and unknowns; do not collapse hardware personalities |

## 6. Reporting, file ownership and stop conditions

- W5's local implementing agent owns runtime/host work, grant handling and **`wii-w5-*` experiments and fixtures**. This cloud addendum owns only new **`wii-gap-dolphin-*` consumer claims**, pinned source records and docs. No edits to `wii-c5-*`, prior `wii-w*-*`, original DualSense records or virtualgamepad.
- W5 should deliver its existing one research + one code PR, record host tuple, command, sample counts/extrema, packet identities sanitized, no raw logs/paths publicly, checks, and explicit limitations. Its coordinating agent should avoid claiming an overall gyro pass from mere registration or enabling.
- Anders merges. No agent merge, driver unbind, root grants, persistent host rules, host RF pairing, unrequested Steam or speaker work, or speculative protocol-model changes. Keep cross-consumer conflicts and early Plus uncertainty open until evidence resolves them.
- Suggested status line for coordinator: *“W4 zero SDL gyro remains blocked; source analysis identifies kernel MP_USED activation and SDL's unconditional open reset as distinct tested hypotheses. Dolphin's direct ControllerInterface actively configures and calibrates MotionPlus, unlike SDL Wii HIDAPI Linux. W5 actor-attributed kernel/SDL host runs are required for causality.”*

Source map: [SDL detailed analysis](wii-gyro-investigation.md); [consumer comparison and hardware cases](wii-gyro-consumer-paths-and-variants.md); [W4 results](wii-w4-sdl-fixed-extension.md); [W5 issue instructions](https://github.com/anderstvoss/virtualgamepad/issues/158#issuecomment-6373947878); new Dolphin source/claim records described in this addendum.
