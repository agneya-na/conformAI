from pathlib import Path

from agents.orchestrator import Orchestrator


def run_pipeline(design_path: Path, upf_path: Path, passes_path: Path) -> str:
    return Orchestrator().run(design_path, upf_path, passes_path)
