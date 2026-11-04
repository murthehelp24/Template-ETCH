/** Source copies the templates are built from (packages/kit/data — copies of _build/src). */
import { readFileSync } from "node:fs";
import { join } from "node:path";

export const DATA_DIR = join(import.meta.dirname, "..", "data");

export function loadData(name: string): any {
  return JSON.parse(readFileSync(join(DATA_DIR, name), "utf8"));
}
