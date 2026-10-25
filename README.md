# Etch Template Kit (main-*)

ชุด template สำหรับ Etch + ACSS ที่ใช้ร่วมกันได้ทุกโปรเจค — ทุกไฟล์ใช้สีชุดเดียวกัน ชื่อคลาสชุดเดียวกัน และวางรวมในเว็บเดียวได้โดยไม่ชนกัน

วิธีวางเหมือนกันทุกไฟล์: เปิดไฟล์ `.etch.txt` → Select All → Copy → ใน Etch คลิกขวาตำแหน่งที่จะวาง → **Paste**

| โฟลเดอร์ | ไฟล์ |
|---|---|
| [etch-header](etch-header/README.md) | `site-header-ohmyetch` (แนะนำ, ต้องมีปลั๊กอิน Oh My Etch) · `site-header` (Menu Builder) |
| [etch-footer](etch-footer/README.md) | `main-footer` (component + ปุ่ม LINE/โทรลอย) |
| [etch-sections](etch-sections/README.md) | hero · page-hero · features · split · stats · steps · reviews · faq · cta · contact · blog · single-post · 404 |
| [builder](#page-builder-ประกอบหน้าก่อนไปทำใน-etch) | **Page Builder** — ลากวาง section ประกอบหน้า ดูผลก่อนไปทำใน Etch (เปิด `builder/index.html`) |
| `preview` | หน้า preview ของแต่ละ template (สร้างอัตโนมัติจาก `.etch.txt`) |
| [เว็บจริง](#เอา-page-builder-ขึ้นเว็บ-cloudflare-workers) | วิธีเอา builder ขึ้น Cloudflare Workers + ล็อกอินด้วย Cloudflare Access |
| `_build` | ไฟล์สร้าง template (Python) — ไม่ต้องใช้ตอนวาง ใช้ตอนแก้ template แล้วสร้างไฟล์ใหม่ |

## Page Builder (ประกอบหน้าก่อนไปทำใน Etch)

เปิดไฟล์ **`builder/index.html`** ด้วย Chrome / Edge / Safari / Firefox ได้เลย (ดับเบิลคลิก ไม่ต้องมี server หรือติดตั้งอะไร)

- **แถบซ้าย** — รายการ template แยกกลุ่ม Header / Sections / Footer พร้อมรูปย่อ → ลากการ์ดไปวางในหน้า หรือกด **+** เพื่อต่อท้าย (header / footer จะแทนตัวเดิม)
- **กลางจอ** — หน้าที่ประกอบไว้ ชี้ที่ section แล้วใช้แถบเครื่องมือด้านซ้าย: **⠿** ลากสลับลำดับ, **↑ ↓** เลื่อน, **✕** ลบ — header อยู่บนสุดและ footer อยู่ล่างสุดเสมอ
- **เลิกทำ** — กด "เลิกทำ" ในแถบแจ้งเตือน หรือ Ctrl+Z (⌘Z) ใช้ได้กับการเพิ่ม/ลบ/สลับ section, เปลี่ยนสี และลบหน้า
- **แถบบน** — สลับจอ Desktop (1440) / Tablet (768) / Mobile (375) และสลับ **1rem = 10px / 16px** (ขนาดต้องเท่าเดิม ถ้าเปลี่ยนแปลว่ามี rem ดิบหลุดมา)
- **แผงขวา** — แก้ 5 สี `--main-*` ด้วย color picker เห็นผลทันที (↺ ตาม ACSS = กลับไปใช้ค่าเริ่มต้น) และจำลองสี Primary / Secondary ของ ACSS (ปุ่ม `btn--*` ใช้สีนี้)
- **อ่านง่ายไหม** — ตรวจ contrast ของสีที่ใช้คู่กัน (ตัวอักษรบนพื้น, บนสีหลัก, หัวข้อ/ลิงก์, ไอคอนบนสีเน้น) ขึ้นสีแดงถ้าต่ำกว่าเกณฑ์ WCAG และเตือนซ้ำในหน้า Export
- **ดูทั้งหน้า ↗** — เปิดหน้าที่ประกอบไว้เป็นหน้าเดียวในแท็บใหม่ (`preview/page.html`) พร้อมสีและขนาด root ที่เลือก เห็น sticky header และปุ่มลอยของ footer ตามจริง ใช้เปิดให้ลูกค้าดูได้
- **หลายหน้า** — ตั้งชื่อหน้าได้ (เช่น "หน้าแรก ลูกค้า A"), สร้างใหม่ / ทำสำเนา / ลบ (กดปุ่มลบ 2 ครั้งเพื่อยืนยัน) — บันทึกอัตโนมัติในเบราว์เซอร์ (localStorage) · **Export JSON** / **Import JSON** เพื่อเก็บไฟล์หรือส่งต่อ (ข้อมูลที่เสียหรือ template ที่ไม่มีแล้วจะถูกข้ามไป ไม่ทำให้ builder เปิดไม่ขึ้น)
- **Export สำหรับ Etch** — แสดงค่าสี 5 บรรทัดสำหรับวางใน `:where(:root)` และลำดับไฟล์ `.etch.txt` ที่ต้องวาง พร้อมปุ่ม **Copy** เนื้อหาทีละไฟล์ → ใน Etch คลิกขวา → Paste ตามลำดับ (ตั้งใจให้วางทีละ section: ยังไม่ได้ยืนยันว่า Etch รับไฟล์ที่รวมหลาย section เป็นก้อนเดียวได้)

**ข้อจำกัด** — ภาพใน builder จำลอง ACSS แบบใกล้เคียง (สี, สเกลตัวอักษร/ระยะ, ปุ่ม `btn--*`, padding ของ section ใน `_build/acss_sim.py`) ไม่ใช่ค่าจริงของแต่ละเว็บ · รูปเป็น placeholder · ข้อมูล dynamic (ชื่อหน้า, โพสต์, related) เป็นข้อมูลตัวอย่าง · ในหน้า builder แต่ละ section อยู่ใน iframe ของตัวเอง จึงไม่เห็น sticky header และปุ่มลอยของ footer จะอยู่มุมของกรอบ footer (ดูแบบจริงได้ที่ **ดูทั้งหน้า**) · เมนูของ Oh My Etch / Menu Builder ใช้ script จำลองใน preview (เปิด dropdown / drawer ได้พอดูหน้าตา) · แผนที่ Google ต้องต่อเน็ต — ตรวจหน้าจริงใน Etch อีกครั้งก่อนส่งงาน

## เอา Page Builder ขึ้นเว็บ (Cloudflare Workers)

เว็บเป็นไฟล์ static ล้วน ใช้ **Cloudflare Workers (static assets)** โฮสต์ (แผนฟรีพอ ใช้กับ repo private ได้) และ **Cloudflare Access** ล็อกอินกันคนนอก — สำคัญ เพราะใน builder มีเนื้อหา `.etch.txt` ทุกไฟล์ ใครเปิดเว็บได้ก็ copy template ไปได้

- `wrangler.jsonc` บอก Cloudflare ว่า Worker ชื่อ `template-etch` เสิร์ฟไฟล์จาก `dist/` และให้รัน `python3 _build/build_site.py` ก่อน deploy ทุกครั้ง (`"name"` ต้องตรงกับชื่อ Worker ใน dashboard)
- `build_site.py` รวมเฉพาะไฟล์ที่ต้องขึ้นเว็บไว้ใน `dist/` (`builder/`, `preview/`, หน้าแรกที่พาไป builder, `_headers`, `robots.txt`) — `_build/`, README, ไฟล์ `.etch.txt` และ `preview/kit.json` ไม่ขึ้นเว็บ (แต่เนื้อหา `.etch.txt` อยู่ในปุ่ม Copy ของ builder)
- ลองในเครื่องแบบเดียวกับบน Cloudflare: `npx wrangler dev` แล้วเปิด `http://localhost:8787`

### ตั้งค่าครั้งแรก (Cloudflare dashboard — ชื่อเมนูอาจต่างเล็กน้อยตามเวอร์ชัน)

1. **เชื่อม repo** — Workers & Pages → Create → **Import a repository** (Connect to Git) → เลือก `Template-ETCH` → ตั้งชื่อ Worker `template-etch`
2. **ตั้งค่า build** — Worker → Settings → **Build**
   - Build command: ว่างไว้ (`wrangler.jsonc` สั่ง build เอง)
   - Deploy command: `npx wrangler deploy`
   - Production branch: `main`
   - push / merge เข้า `main` แล้วดูใน Deployments ว่า build ผ่าน (log ต้องมีบรรทัด `ok site: … dist`)
3. **ล็อกอินก่อนเข้า (Cloudflare Access)** — ทำก่อนเปิดลิงก์ให้ใครดู
   - Worker → Settings → **Domains & Routes** → แถว `workers.dev` → เปิด **Cloudflare Access** (Cloudflare สร้าง Access application ให้)
   - Zero Trust → Access → Applications → เปิด application ที่เพิ่งสร้าง → Policies: ให้เหลือ Action **Allow** · Include **Emails** = อีเมลของคุณ (ลบ rule ที่กว้างกว่านี้ เช่น Everyone)
   - Login methods: **One-time PIN** (ส่งรหัสเข้าอีเมล ไม่ต้องตั้งรหัสผ่าน)
4. **ลิงก์ preview ของ branch** — `wrangler.jsonc` ตั้ง `"preview_urls": false` ไว้แล้ว ตรวจใน Domains & Routes ว่า Preview URLs เป็น Disabled
5. **ตรวจ** — เปิด `https://template-etch.<บัญชีของคุณ>.workers.dev` ในหน้าต่างไม่ระบุตัวตน (Incognito) ต้องเจอหน้าล็อกอินของ Cloudflare ก่อน ล็อกอินแล้วต้องเห็น Page Builder

### หลังจากนั้น

- merge เข้า `main` → Cloudflare build + deploy ให้เองภายในไม่กี่นาที
- เว็บใช้ไฟล์ preview ที่ commit ไว้ ถ้าแก้ template ต้อง build + commit ก่อน (CI จะเตือนถ้าลืม — ดูด้านล่าง)
- `_build/site/_headers` กำหนด security headers ของเว็บ (CSP, ห้ามเว็บอื่นฝัง, `noindex`) ถ้าเพิ่มของที่โหลดจากเว็บอื่น ต้องเพิ่มโดเมนใน CSP ด้วย
- อยากใช้โดเมนของตัวเอง: Worker → Settings → Domains & Routes → Add → Custom domain แล้วเพิ่มโดเมนนั้นใน Access application ด้วย

### ตรวจอัตโนมัติ (GitHub Actions)

ทุก PR และทุก push เข้า `main` รัน `python3 _build/check.py` (`.github/workflows/check.yml`): build template ใหม่ + audit, ตรวจว่า `.etch.txt` ตรงกับที่ commit (ไม่นับ timestamp), ตรวจว่าไฟล์ preview / builder ทันสมัย และลองรวมเว็บด้วย `build_site.py` — รันเองในเครื่องได้ด้วยคำสั่งเดียวกันก่อน commit

## เริ่มเว็บใหม่ (ลำดับที่แนะนำ)

1. ตั้ง ACSS ให้เรียบร้อย (สี Primary / Secondary, ฟอนต์)
2. Template **Header** → วาง header · Template **Footer/ทุก template** → วาง `main-footer`
3. แก้ props ของ **Main Footer** (ที่อยู่ เบอร์ LINE social) — ชื่อเว็บดึงจาก Site Title เอง
4. หน้าแรก: `main-hero` → `main-features` → `main-split` → `main-stats` → `main-steps` → `main-reviews` → `main-faq` → `main-cta`
5. หน้าอื่น: `main-page-hero` ด้านบน + section ตามต้องการ · หน้า Contact: `main-contact`
6. Template Single → `main-single-post` · Posts page/Archive → `main-blog` · Template 404 → `main-404`

## สี

ทุก template อ่านสีจาก custom style **`:where(:root)`** อันเดียว (ถูกสร้างตอนวางไฟล์แรก) เปิดได้ที่ Etch → Styles → ค้นหา `:where(:root)`

```css
--main-primary: var(--primary);    /* แบรนด์: header, footer, FAQ, หัวข้อ, ลิงก์, ป้ายหมวดหมู่ */
--main-accent: var(--secondary);   /* เน้น: เส้นใต้, hover, เส้นหน้า eyebrow, FAQ ที่เปิดอยู่ */
--main-light: var(--white);        /* พื้นอ่อน: section, การ์ด, กล่องบทความ */
--main-text: var(--text-dark);     /* ตัวอักษรบนพื้นอ่อน */
--main-on-primary: var(--white);   /* ตัวอักษร/ไอคอนบนพื้นสี primary */
```

- **ค่าเริ่มต้นตาม ACSS** → เปลี่ยน Primary / Secondary ใน ACSS แล้ว template เปลี่ยนตามทั้งหมด (รวมปุ่ม `btn--*`)
- อยากให้ template ต่างจาก ACSS → แก้ 5 บรรทัดนี้ (ใส่ค่าสีตรงๆ ได้ เช่น `#0e7c66`) สีอ่อน/เส้น/เงา คำนวณจาก 5 สีนี้เอง
- ปุ่ม (`btn--primary`, `btn--secondary`) ยังใช้สีจาก ACSS
- ถ้าเปิด Etch Settings → **Overwrite on Paste** การวางไฟล์ใหม่จะเขียนทับสีที่แก้ไว้ — ปิดไว้หรือแก้สีหลังวางครบ

## ขนาด (ใช้ได้ทั้งเว็บที่ 1rem = 10px และ 16px)

ขนาดใน CSS เขียนเป็น `to-rem(Npx)` ซึ่ง Etch แปลงตาม root font size ของแต่ละเว็บ (เช่น `to-rem(400px)` = 40rem ที่ 62.5% และ 25rem ที่ 100%) จึงได้ขนาดเท่ากันทุกเว็บ — ตอนแก้ CSS เองให้ใช้แบบเดียวกัน

## กติกาที่ทำให้ใช้ร่วมกันได้

- ชื่อคลาสขึ้นต้น `main-` (header Menu Builder ใช้ `site-header-`) → ไม่ชนกับ style เดิมของเว็บปลายทาง
- Etch เก็บ style เดียวต่อ selector: วางซ้ำจะใช้ของเดิม ไม่สร้างซ้ำ — ชิ้นที่ใช้ร่วมกันมี CSS เหมือนกันทุกไฟล์
- Component (`MainFooter`, `MainCta`, `MainContact`) และ loop (`mainRelatedPosts`) ถ้ามีอยู่แล้วจะใช้ของเดิม
- ปุ่ม ACSS ไม่มี style record ของตัวเอง จึงไม่หายตอนวาง
- ไอคอนเป็น SVG สีเดียวฝังในไฟล์ เปลี่ยนสีตามธีม ไม่ต้องอัปโหลดรูป
- ข้อความตัวอย่างเป็นภาษาอังกฤษ

## ต้องมีที่เว็บปลายทาง

Etch 1.6+ และ ACSS 3 · header แบบ Oh My Etch ต้องติดตั้งปลั๊กอิน Oh My Etch

## แก้ template แล้วสร้างไฟล์ใหม่ (`_build`)

```bash
python3 _build/build_all.py
```

สร้างไฟล์ `.etch.txt` ทุกตัวใหม่ แล้วตรวจอัตโนมัติ (`_build/audit.py`) ว่า selector ที่ซ้ำกันมี CSS ตรงกัน, ไม่มีสีฝังตายตัว, ไม่มีหน่วย rem ดิบ และคลาสไม่หายตอนวาง — สีกลาง/ชิ้นที่ใช้ร่วมกันอยู่ใน `_build/kit.py`, ไอคอนใน `_build/icons.py`
(ทุกครั้งที่ build ค่า `"timestamp"` ในไฟล์ `.etch.txt` จะเปลี่ยนตามเวลาที่สร้าง ส่วนอื่นเหมือนเดิมถ้าไม่ได้แก้ template)

**ข้อมูลลูกค้า** — ไฟล์ใน `_build/src` เป็นโครงสร้างต้นแบบที่แทนข้อความด้วยข้อมูลตัวอย่างแล้ว ห้ามใส่ข้อมูลจริงของลูกค้า (ชื่อ เบอร์ ที่อยู่) ลงใน repo · audit จะเตือนถ้าเจอลิงก์ `wp-content/uploads` หรือเบอร์โทรที่ไม่ใช่เบอร์ตัวอย่าง และถ้าสร้างไฟล์ `_build/private-terms.txt` (ชื่อลูกค้าบรรทัดละชื่อ ไฟล์นี้ไม่ถูก commit) จะเตือนเมื่อเจอชื่อเหล่านั้นด้วย

ขั้นสุดท้ายของ `build_all.py` คือ `build_preview.py` ซึ่งสร้าง preview + ข้อมูลของ Page Builder ใหม่ให้อัตโนมัติ ถ้าแก้แค่ไฟล์ preview / builder หรืออยากสร้าง preview อย่างเดียว:

```bash
python3 _build/build_preview.py
```

- อ่านไฟล์ `.etch.txt` ที่ build แล้ว (ตัวเดียวกับที่ copy ไปวางใน Etch) แล้ว render เป็น HTML — **ไม่เขียนทับ `.etch.txt`**
- ได้ `preview/<id>.html` ทีละ template, `preview/page.html` (ทุก template ในหน้าเดียว เลือกลำดับด้วย `?t=header,hero,footer`), `preview/index.html` (รายการ preview), `preview/kit.json`, `preview/assets/` (ACSS จำลอง + `frame.js`) และ `builder/kit-data.js` (รายการ template + เนื้อหาไฟล์สำหรับปุ่ม Copy)
- เพิ่ม template ใหม่: ใส่ใน `CATALOG` ของ `_build/build_preview.py` (id, กลุ่ม header/section/footer, ชื่อ, ไฟล์, คำอธิบาย) แล้ว build ใหม่ — builder จะเห็นเอง
- ไฟล์ที่เกี่ยวข้อง: `_build/render_preview.py` (แปลง payload ของ Etch เป็น HTML: component/props/slot, condition, loop, รูป placeholder, `to-rem()`), `_build/acss_sim.py` (ACSS จำลอง), `_build/preview_assets/frame.js` (รับสี/ขนาด root จาก builder และส่งความสูงกลับ)
- หน้าที่เขียนเอง (`builder/index.html`, `builder.css`, `builder.js`) ไม่ต้อง build
# Template-ETCH
