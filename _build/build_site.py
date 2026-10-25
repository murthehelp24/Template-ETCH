"""Put together the website in dist/ — wrangler.jsonc runs this before every Cloudflare deploy; you can run it too.

    python3 _build/build_site.py

Copies only what the site needs: builder/, preview/ (without kit.json) and _build/site/ (index page, _headers,
robots.txt). Template sources, READMEs and _build/ stay out of the site. Uses the committed preview files —
run build_preview.py (or build_all.py) and commit before deploying."""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIST = os.path.join(ROOT, "dist")
NEEDED = ["builder/index.html", "builder/builder.js", "builder/builder.css", "builder/kit-data.js",
          "preview/page.html", "preview/assets/frame.js", "preview/assets/acss-sim.css"]
SKIP = {"kit.json"}  # every payload in one file — the builder does not use it


def main():
    missing = [p for p in NEEDED if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        sys.exit(f"missing {missing} — run python3 _build/build_preview.py first")
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    for folder in ("builder", "preview"):
        shutil.copytree(os.path.join(ROOT, folder), os.path.join(DIST, folder),
                        ignore=lambda d, names: [n for n in names if n in SKIP or n.startswith(".")])
    for name in os.listdir(os.path.join(HERE, "site")):
        shutil.copy(os.path.join(HERE, "site", name), os.path.join(DIST, name))
    files = sum(len(f) for _, _, f in os.walk(DIST))
    size = sum(os.path.getsize(os.path.join(d, n)) for d, _, f in os.walk(DIST) for n in f)
    print(f"ok site: {DIST} · {files} files · {size // 1024} KB")


if __name__ == "__main__":
    main()
