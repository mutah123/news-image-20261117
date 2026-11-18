#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261117 competition.

Copies the pre-drawn entry.png (rendered by draw.py) into the output
directory the grader provides. Standard library only. The image path is
resolved relative to this file, never relative to the working directory,
because the grader runs this program from a different working directory.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT / "entry.png")


if __name__ == "__main__":
    main()
