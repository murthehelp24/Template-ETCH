"""FAQ, CTA split, Blog archive, Single post and Contact page (main-* family). Colours come from kit.COLORS."""
import json, os, sys
from lib_etch import el, text, svg, img, cond, loop, block, style, prop, write
from kit import (SEC, CON, BASE, HEADING_STYLES, SOCIAL_STYLES, SOCIAL_PROPS, CARD_STYLES, heading, social_list,
                 social_link, card, icon, kit_payload)

S, OUT = sys.argv[1], sys.argv[2]
src = json.load(open(f"{S}/src5.json"))
os.makedirs(OUT, exist_ok=True)


def find(b, pred, out=None):
    out = [] if out is None else out
    if pred(b):
        out.append(b)
    for c in b.get("innerBlocks", []):
        find(c, pred, out)
    return out


CONTACT_PROPS = [
    prop("Address", "address", "123 Example Road, Bangkok 10110", "Empty = hidden. Line breaks are kept"),
    prop("Opening Hours", "hours", "Mon–Sat 09:00–18:00", "Empty = hidden"),
    prop("Phone", "phone", "02-000-0000", "Empty = hidden"),
    prop("Email", "email", "hello@example.com", "Empty = hidden"),
    prop("Map URL", "mapUrl", "https://maps.google.com/", "Link that opens Google Maps"),
    prop("Map Embed URL", "mapEmbedUrl", "https://www.google.com/maps?q=Bangkok&output=embed",
         "Google Maps → Share → Embed a map → copy the src. Empty = no map"),
]
MAP_CSS = """display: block;
  inline-size: 100%;
  block-size: clamp(36rem, 40vw, 52rem);
  border: 0;
  border-radius: var(--radius-s);
  background-color: var(--main-light-alt);"""


def label_value(label_cls, label_ids, label, value_children):
    return [el("Label", "span", {"class": label_cls}, label_ids, [text(label)])] + value_children


outputs = {}

# ================================================================ 1. FAQ (plain section)
FAQ = [
    ("What services do you offer?", "Briefly list your main services and who they are for."),
    ("Do I need to book in advance?", "Explain how to book — phone, LINE or the contact form — and walk-in policy."),
    ("How much does it cost?", "Give a price range or explain how pricing is decided."),
    ("Which payment methods do you accept?", "Cash, bank transfer, credit card, QR payment …"),
    ("How long does it take?", "Typical time for a first visit or project."),
    ("Is there parking?", "Parking details or nearby public transport."),
]
faq_styles = {**BASE, **HEADING_STYLES,
    "mn-faq": style(".main-faq", "background-color: var(--main-light);"),
    "mn-faq-container": style(".main-faq__container", "gap: var(--space-l);"),
    "mn-faq-list": style(".main-faq__list", """display: flex;
  flex-direction: column;
  gap: var(--space-s);
  inline-size: 100%;
  max-inline-size: 82rem;
  margin-inline: auto;"""),
    "mn-faq-item": style(".main-faq__item", """overflow: hidden;
  background-color: var(--main-primary);
  color: var(--main-on-primary);
  border: 1px solid transparent;
  border-radius: var(--radius-m);
  transition: border-color 0.2s ease;

  &:hover,
  &[open] {
    border-color: var(--main-accent);
  }

  &[open] .main-faq__question::after {
    content: "−";
    background-color: var(--main-accent);
  }"""),
    "mn-faq-question": style(".main-faq__question", """display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-s);
  padding: var(--space-s) var(--space-m);
  font-weight: 600;
  cursor: pointer;
  list-style: none;

  &::-webkit-details-marker {
    display: none;
  }

  &::after {
    content: "+";
    display: grid;
    flex: none;
    place-items: center;
    inline-size: 3.2rem;
    block-size: 3.2rem;
    border-radius: 50%;
    background-color: var(--main-line-on-primary);
    font-size: var(--text-l);
    line-height: 1;
    transition: background-color 0.2s ease;
  }

  @media (width <= 768px) {
    padding-inline: var(--space-s);
  }"""),
    "mn-faq-answer": style(".main-faq__answer", """padding: var(--space-s) var(--space-m);
  background-color: var(--main-light);
  color: var(--main-text);

  @media (width <= 768px) {
    padding-inline: var(--space-s);
  }"""),
}
faq = el("FAQ", "section", {**SEC, "class": "main-faq"}, ["etch-section-style", "mn-faq"], [
    el("Container", "div", {**CON, "class": "main-faq__container"}, ["etch-container-style", "mn-faq-container"], [
        heading("FAQ", "Frequently asked questions", center=True),
        el("List", "div", {"class": "main-faq__list"}, ["mn-faq-list"], [
            el("Item", "details", {"class": "main-faq__item"}, ["mn-faq-item"], [
                el("Question", "summary", {"class": "main-faq__question"}, ["mn-faq-question"], [text(q)]),
                el("Answer", "div", {"class": "main-faq__answer"}, ["mn-faq-answer"], [
                    el("Text", "p", {}, None, [text(a)])]),
            ]) for q, a in FAQ]),
    ])])
