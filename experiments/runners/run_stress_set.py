#!/usr/bin/env python3
"""Run a stress-test prompt set (JSONL) against an LLM and record raw responses.

This runner makes NO claims and fabricates NO data. It sends the prompts in a
set to a model via its API and writes one JSON record per (case, repeat),
capturing full provenance (model, timestamp, settings, exact conversation,
raw response). Metric computation is intentionally left to a separate,
offline step.

Supported providers (API key read from the environment):
  - anthropic  (ANTHROPIC_API_KEY)
  - openai     (OPENAI_API_KEY)
  - google     (GOOGLE_API_KEY)

Recovery cases (those carrying a `prior_turn`) are run faithfully as a real
two-turn conversation: the model's OWN answer to the prior (collapse-inducing)
turn is captured first, then the recovery prompt is sent as a follow-up. The
induced assistant turn is never fabricated.

Usage:
  python run_stress_set.py --set ../prompts/contradiction-ladder.v0.1.jsonl \
      --provider anthropic --model claude-opus-4-8 --repeats 5 \
      --out ../results/runs/$(date +%Y%m%d)-anthropic.jsonl

  # Inspect exactly what would be sent, with no network calls or API key:
  python run_stress_set.py --set ../prompts/minimal-stress-set.v0.jsonl \
      --provider anthropic --model claude-opus-4-8 --dry-run
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
import uuid

SCHEMA_VERSION = "results-record/0.1"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "unknown"


def _http_post(url: str, headers: dict, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


# --- Provider adapters -------------------------------------------------------
# Each adapter takes (model, system, turns, temperature, max_tokens) where
# `turns` is a list of {"role": "user"|"assistant", "content": str}, and
# returns (assistant_text, reported_model).

def chat_anthropic(model, system, turns, temperature, max_tokens):
    key = os.environ["ANTHROPIC_API_KEY"]
    body = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": t["role"], "content": t["content"]} for t in turns],
    }
    if system:
        body["system"] = system
    out = _http_post(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        body,
    )
    text = "".join(b.get("text", "") for b in out.get("content", []) if b.get("type") == "text")
    return text, out.get("model", model)


def chat_openai(model, system, turns, temperature, max_tokens):
    key = os.environ["OPENAI_API_KEY"]
    messages = ([{"role": "system", "content": system}] if system else []) + [
        {"role": t["role"], "content": t["content"]} for t in turns
    ]
    out = _http_post(
        "https://api.openai.com/v1/chat/completions",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        {"model": model, "temperature": temperature, "max_tokens": max_tokens, "messages": messages},
    )
    return out["choices"][0]["message"]["content"], out.get("model", model)


def chat_google(model, system, turns, temperature, max_tokens):
    key = os.environ["GOOGLE_API_KEY"]
    contents = [
        {"role": "user" if t["role"] == "user" else "model", "parts": [{"text": t["content"]}]}
        for t in turns
    ]
    body = {
        "contents": contents,
        "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
    }
    if system:
        body["systemInstruction"] = {"parts": [{"text": system}]}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    out = _http_post(url, {"Content-Type": "application/json"}, body)
    parts = out["candidates"][0]["content"]["parts"]
    return "".join(p.get("text", "") for p in parts), model


ADAPTERS = {"anthropic": chat_anthropic, "openai": chat_openai, "google": chat_google}


def build_conversation(case: dict):
    """Return the list of user turns to play, in order.

    For ordinary cases: [prompt].
    For recovery cases (with prior_turn): [prior_turn.user, prompt]; the
    assistant turn between them is filled by the model's real response at run
    time (see run_case).
    """
    prior = case.get("prior_turn")
    if prior and prior.get("user"):
        return [prior["user"], case["prompt"]]
    return [case["prompt"]]


def run_case(case, adapter, model, system, temperature, max_tokens, dry_run):
    user_turns = build_conversation(case)
    convo = []  # full {role, content} list actually exchanged
    responses = []
    for user_text in user_turns:
        convo.append({"role": "user", "content": user_text})
        if dry_run:
            convo.append({"role": "assistant", "content": "<dry-run: not sent>"})
            responses.append(None)
            continue
        text, reported = run_case._adapter_call(adapter, model, system, convo, temperature, max_tokens)
        convo.append({"role": "assistant", "content": text})
        responses.append(text)
        run_case._last_reported = reported
    return convo, responses


run_case._last_reported = None


def _adapter_call(adapter, model, system, convo, temperature, max_tokens):
    # Only the user/assistant turns so far are sent; the trailing user turn is
    # the one we want a response to.
    return adapter(model, system, convo, temperature, max_tokens)


run_case._adapter_call = _adapter_call


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", required=True, help="Path to a prompt set (.jsonl)")
    ap.add_argument("--provider", required=True, choices=sorted(ADAPTERS))
    ap.add_argument("--model", required=True, help="Model id (e.g. claude-opus-4-8, gpt-4o, gemini-1.5-pro)")
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--system", default="", help="Optional system prompt (record it!)")
    ap.add_argument("--out", default="", help="Output .jsonl path (default: stdout)")
    ap.add_argument("--dry-run", action="store_true", help="Print what would be sent; no API calls")
    args = ap.parse_args()

    adapter = ADAPTERS[args.provider]
    run_id = uuid.uuid4().hex[:12]
    started = utc_now()
    code_version = git_sha()

    with open(args.set, encoding="utf-8") as f:
        cases = [json.loads(line) for line in f if line.strip()]

    out_fh = open(args.out, "w", encoding="utf-8") if args.out else sys.stdout
    n = 0
    try:
        for case in cases:
            for rep in range(args.repeats):
                rec = {
                    "schema_version": SCHEMA_VERSION,
                    "run_id": run_id,
                    "timestamp_utc": utc_now(),
                    "run_started_utc": started,
                    "code_version": code_version,
                    "provider": args.provider,
                    "model": args.model,
                    "temperature": args.temperature,
                    "max_tokens": args.max_tokens,
                    "system_prompt": args.system,
                    "set_file": os.path.basename(args.set),
                    "case_id": case.get("id"),
                    "stressor": case.get("stressor"),
                    "intensity": case.get("intensity"),
                    "intensity_level": case.get("intensity_level"),
                    "target_prediction": case.get("target_prediction"),
                    "repeat_index": rep,
                    "is_recovery": bool(case.get("prior_turn")),
                    "dry_run": args.dry_run,
                    "synthetic_example": False,
                }
                try:
                    convo, responses = run_case(
                        case, adapter, args.model, args.system,
                        args.temperature, args.max_tokens, args.dry_run,
                    )
                    rec["conversation"] = convo
                    rec["response_text"] = responses[-1]
                    if rec["is_recovery"]:
                        rec["prior_response_text"] = responses[0]
                    rec["model_version_reported"] = run_case._last_reported
                    rec["error"] = None
                except (urllib.error.URLError, KeyError, OSError) as e:
                    rec["error"] = f"{type(e).__name__}: {e}"
                    rec["response_text"] = None
                out_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                out_fh.flush()
                n += 1
    finally:
        if out_fh is not sys.stdout:
            out_fh.close()
    sys.stderr.write(f"Wrote {n} records (run_id={run_id}, dry_run={args.dry_run}).\n")


if __name__ == "__main__":
    main()
