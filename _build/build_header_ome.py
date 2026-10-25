"""Build a paste-ready Etch header (main-header) on Oh My Etch navigation components."""
import base64, json, sys
from datetime import datetime, timezone
from kit import COLORS

S, OUT = sys.argv[1], sys.argv[2]
orig = json.load(open(f"{S}/original-copy.json"))      # old header copy (script, phone icon, etch base styles)
ome = json.load(open(f"{S}/ome-copy.json"))            # Oh My Etch components + their styles
ome_all = {s["id"]: s for s in json.load(open(f"{S}/ome.json"))["styles"]}

NAV, LIST, ITEM, TRIGGER, CONTENT, MOBILE = 1843, 1844, 1845, 1846, 1847, 1849
MENU_ID = "main-menu"

# ---------------------------------------------------------------- CSS
THEME_CSS = """/* Colours come from the main colours (:where(:root)) — change them there.
     Declared on :root because the mobile drawer is moved to <body> when it opens. */
  --main-header-logo-height: 40px;

  @media (width <= 768px) {
    --main-header-logo-height: 32px;
  }"""

ROOT_CSS = """pointer-events: none;
  z-index: 50;
  padding: 0;

  > * {
    pointer-events: auto;
  }

  /* position (data attributes on this element) */
  &[data-overlay-header='true'],
  &[data-sticky-header='true'] {
    inset-block-start: var(--wp-admin--admin-bar--height, 0px);
  }

  &[data-overlay-header='true'] {
    position: absolute;
  }

  &[data-sticky-header='true'] {
    position: sticky;
  }

  &[data-sticky-header='true'][data-overlay-header='true'] {
    position: fixed;
  }

  &[data-overlay-header='true'][data-overlay-header-offset='true'] + main > :first-child > :first-child {
    margin-block-start: var(--header-height);
  }

  &[data-hide-on-scroll='true'] .main-header__bar {
    transition: transform 0.4s cubic-bezier(0.55, 0, 0.1, 1);
  }

  &.hide .main-header__bar {
    transform: translateY(-100%);
  }

  /* ACSS gives every <button> outside a <nav> button typography — keep menu buttons like links */
  button.main-header__link {
    font-weight: inherit;
    font-family: inherit;
    line-height: inherit;
    letter-spacing: inherit;
    text-transform: none;
  }

  .skip-link {
    position: absolute;
    top: -1500px;
    left: 32px;
    z-index: 999;
    background: var(--main-light);
    color: var(--main-text);

    &:focus-visible {
      top: 32px;
    }
  }"""

BAR_CSS = """inline-size: 100%;
  padding: var(--space-xs) var(--gutter);
  background-color: var(--main-primary);
  color: var(--main-on-primary);
  border-block-end: 1px solid var(--main-line-on-primary);"""

CONTAINER_CSS = """flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-m);

  /* desktop nav (Oh My Etch root) fills the middle so the links sit centred.
     Styled from here: Etch drops class-prop ids on paste for the Nav's styling group. */
  > [data-ome-nav-menu-root] {
    flex: 1 1 auto;

    @media (width <= 1199px) {
      display: none;
    }
  }

  @media (width >= 1200px) {
    > [data-ome-mobile-nav-root] {
      display: none;
    }
  }"""

LOGO_CSS = """display: flex;
  flex-shrink: 0;"""

LOGO_IMG_CSS = """block-size: var(--main-header-logo-height);
  inline-size: auto;
  max-inline-size: 100%;
  object-fit: contain;"""


NAV_LIST_CSS = """justify-content: center;
  align-items: center;
  gap: var(--space-xs);"""

