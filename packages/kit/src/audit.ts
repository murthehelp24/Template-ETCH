/**
 * Check that all templates can live on one site together. Port of _build/audit.py: the same four groups of rules
 * and the same messages.
 *
 * Fails on: the same selector with different CSS in two files, a component / loop key with different content,
 * a file without the shared colour variables, a hard-coded colour in a template-owned style, a style id used by a
 * block but missing from the file. Warns on customMediaDefinitions and on leftovers of the source sites.
 */
import { existsSync, readFileSync } from "node:fs";
import type { Block } from "./etch/lib";
import { pyDumps } from "./etch/pycompat";

export interface AuditOptions {
  /** client names that must not appear in a template (_build/private-terms.txt, git-ignored) */
  privateTerms?: string[];
  /** more texts scanned for leftovers only, like _build/src/*.json in audit.py: {path: text} */
  sources?: Record<string, string>;
}

export interface AuditResult {
  errors: string[];
  warnings: string[];
  /** what audit.py prints: one line per file, the warnings, the errors and the summary */
  lines: string[];
}

// Python's \w, \b and \d count Unicode letters and digits
const W = "\\p{L}\\p{N}_";
const COLOR_LIT = new RegExp(`#[0-9a-fA-F]{3,8}(?![${W}])|(?<![${W}])rgba?\\(|(?<![${W}])hsla?\\(`
  + `|(?<![-${W}])(?:white|black)(?![-${W}])`, "gu");
const ACSS_COLOR = new RegExp("var\\(--(primary|secondary|accent|base|neutral|white|black|text-dark|text-light|bg-"
  + `|shade)(?![${W}-]*-(?:xs|s|m|l|xl)(?![${W}]))[${W}-]*`, "gu");
const RAW_REM = new RegExp(`(?<![${W}.-])\\p{Nd}*\\.?\\p{Nd}+rem(?![${W}])`, "gu");
const CLASS_SELECTOR = new RegExp(`^\\.([${W}-]+)$`, "u");
const SAMPLE_PHONES = new Set(["02-000-0000", "+6620000000"]);

/** Python's repr() of a str and of a list / tuple of str. */
function pyStr(s: string): string {
  const q = s.includes("'") && !s.includes('"') ? '"' : "'";
  const body = s.replace(/\\/g, "\\\\").replace(/\n/g, "\\n").replace(/\r/g, "\\r").replace(/\t/g, "\\t")
    .split(q).join("\\" + q);
  return q + body + q;
}
const pyList = (items: string[]) => `[${items.map(pyStr).join(", ")}]`;
const pyTuple = (items: string[]) => `(${items.map(pyStr).join(", ")})`;
const sorted = (items: Iterable<string>) => [...items].sort();

/** Styles written for this kit (library CSS from Oh My Etch / Menu Builder is left as shipped). */
function owned(sid: string, s: { selector: string }): boolean {
  return sid === "main-colors" || (/\.(main|site-header)/.test(s.selector) && !s.selector.includes(":where(.site-header *)"));
}

function walkBlocks(p: any, visit: (b: Block) => void): void {
  const walk = (b: Block) => {
    visit(b);
    for (const c of b.innerBlocks || []) walk(c);
  };
  walk(p.gutenbergBlock);
  for (const c of Object.values<any>(p.components || {})) for (const b of c.blocks) walk(b);
}

export function readPrivateTerms(path: string): string[] {
  if (!existsSync(path)) return [];
  return readFileSync(path, "utf8").split(/(?<=\n)/)
    .filter((t) => t.trim() && !t.startsWith("#")).map((t) => t.trim());
}

