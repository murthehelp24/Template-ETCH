"""Second batch of main-* sections: hero, page hero, features, split, stats, steps, reviews, 404.
Plain sections (edit the text in the blocks); colours come from kit.COLORS."""
import json, os, sys
from lib_etch import el, text, svg, cond, style, write
from kit import (SEC, CON, BASE, HEADING_STYLES, BAND_STYLES, MEDIA_STYLES, BUTTONS_STYLES, CHECKS_STYLES, heading,
                 buttons, checks, media_img, icon, kit_payload)

OUT = sys.argv[2]
os.makedirs(OUT, exist_ok=True)
outputs = {}


def section(name, block, extra_cls, styles_ids, children, container_cls=None, container_ids=()):
    con_attrs = {**CON, "class": container_cls} if container_cls else CON
    return el(name, "section", {**SEC, "class": " ".join([block, *extra_cls])}, ["etch-section-style", *styles_ids], [
        el("Container", "div", con_attrs, ["etch-container-style", *container_ids], children)])


# ================================================================ 1. Hero (home page)
hero_styles = {**BASE, **HEADING_STYLES, **MEDIA_STYLES, **BUTTONS_STYLES, **CHECKS_STYLES,
    "mn-hero": style(".main-hero", "padding-block: var(--section-space-l);\n"
                                   "  background-color: var(--main-light-alt);"),
    "mn-hero-grid": style(".main-hero__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 40rem), 1fr));
  gap: var(--container-gap);
  align-items: center;"""),
    "mn-hero-content": style(".main-hero__content", """display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--content-gap);"""),
    "mn-hero-media": style(".main-hero__media", "--main-media-ratio: 5 / 4;\n  margin: 0;"),
}
hero = section("Hero", "main-hero", [], ["mn-hero"], [
    el("Grid", "div", {"class": "main-hero__grid"}, ["mn-hero-grid"], [
        el("Content", "div", {"class": "main-hero__content"}, ["mn-hero-content"], [
            heading("Welcome", "A clear headline that says what you do and for whom",
                    "One or two sentences about the main benefit. Keep it short and specific.", tag="h1"),
            buttons("Book now", "/contact/", "Our services", "/services/"),
            checks(["Short trust point", "Another reason to choose you", "Free consultation"]),
        ]),
        el("Media", "figure", {"class": "main-hero__media"}, ["mn-hero-media"], [media_img(eager=True)]),
    ])])
outputs["main-hero"] = kit_payload(hero, hero_styles)

# ================================================================ 2. Page hero (inner pages, breadcrumb)
page_hero_styles = {**BASE, **BAND_STYLES,
    "mn-page-hero": style(".main-page-hero", "padding-block: var(--section-space-m);"),
    "mn-page-hero-container": style(".main-page-hero__container", "align-items: center;\n"
                                                                  "  gap: var(--space-s);\n  text-align: center;"),
    "mn-breadcrumb": style(".main-breadcrumb", """font-size: var(--text-s);

  ol {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: var(--space-xs);
    margin: 0;
    padding: 0;
    list-style: none;
  }

  li:not(:last-child)::after {
    content: "/";
    margin-inline-start: var(--space-xs);
    opacity: 0.6;
  }

  a {
    color: inherit;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
      text-decoration-color: var(--main-accent);
    }
  }

  [aria-current] {
    opacity: 0.8;
  }"""),
    "mn-page-hero-intro": style(".main-page-hero__intro", "max-inline-size: 60rem;"),
}
page_hero = section("Page Hero", "main-page-hero", ["main-band"], ["mn-page-hero", "mn-band"], [
    el("Breadcrumb", "nav", {"class": "main-breadcrumb", "aria-label": "Breadcrumb"}, ["mn-breadcrumb"], [
        el("List", "ol", {}, None, [
            el("Item", "li", {}, None, [el("Link", "a", {"href": "/"}, None, [text("Home")])]),
            el("Current", "li", {"aria-current": "page"}, None, [text("{this.title}")]),
        ])]),
    el("Title", "h1", {}, None, [text("{this.title}")]),
    cond("If excerpt", "this.excerpt", el("Intro", "p", {"class": "main-page-hero__intro"}, ["mn-page-hero-intro"],
                                         [text("{this.excerpt}")])),
], "main-page-hero__container", ["mn-page-hero-container"])
outputs["main-page-hero"] = kit_payload(page_hero, page_hero_styles)

# ================================================================ 3. Features / services grid
FEATURES = [("shield", "Trusted & safe", "One or two lines about this benefit or service."),
            ("users", "Expert team", "One or two lines about this benefit or service."),
            ("heart", "Personal care", "One or two lines about this benefit or service."),
            ("award", "Proven results", "One or two lines about this benefit or service.")]
features_styles = {**BASE, **HEADING_STYLES,
    "mn-features": style(".main-features", "background-color: var(--main-light);"),
    "mn-features-container": style(".main-features__container", "gap: var(--container-gap);"),
    "mn-features-grid": style(".main-features__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 24rem), 1fr));
  gap: var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;"""),
    "mn-features-item": style(".main-features__item", """display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-xs);
  padding: var(--space-m);
  border: 1px solid var(--main-line);
  border-radius: var(--radius-m);
  background-color: var(--main-light);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    border-color: var(--main-accent);
    box-shadow: 0 1rem 2.4rem var(--main-shadow);
  }

  @media (prefers-reduced-motion: reduce) {
    transition: none;
  }"""),
    "mn-features-icon": style(".main-features__icon", """inline-size: 5.6rem;
  block-size: 5.6rem;
  margin-block-end: var(--space-xs);
  padding: var(--space-s);
  border-radius: var(--radius-m);
  background-color: var(--main-accent-soft);
  color: var(--main-primary);"""),
    "mn-features-title": style(".main-features__title", "font-size: var(--h4);\n  color: var(--main-text);"),
    "mn-features-text": style(".main-features__text", "color: var(--main-text-muted);"),
}
features = section("Features", "main-features", [], ["mn-features"], [
    heading("Why choose us", "What we offer", "A short line that introduces your services or main benefits.",
            center=True),
    el("Grid", "ul", {"class": "main-features__grid"}, ["mn-features-grid"], [
        el("Item", "li", {"class": "main-features__item"}, ["mn-features-item"], [
            svg("Icon", icon(ic), "main-features__icon", ["mn-features-icon"]),
            el("Title", "h3", {"class": "main-features__title"}, ["mn-features-title"], [text(t)]),
            el("Text", "p", {"class": "main-features__text"}, ["mn-features-text"], [text(d)]),
        ]) for ic, t, d in FEATURES]),
], "main-features__container", ["mn-features-container"])
outputs["main-features"] = kit_payload(features, features_styles)

