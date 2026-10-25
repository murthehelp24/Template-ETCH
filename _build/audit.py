"""Check that all templates can live on one site together. Run from the kit root (build_all.py does this).

Fails on: the same selector with different CSS in two files, a component / loop key with different content,
a file without the shared colour variables, a hard-coded colour in a template-owned style, a style id used by a
block but missing from the file."""
import collections, glob, json, os, re, sys

files = sorted(glob.glob("etch-*/*.etch.txt"))
P = {f: json.load(open(f)) for f in files}
errors, warnings = [], []

# ---------------------------------------------------------------- 1. shared selectors / keys must be identical
sel, comp, loops = (collections.defaultdict(dict) for _ in range(3))
for f, p in P.items():
    for s in p["styles"].values():
        sel[(s["selector"], s["type"])][f] = s["css"]
    for c in (p.get("components") or {}).values():
        comp[c["key"]][f] = json.dumps({k: c[k] for k in ("blocks", "properties")}, sort_keys=True)
    for l in (p.get("loops") or {}).values():
        loops[l["key"]][f] = json.dumps(l["config"], sort_keys=True)
for what, table in (("selector", sel), ("component", comp), ("loop", loops)):
    for key, d in table.items():
        if len(set(d.values())) > 1:
            errors.append(f"{what} {key} differs between {sorted(d)}")

# ---------------------------------------------------------------- 2. colours only from the main colours
COLOR_LIT = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(|(?<![-\w])(?:white|black)(?![-\w])")
ACSS_COLOR = re.compile(r"var\(--(primary|secondary|accent|base|neutral|white|black|text-dark|text-light|bg-|shade)(?![\w-]*-(?:xs|s|m|l|xl)\b)[\w-]*")


def owned(sid, s):
    """Styles written for this kit (library CSS from Oh My Etch / Menu Builder is left as shipped)."""
    return sid == "main-colors" or (re.search(r"\.(main|site-header)[\w-]*", s["selector"])
                                     and ":where(.site-header *)" not in s["selector"])


for f, p in P.items():
    if "main-colors" not in p["styles"]:
        errors.append(f"{f}: missing main-colors")
    for sid, s in p["styles"].items():
        if sid == "main-colors" or not owned(sid, s):
            continue
        css = re.sub(r"/\*.*?\*/", "", s["css"], flags=re.S)
        css = re.sub(r"white-space:[^;]+;", "", css)
        for m in COLOR_LIT.finditer(css):
            errors.append(f"{f.split('/')[-1]} {s['selector']}: hard-coded colour '{m.group(0)}'")
        for m in re.finditer(r"(?<![\w.-])\d*\.?\d+rem\b", css):
            errors.append(f"{f.split('/')[-1]} {s['selector']}: raw '{m.group(0)}' — use to-rem(px) so it fits any root font size")
        for m in ACSS_COLOR.finditer(css):
            errors.append(f"{f.split('/')[-1]} {s['selector']}: ACSS colour '{m.group(0)})' — use --main-*")

# ---------------------------------------------------------------- 3. every style id used by a block exists
for f, p in P.items():
    used = set()

    def walk(b):
        used.update(b.get("attrs", {}).get("styles") or [])
        for c in b.get("innerBlocks", []):
            walk(c)
    walk(p["gutenbergBlock"])
    for c in (p.get("components") or {}).values():
        for b in c["blocks"]:
            walk(b)
    for sid in used - set(p["styles"]):
        errors.append(f"{f}: block uses missing style {sid}")

    # an element with a styles array only keeps the classes that have a style record
    def classes(b):
        a = b.get("attrs", {})
        if a.get("styles") and "class" in (a.get("attributes") or {}):
            have = {m for sid in a["styles"] if sid in p["styles"]
                    for m in re.findall(r"^\.([\w-]+)$", p["styles"][sid]["selector"])}
            lost = {c for c in a["attributes"]["class"].split() if "{" not in c} - have
            if lost:
                errors.append(f"{f}: '{(a.get('metadata') or {}).get('name')}' would lose class {sorted(lost)} on paste")
        for c in b.get("innerBlocks", []):
            classes(c)
    classes(p["gutenbergBlock"])
    for c in (p.get("components") or {}).values():
        for b in c["blocks"]:
            classes(b)
    if p.get("customMediaDefinitions"):
        warnings.append(f"{f}: has customMediaDefinitions (overwrites the target's)")

# ---------------------------------------------------------------- 4. leftovers from the source sites
# Uploads from the source sites and real phone numbers (the samples are 02-000-0000 / +6620000000).
# Client names are not written here: list them one per line in _build/private-terms.txt (git-ignored).
SAMPLE_PHONES = {"02-000-0000", "+6620000000"}
terms = [t.strip() for t in open("_build/private-terms.txt", encoding="utf-8")
         if t.strip() and not t.startswith("#")] if os.path.exists("_build/private-terms.txt") else []
LEFT = re.compile(r"wp-content/uploads/(?!2026/01/menu-1\.svg)|(?<![\w-])(?:\+66|0)\d{1,2}-\d{3}-\d{4}(?![\w-])"
                  + "".join("|" + re.escape(t) for t in terms), re.I)
for f in files + sorted(glob.glob("_build/src/*.json")):
    hits = set(m.group(0) for m in LEFT.finditer(open(f, encoding="utf-8").read())) - SAMPLE_PHONES
    if hits:
        warnings.append(f"{f}: source-site leftovers {sorted(hits)}")

for f, p in P.items():
    btn = sorted(set(re.findall(r"btn--[\w-]+", json.dumps(p["gutenbergBlock"]) +
                                json.dumps(p.get("components") or {}))))
    print(f"  {f}: {len(p['styles'])} styles, components={[c['key'] for c in (p.get('components') or {}).values()]}"
          f", loops={list(p.get('loops') or {})}, buttons={btn}")
for w in warnings:
    print("  warning:", w)
for e in errors:
    print("  ERROR:", e)
print(f"audit: {len(files)} files, {len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
