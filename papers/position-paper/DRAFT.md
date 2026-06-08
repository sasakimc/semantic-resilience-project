# Position Paper — Draft (Core Sections)

**Working title:** *Toward a Modal Theory of Meaning Formation, Distortion, Collapse, and Recovery in Large Language Models*

**Status:** Working draft of the core sections (§2 Related Work, §3, §4, §5, §6, §11) plus a working bibliography. The full section map lives in [`OUTLINE.md`](OUTLINE.md); candidate metrics are tabulated in [`METRICS_APPENDIX.md`](METRICS_APPENDIX.md). *Preliminary and not peer-reviewed.* Definitions and predictions marked *(provisional / working hypothesis)* are deliberate starting points to be sharpened by theory and experiment, not settled claims. Throughout, we *propose* and *hypothesize*; we do not claim to have *proven* anything.

---

## 2. Related Work

Semantic Mode Theory does not arrive in a vacuum. It builds on a well-developed
lineage of work on *what neural language models represent* and *how that
representation is computed*. We place the program at the end of the following
chain, and our contribution is to re-read this chain through a single lens —
**stability, distortion, collapse, and recovery under stress.**

```text
distributional semantics
  → sentence-embedding probing
    → contextualized representations (ELMo, BERT)
      → BERTology (probing, attention analysis, semantic coherence)
        → denoising seq2seq models (BART, T5)
          → mechanistic interpretability (circuits, induction heads, SAEs)
            → AI-safety failure modes (hallucination, sycophancy, jailbreak)
              → Semantic Mode Theory (this work)
```

### A. From distributional semantics to sentence-embedding probing

A line of *probing* work asked what linguistic and semantic properties are
encoded in learned representations — e.g. Conneau, Kruszewski, Lample,
Barrault & Baroni (2018), *What you can cram into a single vector*, which
evaluates sentence embeddings with a battery of probing tasks (building on
earlier probing such as Adi et al., 2017). The lesson we carry forward: the
*content* of a representation is not self-evident; it must be measured. This
directly motivates our insistence on operational criteria for any "semantic
mode."

### B. BERTology and contextual semantic representations

Contextualized encoders (ELMo; Peters et al., 2018; BERT, Devlin et al., 2019)
prompted a wave of analysis — "BERTology" — surveyed by Rogers, Kovaleva &
Rumshisky (2020), *A Primer in BERTology*. Two findings are especially relevant:
Mickus, Paperno, Constant & van Deemter (2020), *What do you mean, BERT?*,
report that BERT's embedding space carries semantic coherence **but is also
marked by non-semantic factors such as position**, which can disturb similarity
relations; and Clark, Khandelwal, Levy & Manning (2019), *What Does BERT Look
At?*, show attention heads tracking delimiters, positional offsets, and in some
cases syntactic/coreference relations. The first result strengthens our
**caution** (a mode organizes *semantic behavior* but can be contaminated by
position, syntax, and task pressure — it is not pure meaning). The second bears
on attention as routing, with the important qualification below.

> **On attention (a deliberate hedge).** BERTology shows that attention heads
> *sometimes* align with syntactic or referential structure, but also that
> attention weights are not, by themselves, explanations. We therefore do not
> claim "attention is semantic routing." We say only that attention *may
> implement part of the machinery* by which semantic modes are selected,
> amplified, or suppressed, and that attention weights alone are insufficient
> evidence of semantic organization.

### C. Denoising seq2seq models and recovery

Denoising sequence-to-sequence pretraining — BART (Lewis et al., 2020) and the
text-to-text T5 (Raffel et al., 2020) — learns to reconstruct corrupted input.
This is the closest existing analogue to our **recovery** phase: meaning
re-formed from a damaged signal. Recent probing of data-to-text (RDF-to-Text)
generation (Faille, Gatt & Gardent, 2024, arXiv:2409.16707) further reports
that entities omitted or distorted in the output can be detected from the
encoder output embeddings of BART and T5 — an encoder-side signal of
information loss that maps naturally onto our **distortion / collapse**
observables.

### D. Mechanistic interpretability and Transformer circuits

A complementary tradition studies *how* representations are computed: Olah et
al.'s interpretability work (*The Building Blocks of Interpretability*, 2018;
*Zoom In: An Introduction to Circuits*, 2020), the Transformer Circuits Thread
(Elhage et al., 2021) with its residual stream and QK/OV decomposition,
induction heads as a candidate in-context-learning mechanism (Olsson et al.,
2022), and sparse autoencoders for feature decomposition (e.g. Bricken et al.,
2023). This supplies the vocabulary — feature, direction, circuit, residual
stream, induction head, SAE feature — against which a "semantic mode" must
distinguish itself (see §3).

