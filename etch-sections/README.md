# Section templates — Etch (main-* family)

ไม่ผูกกับเว็บไหน วางครั้งเดียวได้ครบ (block + styles + component + loop) และใช้สีกลางชุดเดียวกับ header / footer
วิธีวางเหมือนกันทุกไฟล์: เปิดไฟล์ → Select All → Copy → ใน Etch คลิกขวาตำแหน่งที่จะวาง → **Paste**

| ไฟล์ | เป็นอะไร | วางที่ไหน |
|---|---|---|
| `main-hero.etch.txt` | Hero หน้าแรก: H1, ปุ่ม 2 ปุ่ม, จุดเด่น 3 ข้อ, รูป | บนสุดของหน้าแรก |
| `main-hero-image.etch.txt` | Hero ภาพเต็มจอ: รูปพื้นหลัง + สีหลักทับ, ข้อความกลาง, ปุ่ม Chat on LINE + Our services, จุดเด่น 3 ข้อเรียงแถว | บนสุดของหน้าแรก (ใช้ Hero แบบเดียวต่อหน้า) |
| `main-hero-gradient.etch.txt` | Hero ภาพ + สีไล่: รูปพื้นหลัง สีหลักทับเข้มทางซ้ายจางไปขวา, ข้อความชิดซ้าย, ปุ่ม Chat on LINE + โทร | บนสุดของหน้าแรก |
| `main-hero-collage.etch.txt` | Hero รูปซ้อน: H1, ปุ่ม, ตัวเลข 3 ช่อง, รูป 3 ภาพ + ป้าย "15+ years" | บนสุดของหน้าแรก |
| `main-hero-panel.etch.txt` | Hero พื้นสีหลัก: ข้อความบนสี primary, รูปชิดขอบขวามุมล่างโค้ง | บนสุดของหน้าแรก |
| `main-page-hero.etch.txt` | หัวหน้าเพจด้านใน: breadcrumb + `{this.title}` + excerpt (ถ้ามี) | template **Page** หรือบนสุดของหน้าด้านใน |
| `main-features.etch.txt` | การ์ดไอคอน 4 ใบ (บริการ / จุดเด่น) | หน้าไหนก็ได้ |
| `main-features-image.etch.txt` | Features + รูป: รูปซ้าย · หัวข้อ + จุดเด่น 4 ข้อมีไอคอน (2×2) | หน้าไหนก็ได้ (ใช้ Features แบบเดียวต่อหน้าก็พอ) |
| `main-features-numbered.etch.txt` | Features เลข 01–06: 6 ข้อ เลขลำดับใหญ่ขึ้นเอง ไม่มีไอคอน | หน้าไหนก็ได้ |
| `main-features-band.etch.txt` | Features พื้นสีหลัก: ไอคอนวงกลมสีเน้น 4 ข้อ ข้อความกลาง | หน้าไหนก็ได้ |
| `main-features-cards.etch.txt` | Features การ์ดรูป: บริการ 3 การ์ด รูป + ข้อความ + ลิงก์ (คลิกได้ทั้งการ์ด) | หน้าแรก / หน้าบริการ |
| `main-features-list.etch.txt` | Features หัวข้อ + รายการ: หัวข้อ + ปุ่มด้านซ้าย (ติดตอนเลื่อน) · รายการไอคอน 4 แถวด้านขวา | หน้าไหนก็ได้ |
| `main-split.etch.txt` | รูป + ข้อความ + checklist + ปุ่ม | หน้าไหนก็ได้ |
| `main-split-overlap.etch.txt` | รูป + ข้อความ ป้ายประสบการณ์: รูปบนกรอบสีเน้น · ป้าย "15+ ปี" สีหลัก · checklist + ปุ่ม | หน้าแรก / เกี่ยวกับเรา (ใช้รูป + ข้อความแบบเดียวต่อหน้าก็พอ) |
| `main-split-band.etch.txt` | รูป + ข้อความ พื้นสีหลัก: ข้อความ + checklist + ปุ่มบนสี primary · รูปจัตุรัสขวา | หน้าไหนก็ได้ |
| `main-split-stats.etch.txt` | รูป + ข้อความ + ตัวเลข: ตัวเลขผลงาน 3 ช่องแทน checklist | หน้าแรก / เกี่ยวกับเรา |
| `main-split-images.etch.txt` | รูป 2 ภาพ + ข้อความ: ข้อความซ้าย · รูปใหญ่ + รูปเล็กกรอบขาวซ้อนมุมล่าง | เกี่ยวกับเรา |
| `main-split-full.etch.txt` | รูปเต็มครึ่งจอ + ข้อความ: รูปชิดขอบซ้ายครึ่งหน้า · ข้อความอีกครึ่ง | หน้าไหนก็ได้ |
| `main-stats.etch.txt` | ตัวเลขผลงาน 4 ช่อง บนพื้นสี primary | หน้าไหนก็ได้ |
| `main-stats-light.etch.txt` | Stats พื้นสว่าง: ตัวเลข 4 ช่องสีหลัก ขีดสีเน้นใต้เลข เส้นคั่นระหว่างช่อง | หน้าไหนก็ได้ |
| `main-stats-cards.etch.txt` | Stats การ์ดไอคอน: 4 การ์ด ไอคอน + ตัวเลข + คำอธิบาย | หน้าไหนก็ได้ |
| `main-stats-split.etch.txt` | Stats หัวข้อ + ตัวเลข: หัวข้อซ้าย · ตัวเลข 2×2 ขวา (สลับสีพื้น) | เกี่ยวกับเรา |
| `main-stats-image.etch.txt` | Stats บนรูป: รูปพื้นหลัง + สีหลักทับ · หัวข้อ + ตัวเลข 4 กรอบ | หน้าแรก |
| `main-steps.etch.txt` | ขั้นตอน 4 ขั้น (เลขขึ้นเองอัตโนมัติ) | หน้าไหนก็ได้ |
| `main-steps-line.etch.txt` | Steps เส้นเวลา: วงกลมเลข 4 ขั้นต่อกันด้วยเส้นประ (เลขขึ้นเอง) | หน้าไหนก็ได้ |
| `main-steps-vertical.etch.txt` | Steps แนวตั้ง: หัวข้อ + ปุ่มซ้าย · ขั้นตอนเรียงลงพร้อมเส้นเชื่อมขวา | หน้าบริการ |
| `main-steps-cards.etch.txt` | Steps การ์ด: 4 การ์ด ขอบบนสีเน้น เลขใหญ่จางมุมขวา | หน้าไหนก็ได้ |
| `main-steps-band.etch.txt` | Steps พื้นสีหลัก: ป้าย "Step 1–4" + ลูกศรระหว่างขั้น บนสี primary | หน้าไหนก็ได้ |
| `main-reviews.etch.txt` | รีวิวลูกค้า 3 ใบ + ดาว | หน้าไหนก็ได้ |
| `main-reviews-featured.etch.txt` | Reviews รีวิวเด่น: รีวิวเดียวตัวใหญ่กลางหน้า + ดาว + รูปและชื่อลูกค้า | หน้าแรก |
| `main-reviews-band.etch.txt` | Reviews พื้นสีหลัก: 3 รีวิวในกรอบเส้น บนสี primary | หน้าไหนก็ได้ |
| `main-reviews-split.etch.txt` | Reviews คะแนน + รีวิว: หัวข้อ + คะแนน 4.9 ★ ซ้าย · 4 รีวิว 2×2 ขวา | หน้าแรก / หน้ารีวิว |
| `main-faq.etch.txt` | คำถามที่พบบ่อย เปิด/ปิดได้ | หน้าไหนก็ได้ |
| `main-faq-split.etch.txt` | FAQ หัวข้อ + กล่องติดต่อ: หัวข้อ + กล่อง "ยังมีคำถาม?" สีหลักซ้าย (ติดตอนเลื่อน) · คำถามแบบเส้นขวา | หน้าไหนก็ได้ (ใช้ FAQ แบบเดียวต่อหน้าก็พอ) |
| `main-faq-cards.etch.txt` | FAQ การ์ด: 6 การ์ด "Q." แสดงคำตอบทุกข้อ ไม่ต้องกดเปิด | หน้าบริการ |
| `main-faq-minimal.etch.txt` | FAQ เรียบ: คำถามเลข 01–06 แบบเส้นคั่น + ลิงก์ "Contact us" ใต้รายการ | หน้าไหนก็ได้ |
| `main-faq-image.etch.txt` | FAQ + รูป: รูปซ้าย · คำถามในกล่องสีอ่อนขวา (เปิดแล้วเป็นสีเน้น) | หน้าแรก / เกี่ยวกับเรา |
| `main-cta.etch.txt` | Component **Main CTA** (`MainCta`) ติดต่อ + แผนที่ | ท้ายหน้าต่างๆ — วางซ้ำได้ทุกหน้า |
| `main-cta-form.etch.txt` | CTA ฟอร์ม + ข้อมูลติดต่อ: หัวข้อ + โทร / LINE / อีเมล / เวลาเปิดซ้าย · การ์ดฟอร์มขวา | ท้ายหน้า / หน้าติดต่อ |
| `main-cta-form-band.etch.txt` | CTA ฟอร์ม พื้นสีหลัก: หัวข้อ + checklist + ปุ่มโทรบนสีหลัก · ฟอร์มขอให้โทรกลับ (ชื่อ เบอร์ ข้อความ) | ท้ายหน้าแรก / หน้าบริการ |
| `main-cta-form-image.etch.txt` | CTA ฟอร์ม บนรูป: รูปพื้นหลัง + สีหลักไล่ · ปุ่ม LINE + เบอร์ · การ์ดฟอร์มขวา | ท้ายหน้าแรก |
| `main-cta-form-map.etch.txt` | CTA ฟอร์ม + แผนที่: หัวข้อกลาง · ฟอร์มกับ Google Map คู่กัน · ข้อมูลติดต่อแถวล่าง | หน้าติดต่อ |

