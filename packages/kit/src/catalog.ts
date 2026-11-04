/** Every template the kit builds, in the build order of _build/build_all.py (filled in by Tasks 5–9). */
import type { Payload } from "./etch/lib";
import * as sections from "./sections/sections";

export interface CatalogEntry {
  /** output path relative to the kit root, e.g. "etch-sections/main-faq.etch.txt" */
  path: string;
  /** the Etch copy payload */
  build: () => Payload;
}

/** One entry per output of a builder module whose build() returns { name: payload }. */
function group(dir: string, names: string[], build: () => Record<string, Payload>): CatalogEntry[] {
  return names.map((name) => ({
    path: `${dir}/${name}.etch.txt`,
    build: () => {
      const p = build()[name];
      if (!p) throw new Error(`${name} is not built`);
      return p;
    },
  }));
}

export const catalog: CatalogEntry[] = [
  // build_sections.py
  ...group("etch-sections", ["main-faq", "main-cta", "main-blog", "main-single-post", "main-contact"], sections.build),
];
