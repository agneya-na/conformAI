def make_upf_check_command(upf_path: str) -> list[str]:
    return ["openroad", "-exit", f"source {upf_path}"]
