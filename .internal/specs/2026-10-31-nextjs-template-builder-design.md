# Spec: Next.js template builder (ต่อจาก template kit ของ Etch + ACSS)

> สถานะ: **ร่าง — รออนุมัติ** · ร่างจาก prompt 4 เฟสของผู้ใช้ และสภาพ repo ที่ `main` @ `3db436d` (2026-11-04)
> ไฟล์นี้เป็นตัวอ้างอิงของทุกเฟส ถ้าเฟสไหนต้องทำต่างจากนี้ ให้แก้ spec ก่อนแล้วค่อยแก้โค้ด

## 1. เป้าหมาย

ลูกค้าแต่ละเจ้า (organization) ประกอบหน้าเว็บเองจาก section ใน template kit ได้แก่ เลือกแบบ เรียงลำดับ แก้ข้อความ สี และรูป
แล้ว export เป็นโค้ด Etch เพื่อ Paste ลง WordPress (Etch + ACSS) โดยหน้าตาตรงกับ template ที่ทีมดูแลอยู่

ไม่อยู่ใน spec นี้ (ต้องออกแบบใหม่ก่อน): ส่งตรงเข้า WordPress ผ่าน REST API · ย้ายรูปเข้า WP Media อัตโนมัติ · ให้ลูกค้าสมัครเอง

## 2. สภาพปัจจุบัน (ของที่ต้องรักษาไว้)

| ส่วน | อยู่ที่ | หมายเหตุ |
|---|---|---|
| Template kit | `etch-header/` (7) · `etch-footer/` (5) · `etch-sections/` (46) = **58 ไฟล์ `.etch.txt`** | สร้างจาก Python ใน `_build/` (`build_all.py` รัน 11 สคริปต์ตามลำดับ แล้วรัน `audit.py`) |
| ข้อมูลต้นทาง | `_build/src/*.json` | copy จาก Etch / Oh My Etch / Menu Builder (header, footer, CSS ของ library) |
| Audit | `_build/audit.py` | 4 กลุ่มกติกา (ดูข้อ 8.4) — CI รันผ่าน `_build/check.py` |
| Preview + builder เดิม | `preview/`, `builder/` (vanilla JS) · `_build/render_preview.py`, `build_preview.py` | อ่าน `.etch.txt` แล้วสร้าง HTML · ขึ้นเว็บผ่าน Cloudflare Worker (`worker/`, `wrangler.jsonc`) พร้อมรหัสผ่าน |

ค่าที่ห้ามเปลี่ยน เพราะเว็บจริงที่ Paste ไปแล้วอ้างถึง:
- component id/key: `990001 MainFooter`, `990002–990006` footer variants, `990101 MainCta`, `990102 MainContact`,
  Oh My Etch `1843–1849`, Menu Builder `1971–1974`
- loop key `mainRelatedPosts`
- style id และ selector ทุกตัว (Etch เก็บ style หนึ่งตัวต่อหนึ่ง selector และตัวที่ Paste ก่อนจะชนะ)
- ตัวแปรสี `--main-primary`, `--main-accent`, `--main-light`, `--main-text`, `--main-on-primary` (ตัวอื่นคำนวณต่อจาก 5 ตัวนี้)
- ความยาวเขียนเป็น `to-rem(Npx)` เพื่อให้ใช้ได้ทั้ง root font size 62.5% และ 100%

builder เดิมยังใช้งานต่อจนกว่าเฟส 2 จะเสร็จและผู้ใช้สั่งเลิก

## 3. Stack

- **Monorepo:** pnpm workspace · TypeScript strict · Node 22
- **`packages/kit`:** ตัวสร้าง Etch payload, registry ของ section และ audit ใช้ได้ทั้งใน CLI และใน server ของ app (ไม่มี dependency ของ DOM)
- **`apps/web`:** Next.js (App Router) + React
- **DB:** Postgres (Neon) + Drizzle ORM (migration อยู่ใน repo)
- **Auth:** Better Auth: magic link ส่งผ่าน Resend + Google OAuth · เข้าได้เฉพาะคนที่ถูกเชิญ
- **ไฟล์:** Vercel Blob (เฟส 3)
- **Validation:** zod (ฟอร์ม, server action, content ของ section)
- **ลากเรียง:** dnd-kit
- **เทสต์:** Vitest (unit + integration กับ Postgres จริง) · Playwright (e2e)
- **Hosting:** Vercel (app) · kit build ยังรันใน CI