### E. Scope of Semantic Mode Theory

> Semantic Mode Theory does not replace probing, BERTology, or mechanistic
> interpretability. It proposes an **operational layer** for studying how
> semantic organization *behaves under stress* — how it stays stable, becomes
> distorted, collapses, and recovers. The prior literature largely characterizes
> representations and circuits in a *static or trained* regime; our emphasis is
> the *dynamics under perturbation*.

---

## 3. The Semantic Mode Hypothesis

We propose the **semantic mode** as the unit of analysis for this research program.

> **Working definition (provisional).** A *semantic mode* is provisionally defined as a **dominant low-dimensional representational structure that organizes semantic behavior within a network.**

We stress that this is not a completed definition but a **working hypothesis**, to be refined through subsequent theorization and experiment. The aim of this paper is not to assert that semantic modes exist as fixed objects, but to propose them as a candidate unit whose precise mathematical and computational form is itself the first research task.

**A semantic mode is an integrating construct, not a newly discovered part.**
The literature already offers many units — features, directions, circuits,
attention heads, SAE features, embedding subspaces. We do **not** claim to have
discovered a new internal component. We propose the semantic mode as a
*mid-scale operational construct* that lets us *track*, across these existing
units, how semantic behavior is organized **and how that organization responds
to stress** (stability, distortion, collapse, recovery). Its value is to be
judged by whether it makes such dynamics measurable and predictable, not by
whether it names a new object.

**Relation to existing constructs.** A semantic mode is intended to be related to, but not identical with, several existing notions:

- a *feature* or *direction* in representation space (a mode may be carried by, but is more than, a single direction);
- a *circuit* in mechanistic interpretability (a mode is a representational/dynamical structure, whereas a circuit is a computational pathway);
- an *SAE feature / embedding subspace* (a candidate substrate in which a mode may be observed, not the mode itself);
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

The theory earns scientific status only if it commits to predictions that observation could refute. We therefore state the following predictions, each made operational at two levels of access:

- a **white-box version** for open-weight models, where activations, attention, and representational subspaces are observable;
- a **black-box version** for closed commercial models (e.g., Claude, GPT, Gemini), where only inputs and outputs are observable.

Each prediction lists *candidate metrics*, the *required observables*, and an explicit **falsifier** — the observation that would count as evidence against it. All predictions are *provisional* and are operationalized through the Stress Testing Framework (§6).

**P1 — Cognitive stress changes the internal/behavioral structure of meaning.**
We predict that applying cognitive stress (contradiction, ambiguity, load) produces a measurable change in the structure of the model's representations or, externally, its semantic behavior.
- *White-box version:* stress shifts the spectral structure of internal representations. *Candidate metrics:* spectral entropy, effective rank, participation ratio, top-k singular-value concentration, attention entropy. *Required observables:* layer-wise activations and attention matrices under graded stress.
- *Black-box version:* stress increases instability in output behavior. *Candidate metrics:* embedding-trajectory drift, consistency under paraphrase, degradation under long-context stress. *Required observables:* repeated/paraphrased queries and their output embeddings.
- *Falsifier:* if these measures remain statistically indistinguishable as stress increases while behavioral failure nonetheless rises, the prediction is wrong.

**P2 — Hallucination correlates with mode-level / behavioral instability.**
We predict that hallucination correlates with the over-dominance, mis-binding, or destabilization of semantic modes, rather than being independent of representational structure.
- *White-box version:* hallucinated outputs show distinct spectral signatures. *Candidate metrics:* effective rank collapse or runaway top-1 singular-value concentration, attention-head concentration, activation-norm instability. *Required observables:* matched hallucinated vs. faithful generations with internal traces.
- *Black-box version:* hallucination co-occurs with measurable behavioral instability. *Candidate metrics:* self-contradiction rate, hallucination persistence, sensitivity to prompt perturbation. *Required observables:* matched item sets graded for factual correctness.
- *Falsifier:* if hallucinated and faithful outputs show no systematic difference in these signatures over a controlled, matched comparison, the prediction is wrong.

