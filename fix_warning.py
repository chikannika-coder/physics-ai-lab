"""fix_warning.py — แก้ warning variable_names ใน physics_symbolic_v4.py"""
from pathlib import Path

ROOT = Path(__file__).parent
TARGET = ROOT / "physics_symbolic_v4.py"

if not TARGET.exists():
    print(f"[ERR] ไม่พบ: {TARGET}")
    print("กรุณารัน setup_v4a_symbolic.py ก่อน")
    exit(1)

content = TARGET.read_text(encoding="utf-8")

# แก้ 1: ลบ variable_names ออกจาก PySRRegressor(...)
OLD_1 = "        maxsize=18, random_state=42, deterministic=True, parallelism=\"serial\",\n        variable_names=features, verbosity=0,\n    )"
NEW_1 = "        maxsize=18, random_state=42, deterministic=True, parallelism=\"serial\",\n        verbosity=0,\n    )"

# แก้ 2: เพิ่ม variable_names ใน model.fit(X, y, ...)
OLD_2 = "    model.fit(X, y)"
NEW_2 = "    model.fit(X, y, variable_names=features)"

changes = 0

if OLD_1 in content:
    content = content.replace(OLD_1, NEW_1)
    print("[OK] แก้ PySRRegressor(...)")
    changes += 1
else:
    print("[SKIP] ไม่พบโค้ดส่วน PySRRegressor")

if OLD_2 in content:
    content = content.replace(OLD_2, NEW_2)
    print("[OK] แก้ model.fit(X, y)")
    changes += 1
else:
    print("[SKIP] ไม่พบโค้ด model.fit(X, y)")
    # ลองแบบมี variable_names อยู่แล้ว
    if "model.fit(X, y, variable_names=features)" in content:
        print("[INFO] ไฟล์นี้อัปเดตแล้ว")

if changes > 0:
    TARGET.write_text(content, encoding="utf-8")
    print(f"\n[OK] บันทึก: {TARGET}")
    print(f"[INFO] แก้ไขทั้งหมด {changes} จุด")
    print("\nขั้นต่อไป:")
    print("  py -3 physics_symbolic_v4.py")
else:
    print("\n[INFO] ไม่มีการเปลี่ยนแปลง")