# Joy-Con permissions handoff for virtualgamepad #258 (E)

**Joy-Con research, prep for virtualgamepad #297** · public udev/systemd file source only, not a permission audit of any running host. Version pins: steam-devices `22ec85e5ff5ea2e15c56d71a41bcbef46356cd60`; joycond `0df025ac5dc284b1f31172b6b252321ba788c4de`.

## E1. Steam Input public rules

Pinned `60-steam-input.rules`, source record `joycon-e-steam-input-rules`:

| Identity | Grant touching that identity | Limit |
| --- | --- | --- |
| 057e:2006 (L) | One `hidraw*` match via parent HID ID pattern, sets `MODE=0660` and `TAG+=uaccess` | Does not itself grant read/write to main evdev or prove Steam client pairing/opening |
| 057e:2007 (R) | Same bracket-pattern line as 2006 | Same |
| 057e:2008 (virtual pair) | **No matching identity-specific rule** in this pinned file | Not a denial; virtual device may have independent evdev policy |
| 057e:200e (Charging Grip) | **No matching identity-specific rule** in this pinned file | No claim about inherited/generic seat permissions |

Do not transpose the 2009 Pro Controller USB/BT rules onto Joy-Con or infer closed-source Steam Input internal behavior from these grants.

## E2. joycond files and service

| Pinned joycond file | Host policy | Significance for #258 |
| --- | --- | --- |
| `udev/72-joycond.rules` | Grants `uaccess` to Nintendo IMU event nodes for 2006/2007/200e; removes `uaccess` from the physical main event nodes (not Combined/Virtual/IMU) | Userspace consumers may see the sensor node yet not be allowed the raw main event node |
| `udev/89-joycond.rules` | Tags physical main event nodes `joycond`, changes mode to `0600`; explicitly excludes Combined, Virtual and IMU nodes | Daemon uses exclusive physical main nodes to create a separate virtual combined device |
| `systemd/joycond.service` | Service starts joycond as root and restarts it; enabled under multi-user.target | Root permission is relied on for main input and virtual controller creation; not proof that all distributions deploy the unit |
| `systemd/joycond.conf` | Declares the LED timer module for boot | Player LED flashing dependency, not an evdev or hidraw ACL |
| `/dev/uinput` access | The public service runs with root privileges; `uinput` is required for synthetic combined output | A non-root alternative would need separate authorization; not established by these files |

**Important interaction:** steam-devices grants raw HID access to 2006/2007, while joycond may hide the kernel-produced main event nodes. These are different access surfaces and should be audited separately; rules' file ordering and distribution integration may affect effective ACL. The pinned joycond hidraw denial targets **Pro 2009**, not the Joy-Con half PIDs.

## Proposed #258 host checks (all not run)

Inspect the effective rule ordering and ACL for HID raw, physical main and IMU event nodes; verify active-seat login and root daemon access; test SDL HIDAPI vs SDL evdev vs joycond on the *same* Joy-Con instance; verify no virtual pad duplicates or feedback loops. Record versions and a sanitized access matrix, not host paths or identifier instances.

**Cloud agent (Joy-Con research)**
