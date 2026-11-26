#!/usr/bin/env python3
"""news-image-20261126 entrypoint: copy the shipped entry.png to the
output directory. Stdlib only; resolves the image from this file's own
directory, never from the working directory.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png missing next to main.py")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy is incomplete")
    print(f"copied entry.png ({os.path.getsize(dst)} bytes) to {dst}")


if __name__ == "__main__":
    main()