## 4. สถาปัตยกรรม

```
packages/kit/
  src/etch/       ตัวช่วยระดับล่าง (block, el, text, img, svg, cond, loop, prop, style, payload, portable)
                  + py-compat (formatG, pyDumps) ที่ทำให้ผลตรงกับ Python ทีละ byte
  src/kit/        ของที่ใช้ร่วมกัน: COLORS, BASE, icons, heading, social, card, media, buttons, checks, kitPayload
  src/sections/   ตัวสร้างของแต่ละไฟล์ (แปลงจาก build_*.py) — เฟส 2 ห่อด้วย defineSection()
  src/headers/ src/footers/
  src/audit.ts    กติกาเดียวกับ _build/audit.py
  src/catalog.ts  รายการ template ทั้งหมด: id, กลุ่ม, ชื่อ, ไฟล์ปลายทาง, ฟังก์ชัน build
  src/cli/build.ts  pnpm build:kit → เขียน 58 ไฟล์ + audit
  tests/golden/   .etch.txt ที่แช่แข็งไว้ (ห้ามแก้เพื่อให้เทสต์ผ่าน)
apps/web/         (เฟส 1+) Next.js
```

กติกา: `apps/web` เรียก kit ผ่าน API ของ package เท่านั้น และทุกโค้ดที่สร้าง JSON ของ Etch ต้องอยู่ใน `packages/kit`

## 5. Section registry (เฟส 2)

```ts
defineSection({
  key: "features",                 // ชนิด: hero, features, split, stats, steps, reviews, faq, cta, …
  label: "Features",
  variants: ["features", "features-image", …],   // id เดียวกับ catalog (= id ใน builder เดิม)
  schemaVersion: 1,
  schema: z.object({ … }),         // content ที่ลูกค้าแก้ได้: ข้อความ, ลิงก์, รูป, จำนวนรายการ
  defaults: { … },                 // ค่าที่ทำให้ toEtch() ได้ผล = golden ของเฟส 0
  migrate: (old, fromVersion) => …,
  styles,                          // style records ที่ section นี้ใช้
  Preview,                         // React component สำหรับ iframe preview
  toEtch: (content, variant) => EtchPayload,
})
```

- `toEtch(defaults)` ต้อง deep-equal กับ golden ของเฟส 0 ทุก variant (เทสต์ golden ยังต้องผ่านตลอด)
- section dynamic (blog, single-post, related posts, 404) แก้ได้แค่ข้อความรอบๆ ส่วน preview ใช้โพสต์ตัวอย่าง

## 6. ข้อมูล

| ตาราง | คอลัมน์หลัก | เฟส |
|---|---|---|
| organizations | id, name, slug, created_at | 1 |
| users | id, email (unique), name, created_at (Better Auth) | 1 |
| memberships | user_id, org_id, role (`owner` \| `editor`) · unique(user_id, org_id) | 1 |
| invitations | id, org_id, email, role, token_hash, expires_at (7 วัน), used_at, invited_by | 1 |
| projects | id, org_id, name, colors (jsonb 5 สี), root_font_size (`100` \| `62.5`), header_variant, footer_content (jsonb), is_template, deleted_at | 1 |
| audit_log | id, org_id, user_id, action, target, meta (jsonb), created_at | 1 |
| pages | id, project_id, name, slug, position, deleted_at | 2 |
| page_sections | id, page_id, section_key, variant, position, content (jsonb), schema_version | 2 |
| assets | id, project_id, blob_url, blob_path, mime, bytes, width, height, exported_at, deleted_at | 3 |
| page_versions | id, page_id, created_by, created_at, payload (jsonb) | 3 |

ทุกตารางที่เป็นของลูกค้าผูกกับ `org_id` (ตรงหรือผ่าน project) และทุก query กรองด้วย org ที่ได้จาก `requireMember`

## 7. Builder (เฟส 2) และ Export (เฟส 3)

- **Builder** `/projects/[id]/pages/[pageId]`
  - ซ้าย: คลัง section และลำดับในหน้า ลากเรียงด้วย dnd-kit
  - กลาง: preview ใน iframe
  - ขวา: ฟอร์มแก้ค่าที่สร้างจาก zod schema และตัวเลือก variant
