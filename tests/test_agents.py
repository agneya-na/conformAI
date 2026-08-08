from agents.reporting_agent import ReportingAgent


def test_reporting_agent_summary() -> None:
    out = ReportingAgent().summarize({"lec": {"ok": True}})
    assert "conformAI report" in out