outputs["main-faq"] = kit_payload(faq, faq_styles)

# ================================================================ 2. CTA / Contact split (component)
CTA_ID = 990101
cta_styles = {**BASE, **HEADING_STYLES, **SOCIAL_STYLES,
    "mn-cta": style(".main-cta", "background-color: var(--main-light-alt);"),
    "mn-cta-container": style(".main-cta__container", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 36rem), 1fr));
  gap: var(--container-gap);
  align-items: center;"""),
    "mn-cta-content": style(".main-cta__content", """display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--content-gap);"""),
    "mn-cta-list": style(".main-cta__list", """display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  margin: 0;
  padding: 0;
  list-style: none;
  color: var(--main-text-muted);
  white-space: pre-line;"""),
    "mn-cta-label": style(".main-cta__label", "font-weight: 600;\n  color: var(--main-primary);"),
    "mn-cta-link": style(".main-cta__link", "color: var(--main-primary);"),
    "mn-cta-buttons": style(".main-cta__buttons", """display: flex;
  flex-wrap: wrap;
  gap: var(--space-s);

  > a {
    align-items: center;
  }"""),
    "mn-btn-icon": style(".main-btn-icon", """display: block;
  inline-size: 1.4em;
  block-size: 1.4em;
  flex-shrink: 0;
  margin-inline-end: var(--space-xs);"""),
    "mn-cta-map": style(".main-cta__map", MAP_CSS),
}


def cta_row(name, prop_key, label_key, value):
    return cond(f"If {name}", f"props.{prop_key}", el(name, "li", {}, None,
        label_value("main-cta__label", ["mn-cta-label"], f"{{props.{label_key}}} ", value)))


cta_blocks = [el("CTA Split", "section", {**SEC, "class": "main-cta"}, ["etch-section-style", "mn-cta"], [
    el("Container", "div", {**CON, "class": "main-cta__container"}, ["etch-container-style", "mn-cta-container"], [
        el("Content", "div", {"class": "main-cta__content"}, ["mn-cta-content"], [
            heading("{props.eyebrow}", "{props.title}", "{props.intro}"),
            el("List", "ul", {"class": "main-cta__list"}, ["mn-cta-list"], [
                cta_row("Address", "address", "addressLabel", [text("{props.address}")]),
                cta_row("Hours", "hours", "hoursLabel", [text("{props.hours}")]),
                cta_row("Phone", "phone", "phoneLabel", [el("Link", "a", {"class": "main-cta__link",
                        "href": "tel:{props.phone}"}, ["mn-cta-link"], [text("{props.phone}")])]),
                cta_row("Email", "email", "emailLabel", [el("Link", "a", {"class": "main-cta__link",
                        "href": "mailto:{props.email}"}, ["mn-cta-link"], [text("{props.email}")])]),
                cta_row("Map", "mapUrl", "mapLabel", [el("Link", "a", {"class": "main-cta__link",
                        "href": "{props.mapUrl}", "target": "_blank", "rel": "noopener"}, ["mn-cta-link"],
                        [text("{props.mapLinkText}")])]),
            ]),
            social_list(),
            el("Buttons", "div", {"class": "main-cta__buttons"}, ["mn-cta-buttons"], [
                cond("If LINE", "props.lineUrl", el("LINE", "a", {"class": "btn--primary", "href": "{props.lineUrl}",
                     "target": "_blank", "rel": "noopener"}, None, [
                    svg("LINE icon", icon("line-button"), "main-btn-icon", ["mn-btn-icon"]),
                    text("{props.lineButton}")])),
                cond("If phone", "props.phone", el("Phone", "a", {"class": "btn--primary btn--outline",
                     "href": "tel:{props.phone}"}, None, [text("{props.phoneButton} {props.phone}")])),
            ]),
        ]),
        cond("If map embed", "props.mapEmbedUrl", el("Map", "iframe", {
            "class": "main-cta__map", "src": "{props.mapEmbedUrl}", "title": "{props.title}", "loading": "lazy",
            "referrerpolicy": "no-referrer-when-downgrade"}, ["mn-cta-map"])),
    ])])]
cta_component = {"id": CTA_ID, "legacyId": "", "name": "Main CTA", "key": "MainCta",
                 "description": "Contact / call-to-action split: heading, contact details, social, buttons and map.",
                 "blocks": cta_blocks, "properties": [
                     prop("Eyebrow", "eyebrow", "Contact us"),
                     prop("Title", "title", "Talk to us today"),
                     prop("Intro", "intro", "One or two sentences that invite the visitor to get in touch."),
                     *CONTACT_PROPS,
                     prop("Map Link Text", "mapLinkText", "Open Google Maps"),
                     prop("LINE Button", "lineButton", "Chat on LINE"),
                     prop("Phone Button", "phoneButton", "Call"),
                     prop("Address Label", "addressLabel", "Address"),
                     prop("Hours Label", "hoursLabel", "Hours"),
                     prop("Phone Label", "phoneLabel", "Phone"),
                     prop("Email Label", "emailLabel", "Email"),
                     prop("Map Label", "mapLabel", "Map"),
                     *SOCIAL_PROPS]}
cta_instance = block("etch/component", {"ref": CTA_ID, "attributes": {}})
outputs["main-cta"] = kit_payload(cta_instance, cta_styles, {str(CTA_ID): cta_component})

# ================================================================ 3. Blog archive (plain section)
query_block = find(list(src["blogPage"][0]["components"].values())[0]["blocks"][0],
                   lambda b: b["blockName"] == "core/query")[0]
blog_styles = {**BASE, **CARD_STYLES,
    "mn-blog": style(".main-blog", "background-color: var(--main-light-alt);"),
    "mn-blog-container": style(".main-blog__container", "gap: var(--space-l);"),
    "mn-blog-title": style(".main-blog__title", """align-self: center;
  font-size: var(--h1);
  font-weight: 800;
  line-height: 1.2;
  text-align: center;
  color: var(--main-primary);"""),
    "mn-pager": style(".main-pager", """inline-size: 100%;

  & .wp-block-query-pagination {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: var(--space-xs);
  }

  & .wp-block-query-pagination-numbers {
    display: flex;
    gap: var(--space-xs);
  }

  & .page-numbers,
  & .wp-block-query-pagination-previous,
  & .wp-block-query-pagination-next {
    display: inline-grid;
    place-items: center;
    min-inline-size: 4.4rem;
    block-size: 4.4rem;
    padding-inline: var(--space-s);
    border-radius: var(--radius-circle, 999px);
    background-color: var(--main-light);
    box-shadow: 0 0.2rem 0.6rem var(--main-shadow);
    color: var(--main-primary);
    font-weight: 600;
    text-decoration: none;
    transition: background-color 0.2s ease, color 0.2s ease;
  }

  & a.page-numbers:hover,
  & .wp-block-query-pagination-previous:hover,
  & .wp-block-query-pagination-next:hover {
    background-color: var(--main-accent-soft);
  }

  & .page-numbers.current {
    background-color: var(--main-primary);
    color: var(--main-on-primary);
  }

  & .page-numbers.dots {
    background: none;
    box-shadow: none;
  }"""),
}
blog = el("Blog", "section", {**SEC, "class": "main-blog"}, ["etch-section-style", "mn-blog"], [
    el("Container", "div", {**CON, "class": "main-blog__container"}, ["etch-container-style", "mn-blog-container"], [
        el("Title", "h1", {"class": "main-blog__title"}, ["mn-blog-title"], [text("Blog")]),
        el("Grid", "ul", {"class": "main-card-grid"}, ["mn-card-grid"], [
            loop("Posts", "item", [card("item", "h2")], loop_id="mainQuery")]),
        el("Pager", "nav", {"class": "main-pager", "aria-label": "Pagination"}, ["mn-pager"], [query_block]),
    ])])
outputs["main-blog"] = kit_payload(blog, blog_styles)

# ================================================================ 4. Single post (plain main)
RELATED = {"mainRelatedPosts": {"name": "Main Related Posts", "key": "mainRelatedPosts", "global": True,
           "config": {"type": "wp-query", "args": {"post_type": "post", "post_status": "publish",
                      "posts_per_page": 3, "orderby": "date", "order": "DESC", "post__not_in": ["$post_id"],
                      "meta_query": [], "tax_query": [], "lang": "$lang ?? ''"}}}}
single_src = src["singleCopies"][0]["gutenbergBlock"]
post_core = find(single_src, lambda b: b["blockName"] == "core/post-content")[0]
post_styles = {**BASE, **CARD_STYLES, **HEADING_STYLES, **SOCIAL_STYLES,
    "mn-post-head": style(".main-post__head", """--cover-overlap: min(27rem, 18vw);
  position: relative;
  z-index: 1;
  padding-block: var(--section-space-l) 0;
  background: linear-gradient(180deg, var(--main-light) calc(100% - var(--cover-overlap)), transparent 0);"""),
    "mn-post-inner": style(".main-post__inner", """display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--content-gap);
  inline-size: 100%;
  text-align: center;"""),
    "mn-post-title": style(".main-post__title", """max-inline-size: 96rem;
  font-size: var(--h1);
  font-weight: 800;
  line-height: 1.25;
  color: var(--main-primary);"""),
    "mn-post-meta": style(".main-post__meta", """display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: var(--space-xs);"""),
    "mn-post-date": style(".main-post__date", "font-size: var(--text-s);\n  font-weight: 600;\n"
                                              "  color: var(--main-text-muted);"),
    "mn-post-cover": style(".main-post__cover", "inline-size: 100%;\n  max-inline-size: 96rem;\n"
                                                "  margin: var(--space-m) 0 0;"),
    "mn-post-img": style(".main-post__img", "display: block;\n  inline-size: 100%;\n  block-size: auto;\n"
                                            "  border-radius: var(--radius-m);"),
    "mn-post-body": style(".main-post__body", """--cover-overlap: min(27rem, 18vw);
  margin-block-start: calc(var(--cover-overlap) * -1);
  padding-block: var(--cover-overlap) var(--section-space-l);
  background-color: var(--main-light-alt);"""),
    "mn-post-prose": style(".main-post__prose", """display: flex;
  flex-direction: column;
  gap: var(--space-s);
  inline-size: 100%;
  max-inline-size: 96rem;
  margin-inline: auto;
  padding: var(--space-xl) var(--space-xl) var(--space-l);
  background-color: var(--main-light);
  color: var(--main-text);
  font-size: var(--text-m);
  line-height: 1.85;

  & h2 {
    margin-block-start: var(--space-s);
    font-size: var(--h3);
    font-weight: 800;
    line-height: 1.35;
    color: var(--main-primary);
  }

  & ul,
  & ol {
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
    padding-inline-start: var(--space-m);
  }

  & li::marker {
    color: var(--main-accent);
  }

  & img {
    border-radius: var(--radius-m);
  }

  @media (width <= 768px) {
    padding: var(--space-l) var(--space-m) var(--space-m);
  }"""),
    "mn-post-share": style(".main-post__share", """display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-xs);
  margin-block-start: var(--space-s);
  padding-block-start: var(--space-m);
  border-block-start: 1px solid var(--main-line);"""),
    "mn-post-share-label": style(".main-post__share-label", """margin-inline-end: var(--space-xs);
  font-size: var(--text-s);
  font-weight: 600;
  color: var(--main-primary);"""),
    "mn-post-related": style(".main-post__related", "background-color: var(--main-light-alt);"),
    "mn-post-related-container": style(".main-post__related-container", "gap: var(--space-l);"),
}
share = {
    "Facebook": ("facebook", "https://www.facebook.com/sharer/sharer.php?u={this.permalink.full}"),
    "X": ("x", "https://twitter.com/intent/tweet?url={this.permalink.full}&text={this.title}"),
    "LINE": ("line", "https://social-plugins.line.me/lineit/share?url={this.permalink.full}"),
}
single = el("Main", "main", {"id": "main"}, None, [
    el("Post Head", "section", {**SEC, "class": "main-post__head"}, ["etch-section-style", "mn-post-head"], [
        el("Container", "div", CON, ["etch-container-style"], [
            el("Inner", "div", {"class": "main-post__inner"}, ["mn-post-inner"], [
                el("Title", "h1", {"class": "main-post__title"}, ["mn-post-title"], [text("{this.title}")]),
                el("Meta", "div", {"class": "main-post__meta"}, ["mn-post-meta"], [
                    loop("Categories", "cat", [el("Pill", "span", {"class": "main-pill"}, ["mn-pill"],
                                                  [text("{cat.name}")])], target="this.categories"),
                    el("Date", "time", {"class": "main-post__date", "datetime": "{this.date}"}, ["mn-post-date"],
                       [text('{this.date.dateFormat("j F Y")}')]),
                ]),
                cond("If image", "this.image.id", el("Cover", "figure", {"class": "main-post__cover"},
                     ["mn-post-cover"], [img(
                         "Image", {"class": "main-post__img", "mediaId": "{this.image.id}", "loading": "eager"},
                         ["mn-post-img"])])),
            ])])]),
    el("Post Body", "section", {**SEC, "class": "main-post__body"}, ["etch-section-style", "mn-post-body"], [
        el("Container", "div", CON, ["etch-container-style"], [
            el("Prose", "div", {"class": "main-post__prose"}, ["mn-post-prose"], [
                post_core,
                el("Share", "div", {"class": "main-post__share", "aria-label": "Share this post"},
                   ["mn-post-share"], [
                    el("Label", "span", {"class": "main-post__share-label"}, ["mn-post-share-label"],
                       [text("Share")]),
                    *[social_link(n, u, ic, f"Share on {n}") for n, (ic, u) in share.items()],
                ]),
            ])])]),
    el("Related Posts", "section", {**SEC, "class": "main-post__related"}, ["etch-section-style", "mn-post-related"], [
        el("Container", "div", {**CON, "class": "main-post__related-container"},
           ["etch-container-style", "mn-post-related-container"], [
            heading(None, "Related posts", center=True),
            el("Grid", "ul", {"class": "main-card-grid"}, ["mn-card-grid"], [
                loop("Related", "rp", [card("rp", "h3")], loop_id="mainRelatedPosts",
                     params={"$post_id": "this.id"})]),
        ])]),
])
outputs["main-single-post"] = kit_payload(single, post_styles, loops=RELATED)

# ================================================================ 5. Contact page (component)
CONTACT_ID = 990102
contact_styles = {**BASE, **HEADING_STYLES, **SOCIAL_STYLES,
    "mn-contact": style(".main-contact", "background-color: var(--main-light);"),
    "mn-contact-grid": style(".main-contact__grid", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 40rem), 1fr));
  gap: var(--container-gap);
  align-items: center;
  inline-size: 100%;"""),
    "mn-contact-info": style(".main-contact__info", "display: flex;\n  flex-direction: column;\n"
                                                    "  gap: var(--space-m);"),
    "mn-contact-list": style(".main-contact__list", """display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 24rem), 1fr));
  gap: var(--space-s) var(--space-m);
  margin: 0;
  padding: 0;
  list-style: none;
  color: var(--main-text-muted);
  white-space: pre-line;

  > :first-child {
    grid-column: 1 / -1;
  }"""),
    "mn-contact-item": style(".main-contact__item", "display: flex;\n  align-items: flex-start;\n"
                                                    "  gap: var(--space-s);"),
    "mn-contact-icon": style(".main-contact__icon", """flex: none;
  inline-size: 4.4rem;
  block-size: 4.4rem;
  padding: var(--space-xs);
  border-radius: 50%;
  background-color: var(--main-accent-soft);
  color: var(--main-primary);"""),
    "mn-contact-label": style(".main-contact__label", "display: block;\n  font-weight: 600;\n"
                                                      "  color: var(--main-primary);"),
    "mn-contact-link": style(".main-contact__link", """color: inherit;
  text-decoration-color: var(--main-accent);
  text-underline-offset: 0.4rem;

  &:hover {
    color: var(--main-primary);
  }"""),
    "mn-contact-social": style(".main-contact__social", "display: flex;\n  flex-direction: column;\n"
                                                        "  gap: var(--space-xs);"),
    "mn-contact-social-title": style(".main-contact__social-title", "font-size: var(--h4);"),
    "mn-contact-map": style(".main-contact__map", MAP_CSS),
}


