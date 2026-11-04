/** Python formatting the kit depends on, so the TypeScript build writes the same bytes as _build/*.py. */

/**
 * Python's f"{x:g}": 6 significant digits, trailing zeros dropped, exponent form when the exponent is below -4
 * or at least 6. Rounding follows JavaScript's toExponential / toFixed, which only differs from Python on exact
 * binary ties at the 7th digit (none occur in the kit's lengths).
 */
export function formatG(x: number): string {
  if (Number.isNaN(x)) return "nan";
  if (!Number.isFinite(x)) return x > 0 ? "inf" : "-inf";
  if (x === 0) return Object.is(x, -0) ? "-0" : "0";
  const P = 6;
  const [mantissa, expText] = x.toExponential(P - 1).split("e") as [string, string];
  const exp = Number(expText);
  const strip = (s: string) => (s.includes(".") ? s.replace(/0+$/, "").replace(/\.$/, "") : s);
  if (exp < -4 || exp >= P) {
    const sign = exp < 0 ? "-" : "+";
    return `${strip(mantissa)}e${sign}${String(Math.abs(exp)).padStart(2, "0")}`;
  }
  return strip(x.toFixed(P - 1 - exp));
}

/**
 * Python's json.dumps(v, ensure_ascii=False) with its default separators ", " and ": ".
 * Strings escape the same way as JSON.stringify. Numbers are written by JavaScript, so a float like 1.0
 * or 1e-07 would differ from Python. The kit has none, and the byte checks of the golden files guard this.
 */
export function pyDumps(value: unknown, opts: { sortKeys?: boolean } = {}): string {
  if (value === null || typeof value !== "object") return JSON.stringify(value) ?? "null";
  if (Array.isArray(value)) return `[${value.map((v) => pyDumps(v, opts)).join(", ")}]`;
  let keys = Object.keys(value);
  if (opts.sortKeys) keys = keys.sort();
  const obj = value as Record<string, unknown>;
  return `{${keys.map((k) => `${JSON.stringify(k)}: ${pyDumps(obj[k], opts)}`).join(", ")}}`;
}

/** base64.b64encode(s.encode()).decode() */
export function b64encode(s: string): string {
  return Buffer.from(s, "utf8").toString("base64");
}

/** base64.b64decode(s).decode() */
export function b64decode(s: string): string {
  return Buffer.from(s, "base64").toString("utf8");
}
