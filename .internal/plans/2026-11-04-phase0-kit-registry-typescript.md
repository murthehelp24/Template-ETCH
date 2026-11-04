# แผนเฟส 0: ย้าย template kit จาก Python เป็น TypeScript (`packages/kit`)

> สถานะ: **ร่าง — รออนุมัติ** · spec: `.internal/specs/2026-10-31-nextjs-template-builder-design.md` · branch `phase0-kit-ts`

## เป้าหมายและเกณฑ์เสร็จ

ย้าย `_build/*.py` ส่วนที่สร้าง `.etch.txt` และ audit ไปเป็น TypeScript ใน `packages/kit`
โดย**ผลลัพธ์ต้องเหมือนเดิมทุกไฟล์** เฟสนี้เปลี่ยนแค่ภาษา ไม่เปลี่ยนเนื้อหา, CSS, ชื่อคลาส, style id,
component id/key (`990001–990006`, `990101`, `990102`, `1843–1849`, `1971–1974`) หรือ loop key (`mainRelatedPosts`)

**ต่างจาก prompt เดิม (ผู้ใช้เลือกแล้ว 2026-11-04):** prompt เขียนว่า "16 ไฟล์ / golden จาก commit `3b4e3c1`"
แต่ kit ตอนนี้มี **58 ไฟล์** และโค้ด Python เปลี่ยนไปมาก ผู้ใช้จึงเลือกให้ย้าย**ชุดปัจจุบัน**:
golden = `.etch.txt` ทั้ง 58 ไฟล์ที่ `main` @ `3db436d` และเลข 16 ในเกณฑ์ทุกข้อเปลี่ยนเป็น 58

เสร็จเมื่อ:
- `pnpm test` ผ่านทั้งหมด: golden 58/58, audit และ unit
- `pnpm build:kit` พิมพ์ `audit: 58 files, 0 errors` และ `.etch.txt` เปลี่ยนแค่ timestamp (สคริปต์ใน Task 10 Step 3 ขึ้น `SAME` ทั้ง 58)
- `python3 _build/check.py` ยังผ่าน (CI เดิมยังเขียว)
- รายงานผล: เทสต์ที่รันพร้อม output จริง, รายการ commit, สิ่งที่ค้างหรือข้าม

ไม่อยู่ในเฟสนี้:
- preview/builder เดิม (`render_preview.py`, `build_preview.py`, `acss_sim.py`, `build_site.py`, `builder/`) ยังเป็น Python/JS เหมือนเดิม
  ส่วนนี้อ่าน `.etch.txt` อย่างเดียว จึงใช้ต่อได้ทันที
- `defineSection` / zod schema เป็นของเฟส 2 (เฟสนี้ทำแค่ catalog)

## กติกาการทำงาน

- **TDD ทุก Task:** เขียนเทสต์ → รันให้เห็นว่าล้ม (เก็บ output) → เขียนโค้ด → รันให้ผ่าน → commit ทีละ Task
  (ข้อความ commit ขึ้นต้นด้วย `phase0:`)
- **golden:** อยู่ใน `packages/kit/tests/golden/` ห้ามแก้เพื่อให้เทสต์ผ่าน ถ้าไม่ตรง ให้แก้โค้ด TS
- **audit:** ทั้ง 4 กลุ่มกติกาของ `_build/audit.py` ต้องบังคับใช้ครบ ห้ามลด
- **`_build/`:** ห้ามลบเอง ให้หยุดที่ Task 10 Step 5 แล้วถามผู้ใช้ เพราะผู้ใช้ต้อง Paste ทดสอบบน Etch staging ก่อน

## ตารางแปล Python → TypeScript (จุดที่ทำให้ไม่ตรงกันทีละ byte)

