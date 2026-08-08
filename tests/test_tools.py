from tools.openroad import make_upf_check_command
from tools.yosys import make_lec_command


def test_tool_commands() -> None:
    assert make_lec_command("design.v")[0] == "yosys"
    assert make_upf_check_command("intent.upf")[0] == "openroad"
