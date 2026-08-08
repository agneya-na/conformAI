from engine.lec_engine import run_lec


class EquivalenceAgent:
    def run(self, design_path: str) -> dict:
        return run_lec(design_path)
