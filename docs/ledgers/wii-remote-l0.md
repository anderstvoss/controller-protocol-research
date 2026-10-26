# Wii Remote L0 source and consumer ledger

No physical experiment or device-side promotion. Seven pinned,hashed source files
(kernel core/modules/header/IDs, SDL Wii, Dolphin emulation and HIDAPI) support the
source_only consumer claims. Kernel/SDL/emulator behavior is never on its own
proof of a physical protocol,reference image or revision. No upstream excerpts.

## Revision boundary

| Revision | Record | Disposition |
| --- | --- | --- |
| Original RVL-CNT-01 | wii-original-remote-consumer-revision | Kernel Gen 1 name policy only |
| Early integrated Plus/non-TR | wii-early-plus-revision-gap | Unknown discriminator/calibration; not collapsed into original or TR |
| RVL-CNT-01-TR | wii-tr-consumer-revision | Kernel Gen 2/builtin-MP policy only |

## Protocol inventory

| Area | Records | Limit |
| --- | --- | --- |
| Bluetooth bus match | wii-kernel-bluetooth-match | Bus metadata only; no actual radio |
| Report IDs/modes | wii-kernel-report-modes; wii-sdl-extension-modes | Consumer dispatch, not observed firmware packets |
| Status/ACK flow | wii-kernel-status-ack-flow | Cadence/error behavior still requires a reference |
| Extension ID/init/encryption | wii-kernel-extension-init; wii-extension-encryption-gap | Consumer disable-encryption path is not all encrypted behavior |
| MotionPlus/pass-through | wii-kernel-motionplus-pass-through | External/integrated and downstream extensions remain distinct |
| IR modes | wii-kernel-ir-mode-policy | No image quality or physical point validation |
| LEDs/rumble/battery | wii-kernel-outputs-battery | LED/power-supply endpoints distinct from evdev axes |
| Memory | wii-dolphin-memory-routing; wii-memory-size-hypothesis | EEPROM/I2C separation; 0x1700 is a hypothesis, not a frozen map |
| HIDAPI usability | wii-dolphin-hidapi-probe | Active status write; no host/radio acceptance |

## Pinned Linux consumer shape

All ranges below come from hid-wiimote-modules.c at the wii-linux-modules source
revision. Nodes remain separate; this table is the source-derived reference for
a future uinput oracle, not a fixture captured from hardware. Balance Board,
Wii U Pro and musical accessories are excluded from this base/extension table.

| Logical node | Advertised shape | Source lines |
| --- | --- | --- |
| Base keys | KEY_LEFT,KEY_RIGHT,KEY_UP,KEY_DOWN,KEY_NEXT,KEY_PREVIOUS,BTN_1,BTN_2,BTN_A,BTN_B,BTN_MODE |47-99|
| Base rumble | FF_RUMBLE on base input node, memless consumer path |112-164|
| Accelerometer | ABS_RX/RY/RZ -500..500, fuzz 2, flat 4 |498-506|
| IR | ABS_HAT0X/Y through ABS_HAT3X/Y; X 0..1023,Y 0..767, fuzz 2, flat 4 |750-768|
| Nunchuk | BTN_C,BTN_Z; HAT0X/Y -120..120; RX/RY/RZ -500..500, fuzz 2, flat 4 |809-818, 945-966|
| Classic | Own key map; HAT1X/Y,HAT2X/Y,HAT3X/Y -30..30, fuzz 1, flat 1 |1239-1264|
| MotionPlus | ABS_RX/RY/RZ -16000..16000, fuzz 4, flat 8 |2814-2825|

These consumer units are not raw sensor units,canonical physical calibration or
a promised universal evdev mapping for every revision. The Wii package must
implement a golden shape from the pinned consumer source and validate actual
hid-wiimote binding on an eligible host. Source-only claims plus explicit unknown
device claims express the evidence boundary without a new claim-schema marker.

## C5 synthetic compatibility model

The wii-c5 source records add report-layout, memory-error, camera and extension
emulator locators. Neutral-mode fixtures cover every legal mode; reserved modes
0x38 through 0x3c are not real modes. No-point IR is explicit. The functional HID
descriptor is an authored vendor-page byte-array descriptor, not a retail dump.
Its usage page and usage are synthetic framing decisions; native IDs and report
lengths derive from the source layout. Host binding remains untested.

EEPROM size, early Plus identity, encrypted extension behavior and physical
calibration remain the original unknown claims. Classic Pro identification,
full-mode blob size/intensity and timing are not established by this addition.

