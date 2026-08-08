def normalize_design_name(path: str) -> str:
    return path.rsplit("/", maxsplit=1)[-1]
