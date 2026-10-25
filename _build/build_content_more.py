"""Variants of the content sections: image + text (5), stats (4), steps (4), reviews (3).
Plain sections (edit the text in the blocks); colours come from kit.COLORS. Lengths in rem are written for
1rem = 10px and become to-rem() (lib_etch.portable).

    python3 build_content_more.py <src> <kit>/etch-sections
"""
import json, os, sys
from lib_etch import el, text, svg, img, style, write
from kit import (SEC, CON, BASE, HEADING_STYLES, MEDIA_STYLES, BUTTONS_STYLES, CHECKS_STYLES, BAND_STYLES, heading,
                 buttons, checks, media_img, icon, kit_payload)

OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
outputs = {}
ABOUT = ("About us", "A headline for this part of the page",
         "A paragraph that explains the topic. Two to four sentences work best next to an image.")
POINTS = ["First key point", "Second key point", "Third key point"]
STATS = [("15+", "Years of experience"), ("2,000+", "Happy customers"), ("98%", "Would recommend us"),
         ("24/7", "Online support")]
STEPS = [("Contact us", "Call, chat on LINE or send the form."),
         ("Consultation", "We listen and recommend the right option."),
         ("Service", "Our team does the work with care."),
         ("Follow-up", "We check the result and stay in touch.")]
REVIEW = "Great service from start to finish. The team explained everything clearly and I felt well looked after."
PLACES = ["Bangkok", "Chiang Mai", "Phuket", "Khon Kaen"]


def section(name, cls, style_ids, children, con_cls=None, con_ids=(), extra=()):
    """extra: classes on the section besides cls (each with its style id in style_ids)"""
    con = {**CON, "class": con_cls} if con_cls else CON
    return el(name, "section", {**SEC, "class": " ".join([cls, *extra])}, ["etch-section-style", *style_ids], [
        el("Container", "div", con, ["etch-container-style", *con_ids], children)])


def stars(cls, sid):
    return el("Stars", "div", {"class": cls, "role": "img", "aria-label": "5 out of 5 stars"}, [sid],
              [svg("Star", icon("star")) for _ in range(5)])


STARS_CSS = """display: flex;
  gap: calc(var(--space-xs) / 4);
  color: var(--main-accent);

  svg {
    inline-size: 1.8rem;
    block-size: 1.8rem;
  }"""

ON_DARK = """:is(h1, h2, h3, h4, h5, h6),
  .main-heading__eyebrow {
    color: inherit;
  }

  .main-heading__intro {
    color: var(--main-on-primary-muted);
  }"""

TWO_COL = """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 36rem), 1fr));
  gap: var(--container-gap);
  align-items: center;"""

CONTENT = """display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--content-gap);"""

LIST_RESET = "margin: 0;\n  padding: 0;\n  list-style: none;"

# ================================================================================================ IMAGE + TEXT
# ---------------------------------------------------------------- 1. image on an accent block + experience badge
p, b = "mn-spo", "main-split-overlap"
outputs[b] = kit_payload(section("Split Overlap", b, [p], [
    el("Grid", "div", {"class": f"{b}__grid"}, [p + "-grid"], [
        el("Media", "div", {"class": f"{b}__media"}, [p + "-media"], [
            media_img(),
            el("Badge", "div", {"class": f"{b}__badge"}, [p + "-badge"], [
                el("Value", "b", {"class": f"{b}__badge-value"}, [p + "-badge-value"], [text("15+")]),
                el("Label", "span", {"class": f"{b}__badge-label"}, [p + "-badge-label"],
                   [text("Years of experience")]),
            ]),
        ]),
        el("Content", "div", {"class": f"{b}__content"}, [p + "-content"], [
            heading(*ABOUT), checks(POINTS), buttons("Learn more", "/about/", "Contact us", "/contact/"),
        ]),
    ])]), {**BASE, **HEADING_STYLES, **MEDIA_STYLES, **BUTTONS_STYLES, **CHECKS_STYLES,
    p: style(f".{b}", "background-color: var(--main-light);"),
    p + "-grid": style(f".{b}__grid", TWO_COL),
    p + "-media": style(f".{b}__media", """/* the accent block peeks out behind the photo */
  position: relative;
  isolation: isolate;
  margin: var(--space-m) var(--space-m) var(--space-m) 0;

  --main-media-ratio: 4 / 5;

  &::before {
    content: "";
    position: absolute;
    inset: calc(var(--space-m) * -1) calc(var(--space-m) * -1) var(--space-xl) var(--space-xl);
    z-index: -1;
    border-radius: var(--radius-l);
    background-color: var(--main-accent-soft);
  }"""),
    p + "-badge": style(f".{b}__badge", """position: absolute;
  inset-block-end: var(--space-m);
  inset-inline-start: calc(var(--space-m) * -1);
  display: flex;
  flex-direction: column;
  padding: var(--space-s) var(--space-m);
  border-radius: var(--radius-m);
  background-color: var(--main-primary);
  box-shadow: 0 1.2rem 2.8rem var(--main-shadow);
  color: var(--main-on-primary);

  @media (width <= 768px) {
    inset-inline-start: var(--space-s);
  }"""),
    p + "-badge-value": style(f".{b}__badge-value", "font-size: var(--h2);\n  font-weight: 800;\n  line-height: 1;\n"
                                                    "  color: var(--main-accent);"),
    p + "-badge-label": style(f".{b}__badge-label", "font-size: var(--text-s);"),
    p + "-content": style(f".{b}__content", CONTENT),
})

