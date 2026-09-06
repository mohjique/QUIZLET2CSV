#!/usr/bin/env python3
"""Converts icon.png into icon.ico for the Windows build.

Invoked by build_windows.bat so icon.png stays the single source of truth
for both the macOS (.icns) and Windows (.ico) app icons.
"""

import sys
from PIL import Image


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "icon.png"
    dst = sys.argv[2] if len(sys.argv) > 2 else "icon.ico"

    img = Image.open(src).convert("RGBA")
    sizes = [(16, 16), (32, 32), (48, 48), (128, 128), (256, 256)]
    img.save(dst, sizes=sizes)
    print(f"Wrote {dst}")


if __name__ == "__main__":
    main()
