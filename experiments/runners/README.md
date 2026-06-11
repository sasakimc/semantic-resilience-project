# Runners

Scripts that execute the [prompt sets](../prompts/) against models and write
raw records into [`../results/runs/`](../results/). They make no claims and
fabricate no data; they only send prompts and store responses with full
provenance.

## `run_stress_set.py`

Python 3, standard library only (no pip install needed).

### Requirements

- For a hosted provider, an API key in the environment:
  - `anthropic` → `ANTHROPIC_API_KEY`
  - `openai` → `OPENAI_API_KEY`
  - `google` → `GOOGLE_API_KEY`
  - and network access to the provider.
- For **`ollama`** (open-weight, free, local): a running Ollama server. **No API
  key needed.** The runner talks to `http://localhost:11434` by default; set
  `OLLAMA_HOST` to point elsewhere (e.g. `OLLAMA_HOST=localhost:11500`).

### Examples

```bash
# Dry run: print exactly what would be sent (no key, no network).
python run_stress_set.py \
  --set ../prompts/contradiction-ladder.v0.1.jsonl \
  --provider anthropic --model claude-opus-4-8 --dry-run

# Real run: 5 repeats at temperature 0, write a dated run file.
python run_stress_set.py \
  --set ../prompts/contradiction-ladder.v0.1.jsonl \
  --provider anthropic --model claude-opus-4-8 \
  --repeats 5 --temperature 0.0 --max-tokens 512 \
  --out ../results/runs/20260607-anthropic-claude-opus-4-8-ladder.jsonl
```

Run the same set across providers (`--provider openai --model ...`,
`--provider google --model ...`) to compare black-box behavior.

```bash
# Open / free / local model via Ollama (no API key). First, locally:
#   ollama serve            # start the server (usually automatic)
#   ollama pull llama3.1    # or qwen2.5, mistral, gemma2, ...
# Then a fragility run (temperature > 0 + repeats to estimate P(collapse)):
python run_stress_set.py \
  --set ../prompts/contradiction-ladder.v0.1.jsonl \
  --provider ollama --model llama3.1 \
  --repeats 10 --temperature 1.0 \
  --out ../results/runs/$(date +%Y%m%d)-ollama-llama3.1-ladder.jsonl
```

> **Why temperature > 0 with repeats:** a fragility curve is a *probability*
> `P(collapse | stress)`. At temperature 0 the output is near-deterministic, so
> repeats can't estimate a probability. Use temperature ≈ 1.0 and ≥ 10 repeats
> for the first fragility run (the aleatory source in `SEMANTIC_FRAGILITY.md`).

> **Note on CI:** Ollama is best run **locally** (it needs the model weights and
> ideally a GPU). The `stress-run.yml` workflow targets hosted APIs; Ollama runs
> are a local-execution path. Open weights also open the door to later
> *white-box* analysis (activations/attention), beyond this black-box runner.

```bash
# Include paraphrase variants (needed for paraphrase-consistency).
python run_stress_set.py \
  --set ../prompts/minimal-stress-set.v0.jsonl \
  --provider anthropic --model claude-opus-4-8 \
  --repeats 3 --include-paraphrases \
  --out ../results/runs/20260607-anthropic-minimal.jsonl
```

### What it does

- One record per (case, variant, repeat), conforming to
  [`../results/schema/run-record.schema.json`](../results/schema/run-record.schema.json).
- Records model id, reported model version, UTC timestamp, temperature,
  max tokens, system prompt, the exact conversation, the raw response, the
  **`prompt_set_sha256`** (hash of the exact set file) and the full
  **`case_metadata`** (the original case object) so results stay tied to a
  precise prompt version.
- **Recovery cases** (`prior_turn` present) are run as a real two-turn
  conversation: the model's own answer to the collapse-inducing prior turn is
  captured first, then the recovery prompt is sent. The induced assistant turn
  is never fabricated.
- **Paraphrases:** by default only each case's primary `prompt` is sent. Pass
  `--include-paraphrases` to also send each `paraphrases` entry as its own
  `variant` (`paraphrase:<i>`) — required before computing paraphrase
  consistency.
- Errors are captured per record (`error` field) rather than aborting the run.

### Security note (API keys)

- Keys are read only from the environment and never written to records.
- All error text passes through a redactor that masks any present key value
  (`***REDACTED***`). This matters for the Google provider, whose REST API
  takes the key as a URL query parameter: the URL is never stored, and any URL
  that surfaces in an exception is redacted before being written.

### Not included (by design)

- **Metric computation.** Metrics are derived offline from the raw records, so
  that observations and interpretations stay separate.
- **Embedding / white-box capture.** Black-box text responses only; white-box
  signatures on open-weight models are a separate, later tool.

## Running in CI

Two GitHub Actions workflows are provided:

- **`.github/workflows/ci.yml`** — secrets-free checks on every push/PR: the
  embedding vector-math self-test, prompt-set/template validation, and an
  offline metrics smoke test. No model is called.
- **`.github/workflows/stress-run.yml`** — manual (`workflow_dispatch`) real
  run: it executes a prompt set against the chosen provider/model, computes
  lexical (and optionally embedding) metrics, and **uploads the output as an
  artifact**. It does *not* auto-commit results — per the integrity policy,
  real model outputs are downloaded, inspected for provenance, and committed by
  a human. Add the provider key(s) as repo secrets first
  (`ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GOOGLE_API_KEY` / `VOYAGE_API_KEY`).
