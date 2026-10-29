# Xbox 360 — compatibility versus faithful decisions and calibration provenance (I)

**Research parity, part 2: consumers and decisions** · source-only, no host or hardware tests. Derived from the **“What this settles for virtualgamepad”** table in `docs/ledgers/xbox360-l0.md`, then checked against virtualgamepad `8f60dcce577ab02bd8ed8b3426349729d417393c`. Code is an *implementation choice*, not device evidence. Each row cites merged part-1 records. `faithful` means a genuinely device-grounded answer; source-thin or missing physical records must be **unknown**. No implementation changes are directed in this PR.

| Consumer need (public source) | Observed compat choice in virtualgamepad (code line) | Faithful option / missing proof | Source claim IDs | Proposed tag |
| --- | --- | --- | --- | --- |
| **Neutral standard-HID UHID instead of XUSB** — xpad matches a vendor-specific physical USB interface and SDL HIDAPI XUSB eligibility by type/interface; evdev mapping is separate | `xbox360.rs` 620–639 uses unnumbered generic HID; no native XUSB packet framing | native USB XUSB device identity/20B input only with a true USB interface realization; UHID cannot be declared faithful XUSB | `x360-l0-consumer-xpad-id-usb-binding`; `x360-l0-consumer-sdl360-vs-generic-hid`; `x360-l0-consumer-sdl-backend-selection-unmeasured` | **compat** |
| **Legacy xpad BTN_X/Y on uinput** — Linux xpad uses 307/308 and evdev expects corresponding face positions | `xbox360.rs` 641–658 emits face key codes [304,305,307,308] | keep source-grounded mapping for Linux evdev; report physical button mapping still requires hardware | `x360-l0-consumer-xpad-face-legacy-codes` | **compat** |
| **Explicit nonconsecutive HID Button usage list** — Generic hid-input maps usage n → BTN_GAMEPAD+n-1; EXP-0016 found consecutive mapping wrong | `gr-controller-wire/src/lib.rs` 11–20 encodes usages 1,2,4,5,7,8,11,12,13,14,15 and padding | for generic-HID compatibility retain explicit list; native XUSB has different representation and cannot be substituted | `x360-l0-consumer-exp0016-hid-usage-correction`; `x360-vg-exp0016-uhid-individual-correction` | **compat** |
| **Wired 20B XUSB input and rumble vs UHID** — Independent host parser corroborates protoR2 secondary wired input and outputs | UHID sends generic 9-byte common HID frame, not 00 14 XUSB | No evidence of physical parity without owner-approved USB capture. Single protoR2 secondary wired report plus USB Host Shield corroboration is not retail physical validation | `x360-l0-device-xusb-wired20`; `x360-l0-device-xusb-output-ff-led`; `x360-l0-consumer-sdl360-wire-parser` | **unknown** |
| **FF and LED on evdev/uinput** — xpad has FF_RUMBLE and a separate xpadN LED class; generic uinput endpoint can implement FF handler, not xpad USB LEDs | virtualgamepad uinput FF surface may support EV_FF only; cannot infer xpadN LED output | No evidence uinput alone creates xpadN LED or a physical actuator | `x360-l0-consumer-xpad-ff-uinput`; `x360-l0-consumer-xpad-led-class`; `x360-l0-consumer-uhid-ff-led-unknown` | **unknown** |

## Calibration provenance and fallback

**Calibration:** xpad and SDL Xbox360 parse signed 16-bit sticks and 8-bit triggers; no known factory SPI/IMU calibration feature in pinned 360 wired source. UHID uses common scaled HID axes; distinguish application axis deadzones from device factory calibration. Caller supplied neutral/deadzone policy can be used; no invented factory calibration blobs.

**Policy recommendation:** maintain separate `compat` and `faithful` annotations per realization/consumer, with runtime caller-provided calibration only when provenance and device revision are explicit; a zero-filled/synthetic fallback is not evidence of actual physical calibration. Do not promote physical acceptance from a source-supported kernel parse or a virtual host run.

## Firmware, MAC, serial, revision and provenance

**Identity:** native wired 045e:028e, receiver 045e:0719 (distinct wireless protocol); generic-HID UHID with same PID does not force XUSB. SDL DB GUID has platform/version-sensitive mapping, and B reports corrected evdev usages but no native controller. No serial/firmware branch proven in this corpus.

## Part-2 proposed owner validation (all not run)

1. Capture the exact selected kernel driver, SDL backend, report/version and HID / evdev node identity without recording personal serials.
2. Compare current compatibility choice with source-known consumer acceptance (three independent neutral/one-control sessions), using only virtual paths unless separately authorized.
3. For any hardware-dependent row, request owner-controlled read-only reference capture and preserve unknown status until independent physical evidence exists.
4. Log failures, absent report IDs, recalibration fallback and multi-consumer open conflict separately; maintain lineage to the original source claim IDs.

**Cloud agent (realized-controller research parity)**