LINK_CSS = """position: relative;
  display: inline-flex;
  align-items: center;
  gap: 0.25em;
  padding: var(--btn-padding-block, 0.75em) var(--btn-padding-inline, 1em);
  background: none;
  border: 0;
  font: inherit;
  font-size: var(--text-s);
  line-height: 1;
  white-space: nowrap;
  color: var(--main-on-primary);
  text-decoration: none;
  cursor: pointer;

  /* animated underline */
  &::after {
    content: '';
    position: absolute;
    inset-inline: var(--btn-padding-inline, 1em);
    inset-block-end: 0.35em;
    block-size: 2px;
    background-color: var(--main-accent);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.25s ease;
  }

  &:hover::after,
  &[aria-current='page']::after,
  &[aria-expanded='true']::after {
    transform: scaleX(1);
  }

  [data-ome-nav-menu-trigger-chevron] {
    transition: rotate 0.2s ease;
  }

  &[aria-expanded='true'] [data-ome-nav-menu-trigger-chevron] {
    rotate: 180deg;
  }"""

DROPDOWN_CSS = """display: flex;
  flex-direction: column;
  min-inline-size: 220px;
  padding-block: var(--space-xs);
  background-color: var(--main-primary);
  border-block-start: 3px solid var(--main-accent);
  box-shadow: 0 16px 36px var(--main-shadow);
  transition: opacity 0.15s ease, translate 0.15s ease;

  &[data-ome-state='closed'] {
    opacity: 0;
    translate: 0 8px;
  }"""

DROPDOWN_LINK_CSS = """display: block;
  padding: 0.6em 1.25em;
  font-size: var(--text-s);
  line-height: 1.3;
  white-space: nowrap;
  color: var(--main-on-primary);
  text-decoration: none;
  transition: background-color 0.15s ease;

  &:not(:last-child) {
    box-shadow: inset 0 -1px 0 var(--main-line-on-primary);
  }

  &:hover,
  &:focus-visible {
    background-color: var(--main-accent);
  }

  &:focus-visible {
    outline: 2px solid var(--main-on-primary);
    outline-offset: -2px;
  }"""

ACTIONS_CSS = """display: flex;
  align-items: center;
  gap: var(--space-xs);
  flex-shrink: 0;

  /* tablet: keep the buttons next to the hamburger */
  @media (width <= 1199px) {
    margin-inline-start: auto;
  }

  @media (width <= 768px) {
    display: none;
  }"""

# ----- mobile (OmeNavigationMenuMobile) — own classes replace the plugin's *-default ones
BURGER_CSS = """display: inline-flex;
  align-items: center;
  justify-content: center;
  min-inline-size: 44px;
  min-block-size: 44px;
  padding: 0;
  background: none;
  border: 0;
  color: var(--main-on-primary);
  cursor: pointer;

  svg {
    inline-size: 28px;
    block-size: 28px;
  }"""

DRAWER_CSS = """--ome-drawer-overlay-color: color-mix(in srgb, var(--main-text) 60%, transparent);
  --ome-drawer-animation-duration: 250ms;
  inline-size: min(360px, 85vw);
  padding-block-start: var(--wp-admin--admin-bar--height, 0px);
  background-color: var(--main-primary);
  color: var(--main-on-primary);
  border-block-start: 3px solid var(--main-accent);

  /* ACSS gives every <button> outside a <nav> button typography — keep menu buttons like links */
  .main-header__mobile-link,
  .main-header__drawer-button {
    font-weight: inherit;
    font-family: inherit;
    line-height: inherit;
    letter-spacing: inherit;
    text-transform: none;
  }"""

DRAWER_CONTENT_CSS = """--_min-width: 100%;
  --_min-height: 100dvh;
  --_background: var(--main-primary);
  --_color: var(--main-on-primary);
  --_panel-background: var(--main-primary);"""

DRAWER_HEAD_CSS = """display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--gutter);
  border-block-end: 1px solid var(--main-line-on-primary);"""

