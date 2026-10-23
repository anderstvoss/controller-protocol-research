# W3 unchanged-model diagnosis

Original tools under this repository's tooling license; no upstream source is
copied. Requires already-prepared Linux6.12 aarch64, UHID/event access, cached
Rust dependencies, a C compiler and distro SDL3.2.10+ds-1. Installs nothing and
performs no grants, root operation, unbind or persistent host-policy change.

Build on a clean baseline checkout atb23fd2570069c59e4815f66329fe78ab7b87ad3c:

```sh
python3 tools/wii_w3/build.py --case baseline --virtualgamepad ../virtualgamepad \
  --output /tmp/wii-w3-build \
  --sdl-pkg-config-path /usr/lib/aarch64-linux-gnu/pkgconfig:/usr/share/pkgconfig
LD_PRELOAD=/tmp/wii-w3-build/trace.so W3_TRACE=/tmp/wii-w3-owned-private.jsonl \
  /tmp/wii-w3-build/target/debug/wii-w2-host-probe \
  /tmp/wii-w3-private /tmp/wii-w3-build/sdl_probe \
  b23fd2570069c59e4815f66329fe78ab7b87ad3c
```

The executable package name is retained from the original probe manifest; its
W3 source and binary hashes identify the actual measured tool. The builder uses
locked/offline Cargo and rejects another source head or dirty checkout. The
pkg-config path is an explicit recorded-host selection, not a portable default.

The helper holds one exact-owned Original bus5:057e:0306 device for at most two
hours while pumping. Private grant.json contains identity metadata, never a
published fixture. Verify creation HID_PHYS, canonical virtual UHID ancestry,
wiimote driver, raw-parent relationship and all four LED files under that root.
Send temporary per-node commands **locally in chat** for Anders to run; after
his confirmation reverify identity/access and create `go`. The helper never
changes permissions. At `runs-complete`, create `done`; it closes idempotently
and checks parent removal. The operator separately verifies raw disappearance.

Three27-second child profiles run on the same held device:

1. Wii-enabled hints with dirty-only application commits (the previous schedule).
2. Actual-default SDL hints with repeated explicit application commits.
3. Wii-enabled hints with repeated explicit application commits.

Inherited SDL_* variables are removed. Wii profile sets HIDAPI/WII/playerLED/
background1; no enumerate-all override. Explicit commits are an experimental
application-driven control, never an asserted device cadence or production fix.
Six4-second phases are core, Nunchuk attach, Nunchuk detach, MotionPlus attach,
MP attached with manual deactivation, and MP detach, each with300ms kernel
service. The C helper sends one owned A400F055 write at18seconds. Activation and
reprobe traffic also comes from the bound kernel driver. Actual packets, not
phase labels alone, establish activation/deactivation observations. Last phase
coverage is bounded by child exit. All output summaries filter exact owned paths.

trace.c interposes successful own-process read/write calls only on /dev/uhid,
records OUTPUT and INPUT2 frames and monotonic nanoseconds, and preserves errno.
CREATE/identifying events are excluded. These are virtual syscall-boundary
observations; accepted writes are not physical or individual-consumer delivery.
Host-output aggregates kernel, SDL and the explicit raw probe; it does not prove
an actor for every packet. Phase markers use10ms-quantized uptime after300ms
service; report timestamps use CLOCK_MONOTONIC. Raw debug logs/identities stay
private. analyze.py selects requested host reports, status/read/ACK responses and
first DATA after status/mode, retaining full report counts and relative times.

The resulting diagnosis is host-side extension reinitialization consistent with
pinned SDL HandleStatus1350–1384. Both Wii controls disconnect despite prompt
mode reselection/resumed DATA, while default evdev stays connected. No model fix,
firmware-clock workaround, sustained HIDAPI or reopening claim is made.

N1 attribution uses privately inspected sysfs names/phys/USB ancestry and retained
udev initialization time. Only nonmatching ownership, three class roles and a
relative time with uncertainty are published. No real input data, identities or
hardware capture is published. Historical W2 N1 stays blocked; no replacement
run or harness ordering change is made.
