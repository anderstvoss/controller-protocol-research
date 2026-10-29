# W5 gyro diagnosis tooling

Original tools; no upstream source is copied. Runs against unchanged
virtualgamepad baseline `b23cb416397ec4698c4a2576f7504061447b286d` with the
existing Linux6.12.113+deb13-arm64 / SDL3.2.10+ds-1 tuple. Installs nothing and
performs no grants, root operation, driver unbind or persistent policy change.
Raw logs, identities and local paths stay private. No physical input is read.

Build from a clean baseline checkout with cached dependencies:

```sh
python3 tools/wii_w5/build.py --case baseline --virtualgamepad ../virtualgamepad \
  --output /tmp/wii-w5-build \
  --sdl-pkg-config-path /usr/lib/aarch64-linux-gnu/pkgconfig:/usr/share/pkgconfig
LD_PRELOAD=/tmp/wii-w5-build/trace.so W5_TRACE=/tmp/wii-w5-private.jsonl \
  W5_ROLE=provider /tmp/wii-w5-build/target/debug/wii-w2-host-probe \
  /tmp/wii-w5-held /tmp/wii-w5-build/sdl_probe \
  b23cb416397ec4698c4a2576f7504061447b286d
```

The retained Cargo package name is historical; the W5 source/executable hashes
identify the actual tool. Locked/offline Rust and C/SDL builds use the existing
installation. The pkg-config directory is an explicit recorded-host selection,
not a portable default. The provider is compiled before any code-side test-only
addition. Reproduction requires a clean checkout at the recorded baseline.

The helper creates one MotionPlus-attached virtual device and holds it for up
to two hours, continuously servicing requests. Before any grant, independently
verify exact creation HID_PHYS, canonical virtual UHID ancestry, bus5:057e:0306,
wiimote binding, raw-node parent and four LED files under that root. Confirm the
MotionPlus event node is readable without changing permissions. Send guarded
per-node grants locally to Anders, wait for his confirmation and reverify exact
identity/access before creating `go`. Never reuse paths after removal/expiry.
The helper changes no permissions or host policy.

## Ordered arms

1. Kernel/H3 first, MotionPlus and MotionPlus+Nunchuk: the child holds only the
   exact-owned MP evdev node and its raw observation FD. No SDL initialization.
   It records20seconds of ABS_RX/RY/RZ while the parent drives the two W4 raw
   rotation vectors, all slow flags true. Trace captures mapping/ACK/input.
2. At `h3-complete`, inspect captured active packets with analyze.py. Require
   valid gyro discriminator, reserved bit clear, distinct yaw/roll/pitch values
   matching the application drive, correct slow flags and pass-through
   alternation in mode05. Map/reset tracking uses successful ACKs. Add
   `h3-verified` only after checking evidence. A discrepancy must be reported
   on#158 before any fix; do not continue SDL arms with an unverified encoder.
3. Fresh SDL3.2.10 processes per configuration and arm: no-holder control, then
   holder-open-before-SDL.60second post-open drive windows. The owned MP event FD
   remains open through the holder window and closes only after SDL shutdown.
   Topology is fixed within each child; values toggle250ms with application
   commits around20ms. Neither interval is a firmware-cadence assertion.
4. At `runs-complete`, create `done`; close twice and separately verify owned HID
   root/raw disappearance. No global count/creation/first-neutral timing oracle.

## Observation and attribution limits

trace.c records successful own-process UHID input/output and exact-owned raw
read/write completions with CLOCK_MONOTONIC timestamps. Raw writes from the SDL
process are distinguishable from its explicit probe FD. Provider INPUT2 writes
are labelled provider; aggregate UHID OUTPUT is not automatically labelled SDL.
A unique equal raw write within100ms can identify an observed actor; multiple
matches retain ambiguity. Unmatched events are kernel-or-untraced, not a claim
that every possible host writer was intercepted. Completion timestamps can be
reordered across processes, so nearest-time pairing is not strict causality.

Explicit probes read A400FA/A600FA identifiers before/after public SDL_Init and
SDL_OpenJoystick API boundaries, after sensor enable and during drive. They do
not instrument the private InitDevice entry/exit or directly inspect SDL's
cached m_ucMotionPlusMode. Correlate the observed register transaction sequence
with the pinned source when distinguishing internal initialization/open resets.
The separate probe FD sees copies of reports; same-address concurrent replies
can be ambiguous and must not be treated as a stronger private-state oracle.
A600FA can be unmapped while MotionPlus is active; preserve missing/error replies.

The tracer excludes CREATE identity events. Provider write acceptance does not
prove every consumer received the report; explicit evdev/SDL observations are
separate evidence. SDL gyro sample polls can repeat a cached zero value; retain
actual gyro event counts and numeric extrema independently. Enabling capability
alone is not delivery. No physical/calibrated/radio equivalence is implied.
Optional SDL3.4.18 is not installed by these tools; no system-wide build change.


## Separately requested Dolphin sanity check

Anders requested a direct-backend sanity check after the six main W5 runs.
Dolphin2609a real-Wii HIDAPI IO is independent of its SDL gamepad sensor path.
Use build.py with `--dolphin` to build dolphin_host_probe.rs and dolphin_trace.c;
no SDL development package is needed for this variant. The trace raw actor uses
its explicit role, rather than the baseline tracer's SDL label. The published
child accepts `W5_DOLPHIN_CACHE`, replacing the private run's scratch cache-file
lookup; that portability-only change is not the exact executed-source hash.

Choose a fresh writable scratch directory inside the existing Dolphin Flatpak
cache, pass its absolute path as W5_DOLPHIN_CACHE, and copy trace.so there. Both
the host and sandbox must see it at the same path. Launch the holder as above
with the copied dolphin_child.py (through a small executable wrapper invoking
Python), the Dolphin trace variant and a new hold directory. Do not install a
Flatpak/package or change persistent overrides. The child guards against another
Wii HID before allowing Dolphin scanning; it never captures other raw paths.

Verify exact creation ancestry/identity/raw parent again. This check needs one
human-applied/confirmed per-node hidraw grant, not the four LED-class grants.
Only then add go. Each of the two fixed profiles launches a fresh offscreen
Dolphin2609a private profile for45seconds, no ROM, all Real Wii slots disabled so
scanned remotes may enter controller interface, WiimoteControllerInterface=True,
continuous scanning and speaker disabled. SDL_JOYSTICK_HIDAPI_WII=0 keeps SDL Wii
HIDAPI out of this independent direct path. Other application backend activity
is outside the exact-owned tracer, not a physical-controller experiment.

The installed source's correct key is WiimoteControllerInterface, not the older
W1 helper's ConnectWiimotesForControllerInterface spelling. W1 remains unchanged.
The two W5 runs verify sandbox raw open and bounded app execution, but record no
owned raw read/write trace and establish no direct backend claim, initialization
or numeric gyro. Empty observations are not a proven zero stream. At
runs-complete add done, wait closed and verify root/raw disappearance. No kernel
unbind, replacement build, UI/game polling oracle or physical test was attempted.