| Python | TypeScript | หมายเหตุ |
|---|---|---|
| `f"{x:g}"` ใน `portable()` (`to-rem({px:g}px)`) | `formatG(x)` | precision 6 ตัด 0 ท้าย เช่น `14.000000000000002 → "14"`, `12.5 → "12.5"` และใช้รูป e เมื่อ exp < -4 หรือ ≥ 6 · ห้ามใช้ `String(x)` |
| `json.dumps(v, ensure_ascii=False)` (separator default `", "` / `": "`) ใน `comp()` ของ header Oh My Etch: props แต่ละกลุ่มเก็บเป็น JSON string | `pyDumps(v)` | `JSON.stringify` ไม่มีช่องว่าง จึงต้องเขียน serializer เอง: `[a, b]`, `{"k": v}` |
| `json.dumps(p, ensure_ascii=False, separators=(",", ":"))` (เขียนไฟล์) | `JSON.stringify(p)` | ให้ผลเดียวกันกับข้อมูลชุดนี้ (ไม่มี float เลขจำนวนเต็มอย่าง `1.0` และไม่มี object ที่มี key ตัวเลขปนกับ key อื่น ตรวจแล้ว) มีเทสต์ byte กันไว้ |
| header ทั้งสองไฟล์ (`build_header_ome.py`, `build_header_menubuilder.py`) มี `style()` ของตัวเอง**ที่ไม่เรียก `portable()`** | `rawStyle()` แยกจาก `style()` | ถ้าใช้ `style()` ของ lib จะได้ `to-rem()` เพิ่มเข้าไปใน CSS ของ header |
| `build_header_variants.py` / `build_footer_variants.py` ใช้ `style()` ของ lib (มี portable) | `style()` | ระวังอย่าสลับกับข้อบน |
| `comp()` / `slot()` ของ header ome สร้าง `innerHTML` / `innerContent` เอง: `comp()` ใช้ `innerHTML: "\n\n"` เสมอ และ `innerContent: ["\n", None, "\n"]` แม้มีลูกหลายตัว (ต่างจาก `block()` ของ lib ที่ใส่ `None` ต่อลูกหนึ่งตัว) | port สูตรของแต่ละฟังก์ชันตรงตัว | ห้ามแทนด้วย `block()` ของ lib |
| `{**a, **b}`, `{**a, "k": v}` | `{...a, ...b}` | key ซ้ำ: Python และ JS เก็บตำแหน่งแรก ค่าเป็นตัวหลัง (เหมือนกัน) |
| ลำดับ key ของ dict | ลำดับ key ของ object | JS เรียง key ที่เป็นเลขจำนวนเต็มขึ้นก่อน: `components` มี key `"990001"` (แต่ละไฟล์ key เดียว, OME 6 key เรียงอยู่แล้ว) ถ้าในอนาคตต้องปน ให้ใช้ `Map` |
| `copy.deepcopy`, `json.loads(json.dumps(x))` | `structuredClone(x)` | |
| ตัวแปร variants อ่าน `site-header-ohmyetch.etch.txt` / `main-footer.etch.txt` จากดิสก์ | ส่ง object ที่ผ่าน `JSON.parse(JSON.stringify(base))` | ได้ผลเท่ากับการอ่านไฟล์ (รวม timestamp ที่จะถูกทับใหม่) |
| `base64.b64encode(s.encode())` / `b64decode` (script ของ header, `data_uri` ของไอคอน) | `Buffer.from(s, "utf8").toString("base64")` | utf-8 ทั้งสองฝั่ง |
| `datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00","Z")` | `new Date().toISOString()` | รูปแบบเดียวกัน · ให้ฉีด `now()` ได้ เพื่อให้เทสต์คงที่ |
| `re.sub` / lookbehind `(?<![\w.-])` | `String.replace` + regex flag `g` | JS รองรับ lookbehind · `re.S` → flag `s` · `re.I` → `i` |
| `str.split()` (ไม่ใส่ตัวคั่น) | `s.split(/\s+/).filter(Boolean)` | |
| `sorted(set)` | `[...set].sort()` | ข้อความเป็น ASCII ทั้งหมด ลำดับจึงเท่ากัน |
| `sum(lists, [])`, `"\n\n" * n` | `lists.flat()`, `"\n\n".repeat(n)` | `max(n, 0)` → `Math.max` |
| `assert not missing` ใน `payload()` | `throw new Error(...)` | style id ที่ไม่มีจริงต้องหยุด build |
| `dict.items()` ที่ข้าม key | `Object.entries` | |