The C5 extension-packing claim adds source-model active-low data, bridge
pass-through transformations and zero-filled 21-byte extension register tails.
The synthetic evdev golden resolves the pinned consumer maps into numeric codes
and separate logical nodes; it retains fuzz as well as flat. Providers that
cannot represent fuzz must record that deviation. Classic Pro wire identity,
retail calibration, encrypted workflows and activation latency remain unknown.

## C5 virtual-host qualification

`wii-c5-evdev-native-values` separates advertised ABS ranges from consumer values; do not silently clamp the latter. `wii-c5-bt-host-binding` records driver binding, six interface masks, extension replacement, MP, rumble and battery endpoint presence. LED-class writes were permission-denied; live ranges/fuzz, SDL HIDAPI, Dolphin and physical calibration remain unmeasured. Four `wii-c5-*-host-run` experiments record 10 cycles at N1/N4 on both realizations, with executable/code hashes, missing consumer/oracle cells and no timing budget.

## W7 independent consumer checkpoint

Initial W7 checkpoint: **137 Wii claims** (132 before W7); 9 remained unknown. Historical
checkpoint snapshots above and in the separate checkpoint ledger stay unchanged.
Five `wii-w7-*-consumer-result` records separate Cemu availability, libxwiimote
MotionPlus/normalization, evtest repeatability, RetroArch generic controls and the
Dolphin scanner boundary. All are consumer evidence from virtual devices; none
promotes physical, radio, calibrated or complete controller acceptance.

See [W7 bounded results](../wii-w7-consumer-runs.md). The installed RetroArch 1.20.0
has no udev joypad sensor callbacks, unlike the newer surveyed RXYZ fallback.
The initial Cemu lookup was blocked before discovery (corrected below); Dolphin was blocked
at establishing direct-scanner enumeration despite separate sandbox access and
trace-positive-control passes. Existing `wii-gap-*` claims are unchanged.

## W7 Cemu AppImage correction

Current inventory: **138 Wii claims** (137 at the initial W7 checkpoint); 9
remain unknown, with 124 source-supported and 5 inferred. The original PATH/Flatpak
lookup missed a non-PATH ARM64 AppImage and did not establish application absence.
`wii-w7-cemu-appimage-result` explicitly supersedes that inference; original
records and the 137-claim checkpoint above remain unchanged. Cemu 29f2f1f exchanges
raw status, register and input reports on the owned UHID. All four profile/holder
arms receive EEPROM 0016 calibration error 8 without an imported image. Native
report 37 delivery in Nunchuk arms does not establish decoded gyro; no calibration
or physical/whole-controller promotion. See [AppImage follow-up](../wii-w7-cemu-appimage.md).


## W8 caller-image and native Dolphin baseline

The historical W7 inventory remains 138 Wii claims. The W8 baseline brings the
baseline inventory to **145 Wii claims**, adding seven bounded virtual-consumer
observations without changing the source or physical evidence category. See
[the W8 report](../wii-w8-consumer-runs.md) for the per-arm records and limits.

Cemu with a synthetic caller EEPROM image passes its base calibration read.
The MP+Nunchuk no-holder arm then reads Nunchuk calibration at A40020 and gets
error 7. Native Dolphin 2503 enumerates and adds the ControllerInterface device
in all four default/image arms. Empty EEPROM blocks base calibration; the
image-only arms pass that read but stall on speaker mute acknowledgement before
MP calibration. Mapping UI and decoded motion remain unobserved. No radio,
physical, firmware cadence, audio or whole-controller claim is promoted.

These are the pre-resource and pre-speaker-ACK baselines. Post-merge imported
block reruns remain pending; owner instruction reserves both code merges.


### W8 post-merge reruns

Current inventory: **149 Wii claims**, including four imported-block consumer
arm sets on merged code `5a11e507ac973c23ca10beb36edb44fc35034376`. Native
Dolphin MP-only reads MP calibration and visibly changes mapped A, accelerometer,
basic IR and gyro indicators under explicit lab settings. MP+Nunchuk stops on
A400F6/4 error 7 before calibration. No additional register model is added.
Cemu coexistence arms retain a foreign companion holder: base reads succeed,
but native identity/init exchange and unobserved decoding limit the result.
The mapped 16-byte calibration replies in its MP+Nunchuk arm match the MP block,
not Nunchuk. The clean no-holder retest was blocked before application launch.
These distinctions do not promote physical, calibrated-rate or game acceptance.
