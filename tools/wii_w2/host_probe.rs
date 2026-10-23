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
fn attach(c: &mut WiiRemoteController, phase: usize) {
    let ext = match phase {
        1 => WiiExtension::Nunchuk(WiiNunchukState::default()),
        2 => WiiExtension::Classic(WiiClassicState::default()),
        _ => WiiExtension::None,
    };
    c.attach(ext, phase == 3).unwrap();
}
fn values(c: &mut WiiRemoteController, phase: usize) {
    c.set_accelerometer([600, 400, 512]).unwrap();
    c.set_ir([Some(WiiIrPoint::new(123, 234).unwrap()), None, None, None])
        .unwrap();
    match phase {
        1 => c
            .set_extension(WiiExtension::Nunchuk(WiiNunchukState {
                stick: [150, 100],
                accelerometer: [600, 400, 512],
                c: true,
                z: false,
            }))
            .unwrap(),
        2 => {
            let mut s = WiiClassicState::default();
            s.left = [50, 20];
            s.right = [20, 10];
            s.triggers = [4, 9];
            s.buttons[0] = true;
            c.set_extension(WiiExtension::Classic(s)).unwrap();
        }
        3 => c.set_motion_plus([9000, 8000, 8192], [true; 3]).unwrap(),
        _ => {}
    }
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
fn main() {
    let directory = PathBuf::from(std::env::args().nth(1).expect("output directory"));
    fs::create_dir_all(&directory).unwrap();
    let sdl_helper = PathBuf::from(std::env::args().nth(2).expect("SDL helper executable"));
    let revision = std::env::args().nth(3).expect("source revision");
    let mut c = create_wii_remote(RealizationTarget::LINUX_UHID_BLUETOOTH, 1).unwrap();
    c.set_battery_raw(192).unwrap();
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
        let writes: Vec<_> = leds
            .iter()
            .map(|p| {
                let result = fs::write(p, "1");
                json!({"success":result.is_ok(),"errno":result.err().and_then(|e|e.raw_os_error())})
            })
            .collect();
        pump(&mut c, 100);
        let outputs = c.host_outputs().unwrap();
        fs::write(
            directory.join("led-result.json"),
            serde_json::to_vec_pretty(&json!({"writes":writes,"retained_leds":outputs.leds}))
                .unwrap(),
        )
        .unwrap();
        for mode in ["sdl-default-hints", "sdl-wii-enabled"] {
            let nodes = inputs(&c);
            let core = nodes
                .iter()
                .find(|(n, _)| n == "Nintendo Wii Remote")
                .unwrap();
            let mut command = Command::new(&sdl_helper);
            command.arg(&raw).arg(&core.1);
            for (key, _) in std::env::vars() {
                if key.starts_with("SDL_") {
                    command.env_remove(key);
                }
            }
            command.env_remove("W1_ENUMERATE_ALL");
            if mode == "sdl-wii-enabled" {
                command.env("W2_ENABLE_WII", "1");
            } else {
                command.env_remove("W2_ENABLE_WII");
            }
            let stdout = directory.join(format!("{mode}.stdout"));
            let stderr = directory.join(format!("{mode}.stderr"));
            let mut child = command
                .stdout(fs::File::create(&stdout).unwrap())
                .stderr(fs::File::create(&stderr).unwrap())
                .spawn()
                .unwrap();
            let mut observations = Vec::new();
            let mut shapes = Vec::new();
            for phase in 0..4 {
                attach(&mut c, phase);
                pump(&mut c, 300);
                let current:Vec<_> = inputs(&c).iter().map(|(name, path)| {
                    let event = path.file_name().unwrap();
                    let caps = PathBuf::from("/sys/class/input").join(event).join("device/capabilities");
                    json!({"name":name,"keys":fs::read_to_string(caps.join("key")).unwrap().trim(),"abs":fs::read_to_string(caps.join("abs")).unwrap().trim()})
                }).collect();
                shapes.push(json!({"phase":phase,"nodes":current}));
                let start = Instant::now();
                while start.elapsed() < Duration::from_secs(4)
                    && child.try_wait().unwrap().is_none()
                {
                    values(&mut c, phase);
                    pump(&mut c, 1);
                    let value = c.host_outputs().unwrap();
                    let item = json!({"phase":phase,"leds":value.leds,"rumble":value.rumble});
                    if observations.last() != Some(&item) {
                        observations.push(item);
                    }
                }
            }
            wait(&mut c, &mut child, 4);
            let status = child.wait().unwrap();
            fs::write(directory.join(format!("{mode}.json")),serde_json::to_vec_pretty(&json!({"code":status.code(),"success":status.success(),"stdout":fs::read_to_string(stdout).unwrap(),"stderr":fs::read_to_string(stderr).unwrap(),"outputs":observations,"shapes":shapes})).unwrap()).unwrap();
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
