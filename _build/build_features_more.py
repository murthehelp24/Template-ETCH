"""Features variants: image + list, numbered grid, brand band, image cards, heading + list.
Plain sections (edit the text in the blocks); colours come from kit.COLORS. Lengths in rem are written for
1rem = 10px and become to-rem() (lib_etch.portable).

    python3 build_features_more.py <src> <kit>/etch-sections
"""
import json, os, sys
from lib_etch import el, text, svg, style, write
from kit import (SEC, CON, BASE, HEADING_STYLES, MEDIA_STYLES, BUTTONS_STYLES, heading, buttons, media_img, icon,
                 kit_payload)

OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
outputs = {}
TEXT = "One or two lines about this benefit or service."
FOUR = [("shield", "Trusted & safe"), ("users", "Expert team"), ("heart", "Personal care"), ("award", "Proven results")]


def section(name, cls, style_ids, children):
    return el(name, "section", {**SEC, "class": cls}, ["etch-section-style", *style_ids], [
        el("Container", "div", CON, ["etch-container-style"], children)])


ITEM_TEXT = {  # shared title / text look inside every variant
    "title": "font-size: var(--h4);\n  color: var(--main-text);",
    "text": "margin: 0;\n  color: var(--main-text-muted);",
}

# ================================================================ 1. image + 2×2 icon list
p, b = "mn-fi", "main-features-image"
image_styles = {**BASE, **HEADING_STYLES, **MEDIA_STYLES,
    p: style(f".{b}", "background-color: var(--main-light);"),
    p + "-grid": style(f".{b}__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 40rem), 1fr));
  gap: var(--container-gap);
  align-items: center;"""),
    p + "-media": style(f".{b}__media", "--main-media-ratio: 4 / 5;\n  margin: 0;"),
    p + "-content": style(f".{b}__content", "display: flex;\n  flex-direction: column;\n  gap: var(--space-l);"),
    p + "-list": style(f".{b}__list", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 22rem), 1fr));
  gap: var(--space-l) var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;"""),
    p + "-item": style(f".{b}__item", "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);"),
    p + "-icon": style(f".{b}__icon", """inline-size: 4.8rem;
  block-size: 4.8rem;
  padding: 1.1rem;
  border-radius: 50%;
  background-color: var(--main-accent-soft);
  color: var(--main-primary);"""),
    p + "-title": style(f".{b}__title", ITEM_TEXT["title"]),
    p + "-text": style(f".{b}__text", ITEM_TEXT["text"]),
}
outputs[b] = kit_payload(section("Features Image", b, [p], [
    el("Grid", "div", {"class": f"{b}__grid"}, [p + "-grid"], [
        el("Media", "figure", {"class": f"{b}__media"}, [p + "-media"], [media_img()]),
        el("Content", "div", {"class": f"{b}__content"}, [p + "-content"], [
            heading("Why choose us", "What we offer", "A short line that introduces your services or main benefits."),
            el("List", "ul", {"class": f"{b}__list"}, [p + "-list"], [
                el("Item", "li", {"class": f"{b}__item"}, [p + "-item"], [
                    svg("Icon", icon(ic), f"{b}__icon", [p + "-icon"]),
                    el("Title", "h3", {"class": f"{b}__title"}, [p + "-title"], [text(t)]),
                    el("Text", "p", {"class": f"{b}__text"}, [p + "-text"], [text(TEXT)]),
                ]) for ic, t in FOUR]),
        ]),
    ])]), image_styles)

