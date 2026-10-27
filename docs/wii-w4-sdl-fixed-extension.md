# W4: SDL consumer scope and fixed-extension acceptance

## Pinned source review

This is consumer evidence, not device fidelity, physical observation or a model
fix. All new records use `wii-w4-*`; historical W2/W3 and cloud `wii-gap-*`
records remain unchanged. Their experiment links are retained in the new claims.
The v1 claim schema has no `evidence_role` property. The explicit marker
`evidence_role: consumer` is stored in existing `applicability.scope`; no schema
migration or historical record rewrite is introduced.

SDL release3.2.10 is pinned at
`877399b2b2cf21e67554ed9046410f268ce1d1b2`. The Wii driver and generic HIDAPI
joystick source are independently hash checked and cited by file/line; no
upstream source or excerpts are redistributed.

- Wii `HandleStatus`1350–1384: while MotionPlus is inactive, changed extension
  presence sets the disconnect flag after resetting reporting mode.
- Wii `UpdateDevice`1512–1576: invokes generic joystick removal on that flag or
  the separate read-error/inactivity condition.
- Generic `HIDAPI_JoystickDisconnected`762–800: closes joystick state, removes
  its instance, reports removal and requests a rescan.
- Generic rescan1071–1149: an unchanged, still-enumerated standalone device is
  removed for zero joysticks only when its raw handle is also absent; the
  relevant predicate is1118–1119. New enumeration entries can be added, but an
  existing seen/open device does not take that path.
- Generic `JoystickClose`1626–1657 delegates to Wii `CloseJoystick`1579–1587;
  neither closes the raw device. Wii `FreeDevice`1589–1591 is empty.

Consequently this path leaves the raw device present/open and the joystick
absent. No automatic reattach is found under those conditions. Full SDL quit,
physical node removal, driver disabling/reinitialization and other recovery
paths are outside this claim. W2/W3's observed drop without reattach is
consistent with it. Real-controller behavior has not been tested.

## MotionPlus correction

The handoff's suggested distinction needs qualification. With MotionPlus active,
`HandleStatus` uses status/periodic-check handling instead of its direct
extension-bit disconnect branch. However, `HandleButtonData`1266–1305 checks
MotionPlus packet downstream-presence bits and sets the same disconnect flag
when the cached extension type disagrees. `HandleResponse`1387–1433 can also
set it when MotionPlus sensor availability changes.
`NeedsPeriodicMotionPlusCheck`430–443 distinguishes status-triggered checks
from ordinary periodic scheduling. MotionPlus-active hotplug is therefore not
established safe by this source path. Its separate claim explicitly retains the
disconnect behavior; no live optional hotplug acceptance is inferred.

## Newer source pins

The official latest release checked for this session is
[release3.4.18](https://github.com/libsdl-org/SDL/releases/tag/release-3.4.18),
commit `829a65d769d935c4852f8159e964312c0957260a`. Main is pinned separately at
`8adc0f98837db84fd24f17c339e59dcf36a17156`. Relevant Wii code is byte-identical
between these two pins (SHA256 recorded separately for each source); generic
files differ, so their close/removal/rescan paths were read separately.

Both retain Wii `HandleStatus`1352–1386, downstream-packet disconnect in
`HandleButtonData`1268–1307, sensor-availability disconnect in
`HandleResponse`1389–1435, `UpdateDevice`1514–1578 and non-closing Wii
callbacks1581–1593. Both generic files remove the joystick at810–848. The
still-open rescan predicate is1185–1186 in3.4.18 and1184–1185 in main;
generic joystick close is1703–1734 and1693–1724 respectively. No reattach fix
for this path was found. Neither newer runtime was installed or exercised.
These conclusions apply to the exact pins, not future SDL main.

## Bounded host procedure

The host experiment attaches each configuration before opening a fresh SDL
process, keeps attachment topology unchanged throughout the child, and drives
application inputs for a60-second observation window. Cases are none, Nunchuk,
Classic format01, MotionPlus, and MotionPlus with Nunchuk pass-through. Uses the
interim descriptor and existing SDL3.2.10+ds-1 runtime, explicit Wii hints and
default HID filtering. A retained HIDAPI raw-path claim, control/sensor variation,
player-index LED intent and no disconnect are distinct observations.

Fresh temporary grants are sent locally in chat, applied and confirmed by
Anders, then identity/access reverified before the run. Agent performs no grant,
root, unbind or persistent host-policy operation. Source inspection does not
promote host results. Reports and original tools will retain failures and
missing capabilities explicitly; no production model change is authorized by
this session without first reporting a discovered virtualgamepad bug on#158.

## Observed results and limits

All five exact-owned raw-path HIDAPI joysticks stayed connected for their full
60-second windows: zero disconnected polls and zero removal events. Core button
changes reached SDL in every case. Nunchuk/Classic/MotionPlus+Nunchuk had axis
variation; no-extension and MotionPlus-only have no driven stick/trigger source.
Core accelerometer variation was observed except Classic, for which SDL exposes
no accelerometer sensor. Secondary Nunchuk acceleration was not sampled.

| Fixed configuration | Claim held | Button / applicable axes | Core accel | Gyro | LED intent | Coverage disposition |
| --- | --- | --- | --- | --- | --- | --- |
| None | yes | yes / no axis source | varies | not applicable | observed | passed, bounded |
| Nunchuk | yes | yes / varies | varies | not applicable | observed | passed, bounded |
| Classic01 | yes | yes / varies | not advertised by SDL | not applicable | observed | passed, bounded |
| MotionPlus | yes | yes / no axis source | varies | advertised/enabled, remains zero | observed | blocked for gyro |
| MotionPlus+Nunchuk | yes | yes / varies | varies | advertised/enabled, remains zero | observed | blocked for gyro |

Every profile requested player index1 at open and index2 after30seconds, with
matching retained LED states. SDL's player-LED capability flag was false in every
case; the requests and observations are retained independently from that flag.
This demonstrates software intent, not physical light. Control extrema include
startup, repeated cached reads and concurrent kernel traffic; they establish
selected changes, not expected calibrated values or exhaustive button/axis maps.
Classic triggers, all native controls and secondary Nunchuk acceleration are not
independently accepted by this measurement. Source-valued inputs and observed
SDL extrema are not asserted to be calibrated or physically faithful.

The zero gyro result is retained even though capability/enable calls succeed.
It does not establish delivery, or isolate a virtualgamepad bug. On Linux,
SDL's `ActivateMotionPlusWithMode`455–467 delegates activation to the kernel;
SDL also initializes/resets extension state. The aggregate owned trace contains
activation plus deactivation/reprobe traffic from concurrent consumers. No
unique per-packet actor or causal gyro diagnosis is asserted. No workaround or
production change is made. Optional MotionPlus-active hotplug was not run.

The five profiles share one held kernel device but use separate SDL processes;
topology is fixed only within each child. Explicit application commits drive
inputs, not a new firmware clock. Owned HID and raw nodes disappeared after
idempotent close. Global counts, first-neutral/creation timings, physical or
newer-runtime acceptance were not measured. The source-only Wii inventory grows
102→105 with these three consumer claims; all seven unknowns and historical
W2/W3/wii-gap evidence remain unchanged.
