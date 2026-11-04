/**
 * Shared pieces of the main-* template kit: colours, base Etch styles, icons, heading, social links, post card.
 * Port of _build/kit.py.
 *
 * Every template file carries the styles it uses from here, so all files paste the same CSS for the same selector
 * (Etch keeps one style per selector, the first paste wins).
 */
import { ICONS } from "./icons";
import { type Attrs, type Block, type Payload, type Styles, cond, dataUri, el, img, loop, nowIso, payload, prop,
  style, svg, text } from "../etch/lib";

// ================================================================ colours — the only place colours are defined
export const COLORS_CSS = `/* ===== MAIN TEMPLATE COLOURS — change colours here only =====
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
  --main-shadow: color-mix(in srgb, var(--main-text) 12%, transparent);`;

export const COLORS: Styles = { "main-colors": style(":where(:root)", COLORS_CSS, "custom") };

// ================================================================ Etch base element styles (identical on every site)
export const BASE: Styles = {
  "etch-section-style": {
    type: "element", selector: ':where([data-etch-element="section"])', collection: "default",
    css: "inline-size: 100%;\n  display: flex;\n  flex-direction: column;\n  align-items: center;",
  },
  "etch-container-style": {
    type: "element", selector: ':where([data-etch-element="container"])', collection: "default",
    css: "inline-size: 100%;\n  display: flex;\n  flex-direction: column;\n"
      + "  max-inline-size: var(--content-width, 1366px);\n  align-self: center; margin-inline: auto;",
  },
};
export const SEC: Attrs = { "data-etch-element": "section" };
export const CON: Attrs = { "data-etch-element": "container" };

export function icon(name: string): string {
  const svgMarkup = ICONS[name];
  if (svgMarkup === undefined) throw new Error(`unknown icon ${name}`);
  return dataUri(svgMarkup);
}

// ================================================================ section heading (eyebrow / title / intro)
export const HEADING_STYLES: Styles = {
  "mn-heading": style(".main-heading", "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);\n"
    + "  max-inline-size: 60rem;"),
  "mn-heading-center": style(".main-heading--center", "align-items: center;\n  margin-inline: auto;\n"
    + "  text-align: center;"),
  "mn-eyebrow": style(".main-heading__eyebrow", `display: flex;
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
  }`),
  "mn-intro": style(".main-heading__intro", "color: var(--main-text-muted);"),
};

export function heading(eyebrow: string | null, title: string, intro?: string | null, tag = "h2",
                        center = false): Block {
  let cls = "main-heading";
  let ids = ["mn-heading"];
  if (center) {
    cls += " main-heading--center";
    ids = [...ids, "mn-heading-center"];
  }
  const kids: Block[] = [];
  if (eyebrow != null) {
    kids.push(el("Eyebrow", "p", { class: "main-heading__eyebrow" }, ["mn-eyebrow"], [text(eyebrow)]));
  }
  kids.push(el("Title", tag, {}, null, [text(title)]));
  if (intro != null) kids.push(el("Intro", "p", { class: "main-heading__intro" }, ["mn-intro"], [text(intro)]));
  return el("Heading", "div", { class: cls }, ids, kids);
}

// ================================================================ brand band: a section on the primary colour
export const BAND_STYLES: Styles = {
  "mn-band": style(".main-band", `background-color: var(--main-primary);
  color: var(--main-on-primary);

  :is(h1, h2, h3, h4, h5, h6),
  .main-heading__eyebrow {
    color: inherit;
  }

  .main-heading__intro {
    color: var(--main-on-primary-muted);
  }`),
};

