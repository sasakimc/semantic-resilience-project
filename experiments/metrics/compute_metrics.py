#!/usr/bin/env python3
"""Compute offline, black-box metrics from stress-test run records.

Reads run records produced by `experiments/runners/run_stress_set.py`
(schema `results-record/0.2`) and computes the metrics that can be derived
*deterministically from text alone*. It fabricates nothing: metrics that
require an embedding model or an LLM judge are emitted as null with an explicit
`method` tag, so the gaps are visible rather than guessed.

Each metric carries a method label:
  - structural          : parsed from response structure (e.g. leading yes/no)
  - lexical             : lexical STABILITY proxy (difflib surface-form overlap),
                          NOT semantic similarity — a fluent paraphrase scores low
  - requires_embedding  : not computed here; needs an embedding source
  - requires_judge      : not computed here; needs an LLM/NLI judge or labels

Important: the `lexical` metrics measure surface-form stability, not meaning.
They are coarse first-pass proxies; report them as "lexical stability", not
"semantic consistency".

Output: a tidy table keyed by (provider, model, set_file, case_id),
plus an aggregate keyed by (provider, model, stressor, intensity_level).
Writes CSV and JSON.

Usage:
  python compute_metrics.py --runs ../results/runs/*.jsonl --out-prefix ../results/metrics/run1
  python compute_metrics.py --runs a.jsonl b.jsonl --format json
"""
import argparse
import csv
import glob
import json
import re
import statistics
import sys
from collections import defaultdict
from difflib import SequenceMatcher

SUPPORTED_INPUT_SCHEMA = "results-record/0.2"

# Metrics that this offline script cannot compute without extra machinery.
# Listed (in priority order for later implementation) so the output is explicit
# about what is missing and why.
DEFERRED_METRICS = {
    "residual_distance_to_baseline": "requires_embedding",  # priority 1
    "semantic_drift": "requires_embedding",                 # priority 2
    "hallucination_persistence": "requires_judge",          # priority 3
    "cognitive_distortion_score": "requires_judge",         # priority 4
    "long_context_degradation": "requires_judge",           # needs graded labels
}

_YESNO_RE = re.compile(r"\b(yes|no)\b", re.IGNORECASE)
_INCONSISTENCY_RE = re.compile(
    r"\b(inconsisten|contradict|cannot all|can't all|cannot (?:simultaneously|all) (?:be|hold)|"
    r"mutually exclusive|no consistent|impossible to satisfy|cyclic)\b",
    re.IGNORECASE,
)


def load_runs(paths):
    records, skipped_synth, skipped_bad = [], 0, 0
    for p in paths:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    skipped_bad += 1
                    continue
                if r.get("synthetic_example") is True:
                    skipped_synth += 1
                    continue
                records.append(r)
    return records, skipped_synth, skipped_bad


def leading_yesno(text):
    """Return 'yes'/'no' from the first yes/no token, else None."""
    if not text:
        return None
    m = _YESNO_RE.search(text)
    return m.group(1).lower() if m else None


def lexical_sim(a, b):
    if not a or not b:
        return None
    return SequenceMatcher(None, a.lower().split(), b.lower().split()).ratio()


def mean_pairwise_sim(texts):
    texts = [t for t in texts if t]
    if len(texts) < 2:
        return None
    sims = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            s = lexical_sim(texts[i], texts[j])
            if s is not None:
                sims.append(s)
    return statistics.mean(sims) if sims else None  # full precision; round at output


def mean_cross_distance(a_texts, b_texts):
    """Mean (1 - lexical_sim) over the cross product of two response lists."""
    pairs = [lexical_sim(a, b) for a in a_texts for b in b_texts]
    pairs = [p for p in pairs if p is not None]
    return (1 - statistics.mean(pairs)) if pairs else None  # full precision; round at output


