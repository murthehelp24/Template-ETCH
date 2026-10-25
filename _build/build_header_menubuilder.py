"""Build a generic, paste-ready Etch header (site-header) from the Win Win copy payload."""
import base64, json, re, sys
from datetime import datetime, timezone
from kit import COLORS

S = sys.argv[1]
OUT = sys.argv[2]
orig = json.load(open(f"{S}/original-copy.json"))
lib = json.load(open(f"{S}/lib-styles.json"))

# ---------------------------------------------------------------- CSS
ROOT_CSS = """/* Colours come from the main colours (:where(:root)) — change them there */
  --header-bg: var(--main-primary);
  --header-text: var(--main-on-primary);
  --header-accent: var(--main-accent);
  --header-border: var(--main-line-on-primary);
  --header-panel-bg: var(--main-primary);
  --header-logo-height: 40px;
  --ease-swift: cubic-bezier(0.55, 0, 0.1, 1);

  pointer-events: none;
  z-index: 50;
  padding: 0;

  > * {
    pointer-events: auto;
  }

  @media (width <= 768px) {
    --header-logo-height: 32px;
  }

  /* ===== POSITION (data attributes on this element) ===== */
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

  &[data-hide-on-scroll='true'] .site-header__bar {
    transition: transform 0.4s var(--ease-swift);
  }

  &.hide .site-header__bar {
    transform: translateY(-100%);
  }

  /* ===== HAMBURGER: only while the menu is in mobile mode ===== */
  #mobile-menu-toggle {
    display: none;
  }

  &:has(.menu-wrapper.mobile) :is(#mobile-menu-toggle, .toggle) {
    display: flex;
  }

  /* tablet: keep the buttons next to the hamburger */
  &:has(.menu-wrapper.mobile) .site-header__actions {
    margin-inline-start: auto;
  }

  .toggle {
    --toggle-icon-color: var(--header-text);
    color: var(--header-text);
  }

  /* ===== SKIP LINK (added by script) ===== */
  .skip-link {
    position: absolute;
    top: -1500px;
    left: 32px;
    z-index: 999;
    overflow: hidden;
    background: var(--main-light);
    color: var(--main-text);

    &:focus-visible {
      top: 32px;
    }
  }

  /* ===== MENU VARIABLES ===== */
  --link-color: var(--header-text);
  --link-color-hover: var(--header-text);
  --link-color-active: var(--header-accent);
  --link-bg-color: transparent;
  --link-bg-color-hover: transparent;
  --link-bg-color-active: transparent;
  --link-font-weight: var(--btn-font-weight);
  --link-transition: all 0.2s ease-out;
  --link-padding-inline: var(--btn-padding-inline, 1em);
  --link-padding-block: var(--btn-padding-block, 0.75em);
  --link-border-radius: var(--btn-border-radius);

  --dropdown-padding: calc(to-rem(5px) + 3px) 0 to-rem(5px);
  --dropdown-border-radius: 0;
  --dropdown-border-width: 0px;
  --dropdown-border-color: transparent;
  --dropdown-bg: linear-gradient(var(--header-accent), var(--header-accent)) top / 100% 3px no-repeat, var(--header-panel-bg);
  --dropdown-box-shadow: 0 16px 36px var(--main-shadow);
  --dropdown-closed-top: 30px;
  --dropdown-open-top: 22px;

  --mobile-menu-padding-inline: var(--gutter);
  --mobile-menu-padding-block: var(--space-m);
  --mobile-menu-bg-color: var(--header-panel-bg);
  --mobile-menu-width: 768px;
  --mobile-dropdown-stacked-timing: cubic-bezier(0.86, 0.01, 0.09, 1.01);

  /* ===== DROPDOWN ANIMATION ===== */
  .menu-dropdown .menu-dropdown__content-wrapper {
    filter: blur(4px);
  }

  .menu-dropdown.is-open > .menu-dropdown__content-wrapper {
    filter: blur(0);
  }

  .menu-wrapper.desktop .menu-dropdown .menu-dropdown__content-wrapper,
  .menu-wrapper.desktop .morph-container {
    scale: 0.95;
  }

  .menu-wrapper.desktop .menu-dropdown.is-open > .menu-dropdown__content-wrapper,
  .menu-wrapper.desktop .morph-container.is-active {
    scale: 1;
  }

  .menu-dropdown-back-button {
    font-weight: var(--link-font-weight);
    padding-block: 1em;
    padding-inline: var(--mobile-menu-padding-inline);
    color: var(--link-color);
    background-color: var(--mobile-menu-bg-color);
    border-block-end: 1px solid var(--header-border);
  }

  /* show desktop menu before the menu script initialises */
  .menu-wrapper.desktop:not([data-menu-initialized]) {
    @media (width >= 1200px) {
      opacity: 1;
    }
  }

  /* ===== DESKTOP MENU (centred between logo and buttons) ===== */
  .menu-wrapper.desktop {
    flex: 1 1 auto;

    .site-header__nav-list {
      justify-content: center;
    }

    .site-header__nav-list > li {
      inline-size: fit-content;
      white-space: nowrap;
    }

    .site-header__nav-list > li > *:is(a, button) {
      position: relative;
      padding-inline: var(--link-padding-inline);
      padding-block: var(--link-padding-block);
      border-radius: var(--link-border-radius);
      font-size: var(--text-s);
      line-height: 100%;
      color: var(--link-color);
      text-decoration: none;
      transition: var(--link-transition);

      /* animated underline */
      &::after {
        content: '';
        position: absolute;
        left: var(--link-padding-inline, 1em);
        right: var(--link-padding-inline, 1em);
        bottom: 0.35em;
        height: 2px;
        background-color: var(--header-accent);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.25s ease;
      }

      &:hover::after,
      &[aria-expanded='true']::after {
        transform: scaleX(1);
      }

      &.active-link {
        color: var(--link-color-active);
      }
    }

    .menu-dropdown__content {
      min-inline-size: 220px;
      gap: 0;
    }

    .menu-dropdown__content > li:not(:last-child) > a {
      box-shadow: inset 0 -1px 0 var(--header-border);
    }

    .menu-dropdown__content > li > a {
      display: block;
      padding: 0.6em 1.25em;
      font-size: var(--text-s);
      font-weight: 400;
      line-height: 1.3;
      color: var(--header-text);
      text-decoration: none;
      white-space: nowrap;
      transition: background-color 0.15s ease;

      &:hover,
      &:focus-visible {
        background-color: var(--header-accent);
        color: var(--header-text);
      }

      &:focus-visible {
        outline: 2px solid var(--header-text);
        outline-offset: -2px;
      }

      &[href='#'] {
        cursor: default;
      }
    }
  }

  /* ===== MOBILE MENU ===== */
  .menu-wrapper.mobile {
    .menu-wrapper__inner {
      display: flex;
      flex-direction: column;
      border-block-start: 3px solid var(--header-accent);
      color: var(--header-text);
    }

    .site-header__nav {
      flex: 1;
      position: relative;
      padding-inline: var(--mobile-menu-padding-inline);
      overflow-y: auto;
      overflow-x: clip;
    }

    .site-header__nav-list {
      flex-direction: column;
      justify-content: flex-start;
      flex-grow: 1;
      block-size: 100%;

      > li {
        inline-size: 100%;
        max-inline-size: 100%;
        border-block-end: 1px solid var(--header-border);

        > a,
        .menu-dropdown,
        .menu-dropdown__trigger {
          inline-size: 100%;
        }
      }
    }

    .site-header__nav-list > li > *:is(a, button),
    .menu-dropdown__content > li > *:is(a, button) {
      padding-block: var(--btn-padding-block);
      padding-inline: 0;
      line-height: 100%;
      color: var(--header-text);
      text-decoration: none;
      background-color: transparent;
      transition: var(--link-transition);

      &:hover,
      &[aria-expanded='true'] {
        color: var(--header-accent);
      }
    }

    .menu-dropdown__trigger {
      inline-size: 100%;
      justify-content: space-between;
    }

    .menu-dropdown__content-wrapper {
      background-color: transparent;
    }

    .menu-dropdown__content a {
      opacity: 0.8;
    }

    :where(& .menu-dropdown__content-wrapper.stacked-mode .menu-dropdown__content) {
      padding-block: var(--mobile-menu-padding-block);
      padding-inline: var(--mobile-menu-padding-inline);
    }

    :where(& .menu-dropdown.accordion-mode .menu-dropdown__content) {
      padding-inline: var(--space-xs);
    }

    :where(& .menu-dropdown.accordion-mode[data-mega-menu='true'] .menu-dropdown__content) {
      padding-block: var(--space-xs);
    }
  }"""

