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
hid-wiimote binding on an eligible host. Source-only provenance and explicit unknown device claims remain essential.
The optional `evidence_role: consumer` marker now prevents host-side evidence
from raising device evidence status independently of transport.

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

Inventory before clean follow-up: **149 Wii claims**, including four imported-block consumer
arm sets on merged code `5a11e507ac973c23ca10beb36edb44fc35034376`. Native
Dolphin MP-only reads MP calibration and visibly changes mapped A, accelerometer,
basic IR and gyro indicators under explicit lab settings. MP+Nunchuk stops on
A400F6/4 error 7 before calibration. No additional register model is added.
Cemu coexistence arms retain a foreign companion holder: base reads succeed,
but native identity/init exchange and unobserved decoding limit the result.
The mapped 16-byte calibration replies in its MP+Nunchuk arm match the MP block,
not Nunchuk. The clean no-holder retest was blocked before application launch.
These distinctions do not promote physical, calibrated-rate or game acceptance.


### W8 clean Cemu follow-up

Current inventory: **151 Wii claims**. Two additional 35-second imported-resource
arms pass no-holder preflight after the browser holder closes. MP has no native
extension calibration read; MP+Nunchuk has 18 successful A40020/16 replies,
17 matching caller Nunchuk calibration and one matching MP first half. This
establishes delivery beyond the earlier refusal, with kernel mapping still
shared. Repeated initialization and decoded application motion remain the next
unestablished checkpoint. No additional model change or physical promotion.


### W9 fixed F7 compatibility policy

Current inventory: **167 Wii claims**. `wii-w9-f7-fixed-preparing-compat` pins
the fixed non-ready value chosen by Anders: F7 is held at 0x02 while the active
passthrough identity mirror applies. The source comment describing hardware is
not our physical readback. No challenge is implemented or promoted; offset
0x50 remains error 7. Dolphin ignores this byte when decoding downstream ID.
Runtime shim observations remain not run in this source-only record.


### W9 bound-kernel compat controls

Current inventory: **178 Wii claims**, including the seven `wii-gap-challenge-*` claims from #49. Four new `wii-w9-*` arm sets retain
MP+Nunchuk on/off F6 boundaries after non-Dolphin reinitialization, an MP-only
Dolphin mapped-gyro positive control and a fresh kernel evdev delivery pass.
The reused post-Dolphin missing-MP-node preflight and excluded pilot remain
explicit. No live passthrough-window success or MP+Nunchuk acceptance is
inferred; no bank alias, challenge, physical or calibrated-rate promotion.
See `docs/wii-w9-consumer-runs.md` for P3 scope and cleanup.

### Remote Plus source pass

Current inventory: **187 Wii claims**, adding nine source-only `wii-gap-plus-*`
claims on Remote Plus identity and integrated MotionPlus gates. See
`docs/wii-remote-plus.md`. Integrated MotionPlus ID bytes, calibration,
F6/F7/40 and challenge behaviour remain unmeasured.


### W9e per-device binding preflight

Current inventory: **190 Wii claims**, adding three `wii-w9e-*` claims on
current research main after the 187-claim Remote Plus pass. The historical
W9 adoption pin ceaa48a remains 178. A guarded owner-run per-device generic
bind failed, the original wiimote binding was verified restored, and the
virtual device was closed. Both Dolphin arms and their motion/register/P3
checkpoints remain unmeasured. The expected generic-binding kernel-node
trade-off is unmeasured too. No acceptance extension or host-policy change
follows. See `docs/wii-w9e-binding-preflight.md`.


### W9e generic-binding retry

Current inventory: **193 Wii claims**. Three new consumer claims preserve the
owner-run 2.035782-second creation window, parameter readback 0 before probes,
and persistent generic binding for the two dedicated devices. MP+Nunchuk
reaches exact imported MP and child calibration, but sampled changing decoded
Nunchuk/gyro remains unestablished. F6 was not requested on this path. The
MP-only mapped gyro control passes; both arms have zero native and combined
A400F0=55 after mode 05. Kernel input companions and libxwiimote access are
absent before and after. No MP+Nunchuk adoption or release policy follows;
#258 still gates release use. Earlier #55 preflight records remain historical.
See `docs/wii-w9e-generic-retry.md`.

### Remote Plus consumer startup traces

Current inventory: **203 Wii claims**, adding ten source-only
`wii-gap-plustrace-*` consumer claims on TR / 057e:0330 startup ladders and
the minimal reply contract. See `docs/wii-remote-plus-consumer-traces.md`.
All acceptance experiments remain not run.


### W9f counted stimulus and reporting boundary

Current inventory: **205 Wii claims**. Two new wii-w9f consumer claims
record the scheduled counted stimulus and timestamped report ordering. All
28 MP+Nunchuk data frames precede mapping; post-map MP/child rates over the
180-second window are 0/0. The codec pauses until another report-mode request,
which Dolphin sends in MP-only but not this Nunchuk sequence. No model fix or
adoption follows. MP-only mapped gyro passes. See `docs/wii-w9f-stimulus.md`.

### Plus P1 kernel-bound acceptance

Current inventory: **210 Wii claims** (205 after W9f plus five wii-p1 claims). Five wii-p1 consumer claim sets qualify
Tr separately: changing kernel/xwiimote gyro in MP-only and Nunchuk captures,
no changing SDL gyro in two held-kernel 3.2.10 runs, and changing mapped gyro,
acceleration and basic IR in bound Dolphin MP-only. Both devices are gen20.
The owner-filtered kernel log contains detection but no inactive-ID hex line;
no byte-level kernel log readback is claimed. No Original pass is inherited,
no special-driver window is used, and no physical or release gate is cleared.
See `docs/wii-plus-p1-host-runs.md`.

### MotionPlus activation/status source review

Current inventory: **220 Wii claims** (210 on Plus P1 main and ten new
source-only `wii-gap-mpstatus-*` claims). WiiBrew deactivation documents
0x20 disconnect then reconnect; Dolphin emulator also simulates activation
pin changes, but physical activation and active mode switch edge counts and
timing remain unmeasured. Consumer status re-probes and W9 kernel/SDL risks
are ranked in `docs/wii-motionplus-activation-status.md`. All physical and
host tests proposed here are not run.
