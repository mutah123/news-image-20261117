#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261117 bounty (v3).

Runs draw.py and writes entry.png to the output directory. Stdlib only.
Resolves files relative to this script, never relative to the CWD, so the
grader can run it from any working directory and get identical bytes.

Output directory comes from MAKEFUN_OUTPUT_DIR, default /output.
"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

sys.path.insert(0, str(HERE))

import draw  # noqa: E402

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    img = draw.build()
    img.save(OUT / "entry.png", optimize=True)
    print("wrote", OUT / "entry.png")