# ---------------------------------------------------------------- 2. on the primary colour, image right
p, b = "mn-spb", "main-split-band"
outputs[b] = kit_payload(section("Split Band", b, [p, "mn-band"], [
    el("Grid", "div", {"class": f"{b}__grid"}, [p + "-grid"], [
        el("Content", "div", {"class": f"{b}__content"}, [p + "-content"], [
            heading(*ABOUT), checks(POINTS),
            el("Buttons", "div", {"class": "main-buttons"}, ["mn-buttons"], [
                el("Primary", "a", {"class": "btn--secondary", "href": "/about/"}, None, [text("Learn more")]),
                el("Secondary", "a", {"class": "btn--secondary btn--outline", "href": "/contact/"}, None,
                   [text("Contact us")]),
            ]),
        ]),
        el("Media", "figure", {"class": f"{b}__media"}, [p + "-media"], [media_img()]),
    ])], extra=["main-band"]), {**BASE, **HEADING_STYLES, **MEDIA_STYLES, **BUTTONS_STYLES, **CHECKS_STYLES,
                                **BAND_STYLES,
    p: style(f".{b}", """.main-checks__icon {
    background-color: var(--main-accent);
    color: var(--main-on-primary);
  }"""),
    p + "-grid": style(f".{b}__grid", TWO_COL),
    p + "-content": style(f".{b}__content", CONTENT),
    p + "-media": style(f".{b}__media", "--main-media-ratio: 1 / 1;\n  margin: 0;\n\n  .main-media__img {\n"
                                        "    border-radius: var(--radius-l);\n  }"),
})

# ---------------------------------------------------------------- 3. image + text with three numbers instead of a list
p, b = "mn-sps", "main-split-stats"
outputs[b] = kit_payload(section("Split Stats", b, [p], [
    el("Grid", "div", {"class": f"{b}__grid"}, [p + "-grid"], [
        el("Media", "figure", {"class": f"{b}__media"}, [p + "-media"], [media_img()]),
        el("Content", "div", {"class": f"{b}__content"}, [p + "-content"], [
            heading(*ABOUT),
            el("Stats", "ul", {"class": f"{b}__stats"}, [p + "-stats"], [
                el("Stat", "li", {"class": f"{b}__stat"}, [p + "-stat"], [
                    el("Number", "b", {"class": f"{b}__number"}, [p + "-number"], [text(n)]),
                    el("Label", "span", {"class": f"{b}__label"}, [p + "-label"], [text(l)]),
                ]) for n, l in STATS[:3]]),
            buttons("Learn more", "/about/", "Contact us", "/contact/"),
        ]),
    ])]), {**BASE, **HEADING_STYLES, **MEDIA_STYLES, **BUTTONS_STYLES,
    p: style(f".{b}", "background-color: var(--main-light-alt);"),
    p + "-grid": style(f".{b}__grid", TWO_COL),
    p + "-media": style(f".{b}__media", "--main-media-ratio: 4 / 3;\n  margin: 0;"),
    p + "-content": style(f".{b}__content", CONTENT),
    p + "-stats": style(f".{b}__stats", """display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-s);
  inline-size: 100%;
  """ + LIST_RESET + """

  @media (width <= 480px) {
    grid-template-columns: 1fr;
  }"""),
    p + "-stat": style(f".{b}__stat", """display: flex;
  flex-direction: column;
  gap: calc(var(--space-xs) / 2);
  padding-inline-start: var(--space-s);
  border-inline-start: 3px solid var(--main-accent);"""),
    p + "-number": style(f".{b}__number", "font-size: var(--h3);\n  font-weight: 800;\n  line-height: 1.1;\n"
                                          "  color: var(--main-primary);"),
    p + "-label": style(f".{b}__label", "font-size: var(--text-s);\n  color: var(--main-text-muted);"),
})

