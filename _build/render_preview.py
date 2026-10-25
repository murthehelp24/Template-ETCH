"""Render an Etch copy payload (.etch.txt) to static HTML + CSS for the preview / page builder.

The preview is made from the built .etch.txt file itself — the exact JSON that is pasted into Etch — so what the
builder shows is what Etch gets. Only the frontend render is simulated: components with props + slots, conditions,
loops (sample posts), dynamic images (placeholders) and the WordPress blocks used by the kit.

    from render_preview import render
    body_html, css, scripts = render(payload)

Editable spots are marked for the page builder (it writes the edits back into the copied .etch.txt):
  data-pv-edit="t:<path>"            literal text of an etch/text block
  data-pv-edit="p:<path>:<prop>"     text that shows one prop of a kit component (saved on that instance)
  data-pv-img="i:<path>"             an empty dynamic image (preview only — Etch takes images from Media Library)
<path> is the block's position in the payload: "g.0.2" = gutenbergBlock.innerBlocks[0].innerBlocks[2],
"c.<id>.1.0" = components[<id>].blocks[1].innerBlocks[0].
"""
import base64, copy, html, json, re
from urllib.parse import unquote

# ================================================================ sample data for dynamic content
SITE = {"name": "Your Brand", "currentDate": "2026"}
PAGE = {"id": 1, "title": "About us", "excerpt": "A short page excerpt that introduces what this page is about.",
        "date": "2026-10-25", "permalink": {"full": "https://example.com/about/", "relative": "/about/"},
        "image": {"id": 1}, "categories": [{"name": "News"}]}
POSTS = [
    {"title": t, "excerpt": e, "image": {"id": i + 1}, "categories": [{"name": c}],
     "permalink": {"relative": f"/blog/post-{i + 1}/", "full": f"https://example.com/blog/post-{i + 1}/"}}
    for i, (t, e, c) in enumerate([
        ("How to choose the right service for your home", "A practical checklist to compare options, prices and "
         "what to ask before you book.", "Guides"),
        ("5 things to prepare before your first visit", "Bring these documents and questions so the first "
         "appointment goes smoothly.", "Tips"),
        ("What our customers ask most often", "Answers to the questions we hear every week, in one place.", "News"),
        ("Behind the scenes: a day with our team", "Meet the people who take care of every project from start "
         "to finish.", "Team"),
        ("Pricing explained in plain language", "What is included, what costs extra and how we keep quotes "
         "transparent.", "Guides"),
        ("New opening hours from next month", "We are open longer on weekdays — here is the new schedule.", "News"),
    ])]
LOOPS = {"mainQuery": POSTS, "mainRelatedPosts": POSTS[:3]}
POST_CONTENT = """<p>This is sample article content so you can see how the post body looks. Real posts come from the
WordPress editor (<code>core/post-content</code>).</p>
<h2>A heading inside the article</h2>
<p>Paragraphs use the body text size and a comfortable line height. <a href="#">Links use the theme colour</a>.</p>
<ul><li>First point in a list</li><li>Second point with a little more text to wrap</li><li>Third point</li></ul>
<blockquote><p>A short quote from a customer or an expert.</p></blockquote>
<p>Closing paragraph with a call to action.</p>"""

# neutral photo placeholder (transparent background so the template's own box colour shows through)
PHOTO = ("data:image/svg+xml;utf8," + re.sub(r"\s+", " ", """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 300'
 preserveAspectRatio='xMidYMid slice'><rect width='400' height='300' fill='%23b8bfc9' fill-opacity='.35'/>
 <circle cx='290' cy='95' r='34' fill='%23ffffff' fill-opacity='.6'/>
 <path d='M0 300 L120 150 L200 240 L260 180 L400 300 Z' fill='%23778293' fill-opacity='.45'/></svg>""")).replace("#", "%23")
LOGO = ("data:image/svg+xml;utf8," + re.sub(r"\s+", " ", """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 160 40'>
 <rect x='1' y='1' width='158' height='38' rx='8' fill='none' stroke='%23999' stroke-width='2' stroke-dasharray='5 4'/>
 <text x='80' y='26' text-anchor='middle' font-family='sans-serif' font-size='16' font-weight='700'
 fill='%23999'>LOGO</text></svg>"""))

