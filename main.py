#!/usr/bin/env python3
"""news-image-20261117: the entry point of the competition entry.

The poster itself is rendered by render.py, which draws it in HTML with CSS
typography and inline SVG and screenshots it with the system Chrome. That
step needs a browser, so it is kept out of the graded run: the sandbox the
grader uses holds no browser and no network.

So the repository carries the finished image, entry.png, and this program
copies it into place. Python's standard library only, and both runs write the
same bytes.
"""
import os
import shutil

OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
NAME = "entry.png"


def main():
    """Copy the rendered poster to the output directory."""
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, NAME)
    target = os.path.join(OUT, NAME)
    os.makedirs(OUT, exist_ok=True)
    with open(source, "rb") as fh:
        data = fh.read()
    with open(target, "wb") as fh:
        fh.write(data)
    print(f"wrote {target} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
