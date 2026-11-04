/** Second batch of main-* sections: hero, page hero, features, split, stats, steps, reviews, 404.
 * Port of _build/build_sections_more.py. Plain sections (edit the text in the blocks); colours come from kit COLORS. */
import { type Block, type Payload, type Styles, cond, el, nowIso, style, svg, text } from "../etch/lib";
import { BAND_STYLES, BASE, BUTTONS_STYLES, CHECKS_STYLES, CON, HEADING_STYLES, MEDIA_STYLES, SEC, buttons, checks,
  heading, icon, kitPayload, mediaImg } from "../kit";

function section(name: string, blockCls: string, extraCls: string[], stylesIds: string[], children: Block[],
                 containerCls?: string | null, containerIds: string[] = []): Block {
  const conAttrs = containerCls ? { ...CON, class: containerCls } : CON;
  return el(name, "section", { ...SEC, class: [blockCls, ...extraCls].join(" ") },
    ["etch-section-style", ...stylesIds], [
      el("Container", "div", conAttrs, ["etch-container-style", ...containerIds], children)]);
}

// ================================================================ 1. Hero (home page)
function hero(now: () => string): Payload {
  const styles: Styles = { ...BASE, ...HEADING_STYLES, ...MEDIA_STYLES, ...BUTTONS_STYLES, ...CHECKS_STYLES,
    "mn-hero": style(".main-hero", "padding-block: var(--section-space-l);\n"
      + "  background-color: var(--main-light-alt);"),
    "mn-hero-grid": style(".main-hero__grid", `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 40rem), 1fr));
  gap: var(--container-gap);
  align-items: center;`),
    "mn-hero-content": style(".main-hero__content", `display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--content-gap);`),
    "mn-hero-media": style(".main-hero__media", "--main-media-ratio: 5 / 4;\n  margin: 0;"),
  };
  const b = section("Hero", "main-hero", [], ["mn-hero"], [
    el("Grid", "div", { class: "main-hero__grid" }, ["mn-hero-grid"], [
      el("Content", "div", { class: "main-hero__content" }, ["mn-hero-content"], [
        heading("Welcome", "A clear headline that says what you do and for whom",
          "One or two sentences about the main benefit. Keep it short and specific.", "h1"),
        buttons("Book now", "/contact/", "Our services", "/services/"),
        checks(["Short trust point", "Another reason to choose you", "Free consultation"]),
      ]),
      el("Media", "figure", { class: "main-hero__media" }, ["mn-hero-media"], [mediaImg("Image", true)]),
    ])]);
  return kitPayload(b, styles, null, null, now);
}

// ================================================================ 2. Page hero (inner pages, breadcrumb)
function pageHero(now: () => string): Payload {
  const styles: Styles = { ...BASE, ...BAND_STYLES,
    "mn-page-hero": style(".main-page-hero", "padding-block: var(--section-space-m);"),
    "mn-page-hero-container": style(".main-page-hero__container", "align-items: center;\n"
      + "  gap: var(--space-s);\n  text-align: center;"),
    "mn-breadcrumb": style(".main-breadcrumb", `font-size: var(--text-s);

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
  }`),
    "mn-page-hero-intro": style(".main-page-hero__intro", "max-inline-size: 60rem;"),
  };
  const b = section("Page Hero", "main-page-hero", ["main-band"], ["mn-page-hero", "mn-band"], [
    el("Breadcrumb", "nav", { class: "main-breadcrumb", "aria-label": "Breadcrumb" }, ["mn-breadcrumb"], [
      el("List", "ol", {}, null, [
        el("Item", "li", {}, null, [el("Link", "a", { href: "/" }, null, [text("Home")])]),
        el("Current", "li", { "aria-current": "page" }, null, [text("{this.title}")]),
      ])]),
    el("Title", "h1", {}, null, [text("{this.title}")]),
    cond("If excerpt", "this.excerpt", el("Intro", "p", { class: "main-page-hero__intro" },
      ["mn-page-hero-intro"], [text("{this.excerpt}")])),
  ], "main-page-hero__container", ["mn-page-hero-container"]);
  return kitPayload(b, styles, null, null, now);
}

