from dataclasses import dataclass


@dataclass
class PipelinePlan:
    steps: list[str]


class PlannerAgent:
    def plan(self, configured_passes: list[str]) -> PipelinePlan:
        return PipelinePlan(steps=configured_passes)
