# Section templates — Etch (main-* family)

ไม่ผูกกับเว็บไหน วางครั้งเดียวได้ครบ (block + styles + component + loop) และใช้สีกลางชุดเดียวกับ header / footer
วิธีวางเหมือนกันทุกไฟล์: เปิดไฟล์ → Select All → Copy → ใน Etch คลิกขวาตำแหน่งที่จะวาง → **Paste**

| ไฟล์ | เป็นอะไร | วางที่ไหน |
|---|---|---|
| `main-hero.etch.txt` | Hero หน้าแรก: H1, ปุ่ม 2 ปุ่ม, จุดเด่น 3 ข้อ, รูป | บนสุดของหน้าแรก |
| `main-page-hero.etch.txt` | หัวหน้าเพจด้านใน: breadcrumb + `{this.title}` + excerpt (ถ้ามี) | template **Page** หรือบนสุดของหน้าด้านใน |
| `main-features.etch.txt` | การ์ดไอคอน 4 ใบ (บริการ / จุดเด่น) | หน้าไหนก็ได้ |
| `main-split.etch.txt` | รูป + ข้อความ + checklist + ปุ่ม | หน้าไหนก็ได้ |
| `main-stats.etch.txt` | ตัวเลขผลงาน 4 ช่อง บนพื้นสี primary | หน้าไหนก็ได้ |
| `main-steps.etch.txt` | ขั้นตอน 4 ขั้น (เลขขึ้นเองอัตโนมัติ) | หน้าไหนก็ได้ |
| `main-reviews.etch.txt` | รีวิวลูกค้า 3 ใบ + ดาว | หน้าไหนก็ได้ |
| `main-faq.etch.txt` | คำถามที่พบบ่อย เปิด/ปิดได้ | หน้าไหนก็ได้ |
| `main-cta.etch.txt` | Component **Main CTA** (`MainCta`) ติดต่อ + แผนที่ | ท้ายหน้าต่างๆ — วางซ้ำได้ทุกหน้า |
| `main-contact.etch.txt` | Component **Main Contact** (`MainContact`) | หน้า Contact |
| `main-blog.etch.txt` | การ์ดบทความ + pagination (loop `mainQuery`) | Posts page หรือ template Archive/Index |
| `main-single-post.etch.txt` | `<main>` บทความเดี่ยว + แชร์ + related (loop `mainRelatedPosts`) | template **Single** |
| `main-404.etch.txt` | `<main>` หน้าไม่พบ + ปุ่มกลับหน้าแรก | template **404** |

ทุกตัวใช้ชื่อคลาส `main-*` จึงไม่ชนกับ style เดิมของเว็บปลายทาง ชิ้นที่ใช้ร่วมกัน (`main-heading`, `main-social`, `main-card`, `main-buttons`, `main-checks`, `main-media__img`, `main-band`) มี CSS เหมือนกันทุกไฟล์ วางไฟล์ไหนก่อนก็ได้

---

## Hero / Split — รูป
รูปเป็น Dynamic Image ว่างไว้ (ตอนวางจะเห็นกล่องสีอ่อน) → คลิก **Image** แล้วเลือกรูปจาก Media Library
สัดส่วนรูป: `--main-media-ratio` ใน `.main-hero__media` (5/4) และ `.main-split__media` (4/3)

## Split — สลับรูปไปขวา
เพิ่มคลาส `main-split--reverse` ที่ section (มี style รอไว้แล้ว) — มือถือรูปอยู่บนเสมอ

## Stats — พื้นสีเข้ม
ใช้คลาส `main-band` (พื้น `--main-primary`, ตัวอักษรขาว) — ใส่คลาสนี้ให้ section อื่นก็ได้ถ้าอยากให้เป็นแถบสีเข้ม

## Steps
เลข 01, 02 … มาจาก CSS counter — copy Step เพิ่มได้เลย ไม่ต้องแก้เลข

## Features
ไอคอนเป็น SVG ฝังในไฟล์ (shield, users, heart, award) — เปลี่ยนได้ที่ Icon → SVG source

## FAQ
แก้คำถาม/คำตอบตรงๆ ใน block (Item → Question / Answer) — copy Item เพิ่มได้ ใช้ `<details>` ไม่ต้องมี JS

## CTA / Contact (component)
แก้ **ค่า default ของ properties** ครั้งเดียว ทุกหน้าที่วางไว้เปลี่ยนตาม (หรือแก้บน instance ถ้าหน้านั้นอยากต่าง)
- ข้อความ: Eyebrow, Title, Intro, ปุ่ม, ป้ายกำกับ — แปลเป็นไทยได้ที่นี่
- ข้อมูลติดต่อ: Address, Opening Hours, Phone, Email, Map URL — **ว่าง = ซ่อนแถวนั้น**
- **Map Embed URL**: Google Maps → Share → Embed a map → copy ค่า `src` — ว่าง = ไม่มีแผนที่
- Social: LINE / Facebook / Instagram / TikTok / YouTube URL — ว่าง = ซ่อนไอคอน
- Contact มีเพิ่ม `LINE ID` และ `Social Title` และหัวข้อเป็น H1

> ข้อมูลติดต่อของ Footer, CTA และ Contact เป็น props แยกกันคนละ component — ตอนตั้งเว็บใหม่ให้กรอก 3 ที่ (ครั้งเดียว)

## Blog (archive)
- Loop `mainQuery` = main query ของ WordPress → ต้องอยู่บน **Posts page** หรือ template archive/index จึงจะมีโพสต์
- จำนวนโพสต์ต่อหน้า: Settings → Reading → Blog pages show at most

## Single post
เปิด template **Single** → ลบ `<main>` เดิม → Paste (ถ้ายังไม่มี header/footer ให้วางคู่กัน)

## 404
เปิด template **404** → Paste ระหว่าง header กับ footer

---

## ต้องมีที่เว็บปลายทาง
Etch 1.6+, ACSS (`--text-*`, `--space-*`, `--section-space-*`, `--h1…h5`, `--radius-*`, `--grid-gap`, `--container-gap`, `--content-gap`) และปุ่ม `btn--primary` / `btn--outline`

## ทดสอบแล้ว
- ชุดแรก (FAQ, CTA, Contact, Blog, Single) บน Pinn Pain
- ทั้ง 13 ไฟล์ + header + footer วางรวมหน้าเดียวบน Win Win Esco (1rem = 16px) — สีมาจากชุดเดียวกัน, layout ถูกต้องที่ 1440px และ 375px ไม่ล้นจอ, ลบของทดสอบออกแล้ว
- ยังไม่ได้ทดสอบ: การ์ดใน Blog archive บน Posts page จริง
