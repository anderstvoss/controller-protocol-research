import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class DecisionsI(unittest.TestCase):
    def test_roles_and_decision_labels(self):
        for id in ["ds-l0-hhd-steam-gyro-policy","ds-l0-hhd-feature-replies"]:
            o=json.loads((ROOT/"records/claim"/(id+".json")).read_text())
            self.assertEqual(o["evidence_role"],"consumer")
            self.assertEqual(o["status"],"source_supported")
        for id in ["switch-pro","dualsense","dualshock4","xbox360"]:
            text=(ROOT/"docs"/(id+"-decision-table.md")).read_text()
            for key in ["compat","faithful","unknown","No evidence","Calibration","Identity","not run"]:
                self.assertIn(key.lower(), text.lower())
            self.assertIn("What this settles",text)
        self.assertIn("ds4-l0-device-bt11-output",
                      (ROOT/"docs/dualshock4-decision-table.md").read_text())
if __name__=="__main__": unittest.main()
