/** Build a paste-ready Etch header (main-header) on Oh My Etch navigation components.
 * Port of _build/build_header_ome.py. Its CSS is in omeCss.ts and is kept as written (no portable()). */
import { loadData } from "../data";
import { type Attrs, type Block, type Payload, type Styles, block, nowIso, rawStyle, text } from "../etch/lib";
import { b64decode, b64encode, pyDumps, pyReplace } from "../etch/pycompat";
import { COLORS } from "../kit";
import * as C from "./omeCss";

const [NAV, LIST, ITEM, TRIGGER, CONTENT, MOBILE] = [1843, 1844, 1845, 1846, 1847, 1849];

/** This builder's own el(): the lib one plus an optional script. */
function el(name: string, tag: string, attrs?: Attrs | null, styleIds?: string[] | null, children?: Block[] | null,
            script?: Attrs | null): Block {
  const a: Attrs = { metadata: { name }, tag, attributes: attrs || {} };
  if (styleIds && styleIds.length) a.styles = styleIds;
  if (script) a.script = script;
  return block("etch/element", a, children);
}

function slot(name: string, children: Block[]): Block {
  return block("etch/slot-content", { name }, children);
}

/** attributes: {group: {key: value}} — Etch stores each group prop as a JSON string (Python json.dumps). */
function comp(ref: number, name: string, attributes: Record<string, any> = {}, slots: Block[] = []): Block {
  const norm = (group: Record<string, any>) =>
    Object.fromEntries(Object.entries(group).map(([k, v]) => [k, Array.isArray(v) ? v.join(" ") : v]));
  const attrs = Object.fromEntries(Object.entries(attributes).map(([k, v]) =>
    [k, v && typeof v === "object" && !Array.isArray(v) ? pyDumps(norm(v)) : v]));
  return { blockName: "etch/component", attrs: { ref, metadata: { name }, attributes: attrs },
    innerBlocks: slots, innerHTML: "\n\n", innerContent: slots.length ? ["\n", null, "\n"] : ["\n", "\n"] };
}

const navLink = (label: string, href: string) => comp(ITEM, label, {}, [slot("default", [
  el("Link", "a", { href, class: "main-header__link" }, ["mh-link"], [text(label)])])]);

function navDropdown(label: string, contentId: string, links: [string, string][]): Block {
  return comp(ITEM, label, {}, [slot("default", [
    comp(TRIGGER, "Trigger", {
      identity: { contentId },
      settings: { showArrow: true, triggerAction: "hover" },
      styling: { class: ["ome-nav-menu-default__trigger", "mh-link"] },
    }, [slot("default", [text(label)])]),
    comp(CONTENT, "Dropdown", {
      identity: { contentId },
      styling: { class: ["mh-dropdown"] },
    }, [slot("default", links.map(([l, h]) =>
      el("Link", "a", { href: h, class: "main-header__dropdown-link" }, ["mh-dropdown-link"], [text(l)])))]),
  ])]);
}

const buttons = (): Block[] => [
  el("CTA", "a", { href: "https://line.me/R/ti/p/@example", target: "_blank", rel: "noopener",
    class: "btn--secondary" }, null, [text("Chat on LINE")]),
];

const pick = (s: Attrs) => ({ type: s.type, selector: s.selector, collection: s.collection, css: s.css });

