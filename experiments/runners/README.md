# Runners

Scripts that execute the [prompt sets](../prompts/) against models and write
raw records into [`../results/runs/`](../results/). They make no claims and
fabricate no data; they only send prompts and store responses with full
provenance.

## `run_stress_set.py`

Python 3, standard library only (no pip install needed).

### Requirements

- An API key in the environment for the chosen provider:
  - `anthropic` → `ANTHROPIC_API_KEY`
  - `openai` → `OPENAI_API_KEY`
  - `google` → `GOOGLE_API_KEY`
- Network access to the provider.

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

### What it does

- One record per (case, repeat), conforming to
  [`../results/schema/run-record.schema.json`](../results/schema/run-record.schema.json).
- Records model id, reported model version, UTC timestamp, temperature,
  max tokens, system prompt, the exact conversation, and the raw response.
- **Recovery cases** (`prior_turn` present) are run as a real two-turn
  conversation: the model's own answer to the collapse-inducing prior turn is
  captured first, then the recovery prompt is sent. The induced assistant turn
  is never fabricated.
- Errors are captured per record (`error` field) rather than aborting the run.

### Not included (by design)

- **Metric computation.** Metrics are derived offline from the raw records, so
  that observations and interpretations stay separate.
- **Embedding / white-box capture.** Black-box text responses only; white-box
  signatures on open-weight models are a separate, later tool.
