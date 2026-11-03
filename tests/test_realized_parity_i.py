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
    def test_status_before_after_role_correction(self):
        import sys
        from unittest.mock import patch
        sys.path.insert(0,str(ROOT/"tools"))
        import status as status_module
        original=status_module.load
        corrected={"ds-l0-hhd-steam-gyro-policy","ds-l0-hhd-feature-replies"}
        def before_role(root, category):
            rows=original(root,category)
            if category=="claim":
                for item in rows:
                    if item["id"] in corrected:
                        item["evidence_role"]="device"
            return rows
        with patch.object(status_module,"load",side_effect=before_role):
            before=next(x for x in status_module.status(ROOT) if x["id"]=="dualsense")
        after=next(x for x in status_module.status(ROOT) if x["id"]=="dualsense")
        self.assertEqual(sum(before["claims"].values()),sum(after["claims"].values()))
        print("\\n| controller | device before -> after | consumer before -> after | claims before -> after |")
        print(f"| dualsense | {before['category']} -> {after['category']} | "
              f"{before['consumer_category']} -> {after['consumer_category']} | "
              f"{sum(before['claims'].values())} -> {sum(after['claims'].values())} |")

if __name__=="__main__": unittest.main()
