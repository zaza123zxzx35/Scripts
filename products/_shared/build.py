#!/usr/bin/env python3
"""
ประกอบไฟล์ที่พร้อมใช้งานทั้งหมดจากไลบรารีกลาง — VIP English Hub

ทำไมต้องมีสคริปต์นี้
  ตัวละครและอนิเมชันถูกฝังลงในทุกไฟล์ที่ส่งมอบ เพราะเกมและใบงานต้องเป็น
  ไฟล์เดียวจบที่เปิดได้โดยไม่ต้องมีอะไรอีก แต่ถ้าแก้ไลบรารีกลางแล้วลืมประกอบใหม่
  ไฟล์ที่ส่งมอบจะค้างอยู่ที่เวอร์ชันเก่าโดยไม่มีใครรู้ สคริปต์นี้ตัดปัญหานั้นทิ้ง

วิธีใช้
  python3 products/_shared/build.py

เพิ่มใบงานใหม่
  1. สร้างไฟล์เนื้อหาที่ products/<หน่วย>/worksheets/src/<รหัสไฟล์>.part.html
     บรรทัดแรกใส่  <!--TITLE: ชื่อที่จะขึ้นบนแถบควบคุม -->
  2. รันสคริปต์นี้ ไฟล์ที่พร้อมพิมพ์จะถูกสร้างขึ้นหนึ่งระดับเหนือโฟลเดอร์ src
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SHARED = os.path.join(ROOT, "products", "_shared")
TPL = os.path.join(SHARED, "templates")

C0 = "<!-- ================= CONTENT START ================= -->"
C1 = "<!-- ================= CONTENT END ================= -->"


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("  สร้าง %s (%d KB)" % (os.path.relpath(path, ROOT), len(text.encode()) // 1024))


def main():
    sprite = read(os.path.join(SHARED, "animal-sprite.svg")).strip()
    motion = read(os.path.join(SHARED, "motion-kit.css")).strip()
    ws_tpl = read(os.path.join(TPL, "worksheet.tpl.html"))
    game_tpl = read(os.path.join(TPL, "game.tpl.html"))

    print("สื่อ Interactive")
    write(
        os.path.join(ROOT, "products", "G1-U05-Animals", "interactive", "index.html"),
        game_tpl.replace("__SPRITE__", sprite).replace("__MOTION__", motion),
    )

    print("เทมเพลตใบงานแม่แบบ")
    demo = read(os.path.join(TPL, "worksheet-demo.part.html")).strip()
    write(
        os.path.join(SHARED, "worksheet-template.html"),
        ws_tpl.replace("__SPRITE__", sprite).replace("__CONTENT__", demo),
    )

    print("ใบงาน")
    parts = sorted(glob.glob(os.path.join(ROOT, "products", "*", "worksheets", "src", "*.part.html")))
    if not parts:
        print("  ยังไม่มีไฟล์เนื้อหาใบงานใน src")
    for part_path in parts:
        raw = read(part_path)
        m = re.match(r"\s*<!--TITLE:\s*(.*?)\s*-->\s*", raw)
        title = m.group(1) if m else os.path.basename(part_path)
        body = raw[m.end():] if m else raw
        out = (
            ws_tpl.replace("__SPRITE__", sprite)
            .replace("__CONTENT__", body.strip())
            .replace(
                '<span id="bar-title">เทมเพลตแม่แบบ</span>',
                '<span id="bar-title">%s</span>' % title,
            )
        )
        name = os.path.basename(part_path).replace(".part.html", ".html")
        write(os.path.join(os.path.dirname(os.path.dirname(part_path)), name), out)

    print("\nเสร็จแล้ว ทุกไฟล์ที่ส่งมอบตรงกับไลบรารีกลางเวอร์ชันล่าสุด")
    return 0


if __name__ == "__main__":
    sys.exit(main())
