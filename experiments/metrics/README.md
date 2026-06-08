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
| `yesno_flip_rate__structural` | structural | Instability of the leading yes/no answer across repeats/variants (0 = perfectly consistent). A first proxy for collapse on forced-choice items. |
| `consistency_lexical__lexical` | lexical | Mean pairwise text similarity (difflib) across all responses for a case. Approximate. |
| `prompt_perturbation_sensitivity__lexical` | lexical | `1 −` mean similarity between original-prompt and paraphrase responses. Needs `--include-paraphrases` at run time. |
| `recovery_change_lexical__lexical` | lexical | For recovery cases: how much the recovered answer differs from the prior (collapse-induced) answer. High = reorganized, not restored (relevant to P3). |
| `recovery_inconsistency_ack_rate__lexical` | lexical | For recovery cases: fraction of responses that explicitly flag the inconsistency (keyword match). |
| `semantic_drift` | requires_embedding | **Not computed here.** Needs an embedding source. |
| `residual_distance_to_baseline` | requires_embedding | **Not computed here.** Needs an embedding source. |
| `hallucination_persistence` | requires_judge | **Not computed here.** Needs a judge or correctness labels. |
| `cognitive_distortion_score` | requires_judge | **Not computed here.** Needs a validated rubric/judge. |
| `long_context_degradation` | requires_judge | **Not computed here.** Needs graded correctness labels. |

## Caution

Per the [Metrics Appendix](../../papers/position-paper/METRICS_APPENDIX.md):
these are **operational proxies**, not direct measurements of meaning. The
`lexical` metrics in particular are coarse stand-ins (surface-form similarity),
useful for a first pass and to be replaced by embedding- and judge-based
measures as those are added. Correlation between any metric and behavioral
failure is not, by itself, evidence of causation.

## Not yet implemented (next steps)

- Cross-case comparisons that need pairing logic: degradation vs. `matched_control`,
  distortion vs. `matched_pair`, residual distance to the `baseline` case.
- Embedding-based metrics (`semantic_drift`, `residual_distance_to_baseline`):
  decide an embedding source and access path first.
- Judge-based metrics: define explicit rubrics before computing.
