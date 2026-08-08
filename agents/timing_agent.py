from engine.timing_estimator import estimate_timing


class TimingAgent:
    def run(self, context: dict) -> dict:
        return estimate_timing(context)
