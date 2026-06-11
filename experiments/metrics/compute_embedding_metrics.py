#!/usr/bin/env python3
"""Compute embedding-based (semantic) metrics from stress-test run records.

This is the *semantic* companion to `compute_metrics.py` (which is lexical /
stdlib-only). It embeds model responses with a pluggable embedding provider and
computes cosine-based metrics — the proper version of the distances that
`compute_metrics.py` can only approximate lexically.

Metrics (method tag = `embedding:<provider>/<model>`):
  - semantic_drift                  : within a case, mean pairwise cosine
                                      DISTANCE across responses (variants +
                                      repeats). Semantic instability (P1).
  - recovery_semantic_change_vs_prior : cosine distance recovered vs the prior
                                      (collapse-induced) answer.
  - residual_distance_to_baseline   : for recovery cases, cosine distance of the
                                      recovered answer from the clean baseline
                                      (the `matched_control` case). This is the
                                      PRIMARY signal for P3 (recovery is
                                      reorganization, not restoration): it is
                                      expected to stay > 0 (not a return to
                                      baseline) while change_vs_prior is also > 0.

It fabricates nothing: it calls a real embedding API. With `--self-test` it runs
the cosine/aggregation math on synthetic vectors (no network, no key) so the
logic can be verified offline. With `--dry-run` it reports what it WOULD embed.

Providers (API key from env):
  - openai  (OPENAI_API_KEY)   default model text-embedding-3-small
  - google  (GOOGLE_API_KEY)   default model text-embedding-004
  - voyage  (VOYAGE_API_KEY)   default model voyage-3

Usage:
  python compute_embedding_metrics.py --runs ../results/runs/*.jsonl \
      --embed-provider openai --out-prefix ../results/metrics/run1-emb
  python compute_embedding_metrics.py --self-test
"""
import argparse
import csv
import glob
import json
import math
import os
import sys
import urllib.error
import urllib.request
from collections import defaultdict

SUPPORTED_INPUT_SCHEMA = "results-record/0.2"

DEFAULT_MODELS = {
    "openai": "text-embedding-3-small",
    "google": "text-embedding-004",
    "voyage": "voyage-3",
    "ollama": "nomic-embed-text",
}
KEY_ENV = {"openai": "OPENAI_API_KEY", "google": "GOOGLE_API_KEY", "voyage": "VOYAGE_API_KEY"}


# --- vector math (pure python; unit-tested via --self-test) -------------------

def cosine_sim(a, b):
    if not a or not b or len(a) != len(b):
        return None
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return None
    return dot / (na * nb)


def cosine_dist(a, b):
    s = cosine_sim(a, b)
    return None if s is None else 1 - s


def mean_pairwise_distance(vectors):
    vs = [v for v in vectors if v]
    if len(vs) < 2:
        return None
    ds = []
    for i in range(len(vs)):
        for j in range(i + 1, len(vs)):
            d = cosine_dist(vs[i], vs[j])
            if d is not None:
                ds.append(d)
    return sum(ds) / len(ds) if ds else None  # full precision; round only at output


def mean_cross_distance(a_vecs, b_vecs):
    a_vecs = [v for v in a_vecs if v]
    b_vecs = [v for v in b_vecs if v]
    ds = [cosine_dist(a, b) for a in a_vecs for b in b_vecs]
    ds = [d for d in ds if d is not None]
    return sum(ds) / len(ds) if ds else None  # full precision; round only at output


def _redactor():
    secrets = [v for v in (os.environ.get(n) for n in KEY_ENV.values()) if v]

    def redact(t):
        s = str(t)
        for sec in secrets:
            if sec:
                s = s.replace(sec, "***REDACTED***")
        return s

    return redact


REDACT = _redactor()


