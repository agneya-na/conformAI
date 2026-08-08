# conformAI Architecture

## Scaffold

This repository contains a mixed C++/Python scaffold for conformAI with:
- C++ core interfaces and design database stubs in `core/`
- Python engine/agents/models/cli layers
- Example RTL/UPF inputs and pytest-based validation

## Setup, Build, and Test

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cmake -S . -B build
cmake --build build
pytest -q
```