## โครงไฟล์

```
pnpm-workspace.yaml            packages: ["packages/*", "apps/*"]
package.json                   scripts: test, build:kit, typecheck · packageManager pnpm
packages/kit/
  package.json  tsconfig.json  vitest.config.ts
  data/                        สำเนาของ _build/src/*.json ที่ build ใช้ (original-copy, ome-copy, ome, lib-styles, src5)
  src/etch/pycompat.ts         formatG, pyDumps, b64
  src/etch/lib.ts              block, el, text, img, svg, cond, loop, slotPlaceholder, prop, dataUri, portable, style, rawStyle, payload, serialize
  src/kit/{colors,base,icons,heading,social,card,media,buttons,checks,index}.ts
  src/sections/{sections,sectionsMore,heroMore,featuresMore,contentMore,faqCtaMore}.ts
  src/footers/{footer,footerVariants}.ts
  src/headers/{ome,omeVariants,menuBuilder}.ts
  src/audit.ts                 audit(files: Record<path, payload>, opts) → { errors, warnings, report }
  src/catalog.ts               ลำดับเดียวกับ JOBS ใน build_all.py → { path, build(ctx) }[]
  src/cli/build.ts             pnpm build:kit: เขียน 58 ไฟล์ → audit → exit 1 ถ้ามี error
  tests/golden/                58 ไฟล์ (โครง etch-header/, etch-footer/, etch-sections/)
  tests/helpers.ts             loadGolden, stripTs, normalize
  tests/*.test.ts
```

---

## Task 1: workspace และ package ว่าง

1. สร้าง `pnpm-workspace.yaml`, root `package.json` (`"test": "pnpm -r test"`, `"build:kit": "pnpm --filter @template/kit build:kit"`) และ `packages/kit` (TypeScript strict, Vitest, `tsx` สำหรับ CLI)
2. เทสต์: `tests/smoke.test.ts` import `../src/index` แล้วเช็กว่า export `version`
3. รัน `pnpm install && pnpm test` → ต้องล้ม (ยังไม่มี src) → เขียน `src/index.ts` → ต้องผ่าน
4. เพิ่ม `node_modules/` ใน `.gitignore` แล้ว commit

## Task 2: แช่แข็ง golden

1. `git show 3db436d:<path>` ทั้ง 58 ไฟล์ แล้วเก็บไว้ที่ `packages/kit/tests/golden/<path>` (ไม่ใช่ copy จาก working tree กันกรณีมีไฟล์แก้ค้าง)
2. เขียน `tests/helpers.ts`: `loadGolden()` คืน `{path: object}` และ `stripTs()` ลบ `"timestamp"`
3. เทสต์ `golden.meta.test.ts`:
   - นับได้ 58 ไฟล์ (header 7, footer 5, sections 46)
   - ทุกไฟล์ parse ได้ มี `version: 2.1` และมี style `main-colors`
4. เทสต์ `golden.test.ts`: วนตาม catalog แล้ว `expect(stripTs(build())).toEqual(stripTs(golden))`
   - catalog ยังว่าง จึงใส่ `test.todo` ต่อไฟล์ เพื่อให้รายงานบอกว่าเหลือกี่ไฟล์
5. commit

## Task 3: `etch/` — py-compat และตัวช่วยระดับล่าง

1. เทสต์ `pycompat.test.ts`:
   - `formatG`: `24 → "24"`, `12.5 → "12.5"`, `14.000000000000002 → "14"`, `0.8 → "0.8"`, `1e-5 → "1e-05"`, `1234567 → "1.23457e+06"`
   - `pyDumps`: `{"a": [1, "x"], "b": true}` ต้องได้ `'{"a": [1, "x"], "b": true}'` และไทยไม่ถูก escape
