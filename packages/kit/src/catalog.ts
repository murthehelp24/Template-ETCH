/** Every template the kit builds, in the build order of _build/build_all.py (filled in by Tasks 5–9). */
import type { Payload } from "./etch/lib";
import * as sections from "./sections/sections";
import * as sectionsMore from "./sections/sectionsMore";
import * as heroMore from "./sections/heroMore";
import * as featuresMore from "./sections/featuresMore";
import * as contentMore from "./sections/contentMore";

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
  // build_sections_more.py
  ...group("etch-sections", ["main-hero", "main-page-hero", "main-features", "main-split", "main-stats", "main-steps",
    "main-reviews", "main-404"], sectionsMore.build),
  // build_hero_more.py
  ...group("etch-sections", ["main-hero-image", "main-hero-collage", "main-hero-panel", "main-hero-gradient"],
    heroMore.build),
  // build_features_more.py
  ...group("etch-sections", ["main-features-image", "main-features-numbered", "main-features-band",
    "main-features-cards", "main-features-list"], featuresMore.build),
  // build_content_more.py
  ...group("etch-sections", ["main-split-overlap", "main-split-band", "main-split-stats", "main-split-images",
    "main-split-full", "main-stats-light", "main-stats-cards", "main-stats-split", "main-stats-image",
    "main-steps-line", "main-steps-vertical", "main-steps-cards", "main-steps-band", "main-reviews-featured",
    "main-reviews-band", "main-reviews-split"], contentMore.build),
];
