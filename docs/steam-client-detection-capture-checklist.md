# D9 / physical 1302 — sanitized Steam detection capture checklist

**Owner-operated only; not executed by this research lane.** Complements [physical capture plan Sessions 1 and 3](steam-physical-capture-plan.md#session-1--linux-73-hid-steam-bound-usbmon-bidirectional-registration-evdev-imu-menu-rumble-and-unplug). Keep raw controller log and USB traffic **private and off-repo**. Use the same Steam Stable build when comparing. Never send probes to the retail device outside the existing, authorized passive sessions. Stop at any firmware-update prompt.

## 1. Session separation and setup

- [ ] Record Linux/kernel, Steam build/channel, `hid-steam` binding, whether SDL/other readers are closed, whether device is physical USB or virtual UHID, and the *presence* of a USB parent and interface number (publish **only** the presence/type, not topology path).
- [ ] **Session 1:** Steam closed; fresh physical 1302 attach, **bidirectional usbmon**, only target device URBs, kernel registration and resulting evdev/hidraw state. Record where the capture starts relative to attach. Monitor optional feature-2 but do not inject it.
- [ ] **Session 3:** independently fresh physical 1302 attach with Steam deliberately opened by the owner; run bidirectional bus capture and corresponding `logs/controller.txt` observer; do not enable firmware update. Include a Steam-open-before-attach and Steam-open-after-attach comparison **only** if already approved.
- [ ] **D9 virtual:** one Steam-only trial, then one kernel-only baseline; no simultaneous SDL unless a separately identified simultaneous-read test is intended. Pair each local codec toggle with its exact commit/revision and status, keep raw logs private.

## 2. Record exact safe protocol selectors (report **counts and status**, no raw payload)

For each transaction: **source category** (kernel/SDL/Steam/unknown), report type (feature SET/GET vs output/input), feature report ID (1 or 2), inner command, SET→GET pairing, length, completion success/failure/timeout, and relative timing. A report1 64-byte SET alone **does not prove** which process issued it.

- [ ] **Feature1 `0x83` GET_ATTRIBUTES_VALUES:** count command SET and GET attempts; GET reply opcode, declared payload length, number of 5-byte tag/u32-LE pairs; list **tag IDs** `0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17` present, with targeted attention **1 product, 2 capabilities, 4 firmware build, 9 board revision, 10 bootloader build, 11 connection interval**. Use `value_present=yes/no`, `width=u32le` publicly; physical values only in separately owner-approved private notes. Compare five-tag vs zero-tag and repeated identical commands.
- [ ] **Feature1 `0xae` GET_STRING_ATTRIBUTE:** track requested index **0** board, **1** unit, **3** extra string (plus any other numeric index), command arg size, reply length, return code, string present/empty status. **Never display any string content**, including an apparently constant index3 value.
- [ ] **Feature1 `0x87` SET_SETTINGS_VALUES:** decode each **(setting ID:u8, value:u16-le)** triple; specifically key **9** lizard (zero/nonzero), **48** IMU (0, 0x18, or other), **50** sleep inactivity timeout (value to private log only; publish zero/nonzero/range bucket), **71** Steam watchdog (zero/nonzero), plus **all other IDs encountered** as IDs only. Record whether multi-key writes **succeed or reject atomically**, and any subsequent GET/echo; separate host-written data from device reply.
- [ ] **Feature1 `0x85` SET_DEFAULT_DIGITAL_MAPPINGS**, **`0x8e` LOAD_DEFAULT_SETTINGS**, **`0x81` CLEAR_DIGITAL_MAPPINGS**: capture SET and completion, mode before/after, whether these arose during Steam-closed kernel registration or Steam-active operation.
- [ ] Also count **`0x89` GET_SETTINGS_VALUES**, **`0x8b` GET_SETTINGS_MAXS**, **`0x8c` GET_SETTINGS_DEFAULTS**, **`0xb4` DONGLE_GET_WIRELESS_STATE** (do not assume wired call), **`0xed` TRITON_READ_SETTING** and **feature report2** attempts. Log any unrecognized command *numeric IDs and error types only*. **Do not inject** `0x90` bootloader, `0x9f` power-off, `0x86` factory reset, firmware or streaming commands.
- [ ] Distinguish **HID output report `0x87`** from **feature1 opcode `0x87`**. Input-report `0x42` and `0x43` counts/cadence and optional `0x40/0x41/0x45/0x79` report IDs are useful secondary signals; no raw state/frame upload.

## 3. Steam log and decision alignment

- [ ] Privately examine `logs/controller.txt` for **1302 discovery, hidraw open/close, interface number (often -1 on UHID), bus/usage classification, firmware/version gate, attribute query failure, feature SET failure, repeated GET, device-class promotion/drop, Steam Input configuration and timeout**. Publish only **sanitized verdicts and counts**, not raw log lines.
- [ ] Align relative timestamps of seven key50 writes and 364 attribute writes with client state transitions and failure statuses. **Kernel itself issues 0xae and 0x83**; a count alone is not Steam proof.
- [ ] On virtual only, compare independently: `0x83` empty vs approved typed reply; unknown key50 reject vs compat-accept/store; optional string-index/SET echo only if a real physical Session3 shows those requests. Require complete teardown and a baseline between configurations.
- [ ] If nonprotocol suspicion remains, compare **USB-parent yes/no**, **interface number 0/-1**, udev seat access match yes/no, and HID collection ordering **without** publishing sysfs/udev paths. Do not modify udev policy to force detection.

## 4. Sanitize *before publication*

- [ ] Keep `usbmon` `pcapng`, USB setup/descriptor dumps, local log files and console transcripts **off Git and off public issue comments**. Source records may cite public code and immutable commits; experiment results must first pass independent review.
- [ ] Replace every **board/unit/USB/feature-string serial**, including `0xae` indexes 0,1,3 and fallback strings, with `[REDACTED]`; remove USB `iSerial`, hardware `uniq`, Bluetooth addresses, MAC addresses, UUIDs and firmware unique IDs.
- [ ] Remove absolute/relative **host-specific** paths, usernames, device numbers, bus/port location, controller config filenames/keys, custom udev ACL path, USB URB identifiers, wall-clock timestamp and any ancillary device inventory; publish only relative-order timing bins.
- [ ] Review redaction manually: a serial can be embedded in a filename, key or unlabelled field, so matching the word 'serial' is **not sufficient**. Publish **only** aggregate command counts, tag IDs/types, settings IDs and rejection codes once reviewed; no raw bytes from real traffic.
- [ ] Confirm re-identification checks, publication guard, schema validator, history guard and unit tests before the local owner considers incorporating **any** sanitized evidence.

**Cloud agent (Steam detection research)**