# ---------------------------------------------------------------- 4. two overlapping photos + text
p, b = "mn-spi", "main-split-images"
outputs[b] = kit_payload(section("Split Images", b, [p], [
    el("Grid", "div", {"class": f"{b}__grid"}, [p + "-grid"], [
        el("Content", "div", {"class": f"{b}__content"}, [p + "-content"], [
            heading(*ABOUT), checks(POINTS), buttons("Learn more", "/about/", "Contact us", "/contact/"),
        ]),
        el("Media", "div", {"class": f"{b}__media"}, [p + "-media"], [
            el("Main Photo", "figure", {"class": f"{b}__main"}, [p + "-main"], [media_img("Image 1")]),
            el("Small Photo", "figure", {"class": f"{b}__small"}, [p + "-small"], [media_img("Image 2")]),
        ]),
    ])]), {**BASE, **HEADING_STYLES, **MEDIA_STYLES, **BUTTONS_STYLES, **CHECKS_STYLES,
    p: style(f".{b}", "background-color: var(--main-light);"),
    p + "-grid": style(f".{b}__grid", TWO_COL),
    p + "-content": style(f".{b}__content", CONTENT),
    p + "-media": style(f".{b}__media", """display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  grid-template-rows: repeat(12, auto);"""),
    p + "-main": style(f".{b}__main", """grid-column: 1 / 10;
  grid-row: 1 / 10;
  margin: 0;

  --main-media-ratio: 4 / 5;"""),
    p + "-small": style(f".{b}__small", """grid-column: 6 / 13;
  grid-row: 7 / 13;
  align-self: end;
  margin: 0;
  padding: 0.8rem;
  border-radius: calc(var(--radius-m) + 0.8rem);
  background-color: var(--main-light);
  box-shadow: 0 1.2rem 2.8rem var(--main-shadow);

  --main-media-ratio: 1 / 1;"""),
})

# ---------------------------------------------------------------- 5. photo fills one half edge to edge
p, b = "mn-spf", "main-split-full"
outputs[b] = kit_payload(el("Split Full", "section", {**SEC, "class": b}, ["etch-section-style", p], [
    el("Media", "figure", {"class": f"{b}__media"}, [p + "-media"], [media_img()]),
    el("Content", "div", {"class": f"{b}__content"}, [p + "-content"], [
        heading(*ABOUT), checks(POINTS), buttons("Learn more", "/about/", "Contact us", "/contact/"),
    ]),
]), {**BASE, **HEADING_STYLES, **MEDIA_STYLES, **BUTTONS_STYLES, **CHECKS_STYLES,
    p: style(f".{b}", """display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: stretch;
  padding: 0;
  background-color: var(--main-light-alt);

  @media (width <= 768px) {
    grid-template-columns: 1fr;
  }"""),
    p + "-media": style(f".{b}__media", """min-block-size: 48rem;
  margin: 0;

  .main-media__img {
    block-size: 100%;
    aspect-ratio: auto;
    border-radius: 0;
  }

  @media (width <= 768px) {
    min-block-size: 0;

    .main-media__img {
      aspect-ratio: 4 / 3;
    }
  }"""),
    p + "-content": style(f".{b}__content", """display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  gap: var(--content-gap);
  max-inline-size: 64rem;
  padding: var(--section-space-m) var(--gutter, var(--space-l));"""),
})

# ================================================================================================ STATS
# ---------------------------------------------------------------- 1. light background, lines between the numbers
p, b = "mn-stl", "main-stats-light"
outputs[b] = kit_payload(section("Stats Light", b, [p], [
    el("Grid", "ul", {"class": f"{b}__grid"}, [p + "-grid"], [
        el("Item", "li", {"class": f"{b}__item"}, [p + "-item"], [
            el("Number", "p", {"class": f"{b}__number"}, [p + "-number"], [text(n)]),
            el("Label", "p", {"class": f"{b}__label"}, [p + "-label"], [text(l)]),
        ]) for n, l in STATS]),
]), {**BASE,
    p: style(f".{b}", "padding-block: var(--section-space-s);\n  background-color: var(--main-light);"),
    p + "-grid": style(f".{b}__grid", """display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  """ + LIST_RESET + """
  text-align: center;

  @media (width <= 768px) {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    row-gap: var(--space-l);
  }"""),
    p + "-item": style(f".{b}__item", """display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-xs);
  padding-inline: var(--space-s);

  & + & {
    border-inline-start: 1px solid var(--main-line);
  }

  @media (width <= 768px) {
    &:nth-child(odd) {
      border-inline-start: 0;
    }
  }"""),
    p + "-number": style(f".{b}__number", """margin: 0;
  font-size: var(--h1);
  font-weight: 800;
  line-height: 1;
  color: var(--main-primary);

  /* short accent line under the number */
  &::after {
    content: "";
    display: block;
    inline-size: 3.2rem;
    block-size: 3px;
    margin: var(--space-xs) auto 0;
    background-color: var(--main-accent);
  }"""),
    p + "-label": style(f".{b}__label", "margin: 0;\n  color: var(--main-text-muted);"),
})

