# Xbox Series: xone GIP consumer evidence (source-only)

**Evidence scope:** This is a host-side source inspection of `dlundqvist/xone` at commit
`f2aa9fe01103d7600553b505b298ff0bd47ff280`, not a USB capture, a
physical controller trial, or an implementation proposal. The original project
is `medusalix/xone`; the pinned `dlundqvist/xone` fork describes itself as the
maintained location. The repository's `LICENSE` contains GNU GPL version 2 and
its source files declare SPDX GPL-2.0-or-later. No upstream code is reproduced.

| Rank | Surface | What xone's host code does | Evidence ceiling | Unknown on the device side | Owner issue |
| --- | --- | --- | --- | --- | --- |
| 1 | Startup / identity | Binds vendor-specific wired USB GIP; announce → identify → parsed metadata → class-driven client registration; handles ACK and chunked traffic | **Consumer-only** | Exact descriptors, response/ACK timing, keep-alive, firmware variation | [#168](https://github.com/anderstvoss/virtualgamepad/issues/168) |
| 2 | Rumble / impulse | Emits four-motor GIP command but normal Linux FF updates only the two main amplitudes | **Consumer-only** | Whether impulse motors actuate and their exact transfer function | [#160](https://github.com/anderstvoss/virtualgamepad/issues/160) |
| 3 | Input | Decodes Series-style controls, separately handles Guide, conditionally decodes Share; maps to evdev | **Consumer-only** | Physical packet variants and Share positioning by firmware | [#160](https://github.com/anderstvoss/virtualgamepad/issues/160) |
| 4 | Wireless adapter | USB receiver binding, per-associated-client GIP adapters, data/audio queues and lifecycle | **Consumer-only** | Real association, capacity, timing and radio-frame behavior | [#165](https://github.com/anderstvoss/virtualgamepad/issues/165) |
| 5 | Headset audio | GIP headset class to ALSA full-duplex PCM, optional wired isochronous audio | **Consumer-only** | Attached Series headset topology, microphone routing, formats and fidelity | [#168](https://github.com/anderstvoss/virtualgamepad/issues/168) |
| 6 | Battery / power | Interprets GIP status and sends power controls; publishes power-supply state | **Consumer-only** | Battery cadence and actual power transitions | [#160](https://github.com/anderstvoss/virtualgamepad/issues/160) |
| 7 | LED / brightness | Sends GIP LED mode and brightness, presents a Linux LED class device | **Consumer-only** | Device acceptance, physical brightness and persistence | [#160](https://github.com/anderstvoss/virtualgamepad/issues/160) |

## Provenance and comparison boundary

Pinned source records `xbox-xone-*` all share lineage `xone-dlundqvist`;
multiple files from this single driver are **not** independent corroboration.
The reused kernel xpad source is `xbox-series-linux-xpad` at Linux commit
`4056b3c9d3c92ea45955641dbafeb9b960e146ef`; the reused SDL source is
`xbox-series-sdl-xboxone` at commit
`d4557c1511c721485dc4960f7149730afc9a73a0`. Their original records are
unchanged. `xbox-series-usb-device-gaps` continues to define the device-side
unknowns, while the new records have `evidence_role = consumer` throughout.

## Wired USB and GIP startup

The wired driver recognizes a vendor-specific interface with subclass `0x47`,
protocol `0xd0`, interface number 0 and a supported vendor. It obtains separate
interrupt data endpoints. An optional interface 1 has an alternate setting 1
containing isochronous IN/OUT audio endpoints. It is not USB Audio Class.
Wired code resets the USB device at probe, initializes data URBs and registers
one GIP adapter; absent optional audio interface is allowed. An advertised
audio interface missing the expected alternate setting or endpoints is a probe
error. See `xbox-xone-wired` (`transport/wired.c:12-29, 389-500`).

The protocol parser decodes command, options, nonzero outbound sequence and
variable-length payload size, with optional fragmentation offsets. On arrival,
GIP `ANNOUNCE` (`0x02`) supplies identity/version data and triggers host
`IDENTIFY` (`0x04`). Identification parses metadata tables: supported commands,
firmware versions, possible audio formats, input/output capabilities, logical
classes, interface IDs and an optional HID descriptor. The class-based GIP bus
then binds the gamepad or a separately advertised headset client. The gamepad
probe sends `POWER` (`0x05`) with power-on mode, initializes auxiliary surfaces
and registers the input device. Client registration is deferred, including a
700 ms delay in this pinned host implementation. That delay is not proof of a
device-mandated startup wait. See `xbox-xone-gip-protocol` (`bus/protocol.c:224-501,
1152-1301`) and `xbox-xone-bus` (`bus/bus.c:55-99, 211-240`).

The host acknowledges messages requesting ACK with command `0x01`, reusing the
received sequence. Large messages are fragmented; the implementation bounds
buffers, acknowledges selected chunks and sends completion fragments. Audio
output has a separate sequence counter. Packet length errors, malformed
metadata, conflicts between fragments and initialization failures can reject
processing or prevent input registration. Disconnected GIP status unregisters a
client. **No measured ACK deadline or generic keep-alive interval is established
by these source paths.** Receiver pairing timers and headset startup retries
are not substitutes for a device-side GIP timeout measurement. See
`xbox-xone-gip-protocol` (`bus/protocol.c:357-467, 1080-1150, 1595-1714`).

## Input and Linux evdev comparison

`xbox-xone-gamepad` (`driver/gamepad.c:260-306, 335-482`) interprets the GIP
input as face buttons, Menu/View, shoulders, stick clicks, D-pad hat, two
10-bit triggers and four signed stick axes. The Guide button is handled by an
internal virtual-key message and becomes `BTN_MODE`, not part of the ordinary
input payload. Share becomes `KEY_RECORD` only after an interface-capability
check; the driver calculates an offset from the end of the received payload
and adjusts it when an extension interface is present. This is a host decoding
rule, **not** a physically confirmed universal Series packet.

The xpad baseline `xbox-series-xpad-evdev-shape` describes **26 capabilities**:
12 keys, eight absolute axes and six FF capability entries supplied by the
Linux memoryless FF layer. For a standard xone gamepad advertising Share, xone
configures the same keys and axes (stick fuzz 16, flat 128; triggers 0–1023)
and invokes the same memoryless FF abstraction. Important differences are:

- xone sets the input bus to `BUS_VIRTUAL` and uses a generic Xbox name;
  xpad uses USB input ancestry and its device-specific identity.
- xone conditionally discovers Share from GIP interface identifiers; the pinned
  xpad path uses its device mapping table, with its own Share-offset rule.
- xone has additional firmware-dependent handling for Elite paddles and can
  publish four grip buttons, not part of the standard Series 26-capability set.
- Both expose ordinary FF, but neither makes independent impulse-trigger
  actuation available through the basic `FF_RUMBLE` evdev API.

This comparison concerns **post-driver output**; it does not establish byte-for-byte
USB GIP, driver bind equivalence or controller firmware behavior. See existing
`xbox-series-xpad-evdev-shape`, `xbox-series-xpad-trigger-rumble-limitation`
and `xbox-xone-evdev-compare`.

## Rumble: the key result

The pinned xone `driver/gamepad.c:73-115, 151-215` models the left and right
main actuators and both impulse-trigger actuators in a GIP `0x09` output message.
Its initialized motor-enable mask includes all four, but ordinary Linux
`FF_RUMBLE` receives only strong/weak magnitudes and writes them to the main
motor fields, scaled into a 0–100 command range. The trigger fields remain
zero in this code path. It schedules ordinary updates with a 10 ms delay.

**Answer: xone is not a Linux evdev consumer that independently drives impulse
triggers.** The existing pinned SDL HIDAPI Xbox One consumer **does** contain a
conditional trigger-rumble API path and four-amplitude wired GIP packet
constructor (`SDL_hidapi_xboxone.c:564-640`). This establishes an alternate
Linux **source-level** consumer implementation, not that SDL acquired this
specific hardware under the observed driver stack or that the motors moved.
The xone and xpad main-motor `FF_RUMBLE` limitations must remain explicit.

## LED, battery, power and audio

The gamepad path publishes battery status and coarse capacity using the Linux
power-supply subsystem, and publishes LED mode/brightness through Linux's LED
class. It sends `LED` (`0x0a`) commands, defaults the Guide LED on, and uses
GIP `POWER` (`0x05`) for mode transitions. The status handler decodes battery
fields and removes disconnected clients. These are software surfaces, not
physical cadence, intensity or persistence measurements (`driver/common.c:12-188`,
`bus/protocol.c:475-487, 595-610, 1184-1210`).

The headset class is separately registered only if relevant identification
metadata offers audio formats. `driver/headset.c:295-319, 345-443, 475-595`
registers one ALSA playback and one capture substream, negotiates PCM formats,
uses GIP audio control (`0x08`) and GIP audio samples (`0x60`), and schedules
nominal 8 ms playback blocks. The wired transport enables its isochronous
alternate setting and handles audio URBs (`transport/wired.c:261-385`). Some
headset models have additional startup/authentication behavior. A Linux
microphone node is not proof of actual microphone audio, and attaching a
headset to a particular Series controller is **not** validated here.

Existing claim `audio-xbox-series-xpad-disables-gip-audio` remains valid: xpad
selects alternate setting 0 to disable the GIP audio interface, whereas xone
implements a conditional GIP headset path. This difference does not authorize
a generic UAC2 device to be called a physically accurate Xbox GIP controller.

## Wireless receiver transport (not Bluetooth)

The receiver driver matches Microsoft USB IDs `045e:02e6`, `045e:02fe`,
`045e:02f9` and `045e:091e` for external or built-in adapter variants,
loads separately obtained Microsoft adapter firmware as a prerequisite, and
handles pairing and receiver events. **No vendor firmware was downloaded,
inspected, hashed, disassembled, or redistributed for this research.**
See `xbox-xone-receiver` (`transport/dongle.c:20-45, 1076-1182,
1290-1350, 1547-1587`) and `xbox-xone-readme` (`README.md:126-142`).

The receiver manages multiple associated clients and creates an independent
GIP adapter per client behind the common USB receiver. Wireless input is
passed to the same GIP parser used by the wired path. Data and audio use
separate internal receiver queue types; client association, disconnection,
reconnect and shared receiver teardown are transport-specific. Code allocates
up to 16 client entries; this is **not** a validated maximum simultaneously
usable controller count. See `transport/dongle.c:31-44, 130-251, 482-632,
692-714, 837-945`. This transport is `receiver`, not Bluetooth, and does not
imply the Steam Puck's slot semantics are equivalent.

## Physical validation plan — NOT RUN

1. Compare the physical Series wired USB configuration, endpoint types and
   alternate settings with the pinned xone binding conditions, withholding
   all private identifiers and captures from the public corpus.
2. Capture privately the host-triggered announce/identify/power/ACK exchanges,
   note commands, response order and timing bounds; publish only reviewed,
   identity-free derived observations through the corpus's capture-safety flow.
3. Compare Guide and Share under ordinary and extended firmware behavior,
   including xone versus xpad resulting evdev event domains.
4. Test independent left/right main and impulse-trigger stimulus through
   SDL's explicit trigger API, then xone's FF interface; record actuation
   independently, without assuming packet intent guarantees movement.
5. Test a real headset microphone and playback against ALSA nodes over wired
   USB and receiver separately, including attach/detach and stream failure.
6. Test receiver association/reconnect and multiple clients with pinned xone;
   record transport transitions but no device identity in public files.

**No host, device, firmware, bus capture or timing result was available in this
research session.** These experiments are proposed only, not executed.

## Consumer implications (inference, no implementation proposal)

- [#168](https://github.com/anderstvoss/virtualgamepad/issues/168): A
  host-equivalent wired Xbox Series path must accommodate vendor-specific GIP
  interfaces, client metadata, bidirectional commands and optional isochronous
  GIP headset traffic; a generic HID/UAC approximation is not evidence of GIP.
- [#165](https://github.com/anderstvoss/virtualgamepad/issues/165): The
  receiver demonstrates separation of receiver lifetime, per-client GIP
  adapters and shared transport, but it does **not** settle Steam Puck
  architecture or real-slot limits.
- [#160](https://github.com/anderstvoss/virtualgamepad/issues/160):
  Keep the shipped xpad-style uinput acceptance separate from GIP identity,
  Share protocol variations, native trigger effects and physical validation.

No existing records, accepted evidence levels, or implementation branches are
changed by this source-only research.
