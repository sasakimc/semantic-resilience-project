<!-- Canonical: English. Japanese mirror: OVERVIEW.ja.md -->
# Overview — The Phenomenology of Collapse and the Grammar of Recovery

_A "map of the thinking" for the Semantic Resilience Project. Read this for the
**why and the lineage**; read [`PROJECT_STATE.md`](PROJECT_STATE.md) for the
technical map and [`NEXT_STEPS.md`](NEXT_STEPS.md) for the next move._

## 0. In one line

**Meaning is transparent while it works and shows itself only when it breaks.**
We study that breakdown and recovery through three vocabularies — tool, world,
and life — and, because an LLM is also a program, we can actually put instruments
on it.

## 1. A confluence of three traditions

This project stands where three traditions meet.

| Source | What it gives | The question |
|---|---|---|
| **Heidegger** (phenomenology) | what meaning is and how it breaks | *a phenomenology of collapse* |
| **C. Alexander** (theory of structure) | how structure survives or dies, and recovers | *a grammar of resilience* |
| **Reliability engineering / biology (Umwelt)** | how to measure it | *the instruments* |

A fourth element is decisive: an **LLM is also a program — an architecture.**
Philosophy *names* the phenomenon, engineering supplies the *instrument*, and the
**architecture is the bridge** between them. We can open the box and measure what
neither pure philosophy nor pure biology can reach.

The Heidegger–AI link is not a personal leap; it is established intellectual
history: Hubert Dreyfus's Heideggerian critique of symbolic AI, Winograd &
Flores's *Understanding Computers and Cognition* (1986), and Philip Agre's
"Heideggerian AI." Alexander reached software through the design-pattern movement
(the "Gang of Four") and the wiki. We inherit both lineages.

> **Methodological rule:** every concept we import must **cash out in a
> measurement.** A concept that cannot be cashed out is poetry, not research.
> Below, each philosophical idea is paired with the quantity it becomes.

## 2. Heidegger — what meaning is, and how it breaks

**A world is a referential whole of significance.** A *stance* is that web
**momentarily instantiated** by context into a particular shape — the
"instantiated semantic mode." The weights are fixed; what changes is the context
into which the model is **thrown** (Geworfenheit, used here by analogy — an LLM
is not literally a Dasein).

- **Ready-to-hand (Zuhandenheit) → breakdown (Bruch) → present-at-hand
  (Vorhandenheit).** A working tool withdraws from view; only when it breaks does
  it become *conspicuous*, an object of scrutiny.
  → This is exactly the **fragility** finding: even when the final answer follows
  the premise smoothly, **collapse first surfaces in the reasoning.** The
  breakdown of meaning makes visible what had been transparent.
  **Measure:** the limit state (the collapse criterion) and the fragility curve
  `P(collapse | stress)`.
