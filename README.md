# ConformAI

**Open-source Agentic AI for LEC + UPF Power-Aware Equivalence Verification**

An open-source alternative to Cadence Conformal — with UPF (IEEE 1801) verification,
SAT-based equivalence checking, and multi-agent optimization. Built for tapeout.

---

## ✨ Highlights

- ✅ SAT-based LEC via Yosys `equiv_*` flow
- ✅ IEEE 1801 UPF parsing + structural checks
- ✅ Multi-agent optimization + verification orchestrator
- ✅ C++20 core design database with strong ID types
- ✅ Python-first CLI and demo workflow

---

## 🧭 Interactive Navigation

- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [How It Works](#-how-it-works)
- [Demo](#-demo)
- [CLI Usage](#-cli-usage)
- [Build & Test](#-build--test)
- [Roadmap](#-roadmap)

---

## 🏗 Architecture

ConformAI combines a **high-performance C++ core** with a **Python verification and agent orchestration layer**.

- **C++ core (`core/`)**: design database, hierarchy/entities, UPF intent data structures
- **Python engines (`engine/`)**: Yosys runner, LEC flow, UPF parser/checker, metrics/estimators
- **Agent layer (`agents/`)**: orchestrates optimization + acceptance gates (LEC/UPF/timing/power)
- **Models (`models/`)**: shared typed models for metrics, optimization steps, and verdicts
- **CLI (`cli/`)**: user entrypoint to run end-to-end conformality loop

---

## 📂 Project Structure

```text
conformAI/
├── CMakeLists.txt
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── Makefile
│
├── core/                          # C++20 Core Engine
│   ├── CMakeLists.txt
│   ├── include/
│   │   └── conformai/
│   │       ├── types.hpp
│   │       ├── design_db.hpp
│   │       ├── module.hpp
│   │       ├── net.hpp
│   │       ├── pin.hpp
│   │       ├── instance.hpp
│   │       ├── power_domain.hpp
│   │       └── upf_intent.hpp
│   └── src/
│       ├── design_db.cpp
│       ├── module.cpp
│       ├── net.cpp
│       ├── pin.cpp
│       ├── instance.cpp
│       ├── power_domain.cpp
│       └── upf_intent.cpp
│
├── engine/                        # Python Verification Engine
│   ├── __init__.py
│   ├── yosys_runner.py
│   ├── lec_engine.py
│   ├── upf_parser.py
│   ├── upf_checker.py
│   ├── timing_estimator.py
│   ├── power_estimator.py
│   └── optimizer.py
│
├── agents/                        # Agentic AI Layer
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── parsing_agent.py
│   ├── equivalence_agent.py
│   ├── power_intent_agent.py
│   ├── timing_agent.py
│   ├── power_agent.py
│   ├── optimization_agent.py
│   └── reporting_agent.py
│
├── models/                        # Data Models
│   ├── __init__.py
│   ├── metrics.py
│   ├── lec_result.py
│   ├── upf_models.py
│   └── optimization_step.py
│
├── cli/
│   ├── __init__.py
│   └── main.py
│
├── examples/
│   ├── designs/
│   │   ├── counter.v
│   │   ├── mac_unit.sv
│   │   └── ai_acc_top.sv
│   ├── upf/
│   │   ├── counter.upf
│   │   └── ai_acc_top.upf
│   └── run_demo.py
│
├── tests/
│   ├── test_design_db.py
│   ├── test_yosys_runner.py
│   ├── test_lec_engine.py
│   ├── test_upf_parser.py
│   ├── test_upf_checker.py
│   ├── test_agents.py
│   └── test_integration.py
│
├── config/
│   ├── default.yaml
│   └── passes.yaml
│
└── docs/
    ├── ARCHITECTURE.md
    └── UPF_SUPPORT.md
```

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
sudo apt install yosys cmake

# Build C++ core
mkdir build && cd build && cmake .. && make -j$(nproc) && cd ..

# Run demo
python examples/run_demo.py

# Run CLI
python cli/main.py examples/designs/counter.v --upf examples/upf/counter.upf --top counter
```

---

## ⚙️ How It Works

1. **Parse UPF** → extract domains/isolation/retention/level-shifter intent
2. **Run baseline synthesis** → collect initial area/timing/power estimates
3. **Iterative optimization loop**
   - apply optimization pass
   - enforce **LEC equivalence gate**
   - enforce **UPF conformity gate**
   - enforce **metrics budgets**
4. **Accept/Reject pass** with reasoned verdict
5. **Emit final report** (status, metrics, accepted steps)

---

## 🧪 Demo

```bash
python examples/run_demo.py
```

Expected output: final PASS/FAIL style report with delay/power/area + accepted optimization count.

---

## 💻 CLI Usage

```bash
python cli/main.py <rtl_file> [--upf <file.upf>] [--top <top_module>] [--iterations N] [--delay-budget NS] [-v]
```

Example:

```bash
python cli/main.py examples/designs/counter.v --upf examples/upf/counter.upf --top counter --iterations 5 --delay-budget 10.0 -v
```

---

## 🛠 Build & Test

```bash
# Build
make build

# Python tests
make test

# Lint
make lint

# Clean artifacts
make clean
```

---

## 🗺 Roadmap

- [ ] Full UPF command coverage (beyond structural subset)
- [ ] Real timing/power estimator integration (Liberty + activity)
- [ ] Multi-file netlist partitioning + distributed checks
- [ ] Rich HTML/PDF reporting
- [ ] CI workflows for C++ + Python + sample designs

---

## 📜 License

Apache-2.0
