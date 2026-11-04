/** Build the header variants from the Oh My Etch header (site-header-ohmyetch.etch.txt).
 * Port of _build/build_header_variants.py. Each variant is the same header plus one modifier class
 * (main-header--<name>) whose style overrides the look, and, where the layout needs it, a few changed blocks.
 * The shared main-header__* styles stay identical, so several variants can be pasted into one site (Etch keeps the
 * first copy of a selector) and the audit stays happy. */
import { type Block, type Payload, el, nowIso, style, svg, text } from "../etch/lib";
import { icon } from "../kit";
import { CENTER_CSS, FLOATING_CSS, LIGHT_CSS, RIGHT_CSS, TOPBAR_CSS } from "./omeVariantsCss";

// name, label (block name), css
const VARIANTS: [string, string, string][] = [
  ["light", "Main Header (Light)", LIGHT_CSS],
  ["center", "Main Header (Centred Logo)", CENTER_CSS],
  ["topbar", "Main Header (Top Bar)", TOPBAR_CSS],
  ["floating", "Main Header (Floating)", FLOATING_CSS],
  ["right", "Main Header (Menu Right)", RIGHT_CSS],
];

function find(b: Block, name: string): Block | null {
  if (b.attrs?.metadata?.name === name) return b;
  for (const c of b.innerBlocks || []) {
    const hit = find(c, name);
    if (hit) return hit;
  }
  return null;
}

function mustFind(b: Block, name: string): Block {
  const hit = find(b, name);
  if (!hit) throw new Error(`header block ${name} not found`);
  return hit;
}

function setChildren(b: Block, children: Block[]): void {
  b.innerBlocks = children;
  b.innerHTML = "\n" + "\n\n".repeat(Math.max(children.length - 1, 0)) + "\n";
  b.innerContent = children.length
    ? ["\n", ...children.flatMap(() => [null, "\n\n"]).slice(0, -1), "\n"]
    : ["\n", "\n"];
}

function topbarItem(name: string, iconName: string, label: string, href: string | null = null, extra = ""): Block {
  const cls = "main-header__topbar-item" + (extra ? " main-header__topbar-item--" + extra : "");
  const attrs = { class: cls, ...(href ? { href } : {}) };
  return el(name, href ? "a" : "span", attrs, null,
    [svg("Icon", icon(iconName)), el("Label", "span", {}, null, [text(label)])]);
}

function topbar(): Block {
  return el("Top Bar", "div", { class: "main-header__topbar" }, null, [
    el("Top Bar Inner", "div", { class: "main-header__topbar-inner" }, null, [
      el("Info", "div", { class: "main-header__topbar-group" }, null, [
        topbarItem("Address", "address", "123 Example Road, Bangkok", null, "address"),
        topbarItem("Hours", "hours", "Mon–Sat 09:00–18:00"),
        topbarItem("Phone", "phone", "02-000-0000", "tel:+6620000000"),
      ]),
      el("Links", "div", { class: "main-header__topbar-group main-header__topbar-group--extra" }, null, [
        topbarItem("Email", "email", "hello@example.com", "mailto:hello@example.com"),
        topbarItem("LINE", "line", "@example", "https://line.me/R/ti/p/@example"),
      ]),
    ]),
  ]);
}

function variant(base: Payload, name: string, label: string, css: string, now: () => string): Payload {
  const p = structuredClone(base);
  const header = p.gutenbergBlock;
  const a = header.attrs;
  a.metadata.name = label;
  a.attributes.class = "main-header main-header--" + name;
  a.styles = [...a.styles, "mh-v-" + name];
  p.styles["mh-v-" + name] = style(".main-header--" + name, css);

  if (name === "light") { // on a light bar the primary button stands out (secondary is meant for the dark bar)
    mustFind(header, "Actions").innerBlocks[0]!.attrs.attributes.class = "btn--primary";
  }
  if (name === "topbar") {
    const bar = mustFind(header, "Bar");
    setChildren(bar, [topbar(), ...bar.innerBlocks]);
  }

  p.timestamp = now();
  return p;
}

/** The five variants, from the Oh My Etch header payload (read as written: a JSON copy of it). */
export function build(base: Payload, now: () => string = nowIso): Record<string, Payload> {
  const written = JSON.parse(JSON.stringify(base)) as Payload;
  return Object.fromEntries(VARIANTS.map(([name, label, css]) =>
    [`site-header-ohmyetch-${name}`, variant(written, name, label, css, now)]));
}
