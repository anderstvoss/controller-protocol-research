# Alpha 2 controller polish cleanup 2

All results use virtualgamepad `dda74f526bd40054a1552bce54e2e5e103c4941a`, Linux 7.3.0-1-mainline and SDL 3.4.20. The virtual controllers used UHID. [Cleanup 1 baseline](alpha2-polish-host-evidence.md).

## Wii retail descriptor

| Wii Remote | Typed identity | Driver probe | Usable nodes | Result |
| --- | --- | --- | --- | --- |
| Original | matched | ENOMEM | 0 | unavailable |
| Plus | matched | ENOMEM | 0 | unavailable |

The synthetic-descriptor baseline recorded a matched identity, four of four EEPROM replies, one default SDL evdev joystick and zero default HIDAPI claims after memory compaction. The retail run matched the typed identity for both revisions. The probe failure occurred before either revision produced usable nodes, so comparison stops there. Cleanup 1 has no separate Plus or Dolphin result. [Experiment](../records/experiment/vg-alpha2-polish-cleanup2-wii-retail.json)

## Generic USB binding

| Family | Stock binds (of 3) | SDL evdev | SDL HIDAPI | Generic |
| --- | --- | --- | --- | --- |
| DualSense | 3 | 3 | 3 | unavailable |
| DualShock 4 | 3 | 3 | 3 | unavailable |
| Switch Pro | 3 | 3 | 3 | unavailable |
| Xbox 360 | 3 | 3 | 0 | 3 already generic |

HID core and hid-generic matching predict the cleanup 1 ENODEV for devices that match a specialized driver with the stock setting. The current terminal has no_new_privs set. Sudo could not read or change the root-only module parameter, so the parameter-enabled arms and the Steam Switch Pro arm remained unavailable. No host setting was changed. DualSense bound in 3 of 3 stock sessions. DualShock 4 bound in 3 of 3 stock sessions. Switch Pro bound in 3 of 3 stock sessions. Xbox 360 bound in 3 of 3 stock sessions. The generic Steam Switch Pro was unavailable. [Experiment](../records/experiment/vg-alpha2-polish-cleanup2-usb-binding.json) [Linux HID matching](https://github.com/torvalds/linux/blob/4056b3c9d3c92ea45955641dbafeb9b960e146ef/drivers/hid/hid-generic.c#L33-L49).

## Steam DualSense gyro

Steam opened the attributed hidraw endpoint. File descriptor sampling found zero Steam opens on owned evdev endpoints. UHID received 7 GET_REPORT requests for features 0x05, 0x09 and 0x20. All received successful replies. The provider received 10 asynchronous output reports with ID 0x02 and zero SET_REPORT requests. The UHID trace identifies report types and replies. Attribution of the startup traffic and the presence of a dedicated motion-enable request remain undetermined. After the commit boundary, 233 single-axis and 599 sustained multi-axis reports carried the expected nonzero values. At return to neutral, 114 reports carried zero gyro. The isolated retry opened Steam Settings and stopped when the Controller page transition could not be confirmed. The earlier calibration display remaining neutral is unresolved. The wire trace shows the provider emitted the stimulated motion correctly while Steam held hidraw. [Experiment](../records/experiment/vg-alpha2-polish-cleanup2-steam-dualsense-gyro.json)

## Exact SDL Bluetooth mappings

The columns use physical control position. Cells show the observed changed controls when the expected control did not map exactly. A pass requires the expected control alone to move and return to neutral. Default HIDAPI is the SDL mapping acceptance path. HIDAPI-off evdev measures fallback compatibility. Cleanup 1 measured 1/8, 1/8 and 4/8 exact SDL evdev mappings for DualSense, DualShock 4 and Switch Pro respectively.

| Family | SDL path | South | East | West | North | Left X | Right X | LT | RT | Exact with reset |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DualSense | Default HIDAPI | Exact | Exact | Exact | Exact | left (no reset) | left, right (no reset) | left, right, lt (no reset) | left, right, rt (no reset) | 4/8 |
| DualSense | HIDAPI off | west | south | north | east | Exact | lt (no reset) | right, lt (no reset) | lt (no reset) | 1/8 |
| DualShock 4 | Default HIDAPI | Exact | Exact | Exact | Exact | left (no reset) | left, right (no reset) | left, right, lt (no reset) | left, right, rt (no reset) | 4/8 |
| DualShock 4 | HIDAPI off | west | south | north | east | Exact | lt (no reset) | right, lt (no reset) | lt (no reset) | 1/8 |
| Switch Pro | Default HIDAPI | Exact | Exact | Exact | Exact | Exact | Exact | Exact | Exact | 8/8 |
| Switch Pro | HIDAPI off | east | south | Exact | Exact | Exact | Exact | rt | No change | 4/8 |

Fresh-session checks on both Sony pads isolated the four analog stimuli. Each moved only its intended SDL HIDAPI control to 32767. Both triggers returned to 0. Each stick started at 0 and settled at +128 after its first excursion. The residual stick values account for the extra changes in later controls in the sequential runs. This yields eight correctly attributed controls, six exact initial-baseline returns in isolated checks, and four exact placements with resets in the original sequential run for each Sony pad. The strict initial-baseline criterion remains open for the Sony sticks. Switch Pro passed all eight HIDAPI checks.

## Bluetooth timing

Each xtask batch ran 50 cycles with SDL and no latency budgets. The observer selected the owned evdev joystick with the HIDAPI backend disabled. Counts are published independently for each stage.

| Family | N | Slots | Created | Appeared | Direct open | SDL open | Removed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DualSense | 1 | 50 | 50 | 50 | 50 | 50 | 50 |
| DualSense | 3 | 150 | 150 | 150 | 150 | 150 | 150 |
| DualShock 4 | 1 | 50 | 50 | 50 | 50 | 50 | 50 |
| DualShock 4 | 3 | 150 | 150 | 150 | 150 | 150 | 150 |
| Switch Pro | 1 | 50 | 50 | 50 | 50 | 50 | 50 |
| Switch Pro | 3 | 150 | 150 | 150 | 150 | 150 | 150 |

The first DualSense N3 invocation exceeded the outer process watchdog while Steam was running and did not produce a complete receipt. The reported DualSense N3 run completed with Steam closed. During both DualShock 4 invocations, only documentation, manifest and research-pin edits were present in the worktree. The compiled probe and runtime code came from the stated revision.

DualSense [Experiment](../records/experiment/vg-alpha2-polish-cleanup2-dualsense-bluetooth.json) · DualShock 4 [Experiment](../records/experiment/vg-alpha2-polish-cleanup2-dualshock4-bluetooth.json) · Switch Pro [Experiment](../records/experiment/vg-alpha2-polish-cleanup2-switch-pro-bluetooth.json).
