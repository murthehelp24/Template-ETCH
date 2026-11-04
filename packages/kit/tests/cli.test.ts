import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { afterAll, describe, expect, it } from "vitest";
import { goldenPaths, goldenText, stripTsText } from "./helpers";

describe("pnpm build:kit (src/cli/build.ts)", () => {
  const out = mkdtempSync(join(tmpdir(), "kit-build-"));
  afterAll(() => rmSync(out, { recursive: true, force: true }));
  const stdout = execFileSync("npx", ["tsx", "src/cli/build.ts", "--out", out],
    { cwd: join(import.meta.dirname, ".."), encoding: "utf8" });

  it("prints a clean audit of all 58 templates", () => {
    expect(stdout.trim().split("\n").at(-1)).toBe("audit: 58 files, 0 errors, 0 warnings");
  });

  it("writes every template equal to its golden file, the timestamp aside", () => {
    for (const path of goldenPaths()) {
      expect(stripTsText(readFileSync(join(out, path), "utf8")), path).toBe(stripTsText(goldenText(path)));
    }
  });
});
