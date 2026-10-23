# W5 MotionPlus gyro diagnosis

W5 uses unchanged virtualgamepad main `b23cb416397ec4698c4a2576f7504061447b286d`
on the W4 Linux6.12.113+deb13-arm64 / SDL3.2.10+ds-1 host tuple. It tests only an
owned Bluetooth-bus UHID device, with MotionPlus or MotionPlus+Nunchuk attached
before each fresh child opens. No protocol model, descriptor, driver, package or
persistent permission policy changes. Anders applied and confirmed five guarded
per-device grants supplied locally; the agent only verified identity/access.

## Packet and kernel oracles, before SDL

The two20second kernel-only runs precede SDL initialization. The exact-owned
MotionPlus evdev FD is held open. A600FE mode04 and mode05 writes receive success
ACKs. Captured active reports contain both application drive vectors: decoded
raw yaw/roll/pitch `[8500,7000,9000]` and `[7800,9000,7000]`. Gyro discriminator bit1
is set, reserved bit0 clear, all three slow flags true. Mode05 alternates gyro
and Nunchuk pass-through. There are zero invalid/mismatched packets or mode05
alternation errors: mode04 has1108 gyro packets, mode05 has528 gyro/528 downstream.
This verifies the emitted bytes, beyond checking application state or a test.

Both kernel runs deliver changing ABS_RX/RY/RZ. Expected all-slow centered values
are yaw -3528..2772, roll -10728..7272, pitch -10728..7272, matching observed extrema.
There are93 events per axis in the MP-only arm and91 in MP+Nunchuk. These axes are
kernel consumer coordinates; they are not calibrated physical rates. An explicit
H3 verification gate releases the SDL comparisons only after these checks pass.
A pure Rust code-side test additionally covers both vectors and all eight slow
flag combinations for modes04/05; it changes no runtime behavior.

## SDL arms and attribution

Two no-holder controls and two holder-before-SDL comparisons use fresh SDL
processes,60second post-open windows, default HID filtering and explicit Wii
HIDAPI hints. Each child also has an exact-owned readback probe FD. The control
has no explicit MP evdev holder; this does not assert that SDL or any other
consumer never briefly opens an event FD. Shared device history and kernel
reconciliation are retained as order/timing confounders, not hidden by the label.

Public SDL_Init and SDL_OpenJoystick boundaries are timestamped. Direct probe
readbacks record A400FA/A600FA identity bytes or error/timeout. Every selected
A400F0/A600FE write and A400FA/A600FA read is retained as semantic data with relative
CLOCK_MONOTONIC time. A400FE/A600FE reads and A600F0/A400FE writes are retained too.
The own-process tracer distinguishes direct SDL writes from explicit probe
writes. A unique identical raw write within100ms identifies an observed writer;
multiple matches are ambiguous and unmatched aggregate writes are labelled
kernel_or_untraced. No claim that all writers were traced is made. Cross-process
syscall completion order is not strict command causality.

Private InitDevice entry/exit and SDL's cached MotionPlus mode are **not directly
instrumented**. Public boundaries, observed SDL reset transactions and pinned
source jointly support conditional reasoning about that mode. Same-address
probe/SDL responses may overlap; errors are retained, never converted to an ID.
Provider emission does not prove SDL received every packet; actual SDL gyro event
counts and cached sample extrema are separate observations.

## Observed SDL result and verdicts

| Profile | Arm | Window ms | Gyro capable/enabled | Cached gyro polls | Gyro events | Disconnected polls |
|---|---|---:|---|---:|---:|---:|
| motionplus | control | 60017 | True/True | 8418 | 0 | 0 |
| motionplus-nunchuk | control | 60014 | True/True | 8322 | 0 | 8281 |
| motionplus | holder | 60020 | False/False | 0 | 0 | 8389 |
| motionplus-nunchuk | holder | 60008 | True/True | 8345 | 0 | 0 |

All four SDL arms have zero nonzero gyro polls and `[0,0,0]` extrema. A zero
sample count in MP-holder is not a successful enabled gyro stream: capability
and enable both fail there. MP-control and MP+Nunchuk-holder stay connected;
MP+Nunchuk-control and MP-holder disconnect. No full SDL acceptance follows.
Both holder runs still deliver kernel gyro with expected extrema (257/256 events
per axis), independently of these SDL outcomes.

**H3:** no demonstrated activation/packing defect for these two vectors/modes.
The active emitted bytes and kernel values pass; no model change is justified.
**Kernel delivery:** demonstrated for both20second kernel-only profiles.
**H1:** an explicit MP evdev holder is insufficient to make SDL gyro work here.
It sustains kernel gyro, but SDL stays zero; controls also contain brief aggregate
map traffic, so they are not a proof of exclusive kernel non-use throughout.
**H4:** the predicted SDL reset is observed, and the holder does not preserve an
uninterrupted mapped identity through open. MP-only is active before open, then
both banks error immediately after open, then active again after sensor-enable.
MP+Nunchuk readbacks overlap/reorder around open (including opposite-bank IDs),
so they cannot establish a unique exact transition instant. Later mapped IDs
and kernel gyro coexist with zero SDL gyro. The source explains that Linux SDL
does not restore/assign cached mode and ordinary periodic presence checks do not
recover it; **the cached value itself is not measured**. Disconnect paths and
readback concurrency prevent uniquely attributing every zero to cached NONE.
The supported result is the bounded consumer reset/ownership limitation, not a
universal statement that SDL can never decode Wii gyro or that physical hardware
was tested.

For example, MP-holder SDL-origin A400F0 resets complete at relative3.0412s and
3.0509s during SDL_Init, and4.0695s/4.0776s around SDL_OpenJoystick. Aggregate
kernel-or-untraced map04 writes follow at3.0625s and4.0882s; a later map04 at4.1495s
restores an active stream. Completion timestamps identify observed writers, not
a strict execution-order proof. The fixtures retain every selected read/write
and boundary; no ambiguous actor or missing reply is silently resolved.

The consumer claim cites pinned SDL877399b InitializeExtension630-636,
OpenJoystick773-799, Linux activation457-468, dispatch1266-1298 and periodic
presence1396-1435. Source-derived conditions are distinct from live observations.
No physical consumer claim is promoted.


## Scope and reproduction

Original tools and procedure are in `tools/wii_w5/README.md`. The six new
`wii-w5-*` fixtures reduce owned-only private summaries/transactions; raw logs,
input/output packets, identities, host paths and wall clocks are omitted.
Private source/executable/library/capture hashes retain provenance. Old records
and all `wii-gap-*` claims stay byte-identical. Synthetic analysis tests cover
ACK failure, axis/flag decoding, remap alternation, ambiguous writers and safe
semantic reduction. These fixtures are measured virtual-host runs, not physical
or manually fabricated captures.

H2 SDL3.4.18 is deferred: not built or run; no version comparison is claimed.
H5 multi-consumer order is a remaining timing limitation, not a separately
isolated experiment. H6 Sony-style feature calibration is unsupported by the
pinned Wii source analysis; W5 adds no such protocol behavior. No physical Wii,
radio, gameplay, firmware-cadence, calibration, full mapping or later controller
acceptance follows. No upstream SDL report is filed.
