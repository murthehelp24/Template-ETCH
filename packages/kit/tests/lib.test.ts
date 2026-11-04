import { describe, expect, it } from "vitest";
import * as L from "../src/etch/lib";
import fixtures from "./fixtures/lib.json";

// tests/fixtures/lib.json is written by make_lib_fixtures.py from _build/lib_etch.py itself
const FN: Record<string, (...args: any[]) => unknown> = {
  text: L.text, block: L.block, el: L.el, img: L.img, svg: L.svg, cond: L.cond, loop: L.loop,
  slot_placeholder: L.slotPlaceholder, prop: L.prop, data_uri: L.dataUri, portable: L.portable, style: L.style,
};

describe("etch/lib equals _build/lib_etch.py", () => {
  for (const [name, args, want] of fixtures.cases as [string, unknown[], unknown][]) {
    it(`${name}(${JSON.stringify(args).slice(1, 60)})`, () => {
      expect(FN[name], name).toBeDefined();
      expect(FN[name]!(...structuredClone(args))).toEqual(want);
    });
  }

  it("payload() equals Python, key order and bytes included", () => {
    for (const [args, want, text] of fixtures.payload as [any[], any, string][]) {
      const [gblock, styles, components, loops] = structuredClone(args);
      const p = L.payload(gblock, styles, components, loops, () => fixtures.timestamp);
      expect(p).toEqual(want);
      expect(L.serialize(p)).toBe(text);
    }
  });

  it("payload() stops on a style id that is not in the styles", () => {
    const b = L.el("Box", "div", {}, ["mn-missing"]);
    expect(() => L.payload(b, {})).toThrow(/mn-missing/);
  });

  it("rawStyle() keeps rem as written (the header builders do not call portable)", () => {
    expect(L.rawStyle(".a", "margin: 1.2rem;")).toEqual({
      type: "class", selector: ".a", collection: "default", css: "margin: 1.2rem;" });
    expect(L.style(".a", "margin: 1.2rem;").css).toBe("margin: to-rem(12px);");
  });
});