# ---------------------------------------------------------------- 2. cards with an icon
p, b = "mn-stc", "main-stats-cards"
STAT_ICONS = ["award", "users", "heart", "hours"]
outputs[b] = kit_payload(section("Stats Cards", b, [p], [
    el("Grid", "ul", {"class": f"{b}__grid"}, [p + "-grid"], [
        el("Card", "li", {"class": f"{b}__card"}, [p + "-card"], [
            svg("Icon", icon(ic), f"{b}__icon", [p + "-icon"]),
            el("Number", "p", {"class": f"{b}__number"}, [p + "-number"], [text(n)]),
            el("Label", "p", {"class": f"{b}__label"}, [p + "-label"], [text(l)]),
        ]) for ic, (n, l) in zip(STAT_ICONS, STATS)]),
]), {**BASE,
    p: style(f".{b}", "padding-block: var(--section-space-m);\n  background-color: var(--main-light-alt);"),
    p + "-grid": style(f".{b}__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 22rem), 1fr));
  gap: var(--grid-gap);
  """ + LIST_RESET),
    p + "-card": style(f".{b}__card", """display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-xs);
  padding: var(--space-m);
  border-radius: var(--radius-l);
  background-color: var(--main-light);
  box-shadow: 0 0.4rem 1.2rem var(--main-shadow);"""),
    p + "-icon": style(f".{b}__icon", """inline-size: 4.8rem;
  block-size: 4.8rem;
  margin-block-end: var(--space-xs);
  padding: 1.1rem;
  border-radius: var(--radius-m);
  background-color: var(--main-primary);
  color: var(--main-on-primary);"""),
    p + "-number": style(f".{b}__number", "margin: 0;\n  font-size: var(--h2);\n  font-weight: 800;\n"
                                          "  line-height: 1.1;\n  color: var(--main-primary);"),
    p + "-label": style(f".{b}__label", "margin: 0;\n  color: var(--main-text-muted);"),
})

# ---------------------------------------------------------------- 3. heading left, 2×2 numbers right
p, b = "mn-sts", "main-stats-split"
outputs[b] = kit_payload(section("Stats Split", b, [p], [
    el("Grid", "div", {"class": f"{b}__grid"}, [p + "-grid"], [
        heading("Our results", "Numbers that speak for us",
                "A short line about your experience and the customers you have helped."),
        el("List", "ul", {"class": f"{b}__list"}, [p + "-list"], [
            el("Item", "li", {"class": f"{b}__item"}, [p + "-item"], [
                el("Number", "p", {"class": f"{b}__number"}, [p + "-number"], [text(n)]),
                el("Label", "p", {"class": f"{b}__label"}, [p + "-label"], [text(l)]),
            ]) for n, l in STATS]),
    ])]), {**BASE, **HEADING_STYLES,
    p: style(f".{b}", "background-color: var(--main-light);"),
    p + "-grid": style(f".{b}__grid", TWO_COL),
    p + "-list": style(f".{b}__list", """display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--grid-gap);
  """ + LIST_RESET),
    p + "-item": style(f".{b}__item", """display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  padding: var(--space-m);
  border-radius: var(--radius-m);
  background-color: var(--main-light-alt);

  &:nth-child(2),
  &:nth-child(3) {
    background-color: var(--main-primary);
    color: var(--main-on-primary);

    .main-stats-split__number {
      color: var(--main-accent);
    }

    .main-stats-split__label {
      color: var(--main-on-primary-muted);
    }
  }"""),
    p + "-number": style(f".{b}__number", "margin: 0;\n  font-size: var(--h1);\n  font-weight: 800;\n"
                                          "  line-height: 1;\n  color: var(--main-primary);"),
    p + "-label": style(f".{b}__label", "margin: 0;\n  color: var(--main-text-muted);"),
})

# ---------------------------------------------------------------- 4. numbers on a photo darkened with the primary colour
p, b = "mn-sti", "main-stats-image"
outputs[b] = kit_payload(el("Stats Image", "section", {**SEC, "class": b}, ["etch-section-style", p], [
    el("Background", "figure", {"class": f"{b}__bg"}, [p + "-bg"], [
        img("Background Image", {"class": f"{b}__img", "mediaId": "", "loading": "lazy"}, [p + "-img"])]),
    el("Container", "div", {**CON, "class": f"{b}__container"}, ["etch-container-style", p + "-container"], [
        heading("Our results", "Trusted by thousands of customers", center=True),
        el("Grid", "ul", {"class": f"{b}__grid"}, [p + "-grid"], [
            el("Item", "li", {"class": f"{b}__item"}, [p + "-item"], [
                el("Number", "p", {"class": f"{b}__number"}, [p + "-number"], [text(n)]),
                el("Label", "p", {"class": f"{b}__label"}, [p + "-label"], [text(l)]),
            ]) for n, l in STATS]),
    ]),
]), {**BASE, **HEADING_STYLES,
    p: style(f".{b}", """position: relative;
  isolation: isolate;
  overflow: hidden;
  color: var(--main-on-primary);

  /* overlay over the photo */
  &::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: -1;
    background-color: color-mix(in srgb, var(--main-primary) 82%, transparent);
  }

  """ + ON_DARK),
    p + "-container": style(f".{b}__container", "gap: var(--container-gap);"),
    p + "-bg": style(f".{b}__bg", "position: absolute;\n  inset: 0;\n  z-index: -2;\n  margin: 0;"),
    p + "-img": style(f".{b}__img", """display: block;
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
  background-color: var(--main-primary);"""),
    p + "-grid": style(f".{b}__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr));
  gap: var(--grid-gap);
  """ + LIST_RESET + """
  text-align: center;"""),
    p + "-item": style(f".{b}__item", """display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  padding: var(--space-m) var(--space-s);
  border: 1px solid var(--main-line-on-primary);
  border-radius: var(--radius-m);"""),
    p + "-number": style(f".{b}__number", "margin: 0;\n  font-size: var(--h1);\n  font-weight: 800;\n"
                                          "  line-height: 1;\n  color: var(--main-accent);"),
    p + "-label": style(f".{b}__label", "margin: 0;\n  color: var(--main-on-primary-muted);"),
})

