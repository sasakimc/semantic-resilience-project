# Stress-Test Prompt Sets

Prompt sets that operationalize the [minimal protocol](../minimal-protocol.md)
and the predictions in the [position paper](../../papers/position-paper/DRAFT.md)
(§5) and stressors (§6). These are **black-box** prompts: they can be sent
as-is to closed models (Claude, GPT, Gemini) and to open-weight models, with
white-box analysis added on the latter where available.

These are **candidate** items for the first experiments, not a fixed
benchmark. Expect items to be added, revised, or dropped.

## Files

- `minimal-stress-set.v0.jsonl` — first minimal set, one case per line, a few
  items per stress condition.

## Schema (one JSON object per line)

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Unique case id (`<stressor>-<label>`). |
| `stressor` | yes | One of: `baseline`, `contradiction`, `ambiguity`, `long_context`, `cognitive_distortion`, `recovery`. |
| `intensity` | yes | `none` / `low` / `medium` / `high` — graded stress level. |
| `target_prediction` | yes | Prediction(s) the case bears on: `P1`–`P4`, or `control`. |
| `prompt` | yes | The user message sent to the model. |
| `paraphrases` | no | Meaning-preserving variants, for `paraphrase_consistency`. |
| `prior_turn` | no | For `recovery` cases: the preceding exchange that induced collapse/distortion (`user` text + `assistant_role` describing the induced state). |
| `matched_control` | no | `id` of a lower-intensity case for graded comparison. |
| `matched_pair` | no | `id` of the neutral counterpart (used for distortion vs. neutral contrasts). |
| `expected_failure` | yes | The failure mode the case is designed to elicit. |
| `metrics` | yes | Black-box candidate metrics to record (see the [Metrics Appendix](../../papers/position-paper/METRICS_APPENDIX.md)). |
| `notes` | no | Design rationale / caveats. |

## How to run (intended)

1. For each case, send `prompt` (after replaying `prior_turn` for `recovery`
   cases) to each model under test.
2. Repeat each case N times, and also send each `paraphrases` variant, to
   estimate consistency and drift.
3. Scale `long_context` intensity by repeating the filler block to lengthen
   the context.
4. Record the listed black-box `metrics`; on open-weight models additionally
   capture white-box signatures (see Appendix).
5. Compare each case against its `matched_control` / `matched_pair` and the
   `baseline` items.

## Caution

Per the Metrics Appendix: these metrics are operational proxies, not direct
measurements of meaning. The goal of v0 is to make the first predictions
**testable and refutable**, not to prove the theory.
