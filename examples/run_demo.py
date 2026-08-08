#!/usr/bin/env python3
"""ConformAI end-to-end demo."""
import sys, logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.orchestrator import Orchestrator, OrchestratorConfig

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

cfg = OrchestratorConfig(max_iterations=5, delay_budget_ns=10.0)
orch = Orchestrator(cfg)

report = orch.run(
    rtl="examples/designs/counter.v",
    upf_file="examples/upf/counter.upf",
    top="counter",
)

print("\n── ConformAI Demo Result ──")
for k, v in report.items():
    print(f"  {k}: {v}")
