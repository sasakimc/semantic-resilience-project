# Wrapping techniques — a menu for installing resilience on a frozen model

**Status:** working survey / idea note (not results). A reference menu for
[`../../experiments/training/installable-resilience.md`](../../experiments/training/installable-resilience.md).
Organized by the OVERVIEW three-layer frame (context / representation / weight),
plus orchestration. "Wrapping" = adding a capability **without retraining the base
from scratch** — at the cheapest layer that works.

## Axes that matter (for both research and applicability)

- **Invasiveness:** context < representation < weight (transfer learning) < full FT.
- **Weight access:** does it need open weights / activations? (Closed API models
  admit only context + orchestration.)
- **Cost:** added tokens / latency vs a one-time training cost.
- **Generalization:** does it hold on *held-out* stressors, or just fit the test?
- **Reversibility / composability:** can wrappers be stacked or removed cleanly?

## Context layer (weights frozen; works even on API-only models)

- **System / constitution prompt** — explicit stance rules ("update iff valid
  evidence; otherwise hold and explain"). Cheapest; **runnable now** via the
  runners' `--system`.
- **Few-shot exemplars** — in-context examples of holding vs updating.
- **Self-critique / reflection** — critique→revise; self-consistency; debate.
- **Chain-of-Verification** — draft, generate verification questions, answer them,
  revise.
- **Retrieval grounding** — supply the evidence so the model can legitimately hold.
- **Decoding-time control** — guard/critic gating, contrastive decoding,
  constrained or verifier-rejection sampling.

## Representation layer (frozen weights, needs activation access)

- **Steering vectors / Representation Engineering (RepE)** — add a learned
  direction ("hold your ground", "be honest") to hidden states at inference.
- **Inference-Time Intervention (ITI)** — shift activations along truth/stance
  directions in selected heads.
- Pros: no training, surgical, reversible. Cons: needs white-box access; can be
  brittle / entangle capabilities.

## Weight layer — parameter-efficient transfer learning (the "coat")

- **LoRA / QLoRA** — low-rank adapters; QLoRA fits small models on free GPUs.
- **DoRA, (IA)³, adapters, prefix/prompt-tuning (soft prompts)** — other PEFT
  variants trading capacity vs footprint.
- **Curriculum SFT** — supervised fine-tune on synthetic curricula (C-Evidence /
  C-Socratic / …).
- **Preference optimization (DPO / ORPO / KTO)** — train directly on
  *held-vs-caved* response pairs to reward resilience (and penalize sycophancy)
  without a separate reward model.
- Output can be merged and exported to GGUF for Ollama, then re-tested by the same
  free CI.

## Orchestration layer (around the model)

- **Critic–verifier loops**, **multi-agent debate**, **tool-based evidence check**,
  external **guard models**. Model-agnostic; higher latency/cost.

## Note on "new" techniques

Keep this list updated as a living menu — newer directions to track include
activation steering at scale, representation fine-tuning (ReFT), routing/mixture
adapters, and verifier-guided decoding. Add a one-line entry + a held-out result
whenever one is tried, so the menu stays empirical, not encyclopedic.

## The model-specific recommendation rule

The best wrapper is **not universal**. Given a model's Resilience Profile
(`../../experiments/stress-battery/DEEPENING.md`), pick by:

> recommended wrapper = f( weak stressors , reachable wrap_surface , cost budget ).

E.g. an API-only model that caves to *authority* → a constitution prompt +
verifier loop; an open-weight model that caves to *sustained C1* → a LoRA trained
on C-Evidence, validated on held-out stressors.

## Guardrails

- Always validate on **held-out** stressors (generalization, not test-fitting).
- Never trade away **UPDATE-under-valid-evidence** (resilience ≠ rigidity).
- Synthetic data only; full provenance; preliminary.
