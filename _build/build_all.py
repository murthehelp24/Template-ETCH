"""Rebuild every template into the kit folders, then run the audit.

    python3 _build/build_all.py
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "src")
JOBS = [
    ("build_header_ome.py", "etch-header/site-header-ohmyetch.etch.txt"),
    ("build_header_variants.py", "etch-header"),  # reads the file above
    ("build_header_menubuilder.py", "etch-header/site-header.etch.txt"),
    ("build_footer.py", "etch-footer/main-footer.etch.txt"),
    ("build_footer_variants.py", "etch-footer"),  # reads the file above
    ("build_sections.py", "etch-sections"),
    ("build_sections_more.py", "etch-sections"),
    ("build_hero_more.py", "etch-sections"),
    ("build_features_more.py", "etch-sections"),
]
for script, out in JOBS:
    if not os.path.exists(os.path.join(HERE, script)):
        continue
    subprocess.run([sys.executable, os.path.join(HERE, script), SRC, os.path.join(ROOT, out)], cwd=HERE, check=True)
subprocess.run([sys.executable, os.path.join(HERE, "audit.py")], cwd=ROOT, check=True)
subprocess.run([sys.executable, os.path.join(HERE, "build_preview.py")], cwd=ROOT, check=True)
