# Position Paper — Outline

**Working title:** *Toward a Modal Theory of Meaning Formation, Distortion, Collapse, and Recovery in Large Language Models*

**Status:** Draft outline (skeleton). Each section gives a 2–3 sentence summary of what it will argue. Predictions and definitions marked *(provisional)* are deliberate starting points, to be sharpened, not settled claims.

**Audience:** the AI safety / interpretability research community, and brain/cognitive scientists working on representation and reorganization.

---

## The spine of the paper

The paper is organized around a single research loop, not a single claim:

```text
Theory → Prediction → Stress Testing → Observation → Theory Refinement
```

This is what turns "Semantic Mode Theory" from an interesting idea into a *research program*: the theory generates falsifiable predictions, the stress-testing framework produces observations, and the observations refine the theory.

---

## 0. Abstract

State the unifying conjecture: hallucination, jailbreaks, sycophancy, and alignment failure may be surface manifestations of a single underlying process — *instability in semantic organization*. Introduce the *semantic mode* as the proposed unit of analysis and the four-phase lifecycle (formation → distortion → collapse → recovery). Position the paper as a research program with both an explanatory pillar (theory) and an empirical pillar (stress testing), connected by a closed prediction–observation loop.

## 1. Introduction — Why Now?

Current AI safety research treats hallucination, jailbreaks, sycophancy, alignment failure, and robustness largely as separate problems with separate fixes. This paper explores whether they are better understood as different *failure modes of the same thing*: the loss of stability in how meaning is organized inside a network. We argue the field now has the tools (mechanistic interpretability, representational/spectral analysis, scalable stress testing) to make this conjecture testable rather than merely philosophical.

## 2. Background and Related Work

The lineage (full prose with citations in [`DRAFT.md`](DRAFT.md) §2):

```text
distributional semantics → sentence-embedding probing → contextual reps (ELMo, BERT)
  → BERTology → denoising seq2seq (BART, T5) → mechanistic interpretability
    → AI-safety failure modes → Semantic Mode Theory
```

- **Sentence-embedding probing (Conneau, Lample, Barrault, Baroni; Adi et al.).** What linguistic/semantic content a representation encodes must be *measured*, not assumed — motivating our operational criteria.
- **BERTology and contextual representations (Devlin et al.; Rogers et al.; Mickus et al.; Clark et al.).** Contextual semantic structure exists but is contaminated by non-semantic factors (e.g. position); attention sometimes aligns with structure but is not, alone, an explanation.
- **Denoising seq2seq (BART, T5) and data-to-text probing.** Reconstruction of corrupted input as the closest existing analogue to our *recovery* phase; encoder-side detection of omission/distortion as a *distortion/collapse* signal.
- **Mechanistic interpretability (Olah; Transformer Circuits; induction heads; SAEs).** The vocabulary — feature, direction, circuit, residual stream, induction head, SAE feature — against which a semantic mode must distinguish itself.
- **Deep linear networks and semantic development (Saxe et al.).** Staged emergence of semantic hierarchy via singular values/modes — the mathematical anchor for "meaning as mode."
- **Brain network science / cognitive psychology.** Biological precedents for formation/collapse/reorganization; distortion taxonomies as a vocabulary for biased meaning-making.
- **Modal / spectral / reliability analysis.** SVD, PCA, spectral methods, stability and failure-threshold analysis imported from structural and computational systems thinking.

Summary: the paper sits at the end of this lineage. Its novelty is not a new internal part but the *transfer* of stability/collapse/recovery (stress) reasoning into the study of meaning, as an operational layer over existing units.

## 3. The Semantic Mode Hypothesis

Give the *(provisional)* definition: a **semantic mode** is a dominant low-dimensional representational structure that organizes semantic behavior within a network. Distinguish it from related notions (features, directions, circuits, eigenmodes) and state what would make the definition *precise*: an operational criterion (e.g., via SVD/PCA of activations or weights, spectral structure of attention) plus a behavioral signature. Make explicit that producing this precise definition is Research Task #1, not an assumption.

## 4. The Lifecycle of Meaning

Develop the four phases as the theory's core object, each with proposed observables:

- **4.1 Formation.** How modes emerge during training/in-context; staged, hierarchical, mode-by-mode (connect to Saxe). *Observable:* growth/separation of dominant components over training or context.
- **4.2 Distortion.** How a mode becomes biased or over-weighted; the LLM analogue of cognitive distortion. *Observable:* skew/concentration in the mode spectrum; behavioral over-application.
- **4.3 Collapse.** How meaning destabilizes — hallucination, reasoning breakdown — as over-dominance, fragmentation, or mis-binding of modes. *Observable:* a measurable collapse signature (e.g., spectral collapse / mode flattening / runaway dominance).
- **4.4 Recovery.** Why recovery is *reorganization into a new mode structure*, not restoration of the old one. *Observable:* post-perturbation mode reconfiguration that differs from the pre-perturbation state.

