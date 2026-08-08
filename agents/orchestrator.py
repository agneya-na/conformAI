from pathlib import Path

import yaml

from agents.checker import CheckerAgent
from agents.parser import ParserAgent
from agents.planner import PlannerAgent
from agents.reporter import ReporterAgent


class Orchestrator:
    def __init__(self) -> None:
        self.parser = ParserAgent()
        self.planner = PlannerAgent()
        self.checker = CheckerAgent()
        self.reporter = ReporterAgent()

    def run(self, design_path: Path, upf_path: Path, passes_config_path: Path) -> str:
        graph = self.parser.parse(design_path, upf_path)
        with passes_config_path.open("r", encoding="utf-8") as handle:
            pass_data = yaml.safe_load(handle) or {}
        configured_passes = pass_data.get("passes", ["lec", "upf"])
        plan = self.planner.plan(configured_passes)
        results = self.checker.run_checks(
            plan.steps,
            {
                "graph": graph,
                "design_path": str(design_path),
                "upf_path": str(upf_path),
            },
        )
        return self.reporter.summarize(results)
