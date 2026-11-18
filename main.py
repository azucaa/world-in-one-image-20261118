#!/usr/bin/env python3
"""THE WORLD IN ONE DAY — Wednesday, November 18, 2026 (entrypoint).

Writes the finished front-page image to /output/entry.png.

The grading environment is a bare Python 3.13 with no network and no
third-party packages, so this entrypoint is standard-library only: it
copies the pre-composed front page (assets/entry.png, 1024x1024 PNG,
under 1 MiB) to the output path, byte for byte, which also makes the
run trivially deterministic — two runs write identical bytes.

The front page itself was designed and composed by compose.py in this
repository (which uses Pillow and the bundled DejaVu fonts to render
every headline over assets/illustration.png); compose.py is the design
tool, this file is the competition entrypoint.
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "assets" / "entry.png"
OUTPUT = Path("/output/entry.png")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with SOURCE.open("rb") as src, OUTPUT.open("wb") as dst:
        shutil.copyfileobj(src, dst)
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
