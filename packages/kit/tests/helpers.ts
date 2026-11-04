import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";

/** Golden .etch.txt files frozen from main @ 3db436d (never edit them to make a test pass). */
export const GOLDEN_DIR = join(import.meta.dirname, "golden");

function walk(dir: string): string[] {
  return readdirSync(dir).flatMap((name) => {
    const full = join(dir, name);
    return statSync(full).isDirectory() ? walk(full) : [full];
  });
}

/** Paths relative to the kit root, e.g. "etch-sections/main-faq.etch.txt", sorted. */
export function goldenPaths(): string[] {
  return walk(GOLDEN_DIR)
    .filter((f) => f.endsWith(".etch.txt"))
    .map((f) => relative(GOLDEN_DIR, f).split("\\").join("/"))
    .sort();
}

export function goldenText(path: string): string {
  return readFileSync(join(GOLDEN_DIR, path), "utf8");
}

export function loadGolden(): Record<string, any> {
  return Object.fromEntries(goldenPaths().map((p) => [p, JSON.parse(goldenText(p))]));
}

/** The build time is the only thing allowed to change between builds. */
export function stripTs<T extends { timestamp?: unknown }>(payload: T): Omit<T, "timestamp"> {
  const { timestamp: _ignored, ...rest } = payload;
  return rest;
}

/** Same as check.py's strip_ts, for byte-level comparison of serialized files. */
export function stripTsText(text: string): string {
  return text.replace(/"timestamp":"[^"]*"/g, "");
}
