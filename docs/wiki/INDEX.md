# Controller evidence navigator

This is the hand-maintained entry point for browsing the existing corpus.
Controller names, kinds and parent relations below are taken from
[the controller registry](../../records/controller/). Follow a controller
record to its tracked issue, then consult the individually scoped claims
and source records. The complete per-claim, per-source index is built by
[the wiki generator](README.md) into generated output.

## Sony

| Registry entry | Kind | Supporting research notes |
| --- | --- | --- |
| [DualSense](../../records/controller/dualsense.json) | controller | [Citation map](../dualsense-citation-map.md), [consumer survey](../dualsense-consumer-survey.md), [decision table](../dualsense-decision-table.md) |
| [DualSense Edge](../../records/controller/dualsense-edge.json) | controller | [Sony consumer contention](../sony-consumer-contention.md) |
| [DualSense family](../../records/controller/sony-dualsense-family.json) | family | [DualSense citation map](../dualsense-citation-map.md) |
| [DualShock 4](../../records/controller/dualshock4.json) | controller | [Citation map](../dualshock4-citation-map.md), [consumer survey](../dualshock4-consumer-survey.md), [decision table](../dualshock4-decision-table.md) |

## Nintendo

| Registry entry | Kind | Supporting research notes |
| --- | --- | --- |
| [Wii Remote](../../records/controller/wii-remote.json) | controller | [Consumer survey](../wii-consumer-survey.md), [remote plus](../wii-remote-plus.md), [Dolphin attachment](../wii-dolphin-attachment-technical.md) |
| [Switch 1 Joy-Con family](../../records/controller/switch-joycon-family.json) | family | [Consumer survey](../switch-joycon-consumer-survey.md), [pair shape](../switch-joycon-pair-shape.md) |
| [Joy-Con left](../../records/controller/switch-joycon-left.json) | controller | [Validation plan](../switch-joycon-validation-plan.md) |
| [Joy-Con right](../../records/controller/switch-joycon-right.json) | controller | [Validation plan](../switch-joycon-validation-plan.md) |
| [Switch Pro](../../records/controller/switch-pro.json) | controller | [Citation map](../switch-pro-citation-map.md), [decision table](../switch-pro-decision-table.md) |
| [Switch 2 Pro](../../records/controller/switch2-pro.json) | controller | [Controller registry](../../records/controller/switch2-pro.json) |
| [Switch 2 GameCube USB](../../records/controller/switch2-gamecube.json) | controller | [Consumer survey](../switch2-gamecube-consumer-survey.md), [unrun physical plan](../switch2-gamecube-physical-capture-plan.md) |
| [WUP-028 GameCube USB adapter](../../records/controller/gamecube-usb-adapter.json) | controller | [Consumer survey](../gamecube-adapter-consumer-survey.md), [decision table](../gamecube-adapter-decision-table.md) |

## Valve and OpenPuck

| Registry entry | Kind | Supporting research notes |
| --- | --- | --- |
| [Steam Controller 2026](../../records/controller/steam-controller-2026.json) | controller | [Research gaps](../steam-controller-2026-research-gaps.md), [modes](../steam-controller-modes.md), [consumer survey](../steam-consumer-survey.md) |
| [Steam Controller 2026 Puck](../../records/controller/steam-controller-2026-puck.json) | controller | [Physical capture plan](../steam-physical-capture-plan.md), [receiver interface claim](../../records/claim/steam-puck-interface-selection.json) |
| [OpenPuck](../../records/controller/openpuck-firmware.json) | emulator | [Pinned source](../../records/source/openpuck.json), [identity claim](../../records/claim/puck-current.json) |

The OpenPuck emulator is a distinct registry entry. Its compatibility behavior
must not be presented as physically measured Puck behavior. See the
[worked evidence example](README.md#a-worked-example-steam-controller-2026-puck).

## Microsoft, 8BitDo and host infrastructure

| Registry entry | Kind | Supporting research notes |
| --- | --- | --- |
| [Xbox 360 standard HID](../../records/controller/xbox360.json) | controller | [Citation map](../xbox360-citation-map.md), [consumer survey](../xbox360-consumer-survey.md) |
| [Xbox Series](../../records/controller/xbox-series.json) | controller | [L0 ledger](../ledgers/xbox-series-l0.md) |
| [8BitDo Pro 2](../../records/controller/8bitdo-pro-2.json) | controller | [Pinned FAQ source](../../records/source/8bitdo-pro2-faq.json) |
| [Linux joystick identity](../../records/controller/linux-joystick-identity.json) | host interface | [Consumer evidence rules](../../README.md) |

## Record-level provenance

All research notes remain unmodified. For a statement about an individual
transport, revision or firmware, inspect its corresponding
[claim record](../../records/claim/) before using it as protocol evidence.
That claim links to [source pins](../../records/source/) and
[experiments](../../records/experiment/), whose
[fixtures](../../records/fixture/) link to their reviewed data files.

The wiki generator turns these relationships into a searchable index while
retaining status, source lineage, conflicts and unknowns. See
[README](README.md) and [publishing policy](PUBLISHING.md).