BAR_CSS = """inline-size: 100%;
  padding: var(--space-xs) var(--gutter);
  background-color: var(--header-bg);
  border-block-end: 1px solid var(--header-border);"""

CONTAINER_CSS = """flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-m);"""

LOGO_CSS = """display: flex;
  flex-shrink: 0;"""

LOGO_IMG_CSS = """block-size: var(--header-logo-height);
  inline-size: auto;
  max-inline-size: 100%;
  object-fit: contain;"""

ACTIONS_CSS = """display: flex;
  align-items: center;
  gap: var(--space-xs);
  flex-shrink: 0;

  @media (width <= 768px) {
    display: none;
  }

  /* phone button — no own style record so its ACSS btn classes survive the paste */
  .site-header__phone {
    display: inline-flex;
    align-items: center;
    gap: var(--space-xs);
    white-space: nowrap;

    svg {
      inline-size: 1em;
      block-size: 1em;
      flex: 0 0 auto;
    }
  }"""


NAV_LIST_CSS = """display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--space-xs);
  margin: 0;
  padding: 0;
  list-style: none;

  li {
    max-inline-size: 100%;
  }"""


def ren(css):
    css = css.replace(".nav__list", ".site-header__nav-list")
    return re.sub(r"\.nav(?![\w-])", ".site-header__nav", css)


