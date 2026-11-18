#!/usr/bin/env python3
"""Entry program for news-image-20261117.

Copies the front-page image stored next to this script to the output
directory as entry.png. Deterministic: the same bytes on every run, no
network access.
"""

import os
import shutil
from pathlib import Path


def main():
    here = Path(__file__).parent
    src = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
