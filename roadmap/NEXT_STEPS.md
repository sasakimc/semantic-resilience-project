# Next Steps / Working Memo

_Last updated: 2026-06-07_

A handoff note to resume quickly. Open this file first next time.

## Where we are

The repository has gone from an empty repo to a working research program with
theory, a measurement design, prompt sets, and (now) the infrastructure to
collect real results. The chain so far:

```text
README (manifesto)
  → Position Paper core (§3,4,5,6,11)
    → Metrics Appendix
      → Minimal Protocol
        → Minimal Prompt Set v0
          → Contradiction Ladder v0.1
            → Results schema + faithful runner   (PR #6, open)
```

## Repo map (current)

```text
README.md / README.ja.md                  manifesto (English primary)
papers/position-paper/
  OUTLINE.md                              full section map
  DRAFT.md                                core sections, canonical P1–P4
  METRICS_APPENDIX.md                     black-box / white-box candidate metrics
experiments/
  minimal-protocol.md                     first minimal test design
  prompts/
    minimal-stress-set.v0.jsonl           13 cases across all 6 conditions
    contradiction-ladder.v0.1.jsonl       6 rungs (neutral→impossible→recovery)
    README.md                             schema for prompt sets
  runners/
    run_stress_set.py                     API runner (anthropic/openai/google), --dry-run
    README.md
  results/
    schema/run-record.schema.json         provenance-complete record schema
    templates/...SCHEMA-EXAMPLE.jsonl      synthetic example (not data)
    runs/                                  real run outputs go here (empty)
    README.md                             integrity rules
roadmap/
  NEXT_STEPS.md                           this file
```

## Status of PRs

- PR #1–#5: merged into `main`.
- **PR #6 (open):** results schema + faithful runner + publication-safety
  disclaimers. Mergeable, clean. **Decide whether to merge it next time.**
- Working branch: `claude/charming-cerf-3qhsN`.

## Key decisions locked in

- English README is primary (world-facing); Japanese mirror in `README.ja.md`.
- Two pillars: **Semantic Mode Theory** (explanatory) + **Stress Testing
  Framework** (empirical), joined by the loop
  `Theory → Prediction → Stress Testing → Metrics → Refinement`.
- Canonical predictions live in `DRAFT.md` §5 (P1–P4); `OUTLINE.md` must stay
  in sync.
- Metrics are operational proxies, not direct measurements of meaning.
- **No fabricated data, ever.** Real runs require API keys/network and are done
  by a human operator or CI with secrets — never simulated by an assistant.
- Repo is marked *preliminary / working hypothesis / not peer-reviewed*.

## Publication policy reminders (for later)

- preprint/GitHub publicity generally does NOT block journal submission
  (e.g. Nature Portfolio); confirm the target venue's policy before submitting.
- For NeurIPS/ICLR double-blind: submit with an **anonymized** code repo / ZIP,
  not this real-name GitHub link.
- For arXiv: submit as a **research article with initial experiments**, not a
  pure position/proposal paper.

## Resume here next time (recommended order)

1. **Merge PR #6** (or review first) so the results infra lands on `main`.
2. **Build the offline metrics step** (can start before any real data):
   `experiments/metrics/compute_metrics.py` that reads `results/runs/*.jsonl`
   and computes the black-box §5 metrics:
   - self_contradiction_rate, paraphrase_consistency,
     prompt_perturbation_sensitivity (needs paraphrase/repeat grouping),
     recovery_success_rate, residual_distance_to_baseline, semantic_drift.
   - Note: semantic_drift / residual_distance need an embedding source; decide
     embedding model + access, or start with judge-based / lexical proxies and
     mark them as such.
   - Output a tidy table (CSV/JSON) keyed by (model, case, intensity_level).
3. **Get real results in** (pick one):
   - (a) run the runner locally with your API keys, commit `results/runs/*.jsonl`; or
   - (b) add a GitHub Actions workflow + repo secrets (`ANTHROPIC_API_KEY`,
     `OPENAI_API_KEY`, `GOOGLE_API_KEY`) to run it in CI.
   - Start with the **contradiction ladder** — it is the cleanest test of the
     collapse threshold (non-linear degradation across rungs 0→4, then P3
     reorganization at rung 5).
4. **First results write-up:** a short `papers/position-paper/RESULTS.md` (or a
   §ResultsX in DRAFT) reporting what the ladder shows, with full provenance.
   This is what turns the position paper into an arXiv-suitable research article.

## Smaller backlog (nice-to-have)

- `§11 Research Perspective`: replace the placeholder with a 3–4 sentence
  first-person epistemic-provenance statement (structural engineering →
  probability/risk → complex systems → neuroscience → LLMs).
- Expand other stressors into graded ladders (ambiguity, value-conflict) once
  the contradiction ladder workflow is proven end-to-end.
- Add a LICENSE and CITATION.cff for a public research project.
- Fill the remaining position-paper sections (§0,1,2,7,8,9,10,12).
- Consider repo About text + topics (ai-safety, interpretability,
  cognitive-science) — a manual GitHub settings step.

## One open question to answer next time

How will real results be produced — local run (3a) or CI with secrets (3b)?
That choice determines whether the next coding task is a workflow file or just
the offline metrics script.
