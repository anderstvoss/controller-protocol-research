"""Safety tests for the manual, review-only Steam HID transfer reducer."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "steam_capture_reduce", ROOT / "tools" / "steam_capture_reduce.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SteamCaptureReduceTests(unittest.TestCase):
    def example(self, **kw):
        return dict(session="S2", kind="input", t_rel_ms=32.125,
                    report_hex="42 00 00", **kw)

    def test_input_keeps_report_id_bytes_timing_but_no_metadata(self):
        row = self.example(serial_number="PRIVATE", host_path="PRIVATE",
                           urb_id="private", username="private")
        out = module.reduce_record(row)
        self.assertEqual(out["report_hex"], "420000")
        self.assertEqual(out["wire_bytes"], 3)
        self.assertEqual(out["report_id"], "0x42")
        self.assertEqual(out["t_rel_ms"], 32.125)
        self.assertEqual(set(out), {"session", "kind", "t_rel_ms",
                                    "report_id", "wire_bytes", "report_hex"})

    def test_feature_reply_never_leaks_serial_or_unique_id(self):
        for command in ("0xae", "0x83", "0x87", None):
            row = dict(session="S1", kind="feature_reply", t_rel_ms=2,
                       report_hex="01 53 45 52 49 41 4c", inner_command=command,
                       serial="PRIVATE")
            out = module.reduce_record(row)
            self.assertTrue(out["payload_withheld"])
            self.assertNotIn("report_hex", out)
            self.assertNotIn("53455249414c", json.dumps(out).upper())

    def test_output_preserves_haptic_stream_bytes_for_review(self):
        row = dict(session="S3", kind="output", t_rel_ms=2.25,
                   report_hex="89 03 02 00")
        out = module.reduce_record(row)
        self.assertEqual(out["report_hex"], "89030200")

    def test_unknown_report_and_bad_timing_fail_closed(self):
        for row in (
            self.example(report_hex="01 00"),
            dict(session="S2", kind="input", t_rel_ms=-1,
                 report_hex="42"),
            dict(session="S2", kind="input", t_rel_ms=1,
                 report_hex="bad"),
            dict(session="S2", kind="something", t_rel_ms=1,
                 report_hex="42"),
        ):
            with self.assertRaises(ValueError):
                module.reduce_record(row)

    def test_invalid_late_row_produces_no_partial_output(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "private.jsonl"
            dest = Path(td) / "review.jsonl"
            source.write_text(json.dumps(self.example()) + "\n" +
                              json.dumps(dict(session="S2", kind="output",
                                              t_rel_ms=1, report_hex="01")) + "\n")
            with self.assertRaises(ValueError):
                module.reduce_jsonl(source, dest)
            self.assertFalse(dest.exists())

    def test_jsonl_round_trip(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "private.jsonl"
            dest = Path(td) / "review.jsonl"
            source.write_text(json.dumps(self.example()) + "\n")
            self.assertEqual(module.reduce_jsonl(source, dest), 1)
            self.assertEqual(json.loads(dest.read_text())["report_hex"], "420000")


if __name__ == "__main__":
    unittest.main()
