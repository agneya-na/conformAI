class ReporterAgent:
    def summarize(self, results: dict) -> str:
        lines = ["open-lec-agent report"]
        for name, result in results.items():
            status = "PASS" if result.get("ok") else "FAIL"
            lines.append(f"- {name}: {status}")
        return "\n".join(lines)
