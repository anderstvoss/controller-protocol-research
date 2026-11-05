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
        row = dict(session="S2", kind="input", t_rel_ms=32.125,
                   report_hex="42 00 00")
        row.update(kw)
        return row

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

    def feature(self, command, payload, *, kind="feature_reply", length=63):
        packet = bytes([1, command, len(payload)]) + payload
        packet += bytes(max(0, length - len(packet)))
        return self.example(kind=kind, inner_command=command, report_hex=packet.hex())

    def test_model_attributes_require_opt_in_and_never_copy_feature_bytes(self):
        row = self.feature(0x83, bytes([9, 42, 0, 0, 0]))
        self.assertNotIn("attributes", module.reduce_record(row))
        out = module.reduce_record(row, model_attributes=True)
        self.assertEqual(out["attributes"], [{"id": 9, "value": 42}])
        self.assertTrue(out["payload_withheld"])
        self.assertNotIn("report_hex", out)
        for tag in (0, 6, 7, 255):
            with self.assertRaisesRegex(ValueError, "unreviewed"):
                module.reduce_record(self.feature(0x83, bytes([tag, 1, 2, 3, 4])),
                                     model_attributes=True)

    def test_serial_remains_withheld_even_with_both_model_options(self):
        row = self.feature(0xae, b"FAKE-ID", kind="feature_reply")
        out = module.reduce_record(row, model_attributes=True, model_settings=True)
        self.assertNotIn("attributes", out)
        self.assertNotIn("settings", out)
        self.assertNotIn("report_hex", out)
        self.assertNotIn("FAKE-ID", json.dumps(out))

    def test_model_settings_preserve_order_duplicates_and_u16_values(self):
        row = self.feature(0x87, bytes([50, 0x34, 0x12, 9, 0, 0, 50, 0xff, 0xff]),
                           kind="feature_request", length=64)
        self.assertNotIn("settings", module.reduce_record(row))
        out = module.reduce_record(row, model_settings=True)
        self.assertEqual(out["settings"], [{"key": 50, "value": 0x1234},
                                          {"key": 9, "value": 0},
                                          {"key": 50, "value": 65535}])
        with self.assertRaisesRegex(ValueError, "unreviewed"):
            module.reduce_record(self.feature(0x87, bytes([255, 0, 0]),
                                              kind="feature_request"), model_settings=True)

    def test_model_options_reject_bad_lengths_and_report_command_mismatch(self):
        for command, payload, option in [(0x83, bytes([9, 1, 2, 3]), "model_attributes"),
                                         (0x87, bytes([50, 0]), "model_settings")]:
            kind = "feature_reply" if command == 0x83 else "feature_request"
            with self.assertRaises(ValueError):
                module.reduce_record(self.feature(command, payload, kind=kind), **{option: True})
            row = self.feature(command, b"", kind=kind)
            for replacement in ("02" + row["report_hex"][2:],
                                row["report_hex"][:4] + "ff" + row["report_hex"][6:],
                                row["report_hex"][:-2],
                                row["report_hex"][:2] + "ae" + row["report_hex"][4:]):
                with self.assertRaises(ValueError):
                    module.reduce_record({**row, "report_hex": replacement}, **{option: True})

    def test_model_jsonl_late_failure_does_not_publish_partial_values(self):
        with tempfile.TemporaryDirectory() as td:
            source, dest = Path(td) / "private.jsonl", Path(td) / "review.jsonl"
            source.write_text("\n".join(json.dumps(self.feature(0x83, bytes([tag, 1, 0, 0, 0])))
                                        for tag in (9, 0)) + "\n")
            with self.assertRaises(ValueError):
                module.reduce_jsonl(source, dest, model_attributes=True)
            self.assertFalse(dest.exists())


if __name__ == "__main__":
    unittest.main()
