"""Build the header variants from the Oh My Etch header (etch-header/site-header-ohmyetch.etch.txt).

Each variant is the same header plus one modifier class (main-header--<name>) whose style overrides the look, and,
where the layout needs it, a few changed blocks. The shared main-header__* styles stay identical, so several
variants can be pasted into one site (Etch keeps the first copy of a selector) and the audit stays happy.

    python3 build_header_variants.py <src> <kit>/etch-header
"""
import copy, json, os, sys
from datetime import datetime, timezone
from kit import icon
from lib_etch import el, style, svg, text

S, OUT = sys.argv[1], sys.argv[2]
BASE = json.load(open(os.path.join(OUT, "site-header-ohmyetch.etch.txt"), encoding="utf-8"))

# ---------------------------------------------------------------- CSS (one class style per variant)
LIGHT_CSS = """/* light bar: dark text on the light colour, primary buttons */
  .main-header__bar {
    background-color: var(--main-light);
    color: var(--main-text);
    border-block-end-color: var(--main-line);
    box-shadow: 0 2px 12px var(--main-shadow);
  }

  .main-header__link,
  .main-header__burger {
    color: var(--main-text);
  }

  .main-header__link::after {
    background-color: var(--main-primary);
  }

  .main-header__dropdown {
    background-color: var(--main-light);
    border-block-start-color: var(--main-primary);
  }

  .main-header__dropdown-link {
    color: var(--main-text);

    &:not(:last-child) {
      box-shadow: inset 0 -1px 0 var(--main-line);
    }

    &:hover,
    &:focus-visible {
      background-color: var(--main-light-alt);
      color: var(--main-primary);
    }

    &:focus-visible {
      outline-color: var(--main-primary);
    }
  }"""

CENTER_CSS = """/* desktop: logo centred on the first row, buttons on its right, menu centred on the row below */
  @media (width >= 1200px) {
    --main-header-logo-height: 52px;

    .main-header__container {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      row-gap: var(--space-xs);
    }

    .main-header__logo {
      grid-column: 2;
      grid-row: 1;
      justify-self: center;
    }

    .main-header__actions {
      grid-column: 3;
      grid-row: 1;
      justify-self: end;
    }

    .main-header__container > [data-ome-nav-menu-root] {
      grid-column: 1 / -1;
      grid-row: 2;
      padding-block-start: var(--space-xs);
      border-block-start: 1px solid var(--main-line-on-primary);
    }
  }"""

TOPBAR_CSS = """/* a thin info strip above the bar (inside it, so hide-on-scroll moves both) */
  .main-header__topbar {
    margin-block: calc(var(--space-xs) * -1) var(--space-xs);
    margin-inline: calc(var(--gutter) * -1);
    padding: 0.5em var(--gutter);
    background-color: var(--main-light-alt);
    color: var(--main-text);
    font-size: var(--text-xs, var(--text-s));
    line-height: 1.4;
  }

  .main-header__topbar-inner {
    display: flex;
    inline-size: 100%;
    max-inline-size: var(--content-width, 1366px);
    margin-inline: auto;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.25em var(--space-m);
  }

  .main-header__topbar-group {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.25em var(--space-m);
  }

  .main-header__topbar-item {
    display: inline-flex;
    align-items: center;
    gap: 0.5em;
    color: inherit;
    text-decoration: none;

    svg {
      inline-size: 1.1em;
      block-size: 1.1em;
      flex: 0 0 auto;
      color: var(--main-primary);
    }
  }

  a.main-header__topbar-item:hover {
    color: var(--main-primary);
    text-decoration: underline;
  }

  /* phones: the hours and phone only */
  @media (width <= 768px) {
    .main-header__topbar-inner {
      justify-content: center;
    }

    .main-header__topbar-group--extra,
    .main-header__topbar-item--address {
      display: none;
    }
  }"""

FLOATING_CSS = """/* the bar floats: a rounded, shadowed band with space around it; round buttons to match */
  .main-header__bar {
    background-color: transparent;
    border-block-end: 0;
    padding-block: var(--space-s);
  }

  .main-header__container {
    padding: var(--space-xs) var(--space-xs) var(--space-xs) var(--space-l);
    background-color: var(--main-primary);
    border-radius: 999px;
    box-shadow: 0 10px 30px var(--main-shadow);

    @media (width <= 768px) {
      padding-inline: var(--space-m) var(--space-xs);
    }
  }

  .main-header__actions > a {
    border-radius: 999px;
  }"""

