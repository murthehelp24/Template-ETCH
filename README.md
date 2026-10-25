# Etch Template Kit (main-*)

ชุด template สำหรับ Etch + ACSS ที่ใช้ร่วมกันได้ทุกโปรเจค — ทุกไฟล์ใช้สีชุดเดียวกัน ชื่อคลาสชุดเดียวกัน และวางรวมในเว็บเดียวได้โดยไม่ชนกัน

วิธีวางเหมือนกันทุกไฟล์: เปิดไฟล์ `.etch.txt` → Select All → Copy → ใน Etch คลิกขวาตำแหน่งที่จะวาง → **Paste**

| โฟลเดอร์ | ไฟล์ |
|---|---|
| [etch-header](etch-header/README.md) | `site-header-ohmyetch` (แนะนำ, ต้องมีปลั๊กอิน Oh My Etch) · `site-header` (Menu Builder) |
| [etch-footer](etch-footer/README.md) | `main-footer` (component + ปุ่ม LINE/โทรลอย) |
| [etch-sections](etch-sections/README.md) | hero · page-hero · features · split · stats · steps · reviews · faq · cta · contact · blog · single-post · 404 |
| `_build` | ไฟล์สร้าง template (Python) — ไม่ต้องใช้ตอนวาง ใช้ตอนแก้ template แล้วสร้างไฟล์ใหม่ |

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
# Template-ETCH
