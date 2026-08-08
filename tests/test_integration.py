from core.pipeline import run_pipeline


def test_integration_pipeline_smoke(tmp_path) -> None:
    design = tmp_path / "d.v"
    upf = tmp_path / "d.upf"
    cfg = tmp_path / "p.yaml"
    design.write_text("module top; endmodule\n", encoding="utf-8")
    upf.write_text("create_power_domain PD_TOP -elements {top}\n", encoding="utf-8")
    cfg.write_text("passes: [lec, upf]\n", encoding="utf-8")
    report = run_pipeline(design, upf, cfg)
    assert "lec: PASS" in report
    assert "upf: PASS" in report
