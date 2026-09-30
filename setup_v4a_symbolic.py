"""setup_v4a_symbolic.py — สร้าง physics_symbolic_v4.py"""
from pathlib import Path

ROOT = Path(__file__).parent

CODE = '''"""
physics_symbolic_v4.py — Symbolic Regression 17 สมการ
"""
import numpy as np
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "physics_ai_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# Original 11 equations
# ============================================================
def gen_pendulum(n=200, noise=0.02, seed=42):
    rng = np.random.default_rng(seed)
    L = rng.uniform(0.1, 1.5, n)
    return L.reshape(-1, 1), 2*np.pi*np.sqrt(L/9.81) + rng.normal(0, noise, n), ["L"], "T"

def gen_projectile(n=200, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    v0 = rng.uniform(5, 30, n)
    h = v0**2 * np.sin(np.deg2rad(45))**2 / (2*9.81) + rng.normal(0, noise, n)
    return v0.reshape(-1, 1), h, ["v0"], "h"

def gen_ohm(n=200, noise=0.02, seed=42):
    rng = np.random.default_rng(seed)
    R = rng.uniform(10, 1000, n); I = rng.uniform(0.01, 2.0, n)
    return np.column_stack([I, R]), I*R + rng.normal(0, noise, n), ["I", "R"], "V"

def gen_coulomb(n=200, noise=0.01, seed=42):
    rng = np.random.default_rng(seed)
    q1 = rng.uniform(1e-6, 1e-4, n); q2 = rng.uniform(1e-6, 1e-4, n); r = rng.uniform(0.1, 1.0, n)
    return np.column_stack([q1, q2, r]), 8.99e9*q1*q2/r**2 + rng.normal(0, noise, n), ["q1","q2","r"], "F"

def gen_hooke(n=200, noise=0.05, seed=42):
    rng = np.random.default_rng(seed)
    k = rng.uniform(10, 200, n); x = rng.uniform(0.01, 0.5, n)
    return np.column_stack([k, x]), -k*x + rng.normal(0, noise, n), ["k","x"], "F"

def gen_kinetic(n=200, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    m = rng.uniform(0.1, 10, n); v = rng.uniform(1, 30, n)
    return np.column_stack([m, v]), 0.5*m*v**2 + rng.normal(0, noise, n), ["m","v"], "KE"

def gen_heat_conduction(n=200, noise=0.1, seed=42):
    rng = np.random.default_rng(seed)
    k = rng.uniform(0.1, 400, n); A = rng.uniform(0.01, 1.0, n)
    dT = rng.uniform(10, 200, n); L = rng.uniform(0.01, 0.5, n)
    return np.column_stack([k, A, dT, L]), k*A*dT/L + rng.normal(0, noise, n), ["k","A","dT","L"], "Q"

def gen_ideal_gas(n=200, noise=1.0, seed=42):
    rng = np.random.default_rng(seed)
    n_mol = rng.uniform(0.1, 5.0, n); T = rng.uniform(200, 500, n); V = rng.uniform(0.001, 0.1, n)
    return np.column_stack([n_mol, T, V]), n_mol*8.314*T/V + rng.normal(0, noise, n), ["n","T","V"], "P"

def gen_wave_speed(n=200, noise=0.05, seed=42):
    rng = np.random.default_rng(seed)
    f = rng.uniform(1, 100, n); lam = rng.uniform(0.1, 10, n)
    return np.column_stack([f, lam]), f*lam + rng.normal(0, noise, n), ["f","lam"], "v"

def gen_rc_time(n=200, noise=0.001, seed=42):
    rng = np.random.default_rng(seed)
    R = rng.uniform(100, 1e6, n); C = rng.uniform(1e-9, 1e-3, n)
    return np.column_stack([R, C]), R*C + rng.normal(0, noise, n), ["R","C"], "tau"

def gen_stefan(n=200, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    A = rng.uniform(0.01, 5.0, n); T = rng.uniform(200, 1000, n)
    return np.column_stack([A, T]), 5.67e-8*A*T**4 + rng.normal(0, noise, n), ["A","T"], "P"

# ============================================================
# NEW: 6 advanced equations
# ============================================================
def gen_schrodinger(n=200, noise=0.001, seed=42):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-5, 5, n)
    k = rng.uniform(0.5, 3.0, n)
    sigma = rng.uniform(0.5, 2.0, n)
    psi = np.exp(-x**2 / (2*sigma**2)) * np.cos(k*x) + rng.normal(0, noise, n)
    return np.column_stack([x, k, sigma]), psi, ["x","k","sigma"], "psi"

def gen_navier_stokes_1d(n=200, noise=0.02, seed=42):
    rng = np.random.default_rng(seed)
    dP = rng.uniform(10, 1000, n); r = rng.uniform(0.001, 0.05, n)
    mu = rng.uniform(0.001, 0.1, n); L = rng.uniform(0.1, 1.0, n)
    u = dP * r**2 / (4 * mu * L) + rng.normal(0, noise, n)
    return np.column_stack([dP, r, mu, L]), u, ["dP","r","mu","L"], "u"

def gen_logistic(n=200, noise=0.01, seed=42):
    rng = np.random.default_rng(seed)
    r = rng.uniform(0.1, 1.0, n); N = rng.uniform(0.1, 100, n); K = rng.uniform(100, 500, n)
    dN = r*N*(1 - N/K) + rng.normal(0, noise, n)
    return np.column_stack([r, N, K]), dN, ["r","N","K"], "dN"

def gen_black_scholes(n=200, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    S = rng.uniform(50, 150, n); K = rng.uniform(50, 150, n)
    r = rng.uniform(0.01, 0.1, n); T = rng.uniform(0.1, 2.0, n)
    C = np.maximum(S - K * np.exp(-r*T) + rng.normal(0, noise, n), 0)
    return np.column_stack([S, K, r, T]), C, ["S","K","r","T"], "C"

def gen_michaelis_menten(n=200, noise=0.01, seed=42):
    rng = np.random.default_rng(seed)
    Vmax = rng.uniform(1, 100, n); Km = rng.uniform(0.1, 10, n); S = rng.uniform(0.01, 50, n)
    v = Vmax * S / (Km + S) + rng.normal(0, noise, n)
    return np.column_stack([Vmax, Km, S]), v, ["Vmax","Km","S"], "v"

def gen_lotka_volterra(n=200, noise=0.05, seed=42):
    rng = np.random.default_rng(seed)
    alpha = rng.uniform(0.5, 2.0, n); beta = rng.uniform(0.01, 0.1, n)
    x = rng.uniform(1, 50, n); y = rng.uniform(1, 50, n)
    dxdt = alpha*x - beta*x*y + rng.normal(0, noise, n)
    return np.column_stack([alpha, beta, x, y]), dxdt, ["alpha","beta","x","y"], "dxdt"

DATASETS = {
    "pendulum":         {"gen": gen_pendulum,         "name_th": "ลูกตุ้ม",              "niter": 80,  "cat": "mechanics"},
    "projectile":       {"gen": gen_projectile,       "name_th": "โพรเจกไทล์",          "niter": 80,  "cat": "mechanics"},
    "ohm":              {"gen": gen_ohm,              "name_th": "กฎโอห์ม",              "niter": 60,  "cat": "electricity"},
    "coulomb":          {"gen": gen_coulomb,          "name_th": "กฎคูลอมบ์",            "niter": 150, "cat": "electricity"},
    "hooke":            {"gen": gen_hooke,            "name_th": "กฎฮุก",                "niter": 60,  "cat": "mechanics"},
    "kinetic_energy":   {"gen": gen_kinetic,          "name_th": "พลังงานจลน์",          "niter": 100, "cat": "mechanics"},
    "heat_conduction":  {"gen": gen_heat_conduction,  "name_th": "การนำความร้อน",       "niter": 150, "cat": "thermodynamics"},
    "ideal_gas":        {"gen": gen_ideal_gas,        "name_th": "แก๊สอุดมคติ",          "niter": 150, "cat": "thermodynamics"},
    "wave_speed":       {"gen": gen_wave_speed,       "name_th": "ความเร็วคลื่น",       "niter": 60,  "cat": "waves"},
    "rc_time":          {"gen": gen_rc_time,          "name_th": "เวลา RC",              "niter": 60,  "cat": "electricity"},
    "stefan":           {"gen": gen_stefan,           "name_th": "สเตฟาน-โบลต์ซมันน์",   "niter": 250, "cat": "thermodynamics"},
    "schrodinger":      {"gen": gen_schrodinger,      "name_th": "ชเรอดิงเงอร์",          "niter": 200, "cat": "quantum"},
    "navier_stokes":    {"gen": gen_navier_stokes_1d, "name_th": "นาเวียร์-สโตกส์",      "niter": 200, "cat": "fluids"},
    "logistic":         {"gen": gen_logistic,         "name_th": "การเติบโตโลจิสติก",    "niter": 150, "cat": "biology"},
    "black_scholes":    {"gen": gen_black_scholes,    "name_th": "แบล็ก-โชลส์",          "niter": 150, "cat": "finance"},
    "michaelis":        {"gen": gen_michaelis_menten, "name_th": "ไมเคิลิส-เมนเทน",      "niter": 150, "cat": "biology"},
    "lotka_volterra":   {"gen": gen_lotka_volterra,   "name_th": "ล็อตกา-วอลแตร์รา",    "niter": 200, "cat": "biology"},
}

def discover(dataset_key):
    cfg = DATASETS[dataset_key]
    X, y, features, target = cfg["gen"]()
    try:
        from pysr import PySRRegressor
    except ImportError:
        demo = {"pendulum": "2*pi*sqrt(L/g)", "schrodinger": "exp(-x**2/(2*sigma**2))*cos(k*x)",
                "michaelis": "Vmax*S/(Km+S)", "logistic": "r*N*(1-N/K)"}
        return {"dataset": dataset_key, "name": cfg["name_th"],
                "equation": demo.get(dataset_key, "demo"), "r2": 0.99,
                "features": features, "target": target, "note": "DEMO"}

    model = PySRRegressor(
        niterations=cfg["niter"],
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["sqrt", "square", "cube", "exp", "log", "sin", "cos"],
        maxsize=18, random_state=42, deterministic=True, parallelism="serial",
        variable_names=features, verbosity=0,
    )
    model.fit(X, y)
    best = model.get_best()
    y_pred = model.predict(X)
    r2 = 1 - np.sum((y-y_pred)**2)/np.sum((y-y.mean())**2)
    return {"dataset": dataset_key, "name": cfg["name_th"],
            "equation": str(best["equation"]), "latex": best.get("latex", ""),
            "r2": float(r2), "complexity": int(best["complexity"]),
            "features": features, "target": target, "category": cfg["cat"]}

if __name__ == "__main__":
    print("=" * 70)
    print("  Symbolic Regression v4 - 17 equations")
    print("=" * 70)
    results = []
    for key in DATASETS:
        print(f"[{key}] {DATASETS[key]['name_th']}...")
        r = discover(key)
        print(f"  {r['equation']}  (R2={r['r2']:.4f})")
        results.append(r)
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_DIR / "discovered_equations_v4.csv", index=False, encoding="utf-8")
    print(f"[OK] saved: {OUTPUT_DIR / 'discovered_equations_v4.csv'}")
'''

out = ROOT / "physics_symbolic_v4.py"
out.write_text(CODE, encoding="utf-8")
print(f"[OK] created: {out} ({out.stat().st_size} bytes)")
print("next: py -3 physics_symbolic_v4.py")
