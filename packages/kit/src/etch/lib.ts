/** Small helpers to write Etch copy payloads (gutenberg block JSON). Port of _build/lib_etch.py. */
import { writeFileSync } from "node:fs";
import { b64encode, formatG } from "./pycompat";

export type Attrs = Record<string, any>;
export interface Block {
  blockName: string;
  attrs: Attrs;
  innerBlocks: Block[];
  innerHTML: string;
  innerContent: (string | null)[];
}
export interface StyleRecord {
  type: string;
  selector: string;
  collection: string;
  css: string;
}
export type Styles = Record<string, StyleRecord>;
export interface Payload {
  type: "block";
  gutenbergBlock: Block;
  timestamp: string;
  styles: Styles;
  loops?: Record<string, any>;
  components?: Record<string, any>;
  version: number;
  [key: string]: unknown;
}

/** Python truthiness of an optional dict / list argument. */
const filled = (v: unknown): boolean =>
  v != null && (Array.isArray(v) ? v.length > 0 : typeof v === "object" ? Object.keys(v).length > 0 : Boolean(v));

function inner(children: Block[]): [string, (string | null)[]] {
  if (!children.length) return ["\n\n", ["\n", "\n"]];
  return ["\n" + "\n\n".repeat(children.length - 1) + "\n",
    ["\n", ...children.flatMap(() => [null, "\n\n"]).slice(0, -1), "\n"]];
}

export function block(name: string, attrs: Attrs, children?: Block[] | null): Block {
  const kids = children || [];
  const [html, content] = inner(kids);
  return { blockName: name, attrs, innerBlocks: kids, innerHTML: html, innerContent: content };
}

export function el(name: string, tag: string, attrs?: Attrs | null, styles?: string[] | null,
                   children?: Block[] | null): Block {
  const a: Attrs = { metadata: { name }, tag, attributes: attrs || {} };
  if (filled(styles)) a.styles = styles;
  return block("etch/element", a, children);
}

export function text(content: string): Block {
  const b = block("etch/text", { metadata: { name: "Text" }, content });
  b.innerHTML = "";
  b.innerContent = [];
  return b;
}

export function img(name: string, attrs: Attrs, styles: string[]): Block {
  return block("etch/dynamic-image", { metadata: { name }, tag: "img", attributes: attrs, styles });
}

export function svg(name: string, uri: string, cls?: string | null, styles?: string[] | null): Block {
  let attrs: Attrs = { "aria-hidden": "true", focusable: "false", src: uri };
  if (cls) attrs = { class: cls, ...attrs };
  const a: Attrs = { metadata: { name }, tag: "svg", attributes: attrs };
  if (filled(styles)) a.styles = styles;
  return block("etch/svg", a);
}

export function cond(name: string, expr: string, children: Block | Block[]): Block {
  return block("etch/condition", {
    metadata: { name },
    condition: { leftHand: expr, operator: "isTruthy", rightHand: null },
    conditionString: expr,
  }, Array.isArray(children) ? children : [children]);
}

export function loop(name: string, item: string, children: Block[], loopId?: string | null, target?: string | null,
                     params?: Attrs | null): Block {
  const a: Attrs = { metadata: { name }, itemId: item };
  if (loopId) a.loopId = loopId;
  if (target) a.target = target;
  if (filled(params)) a.loopParams = params;
  return block("etch/loop", a, children);
}

export function slotPlaceholder(name: string): Block {
  return block("etch/slot-placeholder", { name });
}

// Python's \w and \b count Unicode letters and digits, so "ไทย2rem" is left alone; the digits stay ASCII
const REM = /(?<![\p{L}\p{N}_.-])([0-9]*\.?[0-9]+)rem(?![\p{L}\p{N}_])/gu;

/** Lengths are written for 1rem = 10px. Etch's to-rem() converts px with each site's own root font size
 * (62.5% or 100%), so the templates keep the same size on every site. */
export function portable(css: string): string {
  return css.replace(REM, (_m, n: string) => `to-rem(${formatG(parseFloat(n) * 10)}px)`);
}

export function style(sel: string, css: string, typ = "class"): StyleRecord {
  return { type: typ, selector: sel, collection: "default", css: portable(css) };
}

/** The header builders' own style(): the CSS is kept exactly as written (no portable()). */
export function rawStyle(sel: string, css: string, typ = "class"): StyleRecord {
  return { type: typ, selector: sel, collection: "default", css };
}

export function prop(name: string, key: string, dflt: unknown, desc = "", primitive = "string"): Attrs {
  const p: Attrs = { name, key, keyTouched: true, type: { primitive }, default: dflt };
  if (desc) p.description = desc;
  return p;
}

export function dataUri(svgMarkup: string): string {
  return "data:image/svg+xml;base64," + b64encode(svgMarkup);
}

export const nowIso = (): string => new Date().toISOString();

export function payload(gblock: Block, styles: Styles, components?: Record<string, any> | null,
                        loops?: Record<string, any> | null, now: () => string = nowIso): Payload {
  const used = new Set<string>();
  const walk = (b: Block) => {
    for (const s of b.attrs?.styles || []) used.add(s);
    for (const c of b.innerBlocks || []) walk(c);
  };
  walk(gblock);
  for (const c of Object.values(components || {})) for (const b of c.blocks) walk(b);
  const missing = [...used].filter((s) => !(s in styles));
  if (missing.length) throw new Error(`payload uses missing styles: ${missing.join(", ")}`);
  const p: Payload = { type: "block", gutenbergBlock: gblock, timestamp: now(), styles } as Payload;
  if (filled(loops)) p.loops = loops!;
  if (filled(components)) p.components = components!;
  p.version = 2.1;
  return p;
}

/** json.dumps(p, ensure_ascii=False, separators=(",", ":")) */
export function serialize(p: unknown): string {
  return JSON.stringify(p);
}

export function write(path: string, p: unknown): void {
  writeFileSync(path, serialize(p));
}
