"""Preview + page builder data, made from the built .etch.txt files (run by build_all.py, or on its own).

    python3 _build/build_preview.py

Reads only — never writes a .etch.txt. Outputs:
  preview/kit.json            every payload in one file
  preview/<id>.html           one page per template, rendered from the same payload that is pasted into Etch
  preview/assets/             ACSS stand-in (acss_sim.py) + frame.js (talks to the builder)
  preview/index.html          list of all previews
  preview/page.html           every template in one page; ?t=header,hero,footer picks and orders them (builder "ดูทั้งหน้า")
  builder/kit-data.js         template list + .etch.txt contents for builder/index.html (works on file://)
"""
import html, json, os, re, shutil

from acss_sim import css as acss_css, COLORS as ACSS_COLORS
from kit import COLORS_CSS
from render_preview import compile_css, render

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# id, group, label, file, note
CATALOG = [
    ("header", "header", "Header", "etch-header/site-header-ohmyetch.etch.txt",
     "โลโก้ · เมนูกลาง · ปุ่ม (Oh My Etch)"),
    ("header-light", "header", "Header พื้นสว่าง", "etch-header/site-header-ohmyetch-light.etch.txt",
     "พื้นสีอ่อน · ตัวอักษรเข้ม · ปุ่มสีหลัก"),
    ("header-center", "header", "Header โลโก้กลาง", "etch-header/site-header-ohmyetch-center.etch.txt",
     "โลโก้กลาง · เมนูแถวล่าง"),
    ("header-topbar", "header", "Header + แถบข้อมูล", "etch-header/site-header-ohmyetch-topbar.etch.txt",
     "แถบที่อยู่ · เวลาเปิด · โทร · อีเมล · LINE ด้านบน"),
    ("header-floating", "header", "Header ลอยมุมโค้ง", "etch-header/site-header-ohmyetch-floating.etch.txt",
     "แถบเมนูโค้งลอย มีเงา · ปุ่มกลม"),
    ("header-right", "header", "Header เมนูชิดขวา", "etch-header/site-header-ohmyetch-right.etch.txt",
     "เมนูชิดขวา ติดปุ่ม Chat on LINE"),
    ("hero", "section", "Hero หน้าแรก", "etch-sections/main-hero.etch.txt", "H1 · ปุ่ม 2 ปุ่ม · จุดเด่น · รูป"),
    ("hero-image", "section", "Hero ภาพเต็มจอ", "etch-sections/main-hero-image.etch.txt",
     "รูปเต็มจอ + สีทับ · ข้อความกลาง"),
    ("hero-gradient", "section", "Hero ภาพ + สีไล่", "etch-sections/main-hero-gradient.etch.txt",
     "รูปเต็มจอ · สีทับไล่จากซ้าย · ปุ่ม LINE + โทร"),
    ("hero-collage", "section", "Hero รูปซ้อน", "etch-sections/main-hero-collage.etch.txt",
     "ตัวเลข 3 ช่อง · รูป 3 ภาพ · ป้ายประสบการณ์"),
    ("hero-panel", "section", "Hero พื้นสีหลัก", "etch-sections/main-hero-panel.etch.txt",
     "ข้อความบนสีหลัก · รูปชิดขอบขวา"),
    ("page-hero", "section", "Page Hero", "etch-sections/main-page-hero.etch.txt", "breadcrumb + ชื่อหน้า"),
    ("features", "section", "Features", "etch-sections/main-features.etch.txt", "การ์ดไอคอน 4 ใบ"),
    ("features-image", "section", "Features + รูป", "etch-sections/main-features-image.etch.txt",
     "รูปด้านซ้าย · จุดเด่น 4 ข้อมีไอคอน"),
    ("features-numbered", "section", "Features เลข 01–06", "etch-sections/main-features-numbered.etch.txt",
     "6 ข้อ เลขลำดับใหญ่ ไม่มีไอคอน"),
    ("features-band", "section", "Features พื้นสีหลัก", "etch-sections/main-features-band.etch.txt",
     "ไอคอนวงกลม 4 ข้อ บนพื้นสีหลัก"),
    ("features-cards", "section", "Features การ์ดรูป", "etch-sections/main-features-cards.etch.txt",
     "บริการ 3 การ์ด มีรูป + ลิงก์"),
    ("features-list", "section", "Features หัวข้อ + รายการ", "etch-sections/main-features-list.etch.txt",
     "หัวข้อ + ปุ่มซ้าย · รายการไอคอนขวา"),
    ("split", "section", "รูป + ข้อความ", "etch-sections/main-split.etch.txt", "checklist + ปุ่ม"),
    ("split-overlap", "section", "รูป + ข้อความ ป้ายประสบการณ์", "etch-sections/main-split-overlap.etch.txt",
     "รูปบนกรอบสีเน้น · ป้าย 15+ ปี"),
    ("split-band", "section", "รูป + ข้อความ พื้นสีหลัก", "etch-sections/main-split-band.etch.txt",
     "ข้อความบนสีหลัก · รูปสี่เหลี่ยมจัตุรัสขวา"),
    ("split-stats", "section", "รูป + ข้อความ + ตัวเลข", "etch-sections/main-split-stats.etch.txt",
     "ตัวเลข 3 ช่องแทน checklist"),
    ("split-images", "section", "รูป 2 ภาพ + ข้อความ", "etch-sections/main-split-images.etch.txt",
     "ข้อความซ้าย · รูปใหญ่ + รูปเล็กซ้อน"),
    ("split-full", "section", "รูปเต็มครึ่งจอ + ข้อความ", "etch-sections/main-split-full.etch.txt",
     "รูปชิดขอบครึ่งหน้า · ข้อความอีกครึ่ง"),
    ("stats", "section", "Stats", "etch-sections/main-stats.etch.txt", "ตัวเลข 4 ช่อง"),
    ("stats-light", "section", "Stats พื้นสว่าง", "etch-sections/main-stats-light.etch.txt",
     "ตัวเลข 4 ช่อง เส้นคั่น บนพื้นขาว"),
    ("stats-cards", "section", "Stats การ์ดไอคอน", "etch-sections/main-stats-cards.etch.txt",
     "4 การ์ด ไอคอน + ตัวเลข"),
    ("stats-split", "section", "Stats หัวข้อ + ตัวเลข", "etch-sections/main-stats-split.etch.txt",
     "หัวข้อซ้าย · ตัวเลข 2×2 ขวา"),
    ("stats-image", "section", "Stats บนรูป", "etch-sections/main-stats-image.etch.txt",
     "รูปพื้นหลัง + สีหลักทับ · ตัวเลข 4 ช่อง"),
    ("steps", "section", "Steps", "etch-sections/main-steps.etch.txt", "ขั้นตอน 4 ขั้น"),
    ("steps-line", "section", "Steps เส้นเวลา", "etch-sections/main-steps-line.etch.txt",
     "วงกลมเลข 4 ขั้น ต่อด้วยเส้นประ"),
    ("steps-vertical", "section", "Steps แนวตั้ง", "etch-sections/main-steps-vertical.etch.txt",
     "หัวข้อ + ปุ่มซ้าย · ขั้นตอนเรียงลงขวา"),
    ("steps-cards", "section", "Steps การ์ด", "etch-sections/main-steps-cards.etch.txt",
     "4 การ์ด เลขใหญ่จางมุมขวา"),
    ("steps-band", "section", "Steps พื้นสีหลัก", "etch-sections/main-steps-band.etch.txt",
     "ป้าย Step 1–4 + ลูกศร บนสีหลัก"),
    ("reviews", "section", "Reviews", "etch-sections/main-reviews.etch.txt", "รีวิว 3 ใบ"),
    ("reviews-featured", "section", "Reviews รีวิวเด่น", "etch-sections/main-reviews-featured.etch.txt",
     "รีวิวเดียวตัวใหญ่ + รูปลูกค้า"),
    ("reviews-band", "section", "Reviews พื้นสีหลัก", "etch-sections/main-reviews-band.etch.txt",
     "3 รีวิว บนสีหลัก"),
    ("reviews-split", "section", "Reviews คะแนน + รีวิว", "etch-sections/main-reviews-split.etch.txt",
     "คะแนน 4.9 ซ้าย · 4 รีวิวขวา"),
    ("faq", "section", "FAQ", "etch-sections/main-faq.etch.txt", "คำถามเปิด/ปิดได้"),
    ("cta", "section", "CTA ติดต่อ", "etch-sections/main-cta.etch.txt", "component · ข้อมูลติดต่อ + แผนที่"),
    ("contact", "section", "Contact", "etch-sections/main-contact.etch.txt", "component · หน้าติดต่อ"),
    ("blog", "section", "Blog", "etch-sections/main-blog.etch.txt", "การ์ดบทความ + เลขหน้า"),
    ("single-post", "section", "บทความเดี่ยว", "etch-sections/main-single-post.etch.txt", "template Single"),
    ("404", "section", "404", "etch-sections/main-404.etch.txt", "template 404"),
    ("footer", "footer", "Footer", "etch-footer/main-footer.etch.txt", "component · โลโก้ · เมนู · บริการ · ติดต่อ"),
    ("footer-light", "footer", "Footer พื้นสว่าง", "etch-footer/main-footer-light.etch.txt",
     "พื้นสีอ่อน · ตัวอักษรเข้ม"),
    ("footer-center", "footer", "Footer กึ่งกลาง", "etch-footer/main-footer-center.etch.txt",
     "โลโก้ · เมนูแนวนอน · ติดต่อ · social อยู่กลาง"),
    ("footer-map", "footer", "Footer + แผนที่", "etch-footer/main-footer-map.etch.txt",
     "แผนที่ Google แทนคอลัมน์บริการ"),
    ("footer-compact", "footer", "Footer แถวเดียว", "etch-footer/main-footer-compact.etch.txt",
     "โลโก้ · เมนู · social ในแถวเดียว"),
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
PLACE.update({tid: PLACE["footer"] for tid, group, *_ in CATALOG if group == "footer"})

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


ASSEMBLE = """
<script>
/* ?t=header,hero,footer → stamp those templates here, in that order (default: header + every section + footer) */
(function () {
  var q = new URLSearchParams(location.search).get('t');
  var ids = q ? q.split(',') : Array.prototype.map.call(document.querySelectorAll('template[id^="tpl-"]'),
    function (t) { return t.id.slice(4); }).filter(function (id) { return !/^(header|footer)-/.test(id); }); // one header, one footer
  var here = document.currentScript;
  ids.forEach(function (id, i) {
    var t = document.getElementById('tpl-' + id);
    if (!t) return;
    var part = t.content.cloneNode(true);
    // frame.js applies the builder's edits per stamped template (?pb=)
    Array.prototype.forEach.call(part.children, function (el) { el.setAttribute('data-pv-inst', i); });
    here.parentNode.insertBefore(part, here);
  });
})();
</script>"""


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

    bodies, all_styles, all_scripts = [], {}, {}
    for tid, group, label, path, note in CATALOG:
        raw = open(os.path.join(ROOT, path), encoding="utf-8").read()
        payload = json.loads(raw)
        kit["templates"].append({"id": tid, "group": group, "label": label, "note": note,
                                 "file": os.path.basename(path), "payload": payload})
        body, css, scripts = render(payload)
        bodies.append((tid, body))
        for st in payload["styles"].values():  # the audit guarantees one CSS per selector across files
            all_styles.setdefault((st["type"], st["selector"], st["css"]), st)
        for code in scripts:
            all_scripts.setdefault(code, None)
        js = "\n".join(f'<script type="module">\n{s}\n</script>' for s in scripts)
        write(os.path.join(preview, f"{tid}.html"),
              PAGE.format(title=html.escape(label), css=css, id=tid, body=body, scripts=js))
        data["templates"].append({"id": tid, "group": group, "label": label, "note": note, "place": PLACE.get(tid, ""),
                                  "file": os.path.basename(path), "path": path, "preview": f"../preview/{tid}.html",
                                  "etch": raw})

    # one page with every template kept in <template>; a small script stamps the ones named in ?t= in order
    tpls = "\n".join(f'<template id="tpl-{tid}">{body}</template>' for tid, body in bodies)
    css = compile_css({str(i): st for i, st in enumerate(all_styles.values())})
    js = "\n".join(f'<script type="module">\n{code}\n</script>' for code in all_scripts)
    write(os.path.join(preview, "page.html"), PAGE.format(title="Page", css=css, id="page", body=tpls + ASSEMBLE,
                                                         scripts=js))
    data["page"] = "../preview/page.html"

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
