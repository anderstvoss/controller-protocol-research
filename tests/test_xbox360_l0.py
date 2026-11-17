import json
import sys
import unittest
from pathlib import Path
from collections import Counter
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import status as status_module


class Xbox360L0Ledger(unittest.TestCase):
    def claims(self):
        return [json.loads(p.read_text()) for p in (ROOT / "records/claim").glob("x360-l0-*.json")]

    def test_roles_evidence_and_source_only(self):
        c = self.claims()
        self.assertEqual(len(c), 22)
        self.assertEqual(Counter(r["evidence_role"] for r in c),
                         {"device": 7, "consumer": 15})
        self.assertEqual(Counter(r["status"] for r in c),
                         {"source_supported": 18, "unknown": 4})
        self.assertTrue(all(x["applicability"]["controller"] == "xbox360" and x["sources"]
                            and not x["experiments"] and x["status"] != "physically_validated" for x in c))
        self.assertTrue(all(x["applicability"]["transport"] == "source_only"
                            for x in c if not x["id"].startswith("x360-l0-device-physical-")))
        self.assertTrue(all(x["applicability"]["transport"] == "usb"
                            for x in c if x["id"].startswith("x360-l0-device-physical-")))

    def test_device_sources_and_exp0016_usage_list(self):
        c = {x["id"]:x for x in self.claims()}
        self.assertIn("x360-l0-usbhost-wired", c["x360-l0-device-xusb-output-ff-led"]["sources"])
        self.assertIn("x360-l0-community-protor2", c["x360-l0-device-xusb-wired20"]["sources"])
        corrected = c["x360-l0-consumer-exp0016-hid-usage-correction"]
        self.assertIn("1,2,4,5,7,8,11,12,13,14,15", corrected["statement"])
        self.assertIn("vg-alpha1-exp0016", corrected["sources"])
        sources = ["x360-l0-community-protor2", "x360-l0-free60-archived-gamepad",
                   "x360-l0-usbhost-wired", "x360-l0-sdl-hidapi-360-320",
                   "x360-l0-sdl-hidapi-360-3418", "x360-l0-linux-hid-input"]
        for name in sources:
            src = json.loads((ROOT / "records/source" / (name + ".json")).read_text())
            self.assertEqual(len(src["sha256"]), 64)
            self.assertTrue(src["revision"] and src["locator"])

    def test_before_after_status(self):
        loader = status_module.load
        def no_f(root, category):
            rows = loader(root, category)
            return [x for x in rows if not x["id"].startswith("x360-l0-")] if category == "claim" else rows
        with patch.object(status_module, "load", side_effect=no_f):
            before = next(r for r in status_module.status(ROOT) if r["id"] == "xbox360")
        after = next(r for r in status_module.status(ROOT) if r["id"] == "xbox360")
        self.assertEqual(before["category"], "No evidence")
        self.assertEqual(after["category"], "Source evidence")
        self.assertEqual(before["consumer_category"], "Source evidence")
        self.assertEqual(after["consumer_category"], "Source evidence")
        self.assertEqual(sum(after["claims"].values()) - sum(before["claims"].values()), 22)
        print("\n| Controller | Device before → after | Consumer before → after | Claims before → after |")
        print("| --- | --- | --- | --- |")
        print(f"| xbox360 | {before['category']} → {after['category']} | "
              f"{before['consumer_category']} → {after['consumer_category']} | "
              f"{sum(before['claims'].values())} → {sum(after['claims'].values())} |")


if __name__ == "__main__":
    unittest.main()