/** site-header-ohmyetch.etch.txt */
export function build(now: () => string = nowIso): Payload {
  const orig = loadData("original-copy.json"); // old header copy (script, etch base styles)
  const omeCopy = loadData("ome-copy.json"); // Oh My Etch components + their styles
  const omeAll: Record<string, Attrs> = {};
  for (const s of loadData("ome.json").styles) omeAll[s.id] = s;

  const ostyles = orig.styles;
  const styles: Styles = {
    "etch-section-style": ostyles["etch-section-style"],
    "etch-container-style": ostyles["etch-container-style"],
    ...COLORS,
    "mh-theme": rawStyle(":root:has(.main-header)", C.THEME_CSS, "custom"),
    "mh-root": rawStyle(".main-header", C.ROOT_CSS),
    "mh-bar": rawStyle(".main-header__bar", C.BAR_CSS),
    "mh-container": rawStyle(".main-header__container", C.CONTAINER_CSS),
    "mh-logo": rawStyle(".main-header__logo", C.LOGO_CSS),
    "mh-logo-img": rawStyle(".main-header__logo-img", C.LOGO_IMG_CSS),
    "mh-nav-list": rawStyle(".main-header__nav-list", C.NAV_LIST_CSS),
    "mh-link": rawStyle(".main-header__link", C.LINK_CSS),
    "mh-dropdown": rawStyle(".main-header__dropdown", C.DROPDOWN_CSS),
    "mh-dropdown-link": rawStyle(".main-header__dropdown-link", C.DROPDOWN_LINK_CSS),
    "mh-actions": rawStyle(".main-header__actions", C.ACTIONS_CSS),
    "mh-burger": rawStyle(".main-header__burger", C.BURGER_CSS),
    "mh-drawer": rawStyle(".main-header__drawer", C.DRAWER_CSS),
    "mh-drawer-content": rawStyle(".main-header__drawer-content", C.DRAWER_CONTENT_CSS),
    "mh-drawer-head": rawStyle(".main-header__drawer-head", C.DRAWER_HEAD_CSS),
    "mh-drawer-button": rawStyle(".main-header__drawer-button", C.DRAWER_BUTTON_CSS),
    "mh-mlist": rawStyle(".main-header__mobile-list", C.MLIST_CSS),
    "mh-mitem": rawStyle(".main-header__mobile-item", C.MITEM_CSS),
    "mh-mlink": rawStyle(".main-header__mobile-link", C.MLINK_CSS),
    "mh-next-icon": rawStyle(".main-header__next-icon", C.NEXT_ICON_CSS),
    "mh-mslot": rawStyle(".main-header__mobile-slot", C.MSLOT_CSS),
  };
  // Oh My Etch records (reused if the target already has them; base customs carry the behaviour CSS)
  for (const [sid, s] of Object.entries<Attrs>(omeCopy.styles)) {
    if (s.selector.startsWith(".probe")) continue;
    styles[sid] = pick(s);
  }
  for (const sid of ["ome-drawer__host", "ome-drawer__page"]) styles[sid] = pick(omeAll[sid]!); // runtime host, not linked to any block

  let js = b64decode(orig.gutenbergBlock.attrs.script.code);
  js = pyReplace(pyReplace(js, "'.header-wrapper'", "'.main-header'"), "(.header-wrapper)", "(.main-header)");
  js = pyReplace(js, "if (config.skipLink) {", "if (config.skipLink && !header.querySelector('.skip-link')) {");
  if (js.includes(".header-wrapper") || !js.includes("querySelector('.skip-link')")) {
    throw new Error("header script: the expected replacements did not apply");
  }
  const script = { code: b64encode(js), id: "mainheader" };

  const nav = comp(NAV, "Nav", {
    identity: { menuId: C.MENU_ID },
    accessibility: { navAriaLabel: "Main" },
  }, [slot("default", [
    comp(LIST, "Nav List", { styling: { class: ["mh-nav-list"] } }, [slot("default", [
      navLink("Home", "/"),
      navLink("About", "/about/"),
      navDropdown("Services", "main-menu-services", [
        ["Service 1", "/services/service-1/"],
        ["Service 2", "/services/service-2/"],
        ["Service 3", "/services/service-3/"],
      ]),
      navLink("Blog", "/blog/"),
      navLink("Contact", "/contact/"),
    ])]),
  ])]);

  const mobile = comp(MOBILE, "Mobile Menu", {
    identity: { menuId: C.MENU_ID },
    settings: { drawerDirection: "right", dismissible: true },
    content: { showTriggerLabel: false, triggerAriaLabel: "Open menu", backButtonLabel: "Back" },
    rootStyling: { class: [] },
    controlStyling: { triggerClass: ["mh-burger"], backButtonClass: ["mh-drawer-button"],
      closeButtonClass: ["mh-drawer-button"] },
    drawerStyling: { drawerClass: ["mh-drawer"], headerClass: ["mh-drawer-head"],
      contentClass: ["mh-drawer-content"] },
    menuStyling: { listClass: ["mh-mlist"], itemClass: ["mh-mitem"], linkClass: ["mh-mlink"],
      submenuTriggerClass: ["mh-mlink"], nextIconClass: ["mh-next-icon"] },
    slotStyling: { beforeClass: [], afterClass: ["mh-mslot"] },
  }, [slot("after", buttons())]);

  const header = el("Main Header", "header", {
    "data-etch-element": "section",
    "data-overlay-header": "false",
    "data-overlay-header-offset": "false",
    "data-sticky-header": "true",
    "data-hide-on-scroll": "true",
    "data-hide-at": "200px",
    "data-show-on-scroll-up": "true",
    "data-skip-link": "true",
    class: "main-header",
  }, ["etch-section-style", "mh-root"], [
    el("Bar", "div", { class: "main-header__bar" }, ["mh-bar"], [
      el("Container", "div", { "data-etch-element": "container", class: "main-header__container" },
        ["etch-container-style", "mh-container"], [
          el("Logo", "a", { href: "/", "aria-label": "Home", class: "main-header__logo" }, ["mh-logo"], [
            { blockName: "etch/dynamic-image",
              attrs: { metadata: { name: "Logo Image" }, tag: "img",
                attributes: { class: "main-header__logo-img", mediaId: "" },
                styles: ["mh-logo-img"] },
              innerBlocks: [], innerHTML: "\n\n", innerContent: ["\n", "\n"] },
          ]),
          nav,
          el("Actions", "div", { class: "main-header__actions" }, ["mh-actions"], buttons()),
          mobile,
        ]),
    ]),
  ], script);

  const payload: Payload = { type: "block", gutenbergBlock: header, timestamp: now(), styles,
    components: omeCopy.comps, version: 2.1 };

  const used = new Set<string>();
  const walk = (b: Block) => {
    for (const s of b.attrs?.styles || []) used.add(s);
    for (const c of b.innerBlocks || []) walk(c);
  };
  walk(header);
  for (const c of Object.values<any>(omeCopy.comps)) for (const b of c.blocks) walk(b);
  const missing = [...used].filter((s) => !(s in styles));
  if (missing.length) throw new Error(`header uses missing styles: ${missing.join(", ")}`);
  return payload;
}
