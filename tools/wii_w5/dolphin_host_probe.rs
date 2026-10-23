use gr_curated_controllers::wii_remote::*;
use gr_realization_api::RealizationTarget;
use serde_json::json;
use std::{
    fs,
    io::Write,
    path::PathBuf,
    process::{Child, Command},
    time::{Duration, Instant},
};
fn pump(c: &mut WiiRemoteController, ms: u64) {
    let end = Instant::now() + Duration::from_millis(ms);
    while Instant::now() < end {
        c.service(&mut |_| {}).unwrap();
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
    c.set_accelerometer(if high { [600, 400, 700] } else { [400, 600, 500] }).unwrap();
    if case == "nunchuk" || case == "motionplus-nunchuk" {
        c.set_extension(WiiExtension::Nunchuk(WiiNunchukState {
            stick: if high { [180, 70] } else { [70, 180] },
            accelerometer: if high { [600, 400, 700] } else { [400, 600, 500] },
            c: high, z: !high,
        })).unwrap();
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
        c.set_motion_plus(if high { [9000, 7000, 8500] } else { [7000, 9000, 7800] }, [true; 3]).unwrap();
    }
    c.commit().unwrap();
}
fn wait(c: &mut WiiRemoteController, child: &mut Child, seconds: u64) {
    let end = Instant::now() + Duration::from_secs(seconds);
    while child.try_wait().unwrap().is_none() && Instant::now() < end {
        pump(c, 1);
    }
    if child.try_wait().unwrap().is_none() {
        child.kill().unwrap();
    }
}
fn monotonic_ns() -> u64 {
    std::fs::read_to_string("/proc/uptime")
        .unwrap()
        .split_whitespace()
        .next()
        .unwrap()
        .parse::<f64>()
        .map(|n| (n * 1e9) as u64)
        .unwrap()
}
fn main() {
    let directory = PathBuf::from(std::env::args().nth(1).expect("output directory"));
    fs::create_dir_all(&directory).unwrap();
    let sdl_helper = PathBuf::from(std::env::args().nth(2).expect("SDL helper executable"));
    let revision = std::env::args().nth(3).expect("source revision");
    let mut c = create_wii_remote(RealizationTarget::LINUX_UHID_BLUETOOTH, 1).unwrap();
    c.set_battery_raw(192).unwrap();
    c.attach(WiiExtension::None, true).unwrap();
    pump(&mut c, 2000);
    let root = owned(&c)
        .expect("exact creation-owned HID")
        .canonicalize()
        .unwrap();
    assert!(root.starts_with("/sys/devices/virtual/misc/uhid"));
    let uevent = fs::read_to_string(root.join("uevent")).unwrap();
    assert!(
        uevent
            .lines()
            .any(|line| line == "HID_ID=0005:0000057E:00000306")
    );
    let expected = c.association().requested_physical_path.as_ref().unwrap();
    assert!(
        uevent
            .lines()
            .any(|line| line.strip_prefix("HID_PHYS=") == Some(expected))
    );
    let driver = fs::read_link(root.join("driver")).unwrap();
    assert_eq!(driver.file_name().unwrap(), "wiimote");
    let raw_name = fs::read_dir(root.join("hidraw"))
        .unwrap()
        .flatten()
        .next()
        .unwrap()
        .file_name();
    assert_eq!(
        fs::canonicalize(
            PathBuf::from("/sys/class/hidraw")
                .join(&raw_name)
                .join("device")
        )
        .unwrap(),
        root
    );
    let raw = PathBuf::from("/dev").join(raw_name);
    let mut leds: Vec<_> = fs::read_dir(root.join("leds"))
        .unwrap()
        .flatten()
        .map(|e| e.path().join("brightness"))
        .collect();
    leds.sort();
    assert_eq!(leds.len(), 4);
    assert!(
        leds.iter()
            .all(|p| p.canonicalize().unwrap().starts_with(&root))
    );
    fs::write(directory.join("grant.json"), serde_json::to_vec_pretty(&json!({"root":root,"phys":expected,"hidraw":raw,"leds":leds,"bus":5,"vid":1406,"pid":774,"driver":"wiimote","source":revision})).unwrap()).unwrap();
    fs::write(
        directory.join("descriptor.bin"),
        fs::read(root.join("report_descriptor")).unwrap(),
    )
    .unwrap();
    let until = Instant::now() + Duration::from_secs(7200);
    println!("OWNED_DEVICE_READY");
    std::io::stdout().flush().unwrap();
    let mut performed = false;
    while !directory.join("done").exists() && Instant::now() < until {
        pump(&mut c, 10);
        if !directory.join("go").exists() || performed {
            continue;
        }
        performed = true;
        for arm in ["dolphin"] {
            if arm == "control" {
                fs::write(directory.join("h3-complete"), b"kernel-first captures ready").unwrap();
                while !directory.join("h3-verified").exists() && Instant::now() < until && !directory.join("done").exists() { pump(&mut c, 20); }
                if !directory.join("h3-verified").exists() { break; }
            }
            for case in ["motionplus", "motionplus-nunchuk"] {
                configure(&mut c, case);
                drive(&mut c, case, false);
                pump(&mut c, 2500);
                let nodes = inputs(&c);
                let mp = nodes.iter().find(|(name, _)| name == "Nintendo Wii Remote Motion Plus").expect("owned MotionPlus node");
                let mut command = Command::new(&sdl_helper);
                command.arg(&raw).arg(&mp.1).arg(arm);
                for (key, _) in std::env::vars() { if key.starts_with("SDL_") { command.env_remove(key); } }
                command.env_remove("LD_PRELOAD").env_remove("W5_TRACE").env("W5_ROLE", "dolphin").env("W5_RAW", &raw).env("W5_CASE", case).env("W5_ARM", arm);
                let label = format!("{case}-{arm}");
                let stdout = directory.join(format!("{label}.stdout"));
                let stderr = directory.join(format!("{label}.stderr"));
                let mut child = command.stdout(fs::File::create(&stdout).unwrap()).stderr(fs::File::create(&stderr).unwrap()).spawn().unwrap();
                let start = Instant::now();
                while child.try_wait().unwrap().is_none() && start.elapsed() < Duration::from_secs(100) {
                    drive(&mut c, case, (start.elapsed().as_millis() / 250) % 2 == 1);
                    pump(&mut c, 20);
                }
                wait(&mut c, &mut child, 1);
                let status = child.wait().unwrap();
                fs::write(directory.join(format!("{label}.json")), serde_json::to_vec_pretty(&json!({"success": status.success(), "exit_code": status.code(), "stdout": fs::read_to_string(stdout).unwrap(), "stderr": fs::read_to_string(stderr).unwrap(), "attachment_before_open": true, "attachment_changes_during_child": 0})).unwrap()).unwrap();
                println!("CASE_COMPLETE {label}"); std::io::stdout().flush().unwrap();
            }
        }
        fs::write(
            directory.join("runs-complete"),
            b"bounded granted runs complete",
        )
        .unwrap();
    }
    c.close();
    c.close();
    assert!(!root.exists());
    fs::write(directory.join("closed"), b"owned HID gone").unwrap();
}
