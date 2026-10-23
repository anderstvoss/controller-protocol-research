# W1 bounded local virtual-host probes

Original probe code, not upstream source. Requires an unchanged Linux aarch64
host with existing UHID/uinput/event access, SDL3.2.10 development files, a C
compiler, the recorded Rust dependencies already cached and the user-installed
Dolphin Flatpak2609a. It installs nothing and uses no root, udev, driver unbind,
module or permission change. Failed access is an observation.

Build against a clean virtualgamepad checkout at
`50161b913d0f82950c292465625e9cdd8854daf2` (Part A PR235):

```sh
python3 tools/wii_w1/build.py --virtualgamepad ../virtualgamepad \
  --output /tmp/wii-w1-build \
  --sdl-pkg-config-path /usr/lib/aarch64-linux-gnu/pkgconfig:/usr/share/pkgconfig
```

The pkg-config path is an explicit operator selection for this recorded host,
not a portable installation default. The builder pins Cargo.lock and uses
`--locked --offline`; it rejects other SDL versions or a dirty/wrong source head.
No consumer library or emulator installation is performed. The generated Cargo
manifest contains the operator's checkout paths only in the external scratch
folder, never in published fixtures.

From the research checkout, invoke the executable with the probe-source directory
and, for SDL, the compiled helper:

```sh
/tmp/wii-w1-build/target/debug/wii-w1-host-probe numeric bluetooth "$PWD/tools/wii_w1"
/tmp/wii-w1-build/target/debug/wii-w1-host-probe numeric uinput "$PWD/tools/wii_w1"
/tmp/wii-w1-build/target/debug/wii-w1-host-probe sdl bluetooth "$PWD/tools/wii_w1" /tmp/wii-w1-build/sdl_probe
W1_ENUMERATE_ALL=1 /tmp/wii-w1-build/target/debug/wii-w1-host-probe sdl bluetooth "$PWD/tools/wii_w1" /tmp/wii-w1-build/sdl_probe
/tmp/wii-w1-build/target/debug/wii-w1-host-probe dolphin bluetooth "$PWD/tools/wii_w1"
```

Association matching uses the exact creation-owned physical label and sysfs
ancestry, never only the display name. SDL results include only paths owned by
that creation. The generic SDL core evdev fallback is distinguished from HIDAPI.
Both SDL runs explicitly set HIDAPI=1, HIDAPI_WII=1, WII_PLAYER_LED=1 and
ALLOW_BACKGROUND_EVENTS=1. The second also sets
HIDAPI_ENUMERATE_ONLY_CONTROLLERS=0. No kernel driver is unbound.

Numeric phases are core, Nunchuk, Classic and standalone MotionPlus. After node
opening, each phase sends neutral for400ms, explicit test values until1400ms,
then neutral. The child reads for2 seconds and strips event times before output.
It records EVIOCGABS minimum, maximum, fuzz, flat and resolution, unique input
events, and the final ABS values. These ioctl/event layouts are scoped to the
recorded Linux aarch64 ABI. No calibrated defaults, firmware clock, physical
sensor fidelity or first-neutral timing oracle is inferred.

Dolphin runs offscreen with a new private profile inside its existing Flatpak
sandbox. It checks access to the exact owned hidraw path inside that sandbox,
configures slot1 as Real Wii Remote, continuous scanning and controller-interface
connection, and disables speaker output. It logs only the fresh run and is
terminated after14 seconds (with a bounded kill fallback). No ROM or physical
Wii Remote is used. Startup, enumeration, successful connection, initialization,
and gameplay acceptance are separate states; lack of output cannot prove a
successful backend connection. Do not publish raw application logs or identities.

The executable closes its controller idempotently, verifies owned-node removal
and compares its fd count before creation and after dropping the handle. Numeric
neutral transitions are observable but are not a first-valid-neutral oracle at
creation: unchanged core buttons produce no evdev edge, and the probe opens
consumer nodes after initialization.

Publication uses reviewed JSON summaries under fixtures/acceptance and retains
original local artifact hashes. Host paths, process identities, event times and
raw application logs are excluded. The record describes the exact transform.

## Human-granted follow-up

The granted rerun uses merged Part A
`78e667369d57fc3175e4dabd8b13e221f2035ad5`. Build with the same arguments using
`tools/wii_w1/build_granted.py`, then invoke the binary with a private scratch output directory and
its SDL helper executable as two arguments. It holds one exact creation-owned
Original Remote for at most two hours, pumping the controller while waiting.
`grant.json` is private operator metadata, never a publication fixture.

The operator first checks HID_PHYS against the creation association, Bluetooth
VID/PID, wiimote binding, hidraw sysfs ancestry and all four LED files beneath
that exact owned HID root. Supply commands only for that hidraw node and four
LED brightness files. Anders applies the temporary grants himself and confirms;
the agent verifies identity and access again before creating `go` in the private
output directory. This authorization is recorded on virtualgamepad#176 comments
6347519179 and6353166649. The helper never grants access or changes host policy.
No new device is created after the grant, no driver is unbound, and no override
is added to Flatpak.

The helper writes1 to the four LEDs, services100ms and records retained LED
intent. It runs the same two SDL cases and bounded Dolphin configuration above
on that held device, with core/Nunchuk/Classic/standalone MotionPlus phases.
`runs-complete` signals the end of the bounded probes; creating `done` closes
idempotently and verifies the owned HID root disappeared. Existing ungranted
records stay unchanged. Publication omits raw logs and grant metadata; it retains
parsed observations and hashes of the private originals. The published source
replaces the original scratch SDL executable path with the second argument;
source and measured executable hashes remain separate. The helper's4-second
attachment phases and application timeouts are probe schedules, not firmware
cadence or latency acceptance. A passed LED result concerns virtual software
intent only. SDL hidraw access is distinct from Wii HIDAPI claiming, and Dolphin
sandbox access is distinct from backend connection, initialization and gameplay.
