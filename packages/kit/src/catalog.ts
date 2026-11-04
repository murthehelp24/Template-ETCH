/** Every template the kit builds, in the build order of _build/build_all.py (filled in by Tasks 5–9). */
export interface CatalogEntry {
  /** output path relative to the kit root, e.g. "etch-sections/main-faq.etch.txt" */
  path: string;
  /** the Etch copy payload */
  build: () => Record<string, unknown> & { timestamp?: string };
}

export const catalog: CatalogEntry[] = [];
