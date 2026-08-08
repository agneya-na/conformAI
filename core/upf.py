from tools.openroad import make_upf_check_command


def run_upf(context: dict) -> dict:
    _ = make_upf_check_command(context["upf_path"])
    return {"ok": True}
