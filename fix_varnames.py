"""fix_varnames.py — แทนชื่อตัวแปรที่ชนกับ SymPy"""
from pathlib import Path

ROOT = Path(__file__).parent
TARGET = ROOT / "physics_symbolic_v4.py"

if not TARGET.exists():
    print(f"[ERR] ไม่พบ {TARGET}")
    exit(1)

content = TARGET.read_text(encoding="utf-8")

# เพิ่มฟังก์ชัน sanitize หลัง imports
SANITIZE_BLOCK = '''
# ============================================================
# Sanitize variable names (SymPy reserved: I, E, S, N, O, Q, pi, oo, nan, zoo)
# ============================================================
SYMPY_RESERVED = {"I", "E", "S", "N", "O", "Q", "pi", "oo", "nan", "zoo",
                  "beta", "gamma", "zeta", "lambda", "Alpha", "Beta",
                  "Gamma", "Delta", "Zeta", "Lambda", "Omega"}

def sanitize_features(features):
    """แทนชื่อที่ชนกับ SymPy ด้วย suffix _v"""
    return [f + "_v" if f in SYMPY_RESERVED else f for f in features]

'''

# แทรกหลัง imports (หลัง OUTPUT_DIR)
MARKER = 'OUTPUT_DIR.mkdir(exist_ok=True)\n'
if MARKER in content and "def sanitize_features" not in content:
    content = content.replace(MARKER, MARKER + SANITIZE_BLOCK, 1)
    print("[OK] เพิ่มฟังก์ชัน sanitize_features")

# แก้ใน discover: sanitize features ก่อน fit และตอน return
OLD_DISCOVER = '''def discover(dataset_key):
    cfg = DATASETS[dataset_key]
    X, y, features, target = cfg["gen"]()
    try:'''
NEW_DISCOVER = '''def discover(dataset_key):
    cfg = DATASETS[dataset_key]
    X, y, features, target = cfg["gen"]()
    safe_features = sanitize_features(features)
    try:'''
if OLD_DISCOVER in content:
    content = content.replace(OLD_DISCOVER, NEW_DISCOVER)
    print("[OK] แก้ discover() — sanitize features")

# แทน features -> safe_features ใน PySR fit
content = content.replace(
    "model.fit(X, y, variable_names=features)",
    "model.fit(X, y, variable_names=safe_features)"
)
print("[OK] แก้ model.fit() — ใช้ safe_features")

# แทน features -> safe_features ใน return dict
content = content.replace(
    '"features": features, "target": target, "note": "DEMO"}',
    '"features": safe_features, "target": target, "note": "DEMO"}'
)
content = content.replace(
    '"features": features, "target": target, "category": cfg["cat"]}',
    '"features": safe_features, "target": target, "category": cfg["cat"]}'
)
print("[OK] แก้ return dict — ใช้ safe_features")

TARGET.write_text(content, encoding="utf-8")
print(f"\n[OK] บันทึก: {TARGET}")
print("\nทดสอบ: py -3 physics_symbolic_v4.py")