DRAWER_BUTTON_CSS = """display: inline-flex;
  align-items: center;
  gap: 0.375em;
  min-inline-size: 44px;
  min-block-size: 44px;
  margin-inline-start: auto;
  padding: 0;
  background: none;
  border: 0;
  font: inherit;
  color: inherit;
  cursor: pointer;

  &[data-ome-mobile-nav-back] {
    margin-inline-start: 0;
  }"""

# Used in the bar and in the drawer (which lives in <body>). A custom style, because a
# class record on the element would drop its ACSS btn--* classes on paste.
PHONE_CSS = """display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-xs);
  white-space: nowrap;

  svg {
    inline-size: 1em;
    block-size: 1em;
    flex: 0 0 auto;
  }"""

MLIST_CSS = """display: grid;
  padding-inline: var(--gutter);"""

MITEM_CSS = """display: flex;
  align-items: stretch;
  border-block-end: 1px solid var(--main-line-on-primary);"""

MLINK_CSS = """display: flex;
  align-items: center;
  justify-content: space-between;
  inline-size: 100%;
  min-block-size: 48px;
  padding-block: var(--space-xs);
  padding-inline: 0;
  background: none;
  border: 0;
  font: inherit;
  text-align: start;
  color: var(--main-on-primary);
  text-decoration: none;
  cursor: pointer;

  &:hover,
  &:focus-visible {
    color: var(--main-accent);
  }"""

NEXT_ICON_CSS = """display: inline-flex;
  inline-size: 1em;
  block-size: 1em;
  flex-shrink: 0;"""

MSLOT_CSS = """display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  padding: var(--space-m) var(--gutter);"""


def style(sel, css, typ="class"):
    return {"type": typ, "selector": sel, "collection": "default", "css": css}


ostyles = orig["styles"]
styles = {
    "etch-section-style": ostyles["etch-section-style"],
    "etch-container-style": ostyles["etch-container-style"],
    **COLORS,
    "mh-theme": style(":root:has(.main-header)", THEME_CSS, "custom"),
    "mh-root": style(".main-header", ROOT_CSS),
    "mh-bar": style(".main-header__bar", BAR_CSS),
    "mh-container": style(".main-header__container", CONTAINER_CSS),
    "mh-logo": style(".main-header__logo", LOGO_CSS),
    "mh-logo-img": style(".main-header__logo-img", LOGO_IMG_CSS),
    "mh-nav-list": style(".main-header__nav-list", NAV_LIST_CSS),
    "mh-link": style(".main-header__link", LINK_CSS),
    "mh-dropdown": style(".main-header__dropdown", DROPDOWN_CSS),
    "mh-dropdown-link": style(".main-header__dropdown-link", DROPDOWN_LINK_CSS),
    "mh-actions": style(".main-header__actions", ACTIONS_CSS),
    "mh-burger": style(".main-header__burger", BURGER_CSS),
    "mh-drawer": style(".main-header__drawer", DRAWER_CSS),
    "mh-drawer-content": style(".main-header__drawer-content", DRAWER_CONTENT_CSS),
    "mh-drawer-head": style(".main-header__drawer-head", DRAWER_HEAD_CSS),
    "mh-drawer-button": style(".main-header__drawer-button", DRAWER_BUTTON_CSS),
    "mh-phone": style("a.main-header__phone", PHONE_CSS, "custom"),
    "mh-mlist": style(".main-header__mobile-list", MLIST_CSS),
    "mh-mitem": style(".main-header__mobile-item", MITEM_CSS),
    "mh-mlink": style(".main-header__mobile-link", MLINK_CSS),
    "mh-next-icon": style(".main-header__next-icon", NEXT_ICON_CSS),
    "mh-mslot": style(".main-header__mobile-slot", MSLOT_CSS),
}
# Oh My Etch records (reused if the target already has them; base customs carry the behaviour CSS)
for sid, s in ome["styles"].items():
    if s["selector"].startswith(".probe"):
        continue
    styles[sid] = {k: s[k] for k in ("type", "selector", "collection", "css")}
