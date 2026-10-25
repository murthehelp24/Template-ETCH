"""Small helpers to write Etch copy payloads (gutenberg block JSON)."""
import base64, json, re
from datetime import datetime, timezone


def _inner(children):
    if not children:
        return "\n\n", ["\n", "\n"]
    return ("\n" + "\n\n" * (len(children) - 1) + "\n",
            ["\n"] + sum([[None, "\n\n"] for _ in children], [])[:-1] + ["\n"])


def block(name, attrs, children=None):
    children = children or []
    html, content = _inner(children)
    return {"blockName": name, "attrs": attrs, "innerBlocks": children, "innerHTML": html, "innerContent": content}


def el(name, tag, attrs=None, styles=None, children=None):
    a = {"metadata": {"name": name}, "tag": tag, "attributes": attrs or {}}
    if styles:
        a["styles"] = styles
    return block("etch/element", a, children)


def text(content):
    b = block("etch/text", {"metadata": {"name": "Text"}, "content": content})
    b["innerHTML"], b["innerContent"] = "", []
    return b


def img(name, attrs, styles):
    return block("etch/dynamic-image", {"metadata": {"name": name}, "tag": "img", "attributes": attrs, "styles": styles})


def svg(name, uri, cls=None, styles=None):
    attrs = {"aria-hidden": "true", "focusable": "false", "src": uri}
    if cls:
        attrs = {"class": cls, **attrs}
    a = {"metadata": {"name": name}, "tag": "svg", "attributes": attrs}
    if styles:
        a["styles"] = styles
    return block("etch/svg", a)


def cond(name, expr, children):
    return block("etch/condition", {"metadata": {"name": name},
                                    "condition": {"leftHand": expr, "operator": "isTruthy", "rightHand": None},
                                    "conditionString": expr}, children if isinstance(children, list) else [children])


def loop(name, item, children, loop_id=None, target=None, params=None):
    a = {"metadata": {"name": name}, "itemId": item}
    if loop_id:
        a["loopId"] = loop_id
    if target:
        a["target"] = target
    if params:
        a["loopParams"] = params
    return block("etch/loop", a, children)


def slot_placeholder(name):
    b = block("etch/slot-placeholder", {"name": name})
    return b


_REM = re.compile(r"(?<![\w.-])(\d*\.?\d+)rem\b")


def portable(css):
    """Lengths are written for 1rem = 10px. Etch's to-rem() converts px with each site's own root font size
    (62.5% or 100%), so the templates keep the same size on every site."""
    return _REM.sub(lambda m: f"to-rem({float(m.group(1)) * 10:g}px)", css)


def style(sel, css, typ="class"):
    return {"type": typ, "selector": sel, "collection": "default", "css": portable(css)}


def prop(name, key, default, desc="", primitive="string"):
    p = {"name": name, "key": key, "keyTouched": True, "type": {"primitive": primitive}, "default": default}
    if desc:
        p["description"] = desc
    return p


def data_uri(svg_markup):
    return "data:image/svg+xml;base64," + base64.b64encode(svg_markup.encode()).decode()


def payload(gblock, styles, components=None, loops=None):
    used = set()

    def walk(b):
        used.update(b.get("attrs", {}).get("styles") or [])
        for c in b.get("innerBlocks", []):
            walk(c)
    walk(gblock)
    for c in (components or {}).values():
        for b in c["blocks"]:
            walk(b)
    missing = used - set(styles)
    assert not missing, missing
    p = {"type": "block", "gutenbergBlock": gblock,
         "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
         "styles": styles}
    if loops:
        p["loops"] = loops
    if components:
        p["components"] = components
    p["version"] = 2.1
    return p


def write(path, p):
    open(path, "w").write(json.dumps(p, ensure_ascii=False, separators=(",", ":")))
