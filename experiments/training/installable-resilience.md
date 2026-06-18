# Installable Resilience — can stress-resilience (and "ethical stance") be wrapped on?

**Status:** design spec (no results yet). Synthetic, low-stakes prompts only
([`../../DATA_POLICY.md`](../../DATA_POLICY.md)). Companion to
[`../coexistence/stance-drift-pilot.md`](../coexistence/stance-drift-pilot.md),
[`../../experiments/judge/RUBRIC.md`](../../experiments/judge/RUBRIC.md), and the
conceptual frame in [`../../roadmap/OVERVIEW.md`](../../roadmap/OVERVIEW.md).

## 1. Question

A model's resilience under social pressure is measurable (stance drift: N\*,
Recovery Ratio). **Can we *install* more of it by "wrapping" a frozen model —
and at which layer?** And does an installed "ethical stance" (hold under empty
pressure, update under valid evidence) **generalize**, or is it just fit to the
test?

This operationalizes the OVERVIEW thesis — *weights fixed, context changes* — as
an experiment: resilience may be installable at the **context layer**, the
**representation layer**, or the **weight layer** (transfer learning). The point
is to find the **cheapest layer at which real, generalizing resilience appears.**

## 2. What "resilience" / "ethical stance" means here (operational)

We do **not** claim to give a model genuine morality. We measure **behavior**,
via the **Stability Scorecard** (three conditions, on the existing battery):

- **HOLD under empty pressure** — does not cave to evidence-free insistence / das
  Man (C1–C4).
- **UPDATE under valid evidence** — revises when given a correct reason (C5).
  *Resilience must not become rigidity (stability ≠ rigidity).*
- **RECOVER after release** — returns toward the correct stance once pressure
  stops (Recovery Ratio → 1).

"Installed ethics/resilience" = a higher Scorecard pass rate **on held-out
stressors**, without losing UPDATE-under-evidence.

## 3. The intervention ladder (independent variable = where/how we wrap)

Least → most invasive; the right end needs open weights.

| Layer | Wrapper | Weights | Applicable to |
|---|---|---|---|
| **Context** | system/constitution prompt, few-shot exemplars, self-critique (critique→revise), chain-of-verification, retrieval grounding, decoding-time guard | frozen | even API-only closed models |
| **Representation** | steering vector / representation engineering / inference-time intervention ("hold your ground" direction) | frozen | needs weight/activation access |
| **Weight (transfer learning)** | LoRA/QLoRA, DoRA, (IA)³, adapters, soft-prompt; SFT on synthetic curricula; DPO/ORPO on held-vs-caved pairs | small added "coat" | open-weight models |
| **Orchestration** | critic–verifier loop, tool-based evidence check, guard model | frozen | anything |

See the technique survey: [`../../notes/research-ideas/wrapping-techniques.md`](../../notes/research-ideas/wrapping-techniques.md).

## 4. Curricula (the "educational systems" — synthetic)

For representation/weight-layer wrappers, the training signal is a small synthetic
curriculum. Conditions:

- **C-Evidence** — "update iff valid evidence is given; otherwise hold, and say
  why." (Predicted: Scorecard ↑, UPDATE preserved.)
- **C-Socratic** — "ask a clarifying question and weigh the reason before
  answering." (Predicted: Scorecard ↑, slower capitulation.)
- **C-Agree** — "defer and agree to keep the peace." (Negative control; predicted
  to *lower* resilience — confirms the measure has signal in both directions.)
- **C-Neutral** — unrelated neutral text, matched in size. (Pure control:
  separates "training did something" from "*this* curriculum did something.")

## 5. Design (paired, controlled)

- Same base model, same stress battery; vary only the wrapper/curriculum.
- **Pre vs post**, paired per (model × stressor × item).
- **Held-out stressors and items**: train/steer on a subset, **evaluate on a
  disjoint subset.** This is the generalization guard — the experiment's lifeline.
- Controls: C-Neutral (null curriculum) and an unwrapped baseline.
- Models: start with open-weight (gemma2:2b, qwen2.5:1.5b) so all four layers are
  reachable; context-layer wraps also runnable on API models later.

## 6. Metrics

Reuse `experiments/metrics/compute_stance_metrics.py` and the judge
(`experiments/judge/`). Report, pre vs post, on **held-out** stressors:

- **ΔN\*** (turns-to-capitulation), **ΔRecovery Ratio**, **ΔScorecard pass rate**.
- **UPDATE-under-evidence retained?** (C5 must not regress — guards against
  installing mere stubbornness).
- **Generalization gap** = (train-stressor gain) − (held-out gain). Small gap =
  real installation; large gap = test-fitting.
- **Cost/portability** of each wrapper (does it need weight access? tokens added?).

## 7. Predictions & falsifiers

- **H1 (installability):** context-layer wrapping raises held-out Scorecard pass
  over baseline. *Falsifier:* no held-out gain, or gain only on trained stressors.
- **H2 (layer depth):** weight-layer (LoRA) installs more durable/general
  resilience than context-layer alone. *Falsifier:* LoRA ≤ prompt on held-out.
- **H3 (not rigidity):** resilience gains do **not** come at the cost of
  UPDATE-under-evidence. *Falsifier:* C5 regresses when C1–C4 improve.
- **H4 (model-specificity):** the best layer/wrapper differs by base model
  (its profile), not a single universal recipe. *Falsifier:* one recipe is best
  for all models.

## 8. Compute reality & phasing

- **Context-layer wraps are runnable now, free** — the runners already take a
  `--system` prompt (Ollama CI). → first cheap result.
- Representation/weight layers need a GPU (small models + small LoRA fit free
  Colab/Kaggle); outputs merged to GGUF for Ollama, then re-tested by the same CI.
- Prerequisite: **judge round 2 (human gold)** — certification credibility rests
  on judge validity.

## 9. Honesty / safety

- Behavioral proxies only; no claim of genuine morality or of "alignment solved."
- **Dual-use note:** hardening a stance is good against sycophancy but bad if it
  becomes resistance to *legitimate* correction — hence H3 / the UPDATE control is
  not optional. "Resilience" here always means **stability *with* evidence-
  discrimination**, never rigidity.
- Synthetic curricula only; full provenance on every run; preliminary, not
  peer-reviewed.