// ================================================================ 3. Features / services grid
const FEATURES: [string, string, string][] = [
  ["shield", "Trusted & safe", "One or two lines about this benefit or service."],
  ["users", "Expert team", "One or two lines about this benefit or service."],
  ["heart", "Personal care", "One or two lines about this benefit or service."],
  ["award", "Proven results", "One or two lines about this benefit or service."],
];

function features(now: () => string): Payload {
  const styles: Styles = { ...BASE, ...HEADING_STYLES,
    "mn-features": style(".main-features", "background-color: var(--main-light);"),
    "mn-features-container": style(".main-features__container", "gap: var(--container-gap);"),
    "mn-features-grid": style(".main-features__grid", `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 24rem), 1fr));
  gap: var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;`),
    "mn-features-item": style(".main-features__item", `display: flex;
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
  }`),
    "mn-features-icon": style(".main-features__icon", `inline-size: 5.6rem;
  block-size: 5.6rem;
  margin-block-end: var(--space-xs);
  padding: var(--space-s);
  border-radius: var(--radius-m);
  background-color: var(--main-accent-soft);
  color: var(--main-primary);`),
    "mn-features-title": style(".main-features__title", "font-size: var(--h4);\n  color: var(--main-text);"),
    "mn-features-text": style(".main-features__text", "color: var(--main-text-muted);"),
  };
  const b = section("Features", "main-features", [], ["mn-features"], [
    heading("Why choose us", "What we offer", "A short line that introduces your services or main benefits.",
      "h2", true),
    el("Grid", "ul", { class: "main-features__grid" }, ["mn-features-grid"], FEATURES.map(([ic, t, d]) =>
      el("Item", "li", { class: "main-features__item" }, ["mn-features-item"], [
        svg("Icon", icon(ic), "main-features__icon", ["mn-features-icon"]),
        el("Title", "h3", { class: "main-features__title" }, ["mn-features-title"], [text(t)]),
        el("Text", "p", { class: "main-features__text" }, ["mn-features-text"], [text(d)]),
      ]))),
  ], "main-features__container", ["mn-features-container"]);
  return kitPayload(b, styles, null, null, now);
}

// ================================================================ 4. Image + text split
function split(now: () => string): Payload {
  const styles: Styles = { ...BASE, ...HEADING_STYLES, ...MEDIA_STYLES, ...BUTTONS_STYLES, ...CHECKS_STYLES,
    "mn-split": style(".main-split", `background-color: var(--main-light);

  /* add the class main-split--reverse to put the image on the right */
  &.main-split--reverse .main-split__media {
    @media (width > 768px) {
      order: 2;
    }
  }`),
    "mn-split-reverse": style(".main-split--reverse", ""),
    "mn-split-grid": style(".main-split__grid", `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 36rem), 1fr));
  gap: var(--container-gap);
  align-items: center;`),
    "mn-split-media": style(".main-split__media", "--main-media-ratio: 4 / 3;\n  margin: 0;"),
    "mn-split-content": style(".main-split__content", `display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--content-gap);`),
  };
  const b = section("Split", "main-split", [], ["mn-split"], [
    el("Grid", "div", { class: "main-split__grid" }, ["mn-split-grid"], [
      el("Media", "figure", { class: "main-split__media" }, ["mn-split-media"], [mediaImg()]),
      el("Content", "div", { class: "main-split__content" }, ["mn-split-content"], [
        heading("About us", "A headline for this part of the page",
          "A paragraph that explains the topic. Two to four sentences work best next to an image."),
        checks(["First key point", "Second key point", "Third key point"]),
        buttons("Learn more", "/about/", "Contact us", "/contact/"),
      ]),
    ])]);
  return kitPayload(b, styles, null, null, now);
}

// ================================================================ 5. Stats (brand band)
const STATS: [string, string][] = [["15+", "Years of experience"], ["2,000+", "Happy customers"],
  ["98%", "Would recommend us"], ["24/7", "Online support"]];

