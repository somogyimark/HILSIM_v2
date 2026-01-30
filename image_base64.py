import base64
from pathlib import Path


def image_to_base64(path: str | Path) -> str:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    with open(path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode("utf-8")

    return encoded
