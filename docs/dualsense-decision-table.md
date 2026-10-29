# DualSense — compatibility versus faithful decisions and calibration provenance (I)

**Research parity, part 2: consumers and decisions** · source-only, no host or hardware tests. Derived from the **“What this settles for virtualgamepad”** table in `docs/ledgers/dualsense-l0.md`, then checked against virtualgamepad `8f60dcce577ab02bd8ed8b3426349729d417393c`. Code is an *implementation choice*, not device evidence. Each row cites merged part-1 records. `faithful` means a genuinely device-grounded answer; source-thin or missing physical records must be **unknown**. No implementation changes are directed in this PR.

| Consumer need (public source) | Observed compat choice in virtualgamepad (code line) | Faithful option / missing proof | Source claim IDs | Proposed tag |
| --- | --- | --- | --- | --- |
| **0x20 feature firmware bytes 44–45** — SDL 535d80b branches on >=0x0224 for improved rumble; Linux uses separate 2.21 policy | wire feature reply returns 0x0224 from `gr-controller-wire/src/dualsense.rs` 51–60 | caller-provided retail version scoped to actual device, not a generic default | `ds-l0-consumer-firmware0224-branch`; `ds-l0-device-feature20-firmware-shape` | **compat** |
| **Synthetic feature 0x05 gyro/accel calibration** — Linux hid-playstation needs a parseable calibration reply; zero denominator causes fallback; SDL tolerates short reply | 32,000/−32,000 and 8,192/−8,192 canned endpoints in wire module 31–49 | caller-provided measured calibration and provenance; never invent factory values | `ds-l0-consumer-kernel-calibration-fallback`; `ds-l0-consumer-probe-feature-failure-tolerance`; `ds-l0-sdl-calibration-fallback` | **compat** |
| **Feature 0x03 capabilities** — SDL 48-byte marker gate primarily applies to third-party gamepads; Sony recognized path assumes capabilities | synthetic capabilities compatibility lead from OpenPuck; precise current path beyond descriptor not independently established | No evidence the exact bytes are necessary/physical; do not claim Sony requires it | `ds-l0-consumer-feature03-capabilities` | **unknown** |
| **Digital L2/R2 from analog** — SDL uses digital bit when analog is zero as fallback, while Linux exposes separate digital keys | USB report digital bits follow `trigger != 0` in `dualsense.rs` 954–956 | No evidence of physical DS threshold; expose explicit digital actuation or caller-tunable policy | `ds-l0-consumer-l2r2-digital-analog-policy` | **compat** |
| **UHID Steam gyro versus USB gadget** — Historical Steam showed gyro in dummy_hcd USB gadget but not UHID; association cause is inferred | UHID bus identity and sensor node arrangement picked by virtual topology | No evidence for an app-level remedy or a physical requirement; collect exact backend and sysfs sibling links | `ds-l0-dummy-hcd-steam-gyro-contrast`; `ds-l0-uhid-gyro-association-hypothesis` | **unknown** |
| **HHD feature and Steam motion policy** — HHD chooses compatible synthetic feature replies and motion schedule; emulated values cannot prove retail truth | Part 2 retags two `ds-l0-hhd-*` claims as consumer | No evidence emulator policy is exact retail device behavior | `ds-l0-hhd-feature-replies`; `ds-l0-hhd-steam-gyro-policy` | **compat** |
| **IMU axis reorder and battery default** — Linux/SDL consume signed calibrated motion and battery report; no retail user baseline in corpus | wire transform X,Z,-Y and battery defaults to externally powered in `dualsense.rs` 964–987 | caller MotionSample and battery with measured calibration, physical charging unknown | `ds-l0-device-imu-scaling-formulas`; `ds-l0-device-usb01-full-fields` | **compat** |

## Calibration provenance and fallback

**Calibration:** kernel GET 0x05 mandatory at probe, read failure aborts; reported zero denominator substitutes generic bias/scale (hid-playstation.c 1023–1147). SDL's 0x05 short reply uses its own fallback (SDL_hidapi_ps5.c 555–666). Never manufacture a device-specific physical 0x05 for the `faithful` path: accept a caller-supplied, scoped, safely redacted calibration blob only with origin metadata; absence is compatibility-only or explicit refusal.

**Policy recommendation:** maintain separate `compat` and `faithful` annotations per realization/consumer, with runtime caller-provided calibration only when provenance and device revision are explicit; a zero-filled/synthetic fallback is not evidence of actual physical calibration. Do not promote physical acceptance from a source-supported kernel parse or a virtual host run.

## Firmware, MAC, serial, revision and provenance

**Identity:** VID 054c PID 0ce6 remains base; Edge 0df2 separate (`dsedge-l0-consumer-identity-separation`). Firmware feature 0x20 bytes 44–45 branches SDL; pairing/MAC 0x09 read can seed identity; USB report descriptor and serial/`uniq` must not publish a real identifier. Virtual version and Linux bus choice are compatibility identity. No real DS serial/MAC was recorded.

## Part-2 proposed owner validation (all not run)

1. Capture the exact selected kernel driver, SDL backend, report/version and HID / evdev node identity without recording personal serials.
2. Compare current compatibility choice with source-known consumer acceptance (three independent neutral/one-control sessions), using only virtual paths unless separately authorized.
3. For any hardware-dependent row, request owner-controlled read-only reference capture and preserve unknown status until independent physical evidence exists.
4. Log failures, absent report IDs, recalibration fallback and multi-consumer open conflict separately; maintain lineage to the original source claim IDs.

**Cloud agent (realized-controller research parity)**
