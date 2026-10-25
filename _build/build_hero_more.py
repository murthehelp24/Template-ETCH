"""Hero variants for the home page: full image, collage, colour panel, image with a left-to-right overlay.
Plain sections (edit the text in the blocks); colours come from kit.COLORS. Lengths in rem are written for
1rem = 10px and become to-rem() (lib_etch.portable).

    python3 build_hero_more.py <src> <kit>/etch-sections
"""
import json, os, sys
from lib_etch import el, text, svg, img, style, write
from kit import (SEC, CON, BASE, HEADING_STYLES, MEDIA_STYLES, BUTTONS_STYLES, CHECKS_STYLES, heading, checks,
                 media_img, icon, kit_payload)

OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
outputs = {}
LINE_URL = "https://line.me/R/ti/p/@example"
TEXT = ("A clear headline that says what you do and for whom",
        "One or two sentences about the main benefit. Keep it short and specific.")
TRUST = ["Short trust point", "Another reason to choose you", "Free consultation"]

# text on the primary colour or on an image darkened with it (same rules as kit.BAND_STYLES, without the background)
ON_DARK = """color: var(--main-on-primary);

  :is(h1, h2, h3, h4, h5, h6),
  .main-heading__eyebrow {
    color: inherit;
  }

  .main-heading__intro {
    color: var(--main-on-primary-muted);
  }"""

# a photo behind the whole section, under an overlay drawn by the section's ::before
COVER_CSS = """position: relative;
  isolation: isolate;
  overflow: hidden;
  justify-content: center;
  min-block-size: 80rem; /* same height as the colour-panel hero */
  padding-block: var(--section-space-xl);

  &::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: -1;
    background: var(--_overlay);
  }

  @media (width <= 768px) {
    min-block-size: 60rem;
  }"""

BG_CSS = """position: absolute;
  inset: 0;
  z-index: -2;
  margin: 0;"""

BG_IMG_CSS = """display: block;
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
  background-color: var(--main-primary);"""


def section(name, cls, style_ids, children, container=True, behind=()):
    """behind: blocks placed before the container, e.g. a background photo covering the whole section"""
    kids = [el("Container", "div", CON, ["etch-container-style"], children)] if container else children
    kids = list(behind) + kids
    return el(name, "section", {**SEC, "class": cls}, ["etch-section-style", *style_ids], kids)


def cover_bg(block, sid):
    return el("Background", "figure", {"class": f"{block}__bg"}, [f"{sid}-bg"], [
        img("Background Image", {"class": f"{block}__img", "mediaId": "", "loading": "eager"}, [f"{sid}-img"])])


def btn(name, cls, href, label, icon_name=None, blank=False):
    a = {"class": cls, "href": href}
    if blank:
        a.update({"target": "_blank", "rel": "noopener"})
    kids = [svg("Icon", icon(icon_name))] if icon_name else []
    return el(name, "a", a, None, kids + [text(label)])


def button_row(*items):
    return el("Buttons", "div", {"class": "main-buttons"}, ["mn-buttons"], list(items))


# ACSS buttons for a dark background (the same pair the header uses on the primary colour)
def dark_buttons():
    return button_row(btn("LINE", "btn--secondary", LINE_URL, "Chat on LINE", blank=True),
                      btn("Services", "btn--secondary btn--outline", "/services/", "Our services"))


# ================================================================ 1. full image, centred text
p = "mn-hi"
image_styles = {**BASE, **HEADING_STYLES, **BUTTONS_STYLES, **CHECKS_STYLES,
    p: style(".main-hero-image", COVER_CSS.replace("var(--_overlay)",
             "color-mix(in srgb, var(--main-primary) 78%, transparent)") + "\n\n  " + ON_DARK + """

  .main-buttons {
    justify-content: center;
  }

  /* trust points in one row under the buttons */
  .main-checks {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: var(--space-xs) var(--space-l);
    margin-block-start: var(--space-s);
  }"""),
    p + "-bg": style(".main-hero-image__bg", BG_CSS),
    p + "-img": style(".main-hero-image__img", BG_IMG_CSS),
    p + "-content": style(".main-hero-image__content", """display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--content-gap);
  max-inline-size: 96rem;
  margin-inline: auto;
  text-align: center;"""),
}
outputs["main-hero-image"] = kit_payload(section("Hero Image", "main-hero-image", [p], [
    el("Content", "div", {"class": "main-hero-image__content"}, [p + "-content"], [
        heading("Welcome", *TEXT, tag="h1", center=True),
        dark_buttons(),
        checks(TRUST),
    ]),
], behind=[cover_bg("main-hero-image", "mn-hi")]), image_styles)

