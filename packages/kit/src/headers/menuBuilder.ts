/** Build a generic, paste-ready Etch header (site-header) from the Win Win copy payload (Menu Builder components).
 * Port of _build/build_header_menubuilder.py. Its CSS is in menuBuilderCss.ts and is kept as written
 * (no portable()). */
import { loadData } from "../data";
import { type Attrs, type Block, type Payload, type Styles, block, nowIso, rawStyle, text } from "../etch/lib";
import { b64decode, b64encode, pyReplace } from "../etch/pycompat";
import { COLORS } from "../kit";
import * as C from "./menuBuilderCss";

// Python's \w counts Unicode letters and digits
const NAV_CLASS = /\.nav(?![\p{L}\p{N}_-])/gu;

function ren(css: string): string {
  return pyReplace(css, ".nav__list", ".site-header__nav-list").replace(NAV_CLASS, ".site-header__nav");
}

/** This builder's own el(): the lib one plus an optional script. */
function el(name: string, tag: string, attrs?: Attrs | null, styleIds?: string[] | null, children?: Block[] | null,
            script?: Attrs | null): Block {
  const a: Attrs = { metadata: { name }, tag, attributes: attrs || {} };
  if (styleIds && styleIds.length) a.styles = styleIds;
  if (script) a.script = script;
  return block("etch/element", a, children);
}

function component(ref: number, attributes: Attrs, name: string | null = null, children: Block[] = []): Block {
  const a: Attrs = { ref, attributes };
  if (name) a.metadata = { name };
  return { blockName: "etch/component", attrs: a, innerBlocks: children, innerHTML: "\n\n",
    innerContent: children.length ? ["\n", null, "\n"] : ["\n", "\n"] };
}

function slot(name: string, children: Block[]): Block {
  return block("etch/slot-content", { name }, children);
}

const link = (label: string, url: string, name = "Menu Link") =>
  component(1974, { label, linkUrl: url }, name);

