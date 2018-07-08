import os
import subprocess
import re

# This script converts SVG images into PNG because browsers can't display SVGs reliably.
# Requires Python 3, Inkscape and pngquant.

for svg_name in os.listdir():
    base, ext = os.path.splitext(svg_name)
    if ext == ".svg":
        png_name = "{0}.png".format(base)
        if not os.path.exists(png_name) or os.path.getmtime(svg_name) > os.path.getmtime(png_name):
            print(svg_name)
            subprocess.run(["inkscape", "-z", "-e", png_name, "-d", "192", svg_name])
            subprocess.run(["pngquant", "--ext", ".png", "--force", "--skip-if-larger", "--strip", png_name])
