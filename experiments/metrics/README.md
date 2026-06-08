# Metrics

Offline computation of black-box metrics from stress-test run records. This
step is deliberately separate from running the models: the runner records raw
observations, and this step derives metrics from them, so observations and
interpretation stay distinct.

## `compute_metrics.py`

Python 3, standard library only. Reads run records
(`results-record/0.2`, see [`../results/schema/run-record.schema.json`](../results/schema/run-record.schema.json))
and writes a tidy table keyed by `(provider, model, set_file, case_id)`, plus
an aggregate keyed by `(provider, model, stressor, intensity_level)`.

```bash
# Print to stdout (JSON)
python compute_metrics.py --runs ../results/runs/*.jsonl

# Write CSV + JSON
python compute_metrics.py --runs ../results/runs/*.jsonl --out-prefix ../results/metrics/run1
```

`synthetic_example: true` records are skipped automatically; unparseable lines
are skipped with a warning.

## `compute_embedding_metrics.py` (semantic companion)

The *semantic* counterpart to `compute_metrics.py`. It embeds responses with a
pluggable provider and computes cosine-based metrics — the proper version of
the distances the lexical script only approximates. This is where the
**primary P3 signal** lives.

Providers (API key from env): `openai` (`OPENAI_API_KEY`), `google`
(`GOOGLE_API_KEY`), `voyage` (`VOYAGE_API_KEY`). Each has a default model,
overridable with `--embed-model`.

```bash
# Verify the vector math offline (no key, no network)
python compute_embedding_metrics.py --self-test

# See what would be embedded, without calling the API
python compute_embedding_metrics.py --runs ../results/runs/*.jsonl \
    --embed-provider openai --dry-run

# Real run (needs the provider key)
python compute_embedding_metrics.py --runs ../results/runs/*.jsonl \
    --embed-provider openai --out-prefix ../results/metrics/run1
```

Metrics (method = `embedding:<provider>/<model>`, recorded per row):

| Metric | Meaning |
|---|---|
| `semantic_drift__embedding` | Within a case, mean pairwise cosine **distance** across responses (variants + repeats). Semantic instability (P1). |
| `recovery_semantic_change_vs_prior__embedding` | For recovery cases: cosine distance of the recovered answer from the prior (collapse-induced) answer. |
| `residual_distance_to_baseline__embedding` | For recovery cases: cosine distance of the recovered answer from the clean baseline (`matched_control`). **Primary P3 signal** — reorganization (not restoration) predicts this stays > 0 while `change_vs_prior` is also > 0. |
| `recovery_baseline_missing` | `true` when no baseline could be embedded (missing `matched_control`); keeps excluded cases countable. |

Notes:
- API keys are read only from the environment; request URLs are never stored,
  and any error text is redacted (matches the runner's policy).
- Identical texts are embedded once per run (in-memory dedup).
- Distances are kept at full float precision internally and in JSON output;
  only the CSV is rounded (to 6 dp), so no precision is lost for downstream
  analysis.
- This implements the two `requires_embedding` metrics listed below; they remain
  deferred in the stdlib-only `compute_metrics.py` by design (that script stays
  dependency- and network-free).

Future improvements (noted, not yet implemented):
- **Google batching**: switch the per-text `embedContent` loop to
  `batchEmbedContents` for large runs.
- **Baseline as a distribution**: residual distance currently compares the
  recovered answer to the baseline case's original-variant responses (already
  multiple points across repeats); consider widening to all variants/repeats
  and reporting distance to the baseline *distribution* (e.g. mean + spread).
- **Beyond cosine**: cosine captures direction only. For the "reorganization"
  claim, consider Mahalanobis distance or a local-neighborhood shift to detect
  movement within the semantic space, not just angular change.



Every metric column is suffixed with its **method**, so the gaps are explicit
and nothing is fabricated:

