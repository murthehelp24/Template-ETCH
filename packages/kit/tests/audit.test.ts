import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import { audit, readPrivateTerms } from "../src/audit";
import { serialize } from "../src/etch/lib";
import { catalog } from "../src/catalog";
import { goldenPaths, goldenText } from "./helpers";

// tests/fixtures/audit is written by make_audit_fixtures.py, which also runs the real _build/audit.py on it
const FIX = join(import.meta.dirname, "fixtures", "audit");
const expected = JSON.parse(readFileSync(join(FIX, "expected.json"), "utf8"));
const FIX_FILES = ["etch-a/one.etch.txt", "etch-a/two.etch.txt", "etch-b/colours.etch.txt",
  "etch-b/leftovers.etch.txt", "etch-b/missing.etch.txt"];

describe("audit equals _build/audit.py", () => {
  const files = Object.fromEntries(FIX_FILES.map((f) => [f, readFileSync(join(FIX, f), "utf8")]));
  const result = audit(files, { privateTerms: readPrivateTerms(join(FIX, "_build", "private-terms.txt")) });

  it("prints the same report, warnings, errors and summary", () => {
    expect(result.lines.join("\n") + "\n").toBe(expected.stdout);
  });

  it("fails like Python (exit code 1 with errors)", () => {
    expect(result.errors.length > 0 ? 1 : 0).toBe(expected.code);
  });

  it.each([
    ["1 — same selector, different CSS", /^selector \('\.main-x', 'class'\) differs/],
    ["1 — same component key, different blocks", /^component SharedKey differs/],
    ["1 — same loop key, different config", /^loop loopA differs/],
    ["2 — no colour variables", /missing main-colors$/],
    ["2 — hard-coded colour", /hard-coded colour '#fff'$/],
    ["2 — raw rem", /raw '2rem'/],
    ["2 — ACSS colour", /ACSS colour 'var\(--primary\)'/],
    ["3 — missing style id", /block uses missing style mn-nope$/],
    ["3 — class lost on paste", /'Loses Class' would lose class \['extra-one', 'extra-two'\]/],
  ])("rule %s is an error", (_name, re) => {
    expect(result.errors.some((e) => re.test(e))).toBe(true);
  });

  it.each([
    ["3 — customMediaDefinitions", /has customMediaDefinitions/],
    ["4 — uploads, real phone numbers and private terms", /leftovers \['081-234-5678', 'ACME Clinic', 'wp-content\/uploads\/'\]/],
  ])("rule %s is a warning", (_name, re) => {
    expect(result.warnings.some((w) => re.test(w))).toBe(true);
  });

  it("leaves comments, white-space, library styles and ACSS sizes alone", () => {
    const all = result.errors.join("\n");
    expect(all).not.toMatch(/'#000'|'black'/); // only inside a comment
    expect(all).not.toMatch(/\.ome-x|site-header \*/); // library CSS as shipped
    expect(all).not.toMatch(/--primary-l|--space-m/); // ACSS size tokens are not colours
    expect(all.match(/'white'/g)).toHaveLength(1); // white-space: nowrap does not count
  });
});

describe("the kit passes its own audit", () => {
  it("golden: 58 files, 0 errors, 0 warnings", () => {
    const files = Object.fromEntries(goldenPaths().map((p) => [p, goldenText(p)]));
    const result = audit(files);
    expect(result.errors).toEqual([]);
    expect(result.lines.at(-1)).toBe("audit: 58 files, 0 errors, 0 warnings");
  });

  it("the TypeScript build: 0 errors", () => {
    const files = Object.fromEntries(catalog.map((e) => [e.path, serialize(e.build())]));
    expect(audit(files).errors).toEqual([]);
  });
});
