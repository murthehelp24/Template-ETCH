"""Build the footer variants from the Main Footer (etch-footer/main-footer.etch.txt).

Each variant is its own component (MainFooterLight, MainFooterCenter …) whose root carries one modifier class
(main-footer--<name>) holding that look; the shared main-footer__* styles stay identical, so the audit passes and
several footers can live on one site. Layouts that need it also change blocks (drop a column, add a map).

    python3 build_footer_variants.py <src> <kit>/etch-footer
"""
import copy, json, os, sys
from datetime import datetime, timezone
from lib_etch import el, text, cond, style, prop

S, OUT = sys.argv[1], sys.argv[2]
BASE = json.load(open(os.path.join(OUT, "main-footer.etch.txt"), encoding="utf-8"))
BASE_ID = next(iter(BASE["components"]))

LIGHT_CSS = """/* light footer: dark text on the light colour */
  &.main-footer {
    --main-social-color: var(--main-primary);
    background-color: var(--main-light-alt);
    color: var(--main-text);
  }

  .main-footer__title {
    color: var(--main-primary);
  }

  .main-footer__text {
    color: var(--main-text-muted);
  }

  .main-footer__bottom {
    border-block-start-color: var(--main-line);
    color: var(--main-text-muted);
  }"""

CENTER_CSS = """/* one centred column: logo, menu in a row, contact, social */
  .main-footer__grid {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-m);
    text-align: center;
  }

  .main-footer__col {
    align-items: center;
  }

  .main-footer__brand {
    max-inline-size: 56rem;
  }

  .main-footer__list {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: var(--space-xs) var(--space-l);
  }

  .main-social {
    justify-content: center;
  }"""

MAP_CSS = """/* the services column becomes a Google map */
  .main-footer__grid {
    grid-template-columns: 1.6fr 1fr 1.2fr 1.6fr;

    @media (width <= 992px) {
      grid-template-columns: repeat(2, 1fr);
    }

    @media (width <= 768px) {
      grid-template-columns: 1fr;
    }
  }

  .main-footer__map {
    display: block;
    inline-size: 100%;
    block-size: 100%;
    min-block-size: 24rem;
    border: 0;
    border-radius: var(--radius-m);
  }"""

COMPACT_CSS = """/* one row: logo, menu, social — roomy, with a larger logo and links */
  &.main-footer {
    --main-footer-logo-width: 18rem;
    padding-block-start: var(--section-space-m);
  }

  .main-footer__link {
    font-size: var(--text-m);
  }

  .main-footer__grid {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-l);
    padding-block-end: var(--space-l);

    @media (width <= 768px) {
      flex-direction: column;
      text-align: center;
    }
  }

  .main-footer__brand {
    max-inline-size: none;
  }

  .main-footer__list {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: var(--space-xs) var(--space-l);
  }

  .main-footer__bottom {
    margin-block-start: var(--space-m);
    padding-block: var(--space-s);
  }"""

VARIANTS = [
    # name, component id (fixed, so a rebuilt file keeps it), key, label, css
    ("light", 990002, "MainFooterLight", "Main Footer (Light)", LIGHT_CSS),
    ("center", 990003, "MainFooterCenter", "Main Footer (Centred)", CENTER_CSS),
    ("map", 990005, "MainFooterMap", "Main Footer (Map)", MAP_CSS),
    ("compact", 990006, "MainFooterCompact", "Main Footer (Compact)", COMPACT_CSS),
]


def find(blocks, name):
    for b in blocks:
        if b.get("attrs", {}).get("metadata", {}).get("name") == name:
            return b
        hit = find(b.get("innerBlocks", []), name)
        if hit:
            return hit
    return None


def set_children(block, children):
    block["innerBlocks"] = children
    block["innerHTML"] = "\n" + "\n\n" * max(len(children) - 1, 0) + "\n"
    block["innerContent"] = (["\n"] + sum([[None, "\n\n"] for _ in children], [])[:-1] + ["\n"]) if children \
        else ["\n", "\n"]


def drop(parent, *names):
    set_children(parent, [b for b in parent["innerBlocks"]
                          if b.get("attrs", {}).get("metadata", {}).get("name") not in names])


def build(name, new_id, key, label, css):
    p = copy.deepcopy(BASE)
    comp = p["components"].pop(BASE_ID)
    comp.update({"id": new_id, "key": key, "name": label,
                 "description": comp["description"] + " Variant: " + label.split("(")[1].rstrip(")") + "."})
    blocks = comp["blocks"]
    root = blocks[0]
    root["attrs"]["attributes"]["class"] = "main-footer main-footer--" + name
    root["attrs"]["styles"] = root["attrs"]["styles"] + ["mf-v-" + name]
    p["styles"]["mf-v-" + name] = style(".main-footer--" + name, css)
    grid = find(blocks, "Grid")

    if name == "center":
        drop(grid, "Services")
        drop(find(blocks, "Menu"), "Title")
        drop(find(blocks, "Contact"), "Title")
    if name == "map":
        services = find(blocks, "Services")
        idx = grid["innerBlocks"].index(services)
        grid["innerBlocks"].pop(idx)
        grid["innerBlocks"].append(el("Map Column", "div", {"class": "main-footer__col"}, ["mf-col"], [
            cond("If map embed", "props.mapEmbedUrl", el("Map", "iframe", {
                "class": "main-footer__map", "src": "{props.mapEmbedUrl}", "title": "Map", "loading": "lazy",
                "referrerpolicy": "no-referrer-when-downgrade"}))]))
        set_children(grid, grid["innerBlocks"])
        at = next(n for n, pr in enumerate(comp["properties"]) if pr["key"] == "mapLabel") + 1
        comp["properties"].insert(at, prop("Map Embed URL", "mapEmbedUrl",
                                           "https://www.google.com/maps?q=Bangkok&output=embed",
                                           "Google Maps → Share → Embed a map → copy the src. Empty = no map"))
    if name == "compact":
        drop(grid, "Services")
        drop(find(blocks, "Brand"), "Description")
        drop(find(blocks, "Menu"), "Title")
        contact = find(blocks, "Contact")
        drop(contact, *[b["attrs"]["metadata"]["name"] for b in contact["innerBlocks"]
                        if b["attrs"]["metadata"]["name"] != "Social"])

    p["components"] = {str(new_id): comp}
    p["gutenbergBlock"]["attrs"]["ref"] = new_id
    p["timestamp"] = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return p


for name, new_id, key, label, css in VARIANTS:
    payload = build(name, new_id, key, label, css)
    path = os.path.join(OUT, f"main-footer-{name}.etch.txt")
    open(path, "w").write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    print("ok", path)