// ================================================================ social icons (shared by footer, CTA, contact, share)
export const SOCIAL_STYLES: Styles = {
  "mn-social": style(".main-social", "display: flex;\n  flex-wrap: wrap;\n  align-items: center;\n"
    + "  gap: var(--space-xs);\n  margin: 0;\n  padding: 0;\n  list-style: none;"),
  "mn-social-link": style(".main-social__link", `/* colour of the ring + icon; the footer sets --main-social-color */
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
  }`),
  "mn-social-icon": style(".main-social__icon", "display: block;\n  inline-size: 2rem;\n  block-size: 2rem;"),
};
export const SOCIALS: [string, string][] = [["line", "LINE"], ["facebook", "Facebook"], ["instagram", "Instagram"],
  ["tiktok", "TikTok"], ["youtube", "YouTube"]];
export const SOCIAL_PROPS: Attrs[] = [
  prop("LINE URL", "lineUrl", "https://line.me/R/ti/p/@example", "Empty = hidden"),
  prop("Facebook URL", "facebookUrl", "https://facebook.com/", "Empty = hidden"),
  prop("Instagram URL", "instagramUrl", "https://instagram.com/", "Empty = hidden"),
  prop("TikTok URL", "tiktokUrl", "", "Empty = hidden"),
  prop("YouTube URL", "youtubeUrl", "", "Empty = hidden"),
];

export function socialLink(name: string, href: string, iconName: string, label: string, blank = true): Block {
  let a: Attrs = { class: "main-social__link", href, "aria-label": label };
  if (blank) a = { ...a, target: "_blank", rel: "noopener" };
  return el(name, "a", a, ["mn-social-link"], [svg(`${name} icon`, icon(iconName), "main-social__icon",
    ["mn-social-icon"])]);
}

/** <ul> of social links driven by the component props lineUrl, facebookUrl … (empty prop = hidden). */
export function socialList(label = "Social media"): Block {
  const items = SOCIALS.map(([key, name]) => cond(`If ${name}`, `props.${key}Url`, el("Item", "li", {}, null, [
    socialLink(name, `{props.${key}Url}`, key, name)])));
  return el("Social", "ul", { class: "main-social", "aria-label": label }, ["mn-social"], items);
}

// ================================================================ post card (blog archive + related posts)
export const CARD_STYLES: Styles = {
  "mn-card-grid": style(".main-card-grid", `display: grid;
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
  }`),
  "mn-card": style(".main-card", `position: relative;
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
  }`),
  "mn-card-media": style(".main-card__media", "margin: 0;"),
  "mn-card-img": style(".main-card__img", "inline-size: 100%;\n  block-size: auto;\n  aspect-ratio: 6 / 5;\n"
    + "  object-fit: cover;"),
  "mn-card-body": style(".main-card__body", "display: flex;\n  flex: 1;\n  flex-direction: column;\n"
    + "  gap: var(--space-xs);\n"
    + "  padding: var(--space-s) var(--space-m) var(--space-m);"),
  "mn-pill": style(".main-pill", `align-self: flex-start;
  padding: calc(var(--space-xs) / 2) var(--space-s);
  border-radius: var(--radius-circle, 999px);
  background-color: var(--main-primary);
  color: var(--main-on-primary);
  font-size: var(--text-xs);
  font-weight: 500;
  line-height: 1.6;`),
  "mn-card-title": style(".main-card__title", "font-size: var(--h5);\n  font-weight: 700;\n  line-height: 1.45;\n"
    + "  color: var(--main-text);"),
  "mn-card-link": style(".main-card__link", "color: inherit;\n  text-decoration: none;"),
  "acss-clickable-parent": style(".clickable-parent", ""),
  "mn-card-excerpt": style(".main-card__excerpt", `display: -webkit-box;
  overflow: hidden;
  font-size: var(--text-s);
  color: var(--main-text-muted);
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;`),
  "mn-card-more": style(".main-card__more", `margin-block-start: auto;
  padding-block-start: var(--space-xs);
  font-size: var(--text-s);
  font-weight: 700;
  color: var(--main-primary);`),
};

