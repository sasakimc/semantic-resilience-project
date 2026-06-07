# Position Paper — Draft (Core Sections)

**Working title:** *Toward a Modal Theory of Meaning Formation, Distortion, Collapse, and Recovery in Large Language Models*

**Status:** Working draft of the core sections (§3, §4, §5, §6, §11). The full section map lives in [`OUTLINE.md`](OUTLINE.md). Definitions and predictions marked *(provisional / working hypothesis)* are deliberate starting points to be sharpened by theory and experiment, not settled claims. Throughout, we *propose* and *hypothesize*; we do not claim to have *proven* anything.

---

## 3. The Semantic Mode Hypothesis

We propose the **semantic mode** as the unit of analysis for this research program.

> **Working definition (provisional).** A *semantic mode* is provisionally defined as a **dominant low-dimensional representational structure that organizes semantic behavior within a network.**

We stress that this is not a completed definition but a **working hypothesis**, to be refined through subsequent theorization and experiment. The aim of this paper is not to assert that semantic modes exist as fixed objects, but to propose them as a candidate unit whose precise mathematical and computational form is itself the first research task.

**Relation to existing constructs.** A semantic mode is intended to be related to, but not identical with, several existing notions:

- a *feature* or *direction* in representation space (a mode may be carried by, but is more than, a single direction);
- a *circuit* in mechanistic interpretability (a mode is a representational/dynamical structure, whereas a circuit is a computational pathway);
- an *eigenmode / singular component* of a linear operator (the latter offers a mathematical analogue, and a candidate operationalization, rather than a definition).

The hypothesis is that meaning, at the level relevant to behavior, is organized by a relatively small number of such dominant structures, and that their configuration — how they form, dominate, interact, and reorganize — governs the stability of semantic behavior.

**Toward an operational criterion.** For the definition to become precise, we propose it must be paired with (i) a *measurement criterion* and (ii) a *behavioral signature*. Candidate measurement criteria include the dominant components obtained from SVD/PCA of activations or weight matrices, and the spectral structure of attention. The corresponding behavioral signature is that perturbing or removing the structure produces a coherent, interpretable change in semantic behavior. Establishing such a criterion — so that "semantic mode" is measurable rather than merely evocative — is **Research Task #1** of the program.

---

## 4. The Lifecycle of Meaning: Formation, Distortion, Collapse, and Recovery

We hypothesize that semantic systems pass through a recurring four-phase lifecycle. We describe each phase as an *observable* phenomenon, so that the lifecycle can be studied rather than merely asserted.

### 4.1 Formation

Semantic modes form, and a stable semantic structure emerges between input and output. This may occur over the course of training, and — we hypothesize — also dynamically within context. *Candidate observable:* the staged emergence and separation of dominant components (connecting to the staged learning dynamics of deep linear networks), measurable as growth in the leading singular/principal values of internal representations.

### 4.2 Distortion

A particular semantic mode becomes excessively dominant, giving rise to overgeneralization, fixation, and confirmation-bias-like behavior. Distortion is hypothesized to be the LLM analogue of human cognitive distortion: not a loss of structure, but a *biasing* of it. *Candidate observable:* increased skew or concentration in the mode spectrum (a small number of modes capturing a disproportionate share of representational variance), together with behavioral over-application of a single interpretation.

### 4.3 Collapse

Coherence *between* semantic modes is lost, producing hallucination, contradiction, and reasoning breakdown. We hypothesize that collapse is not simply missing knowledge but a structural event — the over-dominance, mis-binding, or destabilization of modes. *Candidate observable:* a measurable collapse signature, such as spectral flattening (loss of clear dominant structure), runaway dominance of a single mode, or a sharp, non-linear degradation of behavior past a critical level of stress.

### 4.4 Recovery

Recovery occurs not as a simple return to the prior state, but as **reorganization into a new semantic mode structure.** We hypothesize that external grounding, self-correction, or recovery prompts induce a reconfiguration rather than a restoration. *Candidate observable:* the post-recovery representation is measurably different from the pre-collapse representation, even when surface behavior appears restored.

