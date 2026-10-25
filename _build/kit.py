"""Shared pieces of the main-* template kit: colours, base Etch styles, icons, heading, social links, post card.

Every template file carries the styles it uses from here, so all files paste the same CSS for the same selector
(Etch keeps one style per selector, the first paste wins)."""
from icons import ICONS
from lib_etch import el, text, svg, img, cond, loop, style, prop, data_uri

# ================================================================ colours — the only place colours are defined
COLORS_CSS = """/* ===== MAIN TEMPLATE COLOURS — change colours here only =====
     Header, footer and every main-* section use these variables.
     By default they follow ACSS: changing Primary / Secondary in ACSS changes the templates too. */
  --main-primary: var(--primary, #1e3a5f);    /* brand: header, footer, FAQ, headings, links, tags */
  --main-accent: var(--secondary, #e8a33d);   /* highlight: underlines, hover, eyebrow line, active */
  --main-light: var(--white, #fff);           /* light backgrounds: sections, cards, article box */
  --main-text: var(--text-dark, #1a1a1a);     /* text on light backgrounds */
  --main-on-primary: var(--white, #fff);      /* text and icons on the primary colour */

  /* derived from the five colours above — no need to edit */
  --main-light-alt: color-mix(in srgb, var(--main-primary) 6%, var(--main-light));
  --main-text-muted: color-mix(in srgb, var(--main-text) 72%, transparent);
  --main-on-primary-muted: color-mix(in srgb, var(--main-on-primary) 78%, transparent);
  --main-line: color-mix(in srgb, var(--main-primary) 18%, transparent);
  --main-line-on-primary: color-mix(in srgb, var(--main-on-primary) 18%, transparent);
  --main-accent-soft: color-mix(in srgb, var(--main-accent) 20%, var(--main-light));
  --main-shadow: color-mix(in srgb, var(--main-text) 12%, transparent);"""

COLORS = {"main-colors": style(":where(:root)", COLORS_CSS, "custom")}

# ================================================================ Etch base element styles (identical on every site)
BASE = {
    "etch-section-style": {"type": "element", "selector": ':where([data-etch-element="section"])',
                           "collection": "default",
                           "css": "inline-size: 100%;\n  display: flex;\n  flex-direction: column;\n"
                                  "  align-items: center;"},
    "etch-container-style": {"type": "element", "selector": ':where([data-etch-element="container"])',
                             "collection": "default",
                             "css": "inline-size: 100%;\n  display: flex;\n  flex-direction: column;\n"
                                    "  max-inline-size: var(--content-width, 1366px);\n  align-self: center; "
                                    "margin-inline: auto;"},
}
SEC = {"data-etch-element": "section"}
CON = {"data-etch-element": "container"}


def icon(name):
    return data_uri(ICONS[name])


# ================================================================ section heading (eyebrow / title / intro)
HEADING_STYLES = {
    "mn-heading": style(".main-heading", "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);\n"
                                         "  max-inline-size: 60rem;"),
    "mn-heading-center": style(".main-heading--center", "align-items: center;\n  margin-inline: auto;\n"
                                                        "  text-align: center;"),
    "mn-eyebrow": style(".main-heading__eyebrow", """display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-size: var(--text-s);
  font-weight: 600;
  letter-spacing: 0.08em;
  color: var(--main-primary);

  &::before {
    content: "";
    inline-size: 2.4rem;
    block-size: 2px;
    background-color: var(--main-accent);
  }"""),
    "mn-intro": style(".main-heading__intro", "color: var(--main-text-muted);"),
}


def heading(eyebrow, title, intro=None, tag="h2", center=False):
    cls, ids = "main-heading", ["mn-heading"]
    if center:
        cls, ids = cls + " main-heading--center", ids + ["mn-heading-center"]
    kids = []
    if eyebrow is not None:
        kids.append(el("Eyebrow", "p", {"class": "main-heading__eyebrow"}, ["mn-eyebrow"], [text(eyebrow)]))
    kids.append(el("Title", tag, {}, None, [text(title)]))
    if intro is not None:
        kids.append(el("Intro", "p", {"class": "main-heading__intro"}, ["mn-intro"], [text(intro)]))
    return el("Heading", "div", {"class": cls}, ids, kids)


# ================================================================ brand band: a section on the primary colour
BAND_STYLES = {
    "mn-band": style(".main-band", """background-color: var(--main-primary);
  color: var(--main-on-primary);

  :is(h1, h2, h3, h4, h5, h6),
  .main-heading__eyebrow {
    color: inherit;
  }

  .main-heading__intro {
    color: var(--main-on-primary-muted);
  }"""),
}

