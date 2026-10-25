# Header templates — Etch

| ไฟล์ | เมนูใช้ | ต้องมีที่เว็บปลายทาง |
|---|---|---|
| `site-header-ohmyetch.etch.txt` (ใหม่) | Oh My Etch — Navigation Menu + Navigation Menu Mobile | ปลั๊กอิน **Oh My Etch** (ทดสอบกับ 1.5.8) |
| `site-header-ohmyetch-light.etch.txt` | เหมือนบรรทัดบน — **พื้นสว่าง**: พื้นสีอ่อน ตัวอักษรเข้ม ปุ่ม `btn--primary` | Oh My Etch |
| `site-header-ohmyetch-center.etch.txt` | **โลโก้กลาง**: จอ ≥1200px โลโก้กลางแถวบน ปุ่มขวา เมนูกึ่งกลางแถวล่าง | Oh My Etch |
| `site-header-ohmyetch-topbar.etch.txt` | **แถบข้อมูลด้านบน**: ที่อยู่ · เวลาเปิด · โทร · อีเมล · LINE (มือถือเหลือเวลาเปิด + โทร) | Oh My Etch |
| `site-header-ohmyetch-floating.etch.txt` | **ลอยมุมโค้ง**: แถบเมนูโค้ง มีเงา เว้นขอบรอบ | Oh My Etch |
| `site-header-ohmyetch-right.etch.txt` | **เมนูชิดขวา**: เส้นสีเน้นด้านบน เมนูชิดขวาติดปุ่มเดียว (ไม่มีปุ่มเบอร์โทรบนแถบ) | Oh My Etch |
| `site-header.etch.txt` (เดิม) | ชุด MenuWrapper / MenuDropdown / ToggleButton | ไม่ต้องมีปลั๊กอินเพิ่ม (script อยู่ใน component) |

วิธีวางเหมือนกันทั้งสองไฟล์: เปิดไฟล์ → Select All → Copy → ใน Etch คลิกขวา → **Paste**
**5 แบบใหม่** สร้างจาก header Oh My Etch ตัวเดียวกัน (`_build/build_header_variants.py`): โครงและ style `main-header__*` เหมือนกันทุกตัว ต่างกันที่คลาสเสริม `main-header--light` / `--center` / `--topbar` / `--floating` / `--right` บน `<header>` ซึ่งเก็บ CSS ของแบบนั้นไว้ — วิธีแก้เมนู ปุ่ม สี และ data attributes ใช้ตามหัวข้อ Oh My Etch ด้านล่างได้ทั้งหมด · ใช้ header ทีละแบบต่อเว็บ (ถ้าวางหลายแบบในเว็บเดียวก็ไม่ชนกัน)
แบบ **แถบข้อมูล**: แก้ข้อความ/ลิงก์ใน **Top Bar** (ที่อยู่, เวลา, `tel:`, `mailto:`, ลิงก์ LINE) · แบบ **ลอยมุมโค้ง** เหมาะกับ `data-overlay-header="true"` ถ้าอยากให้ลอยทับ hero

Page Builder มี header ให้เลือก 6 แบบ (Oh My Etch ทั้งหมด) — header แบบ Menu Builder ยังอยู่ในชุดนี้แต่ไม่อยู่ใน builder แล้ว

ทั้งสองใช้ชื่อคลาสต่างกัน (`main-header` / `site-header`) วางในเว็บเดียวกันได้ไม่ชนกัน

---

## Oh My Etch version (`site-header-ohmyetch.etch.txt`)

**แก้หลังวาง**
- **Logo Image** → เลือกรูปจาก Media Library
- เมนู: แก้ใน **Nav → Nav List** ที่เดียว — เมนูมือถือ (drawer) สร้างตามเมนู desktop อัตโนมัติ เพราะ `menuId` ของ **Nav** และ **Mobile Menu** ตรงกัน (`main-menu`) ถ้าเปลี่ยนต้องเปลี่ยนทั้งคู่
  - ลิงก์ธรรมดา: Item → Link (`a.main-header__link`)
  - Dropdown: Item → Trigger (ข้อความ) + Dropdown (ลิงก์ `a.main-header__dropdown-link`) — `contentId` ของ Trigger กับ Dropdown ต้องตรงกัน และไม่ซ้ำกับ dropdown อื่น
