from pathlib import Path


def test_design_db_cpp_file_exists() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "core" / "src" / "design_db.cpp").exists()
