# W2 bounded descriptor comparison

Original probes under the repository tooling license. No upstream descriptor or
consumer source is copied. Requires the same already-prepared Linux6.12 aarch64
host as W1, existing UHID/event access and Debian SDL3.2.10+ds-1. Installs nothing,
uses no root, changes no policy and never unbinds a driver. Dolphin is not run.

Build separately against clean before/after checkouts (main56fc3f6 and code07e42cb):

```sh
python3 tools/wii_w2/build.py --case after --virtualgamepad ../virtualgamepad \
  --output /tmp/wii-w2-after \
  --sdl-pkg-config-path /usr/lib/aarch64-linux-gnu/pkgconfig:/usr/share/pkgconfig
```

Use `--case before` and a different output directory for the baseline. The
pkg-config path selects the recorded distro installation, not a portable default.
Cargo dependencies are locked/offline; the builder rejects another revision or
dirty checkout. Generated manifests hold operator paths only in private scratch.

Invoke each binary with its private output directory, compiled SDL helper and
full source revision as three arguments. The helper holds one exact Original
bus5:057e:0306 device, pumping it for at most two hours. Before publishing grants,
verify creation HID_PHYS, canonical virtual UHID root, wiimote binding, raw-parent
ancestry and all four LED paths under that root. Never publish `grant.json`, raw
application logs or device paths as research fixtures. Anders applies grants
himself only to the held hidraw node and four brightness files, as directed by
virtualgamepad#1766347519179 and W2#1586354044408. Reverify identity/access after
his confirmation, then create `go`; the helper performs no grant itself.

Both original descriptor cases are held for one human grant round. The helper's
SDL observations include only exact owned raw/core paths even though SDL may
internally enumerate other virtual devices. Each case runs two child profiles:

- `sdl-default-hints`: removes inherited SDL_* environment, sets no SDL hints.
- `sdl-wii-enabled`: same clean environment, explicitly enables HIDAPI, WII,
  WII_PLAYER_LED and background events, retains default controller-only HID
  enumeration. No enumerate-all override is used in either case.

Direct O_RDWR, owned HID enumeration/open and actual joystick backend are distinct
observations. The opened joystick must match the owned hidraw path to count as
HIDAPI; an event-path joystick is evdev. No discovery result alone proves claim,
init, sensor delivery, physical fidelity or game acceptance. Both12-second child
windows attempt core/Nunchuk/Classic/standalone-MP4-second phases; final phase may
be entered at child exit. Owned kernel names/key/axis masks are sampled after a
300ms phase service. The helper also records granted LED writes/retained intent.

`runs-complete` ends bounded probes; create `done` to close idempotently. Parent
HID removal is asserted; post-run raw disappearance is separately checked by the
operator. No first-neutral timestamp or fd count is measured by this helper.

After both held devices close, build/copy xtask on clean PR head07e42cb and run
its unchanged acceptance command for Bluetooth-bus UHID,10 cycles each at N1/N4.
Use the same executable for both. The first cycle is cold, later cycles warm;
missing consumer-open/first-neutral/SDL stages remain explicit. The harness does
not inherit per-node grants for its fresh devices. Compare historical C5#17 as
separate observations, never relabel its distributions or claim a timing budget.
Only sanitized structured summaries, hashes and source revisions are published.
