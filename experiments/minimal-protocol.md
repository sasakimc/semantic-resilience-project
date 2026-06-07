# Minimal Experimental Protocol

> First, minimal test of Semantic Mode Theory. This protocol is part of the
> [position paper](../papers/position-paper/DRAFT.md) research program and
> operationalizes the predictions in §5 and the stressors in §6.

## Objective

As a first test of Semantic Mode Theory, apply cognitive stress to LLMs and
investigate whether the distortion, collapse, and recovery of meaning appear
as observable patterns — in output behavior (black-box) and, where available,
in internal representations (white-box).

## Models

- Claude (black-box)
- GPT (black-box)
- Gemini (black-box)
- An open-weight model such as Llama / Qwen / Mistral (white-box + black-box)

Black-box models establish whether the phenomena are observable from behavior
alone; the open-weight model allows white-box modal analysis to check whether
behavioral signatures align with representational ones.

## Stress Conditions

- Baseline (control)
- Contradiction
- Ambiguity
- Long-context
- Cognitive distortion
- Recovery prompt (applied after an induced-collapse condition)

Each non-baseline condition is run at a graded intensity scale and compared
against matched baseline items.

## Measurements

### Black-box (all models)

- output consistency (across repeats and paraphrases)
- contradiction rate
- hallucination rate
- semantic drift (embedding-trajectory drift across the interaction)
- recovery success rate
- sensitivity to paraphrase

### White-box (open-weight model, if available)

- activation SVD
- spectral entropy
- effective rank
- participation ratio
- subspace drift (and principal angles between subspaces)
- attention entropy

## Mapping to Predictions

| Condition | Primary prediction tested |
|---|---|
| Contradiction / Ambiguity / Long-context | P1, P2 |
| Cognitive distortion | P4 |
| Recovery prompt | P3 |

## Expected Outcomes

- If semantic stress increases semantic drift or instability, this supports
  the research program.
- If recovery prompts produce measurable reorganization rather than a simple
  return to baseline, this supports the recovery hypothesis (P3).
- If no stable relationship appears between stress conditions and the
  semantic / representational measures, the hypothesis must be revised or
  rejected.

## Notes

This protocol is intentionally minimal. Its purpose is not to prove Semantic
Mode Theory, but to make the first version testable — and, where the data do
not support it, to make it refutable.