VOID = {"img", "br", "hr", "input", "meta", "link", "source", "area", "col", "embed", "wbr", "path", "line",
        "circle", "rect", "polyline", "polygon", "ellipse", "use", "stop"}
SVG_VOID = {"path", "line", "circle", "rect", "polyline", "polygon", "ellipse", "use", "stop"}


# ================================================================ tiny expression evaluator (Etch dynamic data)
_TOK = re.compile(r"""\s*(?:(?P<num>\d+(?:\.\d+)?)|(?P<str>"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|"""
                  r"""(?P<op>===|!==|==|!=|&&|\|\||\?\?|[!().,])|(?P<id>[A-Za-z_$][\w$]*))""")


class _Method:
    def __init__(self, obj, name):
        self.obj, self.name = obj, name


def _tokens(src):
    pos, out = 0, []
    while pos < len(src):
        if src[pos:].strip() == "":
            break
        m = _TOK.match(src, pos)
        if not m:
            raise ValueError(f"cannot parse expression: {src!r}")
        pos = m.end()
        kind = m.lastgroup
        out.append((kind, m.group(kind)))
    return out


def evaluate(src, ctx):
    toks, i = _tokens(src), 0

    def peek():
        return toks[i] if i < len(toks) else (None, None)

    def take():
        nonlocal i
        i += 1
        return toks[i - 1]

    def expr():
        return orr()

    def orr():
        v = andd()
        while peek()[1] in ("||", "??"):
            op = take()[1]
            r = andd()
            v = (v or r) if op == "||" else (r if v is None else v)
        return v

    def andd():
        v = cmp()
        while peek()[1] == "&&":
            take()
            r = cmp()
            v = v and r
        return v

    def cmp():
        v = unary()
        if peek()[1] in ("===", "==", "!==", "!="):
            op = take()[1]
            r = unary()
            return (v == r) if op in ("===", "==") else (v != r)
        return v

    def unary():
        if peek()[1] == "!":
            take()
            return not truthy(unary())
        return primary()

    def primary():
        kind, val = take()
        if val == "(":
            v = expr()
            take()
            return v
        if kind == "num":
            return float(val) if "." in val else int(val)
        if kind == "str":
            return val[1:-1].encode().decode("unicode_escape")
        if val in ("true", "false", "null", "undefined"):
            return {"true": True, "false": False}.get(val)
        v = ctx.get(val)
        while peek()[1] in (".", "("):
            if take()[1] == ".":
                key = take()[1]
                v = _get(v, key)
            else:
                args = []
                while peek()[1] != ")":
                    args.append(expr())
                    if peek()[1] == ",":
                        take()
                take()
                v = _call(v, args)
        return v

    return expr()


def _get(v, key):
    if isinstance(v, dict):
        return v.get(key)
    if key in ("dateFormat",):
        return _Method(v, key)
    return None


def _call(m, args):
    if isinstance(m, _Method) and m.name == "dateFormat":
        fmt = args[0] if args else ""
        return "2026" if fmt == "Y" else "25 October 2026"
    return None


def truthy(v):
    return bool(v) and v != "false"


def tostr(v):
    if v is None:
        return ""
    if v is True or v is False:
        return "true" if v else "false"
    if isinstance(v, list):
        return " ".join(tostr(x) for x in v)
    if isinstance(v, dict):
        return json.dumps(v)
    return str(v)


def _braces(s):
    """Yield (start, end) of top-level {...} groups (handles nested braces and quoted strings)."""
    i, n = 0, len(s)
    while i < n:
        if s[i] == "{":
            depth, j, q = 0, i, None
            while j < n:
                c = s[j]
                if q:
                    if c == "\\":
                        j += 1
                    elif c == q:
                        q = None
                elif c in "\"'":
                    q = c
                elif c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        yield i, j + 1
                        break
                j += 1
            i = j + 1
        else:
            i += 1


def _expr_value(inner, ctx):
    inner = inner.strip()
    if inner.startswith("{"):
        try:
            return json.loads(inner)
        except ValueError:
            pass
    try:
        return evaluate(inner, ctx)
    except (ValueError, IndexError, TypeError):
        return None