# ================================================================ 4. Image + text split
split_styles = {**BASE, **HEADING_STYLES, **MEDIA_STYLES, **BUTTONS_STYLES, **CHECKS_STYLES,
    "mn-split": style(".main-split", """background-color: var(--main-light);

  /* add the class main-split--reverse to put the image on the right */
  &.main-split--reverse .main-split__media {
    @media (width > 768px) {
      order: 2;
    }
  }"""),
    "mn-split-reverse": style(".main-split--reverse", ""),
    "mn-split-grid": style(".main-split__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 36rem), 1fr));
  gap: var(--container-gap);
  align-items: center;"""),
    "mn-split-media": style(".main-split__media", "--main-media-ratio: 4 / 3;\n  margin: 0;"),
    "mn-split-content": style(".main-split__content", """display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--content-gap);"""),
}
split = section("Split", "main-split", [], ["mn-split"], [
    el("Grid", "div", {"class": "main-split__grid"}, ["mn-split-grid"], [
        el("Media", "figure", {"class": "main-split__media"}, ["mn-split-media"], [media_img()]),
        el("Content", "div", {"class": "main-split__content"}, ["mn-split-content"], [
            heading("About us", "A headline for this part of the page",
                    "A paragraph that explains the topic. Two to four sentences work best next to an image."),
            checks(["First key point", "Second key point", "Third key point"]),
            buttons("Learn more", "/about/", "Contact us", "/contact/"),
        ]),
    ])])
outputs["main-split"] = kit_payload(split, split_styles)

# ================================================================ 5. Stats (brand band)
STATS = [("15+", "Years of experience"), ("2,000+", "Happy customers"), ("98%", "Would recommend us"),
         ("24/7", "Online support")]
stats_styles = {**BASE, **BAND_STYLES,
    "mn-stats": style(".main-stats", "padding-block: var(--section-space-s);"),
    "mn-stats-grid": style(".main-stats__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 14rem), 1fr));
  gap: var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;
  text-align: center;"""),
    "mn-stats-item": style(".main-stats__item", "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);"),
    "mn-stats-number": style(".main-stats__number", """font-size: var(--h1);
  font-weight: 800;
  line-height: 1;
  color: var(--main-accent);"""),
    "mn-stats-label": style(".main-stats__label", "color: var(--main-on-primary-muted);"),
}
stats = section("Stats", "main-stats", ["main-band"], ["mn-stats", "mn-band"], [
    el("Grid", "ul", {"class": "main-stats__grid"}, ["mn-stats-grid"], [
        el("Item", "li", {"class": "main-stats__item"}, ["mn-stats-item"], [
            el("Number", "p", {"class": "main-stats__number"}, ["mn-stats-number"], [text(n)]),
            el("Label", "p", {"class": "main-stats__label"}, ["mn-stats-label"], [text(l)]),
        ]) for n, l in STATS]),
])
outputs["main-stats"] = kit_payload(stats, stats_styles)