# ================================================================ 2. six numbered points, no icons
p, b = "mn-fn", "main-features-numbered"
SIX = ["Trusted & safe", "Expert team", "Personal care", "Proven results", "Clear pricing", "Easy booking"]
numbered_styles = {**BASE, **HEADING_STYLES,
    p: style(f".{b}", "background-color: var(--main-light-alt);"),
    p + "-container": style(f".{b}__container", "gap: var(--container-gap);"),
    p + "-grid": style(f".{b}__grid", """display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-l) var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;
  counter-reset: main-feature;

  @media (width <= 992px) {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  @media (width <= 600px) {
    grid-template-columns: 1fr;
  }"""),
    p + "-item": style(f".{b}__item", """display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  padding-block-start: var(--space-s);
  border-block-start: 2px solid var(--main-line);
  counter-increment: main-feature;

  /* 01, 02 … numbered automatically */
  &::before {
    content: counter(main-feature, decimal-leading-zero);
    font-size: var(--h2);
    font-weight: 800;
    line-height: 1;
    color: var(--main-accent);
  }"""),
    p + "-title": style(f".{b}__title", ITEM_TEXT["title"]),
    p + "-text": style(f".{b}__text", ITEM_TEXT["text"]),
}
outputs[b] = kit_payload(el("Features Numbered", "section", {**SEC, "class": b}, ["etch-section-style", p], [
    el("Container", "div", {**CON, "class": f"{b}__container"}, ["etch-container-style", p + "-container"], [
        heading("Why choose us", "Six reasons to choose us", "A short line that introduces your main benefits."),
        el("Grid", "ol", {"class": f"{b}__grid"}, [p + "-grid"], [
            el("Item", "li", {"class": f"{b}__item"}, [p + "-item"], [
                el("Title", "h3", {"class": f"{b}__title"}, [p + "-title"], [text(t)]),
                el("Text", "p", {"class": f"{b}__text"}, [p + "-text"], [text(TEXT)]),
            ]) for t in SIX]),
    ])]), numbered_styles)

# ================================================================ 3. on the primary colour, round icons
p, b = "mn-fb", "main-features-band"
band_styles = {**BASE, **HEADING_STYLES,
    p: style(f".{b}", """background-color: var(--main-primary);
  color: var(--main-on-primary);

  :is(h1, h2, h3, h4, h5, h6),
  .main-heading__eyebrow {
    color: inherit;
  }

  .main-heading__intro {
    color: var(--main-on-primary-muted);
  }"""),
    p + "-container": style(f".{b}__container", "gap: var(--container-gap);"),
    p + "-grid": style(f".{b}__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 22rem), 1fr));
  gap: var(--space-l) var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;
  text-align: center;"""),
    p + "-item": style(f".{b}__item", "display: flex;\n  flex-direction: column;\n  align-items: center;\n"
                                      "  gap: var(--space-xs);"),
    p + "-icon": style(f".{b}__icon", """inline-size: 7.2rem;
  block-size: 7.2rem;
  margin-block-end: var(--space-xs);
  padding: 1.8rem;
  border-radius: 50%;
  background-color: var(--main-accent);
  color: var(--main-on-primary);"""),
    p + "-title": style(f".{b}__title", "font-size: var(--h4);\n  color: inherit;"),
    p + "-text": style(f".{b}__text", "margin: 0;\n  color: var(--main-on-primary-muted);"),
}
outputs[b] = kit_payload(el("Features Band", "section", {**SEC, "class": b}, ["etch-section-style", p], [
    el("Container", "div", {**CON, "class": f"{b}__container"}, ["etch-container-style", p + "-container"], [
        heading("Why choose us", "What we offer", "A short line that introduces your services or main benefits.",
                center=True),
        el("Grid", "ul", {"class": f"{b}__grid"}, [p + "-grid"], [
            el("Item", "li", {"class": f"{b}__item"}, [p + "-item"], [
                svg("Icon", icon(ic), f"{b}__icon", [p + "-icon"]),
                el("Title", "h3", {"class": f"{b}__title"}, [p + "-title"], [text(t)]),
                el("Text", "p", {"class": f"{b}__text"}, [p + "-text"], [text(TEXT)]),
            ]) for ic, t in FOUR]),
    ])]), band_styles)

# ================================================================ 4. three cards with a photo each (services)
p, b = "mn-fc", "main-features-cards"
cards_styles = {**BASE, **HEADING_STYLES, **MEDIA_STYLES,
    p: style(f".{b}", "background-color: var(--main-light);"),
    p + "-container": style(f".{b}__container", "gap: var(--container-gap);"),
    p + "-grid": style(f".{b}__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 28rem), 1fr));
  gap: var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;"""),
    p + "-card": style(f".{b}__card", """position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: var(--radius-l);
  background-color: var(--main-light);
  box-shadow: 0 0.4rem 1.2rem var(--main-shadow);
  transition: box-shadow 0.25s ease, translate 0.25s ease;

  --main-media-ratio: 3 / 2;

  .main-media__img {
    border-radius: 0;
  }

  &:hover {
    translate: 0 -3px;
    box-shadow: 0 1.2rem 2.8rem var(--main-shadow);
  }

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }"""),
    p + "-body": style(f".{b}__body", "display: flex;\n  flex: 1;\n  flex-direction: column;\n"
                                      "  gap: var(--space-xs);\n  padding: var(--space-m);"),
    p + "-title": style(f".{b}__title", ITEM_TEXT["title"]),
    p + "-text": style(f".{b}__text", ITEM_TEXT["text"]),
    p + "-link": style(f".{b}__link", """margin-block-start: auto;
  padding-block-start: var(--space-xs);
  font-weight: 700;
  color: var(--main-primary);
  text-decoration: none;

  /* the whole card is clickable */
  &::after {
    content: "";
    position: absolute;
    inset: 0;
  }

  &:hover {
    text-decoration: underline;
    text-decoration-color: var(--main-accent);
  }"""),
}
outputs[b] = kit_payload(el("Features Cards", "section", {**SEC, "class": b}, ["etch-section-style", p], [
    el("Container", "div", {**CON, "class": f"{b}__container"}, ["etch-container-style", p + "-container"], [
        heading("Our services", "What we offer", "A short line that introduces your services.", center=True),
        el("Grid", "ul", {"class": f"{b}__grid"}, [p + "-grid"], [
            el("Card", "li", {"class": f"{b}__card"}, [p + "-card"], [
                media_img(),
                el("Body", "div", {"class": f"{b}__body"}, [p + "-body"], [
                    el("Title", "h3", {"class": f"{b}__title"}, [p + "-title"], [text(f"Service {n}")]),
                    el("Text", "p", {"class": f"{b}__text"}, [p + "-text"], [text(TEXT)]),
                    el("Link", "a", {"class": f"{b}__link", "href": f"/services/service-{n}/"}, [p + "-link"],
                       [text("Learn more →")]),
                ]),
            ]) for n in (1, 2, 3)]),
    ])]), cards_styles)

