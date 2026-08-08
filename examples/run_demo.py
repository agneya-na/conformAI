import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.pipeline import run_pipeline


if __name__ == "__main__":
    print(
        run_pipeline(
            ROOT / "examples" / "designs" / "simple_design.v",
            ROOT / "examples" / "upf" / "simple.upf",
            ROOT / "config" / "passes.yaml",
        )
    )
