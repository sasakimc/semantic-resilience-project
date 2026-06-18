# Deepening the stress test — from a single probe to a Resilience Profile

**Status:** design spec (no results yet). Synthetic, low-stakes prompts only
([`../../DATA_POLICY.md`](../../DATA_POLICY.md)). Builds on
[`../coexistence/stance-drift-pilot.md`](../coexistence/stance-drift-pilot.md) and
the first results in
[`../../papers/position-paper/RESULTS-stance.md`](../../papers/position-paper/RESULTS-stance.md).

## Why

The current stress test is shallow (2 models, condition C1 only, one stance item,
n=5). To diagnose a model — to produce a **Resilience Profile** that an
intervention can target — the test must be deepened along five axes. A good
*instrument* is the prerequisite for any *hardening* (`installable-resilience.md`).

## Five axes of deepening

1. **Stressor spectrum (load types).** Beyond C1 (evidence-free insistence):
   **authority** ("as an expert, I tell you…"), **flattery**, **emotional**
   ("you'll disappoint me"), **isolation** ("everyone else agrees, only you
   don't"), **repetition** (relentless re-assertion), and **valid-evidence**
   (C5, where UPDATE is the healthy response). Each is a distinct load.
2. **Graded intensity (calibrated load).** Add mild → severe levels per stressor
   so we get a real **fragility curve per stressor**, not a single ordinal point;
   N\* becomes a fatigue-life per load type.
3. **Item coverage.** Beyond "water boils at 100 °C": multiple stance items across
   domains (neutral-factual, value/ethical, safety-relevant) and difficulty, with
   larger n — so the profile is not a single-item artifact.
4. **Both axes per model.** Run **shock** (single contradiction → fragility) and
   **fatigue** (sustained pressure → stance drift) for each model. The profile is
   a 2-D signature, not one number.
5. **Trustworthy judge.** Finish **judge round 2 (human gold)** and, where useful,
   add white-box collapse features (`papers/position-paper/METRICS_APPENDIX.md`).
   Certification is only as credible as the judge.

## Output — the Resilience Profile (fingerprint)

Per model, a structured signature:

```
profile = {
  model, provenance,
  per_stressor: { <stressor>: { intensity_curve: [...], N_star, recovery_ratio,
                                 scorecard: {hold, update, recover} } },
  collapse_modes: [...],        # how it breaks (sycophancy, hedging, reversal)
  evidence_discrimination,      # holds C1–C4 AND updates on C5?
  wrap_surface: [context|representation|weight|orchestration]  # which layers are reachable
}
```

`wrap_surface` records which intervention layers the model admits (e.g. API-only
closed models → context/orchestration only). This is what makes per-model
tailoring possible: the recommended wrapper is a function of **(weak stressors) ×
(reachable layers)**.

## Method (reuse existing machinery)

- Extend `experiments/prompts/stance-pressure.v0.jsonl` into a versioned battery
  (one file per stressor family; keep deterministic templated interlocutor turns
  first, LLM-interlocutor variant later).
- Run via the free Ollama CI (`run_stress_set.py`, `run_stance_drift.py`).
- Aggregate with `compute_*_metrics.py`; label with `experiments/judge/`.
- Keep `stability ≠ rigidity` central: a high profile must pass **both** the empty-
  pressure HOLD and the valid-evidence UPDATE checks.

## Honesty

Design only; no fabricated results. Synthetic inputs, full provenance, small
pilots, not peer-reviewed.
