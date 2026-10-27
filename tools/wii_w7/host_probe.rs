use gr_curated_controllers::wii_remote::*;
use gr_realization_api::RealizationTarget;
use serde_json::json;
use std::{
    fs,
    io::Write,
    path::PathBuf,
    sync::{
        OnceLock,
        atomic::{AtomicU64, Ordering},
    },
    time::{Duration, Instant},
};
static TRACE: OnceLock<PathBuf> = OnceLock::new();
static PHASE: AtomicU64 = AtomicU64::new(0);
fn pump(c: &mut WiiRemoteController, ms: u64) {
    let end = Instant::now() + Duration::from_millis(ms);
    while Instant::now() < end {
        c.service(&mut |event| {
            if let gr_realization_api::RawReverseEvent::HidOutput { report_id, bytes } = event {
                let path = TRACE.get().unwrap();
                let mut f = fs::OpenOptions::new().append(true).create(true).open(path).unwrap();
                writeln!(f, "{}", json!({"kind":"host-output","id":report_id,"bytes":bytes,"phase":PHASE.load(std::sync::atomic::Ordering::Relaxed)})).unwrap();
            }
        }).unwrap();
        if c.is_dirty() {
            if let Err(e) = c.commit() {
                assert!(!c.is_closed(), "{e}");
            }
        }
        std::thread::sleep(Duration::from_millis(1));
    }
}
fn owned(c: &WiiRemoteController) -> Option<PathBuf> {
    let phys = c.association().requested_physical_path.as_ref()?;
    fs::read_dir("/sys/bus/hid/devices")
        .ok()?
        .flatten()
        .map(|e| e.path())
        .find(|p| {
            fs::read_to_string(p.join("uevent")).ok().is_some_and(|s| {
                s.lines()
                    .any(|l| l.strip_prefix("HID_PHYS=") == Some(phys.as_str()))
            })
        })
}
#[allow(dead_code)]
fn inputs(c: &WiiRemoteController) -> Vec<(String, PathBuf)> {
    let roots: Vec<PathBuf> = if let Some(hid) = owned(c) {
        fs::read_dir(hid.join("input"))
            .into_iter()
            .flatten()
            .flatten()
            .map(|e| e.path())
            .collect()
    } else {
        let mut labels = vec![c.association().requested_physical_path.clone()];
        labels.extend(
            c.association()
                .companions
                .iter()
                .map(|a| a.requested_physical_path.clone()),
        );
        fs::read_dir("/sys/class/input")
            .unwrap()
            .flatten()
            .map(|e| e.path())
            .filter(|p| {
                p.file_name()
                    .unwrap()
                    .to_string_lossy()
                    .starts_with("input")
                    && fs::read_to_string(p.join("phys"))
                        .ok()
                        .is_some_and(|s| labels.iter().flatten().any(|label| label == s.trim()))
            })
            .collect()
    };
    let mut result = Vec::new();
    for root in roots {
        let name = fs::read_to_string(root.join("name"))
            .unwrap()
            .trim()
            .to_string();
        for event in fs::read_dir(&root).unwrap().flatten() {
            if event.file_name().to_string_lossy().starts_with("event") {
                result.push((
                    name.clone(),
                    PathBuf::from("/dev/input").join(event.file_name()),
                ));
            }
        }
    }
    result.sort();
    result
}
fn configure(c: &mut WiiRemoteController, case: &str) {
    let ext = match case {
        "nunchuk" | "motionplus-nunchuk" => WiiExtension::Nunchuk(WiiNunchukState::default()),
        "classic" => WiiExtension::Classic(WiiClassicState::default()),
        _ => WiiExtension::None,
    };
    c.attach(ext, case.starts_with("motionplus")).unwrap();
}
fn drive(c: &mut WiiRemoteController, case: &str, high: bool) {
    c.set_button(WiiRemoteButton::A, high).unwrap();
    c.set_accelerometer(if high {
        [600, 400, 700]
    } else {
        [400, 600, 500]
    })
    .unwrap();
    if case == "nunchuk" || case == "motionplus-nunchuk" {
        c.set_extension(WiiExtension::Nunchuk(WiiNunchukState {
            stick: if high { [180, 70] } else { [70, 180] },
            accelerometer: if high {
                [600, 400, 700]
            } else {
                [400, 600, 500]
            },
            c: high,
            z: !high,
        }))
        .unwrap();
    }
    if case == "classic" {
        let mut state = WiiClassicState::default();
        state.left = if high { [50, 12] } else { [12, 50] };
        state.right = if high { [25, 6] } else { [6, 25] };
        state.triggers = if high { [25, 6] } else { [6, 25] };
        state.buttons[0] = high;
        c.set_extension(WiiExtension::Classic(state)).unwrap();
    }
    if case.starts_with("motionplus") {
        c.set_motion_plus(
            if high {
                [9000, 7000, 8500]
            } else {
                [7000, 9000, 7800]
            },
            [true; 3],
        )
        .unwrap();
    }
    c.commit().unwrap();
}
fn main() {
    let dir = PathBuf::from(std::env::args().nth(1).unwrap());
    fs::create_dir_all(&dir).unwrap();
    TRACE.set(dir.join("private-host-output.jsonl")).unwrap();
    let mut c = create_wii_remote(RealizationTarget::LINUX_UHID_BLUETOOTH, 71).unwrap();
    c.set_battery_raw(192).unwrap();
    configure(&mut c, "motionplus-nunchuk");
    pump(&mut c, 2000);
    let root = owned(&c).unwrap().canonicalize().unwrap();
    assert!(root.starts_with("/sys/devices/virtual/misc/uhid"));
    let text = fs::read_to_string(root.join("uevent")).unwrap();
    let phys = c.association().requested_physical_path.as_ref().unwrap();
    assert!(text.lines().any(|l| l == "HID_ID=0005:0000057E:00000306"));
    assert!(
        text.lines()
            .any(|l| l.strip_prefix("HID_PHYS=") == Some(phys.as_str()))
    );
    assert_eq!(
        fs::read_link(root.join("driver"))
            .unwrap()
            .file_name()
            .unwrap(),
        "wiimote"
    );
    let raw = PathBuf::from("/dev").join(
        fs::read_dir(root.join("hidraw"))
            .unwrap()
            .next()
            .unwrap()
            .unwrap()
            .file_name(),
    );
    let mut leds: Vec<_> = fs::read_dir(root.join("leds"))
        .unwrap()
        .map(|e| e.unwrap().path().join("brightness"))
        .collect();
    leds.sort();
    assert_eq!(leds.len(), 4);
    fs::write(dir.join("grant.json"),serde_json::to_vec_pretty(&json!({"root":root,"phys":phys,"hidraw":raw,"leds":leds,"inputs":inputs(&c),"source":std::env::args().nth(2).unwrap()})).unwrap()).unwrap();
    println!("OWNED_DEVICE_READY");
    std::io::stdout().flush().unwrap();
    let end = Instant::now() + Duration::from_secs(3600);
    let mut last = 0;
    let mut uc: Option<WiiRemoteController> = None;
    let mut uactive = false;
    let mut case = "motionplus-nunchuk".to_owned();
    while !dir.join("done").exists() && Instant::now() < end {
        pump(&mut c, 10);
        if let Some(u) = &mut uc {
            pump(u, 1);
        }
        if !dir.join("go").exists() {
            continue;
        }
        if let Ok(cmd) = fs::read(dir.join("command.json")) {
            let cmd: serde_json::Value = serde_json::from_slice(&cmd).unwrap();
            let id = cmd["id"].as_u64().unwrap();
            if id != last {
                last = id;
                PHASE.store(id, Ordering::Relaxed);
                case = cmd["case"].as_str().unwrap().to_owned();
                uactive = cmd["target"] == "uinput";
                if uactive && uc.is_none() {
                    uc = Some(create_wii_remote(RealizationTarget::LINUX_UINPUT, 72).unwrap());
                }
                if !uactive {
                    if let Some(mut u) = uc.take() {
                        u.close();
                        u.close();
                    }
                }
                let active = if uactive {
                    uc.as_mut().unwrap()
                } else {
                    &mut c
                };
                configure(active, &case);
                drive(active, &case, false);
                pump(active, 1500);
                fs::write(dir.join("ready.json"),serde_json::to_vec_pretty(&json!({"id":id,"target":cmd["target"],"case":case,"root":if uactive{None}else{Some(&root)},"inputs":inputs(active)})).unwrap()).unwrap();
            }
        }
        if last > 0 {
            let active = if uactive {
                uc.as_mut().unwrap()
            } else {
                &mut c
            };
            drive(
                active,
                &case,
                (end.duration_since(Instant::now()).as_millis() / 250) % 2 == 1,
            );
        }
    }
    if let Some(mut u) = uc.take() {
        u.close();
        u.close();
    }
    c.close();
    c.close();
    assert!(!root.exists());
    assert!(!raw.exists());
    fs::write(
        dir.join("closed"),
        b"both owned sessions closed idempotently; HID/raw removed",
    )
    .unwrap();
}