def style(sel, css, typ="class"):
    return {"type": typ, "selector": sel, "collection": "default", "css": css}


ostyles = orig["styles"]
styles = {
    **COLORS,
    # Etch element base styles (reused if the target site has them)
    "etch-section-style": ostyles["etch-section-style"],
    "etch-container-style": ostyles["etch-container-style"],
    "etch-flex-div-style": ostyles["etch-flex-div-style"],
    # header block
    "sh-root": style(".site-header", ROOT_CSS),
    "sh-bar": style(".site-header__bar", BAR_CSS),
    "sh-container": style(".site-header__container", CONTAINER_CSS),
    "sh-logo": style(".site-header__logo", LOGO_CSS),
    "sh-logo-img": style(".site-header__logo-img", LOGO_IMG_CSS),
    "sh-actions": style(".site-header__actions", ACTIONS_CSS),
    # menu markup classes (library)
    "fy0647x": ostyles["fy0647x"],   # .mobile-menu-header
    "6liaugx": ostyles["6liaugx"],   # .hide-from-desktop-menu
    "sh-nav": style(".site-header__nav", ""),
    "sh-nav-list": style(".site-header__nav-list", NAV_LIST_CSS),
    "7s74zii": ostyles["7s74zii"],   # #menu-wrapper (used inside MenuWrapper)
}
# Menu library CSS (classes the menu/toggle scripts add at runtime). Etch's own copy
# misses these, and unlinked class styles are not always compiled on the frontend
# (the hamburger icon broke). Ship them as custom styles — always compiled — scoped
# with :where(.site-header *) so they never clash with the target site's own records.
for sid, s in lib.items():
    if not s["css"].strip() or s["type"] != "class":
        continue
    styles[f"sh-lib-{sid}"] = style(f"{s['selector']}:where(.site-header *)", ren(s["css"]), "custom")
for s in styles.values():
    s.pop("readonly", None)

# ---------------------------------------------------------------- blocks


def el(name, tag, attrs=None, style_ids=None, children=None, script=None):
    a = {"metadata": {"name": name}, "tag": tag, "attributes": attrs or {}}
    if style_ids:
        a["styles"] = style_ids
    if script:
        a["script"] = script
    children = children or []
    return {
        "blockName": "etch/element",
        "attrs": a,
        "innerBlocks": children,
        "innerHTML": "\n" + "\n\n" * max(len(children) - 1, 0) + "\n" if children else "\n\n",
        "innerContent": (["\n"] + sum([[None, "\n\n"] for _ in children], [])[:-1] + ["\n"]) if children else ["\n", "\n"],
    }


def text(content):
    return {"blockName": "etch/text", "attrs": {"metadata": {"name": "Text"}, "content": content},
            "innerBlocks": [], "innerHTML": "", "innerContent": []}


def component(ref, attributes, name=None, children=None):
    a = {"ref": ref, "attributes": attributes}
    if name:
        a["metadata"] = {"name": name}
    children = children or []
    return {"blockName": "etch/component", "attrs": a, "innerBlocks": children,
            "innerHTML": "\n\n",
            "innerContent": ["\n", None, "\n"] if children else ["\n", "\n"]}


def slot(name, children):
    return {"blockName": "etch/slot-content", "attrs": {"name": name}, "innerBlocks": children,
            "innerHTML": "\n" + "\n\n" * (len(children) - 1) + "\n",
            "innerContent": ["\n"] + sum([[None, "\n\n"] for _ in children], [])[:-1] + ["\n"]}


def link(label, url, name="Menu Link"):
    return component(1974, {"label": label, "linkUrl": url}, name)


g = orig["gutenbergBlock"]
bar0 = g["innerBlocks"][0]
cont0 = bar0["innerBlocks"][0]
menu0 = cont0["innerBlocks"][1]           # MenuWrapper instance
burger0 = cont0["innerBlocks"][3]         # ToggleButton instance
mobile_header0 = menu0["innerBlocks"][0]["innerBlocks"][0]

