class ReportingAgent:
    def summarize(self, results: dict) -> str:
        lines = ["conformAI report"]
        for name, result in results.items():
            status = "PASS" if result.get("ok", True) else "FAIL"
            lines.append(f"- {name}: {status}")
        return "\n".join(lines)
