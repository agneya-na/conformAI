from engine.upf_checker import check_upf
from engine.upf_parser import parse_upf


class PowerIntentAgent:
    def run(self, upf_path: str) -> dict:
        return check_upf(parse_upf(upf_path))
