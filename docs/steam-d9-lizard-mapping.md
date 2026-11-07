# D9 wired desktop mapping

This is physical observation of the wired Steam Controller 2026, not firmware
analysis. The owner ran passive full-snaplen USB captures with `hid-steam` bound
and its lizard-mode parameter enabled. Other consumers were closed except during
the normal SDL open/update/close interval. Raw captures remain private.
Firmware build was not independently re-read in each action session.

## Observed controls

| Native control | Desktop report field |
| --- | --- |
| Right pad X / Y movement | Mouse 0x40 relative X / inverted Y |
| Right pad click or right-trigger button bit | Mouse Button 1 |
| Left-trigger button bit | Mouse Button 2 |
| Left pad X / Y movement | Consumer usage 0x0238 / inverted wheel |
| A | Keyboard 0x41 usage 0x28 (Enter) |
| B or Options/Menu | Usage 0x29 (Escape) |
| View | Usage 0x2b (Tab) |
| D-pad Up / Down / Left / Right | Usages 0x52 / 0x51 / 0x50 / 0x4f |

Each prompted key produced press and release reports. X/Y, QAM, Steam, rear
buttons, shoulders, stick clicks/travel/touch, light pad touch alone, left-pad
click and grip contact produced no desktop reports in their labelled windows.
This absence is bounded to the actions tested. Native reports confirmed actions;
it is not a claim that arbitrary firmware configuration can never map them.

Full-trigger holds repeated identical mouse-button reports about every 4 ms.
A pure changed-wire-only emission rule is therefore not established. Trigger
mouse transitions track the already-present native trigger button bits; there
is no need to infer an analogue threshold for semantic-state emulation.

Slow interior strokes support approximate scales of 128 native units per mouse
count and 1024 per scroll count. These are compatibility fits. Exact retail
filtering, clipping, fractional phase, rounding and scheduling are unverified.
The owner found slow movement difficult and uneven. The first right-pad
horizontal center window contains early movement and is not stationary evidence.
No constant-speed or calibrated-distance assumption is made.

## SDL and reconnect

Normal SDL 3.5.0, source e0232c5, wrote setting 9 = 0 seventeen times, about three
seconds apart. Right-pad mouse completions before/during/after were 773/0/718.
A still produced three Enter presses and three releases in **each** window.
Setting 9 alone did not disable keyboard mappings. No setting 71 or mapping-clear
0x81 was observed in this interval. At close, successful empty 0x85 and 0x8e
writes preceded resumed mouse output. This is kernel restoration at last raw
close, not evidence of an autonomous firmware watchdog.

The first pad capture omitted the requested reconnect. Its action observations
remain valid for the existing state. A separate hands-off reconnect captured
USB enumeration and successful 0xae, 0x83, 0x85 and 0x8e writes. Approximately
46.2 seconds of post-enumeration traffic contained 11,468 native 0x42 reports,
13 opaque 0x43 reports (payloads withheld), and no mouse or keyboard reports.
Hands-off silence does not show that desktop mode was disabled. This measures
USB/kernel attachment, not firmware power-on defaults.

## Publication boundary

`fixtures/steam-d9-lizard-desktop.hex` contains complete, unmodified selected
mouse (6 bytes) and keyboard (9 bytes) reports. Every field is descriptor-defined:
mouse buttons, reserved bits, signed relative axes; keyboard modifiers, reserved
byte and six key usages. Repeated payloads are deduplicated. Counts and labelled
windows are in `evidence/steam-d9-lizard-mapping.json`. No unknown feature reply,
string descriptor, transport header, serial, address, host path or absolute
clock is published. Capture drop counts were not supplied; zero loss is not
claimed. This is mapping correspondence, not universal desktop fidelity.