- **ระดับโปรเจกต์:** สี 5 สี · root font size · header variant · เนื้อหา footer
- **Preview:**
  - ใช้ CSS ของ kit โดยแปลง `to-rem(Npx)` ตาม root font size และใส่สีของโปรเจกต์ใน `:root`
  - ปุ่ม ACSS ใช้ CSS เลียนแบบขั้นต่ำ (เหมือน `_build/acss_sim.py`) พร้อมป้ายบอกว่าหน้าตาอาจต่างจากเว็บจริงเล็กน้อย
- **บันทึก:**
  - บันทึกอัตโนมัติ (debounce ~800ms) และ server validate ด้วย zod ทุกครั้ง
  - ถ้าบันทึกล้มเหลว: แสดง "ยังไม่บันทึก" พร้อมปุ่ม retry และเตือนก่อนปิดแท็บ
- **Clone:** owner clone โปรเจกต์ต้นแบบ (`is_template`) เข้า org ของลูกค้าได้
- **Export** ทำทีละหน้าที่ฝั่ง server (`/api/export/[pageId]`):
  1. Copy หน้า: รวม section ทั้งหน้าเป็น payload เดียว พร้อม style `:where(:root)` ที่ใส่สีของโปรเจกต์
  2. Copy Header / Copy Footer แยกปุ่มกัน
  3. ดาวน์โหลดรูปของหน้านั้นเป็น .zip
  4. ดาวน์โหลด `.etch.txt` สำรอง เมื่อ clipboard ใช้ไม่ได้หรือ payload ใหญ่เกินไป
- **หลังส่ง payload:**
  - payload ต้องผ่าน `audit()` ก่อนส่งทุกครั้ง
  - ทุกครั้งที่ export บันทึก `page_versions` และตั้ง `assets.exported_at`
  - UI เตือนว่า "Overwrite on Paste" ของ Etch จะเขียนทับสีที่แก้ไว้ใน WordPress

## 8. ความปลอดภัย

1. **Auth:**
   - ไม่มีหน้าสมัครเอง ลิงก์เชิญใช้ได้ครั้งเดียว หมดอายุ 7 วัน และเก็บแค่ hash
   - magic link หมดอายุ 15 นาที
   - มี rate limit ที่ login และ invite
2. **สิทธิ์:**
   - ทุก route, server action และ API เช็กฝั่ง server ผ่าน `requireMember(orgId, role)`
   - ห้ามเชื่อ `org_id` จาก browser ให้หา org จาก resource ที่ขอ
   - middleware ใช้แค่ redirect ไม่ได้ใช้คุมสิทธิ์
3. **Session:** cookie เป็น httpOnly, secure และ sameSite=lax · secret อยู่ใน env เท่านั้น (มี `.env.example`)
4. **Content:**
   - ข้อความของลูกค้าเป็น plain text และต้อง escape ทั้งใน preview และใน Etch JSON
   - ลิงก์อนุญาตเฉพาะ `http(s):`, `mailto:`, `tel:`, `/…` และ `#…`
5. **Audit ของ kit:** ทุก payload ที่ export ต้องผ่าน 4 กลุ่มกติกาของ `_build/audit.py`
   1. selector เดียวกันต้องมี CSS เดียวกัน และ component/loop key เดียวกันต้องมีเนื้อหาเดียวกันทุกไฟล์
   2. ทุกไฟล์มี `main-colors` · style ที่เป็นของ kit ห้ามมีสี hard-code, rem ดิบ หรือสี ACSS
   3. style id ที่ block ใช้ต้องมีอยู่จริง และ class บน element ที่มี styles ต้องมี record `.class`
      (ไม่เช่นนั้นจะหายตอน Paste)
   4. ห้ามมีของค้างจากเว็บต้นทาง: uploads, เบอร์จริง และชื่อลูกค้าใน `_build/private-terms.txt`

   ห้ามลดกติกาเหล่านี้
6. **ไฟล์:**
   - รับเฉพาะ jpg/png/webp/avif ไม่เกิน 10MB และตรวจ magic bytes ฝั่ง server ไม่รับ SVG
   - path บน Blob ต้องสุ่มจนเดาไม่ได้
   - รูปที่ `exported_at` ไม่ว่างห้ามลบจาก Blob (ลบได้แค่แบบ soft delete)
7. **บันทึกเหตุการณ์:** `audit_log` บันทึกเมื่อ invite, login และสร้าง/แก้/ลบ

