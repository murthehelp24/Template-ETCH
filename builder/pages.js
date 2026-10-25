/* Page types for the builder's "มาตรฐานหน้า" checklist and "จัดหน้าตามแบบแนะนำ". Hand-maintained.
   sections: the recommended order. need: "required" (red when missing) or "recommended" (amber).
   ids are template ids from builder/kit-data.js (_build/build_preview.py CATALOG). */
window.ETCH_PAGE_TYPES = [
  {
    "id": "home", "label": "หน้าแรก", "note": "หน้าที่คนเห็นเป็นอย่างแรก: บอกว่าทำอะไร ให้ใคร แล้วพาไปติดต่อ",
    "sections": [
      { "id": "hero", "need": "required", "why": "H1 บอกว่าทำอะไรให้ใคร + ปุ่มติดต่อ เห็นทันทีโดยไม่ต้องเลื่อน" },
      { "id": "features", "need": "recommended", "why": "บริการหรือจุดเด่น 3–4 ข้อ ให้รู้ว่ามีอะไรให้" },
      { "id": "split", "need": "recommended", "why": "เกี่ยวกับเรา / ทำไมต้องเลือกเรา พร้อมรูปจริง" },
      { "id": "stats", "need": "recommended", "why": "ตัวเลขผลงาน สร้างความน่าเชื่อถือเร็ว" },
      { "id": "steps", "need": "recommended", "why": "ขั้นตอนใช้บริการ ลดความกังวลก่อนติดต่อ" },
      { "id": "reviews", "need": "recommended", "why": "รีวิวลูกค้าจริง (social proof)" },
      { "id": "faq", "need": "recommended", "why": "ตอบคำถามที่ถามบ่อย ลดการทักถามซ้ำ" },
      { "id": "cta", "need": "required", "why": "ปิดท้ายด้วยช่องทางติดต่อ + แผนที่" }
    ]
  },
  {
    "id": "about", "label": "เกี่ยวกับเรา", "note": "เล่าว่าเป็นใคร ทำไมน่าไว้ใจ",
    "sections": [
      { "id": "page-hero", "need": "required", "why": "ชื่อหน้า (H1) + breadcrumb" },
      { "id": "split", "need": "required", "why": "เรื่องราว / ประวัติ พร้อมรูปทีมหรือสถานที่" },
      { "id": "stats", "need": "recommended", "why": "ตัวเลขประสบการณ์ จำนวนลูกค้า" },
      { "id": "features", "need": "recommended", "why": "คุณค่าหรือจุดยืนของแบรนด์" },
      { "id": "reviews", "need": "recommended", "why": "เสียงจากลูกค้า" },
      { "id": "cta", "need": "required", "why": "ปิดท้ายด้วยช่องทางติดต่อ" }
    ]
  },
  {
    "id": "services", "label": "บริการ", "note": "บอกรายละเอียดบริการ ขั้นตอน และตอบข้อสงสัยก่อนตัดสินใจ",
    "sections": [
      { "id": "page-hero", "need": "required", "why": "ชื่อบริการ (H1) + breadcrumb" },
      { "id": "features", "need": "required", "why": "รายการบริการหรือแพ็กเกจ" },
      { "id": "split", "need": "recommended", "why": "อธิบายบริการหลักพร้อมรูป" },
      { "id": "steps", "need": "recommended", "why": "ขั้นตอนการใช้บริการ" },
      { "id": "faq", "need": "recommended", "why": "คำถามเรื่องราคา เวลา เงื่อนไข" },
      { "id": "cta", "need": "required", "why": "ปุ่มนัดหมาย / ติดต่อ" }
    ]
  },
  {
    "id": "contact", "label": "ติดต่อเรา", "note": "ข้อมูลติดต่อครบ หาง่าย",
    "sections": [
      { "id": "contact", "need": "required", "why": "ที่อยู่ เวลา เบอร์ LINE แผนที่ (มี H1 ในตัว)" },
      { "id": "faq", "need": "recommended", "why": "คำถามก่อนเดินทาง / นัดหมาย" }
    ]
  },
  {
    "id": "blog", "label": "บทความ (Posts page)", "note": "รายการบทความ ใช้บน Posts page หรือ template Archive",
    "sections": [
      { "id": "blog", "need": "required", "why": "การ์ดบทความ + เลขหน้า (loop main query)" },
      { "id": "cta", "need": "recommended", "why": "ชวนติดต่อหลังอ่าน" }
    ]
  },
  {
    "id": "single", "label": "บทความเดี่ยว (template Single)", "note": "แม่แบบหน้าบทความทุกโพสต์",
    "sections": [
      { "id": "single-post", "need": "required", "why": "เนื้อหาบทความ + แชร์ + บทความที่เกี่ยวข้อง" },
      { "id": "cta", "need": "recommended", "why": "ชวนติดต่อหลังอ่านจบ" }
    ]
  },
  {
    "id": "404", "label": "ไม่พบหน้า (template 404)", "note": "หน้าที่เห็นเมื่อลิงก์เสีย",
    "sections": [
      { "id": "404", "need": "required", "why": "แจ้งว่าไม่พบหน้า + ปุ่มกลับหน้าแรก" }
    ]
  },
  {
    "id": "other", "label": "หน้าทั่วไป", "note": "หน้าอื่นๆ เช่น นโยบาย โปรโมชั่น ผลงาน",
    "sections": [
      { "id": "page-hero", "need": "required", "why": "ชื่อหน้า (H1) + breadcrumb" },
      { "id": "cta", "need": "recommended", "why": "ปิดท้ายด้วยช่องทางติดต่อ" }
    ]
  }
];
