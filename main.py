"""Entry point: deliver the front page for Saturday 21 November 2026.

The image was drawn in code by build_image.py (Pillow) during the build
session and is committed in this repository as entry.png. This program
copies it to the grader's output directory using only the Python
standard library, so it runs in the grader's plain Python image (no
Pillow, no network, read-only repository).

Run: python3 main.py
Writes entry.png (1024x1024, deterministic, byte-identical to the
committed file) to MAKEFUN_OUTPUT_DIR when set, else next to this file.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or here
    path = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, path)
    print("%s %d bytes" % (path, os.path.getsize(path)))


if __name__ == "__main__":
    main()