# ================================================================================================ STEPS
STEP_TEXT = {"title": "margin: 0;\n  font-size: var(--h4);\n  color: var(--main-text);",
             "text": "margin: 0;\n  color: var(--main-text-muted);"}


def step_items(b, p, tag="li", body=False):
    def inner(t, d):
        kids = [el("Title", "h3", {"class": f"{b}__title"}, [p + "-title"], [text(t)]),
                el("Text", "p", {"class": f"{b}__text"}, [p + "-text"], [text(d)])]
        return [el("Body", "div", {"class": f"{b}__body"}, [p + "-body"], kids)] if body else kids
    return [el("Step", tag, {"class": f"{b}__item"}, [p + "-item"], inner(t, d)) for t, d in STEPS]


# ---------------------------------------------------------------- 1. horizontal timeline: circles on one line
p, b = "mn-sel", "main-steps-line"
outputs[b] = kit_payload(section("Steps Line", b, [p], [
    heading("How it works", "Four simple steps", "Explain what the customer can expect from start to finish.",
            center=True),
    el("List", "ol", {"class": f"{b}__list"}, [p + "-list"], step_items(b, p)),
], f"{b}__container", [p + "-container"]), {**BASE, **HEADING_STYLES,
    p: style(f".{b}", "background-color: var(--main-light);"),
    p + "-container": style(f".{b}__container", "gap: var(--container-gap);"),
    p + "-list": style(f".{b}__list", """display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--grid-gap);
  """ + LIST_RESET + """
  counter-reset: main-step-line;
  text-align: center;

  @media (width <= 768px) {
    grid-template-columns: 1fr;
  }"""),
    p + "-item": style(f".{b}__item", """position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-xs);
  counter-increment: main-step-line;

  &::before {
    content: counter(main-step-line);
    position: relative;
    z-index: 1;
    display: grid;
    place-items: center;
    inline-size: 6.4rem;
    block-size: 6.4rem;
    margin-block-end: var(--space-xs);
    border: 3px solid var(--main-accent);
    border-radius: 50%;
    background-color: var(--main-light);
    color: var(--main-primary);
    font-size: var(--h4);
    font-weight: 800;
  }

  /* the line joining this circle to the next one */
  &:not(:last-child)::after {
    content: "";
    position: absolute;
    inset-block-start: 3.2rem;
    inset-inline-start: 50%;
    inline-size: calc(100% + var(--grid-gap));
    border-block-start: 2px dashed var(--main-line);

    @media (width <= 768px) {
      display: none;
    }
  }"""),
    p + "-title": style(f".{b}__title", STEP_TEXT["title"]),
    p + "-text": style(f".{b}__text", STEP_TEXT["text"]),
})

