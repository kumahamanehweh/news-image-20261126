#!/usr/bin/env python3
"""Copy the shipped front-page image to the grader's output directory.

Stdlib only. The image lives beside this file in the repository, so it is
resolved from this file's own directory and never from the working
directory. Both grader runs therefore write identical bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "./out")
DST = os.path.join(OUT_DIR, "entry.png")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
if os.path.getsize(SRC) != os.path.getsize(DST):
    raise SystemExit("entry.png copy size mismatch")
print(f"wrote {DST} ({os.path.getsize(DST)} bytes)")