export function card(item: string, titleTag = "h2"): Block {
  return el("Card", "li", { class: "main-card" }, ["mn-card"], [
    cond("If image", `${item}.image.id`, el("Media", "figure", { class: "main-card__media" }, ["mn-card-media"], [
      img("Image", { class: "main-card__img", mediaId: `{${item}.image.id}`, loading: "lazy" }, ["mn-card-img"])])),
    el("Body", "div", { class: "main-card__body" }, ["mn-card-body"], [
      loop("Categories", "cat", [el("Pill", "span", { class: "main-pill" }, ["mn-pill"], [text("{cat.name}")])],
        null, `${item}.categories`),
      el("Title", titleTag, { class: "main-card__title" }, ["mn-card-title"], [
        el("Link", "a", { class: "main-card__link clickable-parent", href: `{${item}.permalink.relative}` },
          ["mn-card-link", "acss-clickable-parent"], [text(`{${item}.title}`)])]),
      cond("If excerpt", `${item}.excerpt`, el("Excerpt", "p", { class: "main-card__excerpt" },
        ["mn-card-excerpt"], [text(`{${item}.excerpt}`)])),
      el("More", "span", { class: "main-card__more", "aria-hidden": "true" }, ["mn-card-more"],
        [text("Read more →")]),
    ]),
  ]);
}

// ================================================================ image placeholder (empty dynamic image shows a tinted box)
export const MEDIA_STYLES: Styles = {
  "mn-media-img": style(".main-media__img", `/* image ratio: set --main-media-ratio on a parent */
  display: block;
  inline-size: 100%;
  block-size: auto;
  aspect-ratio: var(--main-media-ratio, 4 / 3);
  border-radius: var(--radius-m);
  background-color: var(--main-light-alt);
  object-fit: cover;`),
};

export function mediaImg(name = "Image", eager = false): Block {
  const a = { class: "main-media__img", mediaId: "", loading: eager ? "eager" : "lazy" };
  return img(name, a, ["mn-media-img"]);
}

/** Every template file carries the colour variables, so whichever file is pasted first creates them. */
export function kitPayload(gblock: Block, styles: Styles, components?: Record<string, any> | null,
                           loops?: Record<string, any> | null, now: () => string = nowIso): Payload {
  return payload(gblock, { ...COLORS, ...styles }, components, loops, now);
}

// ================================================================ button row + check list (hero, split, 404 …)
export const BUTTONS_STYLES: Styles = {
  "mn-buttons": style(".main-buttons", "display: flex;\n  flex-wrap: wrap;\n  align-items: center;\n"
    + "  gap: var(--space-s);"),
};

/** ACSS buttons carry no style record of their own, so their btn--* classes survive the paste. */
export function buttons(primaryLabel: string, primaryHref: string, outlineLabel: string, outlineHref: string): Block {
  return el("Buttons", "div", { class: "main-buttons" }, ["mn-buttons"], [
    el("Primary", "a", { class: "btn--primary", href: primaryHref }, null, [text(primaryLabel)]),
    el("Secondary", "a", { class: "btn--primary btn--outline", href: outlineHref }, null, [text(outlineLabel)]),
  ]);
}

export const CHECKS_STYLES: Styles = {
  "mn-checks": style(".main-checks", "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);\n"
    + "  margin: 0;\n  padding: 0;\n  list-style: none;"),
  "mn-checks-item": style(".main-checks__item", "display: flex;\n  align-items: flex-start;\n"
    + "  gap: var(--space-xs);"),
  "mn-checks-icon": style(".main-checks__icon", `flex: none;
  inline-size: 2.4rem;
  block-size: 2.4rem;
  padding: calc(var(--space-xs) / 2);
  border-radius: 50%;
  background-color: var(--main-accent-soft);
  color: var(--main-primary);`),
};

export function checks(items: string[]): Block {
  return el("Checks", "ul", { class: "main-checks" }, ["mn-checks"], items.map((t) =>
    el("Item", "li", { class: "main-checks__item" }, ["mn-checks-item"], [
      svg("Check icon", icon("check"), "main-checks__icon", ["mn-checks-icon"]),
      el("Text", "span", {}, null, [text(t)])])));
}
