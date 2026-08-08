"""ConformAI — Yosys subprocess runner (optimized, zero-copy where possible)."""

from __future__ import annotations

import subprocess
import tempfile
import os
import re
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger("conformai.yosys")

__all__ = ["YosysResult", "YosysRunner"]


@dataclass(frozen=True, slots=True)
class YosysResult:
    success: bool
    returncode: int
    stdout: str
    stderr: str
    elapsed_ms: float = 0.0

    @property
    def log(self) -> str:
        return self.stdout + "\n" + self.stderr


class YosysRunner:
    """Thin, fast wrapper around Yosys CLI."""

    __slots__ = ("_bin", "_timeout")

    def __init__(self, yosys_bin: str = "yosys", timeout: int = 600):
        self._bin = yosys_bin
        self._timeout = timeout
        self._verify()

    def _verify(self) -> None:
        try:
            r = subprocess.run(
                [self._bin, "--version"],
                capture_output=True, text=True, timeout=10,
            )
            if r.returncode != 0:
                raise RuntimeError(f"yosys error: {r.stderr.strip()}")
            logger.info("Yosys: %s", r.stdout.strip())
        except FileNotFoundError:
            raise RuntimeError(
                f"'{self._bin}' not found. Install: sudo apt install yosys"
            )

    def run_script(self, script: str, *, timeout: Optional[int] = None) -> YosysResult:
        """Execute a Yosys TCL script string."""
        import time
        t0 = time.perf_counter()

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ys", delete=False
        ) as f:
            f.write(script)
            path = f.name

        try:
            r = subprocess.run(
                [self._bin, "-s", path],
                capture_output=True, text=True,
                timeout=timeout or self._timeout,
            )
            elapsed = (time.perf_counter() - t0) * 1000
            return YosysResult(
                success=(r.returncode == 0),
                returncode=r.returncode,
                stdout=r.stdout,
                stderr=r.stderr,
                elapsed_ms=elapsed,
            )
        except subprocess.TimeoutExpired:
            return YosysResult(False, -1, "", "TIMEOUT")
        finally:
            os.unlink(path)

    def synthesize(self, src: str, top: str = "top") -> YosysResult:
        script = f"""
read_verilog {src}
hierarchy -top {top}
proc; opt; memory; opt; techmap; opt
stat
"""
        return self.run_script(script)

    def write_json(self, src: str, out: str, top: str = "top") -> YosysResult:
        script = f"""
read_verilog {src}
hierarchy -top {top}
proc; opt; memory; opt; techmap; opt
write_json {out}
"""
        return self.run_script(script)
