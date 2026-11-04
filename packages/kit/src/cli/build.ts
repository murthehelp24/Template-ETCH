/**
 * Rebuild every template into the kit folders, then run the audit (replaces the kit part of _build/build_all.py).
 *
 *     pnpm build:kit                 # writes etch-header/, etch-footer/, etch-sections/ at the repo root
 *     pnpm build:kit --out <dir>     # writes them under <dir> instead
 *
 * Exits with 1 when the audit finds errors. Private terms come from _build/private-terms.txt (git-ignored);
 * the source copies in packages/kit/data are scanned for leftovers too, as audit.py scans _build/src.
 */
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, relative, resolve } from "node:path";
import { audit, readPrivateTerms } from "../audit";
import { catalog } from "../catalog";
import { DATA_DIR } from "../data";
import { serialize } from "../etch/lib";

const ROOT = resolve(import.meta.dirname, "..", "..", "..", "..");
const args = process.argv.slice(2);
const at = args.indexOf("--out");
const out = at >= 0 && args[at + 1] ? resolve(args[at + 1]!) : ROOT;

const files: Record<string, string> = {};
for (const entry of catalog) {
  const text = serialize(entry.build());
  const path = join(out, entry.path);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, text);
  files[entry.path] = text;
  console.log("ok", entry.path);
}

const sources = Object.fromEntries(readdirSync(DATA_DIR).filter((f) => f.endsWith(".json")).map((f) =>
  [relative(ROOT, join(DATA_DIR, f)), readFileSync(join(DATA_DIR, f), "utf8")]));
const result = audit(files, { privateTerms: readPrivateTerms(join(ROOT, "_build", "private-terms.txt")), sources });
for (const line of result.lines) console.log(line);
process.exit(result.errors.length ? 1 : 0);