---

## 5. Falsifiable Predictions

The theory earns scientific status only if it commits to predictions that observation could refute. We therefore state the following predictions, each paired with an explicit **falsifier** — the observation that would count as evidence against it. These predictions are *provisional* and intended to be operationalized through the Stress Testing Framework (§6).

**P1 — Cognitive stress changes internal spectral structure.**
We predict that applying cognitive stress (contradiction, ambiguity, load) produces a measurable change in the spectral structure of the LLM's internal representations.
*Falsifier:* if internal spectral structure remains statistically indistinguishable under increasing stress while behavioral failure nonetheless rises, the prediction is wrong.

**P2 — Hallucination correlates with mode-level instability.**
We predict that hallucination correlates with the over-dominance, mis-binding, or destabilization of semantic modes, rather than being independent of internal representational structure.
*Falsifier:* if hallucinated and faithful outputs show no systematic difference in mode-level signatures (over a controlled, matched comparison), the prediction is wrong.

**P3 — Recovery is reorganizational, not restorative.**
We predict that after induced collapse, recovery prompts or external grounding yield a representation that is *reorganized* — measurably different from the original — rather than restored to the pre-collapse state.
*Falsifier:* if post-recovery representations are statistically indistinguishable from pre-collapse representations (a true return to baseline), the prediction is wrong.

**P4 — Human cognitive-distortion conditions induce analogous mode bias in LLMs.**
We predict that prompt conditions designed to mirror human cognitive distortions may induce analogous biases in an LLM's semantic modes (e.g., concentration/fixation signatures).
*Falsifier:* if distortion-mirroring prompts produce no systematic mode-level bias relative to matched neutral prompts, the analogy fails at the representational level (even if surface behavior differs).

We note that confirming a correlation (e.g., P2) is not yet establishing causation; §6 and §7 are designed so that interventions, not only observations, can be brought to bear.

---

## 6. The Stress Testing Framework

We position the Stress Testing Framework not as a benchmark but as the **experimental apparatus by which Semantic Mode Theory is tested, falsified, and refined.** Each stressor is designed to drive the system through the lifecycle of §4 and to test specific predictions from §5. For each, we measure three quantities: **semantic robustness** (degradation under stress), **collapse threshold** (the critical point of non-linear breakdown), and **recoverability** (whether and how the system reorganizes afterward).

| Stressor | Intended effect (lifecycle) | Primarily tests |
|---|---|---|
| **Contradiction stress** | drive Distortion → Collapse via incompatible constraints | P1, P2 |
| **Ambiguity stress** | probe mode competition under under-determined input | P1, P2 |
| **Long-context stress** | probe mode maintenance and drift over extended context | P1, P2 |
| **Value-conflict stress** | induce collapse via conflicting objectives/values | P2 |
| **Cognitive-distortion prompts** | induce human-distortion-analogous mode bias | P4 |
| **Self-correction and recovery prompts** | induce Recovery; test reorganization vs. restoration | P3 |

For each stressor we (i) define a graded intensity scale, (ii) record behavioral outcomes and the corresponding internal mode-level signatures, and (iii) compare against matched control conditions, so that observations feed directly back into the predictions of §5.

---

## 11. Research Perspective

We close by stating the *provenance* of this research program, as an explanation of how the synthesis arose rather than as biographical detail.

This research program emerged from a trajectory across structural engineering, probabilistic and reliability thinking, complex systems, brain network science, and large language models. Concepts such as modal analysis, failure thresholds, damage-and-recovery dynamics, and reliability under uncertainty originally belonged to structural and computational systems. This paper transfers these concepts into the study of meaning, cognition, and AI safety. In this sense, Semantic Mode Theory is not merely an analogy, but an attempt to develop a **structural-reliability perspective on meaning systems** — one in which stability, distortion, collapse, and recovery are treated as first-class, measurable properties of semantic organization.

We regard this cross-domain transfer as the intellectual engine of the program: the vocabulary of structural reliability supplies precisely the categories — load, threshold, failure mode, reorganization — that a science of semantic stability appears to require.