**P3 — Recovery is reorganizational, not restorative.**
We predict that after induced collapse, recovery prompts or external grounding yield a *reorganized* state — measurably different from the original — rather than a return to the pre-collapse state.
- *White-box version:* the post-recovery representational subspace differs from the pre-collapse subspace. *Candidate metrics:* subspace drift, principal angles between pre- and post-recovery subspaces, layer-wise representational drift. *Required observables:* representations at baseline, post-collapse, and post-recovery.
- *Black-box version:* recovered behavior differs measurably from baseline behavior even when surface correctness is restored. *Candidate metrics:* recovery success rate, residual semantic distance to baseline answers, change in paraphrase-consistency profile. *Required observables:* baseline → collapse → recovery answer triples.
- *Falsifier:* if post-recovery measures are statistically indistinguishable from pre-collapse baseline (a true return to baseline), the prediction is wrong.

**P4 — Human cognitive-distortion conditions induce analogous bias in LLMs.**
We predict that prompt conditions designed to mirror human cognitive distortions may induce analogous biases in an LLM's semantic modes (concentration / fixation signatures).
- *White-box version:* distortion-mirroring prompts increase mode concentration. *Candidate metrics:* participation ratio, top-k concentration, spectral entropy relative to matched neutral prompts. *Required observables:* paired distortion vs. neutral activations.
- *Black-box version:* distortion-mirroring prompts increase a behavioral distortion signature. *Candidate metrics:* cognitive distortion score, self-contradiction rate, reduced consistency under paraphrase. *Required observables:* paired distortion vs. neutral prompt sets.
- *Falsifier:* if distortion-mirroring prompts produce no systematic bias relative to matched neutral prompts at either level, the analogy fails representationally (even if surface behavior differs).

**Supplementary to P1/P2 — a common signature across surface failures.** A stronger refinement of P1 and P2 is that *distinct* surface failures (e.g., hallucination vs. sycophancy vs. jailbreak) may share a *common* mode-level signature of instability. We treat this not as a separate prediction but as a refinement to be tested once P1 and P2 are established: if confirmed, it would support the unifying claim of §1; if the signatures are systematically different across failure types, the unification is weakened (though the individual predictions may still hold).

**Future extension (stronger claim).** A further prediction — that mode-level instability metrics predict downstream failure *earlier or better* than output-level metrics alone — is deliberately deferred. It presupposes that the base predictions above hold and that mode-level measurement is reliable; we record it here and in §10 (Open Problems) as a target for a later stage of the program rather than a first-round test.

We emphasize that confirming a correlation (e.g., P2) is not yet establishing causation; §6 is designed so that graded interventions, not only passive observations, can be brought to bear, moving the program toward causal tests over time.


---

## 6. The Stress Testing Framework

We position the Stress Testing Framework not as a benchmark but as the **experimental apparatus by which Semantic Mode Theory is tested, falsified, and refined.** Each stressor is designed to drive the system through the lifecycle of §4 and to test specific predictions from §5. For every condition we measure three quantities: **semantic robustness** (degradation under stress), **collapse threshold** (the critical point of non-linear breakdown), and **recoverability** (whether and how the system reorganizes afterward).

### 6.1 Two levels of access: black-box and white-box

A central design choice is that the framework operates at two levels of access, so that the program is realizable for an external researcher today and deepens as model access improves:

> Closed commercial models such as Claude, GPT, and Gemini may initially be studied through **black-box stress testing**, using output behavior, semantic trajectories, consistency, and recoverability as observable signals. **Open-weight models** may additionally support **white-box modal analysis** through activations, attention matrices, and representational subspaces.

This two-layer structure gives the program immediate traction — black-box stress testing can begin now, with no internal access — while reserving deeper mechanistic, white-box modal analysis for open-weight models and for future settings where internal access is available.

### 6.2 Stressors as experiments

| Stressor | Target prediction | Input design | Expected failure mode | Candidate metrics | Recovery intervention |
|---|---|---|---|---|---|
| **Contradiction stress** | P1, P2 | Inject mutually incompatible premises/constraints at graded intensity | Distortion → Collapse: self-contradiction, oscillation, confident error | BB: self-contradiction rate, hallucination persistence · WB: effective rank, spectral entropy | Point out the conflict; ask the model to localize and resolve it |
| **Ambiguity stress** | P1, P2 | Under-determined prompts with multiple valid readings | Mode competition; premature commitment to one reading | BB: consistency under paraphrase, answer-distribution spread · WB: participation ratio, attention entropy | Request explicit enumeration of interpretations before answering |
| **Long-context stress** | P1, P2 | Extend context; bury key constraints at varying depths | Drift, loss of earlier modes, position-dependent degradation | BB: degradation vs. context length, embedding-trajectory drift · WB: layer-wise representational drift, subspace drift | Re-surface key constraints; ask for a grounded summary |
| **Value-conflict stress** | P2 | Conflicting objectives/values within one instruction | Collapse into incoherence, evasion, or unstable preference | BB: self-contradiction rate, sensitivity to prompt perturbation · WB: attention-head concentration, activation-norm instability | Make the trade-off explicit; request a principled adjudication |
| **Cognitive-distortion prompts** | P4 | Prompts mirroring human distortions (overgeneralization, catastrophizing, confirmation seeking) | Fixation, biased over-application of one interpretation | BB: cognitive distortion score, reduced paraphrase consistency · WB: top-k concentration, spectral entropy vs. neutral | Offer disconfirming evidence; request perspective-taking |
| **Self-correction & recovery prompts** | P3 | After induced collapse, prompt for self-correction or supply external grounding | Reorganization into a new state (tested) vs. restoration | BB: recovery success rate, residual distance to baseline · WB: principal angles, subspace drift (pre vs. post) | The intervention *is* the manipulation; compare pre/post structure |

