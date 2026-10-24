# W7: independent Wii consumers on the bounded Linux virtual host

Runtime baseline: virtualgamepad `840db2771cbcef83b50ee9355c7b6165b95f234a`
(W6 merged; unchanged Wii native model/codec/descriptor). Linux6.12.113+deb13-arm64,
ARM64 Debian13. Research parent `fe4ce9e0386f6c7199ab40699e107469f5a2ec32`.
The [consumer survey](wii-consumer-survey.md) supplied hypotheses, not passes.
Only owned virtual devices were driven; no physical controller, radio transport,
calibrated motion, speaker or complete game/controller acceptance follows.

| Arm, in order | Version and entry | Recorded outcome | Boundary |
| --- | --- | --- | --- |
| Cemu native Wii Remote | No executable; installed Flathub has no aarch64 Cemu ref | **Blocked before discovery** | MP and MP+Nunchuk, with/without kernel holder, were not run. Do not interpret availability as Cemu non-support. |
| xwiishow / libxwiimote | Debian2-4.3; exact owned HID syspath, wiimote driver | **MotionPlus and static normalization pass** | UI lists Nunchuk, but requested Nunchuk interface is absent from the library opened mask. No Nunchuk event acceptance. |
| evtest control | 1:1.35-1+b1; exact owned MotionPlus node | **Kernel gyro repeatability pass** |12seconds, no userspace native protocol decoder or physical calibration. |
| RetroArch udev |1.20.0+dfsg-2+b1, Git b2ceb50; original no-content input diagnostic core | **Generic controls pass on UHID and uinput; sensor activation refused** | Explicit lab bindings, not complete printed-label mapping; no gyro delivery. |
| Dolphin direct |2609a, aarch64 Flatpak; separate MP/MP+Nunchuk profiles | **Blocked at establishing direct-scanner enumeration** | Separate raw-access and trace-positive-control passes do not establish Dolphin status probe, Connect or ControllerInterface AddDevice. |

## Discovery, drive and observations

Anders installed xwiimote/libxwiimote-dev/RetroArch and applied/confirmed five
temporary grants supplied locally. Before starting the consumers, the probe
reverified its own creation identity, bus5 Nintendo057e:0306, wiimote driver,
raw-node ancestry and access. No agent sudo, unbind, persistent policy or game
content. Attachment was fixed throughout each consumer window. The two injected
raw pitch/roll/yaw vectors were `[9000,7000,8500]` and `[7000,9000,7800]`, all slow
flags true, alternating every250ms. Core A, Nunchuk buttons/stick and accel were
also explicitly driven. The helpers service and commit while children execute.

**xwiishow/libxwiimote:** list resolves one exact-owned HID; the UI was launched
by verified syspath, not a guessed index. This version starts MotionPlus enabled;
the final UI run toggled `m` off/on at1/2seconds, `n` at6 and `q` at12, in160x40.
The separate18second library readout requests core/accel/MP/Nunchuk: available
mask775, requested771, opened259. MP events in three6second phases numbered
25/24/24. Default minima were `[-3528,-10728,-10728]`, maxima
`[2772,7272,7272]`; setting offsets10/20/30 subtracts exactly those per-axis
amounts. The final adaptive phase uses factor10 and ends with net offsets zero
under alternating-sign input; it is not a stationary-convergence or calibrated
rate test. Kernel A600FE05 mapping was observed. The installed version's requested
Nunchuk bit512 is not opened; the detected extension label alone is not a pass.

**evtest:** the owned MP-only node produces49 changes per ABS_RX/RY/RZ over12seconds,
with the same extrema as the library default above. Kernel A600FE04 was observed.
This repeats the kernel delivery part of `wii-w5-kernel-motionplus-gyro-delivery`,
without replacing or rewriting the W5 packet-validation evidence.

**RetroArch:** udev identifies the core and Nunchuk as joypads for both realizations.
Each recorded diagnostic window reaches600 core frames; core and accessory
control-change counters are nonzero. The core requests accel and gyro on8 ports:
all return false. Owned FD snapshots at4/8seconds hold the core twice and Nunchuk
once, with no MotionPlus/accelerometer sibling held. All available owned input
nodes are transiently opened during discovery; that is not retained sensor
selection. The installed1.20.0 udev joypad table has no sensor callbacks. The
survey's later RXYZ-as-accel fallback is therefore **not an observed cause** in
this build. uinput has no HID parent for same-parent sensor pairing. Both windows
end at the25second process timeout after the diagnostic core's shutdown request;
those timeouts do not erase the600frame control observations or imply clean exit.

**Dolphin checkpoints:** all real slots0, Core.WiimoteContinuousScanning=True,
Core.WiimoteControllerInterface=True, speaker false, background input, offscreen
Qt and SDL_JOYSTICK_HIDAPI_WII=0. Each fixed profile ran35seconds with no ROM.
The interposer's private destination files were created, but contain no owned
Dolphin libudev/open/read/write observations. A separate sandbox check opens the
owned raw FD; a separate original positive-control executable, using the same
Flatpak and library, records owned enumeration, udev-device construction and raw
open. It sends no status command. Thus trace loading/access are checked, while
Dolphin's direct enumeration is the **first unestablished checkpoint**; status
write, Connect, AddDevice and gyro remain unestablished downstream. These dynamic
hooks are not private method breakpoints: scanner activation, filtering and
observation coverage remain unresolved, rather than an inferred internal error.
Dolphin's installed IOhidapi source hashes identically to the survey's pinned file.

## Evidence and cleanup

Five `wii-w7-*-host-run` experiments each link one reduced acceptance fixture and
one `wii-w7-*-consumer-result` claim. The Cemu and Dolphin claims remain unknown;
three measured consumer results are inferred, never physical. Fixture config
cites the specific survey claims tested; evtest is a W5 repeatability control.
Existing `wii-gap-*`, W1–W5 records and historical checkpoint snapshots are intact.
Current Wii inventory:137 claims,9 unknown,124 source-supported,4 inferred.

Two Dolphin children survived the Flatpak timeout wrapper. They were identified
by their exact fresh profile arguments and explicitly sent TERM; no KILL was
needed. All owned consumers were verified gone, then both device sessions closed
twice. Owned HID, hidraw, LEDs and uinput nodes were verified absent. Resource
cleanup fields describe the complete W7 session, not independent global device
count deltas. Private paths/identities, raw reports, terminal data, wall clocks,
third-party code and debug logs remain outside the corpus. Public fixtures contain
semantic counts/extrema and source/tool hashes only.

Original [tools](../tools/wii_w7/README.md), source pins, reduced fixture hashes and
deterministic boundary tests make the supported scope reviewable. No Wii protocol
bug was demonstrated, so there is no model/codec/descriptor patch. A future Cemu
run needs an available native build/host; a future Dolphin run needs an independently
observed scanner activation/UI path, not assumed kernel unbinding.
