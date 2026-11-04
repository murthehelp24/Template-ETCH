import { describe, expect, it } from "vitest";
import { catalog } from "../src/catalog";
import { serialize } from "../src/etch/lib";
import { goldenPaths, goldenText, loadGolden, stripTs, stripTsText } from "./helpers";

// every template the TypeScript kit builds must equal its golden file, the build time aside;
// templates not ported yet show up as todo so the report says how many are left
describe("TypeScript build equals the golden files", () => {
  const golden = loadGolden();
  const built = new Map(catalog.map((entry) => [entry.path, entry]));

  it("catalog only names golden files", () => {
    for (const path of built.keys()) expect(golden[path], path).toBeDefined();
  });

  for (const path of goldenPaths()) {
    const entry = built.get(path);
    if (!entry) {
      it.todo(path);
      continue;
    }
    it(path, () => {
      const p = entry.build();
      expect(stripTs(p)).toEqual(stripTs(golden[path]));
      // toEqual ignores key order; the written file must match byte for byte (styles paste in key order)
      expect(stripTsText(serialize(p))).toBe(stripTsText(goldenText(path)));
    });
  }
});
