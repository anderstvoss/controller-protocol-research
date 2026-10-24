# W7 independent consumer diagnostics

Original bounded diagnostic helpers. No upstream source/header, ROM, physical
capture or private log is redistributed. See `docs/wii-w7-consumer-runs.md` for
versions, actual outcomes and observation limits. These are not provider changes.

Build with `python3 tools/wii_w7/build.py --virtualgamepad CHECKOUT --output SCRATCH
--libretro-header HEADER`. CHECKOUT must retain the native code from 840db277;
SCRATCH must be outside both repositories. HEADER is an operator-provided
`libretro.h` from RetroArch v1.20.0 `libretro-common/include/libretro.h`;
its reviewed SHA256 is recorded in the W7 fixture environment. Building requires
Rust, C, libxwiimote and libudev development files. No helper installs anything.

`wii-w7-host-probe SCRATCH SOURCE_SHA` creates one Bluetooth-bus Wii Remote with
MotionPlus+Nunchuk, verifies the creation-owned HID identity/driver and writes
private `grant.json`. It services the device without driving inputs until the
operator has applied/confirmed the existing temporary per-node grant procedure
and a coordinator creates `go`. It never grants access. `command.json` atomically
selects `{id,case,target}`; target is `bt` or `uinput`, case is `motionplus` or
`motionplus-nunchuk`. Wait for matching `ready.json` before opening a consumer.
Cases remain fixed throughout each consumer window. Creating `done` closes both
sessions twice and checks HID/raw removal; the outer limit is one hour. All raw
output, session paths and metadata are private, never corpus fixtures.

On that exact HID syspath, `xwiishow SYSPATH` can be run in a 160x40 pseudo-terminal.
The installed version starts with MotionPlus on: the recorded sequence toggled
`m` off/on at seconds1/2, enabled normalization with `n` at6, then `q` at12.
`xwiimote_probe SYSPATH` records18 seconds in three6-second phases: default,
static offsets10/20/30, then zero offsets with factor10. It requests Nunchuk too,
but callers must inspect the returned opened mask rather than infer support.
`evtest` was run for12 seconds on the verified owned MotionPlus event node.

`input_diagnostic.so` is a no-content libretro core, not a game. RetroArch runs
with a fresh private profile, udev input/joypad drivers, null video/audio, explicit
button/axis bindings, and a25-second process limit. After600 core frames it emits
control-change counts and the results of accel/gyro activation on8 ports.
Frame shutdown did not reliably terminate the frontend; both recorded arms ended
at the bounded timeout. Inspect held *owned* event FDs during the window to
separate enumeration/keyboard probing from retained sensor selection.

`owned_io.so` is an interposer for dynamic open/open64/openat, raw read/write and
selected libudev calls. `W7_ALLOWED` is a semicolon-separated exact-owned event/raw
path list; other full-path input/raw opens are denied. `W7_IO_LOG` is a private
trace destination; `W7_RAW_NAME` selects the owned hidraw basename for metadata
observations. It is observation tooling, not a security sandbox or internal
Dolphin function breakpoint. Never open a foreign device. Positive-control
`udev_control RAW_PATH` enumerates metadata and opens only the named raw path;
keep its trace separate from Dolphin's trace.

Dolphin2609a used a fresh private profile per35-second MP/MP+Nunchuk arm, all real
slots0, WiimoteContinuousScanning=True and WiimoteControllerInterface=True under
Core, speaker false, background input, offscreen Qt, Wii SDL HIDAPI disabled.
The library/profile reside in private app cache so no Flatpak filesystem override
or persistent permission change is needed. Compare enumerate, owned status-write,
connection and ControllerInterface checkpoints; missing observations do not prove
an internal method failed. Own trace files were empty although the separate
positive control worked. No ROM/bootstrapping content or UI action was injected.

Timeout does not guarantee Flatpak child cleanup. Identify children by exact
fresh profile argument, send TERM only to those owned children, wait and recheck;
never use a broad process-name kill. The first W7 pilot missed this between-arm
cleanup and its profile comparison is invalid. The corrected fresh-device repeat
performed cleanup before each attachment switch: two TERM actions, no KILL, and
verified no owned children before continuing. Its traces also stayed empty; the
separate access/trace controls passed again. Preserve both the pilot limitation
and corrected observations.
Verify those children and all owned HID/raw/LED/uinput nodes are gone before
reducing/publishing results. Preserve private artifacts locally; publish semantic
counts, version/hash provenance and explicit pass/limit/blocked boundaries only.

## Installed Cemu AppImage repeat

The [additive AppImage experiment](../../docs/wii-w7-cemu-appimage.md) corrects
W7's incomplete PATH/Flatpak availability inference. `cemu_guard.c` adds private
owned-byte trace capture and an AF_BLUETOOTH socket refusal to the original
owned-I/O guard; build.py also produces `cemu_guard.so`. Use only the owned raw
path in W7_ALLOWED, keeping the external kernel holder separate. It is a dynamic
hook guard, not a complete sandbox or proof of application-state decoding.
`cemu_trace.py PRIVATE_TRACE` reduces only native protocol addresses, counts and
report IDs. Raw reports are not a gyro oracle; calibration error8 and missing
decoded-state observations remain explicit. No additional dependency is needed.
