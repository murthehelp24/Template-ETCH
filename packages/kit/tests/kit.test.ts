import { describe, expect, it } from "vitest";
import * as K from "../src/kit";
import { ICONS } from "../src/kit/icons";
import fixtures from "./fixtures/kit.json";

// tests/fixtures/kit.json is written by make_kit_fixtures.py from _build/kit.py and _build/icons.py
const CONSTANTS: Record<string, unknown> = {
  COLORS_CSS: K.COLORS_CSS, COLORS: K.COLORS, BASE: K.BASE, SEC: K.SEC, CON: K.CON,
  HEADING_STYLES: K.HEADING_STYLES, BAND_STYLES: K.BAND_STYLES, SOCIAL_STYLES: K.SOCIAL_STYLES,
  SOCIALS: K.SOCIALS, SOCIAL_PROPS: K.SOCIAL_PROPS, CARD_STYLES: K.CARD_STYLES, MEDIA_STYLES: K.MEDIA_STYLES,
  BUTTONS_STYLES: K.BUTTONS_STYLES, CHECKS_STYLES: K.CHECKS_STYLES,
};
const FN: Record<string, (...args: any[]) => unknown> = {
  icon: K.icon, heading: K.heading, social_link: K.socialLink, social_list: K.socialList, card: K.card,
  media_img: K.mediaImg, buttons: K.buttons, checks: K.checks,
};
// keyword arguments of the Python calls, in the TypeScript signature's position
const KW_ORDER: Record<string, string[]> = {
  heading: ["eyebrow", "title", "intro", "tag", "center"],
};

function args(name: string, positional: unknown[], kw: Record<string, unknown>): unknown[] {
  const order = KW_ORDER[name];
  if (!order || !Object.keys(kw).length) return positional;
  const defaults: Record<string, unknown> = { intro: undefined, tag: undefined, center: undefined };
  const all = Object.fromEntries(order.map((k, i) => [k, i < positional.length ? positional[i] : defaults[k]]));
  Object.assign(all, kw);
  return order.map((k) => all[k]);
}

describe("kit/ equals _build/kit.py", () => {
  it("icons", () => {
    expect(ICONS).toEqual(fixtures.icons);
    expect(Object.keys(ICONS)).toEqual(Object.keys(fixtures.icons));
  });

  for (const [name, want] of Object.entries(fixtures.constants)) {
    it(`constant ${name}`, () => {
      expect(CONSTANTS[name], name).toBeDefined();
      expect(CONSTANTS[name]).toEqual(want);
      if (want && typeof want === "object" && !Array.isArray(want)) {
        expect(Object.keys(CONSTANTS[name] as object)).toEqual(Object.keys(want)); // style order is paste order
      }
    });
  }

  for (const [name, positional, kw, want] of fixtures.calls as [string, unknown[], Record<string, unknown>, unknown][]) {
    it(`${name}(${JSON.stringify([positional, kw]).slice(1, 70)})`, () => {
      expect(FN[name], name).toBeDefined();
      expect(FN[name]!(...args(name, positional, kw))).toEqual(want);
    });
  }

  it("kitPayload adds the colour variables first", () => {
    const [b, styles] = fixtures.kit_payload.args as [any, any];
    const p = K.kitPayload(b, styles, null, null, () => fixtures.timestamp);
    expect(p).toEqual(fixtures.kit_payload.result);
    expect(JSON.stringify(p)).toBe(JSON.stringify(fixtures.kit_payload.result));
  });
});