for sid in ("ome-drawer__host", "ome-drawer__page"):          # runtime host, not linked to any block
    s = ome_all[sid]
    styles[sid] = {k: s[k] for k in ("type", "selector", "collection", "css")}

# ---------------------------------------------------------------- blocks


def el(name, tag, attrs=None, style_ids=None, children=None, script=None):
    a = {"metadata": {"name": name}, "tag": tag, "attributes": attrs or {}}
    if style_ids:
        a["styles"] = style_ids
    if script:
        a["script"] = script
    children = children or []
    return {"blockName": "etch/element", "attrs": a, "innerBlocks": children,
            "innerHTML": "\n" + "\n\n" * max(len(children) - 1, 0) + "\n",
            "innerContent": ["\n"] + sum([[None, "\n\n"] for _ in children], [])[:-1] + ["\n"] if children else ["\n", "\n"]}


def text(content):
    return {"blockName": "etch/text", "attrs": {"metadata": {"name": "Text"}, "content": content},
            "innerBlocks": [], "innerHTML": "", "innerContent": []}


def slot(name, children):
    return {"blockName": "etch/slot-content", "attrs": {"name": name}, "innerBlocks": children,
            "innerHTML": "\n" + "\n\n" * max(len(children) - 1, 0) + "\n",
            "innerContent": ["\n"] + sum([[None, "\n\n"] for _ in children], [])[:-1] + ["\n"]}


def comp(ref, name, attributes=None, slots=None):
    """attributes: {group: {key: value}} — Etch stores each group prop as a JSON string."""
    def norm(group):
        return {k: " ".join(v) if isinstance(v, list) else v for k, v in group.items()}
    attrs = {k: json.dumps(norm(v), ensure_ascii=False) if isinstance(v, dict) else v
             for k, v in (attributes or {}).items()}
    children = slots or []
    return {"blockName": "etch/component", "attrs": {"ref": ref, "metadata": {"name": name}, "attributes": attrs},
            "innerBlocks": children, "innerHTML": "\n\n",
            "innerContent": ["\n", None, "\n"] if children else ["\n", "\n"]}


def nav_link(label, href):
    return comp(ITEM, label, {}, [slot("default", [
        el("Link", "a", {"href": href, "class": "main-header__link"}, ["mh-link"], [text(label)])])])


def nav_dropdown(label, content_id, links):
    return comp(ITEM, label, {}, [slot("default", [
        comp(TRIGGER, "Trigger", {
            "identity": {"contentId": content_id},
            "settings": {"showArrow": True, "triggerAction": "hover"},
            "styling": {"class": ["ome-nav-menu-default__trigger", "mh-link"]},
        }, [slot("default", [text(label)])]),
        comp(CONTENT, "Dropdown", {
            "identity": {"contentId": content_id},
            "styling": {"class": ["mh-dropdown"]},
        }, [slot("default", [
            el("Link", "a", {"href": h, "class": "main-header__dropdown-link"}, ["mh-dropdown-link"], [text(l)])
            for l, h in links])]),
    ])])


og = orig["gutenbergBlock"]
js = base64.b64decode(og["attrs"]["script"]["code"]).decode()
js = js.replace("'.header-wrapper'", "'.main-header'").replace("(.header-wrapper)", "(.main-header)")
js = js.replace("if (config.skipLink) {", "if (config.skipLink && !header.querySelector('.skip-link')) {")
assert ".header-wrapper" not in js and "querySelector('.skip-link')" in js
script = {"code": base64.b64encode(js.encode()).decode(), "id": "mainheader"}

phone_icon = og["innerBlocks"][0]["innerBlocks"][0]["innerBlocks"][2]["innerBlocks"][1]["innerBlocks"][0]


