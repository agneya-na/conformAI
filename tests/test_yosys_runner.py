from engine.yosys_runner import YosysRunner


def test_yosys_runner_build_command() -> None:
    cmd = YosysRunner().build_command("design.v")
    assert cmd[0] == "yosys"
    assert "read_verilog design.v" in cmd[2]
