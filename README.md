# Semantic Mode Theory

*English ・ [日本語](README.ja.md)*

**Exploring the principles of how meaning is formed, distorted, collapses, and recovers — in brains and in AI.**

---

> This research program investigates how meaning, function, and order in complex systems are formed, become distorted, collapse, and recover — across neuroscience, cognitive science, computational science, and AI safety research.

> **Status:** Preliminary working research program. The claims here are *working hypotheses*, not peer-reviewed results, and the metrics are operational proxies rather than direct measurements of meaning.

---

## Why Now?

Current AI safety research treats hallucination, jailbreaks, alignment failures, and robustness largely as separate phenomena. This project explores the possibility that they are manifestations of a common underlying process: **instability in semantic organization.**

If meaning inside a network has structure, then that structure can be stable or unstable, can concentrate or fragment, can collapse and reorganize. Seen this way, many of the most pressing failure modes of large language models become facets of a single question — *how does meaning hold together, and how does it fall apart?*

## The Core Idea

The program organizes a single arc:

```text
Meaning → Distortion → Collapse → Recovery
```

**Working definition (provisional).** A *semantic mode* is a dominant low-dimensional representational structure that organizes semantic behavior within a network. This is a starting point, not a settled definition — giving it a precise mathematical and computational form is itself the first research task (see Theme 1 and the position paper).

## Two Pillars

The program advances on two complementary fronts:

1. **Semantic Mode Theory** — the *explanatory* pillar. What meaning is, how it forms, and how its structure can destabilize, collapse, and reorganize.
2. **Stress Testing Framework** — the *empirical* pillar. A methodology for probing the limits of meaning systems: subjecting LLMs to contradiction, ambiguity, multiple constraints, value conflict, long context, and cognitive load, and measuring semantic robustness, collapse thresholds, and recoverability.

The theory makes the framework interpretable; the framework makes the theory testable.

## Core Research Themes

Four themes orient the entire program before the detailed questions below:

- **Semantic Modes** — meaning as dynamic, low-dimensional structure rather than a static set of facts.
- **Distortion** — how that structure becomes biased: overgeneralization, fixation, self-justification, confirmation-bias-like behavior (in humans and in LLMs).
- **Collapse** — how meaning destabilizes: hallucination, reasoning breakdown, the over-dominance or mis-binding of modes.
- **Recovery** — not a return to the former shape, but reorganization into a new mode structure.

## Research Motivation

The hallucinations, jailbreaks, sycophancy, and alignment failures exhibited by large language models (LLMs) are currently treated, for the most part, as separate problems. Yet these may differ only at the level of surface symptoms. Beneath them may lie a single shared phenomenon: **the loss of stability in semantic structure.**

Comparable phenomena appear in humans. Cognitive distortions, fixed beliefs, rigidity, overgeneralization, and self-justification can all be understood as states in which the process of meaning-making becomes biased in a particular direction and loses its stability. At the level of the brain, reorganization of networks is observed repeatedly across dementia, brain injury, learning, and recovery.

This research program attempts to reframe these phenomena within a single framework: **the formation, distortion, collapse, and recovery of semantic modes.** Its aim is to build a new research program that connects brains and AI — systems with very different substrates — through a shared language of dynamic structure.

## Core Hypothesis

- Meaning is not a static collection of knowledge, but a **dynamic mode structure** formed within a network.
- Cognitive distortion, LLM hallucination, and reasoning collapse may be understood as the **destabilization or uneven concentration** of semantic modes.
- Recovery is not a return of lost semantic structure to its former shape, but a **process of reorganization into a new mode structure.**
- Brains, cognition, and LLMs differ in implementation, but may share a **common dynamics of stability, distortion, collapse, and recovery.**

## Background

This research program sits at the intersection of the following fields.

### Deep Linear Networks and Semantic Development

The work of Andrew Saxe and colleagues on deep linear networks suggests that semantic hierarchies form progressively over the course of learning. Frameworks such as singular value decomposition (SVD) and modal analysis offer important leads for describing the formation of meaning mathematically.

### Mechanistic Interpretability

A body of work that analyzes the internal representations, attention, circuits, and features of Transformers. It provides the foundation for understanding the internal structure of LLMs and for making semantic modes observable.

### Brain Network Science

Findings on connectomes, network reorganization, dementia, and neural plasticity provide concrete examples of the formation, collapse, and recovery of semantic structure in biological systems.

### Cognitive Psychology

Concepts from cognitive psychology — cognitive distortion, confirmation bias, overgeneralization, self-justification, and catastrophizing — supply a vocabulary for describing biases in meaning-making.

### Structural and Computational Systems Thinking

Perspectives from structural and computational systems — modal analysis, stability, damage, collapse, recovery, and uncertainty — provide a framework for abstracting the dynamics common to complex systems.

## Ten Research Programs

The four themes and two pillars above unfold into ten concrete research questions. Programs 1–5 and 7–10 develop the **theory** pillar; **Program 6 (Stress Testing)** is the empirical pillar in detail.

### 1. Semantic Mode Theory

- **Question** — What is meaning?
- **Hypothesis** — Meaning is not a static symbol-to-referent correspondence, but a dynamic mode formed within a network.
- **Goal** — Provide a mathematical and computational definition of semantic modes.