function stats(now: () => string): Payload {
  const styles: Styles = { ...BASE, ...BAND_STYLES,
    "mn-stats": style(".main-stats", "padding-block: var(--section-space-s);"),
    "mn-stats-grid": style(".main-stats__grid", `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 14rem), 1fr));
  gap: var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;
  text-align: center;`),
    "mn-stats-item": style(".main-stats__item", "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);"),
    "mn-stats-number": style(".main-stats__number", `font-size: var(--h1);
  font-weight: 800;
  line-height: 1;
  color: var(--main-accent);`),
    "mn-stats-label": style(".main-stats__label", "color: var(--main-on-primary-muted);"),
  };
  const b = section("Stats", "main-stats", ["main-band"], ["mn-stats", "mn-band"], [
    el("Grid", "ul", { class: "main-stats__grid" }, ["mn-stats-grid"], STATS.map(([n, l]) =>
      el("Item", "li", { class: "main-stats__item" }, ["mn-stats-item"], [
        el("Number", "p", { class: "main-stats__number" }, ["mn-stats-number"], [text(n)]),
        el("Label", "p", { class: "main-stats__label" }, ["mn-stats-label"], [text(l)]),
      ]))),
  ]);
  return kitPayload(b, styles, null, null, now);
}

// ================================================================ 6. Steps / process (numbers by CSS counter)
const STEPS: [string, string][] = [["Contact us", "Call, chat on LINE or send the form."],
  ["Consultation", "We listen and recommend the right option."],
  ["Service", "Our team does the work with care."],
  ["Follow-up", "We check the result and stay in touch."]];

function steps(now: () => string): Payload {
  const styles: Styles = { ...BASE, ...HEADING_STYLES,
    "mn-steps": style(".main-steps", "background-color: var(--main-light-alt);"),
    "mn-steps-container": style(".main-steps__container", "gap: var(--container-gap);"),
    "mn-steps-list": style(".main-steps__list", `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 22rem), 1fr));
  gap: var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;
  counter-reset: main-step;`),
    "mn-steps-item": style(".main-steps__item", `display: flex;
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
  }`),
    "mn-steps-title": style(".main-steps__title", "font-size: var(--h4);\n  color: var(--main-text);"),
    "mn-steps-text": style(".main-steps__text", "color: var(--main-text-muted);"),
  };
  const b = section("Steps", "main-steps", [], ["mn-steps"], [
    heading("How it works", "Four simple steps", "Explain what the customer can expect from start to finish.",
      "h2", true),
    el("List", "ol", { class: "main-steps__list" }, ["mn-steps-list"], STEPS.map(([t, d]) =>
      el("Step", "li", { class: "main-steps__item" }, ["mn-steps-item"], [
        el("Title", "h3", { class: "main-steps__title" }, ["mn-steps-title"], [text(t)]),
        el("Text", "p", { class: "main-steps__text" }, ["mn-steps-text"], [text(d)]),
      ]))),
  ], "main-steps__container", ["mn-steps-container"]);
  return kitPayload(b, styles, null, null, now);
}

// ================================================================ 7. Reviews / testimonials
const REVIEWS: [string, string, string][] = [
  ["Great service from start to finish. The team explained everything clearly.", "Customer Name", "Bangkok"],
  ["Fast, friendly and professional. I would recommend them to friends and family.", "Customer Name",
    "Chiang Mai"],
  ["The result was better than I expected. Thank you for taking such good care of me.", "Customer Name",
    "Phuket"],
];

