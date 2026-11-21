"""Entry point: draw the front page for Saturday 21 November 2026.

Run: python3 main.py
Writes entry.png (1024x1024, deterministic) next to this file.
"""

import os

from build_image import build


def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build(path)
    print("%s %d bytes" % (path, os.path.getsize(path)))


if __name__ == "__main__":
    main()
