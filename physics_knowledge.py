"""physics_knowledge.py — จัดการฐานความรู้ฟิสิกส์"""
import json
from pathlib import Path
from datetime import datetime

KB_FILE = Path(__file__).parent / "physics_knowledge.json"

def load_kb():
    if not KB_FILE.exists():
        return {"version": "0.0.0", "equations": [], "history": []}
    with open(KB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_kb(kb):
    kb["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(KB_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

def add_equation(eq_dict, note=""):
    kb = load_kb()
    if any(e["id"] == eq_dict["id"] for e in kb["equations"]):
        raise ValueError(f"id '{eq_dict['id']}' มีอยู่แล้ว")
    kb["equations"].append(eq_dict)
    kb["history"].append({"date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                          "action": "added", "id": eq_dict["id"],
                          "note": note or f"เพิ่ม {eq_dict['name_en']}"})
    save_kb(kb)
    return eq_dict

def update_equation(eq_id, updates, note=""):
    kb = load_kb()
    for eq in kb["equations"]:
        if eq["id"] == eq_id:
            eq.update(updates)
            kb["history"].append({"date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                  "action": "updated", "id": eq_id,
                                  "note": note or f"อัปเดต {eq_id}"})
            save_kb(kb)
            return eq
    raise ValueError(f"ไม่พบ id '{eq_id}'")

def delete_equation(eq_id, note=""):
    kb = load_kb()
    before = len(kb["equations"])
    kb["equations"] = [e for e in kb["equations"] if e["id"] != eq_id]
    if len(kb["equations"]) == before:
        raise ValueError(f"ไม่พบ id '{eq_id}'")
    kb["history"].append({"date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                          "action": "deleted", "id": eq_id,
                          "note": note or f"ลบ {eq_id}"})
    save_kb(kb)

def get_categories():
    kb = load_kb()
    return sorted(set(e.get("category", "other") for e in kb["equations"]))

if __name__ == "__main__":
    kb = load_kb()
    print(f"KB version: {kb['version']}")
    print(f"สมการ: {len(kb['equations'])}")
    print(f"หมวด: {get_categories()}")