def _http_post(url, headers, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


# --- embedding providers -----------------------------------------------------

def embed_openai(texts, model):
    key = os.environ["OPENAI_API_KEY"]
    out = _http_post(
        "https://api.openai.com/v1/embeddings",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        {"model": model, "input": texts},
    )
    # Sort by index so the returned order matches the input order regardless of
    # how the API orders `data`.
    data = sorted(out["data"], key=lambda d: d.get("index", 0))
    return [d["embedding"] for d in data]


def embed_voyage(texts, model):
    key = os.environ["VOYAGE_API_KEY"]
    out = _http_post(
        "https://api.voyageai.com/v1/embeddings",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        {"model": model, "input": texts},
    )
    data = sorted(out["data"], key=lambda d: d.get("index", 0))
    return [d["embedding"] for d in data]


def embed_google(texts, model):
    # Google embeds one content per call; key goes in the URL (never stored;
    # errors are redacted).
    key = os.environ["GOOGLE_API_KEY"]
    vecs = []
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:embedContent?key={key}"
    for t in texts:
        out = _http_post(url, {"Content-Type": "application/json"},
                         {"content": {"parts": [{"text": t}]}})
        vecs.append(out["embedding"]["values"])
    return vecs


def _ollama_base():
    base = os.environ.get("OLLAMA_HOST", "http://localhost:11434").strip().rstrip("/")
    if not base.startswith("http"):
        base = "http://" + base
    return base


def embed_ollama(texts, model):
    # Local, key-free embeddings via Ollama; one text per call.
    url = f"{_ollama_base()}/api/embeddings"
    vecs = []
    for t in texts:
        out = _http_post(url, {"Content-Type": "application/json"},
                         {"model": model, "prompt": t})
        vecs.append(out["embedding"])
    return vecs


EMBEDDERS = {"openai": embed_openai, "google": embed_google, "voyage": embed_voyage, "ollama": embed_ollama}


class EmbeddingCache:
    """In-run dedup so identical texts are embedded once."""

    def __init__(self, embed_fn, model, batch=64):
        self.embed_fn, self.model, self.batch = embed_fn, model, batch
        self.cache = {}

    def get_many(self, texts):
        todo = [t for t in dict.fromkeys(texts) if t and t not in self.cache]
        for i in range(0, len(todo), self.batch):
            chunk = todo[i:i + self.batch]
            for t, v in zip(chunk, self.embed_fn(chunk, self.model)):
                self.cache[t] = v
        return {t: self.cache.get(t) for t in texts}


# --- record loading ----------------------------------------------------------

def load_runs(paths):
    records, skipped = [], 0
    for p in paths:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get("synthetic_example") is True:
                    skipped += 1
                    continue
                records.append(r)
    return records, skipped


def collect_texts(records):
    texts = set()
    for r in records:
        if r.get("response_text"):
            texts.add(r["response_text"])
        if r.get("prior_response_text"):
            texts.add(r["prior_response_text"])
    return texts


def case_metrics(records, emb, baseline_lookup):
    ref = records[0]
    meta = ref.get("case_metadata") or {}
    resp = [r.get("response_text") for r in records if r.get("response_text")]
    resp_vecs = [emb.get(t) for t in resp if emb.get(t)]

    semantic_drift = mean_pairwise_distance(resp_vecs)

    is_recovery = bool(ref.get("is_recovery"))
    rec_change_vs_prior = None
    residual_distance_to_baseline = None
    recovery_baseline_missing = None
    if is_recovery:
        recovery_baseline_missing = True
        changes = []
        recovered_vecs = []
        for r in records:
            rv = emb.get(r.get("response_text")) if r.get("response_text") else None
            pv = emb.get(r.get("prior_response_text")) if r.get("prior_response_text") else None
            if rv:
                recovered_vecs.append(rv)
            d = cosine_dist(rv, pv) if (rv and pv) else None
            if d is not None:
                changes.append(d)
        rec_change_vs_prior = (sum(changes) / len(changes)) if changes else None
        baseline_id = meta.get("matched_control")
        if baseline_id and recovered_vecs:
            base_texts = baseline_lookup.get(
                (ref.get("provider"), ref.get("model"), ref.get("set_file"), baseline_id), [])
            base_vecs = [emb.get(t) for t in base_texts if emb.get(t)]
            if base_vecs:
                residual_distance_to_baseline = mean_cross_distance(recovered_vecs, base_vecs)
                recovery_baseline_missing = False

    return {
        "provider": ref.get("provider"),
        "model": ref.get("model"),
        "set_file": ref.get("set_file"),
        "prompt_set_sha256": ref.get("prompt_set_sha256"),
        "case_id": ref.get("case_id"),
        "stressor": ref.get("stressor"),
        "intensity": ref.get("intensity"),
        "intensity_level": ref.get("intensity_level"),
        "target_prediction": ref.get("target_prediction"),
        "n_embedded_responses": len(resp_vecs),
        "semantic_drift__embedding": semantic_drift,
        "recovery_semantic_change_vs_prior__embedding": rec_change_vs_prior,
        "residual_distance_to_baseline__embedding": residual_distance_to_baseline,
        "recovery_baseline_missing": recovery_baseline_missing,
    }


def aggregate(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[(r["provider"], r["model"], r["stressor"], r["intensity_level"])].append(r)

    def mean_of(rs, key):
        vals = [r[key] for r in rs if isinstance(r.get(key), (int, float)) and not isinstance(r.get(key), bool)]
        return sum(vals) / len(vals) if vals else None  # full precision; round only at output

    out = []
    for (prov, model, stressor, level), rs in sorted(
        groups.items(),
        key=lambda x: (str(x[0][0]), str(x[0][1]), str(x[0][2]), (x[0][3] is None, x[0][3])),
    ):
        out.append({
            "provider": prov, "model": model, "stressor": stressor, "intensity_level": level,
            "n_cases": len(rs),
            "mean_semantic_drift": mean_of(rs, "semantic_drift__embedding"),
            "mean_recovery_semantic_change_vs_prior": mean_of(rs, "recovery_semantic_change_vs_prior__embedding"),
            "mean_residual_distance_to_baseline": mean_of(rs, "residual_distance_to_baseline__embedding"),
            "n_recovery_baseline_missing": sum(1 for r in rs if r.get("recovery_baseline_missing") is True),
        })
    return out


def _round_for_csv(row, ndigits=6):
    # Round floats only for the human-readable CSV; JSON keeps full precision.
    out = {}
    for k, v in row.items():
        out[k] = round(v, ndigits) if isinstance(v, float) else v
    return out


def write_csv(path, rows):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(_round_for_csv(r) for r in rows)


def self_test():
    """Verify the vector math on synthetic vectors (no network/key)."""
    a, b, c = [1.0, 0.0], [1.0, 0.0], [0.0, 1.0]
    assert abs(cosine_sim(a, b) - 1.0) < 1e-9
    assert abs(cosine_dist(a, c) - 1.0) < 1e-9
    assert abs(cosine_dist(a, b) - 0.0) < 1e-9
    # identical set -> drift 0; orthogonal pair -> drift 1
    assert mean_pairwise_distance([a, b]) == 0.0
    assert mean_pairwise_distance([a, c]) == 1.0
    # cross distance: baseline {a}, recovered {c} -> 1.0 (far from baseline)
    assert mean_cross_distance([c], [a]) == 1.0
    # recovery scenario: recovered close to baseline -> small residual
    near = [0.99, 0.01]
    assert mean_cross_distance([near], [a]) is not None and mean_cross_distance([near], [a]) < 0.01
    print("self-test OK: cosine, pairwise drift, cross distance behave as expected.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", nargs="+", help="Run .jsonl files (globs allowed)")
    ap.add_argument("--embed-provider", choices=sorted(EMBEDDERS))
    ap.add_argument("--embed-model", default="", help="Override the provider's default embedding model")
    ap.add_argument("--out-prefix", default="")
    ap.add_argument("--format", choices=["csv", "json", "both"], default="both")
    ap.add_argument("--dry-run", action="store_true", help="Report what would be embedded; no API calls")
    ap.add_argument("--self-test", action="store_true", help="Run vector-math self-test and exit")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return
    if not args.runs or not args.embed_provider:
        ap.error("--runs and --embed-provider are required (unless --self-test)")

    paths = []
    for pat in args.runs:
        paths.extend(sorted(glob.glob(pat)) or [pat])
    records, skipped = load_runs(paths)
    if skipped:
        sys.stderr.write(f"Skipped {skipped} synthetic_example record(s).\n")
    if not records:
        sys.stderr.write("No real records found.\n")
        return

    model = args.embed_model or DEFAULT_MODELS[args.embed_provider]
    texts = collect_texts(records)
    if args.dry_run:
        sys.stderr.write(
            f"[dry-run] would embed {len(texts)} unique text(s) with "
            f"{args.embed_provider}/{model}; {len(records)} records.\n")
        return

    by_case = defaultdict(list)
    for r in records:
        by_case[(r.get("provider"), r.get("model"), r.get("set_file"), r.get("case_id"))].append(r)
    baseline_lookup = {}
    for key, rs in by_case.items():
        baseline_lookup[key] = [
            r.get("response_text") for r in rs
            if r.get("variant", "original") == "original" and r.get("response_text")
        ]

    cache = EmbeddingCache(EMBEDDERS[args.embed_provider], model)
    try:
        emb = cache.get_many(sorted(texts))
    except (urllib.error.URLError, KeyError, OSError, ValueError) as e:
        sys.stderr.write("Embedding call failed: " + REDACT(f"{type(e).__name__}: {e}") + "\n")
        sys.exit(1)

    dim = next((len(v) for v in emb.values() if v), None)
    method = f"embedding:{args.embed_provider}/{model}"
    per_case = [case_metrics(rs, emb, baseline_lookup)
                for _, rs in sorted(by_case.items(), key=lambda x: tuple(str(v) for v in x[0]))]
    for row in per_case:
        row["embedding_method"] = method
        row["embedding_dim"] = dim
    agg = aggregate(per_case)

    if args.out_prefix:
        if args.format in ("csv", "both"):
            write_csv(f"{args.out_prefix}-emb_per_case.csv", per_case)
            write_csv(f"{args.out_prefix}-emb_aggregate.csv", agg)
        if args.format in ("json", "both"):
            with open(f"{args.out_prefix}-emb_per_case.json", "w", encoding="utf-8") as f:
                json.dump(per_case, f, ensure_ascii=False, indent=2)
            with open(f"{args.out_prefix}-emb_aggregate.json", "w", encoding="utf-8") as f:
                json.dump(agg, f, ensure_ascii=False, indent=2)
        sys.stderr.write(f"Wrote {len(per_case)} per-case and {len(agg)} aggregate rows "
                         f"(method={method}, dim={dim}).\n")
    else:
        json.dump({"method": method, "embedding_dim": dim, "per_case": per_case, "aggregate": agg},
                  sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
