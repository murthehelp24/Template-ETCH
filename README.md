# Etch Template Kit (main-*)

ชุด template สำหรับ Etch + ACSS ที่ใช้ร่วมกันได้ทุกโปรเจค — ทุกไฟล์ใช้สีชุดเดียวกัน ชื่อคลาสชุดเดียวกัน และวางรวมในเว็บเดียวได้โดยไม่ชนกัน

วิธีวางเหมือนกันทุกไฟล์: เปิดไฟล์ `.etch.txt` → Select All → Copy → ใน Etch คลิกขวาตำแหน่งที่จะวาง → **Paste**

| โฟลเดอร์ | ไฟล์ |
|---|---|
| [etch-header](etch-header/README.md) | `site-header-ohmyetch` (แนะนำ, ต้องมีปลั๊กอิน Oh My Etch) + 5 แบบ: พื้นสว่าง · โลโก้กลาง · แถบข้อมูล · ลอยมุมโค้ง · เมนูชิดขวา · `site-header` (Menu Builder — มีในชุด แต่ไม่อยู่ใน builder) |
| [etch-footer](etch-footer/README.md) | `main-footer` (component + ปุ่ม LINE/โทรลอย) |
| [etch-sections](etch-sections/README.md) | hero (+ 4 แบบ: ภาพเต็มจอ · ภาพ + สีไล่ · รูปซ้อน · พื้นสีหลัก) · page-hero · features · split · stats · steps · reviews · faq · cta · contact · blog · single-post · 404 |
| [builder](#page-builder-ประกอบหน้าก่อนไปทำใน-etch) | **Page Builder** — ลากวาง section ประกอบหน้า ดูผลก่อนไปทำใน Etch (เปิด `builder/index.html`) |
| `preview` | หน้า preview ของแต่ละ template (สร้างอัตโนมัติจาก `.etch.txt`) |
| [เว็บจริง](#เอา-page-builder-ขึ้นเว็บ-cloudflare-workers) | วิธีเอา builder ขึ้น Cloudflare Workers + ตั้งรหัสผ่าน |
| `_build` | ไฟล์สร้าง template (Python) — ไม่ต้องใช้ตอนวาง ใช้ตอนแก้ template แล้วสร้างไฟล์ใหม่ |

## Page Builder (ประกอบหน้าก่อนไปทำใน Etch)

เปิดไฟล์ **`builder/index.html`** ด้วย Chrome / Edge / Safari / Firefox ได้เลย (ดับเบิลคลิก ไม่ต้องมี server หรือติดตั้งอะไร)

- **แถบซ้าย** — แท็บ **Header / Sections / Footer** แสดงทีละประเภทพร้อมรูปย่อ · คลิก header / section / footer ในหน้า (หรือช่องว่างของ header / footer) แถบซ้ายจะสลับไปประเภทนั้นเอง
  - ลากการ์ดไปวางในหน้า หรือกด **+**: header / footer = ใช้แทนตัวเดิม · section = แทรกต่อจาก section ที่คลิกเลือกไว้ (ไม่ได้เลือก = ต่อท้ายหน้า)
- **กลางจอ** — หน้าที่ประกอบไว้ ชี้ที่ section แล้วใช้แถบเครื่องมือด้านซ้าย: **⠿** ลากสลับลำดับ, **↑ ↓** เลื่อน, **✕** ลบ — header อยู่บนสุดและ footer อยู่ล่างสุดเสมอ
- **แก้ข้อความ / ใส่รูป** — เปิด **✎ แก้เนื้อหา** (เปิดไว้เป็นค่าเริ่มต้น) แล้วคลิกข้อความในหน้าเพื่อพิมพ์ทับ (Enter = บันทึก, Shift+Enter = ขึ้นบรรทัดใหม่, Esc = ยกเลิก) หรือคลิกช่องรูปเพื่อเลือกรูปจากเครื่อง
  - ข้อความที่แก้ **เข้าไปในไฟล์ที่ Copy ไปวางใน Etch** ด้วย: ข้อความทั่วไปแก้ใน block นั้นเลย, ข้อมูลของ CTA / Contact / Footer (ที่อยู่ เบอร์ หัวข้อ ปุ่ม) บันทึกเป็นค่าของ instance นั้น (Etch เก็บแยกต่อหน้า ไม่ไปเปลี่ยนค่า default ของ component)
  - ข้อความที่ดึงจากข้อมูลจริง (ชื่อหน้า, โพสต์, ปี copyright) และเมนูของปลั๊กอิน แก้ใน builder ไม่ได้ ต้องแก้ใน WordPress / Etch
  - ข้อความใน component ที่ไม่ใช่ props (เช่น ลิงก์เมนูใน Footer) — ถ้าเว็บปลายทางมี component นั้นอยู่แล้ว Etch จะใช้ของเดิม หน้า Export จะเตือน
  - **รูป** ใช้ใน preview เท่านั้น (การ Paste นำรูปเข้า Etch ไม่ได้) — ย่อให้กว้างไม่เกิน 1600px เก็บในเบราว์เซอร์ (IndexedDB) หน้า Export มีรายการรูปพร้อมปุ่มดาวน์โหลด และบอกช่องรูปใน Etch ที่ต้องเลือก
  - ปุ่ม **↺** บนแถบเครื่องมือของ section = คืนข้อความและรูปเดิมของ section นั้น
- **เลิกทำ** — กด "เลิกทำ" ในแถบแจ้งเตือน หรือ Ctrl+Z (⌘Z) ใช้ได้กับการเพิ่ม/ลบ/สลับ section, แก้ข้อความ, ใส่รูป, เปลี่ยนสี สร้าง/ทำสำเนา/ลบ/เปลี่ยนชื่อหน้า และเปลี่ยนประเภทหน้า
- **แถบบน** — ซ้าย: หน้าที่เปิดอยู่ / ชื่อหน้า / + หน้าใหม่ · กลาง: สลับจอ Desktop (1440) / Tablet (768) / Mobile (375) และ ✎ แก้เนื้อหา · ขวา: ดูทั้งหน้า / ไฟล์ JSON / Export สำหรับ Etch (template ใช้ `to-rem()` จึงได้ขนาดเท่ากันทั้งเว็บ 1rem = 10px และ 16px ไม่ต้องสลับดู)
- **แผงขวา: มาตรฐานหน้า** — เลือกว่าหน้านี้คือหน้าอะไร (หน้าแรก เกี่ยวกับเรา บริการ ติดต่อเรา บทความ บทความเดี่ยว 404 หน้าทั่วไป) แล้วดูว่าครบตามมาตรฐานหรือยัง
  - รายการ section ที่ควรมีพร้อมเหตุผล: ✓ มีแล้ว · **!** ต้องมีแต่ยังไม่มี · **○** แนะนำ — กด **+ เพิ่ม** แล้ว section ไปอยู่ตำแหน่งที่แนะนำเอง
  - เตือนปัญหาที่พบบ่อย: ไม่มี Header / Footer, H1 ซ้ำหลายตัว หรือไม่มี H1, section แรกไม่ใช่หัวข้อหลัก, Blog / บทความเดี่ยว / 404 อยู่ผิดประเภทหน้า, CTA ไม่อยู่ท้ายหน้า
  - **จัดหน้าตามแบบแนะนำ** — เพิ่มที่ขาดและเรียงลำดับใหม่ในคลิกเดียว (section เดิมเก็บข้อความที่แก้ไว้ · เลิกทำได้) · หน้า Export เตือนซ้ำถ้ายังไม่ครบ
  - **+ หน้าใหม่** เลือกประเภทหน้าได้ และใส่ section ตามแบบแนะนำให้เลย (สีของเว็บติดมาจากหน้าที่เปิดอยู่)
  - แบบแนะนำของแต่ละประเภทอยู่ใน `builder/pages.js` (แก้หรือเพิ่มประเภทได้) — `_build/check.py` ตรวจว่าใช้ชื่อ section ที่มีอยู่จริง
- **แผงขวา: สี**
  - **ชุดสีสำเร็จรูป** — คลิกครั้งเดียวได้ทั้งสี template และสีปุ่ม · แผงแสดง 8 ชุดแนะนำ กด **ดูทั้งหมด** เพื่อเลือกจาก 56 ชุดแบ่งตามประเภทธุรกิจ (สุขภาพ อาหาร ความงาม ธุรกิจ ธรรมชาติ พรีเมียม) พร้อมภาพตัวอย่างหน้าเว็บย่อ
    ชุดสีอยู่ใน `builder/presets.js` (แก้หรือเพิ่มได้ ชุดละ 9 สี) — `_build/check.py` / CI ตรวจว่าทุกชุดผ่านเกณฑ์อ่านง่ายทุกคู่
  - **สีของ template** — 5 สี `--main-*` คลิกช่องสีหรือพิมพ์รหัส `#rrggbb` เห็นผลทันที · ปุ่ม ↺ = กลับไปใช้สีตาม ACSS
  - **สีปุ่ม** — ปุ่มหลัก (`btn--primary`) และปุ่มรอง (`btn--secondary`) ตั้งได้ทั้งสีพื้นและสีตัวอักษร มีตัวอย่างปุ่มให้ดู
    ปุ่มเป็นของ ACSS: สีพื้น = สี Primary / Secondary ของ ACSS — หน้า Export บอกค่าที่ต้องไปตั้งใน ACSS Dashboard
    เปลี่ยนสีพื้นปุ่มแล้ว สีของ template ที่ยังตาม ACSS จะถูกล็อกไว้ที่สีเดิมให้อัตโนมัติ (header/หัวข้อจึงไม่เปลี่ยนตามปุ่ม)
  - **อ่านง่ายไหม** — ตรวจ contrast ตามเกณฑ์ WCAG 8 คู่ (ตัวอักษรบนพื้น, บนสีหลัก, หัวข้อ/ลิงก์, ไอคอนบนสีเน้น, ตัวอักษรบนปุ่ม 2 แบบ, ปุ่มเส้นขอบ, ปุ่มรองบน header) สรุปบรรทัดเดียว กดดูรายละเอียดได้ และเตือนซ้ำในหน้า Export
- **ดูทั้งหน้า ↗** — เปิดหน้าที่ประกอบไว้เป็นหน้าเดียวในแท็บใหม่ (`preview/page.html`) พร้อมสี ขนาด root ข้อความที่แก้และรูป เห็น sticky header และปุ่มลอยของ footer ตามจริง ใช้เปิดให้ลูกค้าดูได้
- **หลายหน้า** — กดปุ่มชื่อหน้าที่มุมซ้ายบนเพื่อเปิดรายการทุกหน้า: แต่ละแถวบอกประเภทหน้า จำนวน section และสถานะตามมาตรฐาน (ครบ / ต้องแก้) · คลิกแถวเพื่อสลับหน้า (ลำดับหน้าไม่สลับไปมา) · "สำเนา" วางสำเนาต่อจากหน้าเดิม · "ลบ" กด 2 ครั้งเพื่อยืนยัน แล้วเปิดหน้าข้างๆ ให้ · แก้ชื่อหน้าในช่องข้างปุ่ม · **ชื่อกับประเภทหน้าเปลี่ยนตามกัน**: พิมพ์ชื่อเป็นประเภทหน้า (เช่น "เกี่ยวกับเรา", "about", "ติดต่อเรา 2") แล้วประเภทหน้าทางขวาเปลี่ยนตาม และเปลี่ยนประเภทหน้าทางขวาแล้วชื่อเปลี่ยนตามถ้าชื่อยังเป็นชื่อประเภทเดิม (ชื่อที่ตั้งเอง เช่น "ลูกค้า A" ไม่ถูกเปลี่ยน) — ทุกอย่างกด Ctrl+Z ย้อนได้ทีละขั้น · บันทึกอัตโนมัติในเบราว์เซอร์ (localStorage) · เมนู **ไฟล์ JSON** → Export / Import เพื่อเก็บไฟล์หรือส่งต่อ (รวมข้อความที่แก้และรูป ไฟล์จึงใหญ่ขึ้นตามจำนวนรูป) (ข้อมูลที่เสียหรือ template ที่ไม่มีแล้วจะถูกข้ามไป ไม่ทำให้ builder เปิดไม่ขึ้น)
- **Export สำหรับ Etch** — แสดงค่าสี 5 บรรทัดสำหรับวางใน `:where(:root)` และลำดับไฟล์ `.etch.txt` ที่ต้องวาง พร้อมปุ่ม **Copy** เนื้อหาทีละไฟล์ → ใน Etch คลิกขวา → Paste ตามลำดับ (ตั้งใจให้วางทีละ section: ยังไม่ได้ยืนยันว่า Etch รับไฟล์ที่รวมหลาย section เป็นก้อนเดียวได้)

**ข้อจำกัด** — ภาพใน builder จำลอง ACSS แบบใกล้เคียง (สี, สเกลตัวอักษร/ระยะ, ปุ่ม `btn--*`, padding ของ section ใน `_build/acss_sim.py`) ไม่ใช่ค่าจริงของแต่ละเว็บ · รูปเป็น placeholder · ข้อมูล dynamic (ชื่อหน้า, โพสต์, related) เป็นข้อมูลตัวอย่าง · ในหน้า builder แต่ละ section อยู่ใน iframe ของตัวเอง จึงไม่เห็น sticky header และปุ่มลอยของ footer จะอยู่มุมของกรอบ footer (ดูแบบจริงได้ที่ **ดูทั้งหน้า**) · เมนูของ Oh My Etch / Menu Builder ใช้ script จำลองใน preview (เปิด dropdown / drawer ได้พอดูหน้าตา) · แผนที่ Google ต้องต่อเน็ต — ตรวจหน้าจริงใน Etch อีกครั้งก่อนส่งงาน

## เอา Page Builder ขึ้นเว็บ (Cloudflare Workers)

เว็บเป็นไฟล์ static ล้วน ใช้ **Cloudflare Workers (static assets)** โฮสต์ (แผนฟรีพอ ใช้กับ repo private ได้) และกันคนนอกด้วย **รหัสผ่าน** — สำคัญ เพราะใน builder มีเนื้อหา `.etch.txt` ทุกไฟล์ ใครเปิดเว็บได้ก็ copy template ไปได้

- `wrangler.jsonc` — Worker ชื่อ `template-etch` (`"name"` ต้องตรงกับใน dashboard) รัน `python3 _build/build_site.py` ก่อน deploy ทุกครั้ง แล้วเสิร์ฟไฟล์จาก `dist/`
- `worker/index.js` — ด่านรหัสผ่าน: ทุก request (หน้าเว็บ, script, หน้า preview) ต้องผ่านด่านนี้ก่อน (`run_worker_first`) เบราว์เซอร์จะเด้งกล่องถามชื่อผู้ใช้ + รหัสผ่าน (ช่องชื่อผู้ใช้ใส่อะไรก็ได้) **ถ้ายังไม่ได้ตั้งรหัส เว็บจะปฏิเสธทุก request** (ขึ้น 503) จึงไม่มีทางเปิดเป็นสาธารณะโดยไม่ตั้งใจ
- `build_site.py` รวมเฉพาะไฟล์ที่ต้องขึ้นเว็บไว้ใน `dist/` (`builder/`, `preview/`, หน้าแรกที่พาไป builder, `_headers`, `robots.txt`) — `_build/`, README, ไฟล์ `.etch.txt` และ `preview/kit.json` ไม่ขึ้นเว็บ (แต่เนื้อหา `.etch.txt` อยู่ในปุ่ม Copy ของ builder)
- ลองในเครื่องแบบเดียวกับบน Cloudflare: สร้างไฟล์ `.dev.vars` ที่มีบรรทัด `BUILDER_PASSWORD="รหัสทดสอบ"` (ไฟล์นี้ไม่ถูก commit) แล้ว `npx wrangler dev` เปิด `http://localhost:8787`

### ตั้งค่าครั้งแรก (Cloudflare dashboard — ชื่อเมนูอาจต่างเล็กน้อยตามเวอร์ชัน)

1. **เชื่อม repo** — Workers & Pages → Create → **Import a repository** (Connect to Git) → เลือก `Template-ETCH` → ตั้งชื่อ Worker `template-etch`
2. **ตั้งค่า build** — Worker → Settings → **Builds**
   - Build command: ว่างไว้ (`wrangler.jsonc` สั่ง build เอง) · Deploy command: `npx wrangler deploy` · Production branch: `main`
   - ปิด **Builds for Preview branches** (build เฉพาะ `main`)
3. **ตั้งรหัสผ่าน** — Worker → Settings → **Variables and Secrets** → Add
   - Type: **Secret** · Name: `BUILDER_PASSWORD` · Value: รหัสยาว ๆ ที่เดายาก (แนะนำ 20 ตัวขึ้นไป สุ่มจาก password manager)
   - Deploy / Save — รหัสเก็บใน Cloudflare เท่านั้น ไม่อยู่ใน repo และไม่หายตอน deploy ใหม่
   - เปลี่ยนรหัส: แก้ค่า secret เดิม (คนที่ล็อกอินค้างไว้ต้องปิดเบราว์เซอร์แล้วล็อกอินใหม่)
4. **ลิงก์ preview ของ branch** — `wrangler.jsonc` ตั้ง `"preview_urls": false` ไว้แล้ว ตรวจในแท็บ **Domains** ว่า Preview URLs เป็น Disabled
5. **เปิดเว็บ** — แท็บ **Domains** → workers.dev ต้องเป็น Enabled (`wrangler.jsonc` ตั้ง `"workers_dev": true` deploy แล้วจะเปิดเอง)
6. **ตรวจ** — เปิด `https://template-etch.<บัญชีของคุณ>.workers.dev` ในหน้าต่างไม่ระบุตัวตน (Incognito)
   - ต้องเด้งกล่องถามรหัสก่อน กด Cancel ต้องเห็น "Password required." · ใส่รหัสผิดต้องถามซ้ำ · ใส่ถูกต้องเห็น Page Builder
   - ถ้าขึ้น "Page Builder is locked" แปลว่ายังไม่ได้ตั้ง secret ในข้อ 3

> อยากได้ล็อกอินด้วยอีเมลแทนรหัสผ่าน: ใช้ Cloudflare Access (Zero Trust แผน Free ต้องผูกบัตร) — แท็บ Domains → workers.dev → Enable Access แล้วจำกัด Policy เป็นอีเมลของคุณ ใช้คู่กับรหัสผ่านได้

### หลังจากนั้น

- merge เข้า `main` → Cloudflare build + deploy ให้เองภายในไม่กี่นาที
- เว็บใช้ไฟล์ preview ที่ commit ไว้ ถ้าแก้ template ต้อง build + commit ก่อน (CI จะเตือนถ้าลืม — ดูด้านล่าง)
- `_build/site/_headers` กำหนด security headers ของเว็บ (CSP, ห้ามเว็บอื่นฝัง, `noindex`) ถ้าเพิ่มของที่โหลดจากเว็บอื่น ต้องเพิ่มโดเมนใน CSP ด้วย
- อยากใช้โดเมนของตัวเอง: Worker → แท็บ Domains → Add → Custom domain (รหัสผ่านใช้กับทุกโดเมนของ Worker อยู่แล้ว)

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
- หน้าที่เขียนเอง (`builder/index.html`, `builder.css`, `builder.js`, `presets.js`, `pages.js`) ไม่ต้อง build
# Template-ETCH
