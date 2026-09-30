"""fix_params.py — ลบ constraining_op ที่ผิด"""
from pathlib import Path

ROOT = Path(__file__).parent
TARGET = ROOT / "physics_symbolic_v4.py"

content = TARGET.read_text(encoding="utf-8")

# ลบ constraining_op ออก
OLD = "        parsimony=0.05, constraining_op=[\"exp\", \"log\"],\n"
NEW = "        parsimony=0.01,\n"

if OLD in content:
    content = content.replace(OLD, NEW)
    print("[OK] ลบ constraining_op, parsimony -> 0.01")
else:
    print("[SKIP] ไม่พบ constraining_op")
    # ลองหาแบบอื่น
    if "constraining_op" in content:
        import re
        content = re.sub(r"constraining_op=\[[^\]]*\],?\s*", "", content)
        content = content.replace("parsimony=0.05", "parsimony=0.01")
        print("[OK] ลบด้วย regex")

TARGET.write_text(content, encoding="utf-8")
print(f"[OK] บันทึก: {TARGET}")
print()
print("ทดสอบ: py -3 physics_symbolic_v4.py")