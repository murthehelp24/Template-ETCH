"""Bundle every .etch.txt into preview/kit.json for the template preview page (preview/index.html)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# id, group, label, file, note
CATALOG = [
    ("header", "header", "Header", "etch-header/site-header-ohmyetch.etch.txt",
     "โลโก้ · เมนูกลาง · ปุ่ม (Oh My Etch)"),
    ("hero", "section", "Hero หน้าแรก", "etch-sections/main-hero.etch.txt", "H1 · ปุ่ม 2 ปุ่ม · จุดเด่น · รูป"),
    ("page-hero", "section", "Page Hero", "etch-sections/main-page-hero.etch.txt", "breadcrumb + ชื่อหน้า"),
    ("features", "section", "Features", "etch-sections/main-features.etch.txt", "การ์ดไอคอน 4 ใบ"),
    ("split", "section", "รูป + ข้อความ", "etch-sections/main-split.etch.txt", "checklist + ปุ่ม"),
    ("stats", "section", "Stats", "etch-sections/main-stats.etch.txt", "ตัวเลข 4 ช่อง"),
    ("steps", "section", "Steps", "etch-sections/main-steps.etch.txt", "ขั้นตอน 4 ขั้น"),
    ("reviews", "section", "Reviews", "etch-sections/main-reviews.etch.txt", "รีวิว 3 ใบ"),
    ("faq", "section", "FAQ", "etch-sections/main-faq.etch.txt", "คำถามเปิด/ปิดได้"),
    ("cta", "section", "CTA ติดต่อ", "etch-sections/main-cta.etch.txt", "component · ข้อมูลติดต่อ + แผนที่"),
    ("contact", "section", "Contact", "etch-sections/main-contact.etch.txt", "component · หน้าติดต่อ"),
    ("blog", "section", "Blog", "etch-sections/main-blog.etch.txt", "การ์ดบทความ + เลขหน้า"),
    ("single-post", "section", "บทความเดี่ยว", "etch-sections/main-single-post.etch.txt", "template Single"),
    ("404", "section", "404", "etch-sections/main-404.etch.txt", "template 404"),
    ("footer", "footer", "Footer", "etch-footer/main-footer.etch.txt", "component · ปุ่ม LINE/โทรลอย"),
]

out = {"templates": []}
for tid, group, label, path, note in CATALOG:
    out["templates"].append({"id": tid, "group": group, "label": label, "note": note,
                             "file": os.path.basename(path), "payload": json.load(open(os.path.join(ROOT, path)))})
os.makedirs(os.path.join(ROOT, "preview"), exist_ok=True)
dest = os.path.join(ROOT, "preview", "kit.json")
json.dump(out, open(dest, "w"), ensure_ascii=False, separators=(",", ":"))
print("ok", dest, os.path.getsize(dest) // 1024, "KB")
