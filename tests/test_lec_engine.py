from engine.lec_engine import run_lec


def test_run_lec_ok() -> None:
    assert run_lec("design.v")["ok"] is True