/** files: {path: file text}, e.g. {"etch-sections/main-faq.etch.txt": "{...}"} */
export function audit(files: Record<string, string>, opts: AuditOptions = {}): AuditResult {
  const paths = sorted(Object.keys(files));
  const P: Record<string, any> = Object.fromEntries(paths.map((f) => [f, JSON.parse(files[f]!)]));
  const errors: string[] = [];
  const warnings: string[] = [];

  // ---------------------------------------------------------------- 1. shared selectors / keys must be identical
  const sel = new Map<string, Map<string, string>>();
  const comp = new Map<string, Map<string, string>>();
  const loops = new Map<string, Map<string, string>>();
  const put = (table: Map<string, Map<string, string>>, key: string, f: string, value: string) => {
    if (!table.has(key)) table.set(key, new Map());
    table.get(key)!.set(f, value);
  };
  for (const f of paths) {
    const p = P[f];
    for (const s of Object.values<any>(p.styles)) put(sel, pyTuple([s.selector, s.type]), f, s.css);
    for (const c of Object.values<any>(p.components || {})) {
      put(comp, c.key, f, pyDumps({ blocks: c.blocks, properties: c.properties }, { sortKeys: true }));
    }
    for (const l of Object.values<any>(p.loops || {})) put(loops, l.key, f, pyDumps(l.config, { sortKeys: true }));
  }
  for (const [what, table] of [["selector", sel], ["component", comp], ["loop", loops]] as const) {
    for (const [key, d] of table) {
      if (new Set(d.values()).size > 1) errors.push(`${what} ${key} differs between ${pyList(sorted(d.keys()))}`);
    }
  }

  // ---------------------------------------------------------------- 2. colours only from the main colours
  for (const f of paths) {
    const p = P[f];
    const name = f.split("/").at(-1);
    if (!("main-colors" in p.styles)) errors.push(`${f}: missing main-colors`);
    for (const [sid, s] of Object.entries<any>(p.styles)) {
      if (sid === "main-colors" || !owned(sid, s)) continue;
      const css = s.css.replace(/\/\*.*?\*\//gs, "").replace(/white-space:[^;]+;/g, "");
      for (const m of css.matchAll(COLOR_LIT)) errors.push(`${name} ${s.selector}: hard-coded colour '${m[0]}'`);
      for (const m of css.matchAll(RAW_REM)) {
        errors.push(`${name} ${s.selector}: raw '${m[0]}' — use to-rem(px) so it fits any root font size`);
      }
      for (const m of css.matchAll(ACSS_COLOR)) errors.push(`${name} ${s.selector}: ACSS colour '${m[0]})' — use --main-*`);
    }
  }

  // ---------------------------------------------------------------- 3. every style id used by a block exists
  for (const f of paths) {
    const p = P[f];
    const used = new Set<string>();
    walkBlocks(p, (b) => { for (const s of b.attrs?.styles || []) used.add(s); });
    for (const sid of sorted([...used].filter((s) => !(s in p.styles)))) {
      errors.push(`${f}: block uses missing style ${sid}`);
    }

    // an element with a styles array only keeps the classes that have a style record
    walkBlocks(p, (b) => {
      const a = b.attrs || {};
      if (a.styles?.length && "class" in (a.attributes || {})) {
        const have = new Set<string>();
        for (const sid of a.styles) {
          const m = sid in p.styles ? CLASS_SELECTOR.exec(p.styles[sid].selector) : null;
          if (m) have.add(m[1]!);
        }
        const lost = new Set(String(a.attributes.class).split(/\s+/).filter((c) => c && !c.includes("{")));
        for (const c of have) lost.delete(c);
        if (lost.size) errors.push(`${f}: '${a.metadata?.name}' would lose class ${pyList(sorted(lost))} on paste`);
      }
    });
    if (p.customMediaDefinitions && Object.keys(p.customMediaDefinitions).length) {
      warnings.push(`${f}: has customMediaDefinitions (overwrites the target's)`);
    }
  }

  // ---------------------------------------------------------------- 4. leftovers from the source sites
  // Uploads from the source sites and real phone numbers (the samples are 02-000-0000 / +6620000000).
  // Client names are not written here: they come from _build/private-terms.txt (git-ignored).
  const escape = (t: string) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const left = new RegExp("wp-content/uploads/(?!2026/01/menu-1\\.svg)"
    + `|(?<![${W}-])(?:\\+66|0)\\p{Nd}{1,2}-\\p{Nd}{3}-\\p{Nd}{4}(?![${W}-])`
    + (opts.privateTerms || []).map((t) => "|" + escape(t)).join(""), "giu");
  const texts: [string, string][] = [...paths.map((f): [string, string] => [f, files[f]!]),
    ...sorted(Object.keys(opts.sources || {})).map((f): [string, string] => [f, opts.sources![f]!])];
  for (const [f, textOf] of texts) {
    const hits = new Set([...textOf.matchAll(left)].map((m) => m[0]));
    for (const s of SAMPLE_PHONES) hits.delete(s);
    if (hits.size) warnings.push(`${f}: source-site leftovers ${pyList(sorted(hits))}`);
  }

  const lines: string[] = [];
  for (const f of paths) {
    const p = P[f];
    const keys = Object.values<any>(p.components || {}).map((c) => c.key);
    const btn = sorted(new Set((JSON.stringify(p.gutenbergBlock) + JSON.stringify(p.components || {}))
      .match(/btn--[A-Za-z0-9_-]+/g) || []));
    lines.push(`  ${f}: ${Object.keys(p.styles).length} styles, components=${pyList(keys)}`
      + `, loops=${pyList(Object.keys(p.loops || {}))}, buttons=${pyList(btn)}`);
  }
  for (const w of warnings) lines.push(`  warning: ${w}`);
  for (const e of errors) lines.push(`  ERROR: ${e}`);
  lines.push(`audit: ${paths.length} files, ${errors.length} errors, ${warnings.length} warnings`);
  return { errors, warnings, lines };
}
