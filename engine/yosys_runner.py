from dataclasses import dataclass


@dataclass
class YosysRunner:
    executable: str = "yosys"

    def build_command(self, design_path: str) -> list[str]:
        return [self.executable, "-p", f"read_verilog {design_path}; prep -top top"]
