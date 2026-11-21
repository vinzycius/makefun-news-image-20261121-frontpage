"""Entry point: draw the front page for Saturday 21 November 2026.

Run: python3 main.py
Writes entry.png (1024x1024, deterministic) next to this file.
"""

import os
import sys

# The grader runs `python3 -P -s`, which does not put this file's directory
# on sys.path; add it so the sibling module can be imported.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_image import build


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.dirname(
        os.path.abspath(__file__)
    )
    path = os.path.join(out_dir, "entry.png")
    build(path)
    print("%s %d bytes" % (path, os.path.getsize(path)))


if __name__ == "__main__":
    main()
