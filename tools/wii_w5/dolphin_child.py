#!/usr/bin/python3
import sys,os,json,pathlib,subprocess
raw,event,arm=sys.argv[1:4]
case=os.environ['W5_CASE']
cache=os.environ['W5_DOLPHIN_CACHE']
profile=pathlib.Path(cache)/case
(profile/'Config').mkdir(parents=True,exist_ok=False)
(profile/'Config/WiimoteNew.ini').write_text(''.join(f'[Wiimote{i}]\nSource = 0\n'for i in range(1,5))+'[BalanceBoard]\nSource = 0\n')
(profile/'Config/Dolphin.ini').write_text('[Core]\nWiimoteContinuousScanning = True\nWiimoteControllerInterface = True\nWiimoteEnableSpeaker = False\n[Input]\nBackgroundInput = True\n')
(profile/'Config/Logger.ini').write_text('[Options]\nVerbosity = 5\nWriteToFile = False\nWriteToConsole = True\n[Logs]\nWiimote = True\nControllerInterface = True\n')
# Never allow the direct Wii scanner to open a different Nintendo Wii device.
owned=pathlib.Path('/sys/class/hidraw',pathlib.Path(raw).name,'device').resolve()
for node in pathlib.Path('/sys/class/hidraw').iterdir():
 dev=(node/'device').resolve()
 info=(dev/'uevent').read_text()
 hid_id=next((line.split('=',1)[1] for line in info.splitlines() if line.startswith('HID_ID=')), '')
 parts=hid_id.split(':')
 if len(parts)==3 and int(parts[1],16)==0x057e and int(parts[2],16) in (0x0306,0x0330):
  assert dev==owned,'Another Wii HID is present; bounded exact-owned check refused'
cmd=['timeout','--signal=TERM','--kill-after=2','45','flatpak','run','--env=QT_QPA_PLATFORM=offscreen',f'--env=LD_PRELOAD={cache}/trace.so',f'--env=W5_TRACE={cache}/{case}-raw.jsonl','--env=W5_ROLE=dolphin',f'--env=W5_RAW={raw}',f'--env=W5_CASE={case}','--env=W5_ARM=dolphin','--env=SDL_JOYSTICK_HIDAPI_WII=0','--command=sh','org.DolphinEmu.dolphin-emu','-c','if ( : <> "$1" ) 2>/dev/null; then echo OWNED_RAW_OPEN_OK; else echo OWNED_RAW_OPEN_DENIED; exit 3; fi; exec dolphin-emu --user "$2"','w5-dolphin',raw,str(profile)]
status=subprocess.run(cmd,check=False).returncode
print(json.dumps({'kind':'bounded_dolphin_exit','exit_code':status,'profile':case,'no_rom':True,'direct_controller_interface':True,'sdl_wii_disabled':True}))
# A bounded termination is expected; distinguish application signals from success.
sys.exit(0 if status==124 else status)