## 9. Error handling

- **content ไม่ตรง schema:**
  - รัน `migrate` ก่อน
  - ถ้ายังไม่ผ่าน ให้ใช้ default ของช่องนั้นพร้อมคำเตือนในฟอร์ม หน้าต้องไม่พัง
- **บันทึก / export ล้มเหลว:** บอกเหตุผล และให้ลองใหม่ได้ ห้ามเงียบ
- **audit ไม่ผ่านตอน export:** ไม่ส่ง payload และแสดงรายการ error (เป็น bug ของ kit ต้องมีเทสต์ครอบ)
- **ลิงก์เชิญหมดอายุหรือใช้แล้ว:** แสดงหน้าบอกให้ติดต่อ admin

## 10. เทสต์

- **เฟส 0:**
  - golden: ผลจาก TS deep-equal กับ `.etch.txt` 58 ไฟล์ ไม่นับ `timestamp`
  - byte check: `pnpm build:kit` แล้วไฟล์เปลี่ยนแค่ timestamp
  - unit ของ py-compat และ audit (ทุกกติกาต้องมีเคสที่ล้ม)
- **เฟส 1:**
  - integration กับ DB จริง: ผู้ใช้ org A อ่าน/แก้ของ org B ไม่ได้ทุก endpoint
  - Playwright: เชิญ → ล็อกอิน → เห็นเฉพาะโปรเจกต์ของ org ตัวเอง
- **เฟส 2:**
  - schema, migrate และ escape (`<script>`, `javascript:` ต้องไม่หลุดเข้า preview หรือ JSON)
  - golden ยังผ่าน
  - Playwright: flow ประกอบหน้า
- **เฟส 3:**
  - upload: ชนิด, ขนาด, magic bytes และการปฏิเสธ SVG
  - แยกข้อมูล org สำหรับ export และ zip
  - Playwright: อัปรูป → Copy
  - ผู้ใช้ทดสอบ Paste ลง Etch บน staging เอง

## 11. ลำดับเฟส

| เฟส | งาน | branch | ต้องเสร็จก่อน |
|---|---|---|---|
| 0 | ย้าย kit จาก Python เป็น TypeScript (`packages/kit`) | `phase0-kit-ts` | — |
| 1 | Next.js + ล็อกอินแบบเชิญ + org/ลูกค้า + admin | `phase1-auth` | 0 |
| 2 | Builder | `phase2-builder` | 1 |
| 3 | รูป + Export + version | `phase3-export` | 2 |

ทุกเฟสต้องมีแผนใน `.internal/plans/` และผู้ใช้อนุมัติก่อนเขียนโค้ด · ทำแบบ TDD และ commit ทีละ task · ห้าม commit ลง `main`

## 12. ความเสี่ยงที่รับรู้แล้ว

- **การย้ายภาษาอาจเพี้ยนทีละ byte:** เช่น format ตัวเลข `:g`, separator ของ `json.dumps`, ลำดับ key และ base64 ของ script
  - กันด้วย golden และ byte check
  - `_build/` ยังเก็บไว้จนผู้ใช้ Paste ทดสอบบน staging แล้ว
- **kit มีสองที่ระหว่างเฟส 0–2:** Python preview/builder เดิมยังอ่าน `.etch.txt` ที่ TS เขียน จึงยังใช้ได้
  - ถ้าแก้ template ระหว่างนี้ ต้องแก้ฝั่ง TS เท่านั้น เมื่อเฟส 0 จบ
- **Preview ไม่ใช่ ACSS จริง:** ปุ่มและ spacing อาจต่างเล็กน้อย จึงต้องมีป้ายบอกใน UI และผู้ใช้ต้องตรวจบน staging
- **"Overwrite on Paste" ของ Etch:** จะเขียนทับสีหรือ style ที่ลูกค้าแก้ใน WordPress จึงต้องเตือนทุกครั้งที่ export
- **รูปบน Blob:** เว็บจริงโหลดรูปจาก URL ของ Blob ถ้าลบรูปเว็บจะพัง จึงลบได้แค่แบบ soft delete
- **ค่าใช้จ่าย:** Neon, Vercel, Blob และ Resend มีโควต้าฟรีจำกัด ต้องประเมินก่อนเปิดให้ลูกค้าหลายเจ้า