## 5. Predictions (Falsifiable)

State concrete, testable predictions the theory commits to *before* observation. *(provisional, to be operationalized)* The canonical statements, with white-box / black-box versions, candidate metrics, required observables, and falsifiers, live in [`DRAFT.md`](DRAFT.md) §5; the summary below must stay in sync with it.

- **P1.** Cognitive stress (contradiction, ambiguity, load) produces a measurable change in the structure of meaning — internally (spectral structure) and/or behaviorally. *Supplementary:* whether distinct surface failures (hallucination vs. sycophancy vs. jailbreak) share a *common* mode-level signature of instability is treated as a refinement of P1/P2.
- **P2.** Hallucination correlates with mode-level / behavioral instability (over-dominance, mis-binding, destabilization), rather than being independent of representational structure.
- **P3.** Recovery is reorganizational, not restorative: after induced collapse, the recovered state is measurably different from the original, not a return to it.
- **P4.** Prompt conditions mirroring human cognitive distortions induce analogous bias (concentration / fixation signatures) in an LLM.

Each prediction is paired with a way it could be *wrong* (the falsifier). *Future extension (see §10):* whether mode-level instability metrics predict downstream failure **earlier/better** than output-level metrics alone is a stronger claim to be added once the base predictions hold.

## 6. The Stress Testing Framework (Empirical Pillar)

Describe the methodology that produces the observations. Define the stressors — contradiction, ambiguity, multiple constraints, value conflict, long context, cognitive load — and the three core measurements: **semantic robustness**, **collapse threshold**, and **recoverability**. Specify how each stressor maps to a prediction in §5, so the framework is not "yet another benchmark" but a theory-driven instrument.

## 7. The Research Loop

Make the spine explicit: theory yields §5 predictions; §6 stress tests yield observations; observations confirm, bound, or refute predictions; the theory is refined and the loop repeats. Argue this loop is the unit of progress for the program and the criterion by which the theory earns scientific status.

## 8. Implications for AI Safety

Recast hallucination, jailbreak, sycophancy, and alignment failure as facets of semantic instability, and discuss what changes if that view is correct: shared metrics, earlier detection at the representation level, and interventions aimed at stabilizing/reorganizing modes rather than patching symptoms individually. Be explicit about what the theory does *not* yet claim to solve.

## 9. Bridges to Brains and Cognition

Lay out the comparative program: the same lifecycle (formation/distortion/collapse/recovery) as a lens on brain network reorganization (plasticity, injury, dementia) and human cognitive distortion. Frame this as a source of hypotheses and cross-checks, not as a claim of mechanistic identity between brains and LLMs.

## 10. Limitations and Open Problems

Name the hard parts honestly: the definition is provisional; "mode" may be measurement-dependent; correlation between mode signatures and failures is not yet causation; cross-substrate (brain↔LLM) claims are analogical until grounded. List the open problems that the program must close to mature — including the **stronger, deferred claim** that mode-level metrics predict downstream failure *earlier/better* than output-level metrics (a target for a later stage, contingent on the base predictions of §5 holding).

## 11. Research Perspective (Why This Synthesis)

Explain the *provenance* of the theory rather than the author's credentials. The lens — modal analysis, failure thresholds, damage-and-recovery dynamics, reliability under uncertainty — is imported from structural and probabilistic-risk engineering and re-applied to *meaning*; this cross-domain transfer is the intellectual engine behind the program. The interdisciplinary path (structural engineering → probability/risk → complex systems → neuroscience → LLMs) is therefore part of the argument, explaining why this particular integration became visible from this vantage point.

> *Placeholder — to be confirmed/filled by the author:* a 3–4 sentence first-person statement of the path above, written as epistemic justification (why this integration was possible from this background), not as a CV.

## 12. Conclusion

Restate that this is a starting point: a conjecture, a unit of analysis, a lifecycle, a set of falsifiable predictions, and a loop to test them. Invite collaboration and adversarial testing, and state the immediate next steps (operationalize the definition; build the stress-test prompt set; run the first SVD/PCA mode analyses).

---

## Drafting order (suggested)

1. §3 (definition) + §4 (lifecycle) — fix the conceptual core first.
2. §5 (predictions) + §6 (stress testing) — make it falsifiable.
3. §1 (Why Now?) + §0 (abstract) — frame for the reader once the core is solid.
4. §2, §8, §9, §10, §11, §12 — situate, extend, and qualify.
