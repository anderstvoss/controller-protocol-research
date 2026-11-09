# Instrumented SDL Wii MotionPlus gyro on Linux

This follows virtualgamepad [#244](https://github.com/anderstvoss/virtualgamepad/issues/244)
and the earlier [W5 diagnosis](wii-w5-gyro-diagnosis.md). It directly observes
SDL's private MotionPlus state on Linux 7.3.0-1-mainline with the unchanged
virtualgamepad revision `74ff69b12283722bb3d40eb84935fdf926ea2259`.
Every arm uses an owned Bluetooth-bus UHID device and synthetic EEPROM and
extension calibration. The Remote Plus arm uses TR.

## Method

Each arm starts a fresh SDL process with Wii HIDAPI explicitly enabled. The
process selects the exact owned hidraw path and excludes the other test
product ID. The host owner grants temporary raw-node access. The kernel
`wiimote` driver and its battery interface are checked before the arm, and the
driver is checked again afterward. The MotionPlus evdev node is opened before
SDL initialization and held until SDL exits. The Original node is reused
across its four arms, with the profile fixed during each child. The TR node is
reused across its two arms. Kernel and raw state can carry across fresh SDL
processes.

The stimulus alternates the W5 raw pitch, roll and yaw triples every 250 ms.
The probe polls SDL and counts actual gamepad gyro events separately from
kernel ABS_RX, ABS_RY and ABS_RZ. The post-open polling window is 26 seconds,
including time after a removal. Kernel counts in the table are from this
window. Logged kernel extrema also include the pre-open holder period.
Application servicing and polling timings are local harness settings.

Logging-only builds record SDL writes and input responses during private
`HIDAPI_DriverWii_InitDevice` and `HIDAPI_DriverWii_OpenJoystick`, cached
`m_bMotionPlusPresent` and `m_ucMotionPlusMode`, the Linux activation branch,
and the decode decisions. For each dispatch, the trace counts absent cached
mode, short payload, invalid marker, downstream packet, disabled sensors, or
entry into gyro decode as applicable. A separate process-level trace records
exact-owned hidraw and aggregate UHID traffic. Register read responses carry
a low offset only. An interleaved `00fa` response does not uniquely identify
the bank or the requesting client. The probe issues no extra register
requests. An aggregate write with ambiguous or absent SDL attribution stays
ambiguous or kernel-or-untraced.

The local patch, binaries, full traces and harness are outside the corpus.
Fixture provenance distinguishes the upstream source, patched source, patch,
library and harness hashes. The public fixtures retain semantic protocol
transactions, cached transitions and dispatch counts with relative times.
Logging and scheduler timing can affect the shared response race. No physical
Remote, Bluetooth radio link, calibration accuracy, or gameplay was tested.

## Pinned source

Both versions place `ReadRegister`, `ParseExtensionIdentifyResponse`,
`SendExtensionReset`, `GetMotionPlusState`, and `ActivateMotionPlusWithMode`
at the same line numbers. `ReadRegister` waits for the report type in its
synchronous path, while the extension parser subsequently checks offset and
length. The Linux activation branch leaves mapping to the kernel without
assigning the requested mode. Open initializes the extension before querying
the active mode and presence. The decoder checks cached mode before examining
an extension payload. Periodic detection can flag an availability change
without assigning the newly observed mode.

- [SDL 3.2.10 register synchronization and activation](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L284-L468),
  [initialization and open](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L677-L799),
  [dispatch and availability](https://github.com/libsdl-org/SDL/blob/877399b2b2cf21e67554ed9046410f268ce1d1b2/src/joystick/hidapi/SDL_hidapi_wii.c#L1266-L1435).
- [SDL 3.4.20 register synchronization and activation](https://github.com/libsdl-org/SDL/blob/f00dc919ca35b9756316e86c4777392de442f9b2/src/joystick/hidapi/SDL_hidapi_wii.c#L284-L468),
  [initialization and open](https://github.com/libsdl-org/SDL/blob/f00dc919ca35b9756316e86c4777392de442f9b2/src/joystick/hidapi/SDL_hidapi_wii.c#L679-L801),
  [dispatch and availability](https://github.com/libsdl-org/SDL/blob/f00dc919ca35b9756316e86c4777392de442f9b2/src/joystick/hidapi/SDL_hidapi_wii.c#L1268-L1437).

## Results

| Virtual profile | SDL | SDL gyro events | SDL disconnected polls | Kernel events per gyro axis | Expected gyro reports read by SDL |
| --- | --- | ---: | ---: | ---: | ---: |
| Original + MotionPlus | 3.2.10 | 0 | 5044 / 5051 | 3 | 0 |
| Original + MotionPlus | 3.4.20 | 0 | 3491 / 5037 | 11 | 4 |
| Original + MotionPlus + Nunchuk | 3.2.10 | 0 | 5035 / 5042 | 20 | 0 |
| Original + MotionPlus + Nunchuk | 3.4.20 | 0 | 5030 / 5037 | 106 | 0 |
| Remote Plus (TR) | 3.2.10 | 0 | 5041 / 5048 | 28 | 0 |
| Remote Plus (TR) | 3.4.20 | 0 | 5035 / 5042 | 36 | 0 |
| Original + MotionPlus + Nunchuk, late holder | 3.4.20 | 0 | 2602 / 2902 | 55 | 0 |

All six primary arms opened the expected SDL HIDAPI joystick and gamepad.
Each recorded a private cached presence of false and mode `0x00` from
initialization to removal. Each read active identity during initialization,
then requested `A400F0 = 0x55` and logged the Linux activation bypass
with desired mode `0x04` or `0x05`. Each OpenJoystick issued a second
`A400F0 = 0x55` reset, followed by the extension state query. None advertised
gyro or enabled it, and each recorded a removal.

The host trace contains aggregate `A400FA` reads alongside the instrumented
SDL `A400FE` and `A600FE` requests. For example, the Original MotionPlus
3.2.10 arm received a reply at `0x00fa` while waiting for the `A600FE`
read. The read helper accepted the reply type, then the extension parser
rejected its offset. This is evidence of an interleaved reply, with no
unique bank attribution from the response itself.

**The cached-mode gate is confirmed for received reports.** In the Original
MotionPlus 3.4.20 arm, SDL's hidraw handle actually read four six-byte
gyro payloads with the expected moving vector and slow flags. Its packet
dispatch logged all four at the mode-NONE skip, before the sensor-enabled
check. Later, periodic identification read `0x0405` (active mode `0x04`)
while the cache still held false and `0x00`, and SDL removed the joystick.
This reproduces the Linux reset/bypass mechanism on both source revisions
and directly confirms its decode effect in the 3.4.20 arm. The other five
primary arms removed the device before SDL read an expected gyro vector
during drive. Readback and disconnect timing therefore also contribute to
the zero-event result. The TR runs establish the failed SDL path and
changing kernel gyro in this configuration, with SDL delivery still
unestablished.

The late-holder comparison used a fresh 3.4.20 process on the same
MotionPlus + Nunchuk device. It opened the kernel MotionPlus fd 1.5 seconds
into a 15-second drive window. SDL still started with no advertised gyro,
then removed the joystick after the holder opened. Its dispatch logged
some extension bytes with the gyro marker pattern, but the independent
hidraw decoder found none matching the driven vectors. The marker alone
does not establish a gyro packet while the extension mode is unresolved.

Both owned HID and hidraw nodes disappeared after two close calls. An
earlier setup attempt ended before SDL initialization when the Original
detach/re-attach step removed its kernel MotionPlus event node. The
recorded arms used a recreated Original and kept the accessory attached
before each child.

## Acceptance note for `sdl-hidapi-wii-gyro`

Keep the bounded consumer limitation on `linux.uhid.bluetooth`. Supplement
the W5 source inference with the directly observed cached state, Linux
activation bypass, interleaved readbacks and the four valid reports
skipped in SDL 3.4.20. Add the TR result as an early disconnect with no
advertised gyro. Linux 7.3 and both logging-only SDL builds are a new host
tuple. These results establish neither a sustained enabled SDL gyro
stream nor a conclusion about physical Wii Remotes.
