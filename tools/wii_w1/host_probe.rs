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
    let args: Vec<_> = std::env::args().collect();
    let mode = &args[1];
    let target = if args.get(2).is_some_and(|s| s == "uinput") {
        RealizationTarget::LINUX_UINPUT
    } else {
        RealizationTarget::LINUX_UHID_BLUETOOTH
    };
    let before_fds = fs::read_dir("/proc/self/fd").unwrap().count();
    let mut touched = Vec::new();
    let mut c = create_wii_remote(target, 1).unwrap();
    pump(&mut c, 1800);
    let hid = owned(&c);
    let mut observations = vec![];
    if mode == "numeric" {
        for phase in 0..4 {
            attach(&mut c, phase);
            pump(&mut c, 1200);
            let nodes = inputs(&c);
            touched.extend(nodes.iter().map(|(_, p)| p.clone()));
            let out = std::env::temp_dir().join(format!(
                "wii-w1-axes-{}-{}.txt",
                std::process::id(),
                phase
            ));
            let mut child = Command::new("python3")
                .arg(PathBuf::from(&args[3]).join("event_probe.py"))
                .args(nodes.iter().map(|(_, p)| p))
                .stdout(fs::File::create(&out).unwrap())
                .spawn()
                .unwrap();
            let start = Instant::now();
            while child.try_wait().unwrap().is_none() && start.elapsed() < Duration::from_secs(4) {
                if start.elapsed() > Duration::from_millis(400)
                    && start.elapsed() < Duration::from_millis(1400)
                {
                    values(&mut c, phase);
                } else {
                    c.neutralize().unwrap();
                }
                pump(&mut c, 1);
            }
            if child.try_wait().unwrap().is_none() {
                child.kill().unwrap();
            }
            let status = child.wait().unwrap();
            observations.push(json!({"phase":phase,"roles":nodes.iter().map(|(n,_)|n).collect::<Vec<_>>(),"exit_success":status.success(),"probe":fs::read_to_string(&out).unwrap()}));
        }
    } else {
        let root = hid.as_ref().expect("UHID owned root");
        let raw = fs::read_dir(root.join("hidraw"))
            .unwrap()
            .flatten()
            .next()
            .unwrap()
            .file_name();
        let raw = PathBuf::from("/dev").join(raw);
        let nodes = inputs(&c);
        touched.extend(nodes.iter().map(|(_, p)| p.clone()));
        let core = nodes
            .iter()
            .find(|(n, _)| n == "Nintendo Wii Remote")
            .unwrap();
        let out = std::env::temp_dir().join(format!("wii-w1-consumer-{}.txt", std::process::id()));
        let mut command = if mode == "sdl" {
            let mut cmd = Command::new(&args[4]);
            cmd.arg(&raw).arg(&core.1);
            cmd
        } else {
            let mut cmd = Command::new("timeout");
            cmd.args(["--signal=TERM", "--kill-after=2", "18", "flatpak", "run", "--env=QT_QPA_PLATFORM=offscreen", "--command=sh", "org.DolphinEmu.dolphin-emu", "-c", r#"if [ -e "$1" ]; then echo W1_OWNED_HIDRAW_PRESENT; else echo W1_OWNED_HIDRAW_ABSENT; fi
if ( : <> "$1" ) 2>/dev/null; then echo W1_OWNED_HIDRAW_OPEN_OK; else echo W1_OWNED_HIDRAW_OPEN_DENIED; fi
profile=$(mktemp -d)
mkdir -p "$profile/Config"
cat > "$profile/Config/WiimoteNew.ini" <<'END_WIIMOTE'
[Wiimote1]
Source = 2
END_WIIMOTE
cat > "$profile/Config/Dolphin.ini" <<'END_CORE'
[Core]
WiimoteContinuousScanning = True
ConnectWiimotesForControllerInterface = True
WiimoteEnableSpeaker = False
END_CORE
cat > "$profile/Config/Logger.ini" <<'END_LOGGER'
[Options]
Verbosity = 4
WriteToFile = False
WriteToConsole = True
[Logs]
Wiimote = True
END_LOGGER
exec timeout --signal=TERM --kill-after=2 14 dolphin-emu --user "$profile""#]);
            cmd.arg("wii-w1").arg(&raw);
            cmd
        };
        let mut child = command
            .stdout(fs::File::create(&out).unwrap())
            .stderr(fs::File::create(out.with_extension("err")).unwrap())
            .spawn()
            .unwrap();
        let mut outputs = vec![];
        for phase in 0..4 {
            attach(&mut c, phase);
            let start = Instant::now();
            while start.elapsed() < Duration::from_secs(4) && child.try_wait().unwrap().is_none() {
                values(&mut c, phase);
                pump(&mut c, 1);
                let value = c.host_outputs().unwrap();
                let item = json!({"phase":phase,"leds":value.leds,"rumble":value.rumble});
                if outputs.last() != Some(&item) {
                    outputs.push(item);
                }
            }
        }
        wait(&mut c, &mut child, 4);
        let output = child.wait_with_output().unwrap();
        observations.push(json!({"mode":mode,"driver_bound":fs::read_link(root.join("driver")).unwrap().file_name().unwrap().to_string_lossy(),"exit_success":output.status.success(),"exit_code":output.status.code(),"stdout":fs::read_to_string(&out).unwrap(),"stderr":fs::read_to_string(out.with_extension("err")).unwrap(),"host_outputs":outputs}));
    }
    c.close();
    c.close();
    drop(c);
    let after_fds = fs::read_dir("/proc/self/fd").unwrap().count();
    println!(
        "{}",
        json!({"mode":mode,"target":args.get(2),"observations":observations,"owned_hid_gone":hid.as_ref().map(|h|!h.exists()),"owned_inputs_gone":touched.iter().all(|p| !p.exists()),"before_fds":before_fds,"after_fds":after_fds})
    );
    std::io::stdout().flush().unwrap();
}
