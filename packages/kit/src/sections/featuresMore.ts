/** Features variants: image + list, numbered grid, brand band, image cards, heading + list.
 * Port of _build/build_features_more.py. Plain sections (edit the text in the blocks); colours come from kit COLORS.
 * Lengths in rem are written for 1rem = 10px and become to-rem() (portable). */
import { type Block, type Payload, type Styles, el, nowIso, style, svg, text } from "../etch/lib";
import { BASE, BUTTONS_STYLES, CON, HEADING_STYLES, MEDIA_STYLES, SEC, buttons, heading, icon, kitPayload,
  mediaImg } from "../kit";

const TEXT = "One or two lines about this benefit or service.";
const FOUR: [string, string][] = [["shield", "Trusted & safe"], ["users", "Expert team"], ["heart", "Personal care"],
  ["award", "Proven results"]];

function section(name: string, cls: string, styleIds: string[], children: Block[]): Block {
  return el(name, "section", { ...SEC, class: cls }, ["etch-section-style", ...styleIds], [
    el("Container", "div", CON, ["etch-container-style"], children)]);
}

const ITEM_TEXT = { // shared title / text look inside every variant
  title: "font-size: var(--h4);\n  color: var(--main-text);",
  text: "margin: 0;\n  color: var(--main-text-muted);",
};

// ================================================================ 1. image + 2×2 icon list
function image(now: () => string): Payload {
  const p = "mn-fi", b = "main-features-image";
  const styles: Styles = { ...BASE, ...HEADING_STYLES, ...MEDIA_STYLES,
    [p]: style(`.${b}`, "background-color: var(--main-light);"),
    [p + "-grid"]: style(`.${b}__grid`, `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 40rem), 1fr));
  gap: var(--container-gap);
  align-items: center;`),
    [p + "-media"]: style(`.${b}__media`, "--main-media-ratio: 4 / 5;\n  margin: 0;"),
    [p + "-content"]: style(`.${b}__content`, "display: flex;\n  flex-direction: column;\n  gap: var(--space-l);"),
    [p + "-list"]: style(`.${b}__list`, `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 22rem), 1fr));
  gap: var(--space-l) var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;`),
    [p + "-item"]: style(`.${b}__item`, "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);"),
    [p + "-icon"]: style(`.${b}__icon`, `inline-size: 4.8rem;
  block-size: 4.8rem;
  padding: 1.1rem;
  border-radius: 50%;
  background-color: var(--main-accent-soft);
  color: var(--main-primary);`),
    [p + "-title"]: style(`.${b}__title`, ITEM_TEXT.title),
    [p + "-text"]: style(`.${b}__text`, ITEM_TEXT.text),
  };
  return kitPayload(section("Features Image", b, [p], [
    el("Grid", "div", { class: `${b}__grid` }, [p + "-grid"], [
      el("Media", "figure", { class: `${b}__media` }, [p + "-media"], [mediaImg()]),
      el("Content", "div", { class: `${b}__content` }, [p + "-content"], [
        heading("Why choose us", "What we offer", "A short line that introduces your services or main benefits."),
        el("List", "ul", { class: `${b}__list` }, [p + "-list"], FOUR.map(([ic, t]) =>
          el("Item", "li", { class: `${b}__item` }, [p + "-item"], [
            svg("Icon", icon(ic), `${b}__icon`, [p + "-icon"]),
            el("Title", "h3", { class: `${b}__title` }, [p + "-title"], [text(t)]),
            el("Text", "p", { class: `${b}__text` }, [p + "-text"], [text(TEXT)]),
          ]))),
      ]),
    ])]), styles, null, null, now);
}

// ================================================================ 2. six numbered points, no icons
const SIX = ["Trusted & safe", "Expert team", "Personal care", "Proven results", "Clear pricing", "Easy booking"];

