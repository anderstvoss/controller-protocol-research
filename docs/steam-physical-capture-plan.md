# Prep for physical capture and step 16 — Steam Controller 2026 direct USB

**Scope:** retail direct wired `28de:1302` only. **Status:** source-only capture design; no equipment, Linux execution, virtualgamepad build, or measured outcome. The Puck `1304`, internal receiver `1305`, and Bluetooth `1303` require **separate plans later**. Do not mark virtualgamepad #176 steps, modify its build, or infer physical parity from a consumer parser. Owner-controlled observations only; Anders chooses when to run. This prepares #159 and the distinct step-16 decisions in `docs/steam-consumer-contention.md` and [brief 03](https://github.com/anderstvoss/virtualgamepad/blob/main/docs/plans/pre-controller-buildout/03-steam-uhid-consumer-probe.md). It does *not* replace the local agent's UHID/virtual-host matrix.

## Grounding and definitions

- [Operator's July/August 2026 consolidation](https://github.com/anderstvoss/virtualgamepad/blob/7cb46009c8a4d570be2953bef971a17f3f2ca39f/docs/STEAM_CONTROLLER_2026_CAPTURE_NOTES.md) ``1,3,5,8,10,14`, source `sc2-src-capture-notes-2026` (research PR #79, merged as `bae4383`). It already reports `1302`, 372-byte HID report descriptor, declared report IDs/lengths, direct `0x42` length 54 and occasional `0x40`; Puck fallback coexistence and `0x79` values are **not** new capture targets. Raw historical files were withheld and not revalidated. Descriptor **bytes** and USB topology were not imported.
- Linux source pin `steam-ibex-linux-driver` v7.3-rc1, lines 262–391, 618–743, 873–976, 1372–1515, 1602–1695, 2325–2617, 2751–2770. Kernel behavior is **host-consumer code**, not evidence of physical-device transactions. Linux 7.3+ is a prerequisite for the intended bound run; verify actual ID/binding rather than assume version implies a bound driver.
- SDL pins `steam-triton-sdl-driver` and `steam-c6-sdl-structs`; test exactly SDL3 3.4.10 or later (`steam-client-sdl3-triton-rumble-release`) and record the runtime dynamically linked by `testcontroller`. The source-pinned 4032 microsecond sensor update is SDL's assumption, *not* physically measured (`steam-c6-sdl-sensor-4032us`).
- The iczero source `sc2-src-dissector` (lines 46–77, 142–212, 739–795, 812–835), `sc2-src-haptics` (lines 4–15, 60–92, 127–166) and `sc2` share one reverse-engineering lineage; not independent physical evidence. `0x44` ACK and `0x86..0x89` streaming roles remain hypotheses.
- **Wire length** always includes the report ID; body length does not. A USB control-URB setup's `bRequest`, HID report ID, inner feature command and output report ID are four distinct fields. Report counts per ten-second window are *inferred average frequencies* only. Record request *and* completed response URBs with monotonic relative times; keep URB pairing identifiers private.

## A. Outstanding wired claim/document inventory

The table enumerates direct-`1302` unknown/inferred/conflicted claim rows plus No-evidence cells in the research gaps, C6 decision table, contention 4×2 matrix, permissions/open-path and consumer survey. IDs that describe a source-supported decoder still appear where a **device-side field is unmeasured**. `S0`=USB topology; `S1`=bound kernel; `S2`=SDL HIDAPI and differential controls; `S3`=optional Steam. `Different setup` explicitly means **not settled by one 7.3+ bound wired session**. No listed action by itself closes a claim: compare outcome and create evidence only after review.

| Record/cell | Remaining question / source expectation | Capture gate |
| --- | --- | --- |
| `sc2-gap-direct-usb-descriptors`; `steam-ibex-kernel-uhid-selection` | 372 bytes is known historically; actual HID bytes, one interface, endpoint types, bcdDevice, collection usage versus kernel collection filter | S0; save exact bytes, counts and topology (not private strings) |
| `steam-triton-sdl-uhid-selection`; brief 03 P0/P1 | Source predicts PID-based SDL direct match and kernel collection-based match; physical USB topology is *not* a UHID acceptance result | S0/S2 for real hardware; **different setup** for UHID virtual trial |
| `sc2-gap-report-roles`; `steam-c6-disagreement-47-kernel`/`-sdl`; `steam-c6-input-45`/`-47` | Does wired device ever emit `0x45` or SDL-only `0x47` by consumer/mode, versus historical `0x42`? Kernel has no `0x47` dispatcher | S1/S2 time-bounded IDs, lengths, relative timing |
| `sc2-gap-input-layout`; `steam-c6-input-42`; `steam-c6-input-buttons`; `sc2-july-historical-encoder-42-*` | Native bit/axis/control correspondence, Menu/View swap, signedness and final eight bytes (quaternion per kernel vs opaque in historical encoder) | S2 isolated one-control-per-window byte diffs; independent neutral controls |
| `sc2-gap-touch-pressure`; `steam-c6-input-scaling` | Sticks, triggers, pad X/Y, pressure, capacitive grip, touch-versus-click thresholds, axes/units | S2 center/extrema/diagonal and independent touch/press/pressure/stroke windows |
| `sc2-gap-imu-calibration`; `steam-c6-feature-imu` | Actual accel/gyro orientation, scale, sensor setting `0x30`, timestamp increments, optional calibration | S1 sensor open/close, S2 stationary and single-axis rotations; **different setup** for calibrated motion standard |
| `sc2-gap-synthetic-cadence`; `steam-c6-sdl-sensor-4032us` | Actual wired input and sensor interarrival distribution; SDL comments 4032 µs; July Puck ~266 reports/s cannot answer wired timing | S1/S2 monotonic report timestamps and capture loss counters |
| `sc2-gap-battery-cadence`; `steam-c6-battery-43` | Physical `0x43` fields, cadence and charge transitions (historical numbers are **Puck-only**) | S2 bounded idle and battery status; **different setup** for charger state sequence |
| `sc2-gap-feature-roundtrip`; `steam-c6-feature-kernel-exchange`/`-registration` | Real `0xae`, `0x83` replies; valid lengths, tag names, return/failure behavior, no serial disclosure | S1 power-on GET/SET bidirectional; **different setup** for adversarial malformed-reply injection |
| `sc2-gap-firmware-serial`; `steam-parity-kernel-open-feature-gates` | Attribute IDs product/revision/firmware, `0x0b` interval and returned formats; sensitive serial/unique ID values | S1 safe tags/lengths/hashed identities only; do not release value |
| `steam-c6-no-wired-feature2` | Does direct registration ever invoke feature report 2? Kernel/SDL inspected direct paths do not | S1/S2 absence bounded by full startup + close; cannot assert universal absence |
| `steam-c6-disagreement-open-kernel`/`-sdl`; `steam-parity-sdl-open-feature-gates` | Kernel serial→attributes→lizard vs SDL no kernel-style GET; source-specific ordering and failure handling | S1 vs S2 separate newly plugged runs, retain mode and URB completions |
| `steam-c6-feature-kernel-lizard`; `steam-c6-feature-sdl-lizard`; `sc2-gap-lizard-handshake` | Kernel `0x85/0x8e` vs `0x81/0x87`, SDL `0x87` setting 9; physical transition and native `0x42` persistence | S1/S2 with short neutral windows before/after settings, without assuming exclusive fallback |
| `sc2-gap-physical-lizard-watchdog`; `steam-parity-sdl-kernel-lizard-contention` | Real watchdog refresh/expiry timing, mouse/keyboard coexistence and final setting after close | S2 delayed neutral windows at 0,3,7,10 s after close; S3 if Steam modifies it; do not infer 7 s from prompt |
| `steam-c6-kernel-menu-hold-450ms`; `steam-c6-kernel-ibex-evdev-open-close` | Kernel hold threshold nominal 450 ms and whether IBEX evdev open alone changes lizard policy | S1 manual below/above threshold and monitor GET/SET + evdev; no guaranteed exact human timing |
| `steam-c6-kernel-client-raw-forward`; `steam-parity-sdl-kernel-lizard-contention` | Opening raw client can suppress kernel synthetic evdev asynchronously; physical observed open order/node lifetime unknown | S1 evdev-only, S2 SDL raw-open/close with node presence snapshots; S3 for two consumers |
| `sc2-gap-host-output-capture`; `steam-c6-output-80-81`; `-82-85` | Bidirectional haptic commands, which actuator actually moves; historic Puck Ping lacks causative traffic | S1 supported safe `fftest` effect if advertised; S2 SDL low-output rumble; S3 optional Ping |
| `steam-c6-disagreement-gain-kernel`/`-sdl` | Signed `int8` vs unsigned `u8` gain semantics; consumer writes and actual effect | S1/S2 record bytes and response, **different setup** for deliberately exercising high-bit gain; no arbitrary raw writes |
| `steam-c6-kernel-rumble-coalesce-20hz`; `steam-c6-sdl-rumble-resend-40ms` | Host scheduling/coalescing and physical safety timeout | S1/S2 timestamp repeated low-intensity output and cessation after close; no guaranteed period from source |
| `sc2-gap-haptic-ack`; `steam-c6-no-haptic-ack` | Is `0x44` ever correlated with `0x80..0x89`, and does it encode ACK/flow? | S1/S2 correlate output to subsequent `0x44` by time/direction; no injected invalid streams |
| `sc2-gap-haptic-output`; `sc2-gap-audio` | Streaming `0x86..0x89` and per-side motors; effect-6 modes are iczero research leads | S3 passive observation only; **different setup** for consented streaming stress/actuator calibration |
| `sc2-gap-leds` | Physical LED/player feedback and command attribution | S3 user-visible behavior; **different setup** for controlled LED feature API and output isolation |
| `audio-steam-controller-2026-endpoint-unresolved` | USB audio endpoints, speaker/audio vs haptic effects | S0 endpoint/interface inventory; **different setup** for audio signal/codec measurement |
| `steam-parity-udev-valve-raw-grants`; `-uinput-wakeup`; `steam-permissions-open-path.md` | Exact ordinary-user ACL/seat/sandbox grants and side effects | S0/S1 read-only access checks; **different setup** for multi-seat, denial or sandbox matrix (#258) |
| `steam-parity-unbound-legacy-kernel`; contention **unbound** column (evdev, SDL, Steam, SDL+Steam) | Generic binding and prior-kernel acceptance | **Different setup**: operator-authorized boot of another kernel or reversible per-device unbind/rebind; never in default run |
| Contention **bound** column: evdev only, SDL only, Steam only, SDL→Steam and Steam→SDL | Client selection, evdev disappearance, lizard arbitration and order | S1/S2/S3; both open orders only with separate explicit operator consent |
| `steam-parity-sdl2-triton-native-unknown`; `steam-parity-sdl3-versions` | 3.4.0 vs 3.4.10 vs SDL2 code path/rumble differences | S2 uses **3.4.10+**; **different setup** for parallel pinned SDL2/3.4.0 binaries |
| `steam-parity-engine-sdl-linux-paths`; survey Godot/Unity cells | Actual bundled SDL, specialized capabilities and host support | **Different setup**: pinned applications/engine builds |
| Survey InputPlumber/HHD cells | Exact 1302 support, permissions, feedback and native decode | **Different setup**: pinned installed packages and owner-selected consumer |
| `sc2-gap-compound-realization`; `steam-ibex-uhid-provisional` | Virtual native+keyboard companion and UHID acceptance | **Different setup**: local buildout/brief 03; physical baseline does not decide software realization |
| `sc2-gap-ble-identity`; `sc2-gap-puck-slots`; `sc2-gap-puck-usb-descriptors`; `sc2-gap-wireless-events`; `sc2-cadence`; `sc2-gap-physical-report-mix` | Receiver, four slots, BLE transport or Puck report timing | **Separate plan later**; not wired 1302 |
| `sc2-gap-switch-rumble-fidelity`; OpenPuck historical compatibility claims | Other device emulation and receiver/HD-rumble | **Separate plan later**; not wired 1302 |

## B. Four capture sessions: commands, predictions, stopping and restoration

### General safety gate (all sessions)

- Use only a **personally authorized retail controller**, ordinary user session, and consented programs. Steam absent for S0–S2; S3 requires Anders manually starting Steam. Keep network/file sharing disabled for private traces. No shell commands below need `sudo` except *loading/accessing usbmon* in S1–S3.
- Check `uname -r`; do not infer driver identity from version. Record the selected controller's sysfs binding, HID collections, bus number and USB device address locally (do **not** publish them). Do **not** run driver unbind/rebind, global module parameters, changing udev policies, firmware flashing, custom feature writes, arbitrary high-gain haptics, or USB reset.
- For every action record a neutral baseline, start/end marker in the local operator log, success/fail/inconclusive, and relative seconds since capture start. Host logs, paths, URB identifiers and wall-clock timestamps stay off-repo. Stop immediately for battery/thermal warnings, unexpected output, unwanted high-amplitude haptics, sensitive device spillover, or inability to select exactly one `1302`.
- Prefer unplug and replug for a fresh registration only when safe; this is an ordinary operator action, not a driver-binding change. After any session close all readers, stop the capture, unplug/reconnect controller to return to default enumeration if necessary, verify bound driver and evdev/hidraw return; no persistent changes are intended. A failed probe is inconclusive, not evidence of absent support.

### Session 0 — any Linux; unprivileged physical descriptor and endpoint inventory

**Prereqs:** connected direct USB `28de:1302`, `lsusb` and Python 3. No `sudo`. These commands are safe to run now and are also copied into #159. Run from an empty temporary working directory; private files are **not** for a Git commit.

```sh
set -eu
mkdir -p steam-p1-private
set -- /sys/bus/hid/devices/0003:28DE:1302.*/report_descriptor
[ "$#" -eq 1 ] && [ -r "$1" ] || { echo "STOP: need exactly one readable 1302 HID descriptor" >&2; exit 1; }
cat "$1" > steam-p1-private/report_descriptor.bin
sha256sum steam-p1-private/report_descriptor.bin
wc -c < steam-p1-private/report_descriptor.bin
LC_ALL=C lsusb -v -d 28de:1302 2>/dev/null |
  sed -E '/iSerial|Serial Number|SerialNumber|iInterface.*[Ss]erial/Id' \
  > steam-p1-private/lsusb-scrubbed-review-first.txt
for d in /sys/bus/usb/devices/*; do
  [ -r "$d/idVendor" ] && [ -r "$d/idProduct" ] || continue
  [ "$(cat "$d/idVendor")" = 28de ] && [ "$(cat "$d/idProduct")" = 1302 ] || continue
  printf 'configuration interface count: '
  cat "$d/bNumInterfaces"
  for i in "$d":*; do
    [ -r "$i/bInterfaceNumber" ] || continue
    printf 'interface=%s alt=%s class=%s endpoint-count=%s\n' \
      "$(cat "$i/bInterfaceNumber")" "$(cat "$i/bAlternateSetting")" \
      "$(cat "$i/bInterfaceClass")" "$(find "$i" -maxdepth 1 -name 'ep_*' -type d | wc -l)"
  done
done
```

**Check:** `wc -c` is expected from July notes to be **372**; mismatch → halt schema/descriptor assumptions and record new version. Source `steam-ibex-linux-driver` predicts direct unified interface and collection-based selection; `lsusb`/sysfs may falsify topology assumption. `lsusb -v` may display other identifying strings not labeled serial: manually inspect the scrubbed text before any publication. If no matched sysfs path, insufficient permissions or more than one device, **stop**; do not choose an arbitrary controller. **Restore:** none; no driver state modified. Private descriptor bytes can be copied to an explicitly reviewed corpus fixture after separate disclosure check; retain full USB configuration offline until scrubbed.

### Session 1 — Linux 7.3+ **hid-steam bound**; usbmon bidirectional registration, evdev, IMU, Menu, rumble and unplug

**Prereqs:** already-installed `usbmon` + `tshark` (or text usbmon reader), `evtest` and optional `fftest`; consent to monitor the *entire USB bus* privately. Check `uname -r`, `lsusb -d 28de:1302` and the `driver` symlink of the matched HID device. If it is not `hid-steam`, **stop S1**, do not force bind. Temporarily close Steam, SDL and other client readers; only this host state permits the expected kernel evdev path. Find the matched bus/device number locally, not from static examples.

```sh
uname -r
lsusb -d 28de:1302
for h in /sys/bus/hid/devices/0003:28DE:1302.*; do
  [ -e "$h" ] || continue
  readlink "$h/driver" || true
done
command -v tshark
command -v evtest
command -v fftest || true
# Terminal A ONLY. sudo is permitted here ONLY for usbmon access:
sudo modprobe usbmon
# Replace BUS with the decimal bus number printed by lsusb, e.g. 1.
# Start BEFORE manually unplugging/replugging the direct controller.
sudo timeout --signal=INT 240 tshark -i usbmonBUS -w steam-p1-private/s1-bus-PRIVATE.pcapng
```

In **terminal B**, while capture is running: (1) manually unplug/replug to include registration; watch for feature **report ID 1**, inner `0xae` string GET then `0x83` numeric attribute GET and the kernel lizard SETs `0x85/0x8e` (default) or `0x81/0x87` (disabled) per `steam-c6-feature-registration`, `-kernel-exchange`, `-kernel-lizard`. Note *which* branch runs, GET return lengths/status, and whether failure leaves input nodes. Do not disclose `0xae` payload or numeric unique-ID data. (2) `evtest` interactively select **only** the verified controller gamepad event node; start a second `evtest` on the verified sensor event node if present, move one axis at a time, close both with Ctrl-C. Observe IMU mode `0x87` setting `0x30` on sensor open and close (`steam-c6-feature-imu`) and evdev-only unchanged-lizard expectation (`steam-c6-kernel-ibex-evdev-open-close`). (3) Press **Menu** at approximately 200 ms, release/neutral; then approximately 700 ms, release/neutral, recording observer timings; source nominal hold 450 ms (`steam-c6-kernel-menu-hold-450ms`), but manual timing cannot prove the exact threshold. (4) Run `fftest` **only if the verified controller event node advertises EV_FF**, choose a short, low-amplitude effect, do not repeat on unexpected output; kernel source may coalesce to ~20 Hz (`steam-c6-kernel-rumble-coalesce-20hz`). If unavailable, record blocked instead of inventing an output. (5) Unplug; observe removal, Ctrl-C and let timeout stop in terminal A.

**Expected/compare:** kernel may register evdev/sensors, and report `0x42` 54B (`steam-c6-input-42`); `0x43` 15B battery (`steam-c6-battery-43`) may or may not appear. Source uses **feature report 1**, not direct wired report 2 (`steam-c6-no-wired-feature2`). Host GET errors can be nonfatal; do not label a missing reply successful. Capture both submission and completion URBs; usbmon *may not* reveal all semantic values until separately decoded. **Stop:** wrong driver, no exclusive target bus identification, absent usbmon capture permission, sensitive bus content, thermal/unwanted feedback, or stuck device. **Restore:** close evtest/fftest, let `timeout` finish, unplug/replug and verify driver/nodes. Loading usbmon is a transient kernel module change; do not unload globally if other processes use it. No persistent udev/kernel/Steam settings are modified.

**If binary usbmon unavailable:** owner may use `sudo cat /sys/kernel/debug/usb/usbmon/BUSu` for **usbmon access only**, redirected to a private file with a bounded `timeout`, but report that payload completeness and parser availability differ. Never substitute raw hidraw-only reads for a claim about host outputs.

### Session 2 — same host; SDL3 3.4.10+ `testcontroller` and controlled input diffs

**Prereqs:** `hid-steam` remains bound, Steam not running, `testcontroller` compiled/installed from an identified SDL3 **3.4.10 or later** that includes Triton HIDAPI; version and library path verified locally. A system `pkg-config` version alone **does not** prove this executable's linked version. Do not assume SDL calls sensor enable or rumble automatically; exercise those controls in the application if supported and mark unavailable functions as blocked.

```sh
pkg-config --modversion sdl3
command -v testcontroller
ldd "$(command -v testcontroller)" | grep -i SDL || true
# Terminal A: same owner-approved usbmon command, limited to the 1302 bus.
sudo timeout --signal=INT 240 tshark -i usbmonBUS -w steam-p1-private/s2-bus-PRIVATE.pcapng
# Terminal B, ordinary user:
SDL_JOYSTICK_HIDAPI=1 SDL_JOYSTICK_HIDAPI_STEAM=1 testcontroller
```

Capture one input-only 5–10-second neutral baseline and **separate, labeled windows**: A/B/X/Y, View/Menu/QAM/Steam, D-pad, bumpers, rear L4/L5/R4/R5, stick clicks and stick *touch* independently, both triggers analog rest/mid/full and click, each stick center ±X ±Y plus diagonal, individual pad touch in four corners/center, independent clicks and pressure levels, grip touch each side, and stationary→single-axis controlled orientation/motion→stationary. Do not press multiple unknown controls simultaneously; use negative untouched controls. Observe native `0x42`/`0x45`/`0x47` IDs, lengths, seq/timestamp/cadence, lost frames, event decoder fields, and raw byte diffs. Special checks: Menu/View bit-6/bit-14 discrepancy; trigger/pressure signedness; `0x42` bytes 46–53: kernel quaternion versus historical opaque. Follow `steam-c6-input-buttons`, `-input-scaling`, `sc2-july-historical-encoder-42-*`. A lack of an ID in this bounded session is not a universal absence.

Using the UI, **if it provides the control**: opt into accel/gyro then disable (expected SDL `0x87` setting 48 `0x18/0`, `steam-c6-feature-imu`); request low/short rumble with deliberate stop, then close (expected `0x80` and potential re-send after ≥40 ms on update calls; `steam-c6-sdl-rumble-resend-40ms`, `steam-c6-output-80-81`). Keep report-level times to compute actual wired intervals; **Puck's July ~266/s aggregate is not wired cadence**. Record any input `0x44` within an output-correlated window; don't interpret as ACK without correlation and status changes (`sc2-gap-haptic-ack`). Observe the SDL `0x87` lizard disable write roughly each three seconds while active (`steam-c6-feature-sdl-lizard`), and 0/3/7/10 seconds after close for real watchdog transition; do not assume an exact seven-second timeout (`sc2-gap-physical-lizard-watchdog`). Compare evdev node presence before open, during raw client, after close (`steam-c6-kernel-client-raw-forward`).

**Stop:** SDL version mismatched, no Triton classification/hidraw access, unintended concurrent Steam ownership, unbounded output, USB capture on wrong bus or unable-to-correlate report IDs. Classify blocked and retain private log. **Restore:** close SDL, stop bounded usbmon, verify kernel evdev nodes return, unplug/replug if required; do not issue driver unbind or modify persistent controller calibration.

### Session 3 — optional, Anders-controlled Steam client (passive)

**Prereqs:** explicit user consent and chosen account; never enter credentials under a recorder. Avoid chat, browser, purchase, cloud configuration and Steam account fields during recording. Start only after S1/S2 have clean baselines. In terminal A run the same `sudo timeout --signal=INT 180 tshark -i usbmonBUS -w steam-p1-private/s3-bus-PRIVATE.pcapng` (sudo solely for usbmon). In terminal B Anders starts **Steam manually** after capture begins, observes discovery, a neutral window, one input, optional *Identify/Ping* once with low output, close/exit, then watches lizard fallback and unplug/replug. Do not run any command that reads Steam profile/account files. **Expected:** Steam's physical host requests, liveness and order are **No evidence**; record every observed report ID/feature command plus host output, return status, relative time and user-visible effect without declaring an API acceptance. Observe any `0x44` after haptics or `0x86..0x89` only *passively*. Do not play/capture arbitrary audio streams, write unknown feature commands, or modify Steam settings for the study. **Stop:** privacy spillover, app/account telemetry on bus, unexpected update/firmware prompt, unwanted effects. **Restore:** close Steam and capture, verify original device use; omit S3 entirely if not approved.

### Interpretation and boundaries

Record each row as `observed`, `not observed during bounded window`, `blocked` or `inconclusive`, including explicit denominator/window duration and USB capture loss count. Never translate a 10-second report count into 1 kHz hardware polling or assume SDL's 4032 µs rate was measured. A generic `fftest`/evdev success proves kernel output behavior only; SDL's `testcontroller` success is an **actual consumer observation**, not virtualgamepad/UHID acceptance. Compare separate bound/unbound and client-opening-order scenarios only under a later explicitly authorized session.

## C. Private capture reduction, disclosure and publication

**Threat model:** usbmon records the *whole bus*, including unrelated devices, every HID/feature payload, USB string descriptors, hardware unique IDs, and sometimes sensitive on-device input. **Never** commit raw `.pcapng`, unfiltered usbmon text, local sysfs paths, full `lsusb`, a trace with user names/account data, serial values, Bluetooth/MAC addresses, hostnames, full URB IDs or wall-clock times. Use a dedicated quiet bus if possible and verify no unrelated device traffic. The literal USB iSerial and feature-`0xae` serial reply **must be dropped or salted/hash summarized**, never copied verbatim. `0x83` attributes may include unique identifiers; withhold raw attribute bodies until field-level review. Preserve HID **report descriptor bytes**, report ID/length/direction, and non-identifying *input/output report payloads*, including unknown extension bytes, only after a human review and per-frame allowlist. Preserve raw artifacts **offline**, never in a public issue.

**Reduction command (private, exploratory, not itself publication-safe):** enumerate field availability with `tshark -G fields | grep -E 'usb.capdata|usbhid.data|usb.urb_id|frame.time_relative|usbhid.setup'`; then run `tshark -r steam-p1-private/s2-bus-PRIVATE.pcapng -Y 'usb.device_address == DEVICE' -T fields -e frame.time_relative -e usb.endpoint_address -e usb.capdata -e usbhid.data -e usbhid.setup.bRequest > steam-p1-private/s2-selected-PRIVATE.tsv` after substituting a verified USB device address. **Keep that TSV private**: it is neither complete transaction evidence nor automatically sanitized. USBmon setup/completion correlation can require `usb.urb_id` inside the *private* parser. If fields are absent, change extraction under local Wireshark inspection; do not guess where HID report IDs start or treat a feature control header as a report. Only submit report bytes after manually classifying USB transfer direction/type and correlated URB completion.

**Minimal fail-closed pure-Python reduction, run locally on reviewed JSON lines** (create `steam-p1-private/classified-PRIVATE.jsonl` from selected, *reviewed* HID transfer payloads; one object per line with only `session`, `kind` = `input`/`output`/`feature_request`/`feature_reply`, `t_rel_ms`, `report_hex`, and for feature entries `inner_command`). This deliberately does *not* parse raw USB packets; misaligned captures must be resolved off-repo. The script and unit tests under `tools/steam_capture_reduce.py` and `tests/test_steam_capture_reduce.py` implement the exact allowlist and fail closed for serial, attributes and unrecognized feature reports. Run:

```sh
python tools/steam_capture_reduce.py \
  steam-p1-private/classified-PRIVATE.jsonl \
  steam-p1-private/s2-reduced-review-first.jsonl
python -m unittest discover -s tests -p test_steam_capture_reduce.py
```

The output retains per-report **relative** time, ID, direction, length and explicitly allowed input/output bytes, but drops unrecognized metadata. It hashes and omits all feature reply bytes by default (including `0xae`, `0x83`) and retains only the safe **command/length** of feature requests. Manually review entire reduced output for uniqueness/disclosure **before** incorporating any selected sanitized fixture into corpus `fixtures/` with hashes and explicit source/experiment/claim lineage under the schemas. `publication_guard.py` does not certify safety; run it and the schema validator on any public proposal. Keep descriptor/allowed packets only in a consented sanitized physical fixture; otherwise public JSON claims can include categorical outcomes, counts, sizes, relative timings and hashes without a payload. The raw pcap, exact device assignment and private logs stay offline indefinitely or follow the operator's own retention policy.

## D. Session record templates (do not commit fabricated run results)

Use the existing schemas exactly. Templates below are **illustrative payloads** to fill in after execution, not pre-existing experiments or physical claims. Each session has independent IDs; retain `not_run` until its run is performed. Add the `records/experiment/` and `records/claim/` files only when a source pointer, outcome and reviewed evidence exist. If a real physical claim is to be upgraded to `physically_observed`/`physically_validated`, `tools/validate.py` requires a passed `controlled_physical` experiment **and linked physical fixture referencing that claim**; notes alone cannot satisfy the gate.

```json
{
  "schema_version": 1,
  "id": "steam-p1-s0-descriptor-experiment",
  "kind": "controlled_physical",
  "status": "not_run",
  "sources": ["sc2-src-capture-notes-2026"],
  "fixtures": [],
  "procedure": "S0: sysfs HID report descriptor, scrubbed USB config/interface/endpoint inventory on physical direct 1302; read-only ordinary user.",
  "semantic_outcome": null
}
```

S1/S2/S3 experiment IDs `steam-p1-s1-kernel-experiment`, `steam-p1-s2-sdl-experiment`, `steam-p1-s3-steam-experiment` use identical keys, `kind: controlled_physical`, `status: not_run`, `fixtures: []`, `semantic_outcome: null` and individualized `procedure` from Section B. S3 may remain indefinitely absent if no operator consent.

```json
{
  "schema_version": 1,
  "id": "steam-p1-s0-descriptor-claim",
  "statement": "TO REPLACE ONLY AFTER S0: report descriptor bytes/hash, USB interface and endpoint topology with a bounded physical outcome; never include identifiers.",
  "status": "unknown",
  "applicability": {
    "controller": "steam-controller-2026",
    "revision": "physical revision to be recorded non-identifyingly",
    "firmware": "unmeasured unless safely verified",
    "transport": "usb",
    "scope": "S0 direct wired authentic physical device; not an emulated host test"
  },
  "sources": ["sc2-src-capture-notes-2026"],
  "experiments": [],
  "conflicts_with": [],
  "supersedes": [],
  "rejection_scope": null
}
```

S1/S2/S3 claim IDs `steam-p1-s1-kernel-claim`, `steam-p1-s2-sdl-claim`, `steam-p1-s3-steam-claim` use the same schema, `status: unknown` initially, `transport: usb`, and a separate statement/experiment/fixture per measured finding. Add `evidence_role: consumer` for **host behavior** and keep device byte/layout claims as `device`; avoid claiming all controls validated in a single broad claim. Never turn these examples into passing records without a real lab artifact. The claim and experiment template names are an operator drafting aid; no tests were run while writing this plan.

**No persistent configuration changes; no local implementation directives.** Capture prep only, not a step-16 run or authorization to change virtualgamepad branches.

Cloud agent (Steam capture plan)