RIGHT_CSS = """/* menu next to a single button on the right */
  .main-header__bar {
    padding-block: var(--space-s);
  }

  .main-header__nav-list {
    justify-content: flex-end;
  }"""

VARIANTS = [
    # name, file, label (block name), css
    ("light", "site-header-ohmyetch-light.etch.txt", "Main Header (Light)", LIGHT_CSS),
    ("center", "site-header-ohmyetch-center.etch.txt", "Main Header (Centred Logo)", CENTER_CSS),
    ("topbar", "site-header-ohmyetch-topbar.etch.txt", "Main Header (Top Bar)", TOPBAR_CSS),
    ("floating", "site-header-ohmyetch-floating.etch.txt", "Main Header (Floating)", FLOATING_CSS),
    ("right", "site-header-ohmyetch-right.etch.txt", "Main Header (Menu Right)", RIGHT_CSS),
]


def find(block, name):
    if block.get("attrs", {}).get("metadata", {}).get("name") == name:
        return block
    for c in block.get("innerBlocks", []):
        hit = find(c, name)
        if hit:
            return hit
    return None


def set_children(block, children):
    block["innerBlocks"] = children
    block["innerHTML"] = "\n" + "\n\n" * max(len(children) - 1, 0) + "\n"
    block["innerContent"] = (["\n"] + sum([[None, "\n\n"] for _ in children], [])[:-1] + ["\n"]) if children \
        else ["\n", "\n"]


def topbar_item(name, icon_name, label, href=None, extra=""):
    cls = "main-header__topbar-item" + (" main-header__topbar-item--" + extra if extra else "")
    attrs = {"class": cls, **({"href": href} if href else {})}
    return el(name, "a" if href else "span", attrs, None,
              [svg("Icon", icon(icon_name)), el("Label", "span", {}, None, [text(label)])])


def topbar():
    return el("Top Bar", "div", {"class": "main-header__topbar"}, None, [
        el("Top Bar Inner", "div", {"class": "main-header__topbar-inner"}, None, [
               el("Info", "div", {"class": "main-header__topbar-group"}, None, [
                   topbar_item("Address", "address", "123 Example Road, Bangkok", extra="address"),
                   topbar_item("Hours", "hours", "Mon–Sat 09:00–18:00"),
                   topbar_item("Phone", "phone", "02-000-0000", "tel:+6620000000"),
               ]),
               el("Links", "div", {"class": "main-header__topbar-group main-header__topbar-group--extra"}, None, [
                   topbar_item("Email", "email", "hello@example.com", "mailto:hello@example.com"),
                   topbar_item("LINE", "line", "@example", "https://line.me/R/ti/p/@example"),
               ]),
           ]),
    ])


def build(name, label, css):
    p = copy.deepcopy(BASE)
    header = p["gutenbergBlock"]
    a = header["attrs"]
    a["metadata"]["name"] = label
    a["attributes"]["class"] = "main-header main-header--" + name
    a["styles"] = a["styles"] + ["mh-v-" + name]
    p["styles"]["mh-v-" + name] = style(".main-header--" + name, css)

    actions = find(header, "Actions")
    cta, phone = actions["innerBlocks"]
    if name == "light":  # on a light bar the primary buttons stand out (secondary is meant for the dark bar)
        cta["attrs"]["attributes"]["class"] = "btn--primary"
        phone["attrs"]["attributes"]["class"] = "main-header__phone btn--primary btn--outline"
    if name == "right":  # one call to action keeps the right side light next to the menu
        set_children(actions, [cta])
    if name == "topbar":
        bar = find(header, "Bar")
        set_children(bar, [topbar()] + bar["innerBlocks"])

    p["timestamp"] = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return p


for name, fname, label, css in VARIANTS:
    p = build(name, label, css)
    path = os.path.join(OUT, fname)
    open(path, "w").write(json.dumps(p, ensure_ascii=False, separators=(",", ":")))
    print("ok", path)