# ================================================================ 6. Steps / process (numbers by CSS counter)
STEPS = [("Contact us", "Call, chat on LINE or send the form."),
         ("Consultation", "We listen and recommend the right option."),
         ("Service", "Our team does the work with care."),
         ("Follow-up", "We check the result and stay in touch.")]
steps_styles = {**BASE, **HEADING_STYLES,
    "mn-steps": style(".main-steps", "background-color: var(--main-light-alt);"),
    "mn-steps-container": style(".main-steps__container", "gap: var(--container-gap);"),
    "mn-steps-list": style(".main-steps__list", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 22rem), 1fr));
  gap: var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;
  counter-reset: main-step;"""),
    "mn-steps-item": style(".main-steps__item", """display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-xs);
  counter-increment: main-step;

  /* step number — added automatically, in order */
  &::before {
    content: counter(main-step, decimal-leading-zero);
    display: grid;
    place-items: center;
    inline-size: 5.6rem;
    block-size: 5.6rem;
    margin-block-end: var(--space-xs);
    border-radius: 50%;
    background-color: var(--main-primary);
    box-shadow: 0 0 0 0.6rem var(--main-accent-soft);
    color: var(--main-on-primary);
    font-size: var(--text-l);
    font-weight: 800;
  }"""),
    "mn-steps-title": style(".main-steps__title", "font-size: var(--h4);\n  color: var(--main-text);"),
    "mn-steps-text": style(".main-steps__text", "color: var(--main-text-muted);"),
}
steps = section("Steps", "main-steps", [], ["mn-steps"], [
    heading("How it works", "Four simple steps", "Explain what the customer can expect from start to finish.",
            center=True),
    el("List", "ol", {"class": "main-steps__list"}, ["mn-steps-list"], [
        el("Step", "li", {"class": "main-steps__item"}, ["mn-steps-item"], [
            el("Title", "h3", {"class": "main-steps__title"}, ["mn-steps-title"], [text(t)]),
            el("Text", "p", {"class": "main-steps__text"}, ["mn-steps-text"], [text(d)]),
        ]) for t, d in STEPS]),
], "main-steps__container", ["mn-steps-container"])
outputs["main-steps"] = kit_payload(steps, steps_styles)

# ================================================================ 7. Reviews / testimonials
REVIEWS = [("Great service from start to finish. The team explained everything clearly.", "Customer Name",
            "Bangkok"),
           ("Fast, friendly and professional. I would recommend them to friends and family.", "Customer Name",
            "Chiang Mai"),
           ("The result was better than I expected. Thank you for taking such good care of me.", "Customer Name",
            "Phuket")]
reviews_styles = {**BASE, **HEADING_STYLES,
    "mn-reviews": style(".main-reviews", "background-color: var(--main-light);"),
    "mn-reviews-container": style(".main-reviews__container", "gap: var(--container-gap);"),
    "mn-reviews-grid": style(".main-reviews__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 28rem), 1fr));
  gap: var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;"""),
    "mn-reviews-item": style(".main-reviews__item", """position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-s);
  padding: var(--space-l) var(--space-m) var(--space-m);
  border-radius: var(--radius-m);
  background-color: var(--main-light-alt);"""),
    "mn-reviews-quote-icon": style(".main-reviews__quote-icon", """position: absolute;
  inset-block-start: var(--space-s);
  inset-inline-end: var(--space-m);
  inline-size: 4rem;
  block-size: 4rem;
  color: var(--main-line);"""),
    "mn-reviews-stars": style(".main-reviews__stars", """display: flex;
  gap: calc(var(--space-xs) / 4);
  color: var(--main-accent);

  svg {
    inline-size: 1.8rem;
    block-size: 1.8rem;
  }"""),
    "mn-reviews-text": style(".main-reviews__text", "margin: 0;\n  color: var(--main-text);"),
    "mn-reviews-author": style(".main-reviews__author", """margin-block-start: auto;
  padding-block-start: var(--space-s);
  border-block-start: 1px solid var(--main-line);"""),
    "mn-reviews-name": style(".main-reviews__name", "font-weight: 700;\n  color: var(--main-primary);"),
    "mn-reviews-meta": style(".main-reviews__meta", "font-size: var(--text-s);\n  color: var(--main-text-muted);"),
}
reviews = section("Reviews", "main-reviews", [], ["mn-reviews"], [
    heading("Reviews", "What our customers say", center=True),
    el("Grid", "ul", {"class": "main-reviews__grid"}, ["mn-reviews-grid"], [
        el("Review", "li", {"class": "main-reviews__item"}, ["mn-reviews-item"], [
            svg("Quote icon", icon("quote"), "main-reviews__quote-icon", ["mn-reviews-quote-icon"]),
            el("Stars", "div", {"class": "main-reviews__stars", "role": "img", "aria-label": "5 out of 5 stars"},
               ["mn-reviews-stars"], [svg("Star", icon("star")) for _ in range(5)]),
            el("Text", "blockquote", {"class": "main-reviews__text"}, ["mn-reviews-text"], [
                el("Paragraph", "p", {}, None, [text(q)])]),
            el("Author", "div", {"class": "main-reviews__author"}, ["mn-reviews-author"], [
                el("Name", "p", {"class": "main-reviews__name"}, ["mn-reviews-name"], [text(n)]),
                el("Meta", "p", {"class": "main-reviews__meta"}, ["mn-reviews-meta"], [text(m)]),
            ]),
        ]) for q, n, m in REVIEWS]),
], "main-reviews__container", ["mn-reviews-container"])
outputs["main-reviews"] = kit_payload(reviews, reviews_styles)

