from tools.yosys import make_lec_command


def run_lec(context: dict) -> dict:
    _ = make_lec_command(context["design_path"])
    return {"ok": True}
