import { describe, expect, it } from "vitest";
import { b64decode, b64encode, formatG, pyDumps } from "../src/etch/pycompat";

describe("formatG — Python f'{x:g}'", () => {
  it.each([
    [24, "24"],
    [12.5, "12.5"],
    [1.4 * 10, "14"], // 14.000000000000002
    [0.8, "0.8"],
    [0, "0"],
    [-3.5, "-3.5"],
    [100, "100"],
    [123456, "123456"],
    [1234567, "1.23457e+06"],
    [0.0001, "0.0001"],
    [1e-5, "1e-05"],
    [0.1 + 0.2, "0.3"],
    [2.5e-7, "2.5e-07"],
    [1e21, "1e+21"],
    [999999.5, "1e+06"],
  ])("%s → %s", (x, want) => {
    expect(formatG(x)).toBe(want);
  });
});

describe("pyDumps — json.dumps(v, ensure_ascii=False) with the default separators", () => {
  it("puts a space after , and :", () => {
    expect(pyDumps({ a: [1, "x"], b: true, c: null })).toBe('{"a": [1, "x"], "b": true, "c": null}');
  });
  it("keeps Thai and escapes like Python", () => {
    expect(pyDumps({ t: 'ไทย "q" \\ \n\t' })).toBe('{"t": "ไทย \\"q\\" \\\\ \\n\\t"}');
  });
  it("writes empty containers without spaces", () => {
    expect(pyDumps({ a: [], b: {} })).toBe('{"a": [], "b": {}}');
  });
  it("can sort keys like sort_keys=True", () => {
    expect(pyDumps({ b: 1, a: { d: 2, c: 3 } }, { sortKeys: true })).toBe('{"a": {"c": 3, "d": 2}, "b": 1}');
  });
});

describe("base64 — utf-8 like base64.b64encode(s.encode())", () => {
  it("round-trips Thai text", () => {
    expect(b64encode("ไทย")).toBe("4LmE4LiX4Lii");
    expect(b64decode("4LmE4LiX4Lii")).toBe("ไทย");
  });
});