function reviews(now: () => string): Payload {
  const styles: Styles = { ...BASE, ...HEADING_STYLES,
    "mn-reviews": style(".main-reviews", "background-color: var(--main-light);"),
    "mn-reviews-container": style(".main-reviews__container", "gap: var(--container-gap);"),
    "mn-reviews-grid": style(".main-reviews__grid", `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 28rem), 1fr));
  gap: var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;`),
    "mn-reviews-item": style(".main-reviews__item", `position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-s);
  padding: var(--space-l) var(--space-m) var(--space-m);
  border-radius: var(--radius-m);
  background-color: var(--main-light-alt);`),
    "mn-reviews-quote-icon": style(".main-reviews__quote-icon", `position: absolute;
  inset-block-start: var(--space-s);
  inset-inline-end: var(--space-m);
  inline-size: 4rem;
  block-size: 4rem;
  color: var(--main-line);`),
    "mn-reviews-stars": style(".main-reviews__stars", `display: flex;
  gap: calc(var(--space-xs) / 4);
  color: var(--main-accent);

  svg {
    inline-size: 1.8rem;
    block-size: 1.8rem;
  }`),
    "mn-reviews-text": style(".main-reviews__text", "margin: 0;\n  color: var(--main-text);"),
    "mn-reviews-author": style(".main-reviews__author", `margin-block-start: auto;
  padding-block-start: var(--space-s);
  border-block-start: 1px solid var(--main-line);`),
    "mn-reviews-name": style(".main-reviews__name", "font-weight: 700;\n  color: var(--main-primary);"),
    "mn-reviews-meta": style(".main-reviews__meta", "font-size: var(--text-s);\n  color: var(--main-text-muted);"),
  };
  const b = section("Reviews", "main-reviews", [], ["mn-reviews"], [
    heading("Reviews", "What our customers say", null, "h2", true),
    el("Grid", "ul", { class: "main-reviews__grid" }, ["mn-reviews-grid"], REVIEWS.map(([q, n, m]) =>
      el("Review", "li", { class: "main-reviews__item" }, ["mn-reviews-item"], [
        svg("Quote icon", icon("quote"), "main-reviews__quote-icon", ["mn-reviews-quote-icon"]),
        el("Stars", "div", { class: "main-reviews__stars", role: "img", "aria-label": "5 out of 5 stars" },
          ["mn-reviews-stars"], Array.from({ length: 5 }, () => svg("Star", icon("star")))),
        el("Text", "blockquote", { class: "main-reviews__text" }, ["mn-reviews-text"], [
          el("Paragraph", "p", {}, null, [text(q)])]),
        el("Author", "div", { class: "main-reviews__author" }, ["mn-reviews-author"], [
          el("Name", "p", { class: "main-reviews__name" }, ["mn-reviews-name"], [text(n)]),
          el("Meta", "p", { class: "main-reviews__meta" }, ["mn-reviews-meta"], [text(m)]),
        ]),
      ]))),
  ], "main-reviews__container", ["mn-reviews-container"]);
  return kitPayload(b, styles, null, null, now);
}

// ================================================================ 8. 404 page (<main> for the 404 template)
function notFound(now: () => string): Payload {
  const styles: Styles = { ...BASE, ...BUTTONS_STYLES,
    "mn-404": style(".main-404", "padding-block: var(--section-space-xl);\n"
      + "  background-color: var(--main-light-alt);"),
    "mn-404-container": style(".main-404__container", "align-items: center;\n  gap: var(--content-gap);\n"
      + "  text-align: center;"),
    "mn-404-code": style(".main-404__code", `font-size: clamp(8rem, 18vw, 18rem);
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
  }`),
    "mn-404-text": style(".main-404__text", "max-inline-size: 52rem;\n  color: var(--main-text-muted);"),
  };
  const b = el("Main", "main", { id: "main" }, null, [
    section("Not Found", "main-404", [], ["mn-404"], [
      el("Code", "p", { class: "main-404__code", "aria-hidden": "true" }, ["mn-404-code"], [text("404")]),
      el("Title", "h1", {}, null, [text("Page not found")]),
      el("Text", "p", { class: "main-404__text" }, ["mn-404-text"], [
        text("The page you are looking for may have moved or no longer exists.")]),
      buttons("Back to home", "/", "Contact us", "/contact/"),
    ], "main-404__container", ["mn-404-container"])]);
  return kitPayload(b, styles, null, null, now);
}

/** The eight templates of build_sections_more.py, in its output order. */
export function build(now: () => string = nowIso): Record<string, Payload> {
  return {
    "main-hero": hero(now),
    "main-page-hero": pageHero(now),
    "main-features": features(now),
    "main-split": split(now),
    "main-stats": stats(now),
    "main-steps": steps(now),
    "main-reviews": reviews(now),
    "main-404": notFound(now),
  };
}
