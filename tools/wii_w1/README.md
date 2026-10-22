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
