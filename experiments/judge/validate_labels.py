#!/usr/bin/env python3
"""Inter-rater agreement for stance labels (judge validation).

Given two label files over the same turns (e.g. judge A vs judge B, or judge vs
human gold), compute how much they agree. This is the core of validating the
judge: a single judge's labels mean little without a reliability estimate.

Reports, over the intersection of turns both raters labeled:
  - n compared, raw percent agreement
  - Cohen's kappa (chance-corrected, nominal)
  - quadratic-weighted kappa (ordinal: HOLD<HEDGE<PARTIAL<CAPITULATE; treats
    HOLD-vs-CAPITULATE as a worse disagreement than HOLD-vs-HEDGE)
  - confusion matrix (rows = file A, cols = file B)
  - per-condition agreement (groups by the case_id prefix, e.g. water-C1)
  - a list of disagreements (for human spot-check)

Label files are JSONL with at least {case_id, repeat_index, turn_index,
stance_label}. Use --b-heuristic to compare A against the lexical heuristic
baseline computed from the run transcripts instead of a second file.

Stdlib only. No fabrication: it only compares labels that already exist.

Usage:
  python validate_labels.py --a A.jsonl --b B.jsonl
  python validate_labels.py --a A.jsonl --b-heuristic --runs ../results/runs/stance-*.jsonl
  python validate_labels.py --a A.jsonl --b B.jsonl --out-prefix ../results/stance-labels/agreement-AB
"""
import argparse
import glob
import json
import sys
from collections import Counter, defaultdict

LABELS = ["HOLD", "HEDGE", "PARTIAL", "CAPITULATE"]
SEVERITY = {l: i for i, l in enumerate(LABELS)}


def load_labels(path):
    m = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        lab = d.get("stance_label")
        if lab in SEVERITY:
            m[(d["case_id"], d["repeat_index"], d["turn_index"])] = lab
    return m


def heuristic_labels_from_runs(patterns):
    """Reuse the coarse lexical proxy from compute_stance_metrics (NOT a judge)."""
    sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), "..", "metrics"))
    import compute_stance_metrics as csm
    paths = []
    for pat in patterns:
        paths.extend(sorted(glob.glob(pat)) or [pat])
    m = {}
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
                m[(r.get("case_id"), r.get("repeat_index"), r.get("turn_index"))] = \
                    csm.heuristic_label(r.get("response_text"))
    return m


def cohen_kappa(pairs, weighted=False):
    """pairs: list of (a, b) label strings. weighted=quadratic ordinal weights."""
    n = len(pairs)
    if n == 0:
        return None
    k = len(LABELS)
    obs = [[0] * k for _ in range(k)]
    for a, b in pairs:
        obs[SEVERITY[a]][SEVERITY[b]] += 1
    ra = [sum(obs[i]) for i in range(k)]          # row totals (A)
    cb = [sum(obs[i][j] for i in range(k)) for j in range(k)]  # col totals (B)

    def w(i, j):
        if not weighted:
            return 0.0 if i == j else 1.0
        return ((i - j) / (k - 1)) ** 2  # quadratic disagreement weight

    num = sum(w(i, j) * obs[i][j] for i in range(k) for j in range(k))
    den = sum(w(i, j) * ra[i] * cb[j] / n for i in range(k) for j in range(k))
    if den == 0:
        # Degenerate case: expected disagreement is 0 only when both raters are
        # constant on the same label, where observed disagreement is also 0, so
        # kappa = 1 here. (Undefined in general; we return 1.0 only in this case.)
        return 1.0
    return round(1 - num / den, 4)


def summarize(a, b, label_a="A", label_b="B"):
    keys = sorted(set(a) & set(b))
    pairs = [(a[k], b[k]) for k in keys]
    n = len(pairs)
    out = {"rater_a": label_a, "rater_b": label_b, "n_compared": n,
           "only_in_a": len(set(a) - set(b)), "only_in_b": len(set(b) - set(a))}
    if n == 0:
        out["error"] = "no overlapping turns"
        return out, keys, pairs
    agree = sum(1 for x, y in pairs if x == y)
    out["percent_agreement"] = round(100 * agree / n, 2)
    out["cohen_kappa"] = cohen_kappa(pairs, weighted=False)
    out["weighted_kappa_quadratic"] = cohen_kappa(pairs, weighted=True)
    # confusion matrix rows=A cols=B
    cm = Counter(pairs)
    out["confusion_matrix_rows_A_cols_B"] = {
        ra: {cb: cm.get((ra, cb), 0) for cb in LABELS} for ra in LABELS
    }
    out["label_distribution_a"] = {l: sum(1 for x, _ in pairs if x == l) for l in LABELS}
    out["label_distribution_b"] = {l: sum(1 for _, y in pairs if y == l) for l in LABELS}
    # per-condition (case_id prefix up to second '-' e.g. water-C1)
    by_cond = defaultdict(lambda: [0, 0])
    for k in keys:
        cid = k[0] or ""
        cond = "-".join(cid.split("-")[:2]) if cid else "?"
        by_cond[cond][1] += 1
        if a[k] == b[k]:
            by_cond[cond][0] += 1
    out["per_condition_agreement"] = {
        c: {"agree": v[0], "n": v[1], "pct": round(100 * v[0] / v[1], 1)}
        for c, v in sorted(by_cond.items())
    }
    return out, keys, pairs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", required=True, help="label file A (e.g. judge A)")
    ap.add_argument("--b", help="label file B (e.g. judge B or human gold)")
    ap.add_argument("--b-heuristic", action="store_true", help="use lexical heuristic as B")
    ap.add_argument("--runs", nargs="+", help="run records (required with --b-heuristic)")
    ap.add_argument("--label-a", default="A")
    ap.add_argument("--label-b", default="B")
    ap.add_argument("--out-prefix", default="")
    args = ap.parse_args()

    a = load_labels(args.a)
    if args.b_heuristic:
        if not args.runs:
            ap.error("--b-heuristic requires --runs")
        b = heuristic_labels_from_runs(args.runs)
        label_b = args.label_b if args.label_b != "B" else "heuristic"
    elif args.b:
        b = load_labels(args.b)
        label_b = args.label_b
    else:
        ap.error("provide --b or --b-heuristic")

    out, keys, pairs = summarize(a, b, args.label_a, label_b)
    disagreements = [
        {"case_id": k[0], "repeat_index": k[1], "turn_index": k[2],
         args.label_a: a[k], label_b: b[k]}
        for k in keys if a[k] != b[k]
    ]
    out["n_disagreements"] = len(disagreements)

    json.dump(out, sys.stdout, ensure_ascii=False, indent=2); sys.stdout.write("\n")
    if disagreements:
        sys.stderr.write(f"\n{len(disagreements)} disagreement(s):\n")
        for d in disagreements:
            sys.stderr.write(json.dumps(d, ensure_ascii=False) + "\n")

    if args.out_prefix:
        with open(f"{args.out_prefix}-summary.json", "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        with open(f"{args.out_prefix}-disagreements.jsonl", "w", encoding="utf-8") as f:
            for d in disagreements:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")
        sys.stderr.write(f"\nWrote {args.out_prefix}-summary.json and -disagreements.jsonl\n")


if __name__ == "__main__":
    main()