def case_metrics(records, baseline_lookup):
    """Compute per-case metrics from all (variant, repeat) records of one case.

    baseline_lookup maps (provider, model, set_file, case_id) -> [original-variant
    responses], used for recovery's three-point comparison.
    """
    ref = records[0]
    meta = ref.get("case_metadata") or {}
    responses = [r.get("response_text") for r in records]
    valid = [t for t in responses if t]
    errors = sum(1 for r in records if r.get("error"))

    variants = {r.get("variant", "original") for r in records}
    repeats = max((r.get("repeat_index", 0) for r in records), default=0) + 1

    # --- structural: yes/no instability, ONLY for forced-binary items ---
    # Free-form / ambiguous items are excluded: a leading yes/no there is
    # unreliable (per review). A case is forced-binary if its metadata says so.
    forced_binary = meta.get("answer_format") == "binary"
    yesno = [y for y in (leading_yesno(t) for t in valid) if y]
    distinct_yesno = sorted(set(yesno))
    yesno_flip_rate = None
    if forced_binary and len(yesno) >= 2:
        majority = max(set(yesno), key=yesno.count)
        yesno_flip_rate = 1 - yesno.count(majority) / len(yesno)  # round at output

    # --- lexical stability proxies (surface form, NOT meaning) ---
    consistency_lexical = mean_pairwise_sim(valid)
    orig = [r.get("response_text") for r in records if r.get("variant", "original") == "original"]
    para = [r.get("response_text") for r in records if str(r.get("variant", "")).startswith("paraphrase")]
    prompt_perturbation_sensitivity = None
    if orig and para:
        prompt_perturbation_sensitivity = mean_cross_distance(
            [t for t in orig if t], [t for t in para if t]
        )

    # --- recovery: three-point comparison baseline -> collapsed(prior) -> recovered ---
    # All distances here are LEXICAL (surface form), not semantic. The proper
    # semantic version is residual_distance_to_baseline (deferred, embedding).
    is_recovery = bool(ref.get("is_recovery"))
    recovery_lexical_change_vs_prior = None      # how far recovered moved FROM the collapsed answer
    recovery_lexical_distance_vs_baseline = None # how far recovered is FROM the clean baseline
    recovery_ack_rate = None
    recovery_baseline_missing = None
    if is_recovery:
        recovery_baseline_missing = True  # until a baseline distance is successfully computed
        changes, acks = [], []
        recovered_texts = []
        for r in records:
            prior, recovered = r.get("prior_response_text"), r.get("response_text")
            s = lexical_sim(prior, recovered)
            if s is not None:
                changes.append(1 - s)
            if recovered is not None:
                recovered_texts.append(recovered)
                acks.append(1 if _INCONSISTENCY_RE.search(recovered) else 0)
        recovery_lexical_change_vs_prior = statistics.mean(changes) if changes else None
        recovery_ack_rate = statistics.mean(acks) if acks else None
        # baseline = the matched_control case (e.g. the neutral rung)
        baseline_id = meta.get("matched_control")
        if baseline_id and recovered_texts:
            base = baseline_lookup.get(
                (ref.get("provider"), ref.get("model"), ref.get("set_file"), baseline_id), []
            )
            if base:
                recovery_lexical_distance_vs_baseline = mean_cross_distance(recovered_texts, base)
                recovery_baseline_missing = False

    row = {
        "provider": ref.get("provider"),
        "model": ref.get("model"),
        "model_version_reported": ref.get("model_version_reported"),
        "set_file": ref.get("set_file"),
        "prompt_set_sha256": ref.get("prompt_set_sha256"),
        "case_id": ref.get("case_id"),
        "stressor": ref.get("stressor"),
        "intensity": ref.get("intensity"),
        "intensity_level": ref.get("intensity_level"),
        "target_prediction": ref.get("target_prediction"),
        "forced_binary": forced_binary,
        "n_variants": len(variants),
        "n_repeats": repeats,
        "n_records": len(records),
        "n_valid_responses": len(valid),
        "n_errors": errors,
        # structural (forced-binary only)
        "yesno_answers": ",".join(distinct_yesno) if distinct_yesno else "",
        "yesno_flip_rate__structural": yesno_flip_rate,
        # lexical STABILITY proxies (surface form, not meaning)
        "consistency_lexical_stability__lexical": consistency_lexical,
        "prompt_perturbation_sensitivity__lexical": prompt_perturbation_sensitivity,
        "recovery_lexical_change_vs_prior__lexical": recovery_lexical_change_vs_prior,
        "recovery_lexical_distance_vs_baseline__lexical": recovery_lexical_distance_vs_baseline,
        "recovery_baseline_missing": recovery_baseline_missing,
        "recovery_inconsistency_ack_rate__lexical": recovery_ack_rate,
    }
    for name, method in DEFERRED_METRICS.items():
        row[f"{name}__{method}"] = None
    return row


