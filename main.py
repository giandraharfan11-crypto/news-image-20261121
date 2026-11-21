#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261121 bounty.

The picture of the day is drawn by generate.py (kept in this repository as
the image's source) and stored beside this file as entry.png. This program
copies those exact bytes to the grader's output file, /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png when that variable is set, as it is for
local runs). It uses only the Python standard library, needs no network,
and writes the same bytes on every run.
"""

import os
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    data = source.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("entry.png beside main.py is not a PNG file")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    dest.write_bytes(data)
    if dest.read_bytes() != data:
        raise SystemExit("written entry.png does not match the source bytes")
    print(f"wrote {dest} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
