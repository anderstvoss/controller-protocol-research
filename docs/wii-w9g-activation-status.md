# Wii W9g: activation status compatibility and consumer gates

Runtime: virtualgamepad 7445bfa88466f7c519a25d9b0341fc5b59957854,
Part 1 PR #264. Follow-up f918725 changes tests only. Original revision,
Bluetooth UHID metadata, imported synthetic caller EEPROM and extension blocks.
No factory calibration, physical device, radio, game, Cemu or Plus qualification.
The default-on activation re-attach status option remains **compat**.
WiiBrew's pair is documented for deactivation only; `wii-gap-mpstatus-*`
research will decide activation classification or retirement.

| Arm | Binding and options | Outcome / first unpassed checkpoint |
| --- | --- | --- |
| Kernel MP-only | wiimote, re-attach and shims on | Changing evdev and xwiimote gyro; mode 04, single activation status |
| Kernel MP+Nunchuk | wiimote, re-attach and shims on | Changing evdev and xwiimote gyro; mode 05, unplugged/plugged activation edge |
| Dolphin MP+Nunchuk on | hid-generic, re-attach and shims on | Bounded decoded gyro and Nunchuk stick pass; 0x12 re-sent, F6 and both calibration blocks succeed |
| Dolphin re-attach off | hid-generic, both register shims on | No post-map 0x12 resend, no F6 read, no post-map MP or child frames |
| Dolphin F6 mirror off | hid-generic, re-attach and calibration copy on | 0x12 re-sent, F6 error 7 repeated; no calibration reads or changing decoded gyro/stick despite raw frames |

The generic binding is **test/dev only**: hid-wiimote is not bound and #258
still gates release use. The owner ran the 2.048141-second creation window,
restored/read back 0, then verified the exact devices and granted hidraw access.
The agent rechecked identity/linkage/binding/access. No agent sudo, persistent
rule, blacklist, driver manipulation, package or debug-setting change.

Each bound capture runs evtest and xwiimote concurrently for 18 seconds, with a
read-only exact-owned raw status tap. All three gyro axes have two driven values;
each xwiimote run has 76 MotionPlus events. In the first 18 seconds after mapping,
neither A400F0=55 nor A600F0=55 occurs. The first writes occur at reader-close
cleanup, after 18.24 seconds. This does not claim kernel decoded child acceptance
or activation fidelity. The producer's elapsed field continued advancing after
finish-phase, so counts are retained without inferring a commit rate from it.

Native Dolphin 2503 uses fresh isolated emulated ControllerInterface profiles,
zero Real slots, no game content, and gyro calibration period 0. An observation
guard blocks foreign raw/input/USB and Bluetooth radio access; it is not a
complete sandbox. Owned-profile children are gone before the next arm.

An initial private profile used nonexistent directional Nunchuk stick input
names. Its gyro and buttons moved but its stick stayed unbound. The native 2503
source record `wii-w8-dolphin-2503-input` names signed X/Y inputs. The profile
was corrected to X+/X-/Y+/Y- and rerun fresh. Only the corrected 180-second arm
supports stick acceptance; the preliminary artifact is preserved and separately
hashed, not mixed into its frame counts. No upstream excerpts are reproduced.

The corrected on arm receives 4480 MP and 4479 child frames **after** mode 05.
Dividing by the full 180-second consumer bound, including setup, gives
24.888889 and 24.883333 frames per second. Pre-map report 0x37 frames are excluded.
F6 returns the child identity with fixed compat F7 0x02. The MP 0x20/32 reply and
child 0x40/16 reply match the imported blocks exactly. Independent owned-window
samples show changing decoded gyro and Nunchuk stick, plus acceleration and IR.
Buttons are not separately qualified in the corrected arm.

The mirror-off control receives 8947 MP and 8946 child raw frames and 8934 F6
error replies. More raw frames under repeated host reads do not prove decoded
success or a guaranteed input rate. The mapping view stays stationary and neither
calibration read is reached. The re-attach-off control has zero post-map frames;
its gyro view is stationary, and its child view was not separately sampled.
Native post-map A400F0=55 is zero in all three generic arms. These results isolate
report-mode reselection and F6 identity gates without claiming physical fidelity.

All five consumers and all five virtual devices were closed; HID/raw/LED removal
was verified, and the generic devices never created kernel Wii input/LED nodes.
No adoption broadens the prior kernel-bound Dolphin MP+Nunchuk limitation.
