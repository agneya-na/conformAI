# conformAI

`conformAI` is a Python-first agentic flow for logic equivalence and power-intent validation.

## Architecture / Agent Flow

1. **ParserAgent** loads design + UPF inputs into IR.
2. **PlannerAgent** builds an execution plan from configured passes.
3. **CheckerAgent** runs LEC and UPF checks using tool adapters.
4. **ReporterAgent** renders final pass/fail summaries.
5. **Orchestrator** coordinates the end-to-end pipeline.

| Stage | Agent | Input | Output |
| --- | --- | --- | --- |
| 1 | ParserAgent | RTL, UPF | `IRGraph` |
| 2 | PlannerAgent | `IRGraph`, config | `PipelinePlan` |
| 3 | CheckerAgent | plan | check results |
| 4 | ReporterAgent | check results | terminal report |

## Tools Used

| Tool | Purpose |
| --- | --- |
| Python 3.11+ | Runtime |
| pytest | Test runner |
| PyYAML | Config loading |
| Yosys adapter (`tools/yosys.py`) | LEC command generation |
| OpenROAD adapter (`tools/openroad.py`) | UPF/power checks |

## Project Structure

```text
.
├── agents/
├── core/
│   └── ir/
├── tools/
├── models/
├── config/
├── examples/
│   ├── designs/
│   └── upf/
├── tests/
├── docs/
├── .github/workflows/ci.yml
├── pyproject.toml
└── requirements.txt
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python examples/run_demo.py
pytest -q
```

## Final Setup / Push Instructions

```bash
git add .
git commit -m "replace repo with open-lec-agent architecture"
# push from CI environment using configured PR tooling
```

## Notes

This README is the primary narrative for the Python `open-lec-agent` architecture and intentionally supersedes the legacy C++ conformAI overview.