def contact_item(name, prop_key, label_key, icon_name, value):
    return cond(f"If {name}", f"props.{prop_key}", el(name, "li", {"class": "main-contact__item"},
        ["mn-contact-item"], [svg(f"{name} icon", icon(icon_name), "main-contact__icon", ["mn-contact-icon"]),
                              el("Body", "div", {}, None, label_value("main-contact__label", ["mn-contact-label"],
                                                                      f"{{props.{label_key}}}", value))]))


def contact_link(href, label, blank=False):
    a = {"class": "main-contact__link", "href": href}
    if blank:
        a.update({"target": "_blank", "rel": "noopener"})
    return [el("Link", "a", a, ["mn-contact-link"], [text(label)])]


contact_blocks = [el("Contact", "section", {**SEC, "class": "main-contact"}, ["etch-section-style", "mn-contact"], [
    el("Container", "div", CON, ["etch-container-style"], [
        el("Grid", "div", {"class": "main-contact__grid"}, ["mn-contact-grid"], [
            el("Info", "div", {"class": "main-contact__info"}, ["mn-contact-info"], [
                heading("{props.eyebrow}", "{props.title}", "{props.intro}", tag="h1"),
                el("List", "ul", {"class": "main-contact__list"}, ["mn-contact-list"], [
                    contact_item("Address", "address", "addressLabel", "address",
                                 contact_link("{props.mapUrl}", "{props.address}", True)),
                    contact_item("Hours", "hours", "hoursLabel", "hours",
                                 [el("Value", "span", {}, None, [text("{props.hours}")])]),
                    contact_item("Phone", "phone", "phoneLabel", "phone",
                                 contact_link("tel:{props.phone}", "{props.phone}")),
                    contact_item("LINE", "lineUrl", "lineLabel", "line-box",
                                 contact_link("{props.lineUrl}", "{props.lineId}", True)),
                    contact_item("Email", "email", "emailLabel", "email",
                                 contact_link("mailto:{props.email}", "{props.email}")),
                ]),
                el("Social", "div", {"class": "main-contact__social"}, ["mn-contact-social"], [
                    el("Title", "h2", {"class": "main-contact__social-title"}, ["mn-contact-social-title"],
                       [text("{props.socialTitle}")]),
                    social_list(),
                ]),
            ]),
            cond("If map embed", "props.mapEmbedUrl", el("Map", "iframe", {
                "class": "main-contact__map", "src": "{props.mapEmbedUrl}", "title": "{props.title}",
                "loading": "lazy", "referrerpolicy": "no-referrer-when-downgrade"}, ["mn-contact-map"])),
        ])])])]