2. เทสต์ `lib.test.ts`:
   - ค่าคาดหวังสร้างจาก Python ครั้งเดียวด้วยสคริปต์ `tests/fixtures/make_lib_fixtures.py`
     (รัน `python3` แล้ว commit ผล `lib.json` ไว้)
   - ครอบ `el`, `text`, `img`, `svg`, `cond`, `loop`, `prop`, `dataUri`, `portable("1.4rem 2rem .5rem")`, `style`, `payload` (timestamp คงที่)
   - `payload` ที่ใช้ style id ที่ไม่มีอยู่ต้อง throw
3. เขียนโค้ดให้ผ่าน แล้ว commit

## Task 4: `kit/` — ของที่ใช้ร่วมกัน

1. แปลง `_build/kit.py` และ `_build/icons.py`:
   - ค่าคงที่: COLORS, BASE, `*_STYLES`, SEC/CON, SOCIALS, SOCIAL_PROPS
   - ฟังก์ชัน: `heading`, `socialLink`, `socialList`, `card`, `mediaImg`, `buttons`, `checks`, `icon`, `kitPayload`
2. เทสต์: `make_kit_fixtures.py` dump ผลของทุกค่าคงที่และทุกฟังก์ชัน (อาร์กิวเมนต์ตัวอย่าง) เป็น `kit.json`
   แล้ว `toEqual` ทีละตัว
3. commit

## Task 5: sections ชุด 1 — `build_sections.py` (5 ไฟล์)

1. ไฟล์: `main-faq`, `main-cta` (component `990101`), `main-blog`, `main-single-post` (loop `mainRelatedPosts`), `main-contact` (component `990102`)
2. อ่าน `data/src5.json` และ port `find()` / `label_value()` / `CONTACT_PROPS` ตรงตัว
3. เปลี่ยน `test.todo` 5 ไฟล์นี้เป็นเทสต์จริง: รัน → ล้ม → เขียน → ผ่าน
4. commit

## Task 6: sections ชุด 2 — `build_sections_more.py` (8 ไฟล์)

1. ไฟล์: `main-hero`, `main-page-hero`, `main-features`, `main-split`, `main-stats`, `main-steps`, `main-reviews`, `main-404`
2. golden 8/8 แล้ว commit

## Task 7: variants ของ section — 4 สคริปต์ (33 ไฟล์)

1. แปลง 4 สคริปต์:
   - `build_hero_more.py` (4 ไฟล์)
   - `build_features_more.py` (5 ไฟล์)
   - `build_content_more.py` (16 ไฟล์)
   - `build_faq_cta_more.py` (8 ไฟล์)
2. แยก commit ทีละสคริปต์ (4 commit) และแต่ละ commit ต้อง golden ครบตามจำนวนของสคริปต์นั้น
3. จุดระวัง:
   - `section()` ของแต่ละไฟล์มีพารามิเตอร์ต่างกัน (`behind`, `extra`, `con_cls`) ให้ port แยกไฟล์ใครไฟล์มัน
   - การแทนค่าข้อความ CSS ด้วย `.replace()` ใน `hero_more` ต้องให้ผลเหมือนเดิม

## Task 8: footer — `build_footer.py` + `build_footer_variants.py` (5 ไฟล์)

1. ไฟล์: `main-footer` (component `990001`) และ variants `light 990002`, `center 990003`, `map 990005`, `compact 990006`
2. variants สร้างต่อจาก object ของ `main-footer` (ไม่อ่านจากดิสก์) และ port `find`, `set_children`, `drop`
3. golden 5/5 แล้ว commit

## Task 9: header — `build_header_ome.py` + `build_header_variants.py` + `build_header_menubuilder.py` (7 ไฟล์)

