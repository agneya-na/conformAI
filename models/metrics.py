from dataclasses import dataclass


@dataclass
class Metrics:
    area: float = 0.0
    timing_slack: float = 0.0
    power_mw: float = 0.0