contact_component = {"id": CONTACT_ID, "legacyId": "", "name": "Main Contact", "key": "MainContact",
                     "description": "Contact page: heading (H1), contact list with icons, social and map.",
                     "blocks": contact_blocks, "properties": [
                         prop("Eyebrow", "eyebrow", "Contact us"),
                         prop("Title", "title", "Company Name"),
                         prop("Intro", "intro", "How to reach us — booking, opening hours, parking …"),
                         *CONTACT_PROPS,
                         prop("LINE ID", "lineId", "@example", "Shown next to the LINE icon"),
                         prop("Social Title", "socialTitle", "Social Media"),
                         prop("Address Label", "addressLabel", "Address"),
                         prop("Hours Label", "hoursLabel", "Hours"),
                         prop("Phone Label", "phoneLabel", "Phone"),
                         prop("LINE Label", "lineLabel", "LINE"),
                         prop("Email Label", "emailLabel", "Email"),
                         *SOCIAL_PROPS]}
contact_instance = block("etch/component", {"ref": CONTACT_ID, "attributes": {}})
outputs["main-contact"] = kit_payload(contact_instance, contact_styles, {str(CONTACT_ID): contact_component})

for name, p in outputs.items():
    write(f"{OUT}/{name}.etch.txt", p)
    print("ok", name, len(p["styles"]), "styles", len(json.dumps(p)) // 1024, "KB")
