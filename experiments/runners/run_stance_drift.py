#!/usr/bin/env python3
"""Multi-turn stance-drift harness (Coexistence Resilience / fatigue axis).

Drives a multi-turn dialogue per the design in
`experiments/coexistence/stance-drift-pilot.md`:

  turn 0  : establish a stance (the model's position)
  pressure: N scripted interlocutor turns (social pressure or valid evidence)
  release : M neutral turns (does the stance return? homeostasis vs sticky)

It records the model's real response at every turn with full provenance. It makes
no judgement here: per-turn stance labelling (HOLD/HEDGE/PARTIAL/CAPITULATE) and
the drift curve / N* / Recovery Ratio are computed in a separate offline judge
step. Reuses the provider adapters from run_stress_set.py (anthropic/openai/
google/ollama). No data is fabricated.

Usage:
  python run_stance_drift.py --set ../prompts/stance-pressure.v0.jsonl \
      --provider ollama --model gemma2:2b --repeats 5 --temperature 1.0 \
      --out ../results/runs/stance-$(date +%Y%m%d)-ollama-gemma2_2b.jsonl
  python run_stance_drift.py --set ../prompts/stance-pressure.v0.jsonl \
      --provider ollama --model gemma2:2b --dry-run
"""
import argparse
import json
import os
import sys
import urllib.error
import uuid

import run_stress_set as base  # reuse ADAPTERS, helpers, redaction

SCHEMA_VERSION = "stance-drift/0.1"


def play_case(case, adapter, model, system, temperature, max_tokens, dry_run):
    """Run one full dialogue; yield a per-turn record dict (without provenance)."""
    convo = []  # full {role, content} exchanged so far

    def send(user_text, phase, turn_index):
        convo.append({"role": "user", "content": user_text})
        if dry_run:
            convo.append({"role": "assistant", "content": "<dry-run: not sent>"})
            return None, None
        text, reported = adapter(model, system, convo, temperature, max_tokens)
        convo.append({"role": "assistant", "content": text})
        return text, reported

    turns = [("establish", case["establish_prompt"])]
    turns += [("pressure", t) for t in case.get("pressure_turns", [])]
    turns += [("release", t) for t in case.get("release_turns", [])]

    reported_model = None
    for i, (phase, user_text) in enumerate(turns):
        text, reported = send(user_text, phase, i)
        if reported:
            reported_model = reported
        yield {
            "turn_index": i,
            "phase": phase,
            "interlocutor_text": user_text,
            "response_text": text,
            "reported_model": reported_model,
        }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", required=True, help="Path to a stance-pressure set (.jsonl)")
    ap.add_argument("--provider", required=True, choices=sorted(base.ADAPTERS))
    ap.add_argument("--model", required=True)
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--system", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    adapter = base.ADAPTERS[args.provider]
    run_id = uuid.uuid4().hex[:12]
    started = base.utc_now()
    code_version = base.git_sha()
    set_sha = base.sha256_file(args.set)

    with open(args.set, encoding="utf-8") as f:
        cases = [json.loads(line) for line in f if line.strip()]

    out_fh = open(args.out, "w", encoding="utf-8") if args.out else sys.stdout
    n = 0
    try:
        for case in cases:
            for rep in range(args.repeats):
                try:
                    for turn in play_case(case, adapter, args.model, args.system,
                                          args.temperature, args.max_tokens, args.dry_run):
                        rec = {
                            "schema_version": SCHEMA_VERSION,
                            "run_id": run_id,
                            "timestamp_utc": base.utc_now(),
                            "run_started_utc": started,
                            "code_version": code_version,
                            "provider": args.provider,
                            "model": args.model,
                            "model_version_reported": turn["reported_model"],
                            "temperature": args.temperature,
                            "max_tokens": args.max_tokens,
                            "system_prompt": args.system,
                            "set_file": os.path.basename(args.set),
                            "prompt_set_sha256": set_sha,
                            "case_id": case.get("id"),
                            "stance_item": case.get("stance_item"),
                            "condition": case.get("condition"),
                            "has_valid_evidence": case.get("has_valid_evidence"),
                            "expected_behavior": case.get("expected_behavior"),
                            "repeat_index": rep,
                            "turn_index": turn["turn_index"],
                            "phase": turn["phase"],
                            "interlocutor_text": turn["interlocutor_text"],
                            "response_text": turn["response_text"],
                            "dry_run": args.dry_run,
                            "error": None,
                            "synthetic_example": False,
                        }
                        out_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        out_fh.flush()
                        n += 1
                except (urllib.error.URLError, KeyError, OSError, ValueError) as e:
                    err = {
                        "schema_version": SCHEMA_VERSION, "run_id": run_id,
                        "timestamp_utc": base.utc_now(), "provider": args.provider,
                        "model": args.model, "set_file": os.path.basename(args.set),
                        "prompt_set_sha256": set_sha, "case_id": case.get("id"),
                        "condition": case.get("condition"), "repeat_index": rep,
                        "turn_index": None, "phase": "error", "interlocutor_text": None,
                        "response_text": None, "dry_run": args.dry_run,
                        "error": base.REDACT(f"{type(e).__name__}: {e}"),
                        "synthetic_example": False,
                    }
                    out_fh.write(json.dumps(err, ensure_ascii=False) + "\n"); out_fh.flush(); n += 1
    finally:
        if out_fh is not sys.stdout:
            out_fh.close()
    sys.stderr.write(f"Wrote {n} turn-records (run_id={run_id}, dry_run={args.dry_run}).\n")


if __name__ == "__main__":
    main()
