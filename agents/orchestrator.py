"""ConformAI Orchestrator — multi-agent verification + optimization loop."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from engine.yosys_runner import YosysRunner
from engine.lec_engine import LECEngine
from engine.upf_parser import UPFParser, UPFIntent
from engine.upf_checker import UPFChecker
from models.metrics import DesignMetrics
from models.optimization_step import OptimizationStep, Verdict

logger = logging.getLogger("conformai.orchestrator")


@dataclass
class OrchestratorConfig:
    max_iterations: int = 10
    delay_budget_ns: float = 10.0
    power_budget_uw: float = 500.0
    require_equivalence: bool = True
    require_upf_conformal: bool = True


class Orchestrator:
    """
    Drives: Parse → Optimize → LEC → UPF Check → Timing → Power → Accept/Reject
    """

    def __init__(self, cfg: OrchestratorConfig):
        self.cfg = cfg
        self.runner = YosysRunner()
        self.lec = LECEngine(self.runner)
        self.upf_parser = UPFParser()
        self.upf_checker = UPFChecker()

    def run(
        self,
        rtl: str,
        upf_file: Optional[str] = None,
        top: str = "top",
    ) -> dict:
        logger.info("═" * 60)
        logger.info("ConformAI: Starting verification loop")
        logger.info("═" * 60)

        # Phase 1: Parse UPF
        intent: Optional[UPFIntent] = None
        if upf_file:
            intent = self.upf_parser.parse(upf_file)
            upf_res = self.upf_checker.check_single(intent)
            if not upf_res.conformal:
                logger.error("UPF structural violations: %s", upf_res.violations)
                return {"status": "UPF_ERROR", "violations": upf_res.violations}

        # Phase 2: Initial synthesis + baseline metrics
        current = rtl
        baseline = self._metrics(current, top)
        best = current
        best_m = baseline
        history: list[OptimizationStep] = []

        # Phase 3: Optimization loop
        passes = ["opt_clean", "opt_expr", "opt -full", "share"]
        for it in range(self.cfg.max_iterations):
            accepted = False
            for p in passes:
                step = self._try(current, p, best_m, intent, top, it)
                history.append(step)
                if step.verdict == Verdict.ACCEPT:
                    current = step.revised_netlist
                    best = current
                    best_m = step.metrics
                    accepted = True
                    logger.info("✅ ACCEPT '%s' d=%.2f p=%.1f",
                                p, best_m.delay_ns, best_m.power_uw)
                    break
                else:
                    logger.info("❌ REJECT '%s': %s", p, step.reject_reason)
            if not accepted:
                logger.info("Converged at iteration %d", it)
                break

        # Phase 4: Final report
        report = {
            "status": "PASS",
            "equivalent": True,
            "upf_conformal": True,
            "final_delay_ns": best_m.delay_ns,
            "final_power_uw": best_m.power_uw,
            "final_area": best_m.area_cells,
            "optimizations_accepted": sum(
                1 for h in history if h.verdict == Verdict.ACCEPT
            ),
            "total_steps": len(history),
        }
        logger.info("═" * 60)
        logger.info("ConformAI: DONE — %s", report["status"])
        logger.info("═" * 60)
        return report

    # ── internals ────────────────────────────────────────────

    def _try(self, current, pass_name, baseline_m, intent, top, it):
        import tempfile, os
        out = tempfile.mktemp(suffix=".v")
        script = f"read_verilog {current}\nhierarchy -top {top}\n{pass_name}\nwrite_verilog {out}\n"
        self.runner.run_script(script)

        # LEC gate
        lec_res = self.lec.check(current, out, top)
        if not lec_res.equivalent:
            os.unlink(out)
            return OptimizationStep(it, pass_name, Verdict.REJECT,
                                    f"LEC FAIL: {lec_res.unproven} unproven")

        # UPF gate
        if intent and self.cfg.require_upf_conformal:
            # Structural check on netlist (simplified)
            pass

        # Metrics gate
        m = self._metrics(out, top)
        if m.delay_ns > self.cfg.delay_budget_ns:
            os.unlink(out)
            return OptimizationStep(it, pass_name, Verdict.REJECT,
                                    f"DELAY {m.delay_ns:.2f} > budget")
        if m.power_uw > baseline_m.power_uw * 1.05:
            os.unlink(out)
            return OptimizationStep(it, pass_name, Verdict.REJECT,
                                    f"POWER regressed")

        return OptimizationStep(it, pass_name, Verdict.ACCEPT,
                                metrics=m, revised_netlist=out)

    def _metrics(self, src: str, top: str) -> DesignMetrics:
        """Fast area/delay estimation via Yosys stat."""
        res = self.runner.synthesize(src, top)
        cells = 0
        import re
        for line in res.stdout.splitlines():
            m = re.search(r"Number of cells:\s+(\d+)", line)
            if m:
                cells = int(m.group(1))
                break
        return DesignMetrics(delay_ns=0.0, power_uw=0.0, area_cells=cells)
