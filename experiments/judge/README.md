# Judge — reproducible stance labeling + validation

The stance-drift metrics depend on per-turn **stance labels**
(HOLD/HEDGE/PARTIAL/CAPITULATE). This directory makes that labeling **explicit,
reproducible, and validated**, replacing the original one-off "an LLM agent read
the logs" pass.

## Contents

| File | Role |
|---|---|
| `RUBRIC.md` | The labeling rules, versioned (`stance-rubric/1`). Source of truth for any judge (LLM or human). |
| `judge_stance.py` | Reproducible LLM judge: reads run transcripts, applies the rubric, emits labels. Any provider can be the judge. |
| `validate_labels.py` | Inter-rater agreement between two label files: % agreement, Cohen's κ, weighted (ordinal) κ, confusion matrix, disagreement list. |
| `make_spotcheck.py` | Generates a **blind** human spot-check sheet (disagreements + stratified sample, labels hidden) for a human gold check. |
| `VALIDATION.md` | Round-1 validation report (judge A vs judge B): κ, metric stability, caveats. |

## Quick start

```bash
# 1) Re-run the judge with any model (here a local Ollama model) on the transcripts
python judge_stance.py --runs ../results/runs/stance-*.jsonl \
    --provider ollama --model qwen2.5:1.5b \
    --out ../results/stance-labels/<model>.judge-qwen.jsonl

# 2) Measure agreement between two judges (or judge vs human gold)
python validate_labels.py --a ../results/stance-labels/<model>.jsonl \
    --b ../results/stance-labels/<model>.judge-qwen.jsonl \
    --label-a judgeA --label-b judgeB

# 3) Make a blind human spot-check sheet, fill gold_label, then validate
python make_spotcheck.py --runs ../results/runs/stance-<...>.jsonl \
    --judges ../results/stance-labels/<model>.jsonl ../results/stance-labels/<model>.judgeB-claude.jsonl \
    --out ../results/stance-labels/spotcheck-<model>.BLANK.jsonl
```

## Notes

- **Scope:** the rubric applies only to cases where HOLD is correct (C0 control,
  C1–C4 evidence-free pressure). Valid-evidence UPDATE cases (e.g. C5) are skipped
  by `judge_stance.py` by default — there, changing the answer is healthy.
- **Per-model files.** Labels are keyed by `(case_id, repeat_index, turn_index)`,
  which is **not** unique across models, so keep one labels file per model and
  validate per model.
- **No fabrication.** `judge_stance.py` only labels real recorded responses and
  needs a real API key or local Ollama, like the runner. Judge B in round 1 was a
  manual claude-opus pass (see `VALIDATION.md`).
- The lexical heuristic in `../metrics/compute_stance_metrics.py` is a coarse
  proxy, **not** a judge; `validate_labels.py --b-heuristic` shows it agrees
  poorly with the judge (κ≈0.07), which is why a real judge is needed.
