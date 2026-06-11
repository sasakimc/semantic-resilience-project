# Results

Raw outputs from running the [prompt sets](../prompts/) against models, plus
(later) the metrics computed from them. This directory stores **observations,
not conclusions**.

## Integrity rules (non-negotiable)

1. **No fabricated data.** Every record here must come from an actual API call.
   The only non-real file permitted is a clearly-labeled schema example under
   `templates/` with `"synthetic_example": true`.
2. **Full provenance on every record:** model id, reported model version, date
   (UTC), provider, temperature, max tokens, system prompt, exact prompt /
   conversation, and repeat count. The runner records all of these.
3. **Metrics are computed separately and offline** from the raw records, and
   are operational proxies, not direct measurements of meaning (see the
   [Metrics Appendix](../../papers/position-paper/METRICS_APPENDIX.md)).
4. **Synthetic-only inputs; no real personal or patient data.** Runs use only the
   synthetic prompts in this repository. See [`DATA_POLICY.md`](../../DATA_POLICY.md).

## Layout

```text
results/
├── README.md
├── schema/
│   └── run-record.schema.json      # JSON Schema for one (case, repeat) record
├── templates/
│   └── example-run-record.SCHEMA-EXAMPLE.jsonl   # synthetic, illustration only
└── runs/                            # real run outputs go here (one .jsonl per run)
```

Suggested run-file naming: `runs/<YYYYMMDD>-<provider>-<model>-<set>.jsonl`.

## How results are produced

Use the runner in [`../runners/run_stress_set.py`](../runners/run_stress_set.py),
which calls the model API and writes one record per (case, repeat) conforming
to `schema/run-record.schema.json`. Recovery cases are run as a faithful
two-turn conversation in which the model's own collapse-induced answer is
captured before the recovery prompt is sent.

> **Note on execution.** Producing real results requires API keys and network
> access (`ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `GOOGLE_API_KEY`). These
> runs are performed by a human operator (or a CI job with secrets); they are
> not, and must not be, simulated by an assistant role-playing as the model.

## Validating a run file

```bash
python - <<'PY'
import json, sys
from pathlib import Path
rec_schema = json.loads(Path("schema/run-record.schema.json").read_text())
req = rec_schema["required"]
path = sys.argv[1] if len(sys.argv) > 1 else "runs/example.jsonl"
bad = 0
for i, line in enumerate(Path(path).read_text().splitlines(), 1):
    if not line.strip():
        continue
    r = json.loads(line)
    missing = [k for k in req if k not in r]
    if missing:
        print(f"line {i}: missing {missing}"); bad += 1
    if r.get("synthetic_example") is True:
        print(f"line {i}: WARNING synthetic_example=true (not real data)")
print("OK" if not bad else f"{bad} problem(s)")
PY
```
