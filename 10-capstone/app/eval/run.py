"""Run the eval set against the capstone assistant and print scores."""

import os
import sys
import json
import time
import csv
import pathlib

# Allow importing sibling app modules
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv("../../.env")

from assistant import run     # noqa: E402
from judge import judge       # noqa: E402

HERE = pathlib.Path(__file__).parent
SET = HERE / "set.jsonl"
OUT = HERE / "scores.csv"


def main():
    rows = [json.loads(l) for l in SET.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"running {len(rows)} examples...\n")

    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["question", "ok", "correct", "cited", "must_contain_ok",
                    "steps", "in_tokens", "out_tokens", "notes"])

        passed = 0
        for i, row in enumerate(rows, 1):
            t0 = time.perf_counter()
            r = run(row["question"], max_steps=8)
            dt = time.perf_counter() - t0
            report = r["report"] or {"answer": "(no report)"}
            v = judge(row["question"], row["rubric"], row["must_contain"], report)

            ok = v["correct"] and v["cited"] and v.get("must_contain_ok", False)
            passed += int(ok)
            mark = "✓" if ok else "✗"
            print(f"{mark} [{dt:5.1f}s] {row['question'][:60]:<62}  notes: {v['notes']}")
            w.writerow([row["question"], r["ok"], v["correct"], v["cited"],
                        v["must_contain_ok"], r["steps"],
                        r["usage"].input_tokens, r["usage"].output_tokens, v["notes"]])

    print(f"\nscore: {passed}/{len(rows)} = {passed/len(rows):.0%}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