# ================================================================ social icons (shared by footer, CTA, contact, share)
SOCIAL_STYLES = {
    "mn-social": style(".main-social", "display: flex;\n  flex-wrap: wrap;\n  align-items: center;\n"
                                       "  gap: var(--space-xs);\n  margin: 0;\n  padding: 0;\n  list-style: none;"),
    "mn-social-link": style(".main-social__link", """/* colour of the ring + icon; the footer sets --main-social-color */
  display: grid;
  place-items: center;
  inline-size: 4.4rem;
  block-size: 4.4rem;
  border: 1.5px solid currentColor;
  border-radius: 50%;
  color: var(--main-social-color, var(--main-primary));
  transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;

  &:hover,
  &:focus-visible {
    background-color: var(--main-accent);
    border-color: var(--main-accent);
    color: var(--main-on-primary);
  }

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }"""),
    "mn-social-icon": style(".main-social__icon", "display: block;\n  inline-size: 2rem;\n  block-size: 2rem;"),
}
SOCIALS = (("line", "LINE"), ("facebook", "Facebook"), ("instagram", "Instagram"), ("tiktok", "TikTok"),
           ("youtube", "YouTube"))
SOCIAL_PROPS = [
    prop("LINE URL", "lineUrl", "https://line.me/R/ti/p/@example", "Empty = hidden"),
    prop("Facebook URL", "facebookUrl", "https://facebook.com/", "Empty = hidden"),
    prop("Instagram URL", "instagramUrl", "https://instagram.com/", "Empty = hidden"),
    prop("TikTok URL", "tiktokUrl", "", "Empty = hidden"),
    prop("YouTube URL", "youtubeUrl", "", "Empty = hidden"),
]


def social_link(name, href, icon_name, label, blank=True):
    a = {"class": "main-social__link", "href": href, "aria-label": label}
    if blank:
        a.update({"target": "_blank", "rel": "noopener"})
    return el(name, "a", a, ["mn-social-link"], [svg(f"{name} icon", icon(icon_name), "main-social__icon",
                                                     ["mn-social-icon"])])


def social_list(label="Social media"):
    """<ul> of social links driven by the component props lineUrl, facebookUrl … (empty prop = hidden)."""
    items = [cond(f"If {name}", f"props.{key}Url", el("Item", "li", {}, None, [
        social_link(name, f"{{props.{key}Url}}", key, name)])) for key, name in SOCIALS]
    return el("Social", "ul", {"class": "main-social", "aria-label": label}, ["mn-social"], items)


# ================================================================ post card (blog archive + related posts)
CARD_STYLES = {
    "mn-card-grid": style(".main-card-grid", """display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--grid-gap);
  inline-size: 100%;
  margin: 0;
  padding: 0;
  list-style: none;

  @media (width <= 992px) {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  @media (width <= 768px) {
    grid-template-columns: 1fr;
  }"""),
    "mn-card": style(".main-card", """position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: var(--radius-l);
  background-color: var(--main-light);
  box-shadow: 0 0.4rem 1.2rem var(--main-shadow);
  transition: box-shadow 0.25s ease, translate 0.25s ease;

  &:hover {
    translate: 0 -3px;
    box-shadow: 0 1.2rem 2.8rem var(--main-shadow);
  }

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }"""),
    "mn-card-media": style(".main-card__media", "margin: 0;"),
    "mn-card-img": style(".main-card__img", "inline-size: 100%;\n  block-size: auto;\n  aspect-ratio: 6 / 5;\n"
                                            "  object-fit: cover;"),
    "mn-card-body": style(".main-card__body", "display: flex;\n  flex: 1;\n  flex-direction: column;\n"
                                              "  gap: var(--space-xs);\n"
                                              "  padding: var(--space-s) var(--space-m) var(--space-m);"),
    "mn-pill": style(".main-pill", """align-self: flex-start;
  padding: calc(var(--space-xs) / 2) var(--space-s);
  border-radius: var(--radius-circle, 999px);
  background-color: var(--main-primary);
  color: var(--main-on-primary);
  font-size: var(--text-xs);
  font-weight: 500;
  line-height: 1.6;"""),
    "mn-card-title": style(".main-card__title", "font-size: var(--h5);\n  font-weight: 700;\n  line-height: 1.45;\n"
                                                "  color: var(--main-text);"),
    "mn-card-link": style(".main-card__link", "color: inherit;\n  text-decoration: none;"),
    "acss-clickable-parent": style(".clickable-parent", ""),
    "mn-card-excerpt": style(".main-card__excerpt", """display: -webkit-box;
  overflow: hidden;
  font-size: var(--text-s);
  color: var(--main-text-muted);
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;"""),
    "mn-card-more": style(".main-card__more", """margin-block-start: auto;
  padding-block-start: var(--space-xs);
  font-size: var(--text-s);
  font-weight: 700;
  color: var(--main-primary);"""),
}