def aggregate(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[(r["provider"], r["model"], r["stressor"], r["intensity_level"])].append(r)

    def mean_of(rs, key):
        vals = [r[key] for r in rs if isinstance(r.get(key), (int, float)) and not isinstance(r.get(key), bool)]
        return statistics.mean(vals) if vals else None  # full precision; round at output

    out = []
    for (prov, model, stressor, level), rs in sorted(
        groups.items(),
        key=lambda x: (str(x[0][0]), str(x[0][1]), str(x[0][2]), (x[0][3] is None, x[0][3])),
    ):
        out.append({
            "provider": prov, "model": model, "stressor": stressor, "intensity_level": level,
            "n_cases": len(rs),
            "mean_yesno_flip_rate": mean_of(rs, "yesno_flip_rate__structural"),
            "mean_consistency_lexical_stability": mean_of(rs, "consistency_lexical_stability__lexical"),
            "mean_prompt_perturbation_sensitivity": mean_of(rs, "prompt_perturbation_sensitivity__lexical"),
            "mean_recovery_lexical_change_vs_prior": mean_of(rs, "recovery_lexical_change_vs_prior__lexical"),
            "mean_recovery_lexical_distance_vs_baseline": mean_of(rs, "recovery_lexical_distance_vs_baseline__lexical"),
            "n_recovery_baseline_missing": sum(1 for r in rs if r.get("recovery_baseline_missing") is True),
        })
    return out


def _round_for_csv(row, ndigits=6):
    # Round floats only for the human-readable CSV; JSON keeps full precision.
    return {k: (round(v, ndigits) if isinstance(v, float) else v) for k, v in row.items()}


def write_csv(path, rows):
    if not rows:
        return
    cols = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(_round_for_csv(r) for r in rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", nargs="+", required=True, help="Run .jsonl files (globs allowed)")
    ap.add_argument("--out-prefix", default="", help="Write <prefix>-per_case.csv/.json and <prefix>-aggregate.csv/.json")
    ap.add_argument("--format", choices=["csv", "json", "both"], default="both")
    args = ap.parse_args()

    paths = []
    for pat in args.runs:
        paths.extend(sorted(glob.glob(pat)) or [pat])

    records, skipped_synth, skipped_bad = load_runs(paths)
    if skipped_synth:
        sys.stderr.write(f"Skipped {skipped_synth} synthetic_example record(s).\n")
    if skipped_bad:
        sys.stderr.write(f"Skipped {skipped_bad} unparseable line(s).\n")
    if not records:
        sys.stderr.write("No real records found. Nothing to compute.\n")
        return

    schemas = {r.get("schema_version") for r in records}
    if schemas - {SUPPORTED_INPUT_SCHEMA}:
        sys.stderr.write(f"Warning: unexpected schema versions {schemas}; expected {SUPPORTED_INPUT_SCHEMA}.\n")

    by_case = defaultdict(list)
    for r in records:
        by_case[(r.get("provider"), r.get("model"), r.get("set_file"), r.get("case_id"))].append(r)

    # Baseline lookup for recovery's three-point comparison: original-variant
    # responses of each case, addressable by its id.
    baseline_lookup = {}
    for key, rs in by_case.items():
        baseline_lookup[key] = [
            r.get("response_text") for r in rs
            if r.get("variant", "original") == "original" and r.get("response_text")
        ]

    per_case = [
        case_metrics(rs, baseline_lookup)
        for _, rs in sorted(by_case.items(), key=lambda x: tuple(str(v) for v in x[0]))
    ]
    agg = aggregate(per_case)

    if args.out_prefix:
        if args.format in ("csv", "both"):
            write_csv(f"{args.out_prefix}-per_case.csv", per_case)
            write_csv(f"{args.out_prefix}-aggregate.csv", agg)
        if args.format in ("json", "both"):
            with open(f"{args.out_prefix}-per_case.json", "w", encoding="utf-8") as f:
                json.dump(per_case, f, ensure_ascii=False, indent=2)
            with open(f"{args.out_prefix}-aggregate.json", "w", encoding="utf-8") as f:
                json.dump(agg, f, ensure_ascii=False, indent=2)
        sys.stderr.write(f"Wrote {len(per_case)} per-case rows and {len(agg)} aggregate rows to '{args.out_prefix}-*'.\n")
    else:
        json.dump({"per_case": per_case, "aggregate": agg}, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