# ================================================================ 8. 404 page (<main> for the 404 template)
nf_styles = {**BASE, **BUTTONS_STYLES,
    "mn-404": style(".main-404", "padding-block: var(--section-space-xl);\n"
                                 "  background-color: var(--main-light-alt);"),
    "mn-404-container": style(".main-404__container", "align-items: center;\n  gap: var(--content-gap);\n"
                                                      "  text-align: center;"),
    "mn-404-code": style(".main-404__code", """font-size: clamp(8rem, 18vw, 18rem);
  font-weight: 800;
  line-height: 1;
  color: var(--main-primary);

  &::after {
    content: "";
    display: block;
    inline-size: 6rem;
    block-size: 0.4rem;
    margin: var(--space-s) auto 0;
    border-radius: var(--radius-circle, 999px);
    background-color: var(--main-accent);
  }"""),
    "mn-404-text": style(".main-404__text", "max-inline-size: 52rem;\n  color: var(--main-text-muted);"),
}
not_found = el("Main", "main", {"id": "main"}, None, [
    section("Not Found", "main-404", [], ["mn-404"], [
        el("Code", "p", {"class": "main-404__code", "aria-hidden": "true"}, ["mn-404-code"], [text("404")]),
        el("Title", "h1", {}, None, [text("Page not found")]),
        el("Text", "p", {"class": "main-404__text"}, ["mn-404-text"], [
            text("The page you are looking for may have moved or no longer exists.")]),
        buttons("Back to home", "/", "Contact us", "/contact/"),
    ], "main-404__container", ["mn-404-container"])])
outputs["main-404"] = kit_payload(not_found, nf_styles)

for name, p in outputs.items():
    write(f"{OUT}/{name}.etch.txt", p)
    print("ok", name, len(p["styles"]), "styles", len(json.dumps(p)) // 1024, "KB")