# ================================================================ 5. heading + button on the left, icon rows on the right
p, b = "mn-fl", "main-features-list"
list_styles = {**BASE, **HEADING_STYLES, **BUTTONS_STYLES,
    p: style(f".{b}", "background-color: var(--main-light);"),
    p + "-grid": style(f".{b}__grid", """display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 3fr);
  gap: var(--container-gap);
  align-items: start;

  @media (width <= 992px) {
    grid-template-columns: 1fr;
  }"""),
    p + "-intro": style(f".{b}__intro", """position: sticky;
  inset-block-start: var(--space-xl);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--content-gap);

  @media (width <= 992px) {
    position: static;
  }"""),
    p + "-list": style(f".{b}__list", "display: flex;\n  flex-direction: column;\n  margin: 0;\n  padding: 0;\n"
                                      "  list-style: none;"),
    p + "-item": style(f".{b}__item", """display: flex;
  align-items: flex-start;
  gap: var(--space-m);
  padding-block: var(--space-m);
  border-block-end: 1px solid var(--main-line);

  &:first-child {
    padding-block-start: 0;
  }"""),
    p + "-icon": style(f".{b}__icon", """flex: none;
  inline-size: 5.6rem;
  block-size: 5.6rem;
  padding: 1.4rem;
  border-radius: var(--radius-m);
  background-color: var(--main-accent-soft);
  color: var(--main-primary);"""),
    p + "-body": style(f".{b}__body", "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);"),
    p + "-title": style(f".{b}__title", ITEM_TEXT["title"]),
    p + "-text": style(f".{b}__text", ITEM_TEXT["text"]),
}
outputs[b] = kit_payload(section("Features List", b, [p], [
    el("Grid", "div", {"class": f"{b}__grid"}, [p + "-grid"], [
        el("Intro", "div", {"class": f"{b}__intro"}, [p + "-intro"], [
            heading("Why choose us", "What we offer", "A short line that introduces your services or main benefits."),
            buttons("Our services", "/services/", "Contact us", "/contact/"),
        ]),
        el("List", "ul", {"class": f"{b}__list"}, [p + "-list"], [
            el("Item", "li", {"class": f"{b}__item"}, [p + "-item"], [
                svg("Icon", icon(ic), f"{b}__icon", [p + "-icon"]),
                el("Body", "div", {"class": f"{b}__body"}, [p + "-body"], [
                    el("Title", "h3", {"class": f"{b}__title"}, [p + "-title"], [text(t)]),
                    el("Text", "p", {"class": f"{b}__text"}, [p + "-text"], [text(TEXT)]),
                ]),
            ]) for ic, t in FOUR]),
    ])]), list_styles)

for name, payload in outputs.items():
    write(f"{OUT}/{name}.etch.txt", payload)
    print("ok", name, len(payload["styles"]), "styles", len(json.dumps(payload)) // 1024, "KB")
