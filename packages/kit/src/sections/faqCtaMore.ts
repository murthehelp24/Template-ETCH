/** FAQ variants (4) and CTA variants with a contact form (4). Port of _build/build_faq_cta_more.py.
 * Plain sections (edit the text in the blocks); colours come from kit COLORS. Lengths in rem are written for
 * 1rem = 10px and become to-rem() (portable).
 *
 * The form is plain HTML: it posts to the URL in its action attribute (FORM_ACTION — a Formspree form, a
 * form plugin's endpoint …), so set that after pasting, or swap the form for your form plugin's block. */
import { type Attrs, type Block, type Payload, type Styles, el, img, nowIso, style, svg, text } from "../etch/lib";
import { BAND_STYLES, BASE, BUTTONS_STYLES, CHECKS_STYLES, CON, HEADING_STYLES, MEDIA_STYLES, SEC, checks, heading,
  icon, kitPayload, mediaImg } from "../kit";

const FAQ: [string, string][] = [
  ["What services do you offer?", "Briefly list your main services and who they are for."],
  ["Do I need to book in advance?", "Explain how to book — phone, LINE or the contact form — and walk-in policy."],
  ["How much does it cost?", "Give a price range or explain how pricing is decided."],
  ["Which payment methods do you accept?", "Cash, bank transfer, credit card, QR payment …"],
  ["How long does it take?", "Typical time for a first visit or project."],
  ["Is there parking?", "Parking details or nearby public transport."],
];
const LIST_RESET = "margin: 0;\n  padding: 0;\n  list-style: none;";
const TWO_COL = `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 36rem), 1fr));
  gap: var(--container-gap);
  align-items: center;`;
const ON_DARK = `color: var(--main-on-primary);

  :is(h1, h2, h3, h4, h5, h6),
  .main-heading__eyebrow {
    color: inherit;
  }

  .main-heading__intro {
    color: var(--main-on-primary-muted);
  }`;

/** extra: more classes on the section (their style ids go in styleIds); behind: blocks before the container */
function section(name: string, cls: string, styleIds: string[], children: Block[], conCls: string | null = null,
                 conIds: string[] = [], extra: string[] = [], behind: Block[] = []): Block {
  const con = conCls ? { ...CON, class: conCls } : CON;
  return el(name, "section", { ...SEC, class: [cls, ...extra].join(" ") }, ["etch-section-style", ...styleIds], [
    ...behind, el("Container", "div", con, ["etch-container-style", ...conIds], children)]);
}

type Build = (now: () => string) => Payload;

// ================================================================================================ FAQ
/** <details> list: native open / close, no script */
function accordion(b: string, p: string, items: [string, string][] = FAQ, openFirst = true): Block {
  const item = (n: number, q: string, a: string) => {
    const attrs = { class: `${b}__item`, ...(openFirst && n === 0 ? { open: "" } : {}) };
    return el("Item", "details", attrs, [p + "-item"], [
      el("Question", "summary", { class: `${b}__question` }, [p + "-question"], [text(q)]),
      el("Answer", "div", { class: `${b}__answer` }, [p + "-answer"], [el("Text", "p", {}, null, [text(a)])]),
    ]);
  };
  return el("List", "div", { class: `${b}__list` }, [p + "-list"], items.map(([q, a], n) => item(n, q, a)));
}

const SUMMARY_RESET = `display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-s);
  font-weight: 600;
  cursor: pointer;
  list-style: none;

  &::-webkit-details-marker {
    display: none;
  }`;

/** the round + / − marker after the question */
function plus(size: string, bg: string, fg: string, openBg: string, openFg: string): string {
  return `

  &::after {
    content: "+";
    display: grid;
    flex: none;
    place-items: center;
    inline-size: ${size};
    block-size: ${size};
    border-radius: 50%;
    background-color: ${bg};
    color: ${fg};
    font-size: var(--text-l);
    line-height: 1;
    transition: background-color 0.2s ease, color 0.2s ease;
  }

  [open] > &::after {
    content: "−";
    background-color: ${openBg};
    color: ${openFg};
  }`;
}

