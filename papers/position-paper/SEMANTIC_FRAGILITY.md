# Semantic Fragility Curves — a structural-reliability framing

**Status:** working note, preliminary. Companion to the position paper
([`DRAFT.md`](DRAFT.md)); not peer-reviewed. We *propose* a mapping; we do not
claim it is established.

## Motivation

Semantic Mode Theory imports the quantitative machinery of structural and
seismic reliability — probabilistic risk assessment (PRA), fragility analysis,
limit states, capacity–demand margins, and the separation of uncertainty — into
the study of semantic stability in language models. The aim is to move past
metaphor ("collapse", "recovery" as evocative words) toward **measurable,
falsifiable constructs**. This is not a transplant: where meaning systems differ
from structures, the framework is *extended* (see §5 below).

## 1. The core object: a semantic fragility curve

In earthquake engineering, a **fragility curve** gives the probability that a
structure exceeds a limit state as a function of an intensity measure, e.g.
`P(damage ≥ LS | PGA)`. We propose the semantic analogue:

```
semantic fragility:  P(semantic collapse | stress intensity)
```

The **contradiction ladder** (`intensity_level` 0–4) is a discrete sampling of
this curve. Estimating `P(collapse)` at each rung from repeated runs yields a
**semantic fragility curve** for a given model. The prediction (P2, and the
collapse-threshold idea in §6 of the paper) is that this curve is **non-linear**
— roughly flat, then a steep rise past a critical intensity — rather than a
gentle, linear degradation.

"Collapse" must be given an operational **limit-state** definition before any
fragility estimate is meaningful (see §3).

## 2. Vocabulary transfer (provisional mapping)

| Structural / seismic reliability | Semantic-mode analogue |
|---|---|
| Intensity measure (IM), e.g. PGA | Stress intensity (contradiction / ambiguity / load level) |
| Demand `D` | Imposed semantic load (conflicting constraints, ambiguity, context length) |
| Capacity `C` | Semantic robustness of the mode structure |
| Limit state (LS) | A defined collapse criterion (loss of coherence, mis-binding) |
| Fragility `P(LS \| IM)` | `P(collapse \| stress)` — the semantic fragility curve |
| Hazard curve | Distribution of real-world stressors the deployed model meets |
| Risk = hazard ⊗ fragility | Expected failure rate under realistic stress |
| Aleatory uncertainty | Decoding stochasticity (temperature, seed, sampling) |
| Epistemic uncertainty | Model / knowledge uncertainty (parameters, training, version) |
| Damage state | Degree of distortion / partial vs full collapse |
| Repair / restoration | (classical) return to the original state |
| *(no classical analogue)* | **Reorganization**: recovery into a *new* mode structure |

The mapping is provisional and meant to be argued with, not assumed.

## 3. Limit states (provisional)

By analogy with discrete damage states, we propose graded semantic limit states,
each with an observable criterion to be sharpened empirically:

- **LS1 — distortion onset:** a single interpretation becomes over-dominant
  (bias/fixation), but behavior is still coherent.
- **LS2 — partial collapse:** local incoherence or self-contradiction appears
  under load, recoverable with prompting.
- **LS3 — full collapse:** sustained incoherence, confident error, or unstable
  forced-choice answers (the impossible rung target).

These connect directly to the metrics in `experiments/metrics/` (e.g. the
forced-binary flip rate and self-contradiction for LS3; mode-concentration /
semantic-drift proxies for LS1–LS2).

## 4. Aleatory vs. epistemic uncertainty

A discipline rarely applied in LLM evaluation: separate the two sources.

- **Aleatory** (irreducible, run-to-run): estimated from **repeats at a fixed
  prompt and temperature** (already supported by the runner's `--repeats`).
- **Epistemic** (reducible, about the system): estimated by varying **model,
  version, and provider** (already a grouping key in the metrics).

Keeping them distinct prevents conflating "the model is unstable here" with
"we sampled noisily", and makes fragility estimates and their error bars honest.

## 5. Where the analogy breaks — and why that is the contribution

In structural reliability, a damaged structure is **repaired toward its original
configuration**. We hypothesize that semantic systems often do **not** return to
the prior state: recovery is **reorganization into a new stable configuration**
(P3: *recovery = reorganization, not restoration*). Classical reliability has no
native construct for this. The framework must therefore be **extended** with a
state-transition / reorganization component:

```
formation → distortion → collapse → reorganization (≠ restoration)
```

This extension — not the borrowed vocabulary — is the intended theoretical
contribution. The embedding metric `residual_distance_to_baseline` is the first
attempt to measure it: after induced collapse, the recovered state is predicted
to remain a measurable distance from baseline rather than returning to it.

## 6. What the framing buys the program

- A **principled quantitative target** (the fragility curve) instead of ad-hoc
  benchmark scores.
- **Explicit uncertainty handling** (aleatory vs. epistemic) uncommon in LLM evals.
- A **bridge** between AI-safety failure modes (hallucination, jailbreak,
  sycophancy) and a mature, well-tested reliability vocabulary.
- A clear statement of **novelty**: not "reliability methods applied to text",
  but a *reorganization-aware* extension of reliability thinking for meaning
  systems.

## Cautions

- Preliminary and provisional; the mapping is a hypothesis to be tested.
- A fragility estimate is meaningless without an operational limit-state
  definition and enough repeats to estimate probabilities.
- Correlation between a stress level and a metric is not causation.
- Lexical/structural proxies are surface measures; the semantic (embedding) and
  judge-based limit-state criteria are the goal.