**ฟอร์มใน CTA** เป็น HTML ธรรมดา (`<form class="main-form" action="https://formspree.io/f/your-form-id" method="post">`) — หลังวางใน Etch ให้เปลี่ยน `action` เป็น URL ของบริการรับฟอร์ม (เช่น สร้างฟอร์มที่ formspree.io แล้วเอา URL มาใส่) หรือแทนทั้งฟอร์มด้วย block ของปลั๊กอินฟอร์มที่ใช้อยู่ (Fluent Forms, WS Form …) โดยคงกล่อง `main-form-card` ไว้ · แผนที่ใน `cta-form-map` เปลี่ยนที่ `src` ของ iframe (Google Maps → Share → Embed a map)
| `main-contact.etch.txt` | Component **Main Contact** (`MainContact`) | หน้า Contact |
| `main-blog.etch.txt` | การ์ดบทความ + pagination (loop `mainQuery`) | Posts page หรือ template Archive/Index |
| `main-single-post.etch.txt` | `<main>` บทความเดี่ยว + แชร์ + related (loop `mainRelatedPosts`) | template **Single** |
| `main-404.etch.txt` | `<main>` หน้าไม่พบ + ปุ่มกลับหน้าแรก | template **404** |

ทุกตัวใช้ชื่อคลาส `main-*` จึงไม่ชนกับ style เดิมของเว็บปลายทาง ชิ้นที่ใช้ร่วมกัน (`main-heading`, `main-social`, `main-card`, `main-buttons`, `main-checks`, `main-media__img`, `main-band`) มี CSS เหมือนกันทุกไฟล์ วางไฟล์ไหนก่อนก็ได้

