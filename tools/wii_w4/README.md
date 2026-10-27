# W4 fixed-extension consumer probe

Original local tooling under the repository tooling license. Uses the existing
SDL3.2.10+ds-1 installation and unchanged virtualgamepad main
`abb94e226f77eab24b391b24fd181e71daad421f`. No package installation, grants,
root operation, unbind or persistent policy. No physical controller input is
read. Paths and identity metadata in the operator's scratch directory are
private; publish only sanitized summaries and original artifact hashes.

```sh
python3 tools/wii_w4/build.py --case baseline --virtualgamepad ../virtualgamepad \
  --output /tmp/wii-w4-build \
  --sdl-pkg-config-path /usr/lib/aarch64-linux-gnu/pkgconfig:/usr/share/pkgconfig
LD_PRELOAD=/tmp/wii-w4-build/trace.so W3_TRACE=/tmp/wii-w4-owned-private.jsonl \
  /tmp/wii-w4-build/target/debug/wii-w2-host-probe \
  /tmp/wii-w4-private /tmp/wii-w4-build/sdl_probe \
  abb94e226f77eab24b391b24fd181e71daad421f
```

The package name and trace environment variable are retained from the earlier
original tools. The W4 sources and executable hashes identify the measured
versions. The builder uses locked/offline Cargo, rejects a dirty/wrong baseline
and selects the recorded distro SDL pkg-config directory explicitly. The
architecture-specific directory is a recorded-host selection, not a portable
default. The original W3 tracer is reused without copying upstream code.

When `grant.json` appears, independently verify the exact creation HID_PHYS,
canonical virtual UHID ancestry, bus5:057e:0306, wiimote binding, raw-node parent
and all four LED brightness files under that root. Send fresh guarded grants
locally in chat for Anders to run. Wait for confirmation; reverify identity and
read/write access before creating `go`. The helper performs no permission
change. Hold is bounded to two hours and continuously services the controller.
Never reuse paths after removal or expiry.

The five sequential profiles attach none, Nunchuk, Classic format01, MotionPlus
and MotionPlus+Nunchuk before opening a fresh SDL process. Two seconds of service
precede each process. No attachment topology changes while that child runs.
Every child clears inherited SDL_* environment; it enables HIDAPI, Wii, Wii
player LED and background events with default HID filtering, without enumerate-all.
Only an exact-owned raw path can be opened as the observed joystick. It polls
for60seconds after open, recording connection/removal, axis extrema, button
states, sensor capability/enable/sample extrema and own-instance event counts.
Classic acceleration omission is an SDL consumer restriction; it advertises
sensors only for no extension/Nunchuk (source OpenJoystick775–795).
No-extension/MotionPlus-only joystick axes have no driven stick/trigger source;
accelerometer and gyro measurements remain separate from joystick axes.

The application toggles core button and accelerometer inputs every250ms,
Nunchuk/Classic controls where present, and MotionPlus raw gyro values where
attached. It explicitly commits at an application-driven approximately20ms
interval while servicing kernel/SDL requests. This is a diagnostic input drive,
not a firmware-cadence assertion or production change. SDL sensor polling can
repeat cached values; event counts and extrema are reported separately and do
not establish physical calibration, sample rate or timing acceptance.

SDL sets player index1 at open and index2 after30seconds. The holder records
host_outputs transitions. Matching retained LED bits establishes software intent,
not visible light delivery or unique attribution of all concurrent kernel/SDL
traffic. The existing own-process tracer captures aggregate host OUTPUT and
accepted INPUT2 writes; it does not establish individual-consumer delivery.

At `runs-complete`, write `done`; helper closes twice and asserts owned HID root
disappearance. Separately check owned raw disappearance. No global resource
restoration or creation/first-neutral timing is measured. Optional MotionPlus
active hotplug is outside these fixed-topology profiles. No newer SDL build is
installed or exercised. `analyze.py` keeps claim-held separate from complete
control/sensor/LED coverage and blocks incomplete windows or any disconnection.
