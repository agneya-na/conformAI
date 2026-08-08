from dataclasses import dataclass


@dataclass
class OptimizationStep:
    name: str
    description: str = ""