- ปุ่ม CTA / เบอร์โทร มี 2 ชุด: ใน **Actions** (บนแถบ) และใน **Mobile Menu → slot after** (ท้าย drawer)
- **สี**: ใช้สีกลางของชุด template (`--main-primary` = พื้นแถบ/dropdown/drawer, `--main-on-primary` = ตัวอักษร, `--main-accent` = เส้นใต้และ hover) แก้ที่ style `:where(:root)` ที่เดียว ดู [README หลัก](../README.md#สี)
- ปุ่มบนแถบใช้ `btn--secondary` (ปุ่ม primary จะกลืนกับพื้นแถบที่เป็นสี primary)
- ความสูงโลโก้: `--main-header-logo-height` ใน custom style `:root:has(.main-header)` (40px, มือถือ 32px)

**Layout**: ≥1200px โลโก้ · เมนูกึ่งกลาง · ปุ่ม | 769–1199px โลโก้ · ปุ่ม + hamburger | ≤768px โลโก้ · hamburger (drawer จากขวา + ปุ่มอยู่ท้าย drawer)
Sticky / overlay / hide-on-scroll / skip-link ใช้ data attributes ชุดเดียวกับตารางด้านล่าง

**หมายเหตุทางเทคนิค**
- Etch มีบั๊กตอน paste: class prop ใน group ที่มี condition ซ้อน (styling ของ Nav) จะไม่ถูกแปลง id → จึงจัด nav ผ่าน `.main-header__container > [data-ome-nav-menu-root]` แทน
- ACSS ใส่ typography ปุ่ม (ตัวพิมพ์ใหญ่/หนา) ให้ `<button>` ทุกตัว → reset ไว้ใน `.main-header` และ `.main-header__drawer`
- ปุ่มเบอร์โทรใช้ custom style `a.main-header__phone` (ใช้ได้ทั้งบนแถบและใน drawer และไม่ทำให้คลาส `btn--*` หาย)

---

## เวอร์ชันเดิม (`site-header.etch.txt`)

`site-header.etch.txt` คือ JSON แบบเดียวกับที่ Etch Copy สร้าง (version 2.1) วางครั้งเดียวได้ทั้ง block, styles, components และ script

## วิธีใช้

1. เปิดไฟล์ `site-header.etch.txt` → Select All → Copy
2. ใน Etch เลือก element ที่จะวาง header ไว้ถัดไป (หรือเลือก Body/Index ใน Structure) → คลิกขวา → **Paste** (⌘V)
3. แก้ 4 จุด:
   - **Logo Image** → เลือกรูปโลโก้จาก Media Library (ตอนวางจะเป็น placeholder "No image source provided")
   - **Menu Link / Services Dropdown** → เปลี่ยน label + linkUrl
   - **CTA** / **Phone** → ข้อความ, `href`, เบอร์โทร
   - สีมาจากสีกลางของชุด template (`:where(:root)`) — ดู [README หลัก](../README.md#สี); ความสูงโลโก้แก้ที่ `--header-logo-height` ใน `.site-header`

## ตัวเลือก (data attributes บน `<header>`)

| attribute | ค่า | ผล |
|---|---|---|
| `data-sticky-header` | `true` | ติดด้านบนตอน scroll (ค่าเริ่มต้น) |
| `data-overlay-header` | `true` | ลอยทับ hero (sticky + overlay = fixed) |
| `data-overlay-header-offset` | `true` | เว้นระยะ section แรกเท่าความสูง header |
| `data-hide-on-scroll` + `data-hide-at` | `true` / `200px` | ซ่อนเมื่อเลื่อนลงเกินค่า |
| `data-show-on-scroll-up` | `true` | โผล่กลับเมื่อเลื่อนขึ้น |
| `data-skip-link` | `true` | เพิ่มลิงก์ "Skip to main content" |

จุดที่เมนูเปลี่ยนเป็นแบบมือถือตั้งใน component **Menu** → Mobile Settings → Breakpoint (`1199px`)

## Layout

- Desktop: โลโก้ซ้าย · เมนู · ปุ่ม CTA + เบอร์โทร ขวา
- 769–1199px: โลโก้ซ้าย · ปุ่ม + hamburger ขวา
- ≤768px: โลโก้ซ้าย · hamburger ขวา (เมนู off-canvas จากขวา)

## สิ่งที่อยู่ในไฟล์

- Components: `MenuWrapper`, `MenuDropdown`, `MenuLink1`, `ToggleButton` — ถ้าเว็บปลายทางมี key นี้อยู่แล้ว Etch จะใช้ของเดิม (ไม่เขียนทับ เว้นแต่เปิด Settings → Overwrite on Paste)
- Class styles: `.site-header`, `__bar`, `__container`, `__logo`, `__logo-img`, `__actions`, `__nav`, `__nav-list`, `.mobile-menu-header` — ใช้ชื่อขึ้นต้น `site-header` เพื่อไม่ให้ชนกับ style ที่เว็บปลายทางมีอยู่แล้ว (Etch จะใช้ style เดิมของเว็บปลายทางถ้า selector ซ้ำ)
- CSS ของเมนู/hamburger เป็น **custom style** แบบ `.menu-dropdown:where(.site-header *)` — Etch compile custom style เสมอ ส่วน class style ที่ script เติมคลาสให้ตอน runtime จะไม่ถูก compile (นี่คือสาเหตุที่ hamburger ของ header เดิมต้อง copy CSS ไปไว้ใน `.header-wrapper`)
- ปุ่มใช้คลาส ACSS `btn--secondary` / `btn--outline` (ไม่มี style record ของตัวเอง จะได้ไม่ไปทับ CSS ปุ่มของเว็บปลายทาง)

## ต้องมีที่เว็บปลายทาง

Etch 1.6+, ACSS (`--space-*`, `--gutter`, `--text-s`, `--btn-*`, `--black`, `--white`, `--secondary`)
