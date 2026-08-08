from pathlib import Path

from core.pipeline import run_pipeline


def test_pipeline_report_contains_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    report = run_pipeline(
        root / "examples" / "designs" / "simple_design.v",
        root / "examples" / "upf" / "simple.upf",
        root / "config" / "passes.yaml",
    )

    assert "lec: PASS" in report
    assert "upf: PASS" in report