# ---------------------------------------------------------------- 2. heading left, vertical timeline right
p, b = "mn-sev", "main-steps-vertical"
outputs[b] = kit_payload(section("Steps Vertical", b, [p], [
    el("Grid", "div", {"class": f"{b}__grid"}, [p + "-grid"], [
        el("Intro", "div", {"class": f"{b}__intro"}, [p + "-intro"], [
            heading("How it works", "Four simple steps",
                    "Explain what the customer can expect from start to finish."),
            buttons("Book now", "/contact/", "Our services", "/services/"),
        ]),
        el("List", "ol", {"class": f"{b}__list"}, [p + "-list"], step_items(b, p, body=True)),
    ])]), {**BASE, **HEADING_STYLES, **BUTTONS_STYLES,
    p: style(f".{b}", "background-color: var(--main-light-alt);"),
    p + "-grid": style(f".{b}__grid", """display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 3fr);
  gap: var(--container-gap);
  align-items: start;

  @media (width <= 992px) {
    grid-template-columns: 1fr;
  }"""),
    p + "-intro": style(f".{b}__intro", CONTENT),
    p + "-list": style(f".{b}__list", "display: flex;\n  flex-direction: column;\n  " + LIST_RESET +
                       "\n  counter-reset: main-step-vertical;"),
    p + "-item": style(f".{b}__item", """position: relative;
  display: flex;
  gap: var(--space-m);
  padding-block-end: var(--space-l);
  counter-increment: main-step-vertical;

  &::before {
    content: counter(main-step-vertical, decimal-leading-zero);
    flex: none;
    display: grid;
    place-items: center;
    inline-size: 5.6rem;
    block-size: 5.6rem;
    border-radius: 50%;
    background-color: var(--main-primary);
    color: var(--main-on-primary);
    font-size: var(--text-l);
    font-weight: 800;
  }

  /* the line down to the next step */
  &:not(:last-child)::after {
    content: "";
    position: absolute;
    inset-block: 5.6rem 0;
    inset-inline-start: 2.7rem;
    border-inline-start: 2px solid var(--main-line);
  }

  &:last-child {
    padding-block-end: 0;
  }"""),
    p + "-body": style(f".{b}__body", "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);\n"
                                      "  padding-block-start: 1.2rem;"),
    p + "-title": style(f".{b}__title", STEP_TEXT["title"]),
    p + "-text": style(f".{b}__text", STEP_TEXT["text"]),
})

