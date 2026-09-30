"""
physics_symbolic.py v3 — Symbolic Regression ฉบับสมบูรณ์
แก้ warning: deterministic=True, parallelism='serial'
ใช้ชื่อตัวแปรจริง: variable_names=features
iterations boost สำหรับสมการยกกำลัง
"""
import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent / "physics_ai_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# Dataset generators
# ============================================================
def gen_pendulum(n=200, noise=0.02, seed=42):
    rng = np.random.default_rng(seed)
    L = rng.uniform(0.1, 1.5, n)
    T = 2 * np.pi * np.sqrt(L / 9.81) + rng.normal(0, noise, n)
    return L.reshape(-1, 1), T, ["L"], "T"

def gen_projectile(n=200, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    v0 = rng.uniform(5, 30, n)
    theta = np.deg2rad(45)
    h = v0**2 * np.sin(theta)**2 / (2 * 9.81) + rng.normal(0, noise, n)
    return v0.reshape(-1, 1), h, ["v0"], "h"

def gen_ohm(n=200, noise=0.02, seed=42):
    rng = np.random.default_rng(seed)
    R = rng.uniform(10, 1000, n)
    I = rng.uniform(0.01, 2.0, n)
    V = I * R + rng.normal(0, noise, n)
    return np.column_stack([I, R]), V, ["I", "R"], "V"

def gen_coulomb(n=200, noise=0.01, seed=42):
    rng = np.random.default_rng(seed)
    k = 8.99e9
    q1 = rng.uniform(1e-6, 1e-4, n)
    q2 = rng.uniform(1e-6, 1e-4, n)
    r = rng.uniform(0.1, 1.0, n)
    F = k * q1 * q2 / r**2 + rng.normal(0, noise, n)
    return np.column_stack([q1, q2, r]), F, ["q1", "q2", "r"], "F"

def gen_hooke(n=200, noise=0.05, seed=42):
    rng = np.random.default_rng(seed)
    k = rng.uniform(10, 200, n)
    x = rng.uniform(0.01, 0.5, n)
    F = -k * x + rng.normal(0, noise, n)
    return np.column_stack([k, x]), F, ["k", "x"], "F"

def gen_kinetic(n=200, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    m = rng.uniform(0.1, 10, n)
    v = rng.uniform(1, 30, n)
    KE = 0.5 * m * v**2 + rng.normal(0, noise, n)
    return np.column_stack([m, v]), KE, ["m", "v"], "KE"

def gen_heat_conduction(n=200, noise=0.1, seed=42):
    rng = np.random.default_rng(seed)
    k = rng.uniform(0.1, 400, n)
    A = rng.uniform(0.01, 1.0, n)
    dT = rng.uniform(10, 200, n)
    L = rng.uniform(0.01, 0.5, n)
    Q = k * A * dT / L + rng.normal(0, noise, n)
    return np.column_stack([k, A, dT, L]), Q, ["k", "A", "dT", "L"], "Q"

def gen_ideal_gas(n=200, noise=1.0, seed=42):
    rng = np.random.default_rng(seed)
    R = 8.314
    n_mol = rng.uniform(0.1, 5.0, n)
    T = rng.uniform(200, 500, n)
    V = rng.uniform(0.001, 0.1, n)
    P = n_mol * R * T / V + rng.normal(0, noise, n)
    return np.column_stack([n_mol, T, V]), P, ["n", "T", "V"], "P"

def gen_wave_speed(n=200, noise=0.05, seed=42):
    rng = np.random.default_rng(seed)
    f = rng.uniform(1, 100, n)
    lam = rng.uniform(0.1, 10, n)
    v = f * lam + rng.normal(0, noise, n)
    return np.column_stack([f, lam]), v, ["f", "lam"], "v"

def gen_rc_time(n=200, noise=0.001, seed=42):
    rng = np.random.default_rng(seed)
    R = rng.uniform(100, 1e6, n)
    C = rng.uniform(1e-9, 1e-3, n)
    tau = R * C + rng.normal(0, noise, n)
    return np.column_stack([R, C]), tau, ["R", "C"], "tau"

def gen_stefan(n=200, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    sigma = 5.67e-8
    A = rng.uniform(0.01, 5.0, n)
    T = rng.uniform(200, 1000, n)
    P = sigma * A * T**4 + rng.normal(0, noise, n)
    return np.column_stack([A, T]), P, ["A", "T"], "P"

DATASETS = {
    "pendulum":        {"gen": gen_pendulum,        "name_th": "ลูกตุ้ม",             "niter_boost": 80},
    "projectile":      {"gen": gen_projectile,      "name_th": "โพรเจกไทล์",         "niter_boost": 80},
    "ohm":             {"gen": gen_ohm,             "name_th": "กฎโอห์ม",             "niter_boost": 60},
    "coulomb":         {"gen": gen_coulomb,         "name_th": "กฎคูลอมบ์",           "niter_boost": 150},
    "hooke":           {"gen": gen_hooke,           "name_th": "กฎฮุก",               "niter_boost": 60},
    "kinetic_energy":  {"gen": gen_kinetic,         "name_th": "พลังงานจลน์",         "niter_boost": 100},
    "heat_conduction": {"gen": gen_heat_conduction, "name_th": "การนำความร้อน",      "niter_boost": 150},
    "ideal_gas":       {"gen": gen_ideal_gas,       "name_th": "แก๊สอุดมคติ",         "niter_boost": 150},
    "wave_speed":      {"gen": gen_wave_speed,      "name_th": "ความเร็วคลื่น",      "niter_boost": 60},
    "rc_time":         {"gen": gen_rc_time,         "name_th": "เวลา RC",             "niter_boost": 60},
    "stefan":          {"gen": gen_stefan,          "name_th": "สเตฟาน-โบลต์ซมันน์",  "niter_boost": 250},
}

# ============================================================
# Discovery
# ============================================================
def discover(dataset_key):
    cfg = DATASETS[dataset_key]
    X, y, features, target = cfg["gen"]()

    try:
        from pysr import PySRRegressor
        use_pysr = True
    except ImportError:
        use_pysr = False
        print("  [WARN] PySR not installed -> demo mode")

    if use_pysr:
        model = PySRRegressor(
            niterations=cfg["niter_boost"],
            binary_operators=["+", "-", "*", "/"],
            unary_operators=["sqrt", "square", "cube", "exp", "log", "sin", "cos"],
            maxsize=18,
            random_state=42,
            deterministic=True,
            parallelism="serial",
            variable_names=features,
            verbosity=0,
        )
        model.fit(X, y)
        best = model.get_best()
        y_pred = model.predict(X)
        r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - y.mean())**2)

        return {
            "dataset": dataset_key,
            "name": cfg["name_th"],
            "equation": str(best["equation"]),
            "latex": best.get("latex", ""),
            "r2": float(r2),
            "complexity": int(best["complexity"]),
            "features": features,
            "target": target,
        }
    else:
        demo_eqs = {
            "pendulum": "2*pi*sqrt(L/g)",
            "projectile": "v0**2*sin(theta)**2/(2*g)",
            "ohm": "I*R",
            "coulomb": "k*q1*q2/r**2",
            "hooke": "-k*x",
            "kinetic_energy": "0.5*m*v**2",
            "heat_conduction": "k*A*dT/L",
            "ideal_gas": "n*R*T/V",
            "wave_speed": "f*lam",
            "rc_time": "R*C",
            "stefan": "sigma*A*T**4",
        }
        return {
            "dataset": dataset_key,
            "name": cfg["name_th"],
            "equation": demo_eqs.get(dataset_key, "?"),
            "latex": "",
            "r2": 0.99,
            "complexity": 5,
            "features": features,
            "target": target,
            "note": "DEMO (no PySR)",
        }

# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("=" * 70)
    print("  Symbolic Regression v3 — 11 สมการฟิสิกส์")
    print("=" * 70)

    results = []
    for key in DATASETS:
        print(f"\n[{key}] {DATASETS[key]['name_th']}...")
        result = discover(key)
        print(f"  สมการ: {result['equation']}")
        print(f"  R²: {result['r2']:.4f}")
        results.append(result)

    df = pd.DataFrame(results)
    out = OUTPUT_DIR / "discovered_equations.csv"
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"\n[OK] บันทึกที่: {out}")

    # อัปเดต KB
    try:
        from physics_knowledge import load_kb, save_kb
        kb = load_kb()
        kb.setdefault("discoveries", []).append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "results": results,
        })
        save_kb(kb)
        print("[OK] อัปเดต Knowledge Base")
    except Exception as e:
        print(f"[WARN] {e}")
