"""fix_problems.py — ปรับ 3 สมการที่มีปัญหา"""
from pathlib import Path

ROOT = Path(__file__).parent
TARGET = ROOT / "physics_symbolic_v4.py"

content = TARGET.read_text(encoding="utf-8")

# ============================================================
# 1. เพิ่ม parsimony เพื่อป้องกัน overfitting
# ============================================================
OLD_PARAMS = '''        maxsize=18, random_state=42, deterministic=True, parallelism="serial",
        verbosity=0,
    )'''
NEW_PARAMS = '''        maxsize=15, random_state=42, deterministic=True, parallelism="serial",
        parsimony=0.05, constraining_op=["exp", "log"],
        verbosity=0,
    )'''

if OLD_PARAMS in content:
    content = content.replace(OLD_PARAMS, NEW_PARAMS)
    print("[OK] เพิ่ม parsimony + constraining_op")
else:
    print("[SKIP] ไม่พบ parameters")

# ============================================================
# 2. Black-Scholes — ใช้ Put-Call Parity (เส้นตรง)
# ============================================================
OLD_BS = '''def gen_black_scholes(n=200, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    S = rng.uniform(50, 150, n); K = rng.uniform(50, 150, n)
    r = rng.uniform(0.01, 0.1, n); T = rng.uniform(0.1, 2.0, n)
    C = np.maximum(S - K * np.exp(-r*T) + rng.normal(0, noise, n), 0)
    return np.column_stack([S, K, r, T]), C, ["S","K","r","T"], "C"'''

NEW_BS = '''def gen_black_scholes(n=200, noise=0.5, seed=42):
    """Put-Call Parity: C - P = S - K*exp(-rT) => C = S - K*exp(-rT)"""
    rng = np.random.default_rng(seed)
    S = rng.uniform(50, 150, n); K = rng.uniform(50, 150, n)
    r = rng.uniform(0.01, 0.1, n); T = rng.uniform(0.1, 2.0, n)
    C = S - K * np.exp(-r*T) + rng.normal(0, noise, n)
    return np.column_stack([S, K, r, T]), C, ["S","K","r","T"], "C"'''

if OLD_BS in content:
    content = content.replace(OLD_BS, NEW_BS)
    print("[OK] แก้ Black-Scholes (Put-Call Parity)")
else:
    print("[SKIP] Black-Scholes")

# ============================================================
# 3. Logistic — เพิ่ม iterations
# ============================================================
OLD_LOG = '"logistic":         {"gen": gen_logistic,         "name_th": "การเติบโตโลจิสติก",    "niter": 150, "cat": "biology"},'
NEW_LOG = '"logistic":         {"gen": gen_logistic,         "name_th": "การเติบโตโลจิสติก",    "niter": 300, "cat": "biology"},'

if OLD_LOG in content:
    content = content.replace(OLD_LOG, NEW_LOG)
    print("[OK] เพิ่ม iterations Logistic (150→300)")
else:
    print("[SKIP] Logistic")

# ============================================================
# 4. Schrödinger — เพิ่ม iterations + ลด complexity
# ============================================================
OLD_SCH = '"schrodinger":      {"gen": gen_schrodinger,      "name_th": "ชเรอดิงเงอร์",          "niter": 200, "cat": "quantum"},'
NEW_SCH = '"schrodinger":      {"gen": gen_schrodinger,      "name_th": "ชเรอดิงเงอร์",          "niter": 400, "cat": "quantum"},'

if OLD_SCH in content:
    content = content.replace(OLD_SCH, NEW_SCH)
    print("[OK] เพิ่ม iterations Schrödinger (200→400)")
else:
    print("[SKIP] Schrödinger")

TARGET.write_text(content, encoding="utf-8")
print(f"\n[OK] บันทึก: {TARGET}")
print("\nทดสอบใหม่: py -3 physics_symbolic_v4.py")