def card(item, title_tag="h2"):
    return el("Card", "li", {"class": "main-card"}, ["mn-card"], [
        cond("If image", f"{item}.image.id", el("Media", "figure", {"class": "main-card__media"}, ["mn-card-media"], [
            img("Image", {"class": "main-card__img", "mediaId": f"{{{item}.image.id}}", "loading": "lazy"},
                ["mn-card-img"])])),
        el("Body", "div", {"class": "main-card__body"}, ["mn-card-body"], [
            loop("Categories", "cat", [el("Pill", "span", {"class": "main-pill"}, ["mn-pill"], [text("{cat.name}")])],
                 target=f"{item}.categories"),
            el("Title", title_tag, {"class": "main-card__title"}, ["mn-card-title"], [
                el("Link", "a", {"class": "main-card__link clickable-parent", "href": f"{{{item}.permalink.relative}}"},
                   ["mn-card-link", "acss-clickable-parent"], [text(f"{{{item}.title}}")])]),
            cond("If excerpt", f"{item}.excerpt", el("Excerpt", "p", {"class": "main-card__excerpt"},
                                                     ["mn-card-excerpt"], [text(f"{{{item}.excerpt}}")])),
            el("More", "span", {"class": "main-card__more", "aria-hidden": "true"}, ["mn-card-more"],
               [text("Read more →")]),
        ]),
    ])


# ================================================================ image placeholder (empty dynamic image shows a tinted box)
MEDIA_STYLES = {
    "mn-media-img": style(".main-media__img", """/* image ratio: set --main-media-ratio on a parent */
  display: block;
  inline-size: 100%;
  block-size: auto;
  aspect-ratio: var(--main-media-ratio, 4 / 3);
  border-radius: var(--radius-m);
  background-color: var(--main-light-alt);
  object-fit: cover;"""),
}


def media_img(name="Image", eager=False):
    a = {"class": "main-media__img", "mediaId": "", "loading": "eager" if eager else "lazy"}
    return img(name, a, ["mn-media-img"])


def kit_payload(gblock, styles, components=None, loops=None):
    """Every template file carries the colour variables, so whichever file is pasted first creates them."""
    from lib_etch import payload
    return payload(gblock, {**COLORS, **styles}, components, loops)


# ================================================================ button row + check list (hero, split, 404 …)
BUTTONS_STYLES = {
    "mn-buttons": style(".main-buttons", "display: flex;\n  flex-wrap: wrap;\n  align-items: center;\n"
                                         "  gap: var(--space-s);"),
}


def buttons(primary_label, primary_href, outline_label, outline_href):
    """ACSS buttons carry no style record of their own, so their btn--* classes survive the paste."""
    return el("Buttons", "div", {"class": "main-buttons"}, ["mn-buttons"], [
        el("Primary", "a", {"class": "btn--primary", "href": primary_href}, None, [text(primary_label)]),
        el("Secondary", "a", {"class": "btn--primary btn--outline", "href": outline_href}, None, [text(outline_label)]),
    ])


CHECKS_STYLES = {
    "mn-checks": style(".main-checks", "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);\n"
                                       "  margin: 0;\n  padding: 0;\n  list-style: none;"),
    "mn-checks-item": style(".main-checks__item", "display: flex;\n  align-items: flex-start;\n"
                                                  "  gap: var(--space-xs);"),
    "mn-checks-icon": style(".main-checks__icon", """flex: none;
  inline-size: 2.4rem;
  block-size: 2.4rem;
  padding: calc(var(--space-xs) / 2);
  border-radius: 50%;
  background-color: var(--main-accent-soft);
  color: var(--main-primary);"""),
}


def checks(items):
    return el("Checks", "ul", {"class": "main-checks"}, ["mn-checks"], [
        el("Item", "li", {"class": "main-checks__item"}, ["mn-checks-item"], [
            svg("Check icon", icon("check"), "main-checks__icon", ["mn-checks-icon"]),
            el("Text", "span", {}, None, [text(t)])]) for t in items])
