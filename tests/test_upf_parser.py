from engine.upf_parser import parse_upf


def test_parse_upf_includes_path() -> None:
    assert parse_upf("sample.upf")["path"] == "sample.upf"
