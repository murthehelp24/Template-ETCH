"""Paste-ready, project-agnostic footer (MainFooter component) + floating LINE / phone buttons.
Colours come from kit.COLORS, social icons from kit.social_list."""
import sys
from lib_etch import el, text, img, svg, cond, block, style, prop, write
from kit import BASE, SOCIAL_STYLES, SOCIAL_PROPS, social_list, icon, kit_payload

OUT = sys.argv[2]
COMP_ID = 990001          # any id: Etch maps it to the target's component id by key on paste

ROOT_CSS = """--main-social-color: var(--main-on-primary);
  --main-footer-logo-width: 9.6rem;

  padding-block-start: var(--section-space-s);
  padding-inline: var(--gutter);
  background-color: var(--main-primary);
  color: var(--main-on-primary);"""

GRID_CSS = """display: grid;
  grid-template-columns: 2fr repeat(3, 1fr);
  gap: var(--grid-gap);
  padding-block-end: var(--space-l);

  @media (width <= 992px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (width <= 768px) {
    grid-template-columns: 1fr;
  }"""

LINK_CSS = """display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: var(--text-s);
  color: inherit;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
    text-decoration-color: var(--main-accent);
  }"""

FLOAT_CSS = """position: fixed;
  inset-block-end: var(--space-m);
  inset-inline-end: var(--space-m);
  z-index: 40;
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);"""

FLOAT_BTN_CSS = """display: grid;
  place-items: center;
  inline-size: 5.6rem;
  block-size: 5.6rem;
  border-radius: 50%;
  background-color: var(--main-primary);
  color: var(--main-on-primary);
  box-shadow: 0 0 0 3px var(--main-light), 0 0.6rem 1.6rem var(--main-shadow);
  transition: background-color 0.2s ease, scale 0.2s ease;

  svg {
    inline-size: 2.6rem;
    block-size: 2.6rem;
  }

  &:hover,
  &:focus-visible {
    background-color: var(--main-accent);
    scale: 1.06;
  }

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }"""

styles = {
    "etch-container-style": BASE["etch-container-style"],
    **SOCIAL_STYLES,
    "mf-root": style(".main-footer", ROOT_CSS),
    "mf-container": style(".main-footer__container", "gap: var(--container-gap);"),
    "mf-grid": style(".main-footer__grid", GRID_CSS),
    "mf-col": style(".main-footer__col", "display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n"
                                         "  gap: var(--space-s);"),
    "mf-brand": style(".main-footer__brand", "max-inline-size: 44rem;\n\n  @media (width <= 992px) {\n"
                                             "    grid-column: 1 / -1;\n  }"),
    "mf-logo-img": style(".main-footer__logo-img", "display: block;\n  inline-size: var(--main-footer-logo-width);\n"
                                                   "  block-size: auto;"),
    "mf-text": style(".main-footer__text", "font-style: normal;\n  font-size: var(--text-s);\n"
                                           "  color: var(--main-on-primary-muted);\n  white-space: pre-line;"),
    "mf-title": style(".main-footer__title", "font-size: var(--text-m);\n  font-weight: 600;\n  color: inherit;"),
    "mf-list": style(".main-footer__list", "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);\n"
                                           "  margin: 0;\n  padding: 0;\n  list-style: none;"),
    "mf-link": style(".main-footer__link", LINK_CSS),
    "mf-icon": style(".main-footer__icon", "display: block;\n  inline-size: 1.25em;\n  block-size: 1.25em;\n"
                                           "  flex-shrink: 0;"),
    "mf-bottom": style(".main-footer__bottom", """margin-block-start: var(--space-l);
  margin-inline: calc(var(--gutter) * -1);
  padding: var(--space-xs) var(--gutter);
  border-block-start: 1px solid var(--main-line-on-primary);
  font-size: var(--text-s);
  text-align: center;
  color: var(--main-on-primary-muted);"""),
    "mf-float": style(".main-float", FLOAT_CSS),
    "mf-float-btn": style(".main-float__btn", FLOAT_BTN_CSS),
}


def link_item(label, href):
    return el("Item", "li", {}, None, [
        el("Link", "a", {"class": "main-footer__link", "href": href}, ["mf-link"], [text(label)])])


def link_col(name, title, links):
    return el(name, "nav", {"class": "main-footer__col", "aria-label": title}, ["mf-col"], [
        el("Title", "h2", {"class": "main-footer__title"}, ["mf-title"], [text(title)]),
        el("List", "ul", {"class": "main-footer__list"}, ["mf-list"], [link_item(l, h) for l, h in links]),
    ])


def icon_link(name, href, icon_name, label, extra=None):
    a = {"class": "main-footer__link", "href": href, **(extra or {})}
    return el(name, "a", a, ["mf-link"], [svg(f"{name} icon", icon(icon_name), "main-footer__icon", ["mf-icon"]),
                                          text(label)])


