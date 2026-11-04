"""Fixtures for tests/audit.test.ts: template files that break every audit rule, and what _build/audit.py prints
for them.

    python3 packages/kit/tests/fixtures/make_audit_fixtures.py

Writes audit/etch-*/... (the bad files) and audit/expected.json ({stdout, code}) by running the real audit.py in
that folder. private-terms.txt lists one client name to check that rule too."""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..", "..")
sys.path.insert(0, os.path.join(ROOT, "_build"))
from lib_etch import el, text, style  # noqa: E402
from kit import COLORS  # noqa: E402

OUT = os.path.join(HERE, "audit")
shutil.rmtree(OUT, ignore_errors=True)


def payload(block, styles, components=None, loops=None, **extra):
    p = {"type": "block", "gutenbergBlock": block, "timestamp": "2026-01-01T00:00:00.000Z", "styles": styles}
    if loops:
        p["loops"] = loops
    if components:
        p["components"] = components
    p.update(extra)
    p["version"] = 2.1
    return p


def write(path, p):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(json.dumps(p, ensure_ascii=False, separators=(",", ":")))


box = el("Box", "div", {"class": "main-x"}, ["mn-x"])
comp = lambda blocks: {"990001": {"key": "SharedKey", "blocks": blocks, "properties": []}}
# 1. the same selector / component key / loop key with different content in two files
write("etch-a/one.etch.txt", payload(box, {**COLORS, "mn-x": style(".main-x", "gap: 1rem;")},
                                     comp([el("A", "div")]), {"loopA": {"key": "loopA", "config": {"n": 1}}}))
write("etch-a/two.etch.txt", payload(box, {**COLORS, "mn-x": style(".main-x", "gap: 2rem;")},
                                     comp([el("B", "div")]), {"loopA": {"key": "loopA", "config": {"n": 2}}}))
# 2. no colour variables; hard-coded colours, raw rem and ACSS colours in kit styles (comments, white-space and
#    library styles are left alone)
write("etch-b/colours.etch.txt", payload(el("Box", "div", {}, ["mn-y"]), {
    "mn-y": {"type": "class", "selector": ".main-y", "collection": "default",
             "css": "/* #000 white */ color: #fff; background: rgba(0,0,0,.5); border-color: white;\n"
                    "  white-space: nowrap; margin: 2rem; padding: var(--primary); gap: var(--space-m);\n"
                    "  outline-color: hsl(0 0% 0%); fill: var(--text-dark-trans); x: var(--primary-l);"},
    "ome-lib": {"type": "class", "selector": ".ome-x", "collection": "default", "css": "color: #fff;"},
    "sh-lib": {"type": "custom", "selector": ".main-z:where(.site-header *)", "collection": "default",
               "css": "color: #fff;"},
}))
# 3. a style id that is not in the file, a class that would be lost on paste, customMediaDefinitions
write("etch-b/missing.etch.txt", payload(el("Root", "div", {}, None, [
    el("Uses Missing", "div", {}, ["mn-nope"]),
    el("Loses Class", "div", {"class": "main-a extra-one {props.cls} extra-two"}, ["mn-a"], [text("x")]),
]), {**COLORS, "mn-a": style(".main-a", "")}, customMediaDefinitions={"x": 1}))
# 4. leftovers of the source sites: uploads, a real phone number, a client name from private-terms.txt
write("etch-b/leftovers.etch.txt", payload(el("Box", "div", {}, None, [
    text("wp-content/uploads/2020/05/photo.jpg wp-content/uploads/2026/01/menu-1.svg"),
    text("call 081-234-5678 or 02-000-0000 — ACME Clinic"),
]), dict(COLORS)))
os.makedirs(os.path.join(OUT, "_build"), exist_ok=True)
open(os.path.join(OUT, "_build", "private-terms.txt"), "w").write("# client names\nACME Clinic\n\n")

run = subprocess.run([sys.executable, os.path.join(ROOT, "_build", "audit.py")], cwd=OUT, capture_output=True,
                     text=True)
json.dump({"stdout": run.stdout, "code": run.returncode}, open(os.path.join(OUT, "expected.json"), "w"),
          ensure_ascii=False, indent=1)
print(run.stdout)
