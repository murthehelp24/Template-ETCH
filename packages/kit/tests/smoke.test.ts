import { describe, expect, it } from "vitest";
import { version } from "../src/index";

describe("@template/kit", () => {
  it("exports its version", () => {
    expect(version).toBe("0.0.0");
  });
});