def float_btn(name, href, icon_name, label, blank=False):
    a = {"class": "main-float__btn", "href": href, "aria-label": label}
    if blank:
        a.update({"target": "_blank", "rel": "noopener"})
    return el(name, "a", a, ["mf-float-btn"], [svg(f"{name} icon", icon(icon_name))])


blocks = [el("Main Footer", "footer", {"class": "main-footer"}, ["mf-root"], [
    el("Container", "div", {"data-etch-element": "container", "class": "main-footer__container"},
       ["etch-container-style", "mf-container"], [
           el("Grid", "div", {"class": "main-footer__grid"}, ["mf-grid"], [
               el("Brand", "div", {"class": "main-footer__col main-footer__brand"}, ["mf-col", "mf-brand"], [
                   el("Logo", "a", {"href": "/", "aria-label": "{site.name}"}, None, [
                       img("Logo Image", {"class": "main-footer__logo-img", "mediaId": "", "alt": "{site.name}",
                                          "loading": "lazy"}, ["mf-logo-img"])]),
                   el("Description", "p", {"class": "main-footer__text"}, ["mf-text"], [text("{props.description}")]),
               ]),
               link_col("Menu", "Menu", [("Home", "/"), ("About", "/about/"), ("Blog", "/blog/"),
                                         ("Contact", "/contact/"), ("Privacy Policy", "/privacy-policy/")]),
               link_col("Services", "Services", [("Service 1", "/services/service-1/"),
                                                 ("Service 2", "/services/service-2/"),
                                                 ("Service 3", "/services/service-3/"),
                                                 ("Service 4", "/services/service-4/")]),
               el("Contact", "div", {"class": "main-footer__col"}, ["mf-col"], [
                   el("Title", "h2", {"class": "main-footer__title"}, ["mf-title"], [text("{props.contactTitle}")]),
                   cond("If address", "props.address", el("Address", "address", {"class": "main-footer__text"},
                                                          ["mf-text"], [text("{props.address}")])),
                   cond("If hours", "props.hours", el("Hours", "p", {"class": "main-footer__text"}, ["mf-text"],
                                                      [text("{props.hours}")])),
                   cond("If phone", "props.phone", icon_link("Phone", "tel:{props.phone}", "phone", "{props.phone}")),
                   cond("If email", "props.email", icon_link("Email", "mailto:{props.email}", "email",
                                                             "{props.email}")),
                   cond("If map", "props.mapUrl", icon_link("Map", "{props.mapUrl}", "address", "{props.mapLabel}",
                                                            {"target": "_blank", "rel": "noopener"})),
                   social_list(),
               ]),
           ]),
       ]),
    el("Bottom", "div", {"class": "main-footer__bottom"}, ["mf-bottom"], [
        el("Copyright", "p", {}, None, [
            text('Copyright © {site.currentDate.dateFormat("Y")} {site.name}. {props.copyrightNote}')])]),
    cond("If floating buttons", "props.showFloat", el("Floating Buttons", "div", {"class": "main-float"}, ["mf-float"], [
        cond("If LINE", "props.lineUrl", float_btn("LINE", "{props.lineUrl}", "line", "Chat on LINE", True)),
        cond("If phone", "props.phone", float_btn("Phone", "tel:{props.phone}", "phone", "Call {props.phone}")),
    ])),
])]

properties = [
    prop("Description", "description", "Short description of the business — one or two sentences."),
    prop("Contact Title", "contactTitle", "Contact"),
    prop("Address", "address", "123 Example Road, Bangkok 10110", "Line breaks are kept"),
    prop("Opening Hours", "hours", "Mon–Sat 09:00–18:00"),
    prop("Phone", "phone", "02-000-0000", "Empty = hidden"),
    prop("Email", "email", "hello@example.com", "Empty = hidden"),
    prop("Map URL", "mapUrl", "https://maps.google.com/", "Empty = hidden"),
    prop("Map Label", "mapLabel", "View on Google Maps"),
    *SOCIAL_PROPS,
    prop("Copyright Note", "copyrightNote", "All rights reserved."),
    prop("Floating Buttons", "showFloat", True, "Round LINE / phone buttons fixed to the bottom corner of every page",
         "boolean"),
]

component = {"id": COMP_ID, "legacyId": "", "name": "Main Footer", "key": "MainFooter",
             "description": "Project-agnostic site footer with floating LINE / phone buttons. Edit the property "
                            "defaults here so every template's footer updates at once.",
             "blocks": blocks, "properties": properties}

instance = block("etch/component", {"ref": COMP_ID, "attributes": {}})
p = kit_payload(instance, styles, {str(COMP_ID): component})
write(OUT, p)
print("ok", OUT, len(p["styles"]), "styles")
