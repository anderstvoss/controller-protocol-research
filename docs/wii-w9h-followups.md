# Wii W9h: copy isolation, Classic and independent Plus qualification

Runtime is virtualgamepad 74e5fab1ef05ea695cc6a59f341242da875a8fe0,
W9h citation-only PR #267, with executable codec text unchanged from main
cd052cd after comments/whitespace are removed. No model, codec, API or descriptor
behavior was changed for these runs. Research starts from merged main c92438d,
after #65/#66, with 225 Wii claims; five consumer claims bring the total to 230.

| Arm | Mode and result | First unpassed checkpoint |
| --- | --- | --- |
| Kernel Tr MP+Nunchuk | 05, changing evdev and xwiimote gyro | None through required gyro and first-18-second reinitialisation gate |
| Original MP+Nunchuk copy-off | 05, gyro and Nunchuk buttons respond, stick stays centered | Child 0x40/16 calibration: error 7 |
| Original MP+Classic | 07, changing gyro, both sticks and selected A/B buttons | None through those bounded decoded controls |
| Tr MP+Nunchuk default ID | 05, independent decoded gyro and stick pass | None through bounded decoded gyro/stick |
| Tr MP+Nunchuk external-style ID | 05, same decoded controls pass | None through bounded decoded gyro/stick |

All generic arms use native Dolphin 2503, fresh isolated emulated
ControllerInterface profiles, zero Real slots, no content/radio, gyro calibration
period 0 and correct signed X/Y stick input names. The owner alone ran a
2.064523-second ignore-special creation window, restored/read back 0, and
verified/granted four exact virtual devices. The agent revalidated identity,
hidraw linkage, generic binding and access before consumers. The observation
guard is an aid, not a complete sandbox. Generic binding is test/dev only;
#258 still gates release use. No agent sudo or persistent policy change.

The kernel gate is a 22-second concurrent evtest/xwiimote capture for Tr with
wiimote/gen20 binding, default built-in inactive identity and re-attach on. It
has two driven values on each gyro axis and 93 xwiimote MotionPlus events.
No A400F0/A600F0 re-initialisation occurs in the first 18 seconds after mapping;
the first such writes occur during reader-close cleanup after 22.2 seconds.
The owned raw tap observes the unplugged/plugged activation edge. This is not
physical timing, calibration or complete child-controls acceptance.

Copy-off isolates one flag: re-attach/F6 remain on and all imported blocks
match the W9g on arm. It re-sends report mode, reads F6 and MP 0x20/32, then gets
8928 error 7 replies to child 0x40/16. Gyro still changes and Nunchuk buttons
respond, while the correctly bound stick stays centered. Compared with the
published copied-block W9g on pass, this isolates copy necessity for the decoded
Original Nunchuk stick on this native path. It does not prove a gyro requirement,
a refusal of all child controls, or copy necessity for Classic or Plus.

Classic mode 07 re-sends 0x12 and successfully reads F6, MP 0x20/32 and child
0x40/16. The Classic block is synthetic caller data derived from the hash-verified
pinned Dolphin emulator constants and checksum layout, not retail data. Its
SHA256 is 0004980225a9ff9cb8aad02512d856f14e4b9ce9b77e50ecc4c643e0b2d99a09.
Both sticks move between the driven positions and selected A/B highlights
alternate; gyro changes in independent owned-window samples. Other buttons
and triggers are not separately qualified. No consumer workaround was used.

Plus default/external arms are separate Tr PID 0330 devices; no Original pass
is inherited. The default source policy uses A4200005, external-style uses
A6200005. These are configured source identities, not a claim that Dolphin
read the entire inactive identity. Both arms read F6 and exact imported MP and
child calibration and display changing gyro/stick, so the external-style
option is not shown necessary for this consumer. Each creation flag remains
immutable for its device.

An initial default Plus run passed transport and gyro but both saved stick
images hit the same stimulus phase. Its changing-stick observation is unavailable
and its archive is retained separately. A fresh 180-second repeat uses dense
owned-window sampling, capturing opposite decoded stick positions before PNG
conversion, with separate motion samples. Only that fully observed repeat
supplies complete Plus stick acceptance and the counts below. The external-style
control started only after the default repeat passed.

| Final generic arm | Post-map MP / child frames over 180 seconds |
| --- | --- |
| Copy-off | 8946 / 8946 |
| Classic | 4483 / 4483 |
| Default Plus repeat | 4484 / 4483 |
| External-style Plus | 4483 / 4483 |

Pre-map report 0x37 frames are excluded. Rate denominators are the full consumer
bound including setup; repeated reads can produce more raw reports. Counts
are not guaranteed rates, timing acceptance or a decoded oracle. Independent
owned-window observations establish decoded controls. Native post-map
A400F0=55 and A600F0=55 are zero in all four generic arms.

All consumers and five virtual devices were closed idempotently. Kernel HID,
hidraw and LED disappearance was verified; generic devices never created Wii
input/LED nodes, and their HID/raw disappearance was verified. No physical,
radio, game, release, whole-controller or calibrated-rate acceptance follows.
Adoption remains a separate code PR and can promote only the observed bounded
controls and the isolated Original copy requirement, with these preconditions.
