from engine.optimizer import optimize


class OptimizationAgent:
    def run(self, context: dict) -> list[dict]:
        return optimize(context)