/** site-header.etch.txt */
export function build(now: () => string = nowIso): Payload {
  const orig = loadData("original-copy.json");
  const lib = loadData("lib-styles.json");
  const ostyles = orig.styles;
  const styles: Styles = {
    ...COLORS,
    // Etch element base styles (reused if the target site has them)
    "etch-section-style": ostyles["etch-section-style"],
    "etch-container-style": ostyles["etch-container-style"],
    "etch-flex-div-style": ostyles["etch-flex-div-style"],
    // header block
    "sh-root": rawStyle(".site-header", C.ROOT_CSS),
    "sh-bar": rawStyle(".site-header__bar", C.BAR_CSS),
    "sh-container": rawStyle(".site-header__container", C.CONTAINER_CSS),
    "sh-logo": rawStyle(".site-header__logo", C.LOGO_CSS),
    "sh-logo-img": rawStyle(".site-header__logo-img", C.LOGO_IMG_CSS),
    "sh-actions": rawStyle(".site-header__actions", C.ACTIONS_CSS),
    // menu markup classes (library)
    fy0647x: ostyles.fy0647x, // .mobile-menu-header
    "6liaugx": ostyles["6liaugx"], // .hide-from-desktop-menu
    "sh-nav": rawStyle(".site-header__nav", ""),
    "sh-nav-list": rawStyle(".site-header__nav-list", C.NAV_LIST_CSS),
    "7s74zii": ostyles["7s74zii"], // #menu-wrapper (used inside MenuWrapper)
  };
  // Menu library CSS (classes the menu/toggle scripts add at runtime). Etch's own copy
  // misses these, and unlinked class styles are not always compiled on the frontend
  // (the hamburger icon broke). Ship them as custom styles — always compiled — scoped
  // with :where(.site-header *) so they never clash with the target site's own records.
  for (const [sid, s] of Object.entries<Attrs>(lib)) {
    if (!s.css.trim() || s.type !== "class") continue;
    styles[`sh-lib-${sid}`] = rawStyle(`${s.selector}:where(.site-header *)`, ren(s.css), "custom");
  }
  for (const s of Object.values(styles)) delete (s as Attrs).readonly;

  const g = orig.gutenbergBlock;
  const bar0 = g.innerBlocks[0];
  const cont0 = bar0.innerBlocks[0];
  const menu0 = cont0.innerBlocks[1]; // MenuWrapper instance
  const burger0 = cont0.innerBlocks[3]; // ToggleButton instance
  const mobileHeader0 = menu0.innerBlocks[0].innerBlocks[0];

  // header script: same behaviour, new root selector
  let js = b64decode(g.attrs.script.code);
  js = pyReplace(pyReplace(js, "'.header-wrapper'", "'.site-header'"), "(.header-wrapper)", "(.site-header)");
  js = pyReplace(js, "if (config.skipLink) {", "if (config.skipLink && !header.querySelector('.skip-link')) {");
  if (js.includes(".header-wrapper") || !js.includes("querySelector('.skip-link')")) {
    throw new Error("header script: the expected replacements did not apply");
  }
  const script = { code: b64encode(js), id: "siteheader" };

  // mobile menu header (close button) — keep, generic label
  const closeToggle = JSON.parse(JSON.stringify(mobileHeader0.innerBlocks[0]));
  closeToggle.attrs.attributes.ariaLabel = "Close menu";
  const mobileHeader = el("Mobile Header", "div",
    { "data-etch-element": "flex-div", class: "mobile-menu-header hide-from-desktop-menu" },
    ["etch-flex-div-style", "fy0647x", "6liaugx"], [closeToggle]);

  const nav = el("Nav", "nav", { "data-menu-element": "nav", class: "site-header__nav", "aria-label": "Main" },
    ["sh-nav"], [
      el("Nav List", "ul", { "data-etch-element": "flex-div", class: "site-header__nav-list" },
        ["etch-flex-div-style", "sh-nav-list"], [
          link("Home", "/"),
          link("About", "/about/"),
          component(1971, { dropdownLabel: "Services" }, "Services Dropdown", [
            slot("dropdownContent", [
              link("Service 1", "/services/service-1/"),
              link("Service 2", "/services/service-2/"),
              link("Service 3", "/services/service-3/"),
            ]),
          ]),
          link("Blog", "/blog/"),
          link("Contact", "/contact/"),
        ]),
    ]);

  const menu = JSON.parse(JSON.stringify(menu0));
  menu.attrs.metadata = { name: "Menu" };
  menu.innerBlocks = [slot("menuContent", [mobileHeader, nav])];

  const burger = JSON.parse(JSON.stringify(burger0));
  burger.attrs.metadata = { name: "Menu Toggle" };
  burger.attrs.attributes.ariaLabel = "Open menu";
  delete burger.attrs.attributes.customIdForThisToggle;

  const header = el("Site Header", "header", {
    "data-etch-element": "section",
    "data-overlay-header": "false",
    "data-overlay-header-offset": "false",
    "data-sticky-header": "true",
    "data-hide-on-scroll": "true",
    "data-hide-at": "200px",
    "data-show-on-scroll-up": "true",
    "data-skip-link": "true",
    class: "site-header",
  }, ["etch-section-style", "sh-root"], [
    el("Bar", "div", { "data-menu-element": "header-inner", class: "site-header__bar" }, ["sh-bar"], [
      el("Container", "div", { "data-etch-element": "container", class: "site-header__container" },
        ["etch-container-style", "sh-container"], [
          el("Logo", "a", { href: "/", "aria-label": "Home", class: "site-header__logo" }, ["sh-logo"], [
            { blockName: "etch/dynamic-image",
              attrs: { metadata: { name: "Logo Image" }, tag: "img",
                attributes: { class: "site-header__logo-img", mediaId: "" },
                styles: ["sh-logo-img"] },
              innerBlocks: [], innerHTML: "\n\n", innerContent: ["\n", "\n"] },
          ]),
          menu,
          el("Actions", "div", { class: "site-header__actions" }, ["sh-actions"], [
            el("CTA", "a", { href: "https://line.me/R/ti/p/@example", target: "_blank", rel: "noopener",
              class: "btn--secondary" }, null, [text("Chat on LINE")]),
          ]),
          burger,
        ]),
    ]),
  ], script);

  const payload: Payload = { type: "block", gutenbergBlock: header, timestamp: now(), styles,
    components: orig.components, version: 2.1 };

  // sanity: every referenced style id exists
  const used = new Set<string>();
  const walk = (b: Block) => {
    for (const s of b.attrs?.styles || []) used.add(s);
    for (const c of b.innerBlocks || []) walk(c);
  };
  walk(header);
  for (const c of Object.values<any>(orig.components)) for (const b of c.blocks) walk(b);
  const missing = [...used].filter((s) => !(s in styles));
  if (missing.length) throw new Error(`header uses missing styles: ${missing.join(", ")}`);
  return payload;
}
