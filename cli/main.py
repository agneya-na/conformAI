#!/usr/bin/env python3
"""ConformAI CLI — open-source Conformal alternative."""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.orchestrator import Orchestrator, OrchestratorConfig


def main():
    p = argparse.ArgumentParser(
        prog="conformai",
        description="ConformAI — Open-source LEC + UPF verification with agentic optimization",
    )
    p.add_argument("rtl", help="Golden RTL/netlist file")
    p.add_argument("--upf", help="UPF power intent file")
    p.add_argument("--top", default="top", help="Top module name")
    p.add_argument("--iterations", type=int, default=10)
    p.add_argument("--delay-budget", type=float, default=10.0)
    p.add_argument("-v", "--verbose", action="store_true")

    args = p.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    cfg = OrchestratorConfig(
        max_iterations=args.iterations,
        delay_budget_ns=args.delay_budget,
    )
    orch = Orchestrator(cfg)
    report = orch.run(args.rtl, upf_file=args.upf, top=args.top)

    print("\n" + "═" * 50)
    print("  ConformAI Final Report")
    print("═" * 50)
    for k, v in report.items():
        print(f"  {k:25s}: {v}")
    print("═" * 50)

    sys.exit(0 if report.get("status") == "PASS" else 1)


if __name__ == "__main__":
    main()
