import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CONTROLLERS = ("switch-pro", "dualsense", "dualshock4", "xbox360")
class ConsumerSurveyG(unittest.TestCase):
    def test_all_surveys_ranked_and_not_run(self):
        for name in CONTROLLERS:
            with self.subTest(controller=name):
                text = (ROOT / "docs" / (name + "-consumer-survey.md")).read_text()
                self.assertIn("Research parity, part 2: consumers and decisions", text)
                self.assertIn("not run", text)
                self.assertIn("No evidence", text)
                for consumer in ("Steam Input", "SDL3", "SDL2", "Wine", "RetroArch",
                                 "InputPlumber", "HHD", "Dolphin", "Chromium"):
                    self.assertIn(consumer, text)
                record = json.loads((ROOT / "records/claim" /
                                     ("parity-g-" + name + "-consumer-routing.json")).read_text())
                self.assertEqual(record["applicability"]["controller"], name)
                self.assertEqual(record["applicability"]["transport"], "source_only")
                self.assertEqual(record["evidence_role"], "consumer")
                self.assertEqual(record["status"], "source_supported")
                self.assertEqual(record["experiments"], [])
if __name__ == "__main__":
    unittest.main()