def value(s, ctx):
    """Typed value of an attribute/prop string: '{expr}' → value, '{"json": 1}' → dict, else interpolated text."""
    if not isinstance(s, str):
        return s
    st = s.strip()
    if st.startswith("[") and st.endswith("]"):
        try:
            return json.loads(st)
        except ValueError:
            pass
    if st.startswith("{") and st.endswith("}"):
        try:
            return json.loads(st)
        except ValueError:
            spans = list(_braces(st))
            if spans == [(0, len(st))]:
                return _expr_value(st[1:-1], ctx)
    return interpolate(s, ctx)


def interpolate(s, ctx, esc=None):
    out, last = [], 0
    for a, b in _braces(s):
        out.append(s[last:a])
        inner = s[a + 1:b - 1]
        if not re.match(r"\s*[A-Za-z_$!(\"']", inner):
            out.append(s[a:b])
        else:
            v = tostr(_expr_value(inner, ctx))
            out.append(esc(v) if esc else v)
        last = b
    out.append(s[last:])
    return "".join(out)


# ================================================================ renderer
EDITABLE_COMPONENT = re.compile(r"^Main")  # the kit's own components; library ones (menus) stay as shipped
PROP_TEXT = re.compile(r"^\{props\.(\w+)\}\s*$")


def _number(block, path):
    block["_path"] = path
    for i, kid in enumerate(block.get("innerBlocks") or []):
        _number(kid, f"{path}.{i}")