---

## Hero แบบรูปพื้นหลัง (ภาพเต็มจอ / ภาพ + สีไล่)

- รูป: **Background Image** → เลือกรูปจาก Media Library (ตอนยังไม่มีรูปจะเห็นเป็นพื้นสีหลัก)
- ความเข้มของสีทับแก้ที่ `&::before` ใน `.main-hero-image` (78%) / `.main-hero-gradient` (92% → 64% → 0%) — บนมือถือแบบสีไล่จะทับเท่ากันทั้งรูป (80%) ให้อ่านข้อความออก
- ปุ่มใช้ `btn--secondary` (+ `btn--outline`) แบบเดียวกับปุ่มบน header เพราะอยู่บนพื้นสีหลัก · แก้ลิงก์ LINE และเบอร์โทรใน **Buttons**

## Hero รูปซ้อน / พื้นสีหลัก

- รูปซ้อน: รูป 3 ช่องใน **Media** (ช่องแรกสูงเต็ม) · ตัวเลขใน **Stats** (`<dl>`) และป้ายใน **Badge** เป็นตัวอย่าง — ใส่ตัวเลขจริงของลูกค้า
- พื้นสีหลัก: รูปชิดขอบขวาของจอ (ไม่อยู่ใน container) ข้อความเว้นซ้ายเท่าขอบ container · จอ ≤992px รูปลงไปอยู่ใต้ข้อความ

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
- ชุดแรก (FAQ, CTA, Contact, Blog, Single) บนเว็บลูกค้าเว็บแรก
- ทั้ง 13 ไฟล์ + header + footer วางรวมหน้าเดียวบนเว็บลูกค้าอีกเว็บ (1rem = 16px) — สีมาจากชุดเดียวกัน, layout ถูกต้องที่ 1440px และ 375px ไม่ล้นจอ, ลบของทดสอบออกแล้ว
- ยังไม่ได้ทดสอบ: การ์ดใน Blog archive บน Posts page จริง