1. port แยกทีละไฟล์ใน `headers/`:
   - ใช้ `rawStyle()` (ไม่มี portable)
   - ใช้ `pyDumps` ใน `comp()`
   - script ของ header: decode base64 → แทนข้อความ → encode
2. variants (light, center, topbar, floating, right) สร้างต่อจาก object ของ `site-header-ohmyetch`
3. golden 7/7
   - ถ้าไม่ตรง ห้ามเดา ให้ diff ด้วย flatten-path (เทียบทีละ path ของ JSON) แล้วแก้ทีละจุด
4. commit (แยก ome / variants / menubuilder ได้)

## Task 10: audit + CLI + ตรวจทั้งชุด

- **Step 1: `audit.ts`**
  - เทสต์ก่อน: แต่ละกติกาของ `_build/audit.py` ต้องมีอย่างน้อยหนึ่งเคสที่ล้ม และหนึ่งเคสที่ผ่าน
  - **กติกา 1:**
    - selector เดียวกันแต่ CSS ต่างกัน
    - component key ซ้ำแต่เนื้อหาต่างกัน: Python เทียบ `json.dumps(..., sort_keys=True)` ของ `blocks` + `properties`
      (ใน TS ใช้ `stableStringify` ที่เรียง key เหมือนกัน แค่ต้องเทียบภายใน TS ให้คงเส้นคงวา ไม่ต้องตรงกับ Python ทีละ byte)
    - loop key ซ้ำแต่ config ต่างกัน
  - **กติกา 2:**
    - ไม่มี `main-colors`
    - มีสีหรือคำแบบ `#fff`, `rgb(`, `white` ใน style ที่เป็นของ kit (ไม่นับ comment และ `white-space:`)
    - มี rem ดิบ
    - มีสี ACSS เช่น `var(--primary)`
    - style ของ library (Oh My Etch / Menu Builder และ `:where(.site-header *)`) ได้รับยกเว้น
  - **กติกา 3:**
    - block ใช้ style id ที่ไม่มีอยู่
    - class บน element ที่มี styles ไม่มี record `.class` ("would lose class")
    - warning เมื่อมี `customMediaDefinitions`
  - **กติกา 4:** warning เมื่อพบ `wp-content/uploads/` (ยกเว้น `2026/01/menu-1.svg`), เบอร์จริงนอกจาก
    `02-000-0000` / `+6620000000` และคำใน `_build/private-terms.txt` (อ่านถ้ามีไฟล์)
  - รูปแบบผล: ข้อความ error/warning และบรรทัดสรุป `audit: N files, E errors, W warnings` ต้องเหมือน Python
  - เทสต์: golden ทั้ง 58 ไฟล์ต้องได้ 0 errors
- **Step 2: `cli/build.ts` (`pnpm build:kit`)**
  - เขียนทุกไฟล์ตาม catalog ด้วย `serialize()`, รัน audit, พิมพ์รายงาน และ exit 1 ถ้ามี error
  - ลำดับ build ตาม `build_all.py`: header ome → header variants → menubuilder → footer → footer variants → sections …
- **Step 3: ตรวจทีละ byte** (ไม่นับ timestamp)
  ```bash
  pnpm build:kit
  for f in $(git ls-files 'etch-*/*.etch.txt'); do
    a=$(git show HEAD:$f | sed -E 's/"timestamp":"[^"]*"//'); b=$(sed -E 's/"timestamp":"[^"]*"//' $f)
    [ "$a" = "$b" ] && echo "SAME $f" || echo "DIFF $f"
  done | sort | uniq -c -w4
  git checkout -- 'etch-*/*.etch.txt'   # คืนไฟล์ที่เปลี่ยนแค่ timestamp
  ```
  ต้องได้ `58 SAME`