def buttons():
    return [
        el("CTA", "a", {"href": "https://line.me/R/ti/p/@example", "target": "_blank", "rel": "noopener", "class": "btn--secondary"}, None,
           [text("Chat on LINE")]),
        el("Phone", "a", {"href": "tel:+6620000000", "class": "main-header__phone btn--secondary btn--outline"}, None,
           [phone_icon, el("Number", "span", {}, None, [text("02-000-0000")])]),
    ]


nav = comp(NAV, "Nav", {
    "identity": {"menuId": MENU_ID},
    "accessibility": {"navAriaLabel": "Main"},
}, [slot("default", [
    comp(LIST, "Nav List", {"styling": {"class": ["mh-nav-list"]}}, [slot("default", [
        nav_link("Home", "/"),
        nav_link("About", "/about/"),
        nav_dropdown("Services", "main-menu-services", [
            ("Service 1", "/services/service-1/"),
            ("Service 2", "/services/service-2/"),
            ("Service 3", "/services/service-3/"),
        ]),
        nav_link("Blog", "/blog/"),
        nav_link("Contact", "/contact/"),
    ])]),
])])

mobile = comp(MOBILE, "Mobile Menu", {
    "identity": {"menuId": MENU_ID},
    "settings": {"drawerDirection": "right", "dismissible": True},
    "content": {"showTriggerLabel": False, "triggerAriaLabel": "Open menu", "backButtonLabel": "Back"},
    "rootStyling": {"class": []},
    "controlStyling": {"triggerClass": ["mh-burger"], "backButtonClass": ["mh-drawer-button"],
                       "closeButtonClass": ["mh-drawer-button"]},
    "drawerStyling": {"drawerClass": ["mh-drawer"], "headerClass": ["mh-drawer-head"],
                      "contentClass": ["mh-drawer-content"]},
    "menuStyling": {"listClass": ["mh-mlist"], "itemClass": ["mh-mitem"], "linkClass": ["mh-mlink"],
                    "submenuTriggerClass": ["mh-mlink"], "nextIconClass": ["mh-next-icon"]},
    "slotStyling": {"beforeClass": [], "afterClass": ["mh-mslot"]},
}, [slot("after", buttons())])

header = el("Main Header", "header", {
    "data-etch-element": "section",
    "data-overlay-header": "false",
    "data-overlay-header-offset": "false",
    "data-sticky-header": "true",
    "data-hide-on-scroll": "true",
    "data-hide-at": "200px",
    "data-show-on-scroll-up": "true",
    "data-skip-link": "true",
    "class": "main-header",
}, ["etch-section-style", "mh-root"], [
    el("Bar", "div", {"class": "main-header__bar"}, ["mh-bar"], [
        el("Container", "div", {"data-etch-element": "container", "class": "main-header__container"},
           ["etch-container-style", "mh-container"], [
               el("Logo", "a", {"href": "/", "aria-label": "Home", "class": "main-header__logo"}, ["mh-logo"], [
                   {"blockName": "etch/dynamic-image",
                    "attrs": {"metadata": {"name": "Logo Image"}, "tag": "img",
                              "attributes": {"class": "main-header__logo-img", "mediaId": ""},
                              "styles": ["mh-logo-img"]},
                    "innerBlocks": [], "innerHTML": "\n\n", "innerContent": ["\n", "\n"]},
               ]),
               nav,
               el("Actions", "div", {"class": "main-header__actions"}, ["mh-actions"], buttons()),
               mobile,
           ])
    ])
], script)

payload = {
    "type": "block",
    "gutenbergBlock": header,
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    "styles": styles,
    "components": ome["comps"],
    "version": 2.1,
}

used = set()
def walk(b):
    used.update(b.get("attrs", {}).get("styles") or [])
    for c in b.get("innerBlocks", []):
        walk(c)
walk(header)
for c in ome["comps"].values():
    for b in c["blocks"]:
        walk(b)
assert not (used - set(styles)), used - set(styles)

open(OUT, "w").write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
print("ok", OUT, len(styles), "styles", len(ome["comps"]), "components")
