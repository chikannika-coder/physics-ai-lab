"""fix_duplicates.py - ลบสมการซ้ำ + แก้ key"""
from pathlib import Path
import json

R = Path(__file__).parent
KB = R / "physics_knowledge.json"
APP = R / "physics_ai_app_v5.py"

# ============================================================
# 1. ลบสมการที่ id ซ้ำใน KB
# ============================================================
if KB.exists():
    with open(KB, "r", encoding="utf-8") as f:
        kb = json.load(f)

    seen = set()
    unique = []
    removed = 0
    for eq in kb.get("equations", []):
        eid = eq.get("id", "")
        if eid in seen:
            removed += 1
            print(f"  [DEL] ซ้ำ: {eid} - {eq.get('name_th', '')}")
        else:
            seen.add(eid)
            unique.append(eq)

    kb["equations"] = unique
    with open(KB, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    print(f"[OK] ลบสมการซ้ำ {removed} รายการ (เหลือ {len(unique)})")

# ============================================================
# 2. แก้ key ของปุ่มลบให้ unique (ใช้ index)
# ============================================================
if APP.exists():
    c = APP.read_text(encoding="utf-8")

    # แก้ใน loop ของ "ดูสมการ" tab
    OLD = '''        for eq in filtered:
            with st.expander(f"**{eq['name_th']}** — {eq['name_en']}"):'''
    NEW = '''        for _idx, eq in enumerate(filtered):
            with st.expander(f"**{eq['name_th']}** — {eq['name_en']}"):'''

    if OLD in c:
        c = c.replace(OLD, NEW)
        print("[OK] เพิ่ม index ใน loop")

    OLD_BTN = '''if st.button(f"🗑️ ลบ", key=f"del_{eq['id']}"):'''
    NEW_BTN = '''if st.button(f"🗑️ ลบ", key=f"del_{_idx}_{eq.get('id','')}"):'''

    if OLD_BTN in c:
        c = c.replace(OLD_BTN, NEW_BTN)
        print("[OK] แก้ key ของปุ่มลบ")

    # 3. เพิ่มการตรวจ ID ซ้ำตอนเพิ่มสมการ
    OLD_ADD = '''                    kb["equations"].append({
                        "id": i, "name_th": nth, "name_en": nen,
                        "latex": lx, "formula": fm,
                        "variables": json.loads(vj),
                        "category": cat, "level": lv, "domain": [cat],
                    })'''
    NEW_ADD = '''                    # ตรวจ ID ซ้ำ
                    if any(e.get("id") == i for e in kb["equations"]):
                        st.error(f"ID '{i}' มีอยู่แล้ว — ใช้ชื่ออื่น")
                    else:
                        kb["equations"].append({
                            "id": i, "name_th": nth, "name_en": nen,
                            "latex": lx, "formula": fm,
                            "variables": json.loads(vj),
                            "category": cat, "level": lv, "domain": [cat],
                        })'''

    if OLD_ADD in c:
        c = c.replace(OLD_ADD, NEW_ADD)
        print("[OK] เพิ่มการตรวจ ID ซ้ำ")

    APP.write_text(c, encoding="utf-8")
    print(f"[OK] บันทึก: {APP}")

print()
print("=" * 60)
print("ขั้นตอนต่อไป:")
print("  1. Ctrl+C ปิด Streamlit")
print("  2. py -3 -m streamlit run physics_ai_app_v5.py")
print("  3. Refresh browser (F5)")