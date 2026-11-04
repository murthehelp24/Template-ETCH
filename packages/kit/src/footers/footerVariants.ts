/** Build the footer variants from the Main Footer (main-footer.etch.txt). Port of _build/build_footer_variants.py.
 *
 * Each variant is its own component (MainFooterLight, MainFooterCenter …) whose root carries one modifier class
 * (main-footer--<name>) holding that look; the shared main-footer__* styles stay identical, so the audit passes and
 * several footers can live on one site. Layouts that need it also change blocks (drop a column, add a map). */
import { type Block, type Payload, cond, el, nowIso, prop, style } from "../etch/lib";

const LIGHT_CSS = `/* light footer: dark text on the light colour */
  &.main-footer {
    --main-social-color: var(--main-primary);
    background-color: var(--main-light-alt);
    color: var(--main-text);
  }

  .main-footer__title {
    color: var(--main-primary);
  }

  .main-footer__text {
    color: var(--main-text-muted);
  }

  .main-footer__bottom {
    border-block-start-color: var(--main-line);
    color: var(--main-text-muted);
  }`;

const CENTER_CSS = `/* one centred column: logo, menu in a row, contact, social */
  .main-footer__grid {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-m);
    text-align: center;
  }

  .main-footer__col {
    align-items: center;
  }

  .main-footer__brand {
    max-inline-size: 56rem;
  }

  .main-footer__list {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: var(--space-xs) var(--space-l);
  }

  .main-social {
    justify-content: center;
  }`;

const MAP_CSS = `/* the services column becomes a Google map */
  .main-footer__grid {
    grid-template-columns: 1.6fr 1fr 1.2fr 1.6fr;

    @media (width <= 992px) {
      grid-template-columns: repeat(2, 1fr);
    }

    @media (width <= 768px) {
      grid-template-columns: 1fr;
    }
  }

  .main-footer__map {
    display: block;
    inline-size: 100%;
    block-size: 100%;
    min-block-size: 24rem;
    border: 0;
    border-radius: var(--radius-m);
  }`;

const COMPACT_CSS = `/* one row: logo, menu, social — roomy, with a larger logo and links */
  &.main-footer {
    --main-footer-logo-width: 18rem;
    padding-block-start: var(--section-space-m);
  }

  .main-footer__link {
    font-size: var(--text-m);
  }

  .main-footer__grid {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-l);
    padding-block-end: var(--space-l);

    @media (width <= 768px) {
      flex-direction: column;
      text-align: center;
    }
  }

  .main-footer__brand {
    max-inline-size: none;
  }

  .main-footer__list {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: var(--space-xs) var(--space-l);
  }

  .main-footer__bottom {
    margin-block-start: var(--space-m);
    padding-block: var(--space-s);
  }`;

// name, component id (fixed, so a rebuilt file keeps it), key, label, css
const VARIANTS: [string, number, string, string, string][] = [
  ["light", 990002, "MainFooterLight", "Main Footer (Light)", LIGHT_CSS],
  ["center", 990003, "MainFooterCenter", "Main Footer (Centred)", CENTER_CSS],
  ["map", 990005, "MainFooterMap", "Main Footer (Map)", MAP_CSS],
  ["compact", 990006, "MainFooterCompact", "Main Footer (Compact)", COMPACT_CSS],
];

const nameOf = (b: Block): string | undefined => b.attrs?.metadata?.name;

function find(blocks: Block[], name: string): Block | null {
  for (const b of blocks) {
    if (nameOf(b) === name) return b;
    const hit = find(b.innerBlocks || [], name);
    if (hit) return hit;
  }
  return null;
}

function mustFind(blocks: Block[], name: string): Block {
  const b = find(blocks, name);
  if (!b) throw new Error(`footer block ${name} not found`);
  return b;
}

function setChildren(b: Block, children: Block[]): void {
  b.innerBlocks = children;
  b.innerHTML = "\n" + "\n\n".repeat(Math.max(children.length - 1, 0)) + "\n";
  b.innerContent = children.length
    ? ["\n", ...children.flatMap(() => [null, "\n\n"]).slice(0, -1), "\n"]
    : ["\n", "\n"];
}

function drop(parent: Block, ...names: string[]): void {
  setChildren(parent, parent.innerBlocks.filter((b) => !names.includes(nameOf(b) ?? "")));
}

function variant(base: Payload, name: string, newId: number, key: string, label: string, css: string,
                 now: () => string): Payload {
  const p = structuredClone(base);
  const comps = p.components!;
  const baseId = Object.keys(comps)[0]!;
  const comp = comps[baseId];
  Object.assign(comp, { id: newId, key, name: label,
    description: comp.description + " Variant: " + label.split("(")[1]!.replace(/\)+$/, "") + "." });
  const blocks: Block[] = comp.blocks;
  const root = blocks[0]!;
  root.attrs.attributes.class = "main-footer main-footer--" + name;
  root.attrs.styles = [...root.attrs.styles, "mf-v-" + name];
  p.styles["mf-v-" + name] = style(".main-footer--" + name, css);
  const grid = mustFind(blocks, "Grid");

  if (name === "center") {
    drop(grid, "Services");
    drop(mustFind(blocks, "Menu"), "Title");
    drop(mustFind(blocks, "Contact"), "Title");
  }
  if (name === "map") {
    const services = mustFind(blocks, "Services");
    grid.innerBlocks.splice(grid.innerBlocks.indexOf(services), 1);
    grid.innerBlocks.push(el("Map Column", "div", { class: "main-footer__col" }, ["mf-col"], [
      cond("If map embed", "props.mapEmbedUrl", el("Map", "iframe", {
        class: "main-footer__map", src: "{props.mapEmbedUrl}", title: "Map", loading: "lazy",
        referrerpolicy: "no-referrer-when-downgrade" }))]));
    setChildren(grid, grid.innerBlocks);
    const at = comp.properties.findIndex((pr: any) => pr.key === "mapLabel") + 1;
    comp.properties.splice(at, 0, prop("Map Embed URL", "mapEmbedUrl",
      "https://www.google.com/maps?q=Bangkok&output=embed",
      "Google Maps → Share → Embed a map → copy the src. Empty = no map"));
  }
  if (name === "compact") {
    drop(grid, "Services");
    drop(mustFind(blocks, "Brand"), "Description");
    drop(mustFind(blocks, "Menu"), "Title");
    const contact = mustFind(blocks, "Contact");
    drop(contact, ...contact.innerBlocks.map((b) => nameOf(b)!).filter((n) => n !== "Social"));
  }

  p.components = { [String(newId)]: comp };
  p.gutenbergBlock.attrs.ref = newId;
  p.timestamp = now();
  return p;
}

/** The four variants, from the Main Footer payload (read as written: a JSON copy of it). */
export function build(base: Payload, now: () => string = nowIso): Record<string, Payload> {
  const written = JSON.parse(JSON.stringify(base)) as Payload;
  return Object.fromEntries(VARIANTS.map(([name, id, key, label, css]) =>
    [`main-footer-${name}`, variant(written, name, id, key, label, css, now)]));
}
