# conformAI

`conformAI` provides a C++/Python scaffold for logic equivalence and power-intent validation workflows.

## Repository Layout

- `core/`: C++ IR and design-database scaffold
- `engine/`: Python execution engines (LEC, UPF, timing, power, optimizer)
- `agents/`: orchestration and domain agents
- `models/`: shared Python data models
- `cli/`: command-line entrypoint
- `examples/`: sample RTL and UPF inputs
- `tests/`: pytest and C++ scaffold tests

## Setup, Build, and Test

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cmake -S . -B build
cmake --build build
pytest -q
```
