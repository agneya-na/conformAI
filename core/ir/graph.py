from dataclasses import dataclass, field


@dataclass
class IRGraph:
    design_path: str
    upf_path: str
    modules: list[str] = field(default_factory=list)
    power_domains: list[str] = field(default_factory=list)