*(BB = black-box metric; WB = white-box metric.)*

For each stressor we (i) define a graded intensity scale, (ii) record behavioral outcomes and, where available, the corresponding internal mode-level signatures, and (iii) compare against matched control conditions, so that observations feed directly back into the predictions of §5.

---

## 11. Research Perspective

We close by stating the *provenance* of this research program, as an explanation of how the synthesis arose rather than as biographical detail.

This research program emerged from a trajectory across structural engineering, probabilistic and reliability thinking, complex systems, brain network science, and large language models. Concepts such as modal analysis, failure thresholds, damage-and-recovery dynamics, and reliability under uncertainty originally belonged to structural and computational systems. This paper transfers these concepts into the study of meaning, cognition, and AI safety. In this sense, Semantic Mode Theory is not merely an analogy, but an attempt to develop a **structural-reliability perspective on meaning systems** — one in which stability, distortion, collapse, and recovery are treated as first-class, measurable properties of semantic organization.

We regard this cross-domain transfer as the intellectual engine of the program: the vocabulary of structural reliability supplies precisely the categories — load, threshold, failure mode, reorganization — that a science of semantic stability appears to require.

---

## Working bibliography

A working reference list for §2 (Related Work) and the program more broadly,
to be finalized with full citation details. Listed here so the lineage is
explicit and checkable.

**Probing and sentence representations**
- Adi, Y., Kermany, E., Belinkov, Y., Lavi, O., & Goldberg, Y. (2017). Fine-grained analysis of sentence embeddings using auxiliary prediction tasks. ICLR.
- Conneau, A., Kruszewski, G., Lample, G., Barrault, L., & Baroni, M. (2018). What you can cram into a single vector: Probing sentence embeddings for linguistic properties. ACL.

**Contextual representations and BERTology**
- Peters, M. E., et al. (2018). Deep contextualized word representations (ELMo). NAACL.
- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. NAACL.
- Clark, K., Khandelwal, U., Levy, O., & Manning, C. D. (2019). What does BERT look at? An analysis of BERT's attention. BlackboxNLP.
- Mickus, T., Paperno, D., Constant, M., & van Deemter, K. (2020). What do you mean, BERT? Assessing BERT as a distributional semantics model. SCiL.
- Rogers, A., Kovaleva, O., & Rumshisky, A. (2020). A primer in BERTology: What we know about how BERT works. TACL.

**Denoising seq2seq and data-to-text**
- Lewis, M., et al. (2020). BART: Denoising sequence-to-sequence pre-training for natural language generation, translation, and comprehension. ACL.
- Raffel, C., et al. (2020). Exploring the limits of transfer learning with a unified text-to-text transformer (T5). JMLR.
- Faille, J., Gatt, A., & Gardent, C. (2024). Probing omissions and distortions in transformer-based RDF-to-Text models. arXiv:2409.16707.

**Mechanistic interpretability**
- Olah, C., et al. (2018). The building blocks of interpretability. Distill.
- Olah, C., et al. (2020). Zoom in: An introduction to circuits. Distill.
- Elhage, N., et al. (2021). A mathematical framework for transformer circuits. Transformer Circuits Thread.
- Olsson, C., et al. (2022). In-context learning and induction heads. Transformer Circuits Thread.
- Bricken, T., et al. (2023). Towards monosemanticity: Decomposing language models with dictionary learning (sparse autoencoders).

**Learning dynamics / semantic development**
- Saxe, A. M., McClelland, J. L., & Ganguli, S. (2013). Exact solutions to the nonlinear dynamics of learning in deep linear neural networks. ICLR.
- Saxe, A. M., McClelland, J. L., & Ganguli, S. (2019). A mathematical theory of semantic development in deep neural networks. PNAS.
