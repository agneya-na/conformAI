from engine.power_estimator import estimate_power


class PowerAgent:
    def run(self, context: dict) -> dict:
        return estimate_power(context)
