from core.lec import run_lec
from core.upf import run_upf


class CheckerAgent:
    def run_checks(self, plan_steps: list[str], context: dict) -> dict:
        results = {}
        if "lec" in plan_steps:
            results["lec"] = run_lec(context)
        if "upf" in plan_steps:
            results["upf"] = run_upf(context)
        return results
