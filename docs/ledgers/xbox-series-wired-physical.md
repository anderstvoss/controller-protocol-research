# Xbox Series wired reference on Linux xpad

One USB `045e:0b12` reference on Linux
`7.3.0-1-mainline` x86_64 with stock `xpad` and evtest 1.36. USB
`bcdDevice` was `5.17` and the evdev input version was `0x0517`.
The exact model label and installed firmware are unconfirmed.

## Inputs and USB reconnect

The physical input name, bus/vendor/product/input version, 12 key codes,
eight axis codes, ranges and flat values matched the
[C9 virtual evdev definition](https://github.com/anderstvoss/virtualgamepad/tree/69c2283/crates/gr-curated-controllers/src/xbox_series).
Stick fuzz was 16 on physical xpad and 0 on C9 uinput. The sweep observed all
button presses and releases, including Guide as `BTN_MODE` and Share as
`KEY_RECORD`, all eight D-pad directions and center, full signed travel on
all four stick axes, and both triggers at 0 and 1023. Up to four buttons
were held together, with axis changes during key holds. The triggers and
hat returned to zero. Released physical sticks retained small nonzero
samples.

Unplugging removed the original input object. Replugging yielded the same
USB descriptor hash and evdev identity. The first evtest open preceded the
active-seat ACL and returned permission denied. An ordinary-user retry
captured A, Guide and Share presses and releases on the replacement node.
The [sweep](../../fixtures/xsphys-xpad-sweep.json) and
[reconnect](../../fixtures/xsphys-xpad-reconnect.json) fixtures
contain 799 and 22 completed frames respectively, with zero dropped frames.
The fixtures retain numeric input events and public capabilities. Raw
captures and wall-clock event timestamps stay private.

## Wired outputs

| Surface | Observation |
| --- | --- |
| Main rumble | Two evdev `FF_RUMBLE` effects requested strong-only then weak-only, each for 450 ms at magnitude 32768 of 65535. The kernel accepted each upload, play, stop and erase. The operator felt both pulses. The test measured tactile response to each command. Independent trigger motors and motor isolation were outside the test. |
| Guide LED | No LED class device or evdev `EV_LED` capability belonged to the controller. The ordinary user lacked raw USB write access. Direct actuation remains untested. [Microsoft specifies the Guide LED command](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-gipusb/ec312389-2e05-4915-85ed-0e8fe9c3d33b). |
| Headset audio | A 3.5 mm headset was plugged into the controller. Interface 1 remained unbound at alternate setting 0. Linux exposed no associated ALSA sound node or Pulse-compatible card, sink, or source. No endpoint was available for a playback or microphone test. The result is scoped to stock `xpad`. |

The USB descriptors showed three vendor-specific interfaces. Interface 0
bound to `xpad`; its active interrupt endpoints were `0x02` and `0x82`.
Interface 1 alternate setting 1 advertised isochronous endpoints. GIP audio
negotiation and PCM, direct LED commands, raw USB packets and Bluetooth
remain open.

## xone headset follow-up

After reboot the driver lab socket was active. The physical wired controller
bound to xone 0.5.8. With only the transport and GIP core loaded, there was no
headset PCM. Loading the gamepad and headset modules and reconnecting the
controller over USB produced distinct gamepad and headset clients and enabled
interface 1 alternate setting 1. Rebinding alone had left only the adapter
visible in the initial run.

The associated ALSA headset exposed S16_LE, 48 kHz stereo playback and
24 kHz mono capture, with 8–16 ms hardware periods. The operator heard the
left and right playback markers. An initial capture overran when the probe
deferred draining its pipe. With concurrent draining, the five-second repeat
captured all 120,000 microphone frames with no reported xrun. One-second
microphone RMS rose from 33.3 to 509.5 during the response interval and
returned near baseline. No recorded PCM was saved. This is a bounded physical
full-duplex result. Sustained streaming, explicit headset jack hotplug
recovery, PipeWire routing and a native virtual GIP transport still need tests.

The xone gamepad also exposed a white status LED node. The caller had
read access only, so host-controlled brightness remains unverified.

## Corroboration and installed revision

The bounded xone headset result corroborates the consumer path in
`xbox-xone-gip-headset` from research #123. The observed white status LED
node corroborates the LED publication portion of
`xbox-xone-led-battery-power`. Brightness writes, battery reporting and
power-state timing remain untested. The installed xone module reported
0.5.8. Its precise source revision is unknown, so the physical result is
not attributed to the f2aa9fe source revision pinned by #123.