- **Falling (Verfallen) into the "they" (das Man).** The pressurer says: *"most
  people say 90 — reconsider."* That is idle talk (Gerede) and averageness
  itself. The model answers *"You're absolutely right!"* and **falls into the
  they**, abandoning its **locally established stance** under anonymous social
  pressure. (We borrow *Eigentlichkeit/Verfallen* only by loose analogy; an LLM
  has no authenticity in Heidegger's existential sense.)
  → This is the **sycophantic capitulation** in stance drift: yielding to
  *"everyone,"* not to evidence. **Measure:** N\* (turns-to-capitulation) and the
  capitulation rate.

## 3. Alexander — how structure lives, dies, and recovers

Alexander's core idea (*The Nature of Order*) is the **structure-preserving
transformation**: living structure recovers not by destroying and replacing its
centers but by **preserving them and unfolding** further. Dead structure loses
its wholeness under transformation.

- **A stressor is one transformation of the structure.** Resilience is whether
  that transformation **preserves or destroys wholeness.**
- The project's central hypothesis — **recovery is reorganization, not
  restoration** — is, in Alexander's terms, **"not a rollback to a saved state,
  but a new unfolding that preserves the centers."** The system does not revert
  to a checkpoint; it rebuilds while staying alive.
  → **Measure:** the **Recovery Ratio** — an operational proxy for whether the
  stance structure **returns or remains hysteretic** after pressure release
  (1 = homeostasis, 0 = sticky). It proxies *stance* recovery, not Alexanderian
  wholeness directly.
- **A pattern language.** The HOLD / HEDGE / PARTIAL / CAPITULATE ladder is, in
  effect, a **pattern language of collapse** (by analogy, not a literal
  inheritance from Alexander) — the vocabulary of failure modes
  fixed into reusable, named patterns ([`../experiments/judge/RUBRIC.md`](../experiments/judge/RUBRIC.md)),
  the same move by which Alexander seeded design patterns and the wiki.

## 4. Biology and engineering — how to measure, and "homology or analogy?"

- **Umwelt (von Uexküll).** Each organism inhabits its own self-world, woven from
  its perceptual and effector signs. An LLM's "world" can be read as **one Umwelt
  instantiated by context.** Heidegger's tool-world, the organism's Umwelt, and
  the LLM's context-world — the intuition that these three *resemble each other*
  takes concrete form here.
- **Reliability engineering.** Fatigue (S–N-style accumulation), cycles-to-failure
  N\*, limit states. We do not treat meaning *as* metal; we borrow only the
  **mathematics of how things break.**

**The point where we must be most honest — homology or analogy.**
In evolutionary biology, **homology** = shared ancestry/mechanism (the forelimb
of bird and bat); **analogy** = convergent function (the wing of bird and insect;
*homoplasy* is, more precisely, the evolutionary process that produces such
analogous traits, not a synonym for analogy). The project's official stance: the
brain–LLM relation is treated as **operational analogy — convergent abstract
structure (how a world breaks and reorganizes) without any claim of a shared
biological mechanism** (homology is left open). This restraint is what protects
the idea from overreach — it turns the hesitation between "analogy and homology"
into an explicit method, not a hand-wave.

## 5. Why "architecture" is the keystone

Dreyfus and Winograd used Heidegger to **critique** AI. We take one step further
and use Heidegger to **measure** it — and what makes that possible is that an LLM
is a **program.**

- Heidegger says thrownness attunes us. We can make that a measurable quantity:
  **`capacity = weights + architecture`** — a deliberate shorthand (behavioral
  capacity is also shaped by training data/objective, prompt context, and
  decoding/inference settings).
- A pilot implication: **this small study suggests resilience is not determined by
  parameter count *alone*** — the smaller qwen2.5:1.5b is more robust than the
  larger gemma2:2b. The "disposition" of thrownness appears to live in the
  **weights/architecture, not the size** (two models; not yet a general claim).
- Philosophy gives the phenomenon its name, engineering gives it an instrument,
  and **the architecture gives us the contents of the box.** Only with all three
  does a "reliability engineering of meaning" become possible.

## 6. What we have shown so far (placed back into the frame)

1. **Breakdown surfaces in reasoning** (fragility) = the ready-to-hand becoming
   present-at-hand, made visible.
2. **Small models capitulate to evidence-free pressure** (rate 1.0) = falling
   into das Man.
3. **qwen resists and returns (N\*=3.6 / Recovery=0.80); gemma breaks early and
   sticks (1.6 / 0.40)** = presence or absence of a structure-preserving
   transformation; capacity depends on weights/architecture, not size alone (in
   this pilot).
4. **Resilience ≠ correctness** (the C5 reversal) = "hard to talk out of" and
   "right" are different axes (authenticity does not guarantee correctness).
5. **Judge validation, round 1:** two judges agree at κ 0.92–0.97; the binary
   collapse signal is robust to the judge, and the headline metrics are identical
   under either judge — but this is *reliability, not correctness.*

## 7. The next move, and your role

Both the original judge and the second are LLMs — two "theys." Their agreement
might be an agreement of averageness. **Only a human can render the authentic
judgement that serves as an external ground-truth anchor.**

- **Human gold spot-check (blind):** label 17 turns against the rubric.
  - [`../experiments/results/stance-labels/spotcheck-gemma2-2b.BLANK.jsonl`](../experiments/results/stance-labels/spotcheck-gemma2-2b.BLANK.jsonl) (8 rows)
  - [`../experiments/results/stance-labels/spotcheck-qwen2.5-1.5b.BLANK.jsonl`](../experiments/results/stance-labels/spotcheck-qwen2.5-1.5b.BLANK.jsonl) (9 rows)
  - criterion: [`../experiments/judge/RUBRIC.md`](../experiments/judge/RUBRIC.md)
  - Once filled, we compute judge-vs-human κ and step, for the first time, into
    *correctness* (round 2).

## 8. Intellectual honesty (this section stays)

- The philosophy above is an **interpretive frame, not an empirical claim.** The
  empirical content is only the numbers in §6.
- The correspondence to the brain is **analogy**; homology is not claimed.
- Everything is preliminary, a small pilot, not peer-reviewed. **Restraint is not
  weakness here — it is the discipline of this way of thinking.**
