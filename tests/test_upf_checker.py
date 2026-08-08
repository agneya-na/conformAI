from engine.upf_checker import check_upf


def test_upf_checker_returns_ok() -> None:
    assert check_upf({"domains": []})["ok"] is True
