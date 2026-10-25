# W7 Cemu ARM64 AppImage follow-up

The initial W7 lookup checked PATH and the aarch64 Flathub ref. It missed an
installed AppImage outside PATH and did not establish that Cemu was absent.
`wii-w7-cemu-appimage-result` supersedes that availability inference. Original
W7 records, including the failed lookup, remain unchanged.

The owner requested the installed ARM64 AppImage 29f2f1f, matching surveyed Cemu
commit `29f2f1fae4631e2317977debd9eacd55cc28dd7d`. Binary hashes are in the reduced
fixture. It was extracted privately and launched through its own AppRun, with
separate temporary XDG settings/data/cache and a native `Wiimote` slot 0 profile
(motion enabled), no game or ROM. Native virtualgamepad code remains 840db277 on
Linux 6.12.113 ARM64. A fresh exact-owned UHID identity and five locally supplied
human grants were verified before go. No agent grant, sudo, unbind, installation,
persistent policy or radio operation was performed.

## Runs and checkpoints

Four 35-second profiles compare MP and MP+Nunchuk with/without an external holder
of the exact-owned kernel MotionPlus evdev FD. An initial four-arm metadata trace
was repeated in four fresh app profiles with complete owned raw byte capture to
attribute Cemu requests. Only reduced counts are public. The byte-capture repeat
is authoritative for request attribution; the initial trace had only lengths and
report IDs. All eight observation windows reached their bounds; TERM closed each
app with exit 0 and no surviving exact-profile child, before the next arm. Holders
closed between arms. The same UHID/protocol state was reused: this is not a
cold-device independence or timing experiment.

A process-only original guard admits only the owned raw path in Cemu, denies
full-path input/USB opens outside that allowlist, and rejects AF_BLUETOOTH socket
calls. Thus generic SDL cannot open the MotionPlus node in no-holder arms. The
external holder is separate from Cemu. Preflight found no unexpected holders.
The dynamic guard is not a complete security sandbox or an application-state
oracle; relative/internal I/O hooks can have coverage limits.

| Byte-capture arm | Cemu native A600FE04 writes | Combined host maps | Native requested modes | EEPROM 0016/8 error 8 replies | Received 37 packets |
| --- | ---: | --- | --- | ---: | ---: |
| MP, no holder |1 |04 x 1 |33 x 52 |39 |0 |
| MP, holder |0 |04 x 122 |33 x 439 |232 |0 |
| MP+Nunchuk, no holder |1 |04 x 1 |33 x 31, 37 x 58 |40 |2480 |
| MP+Nunchuk, holder |0 |05 x 40 |33 x 175, 37 x 129 |104 |1398 |

Combined host counts cover configuration settling, app observation and cleanup;
they are not only the app window. Cemu raw counts cover that app instance's I/O.
In both no-holder runs Cemu directly writes A600F0=55 and A600FE=04. In holder runs
Cemu sends no A600FE writes, but repeatedly writes A400F0=55 and A400FB=00 while
the kernel maps 04/05. Native resets and kernel mapping can coexist; no single
cause of the mixed report selection or dispatch is inferred from these races.

All four arms establish native enumeration/open, status write/read, EEPROM read
requests, register traffic and input-report transport. The first unsatisfied
handshake checkpoint is calibration: each requests 8 bytes at EEPROM 0016 and
receives error 8. The unchanged default caller image is empty and no image was
imported. The pinned virtualgamepad memory implementation explicitly returns 8
for reads outside that image; this is its existing caller-resource policy, not
a newly proved protocol defect. Importing a suitable calibration fixture and
rerunning is a separate experiment, not performed here.

MP-only Cemu requests 33, not the 37 gyro-parser path. Nunchuk arms also request
and receive 37, but delivered raw packets do not establish the variant selected
by the decoder or a changing application gyro value. The installed build does
not expose the source's debug gyro log. No decoded-state/UI gyro oracle was
observed. Source expectations, raw report delivery and kernel gyro are separate
from decoded Cemu gyro. End-to-end gyro remains **blocked**, not measured zero,
not calibrated rates or general Cemu non-support. No Cemu gyro acceptance cell
is justified by this run; no model/codec/descriptor change follows.

## Reproduction and cleanup

Use the existing original W7 host probe and human grant procedure. Wait for a
matching phase `ready.json`; record exact owned input names. Configure native
Wiimote API, slot 0, motion enabled in a fresh profile. Set W7_ALLOWED to only the
owned raw node, W7_RAW_NAME to that node's basename and W7_IO_LOG to private
scratch. Preload `cemu_guard.so`; keep SDL Wii HIDAPI disabled. A holder is an
external nonblocking read FD on the owned MotionPlus node, drained during the
window. Record 35 seconds, terminate only the exact-owned app/profile, verify no
child survives, close the holder, then switch attachment. Do not open unrelated
devices, pair, unbind or introduce game content. `cemu_trace.py PRIVATE_TRACE`
reduces native requests and reports without promoting them to decoded gyro.

The fixture records actual helper/runner/guard source and executable hashes.
The published guard has the same opaque libudev ABI declaration correction as
W7's public guard; private executed source provenance remains explicit. The
initial and capture runners used no native-code patch or application injection
other than the original dynamic I/O guard. Private profiles, raw bytes, identities,
paths, terminal/app logs and wall clocks are not redistributed.

After all eight app instances/holders closed, the producer closed idempotently;
owned HID, raw and LED nodes were verified absent. No uinput device was created
in this follow-up. Deterministic tests use fake request bytes, reject incomplete
writes and preserve calibration, decoded-state and availability-correction limits.
