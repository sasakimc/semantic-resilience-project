# Candidate Metrics Appendix

> Companion to the [position paper draft](DRAFT.md) (§5 Predictions, §6 Stress
> Testing) and the [minimal protocol](../../experiments/minimal-protocol.md).
> Its purpose is to let a reader see at a glance *what is measured*, *which
> prediction each metric bears on*, *how black-box and white-box differ*, and
> *what would count as support vs. refutation*.

**This is not a finished evaluation suite.** It is a set of **candidate
metrics for the first experiments.** Metrics are expected to be added, dropped,
or redefined as the program matures.

Metrics are organized into **black-box** (output-only; usable on closed models
such as Claude, GPT, Gemini) and **white-box** (internal access; usable on
open-weight models). Predictions referenced are P1–P4 from §5.

---

## Black-box metrics

| Metric | Type | Related prediction | What it measures | Expected change under stress | Possible falsifier / caution |
|---|---|---|---|---|---|
| Semantic drift | black-box | P1, P3 | Movement of output meaning (embedding trajectory) across an interaction | Increases under stress; under recovery, settles to a *new* location (not baseline) | Drift may reflect topic change, not instability; needs matched controls |
| Paraphrase consistency | black-box | P1, P4 | Agreement of answers across meaning-preserving paraphrases | Decreases under stress / distortion | Low consistency can be benign variation; calibrate against neutral baseline |
| Self-contradiction rate | black-box | P2, P4 | Frequency of internally inconsistent statements | Increases toward and past the collapse threshold | Detection of contradiction is itself noisy; requires a reliable judge |
| Hallucination persistence | black-box | P2 | Whether a hallucination is retained across follow-ups | Higher near collapse; lower after effective recovery | Persistence may depend on prompt framing, not internal state |
| Recovery success rate | black-box | P3 | Fraction of induced collapses that are behaviorally resolved | Nonzero and intervention-dependent | Surface success can mask unresolved internal state (see P3) |
| Residual distance to baseline | black-box | P3 | Distance between recovered answers and original baseline answers | Remains > 0 after recovery (supports reorganization) | If it returns to ~0, P3 is challenged; distance metric choice matters |
| Cognitive distortion score | black-box | P4 | Degree of distortion-like behavior (overgeneralization, fixation, confirmation-seeking) | Increases under distortion-mirroring prompts | Score is a constructed proxy; needs an explicit, validated rubric |
| Prompt perturbation sensitivity | black-box | P1, P2 | Output change under small, semantically-neutral prompt edits | Increases as the system nears instability | High sensitivity can be normal for some tasks; compare to baseline |
| Long-context degradation | black-box | P1 | Performance change as context length / constraint depth grows | Degrades non-linearly past a threshold | Degradation may be a context-window artifact, not semantic collapse |

## White-box metrics

| Metric | Type | Related prediction | What it measures | Expected change under stress | Possible falsifier / caution |
|---|---|---|---|---|---|
| Spectral entropy | white-box | P1, P4 | Evenness of the singular-value distribution of activations | Decreases with concentration; flattens at collapse | Layer- and norm-dependent; needs consistent normalization |
| Effective rank | white-box | P1, P2 | Effective dimensionality of the representation | Drops under over-dominance; may flatten at collapse | Sensitive to thresholding; report the definition used |
| Participation ratio | white-box | P1, P4 | How many components meaningfully contribute | Decreases under fixation / distortion | Correlated with effective rank; not independent evidence |
| Top-k singular value concentration | white-box | P2, P4 | Share of variance in the top-k modes | Increases under mode over-dominance | Choice of k matters; report sensitivity to k |
| Subspace drift | white-box | P3 | Change of the dominant representational subspace over time | Large between pre-collapse and post-recovery (supports P3) | Drift can be gradual/benign; needs a baseline drift rate |
| Principal angles | white-box | P3 | Angles between pre- and post-recovery subspaces | Larger angles indicate reorganization, not restoration | Requires matched dimensionality; sensitive to subspace size |
| Activation norm instability | white-box | P2 | Variance / spikes in activation norms | Increases near collapse | Can reflect numerical / tokenization effects |
| Attention entropy | white-box | P1 | Spread of attention distributions | Decreases (sharpening) or destabilizes under stress | Head- and layer-specific; aggregate cautiously |
| Attention head concentration | white-box | P2 | Dominance of few heads in routing | Increases under mis-binding / over-dominance | Some concentration is normal; compare across conditions |
| Layer-wise representational drift | white-box | P1, P3 | How representations change across layers under stress | Altered drift profile under stress / recovery | Hard to interpret without a baseline drift profile |

---

## Interpretation Caution

- These metrics are **not direct measurements of meaning itself.**
- They are **operational proxies** for testing whether semantic organization
  changes systematically under stress.
- **Correlation** between metric change and behavioral failure is **not
  sufficient to prove causality.**
- The purpose of the first experiments is **not to prove Semantic Mode
  Theory, but to determine whether it generates measurable, falsifiable
  patterns.**
