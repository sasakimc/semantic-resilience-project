#!/usr/bin/env python3
"""Generate a BLIND human spot-check sheet for stance labels.

Judge-vs-judge agreement (LLM vs LLM) measures reliability, not correctness. The
stronger test is a human gold standard. This script samples turns from the run
transcripts and emits a sheet a human fills in WITHOUT seeing any judge label, so
the human labels are independent. Feed the filled sheet back through
`validate_labels.py` (as file B, with a judge file as A) to get judge-vs-human
agreement.

Sampling is stratified and reproducible (fixed seed):
  - ALL turns where the supplied judge files disagree (the hard cases), plus
  - a per-(condition x label) random sample from one reference judge.

It NEVER writes a label into the human sheet (the `gold_label` field is blank).

Usage:
  python make_spotcheck.py \
      --runs ../results/runs/stance-20260612-ollama-gemma2_2b.jsonl \
      --judges ../results/stance-labels/gemma2-2b.jsonl ../results/stance-labels/gemma2-2b.judgeB-claude.jsonl \
      --per-stratum 1 --seed 7 \
      --out ../results/stance-labels/spotcheck-gemma2-2b.BLANK.jsonl
"""
import argparse
import glob
import json
import random
import sys
from collections import defaultdict

LABELS = ["HOLD", "HEDGE", "PARTIAL", "CAPITULATE"]


def load_runs(patterns):
    recs = {}
    paths = []
    for pat in patterns:
        paths.extend(sorted(glob.glob(pat)) or [pat])
    for p in paths:
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("synthetic_example") is True or r.get("phase") == "error":
                continue
            if r.get("response_text") and r.get("turn_index") is not None:
                recs[(r.get("case_id"), r.get("repeat_index"), r.get("turn_index"))] = r
    return recs


def load_labels(path):
    m = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if d.get("stance_label") in LABELS:
            m[(d["case_id"], d["repeat_index"], d["turn_index"])] = d["stance_label"]
    return m


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--judges", nargs="+", required=True, help="one or more judge label files")
    ap.add_argument("--per-stratum", type=int, default=1, help="random samples per (condition,label) stratum")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    recs = load_runs(args.runs)
    judges = [load_labels(p) for p in args.judges]
    keys = sorted(recs)

    chosen = set()
    # 1) all disagreements among judges
    for k in keys:
        labs = {j[k] for j in judges if k in j}
        if len(labs) > 1:
            chosen.add(k)
    # 2) stratified random sample by (condition, reference-judge label)
    ref = judges[0]
    strata = defaultdict(list)
    for k in keys:
        if k in ref:
            cond = "-".join((k[0] or "").split("-")[:2])
            strata[(cond, ref[k])].append(k)
    for _, ks in strata.items():
        rng.shuffle(ks)
        for k in ks[:args.per_stratum]:
            chosen.add(k)

    rows = []
    for k in sorted(chosen):
        r = recs[k]
        rows.append({
            "case_id": k[0], "repeat_index": k[1], "turn_index": k[2],
            "phase": r.get("phase"), "model_judged": r.get("model"),
            "stance_item": r.get("stance_item"),
            "interlocutor_text": r.get("interlocutor_text"),
            "response_text": r.get("response_text"),
            "gold_label": "",   # <-- HUMAN FILLS THIS (HOLD|HEDGE|PARTIAL|CAPITULATE)
            "gold_note": "",
        })
    rng.shuffle(rows)  # present in random order so the human isn't cued by structure

    out_fh = open(args.out, "w", encoding="utf-8") if args.out else sys.stdout
    for r in rows:
        out_fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    if out_fh is not sys.stdout:
        out_fh.close()
    sys.stderr.write(
        f"Wrote {len(rows)} blind spot-check rows (disagreements + {args.per_stratum}/stratum, seed={args.seed}).\n"
        f"Fill 'gold_label' per RUBRIC.md, then:\n"
        f"  python validate_labels.py --a <judge>.jsonl --b <filled>.jsonl --label-a judge --label-b human\n")


if __name__ == "__main__":
    main()
