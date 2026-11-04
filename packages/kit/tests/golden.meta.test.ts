import { describe, expect, it } from "vitest";
import { goldenPaths, loadGolden } from "./helpers";

describe("golden files", () => {
  const paths = goldenPaths();

  it("holds the 58 templates of main @ 3db436d", () => {
    const count = (dir: string) => paths.filter((p) => p.startsWith(dir + "/")).length;
    expect(paths).toHaveLength(58);
    expect(count("etch-header")).toBe(7);
    expect(count("etch-footer")).toBe(5);
    expect(count("etch-sections")).toBe(46);
  });

  it("are Etch copy payloads with the shared colour variables", () => {
    for (const [path, p] of Object.entries(loadGolden())) {
      expect(p.type, path).toBe("block");
      expect(p.version, path).toBe(2.1);
      expect(p.styles["main-colors"], path).toBeDefined();
      expect(typeof p.timestamp, path).toBe("string");
    }
  });
});