- **Step 4: CI**
  - เพิ่ม job Node ใน `.github/workflows/` รัน `pnpm install --frozen-lockfile && pnpm test && pnpm build:kit` ต่อด้วยสคริปต์ Step 3
  - job Python เดิม (`_build/check.py`) ยังอยู่
  - ให้ `build_all.py` เรียก `pnpm build:kit` แทนสคริปต์ Python ของ kit ได้ แต่ทำ**หลัง**ผู้ใช้ตอบ Step 5 เท่านั้น
- **Step 5: หยุดและถามผู้ใช้**
  - รายงานผล (เทสต์, commit, สิ่งที่ค้าง)
  - ขอให้ผู้ใช้ Paste ไฟล์ที่ TS สร้างลง Etch staging อย่างน้อย:
    header Oh My Etch 1 แบบ, footer 1 แบบ, `main-cta`, `main-single-post`, `main-cta-form`
  - ถามว่าจะลบสคริปต์ Python ที่สร้าง kit ใน `_build/` หรือเก็บไว้
  - **ห้ามลบเอง**

## สิ่งที่ต้องระวังเพิ่ม

- `_build/src/footer-copy.json` ไม่มีสคริปต์ kit ไหนใช้ จึงไม่ต้อง copy ไป `data/` (ตรวจด้วย grep อีกครั้งตอนทำ Task 8)
- check.py เดิมต้องยังผ่านหลังทุก Task:
  - เฟสนี้ไม่แตะ `.etch.txt` ที่ commit ไว้
  - `preview/` และ `builder/kit-data.js` ไม่เปลี่ยน
- ถ้าระหว่างเฟส 0 มีคนแก้ template ใน Python บน `main`:
  - merge `main` เข้ามา
  - แช่แข็ง golden ใหม่จาก commit นั้น (บันทึก hash ใหม่ในแผนนี้)
  - แก้ TS ตาม
  - ห้ามแก้ golden ด้วยมือ

## บันทึกระหว่างทำ (ต่างจากแผน / เพิ่มจากแผน)

- **Task 5:** `golden.test.ts` เทียบไฟล์ที่ serialize แล้ว**ทีละ byte** ด้วยตั้งแต่ Task 5
  เพราะ `toEqual` ไม่สนลำดับ key แต่ Etch วาง style ตามลำดับ key (ทดลองสลับ style สองตัวแล้ว: `toEqual` ผ่าน, byte check ล้ม)
- **Task 7:** เพิ่ม `pyReplace` ใน py-compat
  เพราะ `str.replace` ของ Python แทนทุกตัว ส่วน `String.replace` แทนตัวแรก และตีความ `$` ในข้อความใหม่
- **Task 9:** CSS ระดับบนสุดของ header ทั้งสามสคริปต์ (34 ค่าคงที่)
  - ดึงด้วย `ast` ของ Python (ค่าตามที่ Python คำนวณ) เป็น `headers/*Css.ts` แทนการพิมพ์ใหม่
  - ตรวจแล้วว่าไม่มีค่าคงที่ตัวไหนถูกกำหนดค่าซ้ำ และทุกค่าตรงกับ Python 34/34
- **Task 10:** audit เทียบกับ `_build/audit.py` ด้วยวิธีนี้:
  - `make_audit_fixtures.py` สร้างไฟล์ที่ผิดทุกกติกา แล้วรัน `audit.py` ตัวจริงเก็บ output ไว้
  - TS ต้องพิมพ์ออกมาเหมือนกันทุกบรรทัด
- **Task 10:** สคริปต์ตรวจ SAME อยู่ที่ `packages/kit/scripts/same-as-head.sh`
  - คืนไฟล์ที่ต่างกันแค่ timestamp ให้เอง และ exit 1 ถ้ามี DIFF
  - CI job `kit-ts` ใช้สคริปต์เดียวกัน
- **ยังไม่ทำ (รอผู้ใช้ตอบ Step 5):**
  - ให้ `build_all.py` เรียก `pnpm build:kit` แทนสคริปต์ Python
  - ลบสคริปต์ Python ของ kit ใน `_build/`