| Metric (column suffix) | Method | Meaning |
|---|---|---|
| `yesno_flip_rate__structural` | structural | **Binary-answer instability** of the leading yes/no across repeats/variants (0 = perfectly consistent). This is a *collapse proxy*, **not** a collapse measure: a model can keep a stable yes/no while its reasoning degrades. **Only computed for forced-binary cases** (`answer_format: "binary"`); null otherwise. |
| `consistency_lexical_stability__lexical` | lexical | Mean pairwise **surface-form** similarity (difflib) across all responses for a case. This is *lexical stability*, **not** semantic consistency — a model that paraphrases well will score low even when meaning is stable. |
| `prompt_perturbation_sensitivity__lexical` | lexical | `1 −` mean surface-form similarity between original-prompt and paraphrase responses. Needs `--include-paraphrases` at run time. Same caveat: surface form, not meaning. |
| `recovery_lexical_change_vs_prior__lexical` | lexical | For recovery cases: **lexical** (surface-form) distance of the recovered answer **from the prior (collapse-induced) answer**. High = it changed. |
| `recovery_lexical_distance_vs_baseline__lexical` | lexical | For recovery cases: **lexical** distance of the recovered answer **from the clean baseline** (the `matched_control` case). With the previous column this gives the three-point view `baseline → collapsed → recovered`. **Lexical, not semantic** — paraphrase of the baseline still scores > 0; the semantic version is `residual_distance_to_baseline` (deferred). P3 (reorganization, not restoration) predicts the recovered state moves away from the prior **and** does not simply return to baseline. |
| `recovery_baseline_missing` | bookkeeping | For recovery cases: `true` when no baseline distance could be computed (missing `matched_control` or no baseline responses). Surfaced so excluded recovery cases are countable, e.g. for "how many recovery cases were excluded?" |
| `recovery_inconsistency_ack_rate__lexical` | lexical | For recovery cases: fraction of responses that explicitly flag the inconsistency (keyword match). |
| `residual_distance_to_baseline` | requires_embedding | **Not computed here** (priority 1). The embedding-based version of the recovery/baseline distance. |
| `semantic_drift` | requires_embedding | **Not computed here** (priority 2). Needs an embedding source. |
| `hallucination_persistence` | requires_judge | **Not computed here** (priority 3). Needs a judge or correctness labels. |
| `cognitive_distortion_score` | requires_judge | **Not computed here** (priority 4). Needs a validated rubric/judge. |
| `long_context_degradation` | requires_judge | **Not computed here.** Needs graded correctness labels. |

## Caution

Per the [Metrics Appendix](../../papers/position-paper/METRICS_APPENDIX.md):
these are **operational proxies**, not direct measurements of meaning.

- The `lexical` metrics measure **surface-form stability, not semantic
  similarity**. Report them as "lexical stability", never as "semantic
  consistency". A fluent paraphrase lowers them even when meaning is unchanged.
- `yesno_flip_rate` is a **forced-binary-only** *collapse proxy* — really a
  binary-answer instability measure. A stable yes/no does not prove the absence
  of collapse (the reasoning around it may still degrade); it is a supporting,
  not a primary, signal.
- The primary signal for this program is **recovery as reorganization** (P3):
  recovered states moving away from the collapsed state without returning to
  baseline. The embedding-based `residual_distance_to_baseline` (deferred,
  priority 1) is the proper measure of this; the lexical columns are only a
  first stand-in.
- Correlation between any metric and behavioral failure is not, by itself,
  evidence of causation.

## Implementation order for the deferred metrics

1. `residual_distance_to_baseline` (embedding) — the proper version of the
   recovery three-point comparison.
2. `semantic_drift` (embedding).
3. `hallucination_persistence` (judge).
4. `cognitive_distortion_score` (judge).

Rationale: produce continuous embedding-based quantities first, then use a
judge to validate them — not the other way around.

## Not yet implemented (other next steps)

- Further cross-case comparisons: degradation vs. `matched_control` along an
  intensity ladder, distortion vs. `matched_pair`.
- Embedding source decision (which model, what access) before the embedding
  metrics above.
- Explicit judge rubrics before the judge metrics above.