class Renderer:
    def __init__(self, payload):
        self.p = payload = copy.deepcopy(payload)  # paths are added to a copy, never to the payload itself
        _number(payload["gutenbergBlock"], "g")
        for cid, comp in (payload.get("components") or {}).items():
            for i, b in enumerate(comp.get("blocks") or []):
                _number(b, f"c.{cid}.{i}")
        self.styles = payload.get("styles") or {}
        self.components = {str(c["id"]): c for c in (payload.get("components") or {}).values()}
        self.id_class = {}
        for sid, s in self.styles.items():
            m = re.fullmatch(r"\.([\w-]+)", s["selector"].strip())
            if m:
                self.id_class[sid] = m.group(1)
        self.scripts = {}

    # ---------------------------------------------------------------- helpers
    def classes(self, v):
        """Class props hold style ids (Etch converts them to class names); plain class names pass through."""
        toks = v if isinstance(v, list) else tostr(v).split()
        out = []
        for t in toks:
            for c in tostr(t).split():
                c = self.id_class.get(c, c)
                if c and c not in out:
                    out.append(c)
        return " ".join(out)

    def class_tokens(self, v, ctx):
        """'a {props.cls}' → ['a', ...prop value]; class props are arrays of style ids or space-separated ids."""
        if not isinstance(v, str):
            return v if isinstance(v, list) else [v]
        out, last = [], 0
        for a, b in _braces(v):
            out += v[last:a].split()
            val = _expr_value(v[a + 1:b - 1], ctx)
            if isinstance(val, str) and val.strip().startswith("["):
                val = value(val, ctx)
            out += val if isinstance(val, list) else tostr(val).split()
            last = b
        return out + v[last:].split()

    def attrs(self, attrs, ctx, tag):
        out = []
        for k, v in (attrs or {}).items():
            if k in ("mediaId",):
                continue
            if k == "class":
                val = self.classes(self.class_tokens(v, ctx))
                if not val:
                    continue
            else:
                raw = value(v, ctx) if isinstance(v, str) else v
                if raw is None:
                    continue
                val = tostr(raw)
            out.append(f" {k}" if val == "" and k == "hidden" else f' {k}="{html.escape(val, quote=True)}"')
        return "".join(out)

    def script(self, a):
        sc = a.get("script")
        if not sc or not sc.get("code"):
            return
        code = base64.b64decode(sc["code"]).decode("utf-8", "replace")
        if not code.strip() or "/wp-content/" in code:
            return  # plugin assets (Oh My Etch) are not available offline — see frame.js for the preview shim
        self.scripts.setdefault(sc.get("id") or str(len(self.scripts)), code)

    # ---------------------------------------------------------------- editable spots
    def edit_key(self, b, ctx):
        """Key of an editable etch/text block, or None (dynamic text, markup, library components)."""
        if b.get("blockName") != "etch/text":
            return None
        content = (b.get("attrs") or {}).get("content", "")
        path = b.get("_path", "")
        in_kit = path.startswith("g") or EDITABLE_COMPONENT.match(ctx.get("__comp__") or "")
        if not in_kit:
            return None
        if "{" not in content and "<" not in content and content.strip():
            return "t:" + path
        m = PROP_TEXT.match(content)
        if m and ctx.get("__inst__") and EDITABLE_COMPONENT.match(ctx.get("__comp__") or ""):
            return f"p:{ctx['__inst__']}:{m.group(1)}"
        return None

    # ---------------------------------------------------------------- blocks
    def blocks(self, blocks, ctx):
        return "".join(self.block(b, ctx) for b in blocks)

    def block(self, b, ctx):
        name, a = b["blockName"], b.get("attrs") or {}
        kids = b.get("innerBlocks") or []
        if name in ("etch/element", "etch/dynamic-element"):
            self.script(a)
            tag = tostr(value(a.get("tag") or "div", ctx)) or "div"
            key = self.edit_key(kids[0], ctx) if len(kids) == 1 else None
            if key:  # element holding just this text: mark the element itself, no extra wrapper
                inner = interpolate(kids[0]["attrs"].get("content", ""), ctx, html.escape)
                return self.element(tag, {**(a.get("attributes") or {}), "data-pv-edit": key}, inner, ctx)
            return self.element(tag, a.get("attributes"), self.blocks(kids, ctx), ctx)
        if name == "etch/text":
            out = interpolate(a.get("content", ""), ctx, html.escape)
            key = self.edit_key(b, ctx)
            return f'<span data-pv-edit="{key}">{out}</span>' if key else out
        if name == "etch/raw-html":
            return interpolate(a.get("content", ""), ctx)
        if name == "etch/svg":
            return self.svg(a, ctx)
        if name == "etch/dynamic-image":
            return self.image(b, a, ctx)
        if name == "etch/condition":
            return self.blocks(kids, ctx) if truthy(_expr_value(a.get("conditionString", ""), ctx)) else ""
        if name == "etch/loop":
            return self.loop(a, kids, ctx)
        if name == "etch/component":
            return self.component(b, a, kids, ctx)
        if name == "etch/slot-placeholder":
            slots = ctx.get("__slots__") or {}
            slot = slots.get(a.get("name") or "default") or slots.get("")
            if not slot:
                return ""
            blocks, slot_ctx = slot
            return self.blocks(blocks, slot_ctx)
        if name == "etch/slot-content":
            return self.blocks(kids, ctx)
        if name == "core/query":
            return self.blocks(kids, ctx)
        if name == "core/query-pagination":
            return f'<nav class="wp-block-query-pagination" aria-label="Pagination">{self.blocks(kids, ctx)}</nav>'
        if name == "core/query-pagination-previous":
            return ""  # page 1: WordPress prints no "previous" link
        if name == "core/query-pagination-numbers":
            return ('<div class="wp-block-query-pagination-numbers"><span aria-current="page" '
                    'class="page-numbers current">1</span><a class="page-numbers" href="#">2</a>'
                    '<a class="page-numbers" href="#">3</a></div>')
        if name == "core/query-pagination-next":
            return '<a href="#" class="wp-block-query-pagination-next">Next Page →</a>'
        if name == "core/post-content":
            return f'<div class="entry-content wp-block-post-content">{POST_CONTENT}</div>'
        return f"<!-- unsupported block {name} -->" + self.blocks(kids, ctx)

    def element(self, tag, attrs, inner, ctx):
        if tag in VOID and not inner:
            end = " />" if tag in SVG_VOID else ">"
            return f"<{tag}{self.attrs(attrs, ctx, tag)}{end}"
        return f"<{tag}{self.attrs(attrs, ctx, tag)}>{inner}</{tag}>"

    def svg(self, a, ctx):
        attrs = dict(a.get("attributes") or {})
        src = attrs.pop("src", "")
        markup = ""
        if src.startswith("data:image/svg+xml;base64,"):
            markup = base64.b64decode(src.split(",", 1)[1]).decode("utf-8", "replace")
        elif src.startswith("data:image/svg+xml"):
            markup = unquote(src.split(",", 1)[1])
        if "<svg" not in markup:
            return f"<svg{self.attrs(attrs, ctx, 'svg')}></svg>"
        markup = re.sub(r"<\?xml[^>]*>|<!--.*?-->", "", markup, flags=re.S).strip()
        # merge the block's attributes into the root <svg> (Etch inlines the file the same way)
        m = re.match(r"<svg\b([^>]*)>", markup)
        root = m.group(1)
        for k in attrs:
            root = re.sub(rf'\s{re.escape(k)}="[^"]*"', "", root)
        return f"<svg{root}{self.attrs(attrs, ctx, 'svg')}>" + markup[m.end():]

    def image(self, b, a, ctx):
        attrs = dict(a.get("attributes") or {})
        cls = tostr(attrs.get("class", ""))
        if "{" not in tostr(attrs.get("mediaId", "")):  # fixed image slot (not a post's featured image)
            attrs["data-pv-img"] = "i:" + b.get("_path", "")
        attrs["src"] = LOGO if "logo" in cls else PHOTO
        attrs.setdefault("alt", "")
        return self.element("img", attrs, "", ctx)

    def loop(self, a, kids, ctx):
        if a.get("loopId"):
            items = LOOPS.get(a["loopId"], POSTS[:3])
        else:
            items = _expr_value(a.get("target", ""), ctx) or []
        out = []
        for it in items:
            c = dict(ctx)
            c[a.get("itemId") or "item"] = it
            out.append(self.blocks(kids, c))
        return "".join(out)

    # ---------------------------------------------------------------- components
    def defaults(self, props):
        d = {}
        for p in props or []:
            t = p.get("type") or {}
            if t.get("primitive") == "object" or t.get("specialized") == "condition" and p.get("properties"):
                sub = self.defaults(p.get("properties"))
                if t.get("specialized") == "condition":
                    d.update(sub)  # conditional groups only toggle UI; their props live on the parent group
                else:
                    d[p["key"]] = sub
            elif t.get("specialized") == "condition":
                continue
            else:
                d[p["key"]] = p.get("default")
        return d

    def component(self, b, a, kids, ctx):
        comp = self.components.get(str(a.get("ref")))
        if not comp:
            return f"<!-- missing component {a.get('ref')} -->"
        props = self.defaults(comp.get("properties"))
        for k, v in (a.get("attributes") or {}).items():
            v = value(v, ctx)
            if isinstance(props.get(k), dict) and isinstance(v, dict):
                props[k] = {**props[k], **v}
            else:
                props[k] = v
        # default values may themselves be expressions ('{false}')
        props = {k: (value(v, ctx) if isinstance(v, str) and v.startswith("{") else v) for k, v in props.items()}
        slots = {}
        loose = []
        for k in kids:
            if k["blockName"] == "etch/slot-content":
                # an unnamed slot-content fills whichever slot the component has
                slots[(k.get("attrs") or {}).get("name") or ""] = (k.get("innerBlocks") or [], ctx)
            else:
                loose.append(k)
        if loose and "" not in slots:
            slots[""] = (loose, ctx)
        c = {"site": SITE, "this": PAGE, "environment": {"current": "frontend"}, "props": props,
             "__inst__": b.get("_path"), "__comp__": comp.get("key", ""),
             "slots": {n: {"empty": not s[0]} for n, s in slots.items()}, "__slots__": slots}
        # slots that the instance did not fill are empty
        c["slots"] = _SlotView(c["slots"])
        return self.blocks(comp.get("blocks") or [], c)

    # ---------------------------------------------------------------- whole payload
    def render(self):
        ctx = {"site": SITE, "this": PAGE, "environment": {"current": "frontend"}, "props": {},
               "slots": _SlotView({}), "__slots__": {}}
        body = self.block(self.p["gutenbergBlock"], ctx)
        return body, compile_css(self.styles), list(self.scripts.values())


class _SlotView(dict):
    def get(self, k, d=None):
        return super().get(k, {"empty": True})


_TO_REM = re.compile(r"to-rem\(\s*(-?[\d.]+)px\s*\)")


def compile_css(styles):
    """Etch style records → CSS. to-rem(Npx) keeps N px on any root font size, like Etch does per site."""
    out = []
    for s in styles.values():
        css = _TO_REM.sub(lambda m: f"calc({m.group(1)} * 1rem / var(--etch-root-px, 10))", s["css"])
        out.append(f"{s['selector']} {{\n  {css}\n}}")
    return "\n\n".join(out)


def render(payload):
    return Renderer(payload).render()
