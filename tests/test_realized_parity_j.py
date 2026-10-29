import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PermissionsTimingJ(unittest.TestCase):
 def test_source_only_roles_and_4_cadences(self):
  ids=["parity-j-switch-pro-report-cadence","parity-j-dualsense-report-cadence",
       "parity-j-ds4-report-cadence","parity-j-xbox360-report-cadence"]
  for id in ids:
   o=json.loads((ROOT/"records/claim"/(id+".json")).read_text())
   self.assertEqual(o["evidence_role"],"consumer")
   self.assertEqual(o["applicability"]["transport"],"source_only")
   self.assertIn(o["status"],("inferred","unknown"))
  for p in (ROOT/"records/claim").glob("steam-client-udev-*.json"):
   if p.stem.endswith("-grants") or p.stem.endswith("-grant"):
    self.assertEqual(json.loads(p.read_text())["evidence_role"],"consumer")
  s=(ROOT/"docs/realized-controller-permissions.md").read_text()
  self.assertIn("ID_INPUT_JOYSTICK",s)
  self.assertIn("No evidence",s)
  self.assertIn("#166",s)
  self.assertIn("#258",s)
  for c in ("DualSense","DualShock4","Switch Pro","Xbox360"):
   self.assertIn(c,s)
if __name__=="__main__": unittest.main()
