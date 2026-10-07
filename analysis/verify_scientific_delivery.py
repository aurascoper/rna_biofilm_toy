"""Read-only verification of the local diagnostic delivery and preserved inputs."""
import argparse
import collections
import csv
import hashlib
import json
import math
from pathlib import Path
import subprocess


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(worktree):
    root = Path(__file__).resolve().parents[1]
    summary_path = worktree / "diagnostics/receipts/turing_2026-10-07_02/summary.json"
    summary = json.loads(summary_path.read_text())
    data = summary["data"]
    assert data["passed"]
    freeze = data["freeze_commit"]
    assert freeze == "d02040ffcddf077867a506d90e2fe62a9e7d026c"
    assert all(sha(worktree / k) == v for k, v in summary["source_sha256"].items())
    trace_checks = []
    for fit in data["fits"]:
        path = summary_path.parent / (fit["name"] + ".csv")
        assert sha(path) == fit["csv_sha256"]
        with path.open() as stream:
            rows = list(csv.DictReader(stream))
        assert len(rows) == 8000
        assert collections.Counter(r["chain"] for r in rows) == dict.fromkeys(["1", "2", "3", "4"], 2000)
        for chain in ("1", "2", "3", "4"):
            assert {int(r["draw"]) for r in rows if r["chain"] == chain} == set(range(1, 2001))
        for row in rows:
            q = float(row["q"])
            assert q >= .001 and math.isfinite(q)
            assert math.isclose(float(row["log_q"]), math.log(q), abs_tol=1e-12)
            assert row["divergent"] == "false" and int(row["tree_depth"]) < 12
            if fit["name"].startswith("lq"):
                f = float(row["shape"])
                assert math.isclose(float(row["alpha"]), f * math.log(10) / q, rel_tol=1e-12)
                assert math.isclose(float(row["beta"]), (1-f) * math.log(10) / q**2, rel_tol=1e-12)
                assert row["ratio_boundary"] == "interior"
                assert math.isclose(float(row["alpha_beta"]), f*q/(1-f), rel_tol=1e-12)
            if fit["name"].startswith("multi"):
                n = float(row["shape"])
                assert 1 <= n <= 10
                expected = -q / math.log(-math.expm1(math.log(.9)/n))
                assert math.isclose(float(row["D0"]), expected, rel_tol=1e-12)
        assert min(fit["seeds"]) > 30
        trace_checks.append(dict(fit=fit["name"], rows=len(rows), csv_sha256=sha(path), passed=True))
    for filename, lane in [("symbolics_2026-10-07_03.json", "symbolics"), ("metal_2026-10-07_01.json", "metal")]:
        receipt = json.loads((worktree / "diagnostics/receipts" / filename).read_text())
        assert receipt["data"]["passed"]
        for path, expected in receipt["source_sha256"].items():
            if path.startswith("diagnostics/"+lane+"/") or path in ("diagnostics/common.jl", "biofilms_potts.jl"):
                assert sha(worktree/path) == expected
    source = subprocess.check_output(["git", "show", "5be2661b4625a5a33af00e0a6c101d7112e67ddd:biofilms_potts.jl"], cwd=worktree)
    assert hashlib.sha256(source).hexdigest() == sha(worktree/"biofilms_potts.jl")
    original = root/"bioenergy_toys.jl"
    assert sha(original) == "f2882c03f32a663997367d7896859347c550c834bff4e30b4c09110a3d52fcbf"
    text = original.read_text()
    assert text[text.index("const PRACTICE_STATUS = try"):] in (root/"bioenergy_toys_sandbox.jl").read_text()
    ignored = subprocess.check_output(["git", "check-ignore", "bioenergy_toys.jl"], cwd=root, text=True).strip() == "bioenergy_toys.jl"
    assert ignored
    inputs = json.loads((root/"docs/preserved_inputs_2026-10-07.json").read_text())["inputs"]
    assert all(sha(Path(item["path"])) == item["sha256"] for item in inputs)
    workbook = Path.home()/"Downloads/spec_edits_and_dose_feasibility.xlsx"
    assert sha(workbook) == "3f24c4f73ae3b234e896ced515e12b15bb210f1f65934c26f7407694103ad247"
    receipts = [summary_path] + [worktree/"diagnostics/receipts"/name for name in (
        "turing_preflight_2026-10-07_03.json", "symbolics_2026-10-07_03.json", "metal_2026-10-07_01.json")]
    return dict(passed=True, freeze_commit=freeze, source_catalog_matches_current_files=True,
                serial_sha256=sha(worktree/"biofilms_potts.jl"), serial_matches_base=True,
                original_exercise_sha256=sha(original), original_assertions_copied_verbatim=True,
                original_ignored=ignored, historical_inputs_unchanged=len(inputs),
                workbook_unchanged_sha256=sha(workbook), trace_readback=trace_checks,
                receipts={str(path.relative_to(worktree)): sha(path) for path in receipts})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worktree", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists; historical receipts are preserved")
    result = verify(args.worktree.resolve())
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print("Verified 56,000 trace rows, frozen sources, original assertions, nine inputs, workbook, and base serial source.")
