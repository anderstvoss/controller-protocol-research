# W3: bounded SDL diagnosis and W2 N1 attribution

These observations use unchanged virtualgamepad main
`b23fd2570069c59e4815f66329fe78ab7b87ad3c`, the interim Game Pad descriptor,
Linux6.12.113+deb13-arm64 aarch64 and distro SDL3.2.10+ds-1. They are virtual
host observations, not physical controller evidence. One human-granted device
was held across all three profiles and then closed; its owned HID root and raw
node disappeared. No production protocol, report cadence or host policy changed.
The original reproducible tools and operator procedure are in
[tools/wii_w3](../tools/wii_w3/README.md).

## Source and observed sequence

The inherited SDL source record `wii-w1-sdl-3-2-10` pins commit
`877399b2b2cf21e67554ed9046410f268ce1d1b2`. Its
`src/joystick/hidapi/SDL_hidapi_wii.c` SHA256 is
`6e4693d2b165ec1fa8cbdeec988d3825890192e24db45f9bc2059f2f4c63f959`.
The upstream source was hash checked privately and is not copied here.

`HandleStatus` (1350–1384) first resets the button packet type, sending report
0x12. With MotionPlus inactive, a changed extension-presence bit then sets
`m_bDisconnected` to reinitialize. `HandleResponse` (1387–1433) also requests
reinitialization when MotionPlus sensor availability changes. `UpdateDevice`
(1511–1576) has a separate inactivity/read-error condition and disconnects for
either that condition or the reinitialization flag. Its input wait timeout is
three seconds, as retained by `wii-gap-sdl-constant-input-inactivity-timeout`.
The status-change path does not require an inactivity timeout. Prompt 0x12 and
DATA resume are also consistent with `wii-gap-wiibrew-status-20-resend`; no
change to that pause/resume contract or the deactivation records was made.

The timestamped trace shows a Nunchuk-connected status, a host mode-selection
report within milliseconds, then resumed DATA immediately after the mode
selection. Read-memory responses and success acknowledgements continue.
For example, in the Wii-enabled dirty-only application-commit profile:

| Relative to connected status | Direction | Report |
| --- | --- | --- |
| 0 ms | device input | 0x20, extension-connected bit set |
| +1.309 ms | host output | 0x12 mode selection |
| +1.321 ms | device input | 0x30 DATA |
| +2.505 ms | host output | 0x17 read A400FA |
| +2.539 ms | device input | 0x21 memory response |
| +3.906 ms | host output | 0x16 write A400F0=55 |
| +3.931 ms | device input | 0x22 success ACK |
| +5.265 ms | host output | 0x12 mode selection |
| +5.272 ms | device input | 0x30 DATA |

All three 27-second profiles cover core, Nunchuk attach/detach and MotionPlus
attach/manual deactivation/detach phases. The retained reports include status
requests, A400FA/A600FA reads, A600FE=04 activation and A400F0=55 deactivation,
with ACK/read/status responses. Phase labels alone are not activation evidence.

| Profile | Initial owned joystick | Later connection |
| --- | --- | --- |
| Wii enabled, dirty-only application commits | HIDAPI,6axes/26buttons; accel capability, no gyro | disconnects after Nunchuk attachment |
| Actual-default SDL, repeated explicit application commits | evdev core | stays connected throughout child snapshots |
| Wii enabled, repeated explicit application commits | HIDAPI,6axes/26buttons; accel capability, no gyro | disconnects after Nunchuk attachment |

Repeated explicit commits are an experimental application-driven control. They
do not assert a physical firmware clock or introduce periodic production reports.
The prompt mode reselection and DATA resume, extension debug observation and
same disconnect under this control support SDL's extension reinitialization
path. The run does not support an AwaitingMode DATA-pause deadlock as the cause.
This is an inference from pinned source and aggregate observations, not a unique
per-packet attribution to SDL. No model fix is warranted by this diagnosis.
Sustained HIDAPI reopening is **blocked**, and neither initial claim nor evdev
continuity establishes sustained extension/sensor/game acceptance.

The own-process tracer observes successful UHID read/write boundaries. Host
OUTPUT includes the kernel, SDL and the owned explicit raw probe; accepted
INPUT2 writes do not prove delivery to each consumer or physical delivery.
Report clocks are monotonic nanoseconds. Phase markers are 10 ms-quantized uptime
emitted after 300 ms service. The filtered fixture retains all requested reports,
first DATA after status/mode, full report counts, source/binary hashes and these
limits. Raw logs, local identities and upstream source remain private.

## Original W2 N1 global count

Private sysfs names/phys/ancestry and retained udev initialization time identify
three surviving class entries belonging to one unrelated external USB gamepad:
one input, one event and one joystick entry. Their parent is outside virtual
UHID and their physical association does not match the owned virtual device.
They explain the exact global26→29 delta. Clock conversion places initialization
18.530 seconds into the original 78.483-second W2 N1 window, with 1.1 seconds
uncertainty. Published evidence contains roles, relative times and ownership
booleans, not real device identity, physical paths or user input.

The new attribution experiment **passed**. The historical W2 N1 record remains
**blocked** as directed; its measurements are unchanged. No harness ordering
change or replacement timing run was made. N4's existing result is unchanged.

## Research adoption and remaining limits

The code PR pins research main `c380e6b5dc8d2fa0289deb5711a8858541a7ae03`,
including reviewed W2 and WiiBrew work. It adopts only bounded W2 default HID
enumeration/open and initial Wii-enabled HIDAPI claim, keeping sustained HIDAPI
WIP. WiiBrew packing corroboration adds source locators, no behavior. These W3
records do not promote any claim; the inherited inventory remains 102 Wii claims
with 7 unknowns. Existing C5/W1/W2 records and all wii-gap claims remain unchanged.
Dolphin, retail descriptor #238, speaker, radio, USB UHID production, ClassicPro,
BalanceBoard and physical acceptance remain outside this session.
