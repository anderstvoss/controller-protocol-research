# W2 interim descriptor: bounded local comparison

This is virtual-only evidence on Linux6.12.113+deb13-arm64 aarch64, not retail
fidelity, physical calibration, gameplay or final-release performance acceptance.
Before code56fc3f6 and after code07e42cb retain distinct source/executable hashes.
The interim Game Pad collection is independently authored; fields remain vendor
Variable bytes and the report table is unchanged. No rnconrad descriptor was
copied. Retail-evidence successor is virtualgamepad#238.

## SDL3.2.10 comparison

The first child removes all inherited SDL_* environment and sets no hints. The
second enables HIDAPI/WII/WII_PLAYER_LED/background events, while retaining the
default controller-only HID filter. Neither uses enumerate-all. Both use distro
SDL3.2.10+ds-1 and the same hashed original helper.

| Observation | Vendor collection before | Interim Game Pad after |
| --- | --- | --- |
| Granted direct raw open | succeeds | succeeds |
| Actual-default owned HID enumeration |0 |1, Bluetooth bus2, usage1/5, open succeeds |
| Actual-default owned joystick | evdev,11buttons/0axes/hats, no sensors | same evdev core |
| Wii-enabled/default-filter owned HID entry |0 |1, usage1/5 |
| Wii-enabled opened owned joystick | none observed | initial HIDAPI,6axes/26buttons/0hats; accel capability1, gyro0 |
| Sustained attachment sequence | no owned joystick to assess | disconnects and stays disconnected in later snapshots |

These runs establish default HID discovery and an initial Wii-enabled raw-path
claim for the interim collection. They do not establish sustained extension,
sensor delivery or game acceptance. No timeout cause is diagnosed, no cadence
invented and no additional descriptor change made to chase that disconnect.
Actual-default enumeration is distinct from enabling the Wii HIDAPI driver.

Both comparison devices coexist during the baseline human-grant round. SDL may
internally enumerate the other virtual device even though the helper publishes
only the target creation's exact raw/core paths. Therefore the baseline
Wii-enabled absence of an evdev joystick has an explicit other-device limit;
this run cannot establish its cause. Baseline closes before the revised run.

wiimote remains bound. Default-profile owned kernel names/key/axis masks match
before/after across core, accelerometer, IR, Nunchuk, Classic and MotionPlus.
Four granted brightness writes succeed and all four retained LED bits are true
in both cases. This is software intent, not physical light delivery. Both owned
HID roots and raw nodes disappeared after idempotent close, before timing reused
raw indices. No unbind, agent grant, root operation or persistent policy change.
Optional Dolphin was not rerun; its backend is a separate unresolved observation.

Each12-second SDL child attempts four4-second phases with300ms kernel service
before sampling. The last phase may start after child exit; kernel-shape samples
are separate from SDL sensor/extension coverage. No first-neutral timestamps or
fd counts are measured by this functional helper. Private raw logs/identities
are excluded; fixture transforms retain original result hashes.

## Final-head creation/removal timing

The unchanged #166 xtask harness was built on tracked-clean code07e42cb, copied
and hashed once, then used for10 cycles each at N1/N4 after both comparison
devices closed. All N sessions coexist before removal. First cycle is labelled
cold, later cycles warm. Both runs exit0 with no operation errors, and every
owned node-gone stage is observed. These fresh nodes inherit no comparison
grants; consumer-open remains denied, first-neutral lacks an oracle and no SDL
probe is requested. The harness pkg-config SDL3.5.0 metadata is not the SDL3.2.10
consumer runtime used above.

| Source/run | N | Warm samples | API return p50 ms | Close p50 ms | Close max ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| C5 research#17, ccb98dc |1 |9 |0.152417 |8277.520420 |9364.405088 |
| W2 code07e42cb |1 |9 |0.234417 |8245.893462 |8295.497837 |
| C5 research#17, ccb98dc |4 |36 |0.243083 |4130.360502 |8300.426754 |
| W2 code07e42cb |4 |36 |0.096041 |4090.454002 |8260.341129 |

N1 fd4→4, thread1→1 and hidraw4→4 restore, but global input-node count26→29
changes without attribution. Its experiment is **blocked** for complete global
resource-restoration acceptance; no conclusion is drawn about an owned leak or
an unrelated actor. N4 starts at29 and ends29, with all other counts restored,
so its bounded creation/removal experiment is **passed**. The counts and missing
stages remain in the fixtures. No failed/blocked record is replaced or silently
rerun to obtain an equal count.

The revisions, initialization history, CPU load and live environment differ.
These are separate bounded distributions, not a causal descriptor speedup,
parallel-throughput result, fixed latency budget or final release qualification.
Earlier W1/C5 records and every wii-gap claim remain unchanged. Current inherited
research inventory is92 Wii claims with7 unknowns; these new observations add
no claim promotion.
