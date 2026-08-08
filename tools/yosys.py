def make_lec_command(design_path: str) -> list[str]:
    return ["yosys", "-p", f"read_verilog {design_path}; prep -top top"]
