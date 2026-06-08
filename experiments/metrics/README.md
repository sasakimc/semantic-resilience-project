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

## What is computed (and what is not)

Every metric column is suffixed with its **method**, so the gaps are explicit
and nothing is fabricated:

| Metric (column suffix) | Method | Meaning |
|---|---|---|
| `yesno_flip_rate__structural` | structural | Instability of the leading yes/no answer across repeats/variants (0 = perfectly consistent). **Only computed for forced-binary cases** (`answer_format: "binary"`); null otherwise, because a leading yes/no is unreliable on free-form/ambiguous items. |
| `consistency_lexical_stability__lexical` | lexical | Mean pairwise **surface-form** similarity (difflib) across all responses for a case. This is *lexical stability*, **not** semantic consistency — a model that paraphrases well will score low even when meaning is stable. |
| `prompt_perturbation_sensitivity__lexical` | lexical | `1 −` mean surface-form similarity between original-prompt and paraphrase responses. Needs `--include-paraphrases` at run time. Same caveat: surface form, not meaning. |
| `recovery_change_vs_prior__lexical` | lexical | For recovery cases: how far the recovered answer moved **from the prior (collapse-induced) answer**. High = it changed. |
| `recovery_distance_vs_baseline__lexical` | lexical | For recovery cases: how far the recovered answer is **from the clean baseline** (the `matched_control` case's responses). Together with the previous column this gives the three-point view `baseline → collapsed → recovered`: P3 (reorganization, not restoration) predicts the recovered state moves away from the prior **and** does not simply return to baseline. |
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
- `yesno_flip_rate` is a **forced-binary-only** collapse proxy; it is not
  applied to free-form or ambiguous items.
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