# ================================================================ 3. text + stats, three-photo collage with a badge
p = "mn-hc"
STATS = [("15+", "Years of experience"), ("2,000+", "Happy customers"), ("4.9", "Google rating")]
collage_styles = {**BASE, **HEADING_STYLES, **MEDIA_STYLES, **BUTTONS_STYLES,
    p: style(".main-hero-collage", "padding-block: var(--section-space-l);\n  background-color: var(--main-light);"),
    p + "-grid": style(".main-hero-collage__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 44rem), 1fr));
  gap: var(--container-gap);
  align-items: center;"""),
    p + "-content": style(".main-hero-collage__content", """display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--content-gap);"""),
    p + "-stats": style(".main-hero-collage__stats", """display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-m);
  inline-size: 100%;
  margin: var(--space-s) 0 0;
  padding-block-start: var(--space-m);
  border-block-start: 1px solid var(--main-line);"""),
    p + "-stat": style(".main-hero-collage__stat", "display: flex;\n  flex-direction: column;\n  gap: 0.4rem;\n"
                                                    "  margin: 0;"),
    p + "-value": style(".main-hero-collage__value", """font-size: var(--h3);
  font-weight: 800;
  line-height: 1.1;
  color: var(--main-primary);"""),
    p + "-label": style(".main-hero-collage__label", "margin: 0;\n  font-size: var(--text-s);\n"
                                                      "  color: var(--main-text-muted);"),
    p + "-media": style(".main-hero-collage__media", """/* one tall photo on the left, two stacked on the right */
  position: relative;
  display: grid;
  grid-template-columns: 3fr 2fr;
  grid-template-rows: repeat(2, minmax(0, 1fr));
  gap: var(--space-s);
  aspect-ratio: 1 / 1;
  margin: 0;

  .main-media__img {
    block-size: 100%;
    aspect-ratio: auto;
    border-radius: var(--radius-l);
  }

  > :first-child {
    grid-row: 1 / -1;
  }"""),
    p + "-badge": style(".main-hero-collage__badge", """position: absolute;
  inset-inline-start: calc(var(--space-m) * -1);
  inset-block-end: var(--space-l);
  display: flex;
  align-items: center;
  gap: var(--space-s);
  padding: var(--space-s) var(--space-m);
  border-radius: var(--radius-m);
  background-color: var(--main-light);
  box-shadow: 0 1.6rem 4rem var(--main-shadow);

  @media (width <= 768px) {
    inset-inline-start: var(--space-xs);
    inset-block-end: var(--space-xs);
  }"""),
    p + "-badge-icon": style(".main-hero-collage__badge-icon", """flex: none;
  inline-size: 4.8rem;
  block-size: 4.8rem;
  padding: 1.1rem;
  border-radius: 50%;
  background-color: var(--main-accent);
  color: var(--main-on-primary);"""),
    p + "-badge-text": style(".main-hero-collage__badge-text", "display: flex;\n  flex-direction: column;\n"
                                                                "  font-size: var(--text-s);\n"
                                                                "  color: var(--main-text-muted);"),
    p + "-badge-value": style(".main-hero-collage__badge-value", "font-size: var(--h4);\n  font-weight: 800;\n"
                                                                  "  line-height: 1.2;\n  color: var(--main-text);"),
}
outputs["main-hero-collage"] = kit_payload(section("Hero Collage", "main-hero-collage", [p], [
    el("Grid", "div", {"class": "main-hero-collage__grid"}, [p + "-grid"], [
        el("Content", "div", {"class": "main-hero-collage__content"}, [p + "-content"], [
            heading("Welcome", *TEXT, tag="h1"),
            button_row(btn("LINE", "btn--primary", LINE_URL, "Chat on LINE", blank=True),
                       btn("Services", "btn--primary btn--outline", "/services/", "Our services")),
            el("Stats", "dl", {"class": "main-hero-collage__stats"}, [p + "-stats"], [
                el("Stat", "div", {"class": "main-hero-collage__stat"}, [p + "-stat"], [
                    el("Value", "dt", {"class": "main-hero-collage__value"}, [p + "-value"], [text(v)]),
                    el("Label", "dd", {"class": "main-hero-collage__label"}, [p + "-label"], [text(l)]),
                ]) for v, l in STATS]),
        ]),
        el("Media", "figure", {"class": "main-hero-collage__media"}, [p + "-media"], [
            media_img("Image 1", eager=True), media_img("Image 2", eager=True), media_img("Image 3"),
            el("Badge", "div", {"class": "main-hero-collage__badge"}, [p + "-badge"], [
                svg("Badge icon", icon("award"), "main-hero-collage__badge-icon", [p + "-badge-icon"]),
                el("Badge Text", "span", {"class": "main-hero-collage__badge-text"}, [p + "-badge-text"], [
                    el("Value", "b", {"class": "main-hero-collage__badge-value"}, [p + "-badge-value"],
                       [text("15+ years")]),
                    text("of trusted service"),
                ]),
            ]),
        ]),
    ])]), collage_styles)

# ================================================================ 5. text on the primary colour, photo to the edge
p = "mn-hp"
panel_styles = {**BASE, **HEADING_STYLES, **BUTTONS_STYLES,
    p: style(".main-hero-panel", """padding: 0;
  overflow: hidden;
  background-color: var(--main-primary);
  """ + ON_DARK),
    p + "-grid": style(".main-hero-panel__grid", """display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  inline-size: 100%;
  min-block-size: 80rem; /* same height as the full-image heroes */

  @media (width <= 992px) {
    grid-template-columns: 1fr;
  }"""),
    p + "-content": style(".main-hero-panel__content", """/* lines up with the page container on the left */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: var(--content-gap);
  padding-block: var(--section-space-l);
  padding-inline: max(var(--gutter), calc((100vw - var(--content-width, 1366px)) / 2)) var(--space-xl);

  @media (width <= 992px) {
    padding-inline: var(--gutter);
  }"""),
    p + "-media": style(".main-hero-panel__media", """margin: 0;
  overflow: hidden;
  border-end-start-radius: 12rem;
  background-color: var(--main-light-alt);

  @media (width <= 992px) {
    aspect-ratio: 4 / 3;
    border-end-start-radius: 0;
    border-start-start-radius: 6rem;
  }"""),
    p + "-img": style(".main-hero-panel__img", "display: block;\n  inline-size: 100%;\n  block-size: 100%;\n"
                                               "  object-fit: cover;"),
}
outputs["main-hero-panel"] = kit_payload(section("Hero Panel", "main-hero-panel", [p], [
    el("Grid", "div", {"class": "main-hero-panel__grid"}, [p + "-grid"], [
        el("Content", "div", {"class": "main-hero-panel__content"}, [p + "-content"], [
            heading("Welcome", *TEXT, tag="h1"),
            dark_buttons(),
        ]),
        el("Media", "figure", {"class": "main-hero-panel__media"}, [p + "-media"], [
            img("Image", {"class": "main-hero-panel__img", "mediaId": "", "loading": "eager"}, [p + "-img"])]),
    ])], container=False), panel_styles)

# ================================================================ 6. full image, overlay fading left to right
p = "mn-hg"
gradient_styles = {**BASE, **HEADING_STYLES, **BUTTONS_STYLES,
    p: style(".main-hero-gradient", COVER_CSS.replace("var(--_overlay)", """linear-gradient(
      90deg,
      color-mix(in srgb, var(--main-primary) 92%, transparent) 0%,
      color-mix(in srgb, var(--main-primary) 64%, transparent) 40%,
      color-mix(in srgb, var(--main-primary) 0%, transparent) 75%
    )""").replace("""  @media (width <= 768px) {
    min-block-size: 60rem;
  }""", """  /* phones: the text covers the photo, so darken it evenly */
  @media (width <= 768px) {
    min-block-size: 60rem;

    &::before {
      background: color-mix(in srgb, var(--main-primary) 80%, transparent);
    }
  }""") + "\n\n  " + ON_DARK + """

  .main-buttons a {
    gap: var(--space-xs);
  }

  .main-buttons svg {
    flex: none;
    inline-size: 1.25em;
    block-size: 1.25em;
  }"""),
    p + "-bg": style(".main-hero-gradient__bg", BG_CSS),
    p + "-img": style(".main-hero-gradient__img", BG_IMG_CSS),
    p + "-content": style(".main-hero-gradient__content", """display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--content-gap);
  max-inline-size: 64rem;"""),
}
outputs["main-hero-gradient"] = kit_payload(section("Hero Gradient", "main-hero-gradient", [p], [
    el("Content", "div", {"class": "main-hero-gradient__content"}, [p + "-content"], [
        heading("Business name · Area, City", *TEXT, tag="h1"),
        button_row(btn("LINE", "btn--secondary", LINE_URL, "Chat on LINE", blank=True),
                   btn("Phone", "btn--secondary btn--outline", "tel:+6620000000", "Call 02-000-0000", "phone")),
    ]),
], behind=[cover_bg("main-hero-gradient", "mn-hg")]), gradient_styles)

for name, payload in outputs.items():
    write(f"{OUT}/{name}.etch.txt", payload)
    print("ok", name, len(payload["styles"]), "styles", len(json.dumps(payload)) // 1024, "KB")
