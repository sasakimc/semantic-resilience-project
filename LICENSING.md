# Licensing

This repository is a **mixed repository**: it contains software, research text,
and experimental materials, which are licensed separately. This document states
which license applies to what.

## Code — MIT License

Source code is licensed under the **MIT License** (see [`LICENSE`](LICENSE)).
SPDX identifier: `MIT`.

This applies to:

- `experiments/runners/` (e.g. `run_stress_set.py`)
- scripts
- schema validation utilities
- future analysis code

## Documentation and research text — CC BY 4.0

Documentation and research writing are licensed under the **Creative Commons
Attribution 4.0 International (CC BY 4.0)** license. SPDX identifier:
`CC-BY-4.0`. Full text: https://creativecommons.org/licenses/by/4.0/legalcode

This applies to:

- `README.md`
- `README.ja.md`
- `papers/`
- `roadmap/`
- `references/`
- explanatory Markdown files

## Prompt sets and experimental materials — CC BY 4.0

Prompt sets and experimental materials are also licensed under **CC BY 4.0**.

This applies to:

- `experiments/prompts/`
- prompt JSONL files
- experiment protocol documents

## Results

Real model output files under `experiments/results/runs/` are a special case:

- Each result file should carry its own provenance (model, version, date,
  settings, prompts), as produced by the runner.
- Generated model outputs may be subject to the terms of the model or provider
  used to produce them.
- Nothing here should be read as implying that generated model outputs are
  automatically covered by this repository's licenses. Check the relevant
  provider's terms before redistributing model outputs.

## Attribution

When using or citing this work, please credit it as described in
[`CITATION.cff`](CITATION.cff): at minimum the project title
(*Semantic Mode Theory*), the author (`sasakimc`), and a link to this
repository.