function numbered(now: () => string): Payload {
  const p = "mn-fn", b = "main-features-numbered";
  const styles: Styles = { ...BASE, ...HEADING_STYLES,
    [p]: style(`.${b}`, "background-color: var(--main-light-alt);"),
    [p + "-container"]: style(`.${b}__container`, "gap: var(--container-gap);"),
    [p + "-grid"]: style(`.${b}__grid`, `display: grid;
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
  }`),
    [p + "-item"]: style(`.${b}__item`, `display: flex;
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
  }`),
    [p + "-title"]: style(`.${b}__title`, ITEM_TEXT.title),
    [p + "-text"]: style(`.${b}__text`, ITEM_TEXT.text),
  };
  return kitPayload(el("Features Numbered", "section", { ...SEC, class: b }, ["etch-section-style", p], [
    el("Container", "div", { ...CON, class: `${b}__container` }, ["etch-container-style", p + "-container"], [
      heading("Why choose us", "Six reasons to choose us", "A short line that introduces your main benefits."),
      el("Grid", "ol", { class: `${b}__grid` }, [p + "-grid"], SIX.map((t) =>
        el("Item", "li", { class: `${b}__item` }, [p + "-item"], [
          el("Title", "h3", { class: `${b}__title` }, [p + "-title"], [text(t)]),
          el("Text", "p", { class: `${b}__text` }, [p + "-text"], [text(TEXT)]),
        ]))),
    ])]), styles, null, null, now);
}

// ================================================================ 3. on the primary colour, round icons
function band(now: () => string): Payload {
  const p = "mn-fb", b = "main-features-band";
  const styles: Styles = { ...BASE, ...HEADING_STYLES,
    [p]: style(`.${b}`, `background-color: var(--main-primary);
  color: var(--main-on-primary);

  :is(h1, h2, h3, h4, h5, h6),
  .main-heading__eyebrow {
    color: inherit;
  }

  .main-heading__intro {
    color: var(--main-on-primary-muted);
  }`),
    [p + "-container"]: style(`.${b}__container`, "gap: var(--container-gap);"),
    [p + "-grid"]: style(`.${b}__grid`, `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 22rem), 1fr));
  gap: var(--space-l) var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;
  text-align: center;`),
    [p + "-item"]: style(`.${b}__item`, "display: flex;\n  flex-direction: column;\n  align-items: center;\n"
      + "  gap: var(--space-xs);"),
    [p + "-icon"]: style(`.${b}__icon`, `inline-size: 7.2rem;
  block-size: 7.2rem;
  margin-block-end: var(--space-xs);
  padding: 1.8rem;
  border-radius: 50%;
  background-color: var(--main-accent);
  color: var(--main-on-primary);`),
    [p + "-title"]: style(`.${b}__title`, "font-size: var(--h4);\n  color: inherit;"),
    [p + "-text"]: style(`.${b}__text`, "margin: 0;\n  color: var(--main-on-primary-muted);"),
  };
  return kitPayload(el("Features Band", "section", { ...SEC, class: b }, ["etch-section-style", p], [
    el("Container", "div", { ...CON, class: `${b}__container` }, ["etch-container-style", p + "-container"], [
      heading("Why choose us", "What we offer", "A short line that introduces your services or main benefits.",
        "h2", true),
      el("Grid", "ul", { class: `${b}__grid` }, [p + "-grid"], FOUR.map(([ic, t]) =>
        el("Item", "li", { class: `${b}__item` }, [p + "-item"], [
          svg("Icon", icon(ic), `${b}__icon`, [p + "-icon"]),
          el("Title", "h3", { class: `${b}__title` }, [p + "-title"], [text(t)]),
          el("Text", "p", { class: `${b}__text` }, [p + "-text"], [text(TEXT)]),
        ]))),
    ])]), styles, null, null, now);
}

