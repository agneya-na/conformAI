from pathlib import Path

from core.ir.graph import IRGraph


class ParsingAgent:
    def parse(self, design_path: Path, upf_path: Path) -> IRGraph:
        return IRGraph(
            design_path=str(design_path),
            upf_path=str(upf_path),
            modules=["top"],
            power_domains=["PD_TOP"],
        )