### 2. Meaning Formation in Deep Networks

- **Question** — How do neural networks acquire meaning?
- **Background** — Saxe et al.'s deep linear network theory suggests that semantic hierarchies form progressively during learning.
- **Goal** — Analyze the process of meaning formation as modes, using SVD, PCA, and representational analysis.

### 3. Hallucination as Semantic Mode Instability

- **Question** — Why do LLMs hallucinate?
- **Hypothesis** — Hallucination may be understood not as mere knowledge gaps, but as the destabilization, over-dominance, or mis-binding of semantic modes.
- **Goal** — Build metrics for detecting semantic collapse.

### 4. Cognitive Distortion in Humans and LLMs

- **Question** — Do human cognitive distortions correspond to distortions in LLM reasoning?
- **Hypothesis** — The two differ in implementation, but may share common structure — overgeneralization, fixation, self-justification, and confirmation-bias-like behavior.
- **Goal** — Create a taxonomy of cognitive distortions shared between humans and LLMs.

### 5. Semantic Collapse and Recovery

- **Question** — How do semantic systems collapse, and how do they recover?
- **Hypothesis** — Recovery is not mere repair, but occurs as the reorganization of new semantic modes.
- **Goal** — Build dynamical models of collapse and recovery.

### 6. Stress Testing of Meaning Systems

- **Question** — Where are the limits of meaning systems?
- **Method** — Subject LLMs to contradiction, ambiguity, multiple constraints, value conflict, long-context, and cognitive load.
- **Goal** — Build an evaluation framework that measures semantic robustness, collapse thresholds, and recoverability.

### 7. Brain Network Reorganization and Meaning

- **Question** — How does the brain form, lose, and reorganize meaning?
- **Targets** — Dementia, brain injury, learning, neural plasticity, TBI, Alzheimer's disease.
- **Goal** — Clarify the relationship between brain network reorganization and semantic modes.

### 8. Attention as Dynamic Semantic Routing

- **Question** — What is attention doing?
- **Hypothesis** — Attention is not mere weighting, but can be understood as dynamic routing between semantic modes.
- **Goal** — Provide a semantic and dynamical interpretation of attention.

### 9. Modal Analysis of Transformer Systems

- **Question** — Can the mode structure inside a Transformer be observed?
- **Method** — Apply SVD, PCA, low-dimensional embedding, and spectral analysis to weight matrices, attention matrices, and activation representations.
- **Goal** — Visualize semantic modes and detect mode changes during collapse and recovery.

### 10. Toward a Unified Theory of Stability, Distortion, Collapse, and Recovery

- **Question** — Is there a stability principle common to structures, brains, cognition, and LLMs?
- **Hypothesis** — Complex adaptive systems may share a common dynamics of stability, distortion, collapse, and recovery.
- **Goal** — Build a general theory that integrates neuroscience, cognitive science, computational science, and AI safety research.

## Proposed Methods

- SVD / PCA / low-dimensional representational analysis
- Transformer activation analysis
- Attention pattern analysis
- Cognitive distortion prompt set
- LLM stress testing
- Hallucination and recovery evaluation
- Brain network analysis
- Normative modeling
- Dynamic state-space modeling
- Comparative analysis between human cognition and LLM behavior

## Repository Roadmap

```text
semantic-mode-theory/
├── README.md
├── papers/
│   └── position-paper/
├── references/
│   ├── saxe/
│   ├── mechanistic-interpretability/
│   ├── cognitive-distortion/
│   └── brain-network-science/
├── experiments/
│   ├── llm-stress-tests/
│   ├── cognitive-distortion-prompts/
│   ├── svd-analysis/
│   └── attention-analysis/
├── notes/
│   ├── research-ideas/
│   ├── theory-notes/
│   └── literature-notes/
└── roadmap/
```

## Initial Milestones

- **Milestone 1** — Publish the README and the research program.
- **Milestone 2** — Write the position paper.
  - Working title: *Toward a Modal Theory of Meaning Formation, Distortion, Collapse, and Recovery in Large Language Models*
- **Milestone 3** — Build a prompt set for LLM stress testing.
- **Milestone 4** — Comparative analysis of cognitive distortion taxonomy and LLM responses.
- **Milestone 5** — Initial semantic mode analysis via SVD/PCA.
- **Milestone 6** — Submit the position paper to arXiv.

## Contribution Policy

This project begins, at the current stage, as an individual research project. Solidifying the direction of the research program is the immediate priority.

In the future, the following forms of participation and collaboration are welcome:

- Collaborative research
- Help with literature review
- Experimental design
- Code implementation
- LLM evaluation
- Comments from neuroscience and cognitive science

## License

Code is licensed under the MIT License. Documentation, research text, prompt sets, and experimental materials are licensed under CC BY 4.0 unless otherwise noted. See [`LICENSING.md`](LICENSING.md) for details.

---

This research program aims to integrate neuroscience, cognitive science, computational science, and AI safety research toward a general theory of the formation, distortion, collapse, and recovery of meaning. It is not a completed theory, but a starting point for future theorization, experimentation, validation, and collaboration.
