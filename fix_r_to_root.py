"""fix_r_to_root.py - แทน R ด้วย ROOT ใน physics_ai_app_v5.py"""
from pathlib import Path

R = Path(__file__).parent
TARGET = R / "physics_ai_app_v5.py"

if not TARGET.exists():
    print(f"[ERR] ไม่พบ {TARGET}")
    print("รัน setup_v5c_app.py ก่อน")
    exit(1)

c = TARGET.read_text(encoding="utf-8")

# แทน R / "uploads" → ROOT / "uploads"
old1 = 'R / "uploads"'
new1 = 'ROOT / "uploads"'

# นับ occurrences
count = c.count(old1)
if count > 0:
    c = c.replace(old1, new1)
    print(f"[OK] แทน R -> ROOT จำนวน {count} จุด")
else:
    print("[SKIP] ไม่พบ R / uploads")

TARGET.write_text(c, encoding="utf-8")
print(f"\n[OK] บันทึก: {TARGET}")
print("\nปิด Streamlit (Ctrl+C) แล้วเปิดใหม่:")
print("  py -3 -m streamlit run physics_ai_app_v5.py")