# ---------------------------------------------------------------- 3. cards with a large faded number
p, b = "mn-sec", "main-steps-cards"
outputs[b] = kit_payload(section("Steps Cards", b, [p], [
    heading("How it works", "Four simple steps", "Explain what the customer can expect from start to finish."),
    el("List", "ol", {"class": f"{b}__list"}, [p + "-list"], step_items(b, p)),
], f"{b}__container", [p + "-container"]), {**BASE, **HEADING_STYLES,
    p: style(f".{b}", "background-color: var(--main-light);"),
    p + "-container": style(f".{b}__container", "gap: var(--container-gap);"),
    p + "-list": style(f".{b}__list", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 24rem), 1fr));
  gap: var(--grid-gap);
  """ + LIST_RESET + """
  counter-reset: main-step-card;"""),
    p + "-item": style(f".{b}__item", """position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  padding: 9.6rem var(--space-m) var(--space-m); /* room for the number */
  border-block-start: 4px solid var(--main-accent);
  border-radius: var(--radius-m);
  background-color: var(--main-light-alt);
  counter-increment: main-step-card;

  &::before {
    content: counter(main-step-card, decimal-leading-zero);
    position: absolute;
    inset-block-start: var(--space-xs);
    inset-inline-end: var(--space-s);
    font-size: 8rem;
    font-weight: 800;
    line-height: 1;
    color: var(--main-line);
  }"""),
    p + "-title": style(f".{b}__title", STEP_TEXT["title"]),
    p + "-text": style(f".{b}__text", STEP_TEXT["text"]),
})

# ---------------------------------------------------------------- 4. on the primary colour, arrows between the steps
p, b = "mn-seb", "main-steps-band"
outputs[b] = kit_payload(section("Steps Band", b, [p, "mn-band"], [
    heading("How it works", "Four simple steps", "Explain what the customer can expect from start to finish.",
            center=True),
    el("List", "ol", {"class": f"{b}__list"}, [p + "-list"], step_items(b, p)),
], f"{b}__container", [p + "-container"], extra=["main-band"]), {**BASE, **HEADING_STYLES, **BAND_STYLES,
    p: style(f".{b}", "padding-block: var(--section-space-m);"),
    p + "-container": style(f".{b}__container", "gap: var(--container-gap);"),
    p + "-list": style(f".{b}__list", """display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--space-xl);
  """ + LIST_RESET + """
  counter-reset: main-step-band;

  @media (width <= 992px) {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  @media (width <= 600px) {
    grid-template-columns: 1fr;
  }"""),
    p + "-item": style(f".{b}__item", """position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  counter-increment: main-step-band;

  &::before {
    content: "Step " counter(main-step-band);
    align-self: flex-start;
    padding: calc(var(--space-xs) / 2) var(--space-s);
    border-radius: var(--radius-circle, 999px);
    background-color: var(--main-accent);
    color: var(--main-on-primary);
    font-size: var(--text-s);
    font-weight: 700;
  }

  /* arrow pointing to the next step */
  &:not(:last-child)::after {
    content: "→";
    position: absolute;
    inset-block-start: 0;
    inset-inline-end: calc(var(--space-xl) / -2);
    translate: 50% 0;
    font-size: var(--h4);
    color: var(--main-accent);

    @media (width <= 992px) {
      display: none;
    }
  }"""),
    p + "-title": style(f".{b}__title", "margin: 0;\n  font-size: var(--h4);\n  color: inherit;"),
    p + "-text": style(f".{b}__text", "margin: 0;\n  color: var(--main-on-primary-muted);"),
})

# ================================================================================================ REVIEWS
# ---------------------------------------------------------------- 1. one big quote with a photo of the customer
p, b = "mn-rvf", "main-reviews-featured"
outputs[b] = kit_payload(section("Reviews Featured", b, [p], [
    el("Card", "figure", {"class": f"{b}__card"}, [p + "-card"], [
        svg("Quote icon", icon("quote"), f"{b}__icon", [p + "-icon"]),
        stars(f"{b}__stars", p + "-stars"),
        el("Quote", "blockquote", {"class": f"{b}__quote"}, [p + "-quote"], [el("Paragraph", "p", {}, None, [
            text("The best decision I made this year. The team was friendly, honest and the result was better "
                 "than I expected. I recommend them to everyone.")])]),
        el("Author", "figcaption", {"class": f"{b}__author"}, [p + "-author"], [
            img("Photo", {"class": f"{b}__photo", "mediaId": "", "loading": "lazy", "alt": ""}, [p + "-photo"]),
            el("Who", "span", {"class": f"{b}__who"}, [p + "-who"], [
                el("Name", "b", {"class": f"{b}__name"}, [p + "-name"], [text("Customer Name")]),
                el("Meta", "span", {"class": f"{b}__meta"}, [p + "-meta"], [text("Bangkok")]),
            ]),
        ]),
    ])]), {**BASE,
    p: style(f".{b}", "background-color: var(--main-light-alt);"),
    p + "-card": style(f".{b}__card", """display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-m);
  max-inline-size: 86rem;
  margin: 0 auto;
  text-align: center;"""),
    p + "-icon": style(f".{b}__icon", "inline-size: 6.4rem;\n  block-size: 6.4rem;\n  color: var(--main-accent);"),
    p + "-stars": style(f".{b}__stars", STARS_CSS),
    p + "-quote": style(f".{b}__quote", """margin: 0;
  padding: 0;
  border: 0;
  font-size: var(--h4);
  font-weight: 500;
  line-height: 1.5;
  color: var(--main-text);

  p {
    margin: 0;
  }"""),
    p + "-author": style(f".{b}__author", "display: flex;\n  align-items: center;\n  gap: var(--space-s);\n"
                                          "  text-align: start;"),
    p + "-photo": style(f".{b}__photo", """inline-size: 6.4rem;
  block-size: 6.4rem;
  border-radius: 50%;
  background-color: var(--main-line);
  object-fit: cover;"""),
    p + "-who": style(f".{b}__who", "display: flex;\n  flex-direction: column;"),
    p + "-name": style(f".{b}__name", "font-weight: 700;\n  color: var(--main-primary);"),
    p + "-meta": style(f".{b}__meta", "font-size: var(--text-s);\n  color: var(--main-text-muted);"),
})

# ---------------------------------------------------------------- 2. three quotes on the primary colour
p, b = "mn-rvb", "main-reviews-band"
outputs[b] = kit_payload(section("Reviews Band", b, [p, "mn-band"], [
    heading("Reviews", "What our customers say", center=True),
    el("Grid", "ul", {"class": f"{b}__grid"}, [p + "-grid"], [
        el("Review", "li", {"class": f"{b}__item"}, [p + "-item"], [
            stars(f"{b}__stars", p + "-stars"),
            el("Text", "blockquote", {"class": f"{b}__text"}, [p + "-text"], [
                el("Paragraph", "p", {}, None, [text(REVIEW)])]),
            el("Author", "div", {"class": f"{b}__author"}, [p + "-author"], [
                el("Name", "p", {"class": f"{b}__name"}, [p + "-name"], [text("Customer Name")]),
                el("Meta", "p", {"class": f"{b}__meta"}, [p + "-meta"], [text(place)]),
            ]),
        ]) for place in PLACES[:3]]),
], f"{b}__container", [p + "-container"], extra=["main-band"]), {**BASE, **HEADING_STYLES, **BAND_STYLES,
    p: style(f".{b}", "padding-block: var(--section-space-m);"),
    p + "-container": style(f".{b}__container", "gap: var(--container-gap);"),
    p + "-grid": style(f".{b}__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 28rem), 1fr));
  gap: var(--grid-gap);
  """ + LIST_RESET),
    p + "-item": style(f".{b}__item", """display: flex;
  flex-direction: column;
  gap: var(--space-s);
  padding: var(--space-m);
  border: 1px solid var(--main-line-on-primary);
  border-radius: var(--radius-m);"""),
    p + "-stars": style(f".{b}__stars", STARS_CSS),
    p + "-text": style(f".{b}__text", "margin: 0;\n  padding: 0;\n  border: 0;\n  color: inherit;\n\n  p {\n    margin: 0;\n  }"),
    p + "-author": style(f".{b}__author", """margin-block-start: auto;
  padding-block-start: var(--space-s);
  border-block-start: 1px solid var(--main-line-on-primary);"""),
    p + "-name": style(f".{b}__name", "margin: 0;\n  font-weight: 700;\n  color: var(--main-accent);"),
    p + "-meta": style(f".{b}__meta", "margin: 0;\n  font-size: var(--text-s);\n"
                                      "  color: var(--main-on-primary-muted);"),
})

