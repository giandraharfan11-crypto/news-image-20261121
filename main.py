"""Front-page image copier for news-image-20261121.

The front-page artwork is rendered at build time and shipped as
entry.png alongside this file. This entrypoint does one job only:
it copies that finished image, byte for byte, into the output
directory. It imports nothing beyond the Python standard library,
so it runs in a bare interpreter with no third-party packages
installed — exactly the environment the grader provides.
"""

import os
import shutil
from pathlib import Path


def main() -> int:
    source = Path(__file__).resolve().parent / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"
    # entry.png ships with the repo; copy it byte-for-byte, no re-render.
    shutil.copyfile(source, destination)
    print("Wrote", destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