// ================================================================ 4. three cards with a photo each (services)
function cards(now: () => string): Payload {
  const p = "mn-fc", b = "main-features-cards";
  const styles: Styles = { ...BASE, ...HEADING_STYLES, ...MEDIA_STYLES,
    [p]: style(`.${b}`, "background-color: var(--main-light);"),
    [p + "-container"]: style(`.${b}__container`, "gap: var(--container-gap);"),
    [p + "-grid"]: style(`.${b}__grid`, `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 28rem), 1fr));
  gap: var(--grid-gap);
  margin: 0;
  padding: 0;
  list-style: none;`),
    [p + "-card"]: style(`.${b}__card`, `position: relative;
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
  }`),
    [p + "-body"]: style(`.${b}__body`, "display: flex;\n  flex: 1;\n  flex-direction: column;\n"
      + "  gap: var(--space-xs);\n  padding: var(--space-m);"),
    [p + "-title"]: style(`.${b}__title`, ITEM_TEXT.title),
    [p + "-text"]: style(`.${b}__text`, ITEM_TEXT.text),
    [p + "-link"]: style(`.${b}__link`, `margin-block-start: auto;
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
  }`),
  };
  return kitPayload(el("Features Cards", "section", { ...SEC, class: b }, ["etch-section-style", p], [
    el("Container", "div", { ...CON, class: `${b}__container` }, ["etch-container-style", p + "-container"], [
      heading("Our services", "What we offer", "A short line that introduces your services.", "h2", true),
      el("Grid", "ul", { class: `${b}__grid` }, [p + "-grid"], [1, 2, 3].map((n) =>
        el("Card", "li", { class: `${b}__card` }, [p + "-card"], [
          mediaImg(),
          el("Body", "div", { class: `${b}__body` }, [p + "-body"], [
            el("Title", "h3", { class: `${b}__title` }, [p + "-title"], [text(`Service ${n}`)]),
            el("Text", "p", { class: `${b}__text` }, [p + "-text"], [text(TEXT)]),
            el("Link", "a", { class: `${b}__link`, href: `/services/service-${n}/` }, [p + "-link"],
              [text("Learn more →")]),
          ]),
        ]))),
    ])]), styles, null, null, now);
}

// ================================================================ 5. heading + button on the left, icon rows on the right
function list(now: () => string): Payload {
  const p = "mn-fl", b = "main-features-list";
  const styles: Styles = { ...BASE, ...HEADING_STYLES, ...BUTTONS_STYLES,
    [p]: style(`.${b}`, "background-color: var(--main-light);"),
    [p + "-grid"]: style(`.${b}__grid`, `display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 3fr);
  gap: var(--container-gap);
  align-items: start;

  @media (width <= 992px) {
    grid-template-columns: 1fr;
  }`),
    [p + "-intro"]: style(`.${b}__intro`, `position: sticky;
  inset-block-start: var(--space-xl);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--content-gap);

  @media (width <= 992px) {
    position: static;
  }`),
    [p + "-list"]: style(`.${b}__list`, "display: flex;\n  flex-direction: column;\n  margin: 0;\n  padding: 0;\n"
      + "  list-style: none;"),
    [p + "-item"]: style(`.${b}__item`, `display: flex;
  align-items: flex-start;
  gap: var(--space-m);
  padding-block: var(--space-m);
  border-block-end: 1px solid var(--main-line);

  &:first-child {
    padding-block-start: 0;
  }`),
    [p + "-icon"]: style(`.${b}__icon`, `flex: none;
  inline-size: 5.6rem;
  block-size: 5.6rem;
  padding: 1.4rem;
  border-radius: var(--radius-m);
  background-color: var(--main-accent-soft);
  color: var(--main-primary);`),
    [p + "-body"]: style(`.${b}__body`, "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);"),
    [p + "-title"]: style(`.${b}__title`, ITEM_TEXT.title),
    [p + "-text"]: style(`.${b}__text`, ITEM_TEXT.text),
  };
  return kitPayload(section("Features List", b, [p], [
    el("Grid", "div", { class: `${b}__grid` }, [p + "-grid"], [
      el("Intro", "div", { class: `${b}__intro` }, [p + "-intro"], [
        heading("Why choose us", "What we offer", "A short line that introduces your services or main benefits."),
        buttons("Our services", "/services/", "Contact us", "/contact/"),
      ]),
      el("List", "ul", { class: `${b}__list` }, [p + "-list"], FOUR.map(([ic, t]) =>
        el("Item", "li", { class: `${b}__item` }, [p + "-item"], [
          svg("Icon", icon(ic), `${b}__icon`, [p + "-icon"]),
          el("Body", "div", { class: `${b}__body` }, [p + "-body"], [
            el("Title", "h3", { class: `${b}__title` }, [p + "-title"], [text(t)]),
            el("Text", "p", { class: `${b}__text` }, [p + "-text"], [text(TEXT)]),
          ]),
        ]))),
    ])]), styles, null, null, now);
}

/** The five templates of build_features_more.py, in its output order. */
export function build(now: () => string = nowIso): Record<string, Payload> {
  return {
    "main-features-image": image(now),
    "main-features-numbered": numbered(now),
    "main-features-band": band(now),
    "main-features-cards": cards(now),
    "main-features-list": list(now),
  };
}