# ---------------------------------------------------------------- 3. rating summary left, four reviews right
p, b = "mn-rvs", "main-reviews-split"
outputs[b] = kit_payload(section("Reviews Split", b, [p], [
    el("Grid", "div", {"class": f"{b}__grid"}, [p + "-grid"], [
        el("Summary", "div", {"class": f"{b}__summary"}, [p + "-summary"], [
            heading("Reviews", "What our customers say"),
            el("Score", "div", {"class": f"{b}__score"}, [p + "-score"], [
                el("Value", "b", {"class": f"{b}__value"}, [p + "-value"], [text("4.9")]),
                el("Score Text", "span", {"class": f"{b}__score-text"}, [p + "-score-text"], [
                    stars(f"{b}__stars", p + "-stars"),
                    el("Count", "span", {"class": f"{b}__count"}, [p + "-count"],
                       [text("From 200+ Google reviews")]),
                ]),
            ]),
        ]),
        el("List", "ul", {"class": f"{b}__list"}, [p + "-list"], [
            el("Review", "li", {"class": f"{b}__item"}, [p + "-item"], [
                el("Text", "blockquote", {"class": f"{b}__text"}, [p + "-text"], [
                    el("Paragraph", "p", {}, None, [text(REVIEW)])]),
                el("Name", "p", {"class": f"{b}__name"}, [p + "-name"], [text("Customer Name · " + place)]),
            ]) for place in PLACES]),
    ])]), {**BASE, **HEADING_STYLES,
    p: style(f".{b}", "background-color: var(--main-light);"),
    p + "-grid": style(f".{b}__grid", """display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 2fr);
  gap: var(--container-gap);
  align-items: start;

  @media (width <= 992px) {
    grid-template-columns: 1fr;
  }"""),
    p + "-summary": style(f".{b}__summary", "display: flex;\n  flex-direction: column;\n  gap: var(--space-l);"),
    p + "-score": style(f".{b}__score", """display: flex;
  align-items: center;
  gap: var(--space-s);
  padding: var(--space-m);
  border-radius: var(--radius-m);
  background-color: var(--main-primary);
  color: var(--main-on-primary);"""),
    p + "-value": style(f".{b}__value", "font-size: var(--h1);\n  font-weight: 800;\n  line-height: 1;"),
    p + "-score-text": style(f".{b}__score-text", "display: flex;\n  flex-direction: column;\n"
                                                  "  gap: calc(var(--space-xs) / 2);"),
    p + "-stars": style(f".{b}__stars", STARS_CSS),
    p + "-count": style(f".{b}__count", "font-size: var(--text-s);\n  color: var(--main-on-primary-muted);"),
    p + "-list": style(f".{b}__list", """display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--grid-gap);
  """ + LIST_RESET + """

  @media (width <= 600px) {
    grid-template-columns: 1fr;
  }"""),
    p + "-item": style(f".{b}__item", """display: flex;
  flex-direction: column;
  gap: var(--space-s);
  padding: var(--space-m);
  border-radius: var(--radius-m);
  background-color: var(--main-light-alt);"""),
    p + "-text": style(f".{b}__text", "margin: 0;\n  padding: 0;\n  border: 0;\n  color: var(--main-text);\n\n  p {\n    margin: 0;\n  }"),
    p + "-name": style(f".{b}__name", "margin: 0;\n  margin-block-start: auto;\n  font-weight: 700;\n"
                                      "  color: var(--main-primary);"),
})

for name, payload in outputs.items():
    write(f"{OUT}/{name}.etch.txt", payload)
    print("ok", name, len(payload["styles"]), "styles", len(json.dumps(payload)) // 1024, "KB")
