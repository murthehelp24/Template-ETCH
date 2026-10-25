# Main Footer — Etch template

`main-footer.etch.txt` วางครั้งเดียวได้ทั้ง component, styles, ไอคอน และปุ่ม LINE / โทรแบบลอยมุมจอ

## วิธีใช้

1. เปิด `main-footer.etch.txt` → Select All → Copy
2. ใน Etch คลิกขวาท้าย template → **Paste**
   Etch จะสร้าง component **Main Footer** (key `MainFooter`) และวาง instance ให้
3. วาง instance เดียวกันในทุก template (Index, Single, 404 …) จาก Components panel

## แก้ข้อมูล — ทำที่เดียว ทุก template เปลี่ยนตาม

เปิด component **Main Footer** → แก้ **ค่า default ของ properties**:

| Property | หมายเหตุ |
|---|---|
| Description | ข้อความใต้โลโก้ |
| Contact Title | หัวข้อคอลัมน์ติดต่อ |
| Address / Opening Hours | ว่าง = ซ่อน, ขึ้นบรรทัดใหม่ได้ |
| Phone / Email / Map URL | ว่าง = ซ่อน |
| Map Label | ข้อความลิงก์แผนที่ |
| LINE / Facebook / Instagram / TikTok / YouTube URL | ว่าง = ซ่อนไอคอนนั้น |
| Copyright Note | ต่อท้าย copyright |
| **Floating Buttons** | เปิด/ปิดปุ่มลอยมุมขวาล่าง (LINE + โทร) ใช้ LINE URL และ Phone ชุดเดียวกัน |

- **ชื่อเว็บ** ใน copyright และ alt ของโลโก้ดึงจาก **Settings → General → Site Title** อัตโนมัติ (`{site.name}`) ปีขึ้นเอง
- ถ้าต้องการให้บางหน้าต่างออกไป แก้ property บน instance นั้นแทน

**แก้ใน component โดยตรง (Edit component):**
- **Logo Image** → เลือกรูปโลโก้ (ตอนวางเป็น placeholder)
- คอลัมน์ **Menu** และ **Services** → แก้ข้อความ/ลิงก์, เพิ่ม/ลบ Item ได้

## สี

พื้น footer = `--main-primary`, ตัวอักษร = `--main-on-primary` จากสีกลางของชุด — ดู [README หลัก](../README.md#สี)
ขนาดโลโก้: `--main-footer-logo-width` ใน `.main-footer`

## Layout

- ≥993px: แบรนด์ (กว้าง 2 ส่วน) · Menu · Services · Contact
- 769–992px: แบรนด์เต็มแถว แล้ว 2 คอลัมน์
- ≤768px: คอลัมน์เดียว

## ต่างจาก footer ของ Pinn Pain

- ข้อมูลติดต่อใช้ **component properties** แทน Meta Box options — เว็บใหม่ไม่ต้องสร้าง options page
- คอลัมน์ Services เป็นลิงก์ธรรมดาแทน loop ของ CPT `service`
- ไอคอน social เป็น SVG สีเดียว (ตามสีธีม) ฝังในไฟล์ ไม่ต้องอัปโหลด และใช้คลาส `main-social` ชุดเดียวกับ CTA / Contact / ปุ่มแชร์
- ใช้ media query ธรรมดา (992 / 768px) แทน `@custom-media` เพื่อไม่ไปทับค่า breakpoint ของเว็บปลายทาง

## ต้องมีที่เว็บปลายทาง

Etch 1.6+, ACSS (`--space-*`, `--section-space-s`, `--gutter`, `--grid-gap`, `--container-gap`, `--text-s/m`)
