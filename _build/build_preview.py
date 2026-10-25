"""Preview + page builder data, made from the built .etch.txt files (run by build_all.py, or on its own).

    python3 _build/build_preview.py

Reads only — never writes a .etch.txt. Outputs:
  preview/kit.json            every payload in one file
  preview/<id>.html           one page per template, rendered from the same payload that is pasted into Etch
  preview/assets/             ACSS stand-in (acss_sim.py) + frame.js (talks to the builder)
  preview/index.html          list of all previews
  builder/kit-data.js         template list + .etch.txt contents for builder/index.html (works on file://)
"""
import html, json, os, re, shutil

from acss_sim import css as acss_css, COLORS as ACSS_COLORS
from kit import COLORS_CSS
from render_preview import render

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# id, group, label, file, note
CATALOG = [
    ("header", "header", "Header", "etch-header/site-header-ohmyetch.etch.txt",
     "โลโก้ · เมนูกลาง · ปุ่ม (Oh My Etch)"),
    ("header-menubuilder", "header", "Header (Menu Builder)", "etch-header/site-header.etch.txt",
     "แบบเดิม · ไม่ต้องมีปลั๊กอินเพิ่ม"),
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
# where a template belongs in Etch (shown in the builder export)
PLACE = {
    "page-hero": "บนสุดของหน้าด้านใน หรือ template Page",
    "blog": "Posts page หรือ template Archive/Index เท่านั้น (loop ใช้ main query)",
    "single-post": "template Single เท่านั้น (แทน <main> เดิม)",
    "404": "template 404 เท่านั้น",
    "cta": "component — วางซ้ำได้ทุกหน้า แก้ข้อมูลที่ props ครั้งเดียว",
    "contact": "component — หน้า Contact",
    "footer": "component — วางใน template ทุกตัว",
}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — preview</title>
<link rel="stylesheet" href="assets/acss-sim.css">
<style>
{css}
</style>
</head>
<body data-template="{id}">
{body}
<script src="assets/frame.js"></script>
{scripts}
</body>
</html>
"""


def main_colors():
    """The five --main-* defaults from kit.COLORS_CSS: which ACSS variable each follows + the preview value."""
    out = []
    for key, var, fallback in re.findall(r"--(main-[\w-]+):\s*var\(--([\w-]+),\s*([^)]+)\)", COLORS_CSS):
        out.append({"key": key, "acss": var, "value": ACSS_COLORS.get(var, fallback.strip())})
    return out


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    preview = os.path.join(ROOT, "preview")
    kit = {"templates": []}
    data = {"templates": [], "colors": main_colors(), "acss": {k: ACSS_COLORS[k] for k in ("primary", "secondary")}}
    write(os.path.join(preview, "assets", "acss-sim.css"), acss_css())
    shutil.copyfile(os.path.join(HERE, "preview_assets", "frame.js"), os.path.join(preview, "assets", "frame.js"))

    for tid, group, label, path, note in CATALOG:
        raw = open(os.path.join(ROOT, path), encoding="utf-8").read()
        payload = json.loads(raw)
        kit["templates"].append({"id": tid, "group": group, "label": label, "note": note,
                                 "file": os.path.basename(path), "payload": payload})
        body, css, scripts = render(payload)
        js = "\n".join(f'<script type="module">\n{s}\n</script>' for s in scripts)
        write(os.path.join(preview, f"{tid}.html"),
              PAGE.format(title=html.escape(label), css=css, id=tid, body=body, scripts=js))
        data["templates"].append({"id": tid, "group": group, "label": label, "note": note, "place": PLACE.get(tid, ""),
                                  "file": os.path.basename(path), "path": path, "preview": f"../preview/{tid}.html",
                                  "etch": raw})

    dest = os.path.join(preview, "kit.json")
    json.dump(kit, open(dest, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))

    items = "\n".join(f'<li><a href="{t["id"]}.html">{html.escape(t["label"])}</a> <small>{t["file"]}</small></li>'
                      for t in data["templates"])
    write(os.path.join(preview, "index.html"), f"""<!doctype html>
<html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Etch Template Kit — previews</title>
<style>body{{font:16px/1.6 system-ui,sans-serif;max-width:720px;margin:40px auto;padding:0 16px}}small{{color:#777}}</style>
</head><body><h1>Etch Template Kit — previews</h1>
<p>สร้างจากไฟล์ .etch.txt โดย <code>_build/build_preview.py</code> · ประกอบหน้าเว็บได้ที่ <a href="../builder/index.html">Page Builder</a>
· เพิ่ม <code>?root=16</code> ท้าย URL เพื่อดูแบบ 1rem = 16px</p>
<ul>
{items}
</ul></body></html>
""")

    write(os.path.join(ROOT, "builder", "kit-data.js"),
          "/* generated by _build/build_preview.py — do not edit */\nwindow.ETCH_KIT = "
          + json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + ";\n")
    print("ok preview:", len(CATALOG), "pages,", os.path.getsize(dest) // 1024, "KB kit.json · builder/kit-data.js",
          os.path.getsize(os.path.join(ROOT, "builder", "kit-data.js")) // 1024, "KB")


if __name__ == "__main__":
    main()
