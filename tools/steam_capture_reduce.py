"""Fail-closed reduction of *manually classified* Steam 1302 USB transfers.

Not a pcap/usbmon parser and not a public-disclosure authorization.
Input is local JSONL: session, kind, t_rel_ms, report_hex, and optional
inner_command for feature transfers. Only reviewed transfer payloads belong here.
"""
import argparse
import json
import math
import re
from pathlib import Path

ALLOWED_INPUT = {0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x47, 0x79, 0x7B}
ALLOWED_OUTPUT = set(range(0x80, 0x8A))
KINDS = {"input", "output", "feature_request", "feature_reply"}
SAFE_FIELDS = {"session", "kind", "t_rel_ms", "report_hex", "inner_command"}


def reduce_record(row):
    if not isinstance(row, dict):
        raise ValueError("record must be an object")
    kind = row.get("kind")
    if kind not in KINDS:
        raise ValueError("unrecognized transfer kind (fail closed)")
    session = row.get("session")
    if session not in ("S0", "S1", "S2", "S3"):
        raise ValueError("session must be S0/S1/S2/S3")
    when = row.get("t_rel_ms")
    if isinstance(when, bool) or not isinstance(when, (int, float)) or not math.isfinite(when) or when < 0:
        raise ValueError("only nonnegative relative milliseconds are allowed")
    raw = row.get("report_hex")
    if not isinstance(raw, str) or not re.fullmatch(r"[0-9a-fA-F\s:]+", raw):
        raise ValueError("report_hex must be nonempty hex")
    raw = raw.replace(":", "").replace(" ", "").replace("\n", "").replace("\t", "")
    if len(raw) % 2:
        raise ValueError("odd-length report_hex")
    packet = bytes.fromhex(raw)
    if not packet:
        raise ValueError("empty report")
    # Construct an entirely new output object: no copied URB IDs, bus addresses,
    # host paths, account data, serial/unique IDs or wall-clock metadata.
    result = {"session": session, "kind": kind,
              "t_rel_ms": round(when, 3), "report_id": f"0x{packet[0]:02x}",
              "wire_bytes": len(packet)}
    if kind == "input" and packet[0] not in ALLOWED_INPUT:
        raise ValueError("unreviewed input ID")
    if kind == "output" and packet[0] not in ALLOWED_OUTPUT:
        raise ValueError("unreviewed output ID")
    if kind in ("input", "output"):
        # Human review STILL required before publishing these bytes. The ID is
        # part of the wire length; keeping the trailing extension is deliberate.
        result["report_hex"] = packet.hex()
    else:
        # Never publish raw feature payloads: 0xae can contain unique serial;
        # 0x83 attributes may contain unique identifiers. Even an unsalted
        # digest of a low-entropy identifier could be identifying.
        command = row.get("inner_command")
        if command is not None:
            if isinstance(command, bool):
                raise ValueError("invalid feature command")
            if isinstance(command, str):
                try:
                    command = int(command, 0)
                except ValueError as error:
                    raise ValueError("invalid feature command") from error
            if not isinstance(command, int) or not 0 <= command <= 255:
                raise ValueError("invalid feature command")
            result["inner_command"] = f"0x{command:02x}"
        result["payload_withheld"] = True
    return result


def reduce_jsonl(source, destination):
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError("do not overwrite private input")
    rows = []
    for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(reduce_record(json.loads(line)))
        except (ValueError, TypeError) as error:
            raise ValueError(f"private input line {number}: {error}") from error
    # No partial output if a later row is invalid.
    destination.write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in rows), encoding="utf-8")
    return len(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("private_jsonl")
    p.add_argument("review_only_jsonl")
    args = p.parse_args()
    print("Reduced", reduce_jsonl(args.private_jsonl, args.review_only_jsonl),
          "classified transfers; HUMAN REVIEW REQUIRED before disclosure")


if __name__ == "__main__":
    main()