# header script: same behaviour, new root selector
js = base64.b64decode(g["attrs"]["script"]["code"]).decode()
js = js.replace("'.header-wrapper'", "'.site-header'").replace("(.header-wrapper)", "(.site-header)")
js = js.replace("if (config.skipLink) {", "if (config.skipLink && !header.querySelector('.skip-link')) {")
assert ".header-wrapper" not in js and "querySelector('.skip-link')" in js
script = {"code": base64.b64encode(js.encode()).decode(), "id": "siteheader"}

# mobile menu header (close button) — keep, generic label
close_toggle = json.loads(json.dumps(mobile_header0["innerBlocks"][0]))
close_toggle["attrs"]["attributes"]["ariaLabel"] = "Close menu"
mobile_header = el("Mobile Header", "div",
                   {"data-etch-element": "flex-div", "class": "mobile-menu-header hide-from-desktop-menu"},
                   ["etch-flex-div-style", "fy0647x", "6liaugx"], [close_toggle])

nav = el("Nav", "nav", {"data-menu-element": "nav", "class": "site-header__nav", "aria-label": "Main"}, ["sh-nav"], [
    el("Nav List", "ul", {"data-etch-element": "flex-div", "class": "site-header__nav-list"},
       ["etch-flex-div-style", "sh-nav-list"], [
           link("Home", "/"),
           link("About", "/about/"),
           component(1971, {"dropdownLabel": "Services"}, "Services Dropdown", [
               slot("dropdownContent", [
                   link("Service 1", "/services/service-1/"),
                   link("Service 2", "/services/service-2/"),
                   link("Service 3", "/services/service-3/"),
               ])
           ]),
           link("Blog", "/blog/"),
           link("Contact", "/contact/"),
       ])
])

menu = json.loads(json.dumps(menu0))
menu["attrs"]["metadata"] = {"name": "Menu"}
menu["innerBlocks"] = [slot("menuContent", [mobile_header, nav])]

burger = json.loads(json.dumps(burger0))
burger["attrs"]["metadata"] = {"name": "Menu Toggle"}
burger["attrs"]["attributes"]["ariaLabel"] = "Open menu"
burger["attrs"]["attributes"].pop("customIdForThisToggle", None)

phone_path = cont0["innerBlocks"][2]["innerBlocks"][1]["innerBlocks"][0]  # svg block

header = el("Site Header", "header", {
    "data-etch-element": "section",
    "data-overlay-header": "false",
    "data-overlay-header-offset": "false",
    "data-sticky-header": "true",
    "data-hide-on-scroll": "true",
    "data-hide-at": "200px",
    "data-show-on-scroll-up": "true",
    "data-skip-link": "true",
    "class": "site-header",
}, ["etch-section-style", "sh-root"], [
    el("Bar", "div", {"data-menu-element": "header-inner", "class": "site-header__bar"}, ["sh-bar"], [
        el("Container", "div", {"data-etch-element": "container", "class": "site-header__container"},
           ["etch-container-style", "sh-container"], [
               el("Logo", "a", {"href": "/", "aria-label": "Home", "class": "site-header__logo"}, ["sh-logo"], [
                   {"blockName": "etch/dynamic-image",
                    "attrs": {"metadata": {"name": "Logo Image"}, "tag": "img",
                              "attributes": {"class": "site-header__logo-img", "mediaId": ""},
                              "styles": ["sh-logo-img"]},
                    "innerBlocks": [], "innerHTML": "\n\n", "innerContent": ["\n", "\n"]},
               ]),
               menu,
               el("Actions", "div", {"class": "site-header__actions"}, ["sh-actions"], [
                   el("CTA", "a", {"href": "/contact/", "class": "btn--secondary"},
                      None, [text("Get a Quote")]),
                   el("Phone", "a", {"href": "tel:+6620000000",
                                     "class": "site-header__phone btn--secondary btn--outline"},
                      None, [
                          phone_path,
                          el("Number", "span", {}, None, [text("02-000-0000")]),
                      ]),
               ]),
               burger,
           ])
    ])
], script)

payload = {
    "type": "block",
    "gutenbergBlock": header,
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
    "styles": styles,
    "components": orig["components"],
    "version": 2.1,
}

# sanity: every referenced style id exists
used = set()
def walk(b):
    used.update(b.get("attrs", {}).get("styles") or [])
    for c in b.get("innerBlocks", []):
        walk(c)
walk(header)
for c in orig["components"].values():
    for b in c["blocks"]:
        walk(b)
missing = used - set(styles)
assert not missing, missing

with open(OUT, "w") as f:
    f.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
print("ok", OUT, len(styles), "styles", len(orig["components"]), "components")