// ---------------------------------------------------------------- 1. heading + contact box left, accordion right
const faqSplit: Build = (now) => {
  const p = "mn-fqs", b = "main-faq-split";
  return kitPayload(section("FAQ Split", b, [p], [
    el("Grid", "div", { class: `${b}__grid` }, [p + "-grid"], [
      el("Intro", "div", { class: `${b}__intro` }, [p + "-intro"], [
        heading("FAQ", "Frequently asked questions", "Can't find your answer? Ask us directly."),
        el("Box", "div", { class: `${b}__box` }, [p + "-box"], [
          el("Box Title", "p", { class: `${b}__box-title` }, [p + "-box-title"], [text("Still have questions?")]),
          el("Box Text", "p", { class: `${b}__box-text` }, [p + "-box-text"],
            [text("Our team replies within a few hours.")]),
          el("Button", "a", { class: "btn--secondary", href: "/contact/" }, null, [text("Contact us")]),
        ]),
      ]),
      accordion(b, p),
    ])]), { ...BASE, ...HEADING_STYLES,
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
  gap: var(--space-l);

  @media (width <= 992px) {
    position: static;
  }`),
    [p + "-box"]: style(`.${b}__box`, `display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-xs);
  padding: var(--space-m);
  border-radius: var(--radius-m);
  background-color: var(--main-primary);
  color: var(--main-on-primary);

  .btn--secondary {
    margin-block-start: var(--space-xs);
  }`),
    [p + "-box-title"]: style(`.${b}__box-title`, "margin: 0;\n  font-size: var(--h4);\n  font-weight: 700;"),
    [p + "-box-text"]: style(`.${b}__box-text`, "margin: 0;\n  color: var(--main-on-primary-muted);"),
    [p + "-list"]: style(`.${b}__list`, "display: flex;\n  flex-direction: column;\n"
      + "  border-block-start: 1px solid var(--main-line);"),
    [p + "-item"]: style(`.${b}__item`, "border-block-end: 1px solid var(--main-line);"),
    [p + "-question"]: style(`.${b}__question`, SUMMARY_RESET + `
  padding-block: var(--space-m);
  font-size: var(--text-l);
  color: var(--main-text);` + plus("3.6rem", "var(--main-accent-soft)", "var(--main-primary)",
      "var(--main-primary)", "var(--main-on-primary)")),
    [p + "-answer"]: style(`.${b}__answer`, `padding-block-end: var(--space-m);
  padding-inline-end: var(--space-xl);
  color: var(--main-text-muted);

  p {
    margin: 0;
  }`),
  }, null, null, now);
};

// ---------------------------------------------------------------- 2. all answers shown, two columns of cards
const faqCards: Build = (now) => {
  const p = "mn-fqc", b = "main-faq-cards";
  return kitPayload(section("FAQ Cards", b, [p], [
    heading("FAQ", "Frequently asked questions", "Quick answers to the questions we hear most.", "h2", true),
    el("Grid", "ul", { class: `${b}__grid` }, [p + "-grid"], FAQ.map(([q, a]) =>
      el("Card", "li", { class: `${b}__card` }, [p + "-card"], [
        el("Question", "h3", { class: `${b}__question` }, [p + "-question"], [text(q)]),
        el("Answer", "p", { class: `${b}__answer` }, [p + "-answer"], [text(a)]),
      ]))),
  ], `${b}__container`, [p + "-container"]), { ...BASE, ...HEADING_STYLES,
    [p]: style(`.${b}`, "background-color: var(--main-light-alt);"),
    [p + "-container"]: style(`.${b}__container`, "gap: var(--container-gap);"),
    [p + "-grid"]: style(`.${b}__grid`, `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 40rem), 1fr));
  gap: var(--grid-gap);
  ` + LIST_RESET),
    [p + "-card"]: style(`.${b}__card`, `display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  padding: var(--space-m);
  border-inline-start: 4px solid var(--main-accent);
  border-radius: var(--radius-m);
  background-color: var(--main-light);
  box-shadow: 0 0.4rem 1.2rem var(--main-shadow);`),
    [p + "-question"]: style(`.${b}__question`, `display: flex;
  gap: var(--space-xs);
  margin: 0;
  font-size: var(--h5);
  color: var(--main-primary);

  &::before {
    content: "Q.";
    flex: none;
    color: var(--main-accent);
  }`),
    [p + "-answer"]: style(`.${b}__answer`, "margin: 0;\n  color: var(--main-text-muted);"),
  }, null, null, now);
};

// ---------------------------------------------------------------- 3. centred, lines only, numbered questions
const faqMinimal: Build = (now) => {
  const p = "mn-fqm", b = "main-faq-minimal";
  return kitPayload(section("FAQ Minimal", b, [p], [
    heading("FAQ", "Frequently asked questions", null, "h2", true),
    accordion(b, p),
    el("More", "p", { class: `${b}__more` }, [p + "-more"], [
      text("More questions? "),
      el("Link", "a", { class: `${b}__link`, href: "/contact/" }, [p + "-link"], [text("Contact us →")]),
    ]),
  ], `${b}__container`, [p + "-container"]), { ...BASE, ...HEADING_STYLES,
    [p]: style(`.${b}`, "background-color: var(--main-light);"),
    [p + "-container"]: style(`.${b}__container`, "gap: var(--space-l);"),
    [p + "-list"]: style(`.${b}__list`, `inline-size: 100%;
  max-inline-size: 82rem;
  margin-inline: auto;
  counter-reset: main-faq;`),
    [p + "-item"]: style(`.${b}__item`, "border-block-end: 1px solid var(--main-line);\n"
      + "  counter-increment: main-faq;"),
    [p + "-question"]: style(`.${b}__question`, SUMMARY_RESET + `
  justify-content: flex-start;
  padding-block: var(--space-m);
  font-size: var(--text-l);
  color: var(--main-text);

  /* 01, 02 … before the question */
  &::before {
    content: counter(main-faq, decimal-leading-zero);
    flex: none;
    min-inline-size: 3.6rem;
    font-weight: 800;
    color: var(--main-accent);
  }` + plus("3.2rem", "transparent", "var(--main-primary)", "var(--main-accent)", "var(--main-on-primary)")
      + `

  &::after {
    margin-inline-start: auto;
    border: 1.5px solid var(--main-line);
  }`),
    [p + "-answer"]: style(`.${b}__answer`, `padding: 0 var(--space-xl) var(--space-m) 3.6rem;
  padding-inline-start: calc(3.6rem + var(--space-s));
  color: var(--main-text-muted);

  p {
    margin: 0;
  }`),
    [p + "-more"]: style(`.${b}__more`, "margin: 0;\n  text-align: center;\n  color: var(--main-text-muted);"),
    [p + "-link"]: style(`.${b}__link`, `font-weight: 700;
  color: var(--main-primary);
  text-decoration-color: var(--main-accent);
  text-underline-offset: 0.4rem;`),
  }, null, null, now);
};

// ---------------------------------------------------------------- 4. photo left, accordion of soft boxes right
const faqImage: Build = (now) => {
  const p = "mn-fqi", b = "main-faq-image";
  return kitPayload(section("FAQ Image", b, [p], [
    el("Grid", "div", { class: `${b}__grid` }, [p + "-grid"], [
      el("Media", "figure", { class: `${b}__media` }, [p + "-media"], [mediaImg()]),
      el("Content", "div", { class: `${b}__content` }, [p + "-content"], [
        heading("FAQ", "Frequently asked questions", "Everything you need to know before your first visit."),
        accordion(b, p, FAQ.slice(0, 5)),
      ]),
    ])]), { ...BASE, ...HEADING_STYLES, ...MEDIA_STYLES,
    [p]: style(`.${b}`, "background-color: var(--main-light);"),
    [p + "-grid"]: style(`.${b}__grid`, `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 40rem), 1fr));
  gap: var(--container-gap);
  align-items: start;`),
    [p + "-media"]: style(`.${b}__media`, "--main-media-ratio: 4 / 5;\n  margin: 0;"),
    [p + "-content"]: style(`.${b}__content`, "display: flex;\n  flex-direction: column;\n  gap: var(--space-l);"),
    [p + "-list"]: style(`.${b}__list`, "display: flex;\n  flex-direction: column;\n  gap: var(--space-xs);"),
    [p + "-item"]: style(`.${b}__item`, `border-radius: var(--radius-m);
  background-color: var(--main-light-alt);
  transition: background-color 0.2s ease;

  &[open] {
    background-color: var(--main-accent-soft);
  }`),
    [p + "-question"]: style(`.${b}__question`, SUMMARY_RESET + `
  padding: var(--space-s) var(--space-m);
  color: var(--main-primary);` + plus("3.2rem", "var(--main-light)", "var(--main-primary)",
      "var(--main-primary)", "var(--main-on-primary)")),
    [p + "-answer"]: style(`.${b}__answer`, `padding: 0 var(--space-m) var(--space-s);
  color: var(--main-text);

  p {
    margin: 0;
  }`),
  }, null, null, now);
};

// ================================================================================================ CTA + FORM
const FORM_ACTION = "https://formspree.io/f/your-form-id"; // replace with your form endpoint after pasting
const FORM_STYLES: Styles = {
  "mn-form": style(".main-form", `/* plain HTML form: set its action to your form endpoint (Formspree, a form plugin …) */
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-s);
  inline-size: 100%;

  @media (width <= 600px) {
    grid-template-columns: 1fr;
  }`),
  "mn-form-field": style(".main-form__field", "display: flex;\n  flex-direction: column;\n"
    + "  gap: calc(var(--space-xs) / 2);"),
  "mn-form-wide": style(".main-form__field--wide", "grid-column: 1 / -1;"),
  "mn-form-label": style(".main-form__label", "font-size: var(--text-s);\n  font-weight: 600;\n"
    + "  color: var(--main-text);"),
  "mn-form-input": style(".main-form__input", `inline-size: 100%;
  padding: 1.2rem 1.4rem;
  border: 1px solid var(--main-line);
  border-radius: var(--radius-s);
  background-color: var(--main-light);
  color: var(--main-text);
  font: inherit;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;

  &::placeholder {
    color: var(--main-text-muted);
  }

  &:focus {
    outline: none;
    border-color: var(--main-primary);
    box-shadow: 0 0 0 3px var(--main-accent-soft);
  }

  &:is(textarea) {
    min-block-size: 12rem;
    resize: vertical;
  }`),
  "mn-form-submit": style(".main-form__submit", "grid-column: 1 / -1;"),
  "mn-form-note": style(".main-form__note", "grid-column: 1 / -1;\n  margin: 0;\n  font-size: var(--text-s);\n"
    + "  color: var(--main-text-muted);"),
  "mn-form-card": style(".main-form-card", `display: flex;
  flex-direction: column;
  gap: var(--space-m);
  padding: var(--space-l);
  border-radius: var(--radius-l);
  background-color: var(--main-light);
  color: var(--main-text);
  box-shadow: 0 1.2rem 2.8rem var(--main-shadow);

  /* stays primary inside a dark section, whose headings inherit the light text colour */
  & .main-form-card__title {
    color: var(--main-primary);
  }

  @media (width <= 600px) {
    padding: var(--space-m);
  }`),
  "mn-form-card-title": style(".main-form-card__title", "margin: 0;\n  font-size: var(--h4);"),
};

interface FieldOpts { tag?: string; typ?: string; wide?: boolean; required?: boolean; placeholder?: string }

function field(name: string, label: string, fid: string,
               { tag = "input", typ = "text", wide = false, required = false, placeholder = "" }: FieldOpts = {}): Block {
  const cls = "main-form__field" + (wide ? " main-form__field--wide" : "");
  const ids = ["mn-form-field", ...(wide ? ["mn-form-wide"] : [])];
  const attrs: Attrs = { class: "main-form__input", id: fid, name: fid, placeholder };
  if (tag === "input") attrs.type = typ;
  if (required) attrs.required = "";
  return el(name, "div", { class: cls }, ids, [
    el("Label", "label", { class: "main-form__label", for: fid }, ["mn-form-label"],
      [text(label + (required ? " *" : ""))]),
    el("Input", tag, attrs, ["mn-form-input"]),
  ]);
}

/** key: makes the field ids unique when two forms share a page */
function form(key: string, cardTitle: string | null = null, compact = false): Block {
  const fields = [
    field("Name", "Name", `${key}-name`, { required: true, placeholder: "Your name" }),
    field("Phone", "Phone", `${key}-phone`, { typ: "tel", required: true, placeholder: "08x-xxx-xxxx" }),
  ];
  if (!compact) {
    fields.push(field("Email", "Email", `${key}-email`, { typ: "email", wide: true,
      placeholder: "you@example.com" }));
  }
  fields.push(field("Message", "Message", `${key}-message`, { tag: "textarea", wide: true,
    placeholder: "How can we help?" }));
  fields.push(el("Submit Row", "div", { class: "main-form__submit" }, ["mn-form-submit"], [
    el("Submit", "button", { class: "btn--primary", type: "submit" }, null, [text("Send message")])]));
  fields.push(el("Note", "p", { class: "main-form__note" }, ["mn-form-note"],
    [text("We reply within one business day. Your details stay private.")]));
  const f = el("Form", "form", { class: "main-form", action: FORM_ACTION, method: "post" }, ["mn-form"], fields);
  if (cardTitle === null) return f;
  return el("Form Card", "div", { class: "main-form-card" }, ["mn-form-card"], [
    el("Card Title", "h3", { class: "main-form-card__title" }, ["mn-form-card-title"], [text(cardTitle)]), f]);
}

type ContactRow = [string, string, string, string | null];
const CONTACTS: ContactRow[] = [["phone", "Phone", "02-000-0000", "tel:020000000"],
  ["line-box", "LINE", "@example", "https://line.me/R/ti/p/@example"],
  ["email", "Email", "hello@example.com", "mailto:hello@example.com"],
  ["hours", "Hours", "Mon–Sat 09:00–18:00", null]];

function contactList(b: string, p: string, rows: ContactRow[] = CONTACTS): Block {
  const row = ([ic, label, value, href]: ContactRow) => {
    const val = href
      ? el("Link", "a", { class: `${b}__link`, href,
        ...(href.startsWith("http") ? { target: "_blank", rel: "noopener" } : {}) }, [p + "-link"], [text(value)])
      : el("Value", "span", {}, null, [text(value)]);
    return el("Item", "li", { class: `${b}__item` }, [p + "-item"], [
      svg("Icon", icon(ic), `${b}__icon`, [p + "-icon"]),
      el("Body", "div", { class: `${b}__body` }, [p + "-body"], [
        el("Label", "span", { class: `${b}__label` }, [p + "-label"], [text(label)]), val])]);
  };
  return el("Contacts", "ul", { class: `${b}__contacts` }, [p + "-contacts"], rows.map(row));
}

function contactStyles(p: string, b: string, onDark = false): Styles {
  return {
    [p + "-contacts"]: style(`.${b}__contacts`, "display: flex;\n  flex-direction: column;\n"
      + "  gap: var(--space-s);\n  " + LIST_RESET),
    [p + "-item"]: style(`.${b}__item`, "display: flex;\n  align-items: center;\n  gap: var(--space-s);"),
    [p + "-icon"]: style(`.${b}__icon`, `flex: none;
  inline-size: 4.8rem;
  block-size: 4.8rem;
  padding: 1.2rem;
  border-radius: 50%;
  background-color: ` + (onDark ? "var(--main-accent);\n  color: var(--main-on-primary);"
      : "var(--main-accent-soft);\n  color: var(--main-primary);")),
    [p + "-body"]: style(`.${b}__body`, "display: flex;\n  flex-direction: column;"),
    [p + "-label"]: style(`.${b}__label`, "font-size: var(--text-s);\n  color: "
      + (onDark ? "var(--main-on-primary-muted);" : "var(--main-text-muted);")),
    [p + "-link"]: style(`.${b}__link`, `font-weight: 700;
  color: inherit;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
    text-decoration-color: var(--main-accent);
  }`),
  };
}

const CTA_HEAD: [string, string, string] = ["Contact us", "Let's talk about what you need",
  "Send us a message and we'll get back to you, or reach us directly by phone or LINE."];

// ---------------------------------------------------------------- 1. contact details left, form card right
const ctaForm: Build = (now) => {
  const p = "mn-cfs", b = "main-cta-form";
  return kitPayload(section("CTA Form", b, [p], [
    el("Grid", "div", { class: `${b}__grid` }, [p + "-grid"], [
      el("Info", "div", { class: `${b}__info` }, [p + "-info"], [heading(...CTA_HEAD), contactList(b, p)]),
      form("cta-form", "Send us a message"),
    ])]), { ...BASE, ...HEADING_STYLES, ...FORM_STYLES, ...contactStyles(p, b),
    [p]: style(`.${b}`, "background-color: var(--main-light-alt);"),
    [p + "-grid"]: style(`.${b}__grid`, `display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 3fr);
  gap: var(--container-gap);
  align-items: center;

  @media (width <= 992px) {
    grid-template-columns: 1fr;
  }`),
    [p + "-info"]: style(`.${b}__info`, "display: flex;\n  flex-direction: column;\n  gap: var(--space-l);"),
  }, null, null, now);
};

// ---------------------------------------------------------------- 2. on the primary colour: text + checks + phone, form card
const ctaFormBand: Build = (now) => {
  const p = "mn-cfb", b = "main-cta-form-band";
  return kitPayload(section("CTA Form Band", b, [p, "mn-band"], [
    el("Grid", "div", { class: `${b}__grid` }, [p + "-grid"], [
      el("Info", "div", { class: `${b}__info` }, [p + "-info"], [
        heading("Free consultation", "Book your free consultation today",
          "Tell us a little about what you need. We'll call you back to find the best option."),
        checks(["No cost, no obligation", "Reply within one business day", "Friendly, expert team"]),
        el("Call", "a", { class: `${b}__call`, href: "tel:020000000" }, [p + "-call"], [
          svg("Phone icon", icon("phone"), `${b}__call-icon`, [p + "-call-icon"]),
          el("Call Text", "span", { class: `${b}__call-text` }, [p + "-call-text"], [
            el("Call Label", "small", {}, null, [text("Or call us now")]),
            el("Call Number", "b", {}, null, [text("02-000-0000")]),
          ]),
        ]),
      ]),
      form("cta-band", "Request a call back", true),
    ])], null, [], ["main-band"]), { ...BASE, ...HEADING_STYLES, ...CHECKS_STYLES, ...BAND_STYLES,
    ...FORM_STYLES,
    [p]: style(`.${b}`, `.main-checks__icon {
    background-color: var(--main-accent);
    color: var(--main-on-primary);
  }`),
    [p + "-grid"]: style(`.${b}__grid`, TWO_COL),
    [p + "-info"]: style(`.${b}__info`, "display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n"
      + "  gap: var(--content-gap);"),
    [p + "-call"]: style(`.${b}__call`, `display: flex;
  align-items: center;
  gap: var(--space-s);
  color: inherit;
  text-decoration: none;

  &:hover b {
    color: var(--main-accent);
  }`),
    [p + "-call-icon"]: style(`.${b}__call-icon`, `inline-size: 5.6rem;
  block-size: 5.6rem;
  padding: 1.5rem;
  border: 1.5px solid var(--main-line-on-primary);
  border-radius: 50%;`),
    [p + "-call-text"]: style(`.${b}__call-text`, `display: flex;
  flex-direction: column;

  small {
    color: var(--main-on-primary-muted);
  }

  b {
    font-size: var(--h4);
    transition: color 0.2s ease;
  }`),
  }, null, null, now);
};

// ---------------------------------------------------------------- 3. photo behind, text left, form card right
const ctaFormImage: Build = (now) => {
  const p = "mn-cfi", b = "main-cta-form-image";
  return kitPayload(section("CTA Form Image", b, [p], [
    el("Grid", "div", { class: `${b}__grid` }, [p + "-grid"], [
      el("Info", "div", { class: `${b}__info` }, [p + "-info"], [
        heading(...CTA_HEAD),
        el("Buttons", "div", { class: "main-buttons" }, ["mn-buttons"], [
          el("LINE", "a", { class: "btn--secondary", href: "https://line.me/R/ti/p/@example",
            target: "_blank", rel: "noopener" }, null, [text("Chat on LINE")]),
          el("Phone", "a", { class: "btn--secondary btn--outline", href: "tel:020000000" }, null,
            [text("02-000-0000")]),
        ]),
      ]),
      form("cta-image", "Send us a message"),
    ])], null, [], [], [el("Background", "figure", { class: `${b}__bg` }, [p + "-bg"], [
    img("Background Image", { class: `${b}__img`, mediaId: "", loading: "lazy" }, [p + "-img"])])]),
  { ...BASE, ...HEADING_STYLES, ...BUTTONS_STYLES, ...FORM_STYLES,
    [p]: style(`.${b}`, `position: relative;
  isolation: isolate;
  overflow: hidden;

  /* the photo is darkened with the primary colour, strongest on the left behind the text */
  &::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: -1;
    background: linear-gradient(90deg, color-mix(in srgb, var(--main-primary) 92%, transparent) 30%,
      color-mix(in srgb, var(--main-primary) 55%, transparent));
  }

  ` + ON_DARK),
    [p + "-bg"]: style(`.${b}__bg`, "position: absolute;\n  inset: 0;\n  z-index: -2;\n  margin: 0;"),
    [p + "-img"]: style(`.${b}__img`, `display: block;
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
  background-color: var(--main-primary);`),
    [p + "-grid"]: style(`.${b}__grid`, TWO_COL),
    [p + "-info"]: style(`.${b}__info`, "display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n"
      + "  gap: var(--content-gap);"),
  }, null, null, now);
};

// ---------------------------------------------------------------- 4. heading, then form + map side by side, contacts below
const ctaFormMap: Build = (now) => {
  const p = "mn-cfm", b = "main-cta-form-map";
  const rows: ContactRow[] = [["address", "Address", "123 Example Road, Bangkok 10110", "https://maps.google.com/"],
    ...CONTACTS.slice(0, 3)];
  return kitPayload(section("CTA Form Map", b, [p], [
    heading(...CTA_HEAD, "h2", true),
    el("Grid", "div", { class: `${b}__grid` }, [p + "-grid"], [
      form("cta-map"),
      el("Map", "iframe", { class: `${b}__map`, src: "https://www.google.com/maps?q=Bangkok&output=embed",
        title: "Map", loading: "lazy", referrerpolicy: "no-referrer-when-downgrade" }, [p + "-map"]),
    ]),
    contactList(b, p, rows),
  ], `${b}__container`, [p + "-container"]), { ...BASE, ...HEADING_STYLES, ...FORM_STYLES, ...contactStyles(p, b),
    [p]: style(`.${b}`, "background-color: var(--main-light);"),
    [p + "-container"]: style(`.${b}__container`, "gap: var(--container-gap);"),
    [p + "-grid"]: style(`.${b}__grid`, `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 40rem), 1fr));
  gap: var(--container-gap);
  align-items: stretch;`),
    // the contact row under the form + map runs across instead of down (keeps its place from contactStyles)
    [p + "-contacts"]: style(`.${b}__contacts`, `display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 24rem), 1fr));
  gap: var(--space-m);
  padding-block-start: var(--space-l);
  border-block-start: 1px solid var(--main-line);
  ` + LIST_RESET),
    [p + "-map"]: style(`.${b}__map`, `display: block;
  inline-size: 100%;
  block-size: 100%;
  min-block-size: 36rem;
  border: 0;
  border-radius: var(--radius-m);
  background-color: var(--main-light-alt);`),
  }, null, null, now);
};

/** The eight templates of build_faq_cta_more.py, in its output order. */
export function build(now: () => string = nowIso): Record<string, Payload> {
  return {
    "main-faq-split": faqSplit(now),
    "main-faq-cards": faqCards(now),
    "main-faq-minimal": faqMinimal(now),
    "main-faq-image": faqImage(now),
    "main-cta-form": ctaForm(now),
    "main-cta-form-band": ctaFormBand(now),
    "main-cta-form-image": ctaFormImage(now),
    "main-cta-form-map": ctaFormMap(now),
  };
}
