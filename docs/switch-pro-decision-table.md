# Switch Pro — compatibility versus faithful decisions and calibration provenance (I)

**Research parity, part 2: consumers and decisions** · source-only, no host or hardware tests. Derived from the **“What this settles for virtualgamepad”** table in `docs/ledgers/switch-pro-l0.md`, then checked against virtualgamepad `8f60dcce577ab02bd8ed8b3426349729d417393c`. Code is an *implementation choice*, not device evidence. Each row cites merged part-1 records. `faithful` means a genuinely device-grounded answer; source-thin or missing physical records must be **unknown**. No implementation changes are directed in this PR.

| Consumer need (public source) | Observed compat choice in virtualgamepad (code line) | Faithful option / missing proof | Source claim IDs | Proposed tag |
| --- | --- | --- | --- | --- |
| **Y-axis inversion compensation** — Linux hid-nintendo publishes ABS_Y/RY after sign inversion; SDL Switch path has separate mapping | `switch_pro.rs` 678–690 negates wire Y at frame packing boundary | Measured per-device raw stick orientation, host cross-check; converter may remain but not a physical statement | `swpro-l0-consumer-kernel-open-order`; `swpro-l0-consumer-sdl-open-order` | **compat** |
| **Generic ACK for unmodeled 0x30/0x40/0x48** — Linux waits for 0x40/0x03/0x48 ACK; SDL 0x48 on open and 0x40 on sensor enable | `switch_pro.rs` 763–801 responds generic 0x80 ACK for otherwise unknown subcommands | Device-verified ACK bytes and state transitions; No evidence generic reply is accepted universally | `swpro-l0-consumer-imu-rumble-ack-gates`; `swpro-l0-device-subcmd21-ack` | **compat** |
| **Fixed virtual device MAC** — SDL derives serial from 0x02 MAC, GUID includes controller type not MAC; Linux derives uniq | `switch_pro.rs` 722–728 and 763–769 send a synthetic six-byte a fixed, locally administered synthetic six-byte address value | per-instance stable/random locally administered identity with provenance and no public real MAC; default fixed identity risks collisions | `swpro-l0-consumer-sdl-mac-serial-guid`; `swpro-l0-consumer-linux-mac-uniq` | **compat** |
| **Battery/report byte 0x80** — Host consumes battery nibble and USB charging bits from 0x30 input | `switch_pro.rs` 654–658 sets 0x80 constant | physical battery/charger status remains unknown; use caller BatteryState or represent unknown | `swpro-l0-device-30-full-report-layout` | **compat** |
| **Always three IMU samples / 0x40 enable** — Kernel enable 0x40 ACK gates IMU; SDL enables sensors on request | `switch_pro.rs` 691–710 repeats three motion samples in each 0x30, with mode ACK handled separately | true sample cadence and enabled/disabled state machine per actual firmware; no retail gyro capture | `swpro-l0-consumer-imu-rumble-ack-gates`; `swpro-l0-device-30-full-report-layout` | **compat** |
| **Nominal 250 Hz send interval** — Community sources disagree on USB 60/120/250 Hz and OpenPuck frame timing; source_conflicted | Encoder worker uses 250 Hz nominal report period (code-level timing contract to verify) | No evidence of physical universal 250Hz; preserve conflict and measure timestamp delta | `swpro-l0-device-report-period-conflict` | **unknown** |
| **SPI factory calibration/colour** — Linux and SDL read 0x6020 IMU, 0x603d sticks; colours in 0x6050..0x605b | `switch_pro.rs` 735–750 returns OpenPuck neutral calibration for IMU/sticks; colour addresses FF, with 'colours not available' in 0x02 info | caller import SPI data from physical device and provenance, not arbitrary colours or fake magic; missing values must use per-consumer fallback | `swpro-l0-consumer-kernel-calibration-fallback`; `swpro-l0-consumer-sdl-calibration-fallback`; `swpro-l0-consumer-colour-spi-no-evidence` | **compat** |
| **Steam neutral offset symptom** — Unversioned historical Steam/Eden report; no backend trace or physical comparison | Synthetic SPI and axis center accommodation is a candidate, not a proven root cause | No evidence which calibration/GUID path drives reported offset | `swpro-l0-consumer-steam-neutral-causation-unknown`; `swpro-vg-exp0016-eden-steam-neutral` | **unknown** |

## Calibration provenance and fallback

**Calibration:** factory IMU 0x6020 and sticks 0x603d (kernel, SDL); user calibration markers at 0x8010 and fallback differ by consumer. The OpenPuck values in virtualgamepad are *compatibility constants*, not device observations. A faithful API accepts caller-supplied SPI EEPROM/calibration with provenance; no synthetic 'factory' values when claiming faithful. Colours all FF: Linux/SDL no evidenced rejection; physical behaviour No evidence.

**Policy recommendation:** maintain separate `compat` and `faithful` annotations per realization/consumer, with runtime caller-provided calibration only when provenance and device revision are explicit; a zero-filled/synthetic fallback is not evidence of actual physical calibration. Do not promote physical acceptance from a source-supported kernel parse or a virtual host run.

## Firmware, MAC, serial, revision and provenance

**Identity:** VID/PID 057e:2009. SDL constructs serial from device-info 0x02 MAC, type influences GUID; Linux uses MAC-derived `uniq`. Use per-instance identity policy and don't expose real MACs in public; fixed a fixed, locally administered synthetic six-byte address is a virtual placeholder. Battery nibble 0x80, SPI 0x6050..0x605b colours and 250Hz timing are compatibility/unproven.

## Part-2 proposed owner validation (all not run)

1. Capture the exact selected kernel driver, SDL backend, report/version and HID / evdev node identity without recording personal serials.
2. Compare current compatibility choice with source-known consumer acceptance (three independent neutral/one-control sessions), using only virtual paths unless separately authorized.
3. For any hardware-dependent row, request owner-controlled read-only reference capture and preserve unknown status until independent physical evidence exists.
4. Log failures, absent report IDs, recalibration fallback and multi-consumer open conflict separately; maintain lineage to the original source claim IDs.

**Cloud agent (realized-controller research parity)**
