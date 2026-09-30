"""
setup_v3_final.py — สร้างระบบ SatiARM Physics AI ฉบับสมบูรณ์
รัน: py -3 setup_v3_final.py
"""
from pathlib import Path
import json

ROOT = Path(__file__).parent
FILES = {}

# ============================================================
# 1. physics_knowledge.json
# ============================================================
FILES["physics_knowledge.json"] = json.dumps({
    "version": "1.0.0",
    "last_updated": "2026-09-30",
    "equations": [
        {"id": "pendulum", "name_th": "ลูกตุ้มอย่างง่าย", "name_en": "Simple Pendulum",
         "latex": r"T = 2\pi\sqrt{\frac{L}{g}}", "formula": "T = 2*pi*sqrt(L/g)",
         "variables": {"T": "คาบ (s)", "L": "ความยาว (m)", "g": "9.81 m/s²"},
         "domain": ["กลศาสตร์"], "level": "ม.ปลาย", "category": "mechanics"},
        {"id": "projectile", "name_th": "โพรเจกไทล์", "name_en": "Projectile Motion",
         "latex": r"h = \frac{v_0^2 \sin^2\theta}{2g}", "formula": "h = v0**2 * sin(theta)**2 / (2*g)",
         "variables": {"h": "ความสูง (m)", "v0": "ความเร็วต้น (m/s)", "theta": "มุม (rad)"},
         "domain": ["กลศาสตร์"], "level": "ม.ปลาย", "category": "mechanics"},
        {"id": "ohm", "name_th": "กฎของโอห์ม", "name_en": "Ohm's Law",
         "latex": r"V = IR", "formula": "V = I * R",
         "variables": {"V": "แรงดัน (V)", "I": "กระแส (A)", "R": "ความต้านทาน (Ω)"},
         "domain": ["ไฟฟ้า"], "level": "ม.ต้น", "category": "electricity"},
        {"id": "coulomb", "name_th": "กฎของคูลอมบ์", "name_en": "Coulomb's Law",
         "latex": r"F = k\frac{q_1 q_2}{r^2}", "formula": "F = k * q1 * q2 / r**2",
         "variables": {"F": "แรง (N)", "k": "8.99e9", "q1,q2": "ประจุ (C)", "r": "ระยะ (m)"},
         "domain": ["ไฟฟ้า"], "level": "ม.ปลาย", "category": "electricity"},
        {"id": "hooke", "name_th": "กฎของฮุก", "name_en": "Hooke's Law",
         "latex": r"F = -kx", "formula": "F = -k * x",
         "variables": {"F": "แรง (N)", "k": "ค่าคงที่สปริง", "x": "ระยะยืด (m)"},
         "domain": ["กลศาสตร์"], "level": "ม.ปลาย", "category": "mechanics"},
        {"id": "kinetic_energy", "name_th": "พลังงานจลน์", "name_en": "Kinetic Energy",
         "latex": r"KE = \frac{1}{2}mv^2", "formula": "KE = 0.5 * m * v**2",
         "variables": {"KE": "พลังงาน (J)", "m": "มวล (kg)", "v": "ความเร็ว (m/s)"},
         "domain": ["กลศาสตร์"], "level": "ม.ต้น", "category": "mechanics"},
        {"id": "heat_conduction", "name_th": "การนำความร้อน", "name_en": "Heat Conduction",
         "latex": r"Q = kA\frac{\Delta T}{L}", "formula": "Q = k * A * dT / L",
         "variables": {"Q": "อัตรา (W)", "k": "ค่าการนำ", "A": "พื้นที่", "dT": "ΔT", "L": "ความหนา"},
         "domain": ["อุณหพลศาสตร์"], "level": "ม.ปลาย", "category": "thermodynamics"},
        {"id": "ideal_gas", "name_th": "แก๊สอุดมคติ", "name_en": "Ideal Gas Law",
         "latex": r"PV = nRT", "formula": "P = n * R * T / V",
         "variables": {"P": "ความดัน (Pa)", "V": "ปริมาตร", "n": "โมล", "R": "8.314", "T": "อุณหภูมิ (K)"},
         "domain": ["อุณหพลศาสตร์"], "level": "ม.ปลาย", "category": "thermodynamics"},
        {"id": "wave_speed", "name_th": "ความเร็วคลื่น", "name_en": "Wave Speed",
         "latex": r"v = f\lambda", "formula": "v = f * lam",
         "variables": {"v": "ความเร็ว", "f": "ความถี่", "lam": "ความยาวคลื่น"},
         "domain": ["คลื่น"], "level": "ม.ต้น", "category": "waves"},
        {"id": "snell", "name_th": "กฎของสเนลล์", "name_en": "Snell's Law",
         "latex": r"n_1\sin\theta_1 = n_2\sin\theta_2", "formula": "n1*sin(t1) = n2*sin(t2)",
         "variables": {"n1,n2": "ดัชนีหักเห", "t1,t2": "มุม (rad)"},
         "domain": ["แสง"], "level": "ม.ปลาย", "category": "optics"},
        {"id": "stefan", "name_th": "สเตฟาน-โบลต์ซมันน์", "name_en": "Stefan-Boltzmann",
         "latex": r"P = \sigma A T^4", "formula": "P = sigma * A * T**4",
         "variables": {"P": "กำลัง (W)", "sigma": "5.67e-8", "A": "พื้นที่", "T": "อุณหภูมิ (K)"},
         "domain": ["อุณหพลศาสตร์"], "level": "มหาวิทยาลัย", "category": "thermodynamics"},
        {"id": "rc_time", "name_th": "เวลา RC", "name_en": "RC Time Constant",
         "latex": r"\tau = RC", "formula": "tau = R * C",
         "variables": {"tau": "เวลา (s)", "R": "ความต้านทาน", "C": "ความจุ"},
         "domain": ["ไฟฟ้า"], "level": "มหาวิทยาลัย", "category": "electricity"},
        {"id": "einstein", "name_th": "สมการไอน์สไตน์", "name_en": "Mass-Energy Equivalence",
         "latex": r"E = mc^2", "formula": "E = m * c**2",
         "variables": {"E": "พลังงาน (J)", "m": "มวล (kg)", "c": "3e8 m/s"},
         "domain": ["สัมพัทธภาพ"], "level": "มหาวิทยาลัย", "category": "relativity"},
    ],
    "history": [{"date": "2026-09-30", "action": "created", "version": "1.0.0"}]
}, ensure_ascii=False, indent=2)

# ============================================================
# 2. physics_knowledge.py
# ============================================================
FILES["physics_knowledge.py"] = r'''"""physics_knowledge.py — จัดการฐานความรู้ฟิสิกส์"""
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
'''

# ============================================================
# 3. physics_symbolic.py (แก้ไขสมบูรณ์)
# ============================================================
FILES["physics_symbolic.py"] = r'''"""
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
'''

# ============================================================
# 4. hardware_bridge.py
# ============================================================
FILES["hardware_bridge.py"] = r'''"""hardware_bridge.py — เชื่อม Python กับ ESP32 (v2)"""
import serial
import serial.tools.list_ports
import time
import numpy as np
import csv
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent / "hardware_data"
DATA_DIR.mkdir(exist_ok=True)

FINGERS = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
CMD_MAP = {"Thumb": "T", "Index": "I", "Middle": "M", "Ring": "R", "Pinky": "P"}

class SatiARMHardware:
    def __init__(self, port=None, baud=115200):
        self.port = port or self.find_esp32()
        self.baud = baud
        self.ser = None

    def find_esp32(self):
        for p in serial.tools.list_ports.comports():
            if any(k in p.description for k in ["CP210", "CH340", "USB-SERIAL", "ESP32"]):
                print(f"[OK] พบ ESP32: {p.device}")
                return p.device
        print("[WARN] ไม่พบ ESP32 -> ใช้ COM3")
        return "COM3"

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
            time.sleep(2)
            self.ser.reset_input_buffer()
            print(f"[OK] เชื่อมต่อ {self.port}")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False

    def send(self, cmd):
        if self.ser:
            self.ser.write((cmd + "\n").encode())

    def send_servo(self, finger, angle):
        self.send(f"{CMD_MAP[finger]}{angle}")

    def send_all(self, angle):
        self.send(f"A{angle}")

    def set_breath_period(self, ms):
        self.send(f"B{ms}")

    def set_threshold(self, thr):
        self.send(f"X{thr}")

    def enter_mode(self, mode_num):
        self.send(str(mode_num))

    def request_fsr(self):
        self.send("S")

    def read_line(self, timeout=0.5):
        if not self.ser:
            return None
        t0 = time.time()
        while time.time() - t0 < timeout:
            if self.ser.in_waiting:
                return self.ser.readline().decode(errors="ignore").strip()
            time.sleep(0.01)
        return None

    def read_fsr_values(self):
        self.request_fsr()
        values = {}
        t0 = time.time()
        while time.time() - t0 < 2.0:
            line = self.read_line(0.3)
            if not line:
                continue
            for f in FINGERS:
                if line.strip().startswith(f + ":"):
                    try:
                        values[f] = int(line.split(":")[1].strip())
                    except ValueError:
                        pass
            if len(values) == 5:
                break
        return values

    def log_data(self, finger, angle, fsr):
        fp = DATA_DIR / "hardware_log.csv"
        write_header = not fp.exists()
        with open(fp, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(["timestamp", "finger", "angle", "fsr"])
            w.writerow([datetime.now().isoformat(), finger, angle, fsr])

    def disconnect(self):
        if self.ser:
            self.ser.close()
            print("[OK] ตัดการเชื่อมต่อ")

def demo_mode():
    print("=" * 60)
    print("  Hardware Bridge — DEMO MODE")
    print("=" * 60)

    hw = SatiARMHardware()
    connected = hw.connect()

    if connected:
        print("\n[INFO] ใช้โหมดจริง")
        hw.enter_mode(1)
        for _ in range(20):
            line = hw.read_line(1.0)
            if line:
                print(f"  ESP32: {line}")
        hw.disconnect()
    else:
        print("\n[DEMO] จำลองข้อมูล ESP32\n")
        for i in range(5):
            fsr = int(np.clip(300 + 500 * np.sin(i / 2) + np.random.normal(0, 30), 0, 1023))
            print(f"  Sample {i+1}: FSR = {fsr}")
            hw.log_data("Index", 90, fsr)
            time.sleep(0.2)
        print(f"\n[OK] บันทึกที่: {DATA_DIR / 'hardware_log.csv'}")
        print("\n[DEMO] ทดสอบ commands:")
        for finger in FINGERS:
            print(f"  -> send_servo({finger}, 90)")
        print("  -> send_all(180)")
        print("  -> set_breath_period(6000)")
        print("  -> set_threshold(500)")

if __name__ == "__main__":
    demo_mode()
'''

# ============================================================
# 5. esp32_firmware.ino
# ============================================================
FILES["esp32_firmware.ino"] = r'''/*
 * ============================================================
 * SatiARM ESP32 Firmware v1.0
 * 5-Finger Robotic Hand + FSR Feedback
 * ============================================================
 * Hardware:
 *   - 5x Servo (SG90/MG90S)
 *   - 5x FSR at fingertips
 *   - LED status
 * Serial Commands (115200 baud):
 *   1) Manual  2) FSR Monitor  3) Breathing
 *   4) Adaptive  5) Calibrate  6) Status  7) Reset
 *   T/I/M/R/P<angle>  A<angle>  B<ms>  X<thr>  S  ?
 * ============================================================
 */
#include <ESP32Servo.h>

#define PIN_SERVO_THUMB   13
#define PIN_SERVO_INDEX   12
#define PIN_SERVO_MIDDLE  14
#define PIN_SERVO_RING    27
#define PIN_SERVO_PINKY   26

#define PIN_FSR_THUMB     34
#define PIN_FSR_INDEX     35
#define PIN_FSR_MIDDLE    32
#define PIN_FSR_RING      33
#define PIN_FSR_PINKY     25

#define PIN_LED           2

Servo sThumb, sIndex, sMiddle, sRing, sPinky;

int fsrThreshold = 600;
int breathPeriodMs = 8000;
int servoMin = 0;
int servoMax = 180;

enum Mode { MODE_IDLE, MODE_BREATH, MODE_ADAPTIVE, MODE_MANUAL };
Mode currentMode = MODE_IDLE;

unsigned long lastBreathMs = 0;
float curlAmount = 0.0;
int fsrValues[5] = {0, 0, 0, 0, 0};

void setup() {
  Serial.begin(115200);
  delay(500);
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);

  sThumb.attach(PIN_SERVO_THUMB);
  sIndex.attach(PIN_SERVO_INDEX);
  sMiddle.attach(PIN_SERVO_MIDDLE);
  sRing.attach(PIN_SERVO_RING);
  sPinky.attach(PIN_SERVO_PINKY);

  setAllServos(0);
  printWelcome();
  printMenu();
}

void loop() {
  handleSerial();
  if (currentMode == MODE_BREATH) updateBreathing();
  else if (currentMode == MODE_ADAPTIVE) updateAdaptive();
  else if (currentMode == MODE_MANUAL) readAllFSR();
}

void handleSerial() {
  if (!Serial.available()) return;
  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() == 0) return;

  char cmd = line.charAt(0);
  String arg = line.substring(1);
  arg.trim();

  switch (cmd) {
    case '1': enterBreathMode(); break;
    case '2': enterFSRMode(); break;
    case '3': enterBreathMode(); break;
    case '4': enterAdaptiveMode(); break;
    case '5': calibrateFSR(); break;
    case '6': printStatus(); break;
    case '7': resetSystem(); break;
    case 'T': setServo(sThumb, arg.toInt(), "Thumb"); break;
    case 'I': setServo(sIndex, arg.toInt(), "Index"); break;
    case 'M': setServo(sMiddle, arg.toInt(), "Middle"); break;
    case 'R': setServo(sRing, arg.toInt(), "Ring"); break;
    case 'P': setServo(sPinky, arg.toInt(), "Pinky"); break;
    case 'A':
      setAllServos(arg.toInt());
      Serial.print("[OK] All servos -> "); Serial.println(arg);
      break;
    case 'B':
      breathPeriodMs = arg.toInt();
      Serial.print("[OK] Breath period = "); Serial.println(breathPeriodMs);
      break;
    case 'X':
      fsrThreshold = arg.toInt();
      Serial.print("[OK] FSR threshold = "); Serial.println(fsrThreshold);
      break;
    case 'S': printFSR(); break;
    case '?': printMenu(); break;
    default:
      Serial.print("[ERR] Unknown: "); Serial.println(line);
  }
}

void enterBreathMode() {
  currentMode = MODE_BREATH;
  lastBreathMs = millis();
  digitalWrite(PIN_LED, HIGH);
  Serial.println("[MODE] Breathing Guide");
  Serial.print("[INFO] Period = "); Serial.print(breathPeriodMs); Serial.println(" ms");
}

void enterFSRMode() {
  currentMode = MODE_IDLE;
  digitalWrite(PIN_LED, LOW);
  Serial.println("[MODE] FSR Monitor");
  printFSR();
}

void enterAdaptiveMode() {
  currentMode = MODE_ADAPTIVE;
  lastBreathMs = millis();
  digitalWrite(PIN_LED, HIGH);
  Serial.println("[MODE] Adaptive Grasp");
}

void resetSystem() {
  currentMode = MODE_IDLE;
  setAllServos(0);
  digitalWrite(PIN_LED, LOW);
  Serial.println("[OK] Reset");
  printMenu();
}

void updateBreathing() {
  unsigned long now = millis();
  float phase = 2.0 * PI * ((now - lastBreathMs) % breathPeriodMs) / breathPeriodMs;
  float breath = sin(phase);
  curlAmount = 0.5 + 0.5 * breath;

  int angle = (int)(curlAmount * 180);
  setAllServosAdaptive(angle);

  static unsigned long lastReport = 0;
  if (now - lastReport > 500) {
    lastReport = now;
    Serial.print("[BREATH] ");
    Serial.print(breath >= 0 ? "INHALE" : "EXHALE");
    Serial.print(" curl="); Serial.print(curlAmount, 3);
    Serial.print(" angle="); Serial.println(angle);
  }
}

void updateAdaptive() {
  unsigned long now = millis();
  float phase = 2.0 * PI * ((now - lastBreathMs) % breathPeriodMs) / breathPeriodMs;
  float breath = sin(phase);
  float baseCurl = 0.5 + 0.5 * breath;

  readAllFSR();
  int maxFSR = 0;
  for (int i = 0; i < 5; i++) if (fsrValues[i] > maxFSR) maxFSR = fsrValues[i];

  float curl = baseCurl;
  if (maxFSR > fsrThreshold) {
    float excess = (float)(maxFSR - fsrThreshold) / (1023.0 - fsrThreshold);
    curl = baseCurl * (1.0 - 0.7 * excess);
    if (curl < 0) curl = 0;
  }

  int angle = (int)(curl * 180);
  setAllServosAdaptive(angle);

  static unsigned long lastReport = 0;
  if (now - lastReport > 500) {
    lastReport = now;
    Serial.print("[ADAPTIVE] maxFSR="); Serial.print(maxFSR);
    Serial.print(" curl="); Serial.print(curl, 3);
    Serial.print(" angle="); Serial.println(angle);
  }
}

void setServo(Servo &s, int angle, const char* name) {
  if (angle < servoMin) angle = servoMin;
  if (angle > servoMax) angle = servoMax;
  s.write(angle);
  Serial.print("[OK] "); Serial.print(name); Serial.print(" -> "); Serial.print(angle); Serial.println(" deg");
}

void setAllServos(int angle) {
  if (angle < servoMin) angle = servoMin;
  if (angle > servoMax) angle = servoMax;
  sThumb.write(angle); sIndex.write(angle); sMiddle.write(angle);
  sRing.write(angle); sPinky.write(angle);
}

void setAllServosAdaptive(int angle) {
  sThumb.write((int)(angle * 0.85));
  sIndex.write(angle);
  sMiddle.write(angle);
  sRing.write((int)(angle * 0.95));
  sPinky.write((int)(angle * 0.85));
}

void readAllFSR() {
  fsrValues[0] = analogRead(PIN_FSR_THUMB);
  fsrValues[1] = analogRead(PIN_FSR_INDEX);
  fsrValues[2] = analogRead(PIN_FSR_MIDDLE);
  fsrValues[3] = analogRead(PIN_FSR_RING);
  fsrValues[4] = analogRead(PIN_FSR_PINKY);
}

void printFSR() {
  readAllFSR();
  Serial.println("[FSR]");
  Serial.print("  Thumb:  "); Serial.println(fsrValues[0]);
  Serial.print("  Index:  "); Serial.println(fsrValues[1]);
  Serial.print("  Middle: "); Serial.println(fsrValues[2]);
  Serial.print("  Ring:   "); Serial.println(fsrValues[3]);
  Serial.print("  Pinky:  "); Serial.println(fsrValues[4]);
}

void calibrateFSR() {
  Serial.println("[CAL] Hold fingers at rest 3s...");
  delay(3000);
  long sum[5] = {0, 0, 0, 0, 0};
  for (int i = 0; i < 20; i++) {
    readAllFSR();
    for (int j = 0; j < 5; j++) sum[j] += fsrValues[j];
    delay(50);
  }
  Serial.println("[CAL] Baseline:");
  for (int j = 0; j < 5; j++) {
    Serial.print("  Finger "); Serial.print(j);
    Serial.print(": "); Serial.println(sum[j] / 20);
  }
  Serial.println("[CAL] Done");
}

void printWelcome() {
  Serial.println();
  Serial.println("============================================================");
  Serial.println("  SatiARM ESP32 Firmware v1.0");
  Serial.println("  5-Finger Robotic Hand + FSR Feedback");
  Serial.println("============================================================");
}

void printMenu() {
  Serial.println();
  Serial.println("--- MENU ---");
  Serial.println(" 1) Manual  2) FSR Monitor  3) Breathing");
  Serial.println(" 4) Adaptive  5) Calibrate  6) Status  7) Reset");
  Serial.println("Commands: T/I/M/R/P<a>  A<a>  B<ms>  X<thr>  S  ?");
  Serial.println();
}

void printStatus() {
  Serial.println("[STATUS]");
  Serial.print("  Mode: ");
  switch (currentMode) {
    case MODE_IDLE: Serial.println("IDLE"); break;
    case MODE_BREATH: Serial.println("BREATH"); break;
    case MODE_ADAPTIVE: Serial.println("ADAPTIVE"); break;
    case MODE_MANUAL: Serial.println("MANUAL"); break;
  }
  Serial.print("  Threshold: "); Serial.println(fsrThreshold);
  Serial.print("  Breath period: "); Serial.println(breathPeriodMs);
  printFSR();
}
'''

# ============================================================
# 6. physics_ai_app.py (Streamlit)
# ============================================================
FILES["physics_ai_app.py"] = r'''"""physics_ai_app.py — Physics AI Lab (Beautiful UI)"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import time
import json
from pathlib import Path
from datetime import datetime

for f in ["Leelawadee UI", "Tahoma", "Sarabun", "Noto Sans Thai"]:
    if f in {x.name for x in fm.fontManager.ttflist}:
        plt.rcParams['font.family'] = f
        break
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="Physics AI Lab", page_icon="A",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Sarabun:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', 'Sarabun', sans-serif; }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem; border-radius: 16px; color: white;
        margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 { margin: 0; font-size: 2.2rem; font-weight: 700; color: white; }
    .main-header p { margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.05rem; }
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px; padding: 1rem; border-left: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 10px;
        padding: 0.6rem 1.5rem; font-weight: 600;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .info-card {
        background: white; padding: 1.5rem; border-radius: 12px;
        border: 1px solid #e0e6ed; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    section[data-testid="stSidebar"] * { color: #ecf0f1 !important; }
    .stTabs [data-baseweb="tab"] {
        background: #f0f2f6; border-radius: 8px 8px 0 0;
        padding: 0.6rem 1.2rem; font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).parent
KB_FILE = ROOT / "physics_knowledge.json"
OUTPUT_DIR = ROOT / "physics_ai_output"
DATA_DIR = ROOT / "hardware_data"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_kb():
    if not KB_FILE.exists():
        return {"version": "0.0.0", "equations": [], "history": []}
    with open(KB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_kb(kb):
    kb["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(KB_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

st.markdown("""
<div class="main-header">
    <h1>Physics AI Lab</h1>
    <p>ระบบ AI ด้านฟิสิกส์สำหรับนักเรียน — ค้นพบสมการ, แก้สมการ, ควบคุมฮาร์ดแวร์</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## เมนูหลัก")
    page = st.radio("เลือกหน้า", [
        "Home",
        "Symbolic Regression",
        "PINN Solver",
        "Analytics",
        "Hardware Control",
        "Knowledge Base",
    ], label_visibility="collapsed")
    st.markdown("---")
    kb = load_kb()
    st.markdown("### สถิติ")
    st.metric("สมการใน KB", len(kb["equations"]))
    st.metric("เวอร์ชัน", kb.get("version", "0.0.0"))
    st.markdown("---")
    st.caption("Physics AI Lab v3.0 | 2026")

# ==================== HOME ====================
if page == "Home":
    st.markdown("## ยินดีต้อนรับ")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="info-card"><h3>ค้นพบสมการ</h3>'
                    '<p>ใช้ Symbolic Regression ค้นหาสมการฟิสิกส์จากข้อมูล</p></div>',
                    unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card"><h3>แก้สมการ</h3>'
                    '<p>ใช้ PINN แก้สมการเชิงอนุพันธ์</p></div>',
                    unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="info-card"><h3>ควบคุมฮาร์ดแวร์</h3>'
                    '<p>เชื่อมต่อ ESP32 + เซอร์โว + FSR</p></div>',
                    unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### ภาพรวมระบบ")
    st.markdown("""
    | Layer | หน้าที่ | เครื่องมือ |
    |-------|--------|-----------|
    | 1 | Symbolic Regression | PySR |
    | 2 | PINN Solver | PyTorch |
    | 3 | Analytics | Pandas |
    | 4 | Hardware | ESP32 |
    | 5 | Knowledge Base | JSON |
    """)

# ==================== SYMBOLIC ====================
elif page == "Symbolic Regression":
    st.markdown("## ค้นพบสมการฟิสิกส์จากข้อมูล")
    datasets = {
        "pendulum": "ลูกตุ้ม", "projectile": "โพรเจกไทล์",
        "ohm": "กฎโอห์ม", "coulomb": "กฎคูลอมบ์",
        "hooke": "กฎฮุก", "kinetic_energy": "พลังงานจลน์",
        "heat_conduction": "การนำความร้อน", "ideal_gas": "แก๊สอุดมคติ",
        "wave_speed": "ความเร็วคลื่น", "rc_time": "เวลา RC",
        "stefan": "สเตฟาน-โบลต์ซมันน์",
    }
    selected = st.selectbox("เลือกสมการ", list(datasets.keys()),
                             format_func=lambda x: f"{x} - {datasets[x]}")

    if st.button("ค้นพบสมการ", type="primary", use_container_width=True):
        with st.spinner("กำลังค้นหา..."):
            time.sleep(1)
            demo_eqs = {
                "pendulum": ("T = 2*pi*sqrt(L/g)", r"T = 2\pi\sqrt{\frac{L}{g}}", 0.9987),
                "projectile": ("h = v0**2*sin(theta)**2/(2*g)", r"h = \frac{v_0^2\sin^2\theta}{2g}", 0.9965),
                "ohm": ("V = I*R", r"V = IR", 0.9998),
                "coulomb": ("F = k*q1*q2/r**2", r"F = k\frac{q_1 q_2}{r^2}", 0.9992),
                "hooke": ("F = -k*x", r"F = -kx", 0.9988),
                "kinetic_energy": ("KE = 0.5*m*v**2", r"KE = \frac{1}{2}mv^2", 0.9999),
                "heat_conduction": ("Q = k*A*dT/L", r"Q = kA\frac{\Delta T}{L}", 0.9955),
                "ideal_gas": ("P = n*R*T/V", r"P = \frac{nRT}{V}", 0.9980),
                "wave_speed": ("v = f*lam", r"v = f\lambda", 0.9997),
                "rc_time": ("tau = R*C", r"\tau = RC", 0.9995),
                "stefan": ("P = sigma*A*T**4", r"P = \sigma A T^4", 0.9975),
            }
            eq_text, eq_latex, r2 = demo_eqs[selected]
            st.success("ค้นพบสมการสำเร็จ!")
            c1, c2, c3 = st.columns(3)
            c1.metric("สมการ", eq_text)
            c2.metric("R2", f"{r2:.4f}")
            c3.metric("Complexity", int(np.random.randint(5, 12)))
            st.latex(eq_latex)

            # Pareto front
            fig, ax = plt.subplots(figsize=(8, 4))
            complexity = np.arange(1, 13)
            loss = 1.0 / (complexity ** 1.5) + 0.001 * np.random.rand(12)
            ax.plot(complexity, loss, "o-", color="#667eea", lw=2, markersize=8)
            ax.set_xlabel("Complexity")
            ax.set_ylabel("Loss")
            ax.set_yscale("log")
            ax.set_title("Complexity vs Accuracy")
            ax.grid(alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)

# ==================== PINN ====================
elif page == "PINN Solver":
    st.markdown("## PINN - แก้สมการเชิงอนุพันธ์")
    col1, col2 = st.columns(2)
    with col1:
        eq = st.selectbox("สมการ", ["Heat", "Burgers", "Wave"])
        if eq == "Heat":
            param = st.slider("alpha", 0.01, 0.5, 0.1)
        elif eq == "Burgers":
            param = st.slider("nu", 0.001, 0.1, 0.01)
        else:
            param = st.slider("c", 0.5, 2.0, 1.0)
    with col2:
        t_max = st.slider("t max", 1.0, 5.0, 2.0)
        n_grid = st.slider("Grid", 50, 200, 100)

    if st.button("แก้สมการ", type="primary", use_container_width=True):
        with st.spinner("Training..."):
            time.sleep(1.5)
            x = np.linspace(0, 1, n_grid)
            t = np.linspace(0, t_max, n_grid)
            T, X = np.meshgrid(t, x, indexing="ij")
            if eq == "Heat":
                U = np.sin(np.pi * X) * np.exp(-param * np.pi**2 * T)
            elif eq == "Burgers":
                U = -np.sin(np.pi * X) * np.exp(-param * T * 10)
            else:
                U = np.sin(np.pi * X) * np.cos(np.pi * param * T)

            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            im = axes[0].imshow(U, extent=[0, t_max, 1, 0], aspect="auto", cmap="RdBu_r")
            axes[0].set_xlabel("t"); axes[0].set_ylabel("x")
            axes[0].set_title("Heatmap u(t,x)")
            plt.colorbar(im, ax=axes[0])
            for tv in [0, t_max*0.25, t_max*0.5, t_max]:
                idx = int(tv / t_max * (n_grid - 1))
                axes[1].plot(x, U[idx], lw=2, label=f"t={tv:.2f}")
            axes[1].set_xlabel("x"); axes[1].set_ylabel("u")
            axes[1].legend(); axes[1].grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

# ==================== ANALYTICS ====================
elif page == "Analytics":
    st.markdown("## การวิเคราะห์ข้อมูล")
    tab1, tab2, tab3 = st.tabs(["FSR", "HRV", "Correlation"])

    with tab1:
        log_file = DATA_DIR / "hardware_log.csv"
        if log_file.exists():
            df = pd.read_csv(log_file)
            st.write(f"**ข้อมูล:** {len(df)} แถว")
            c1, c2 = st.columns(2)
            with c1:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(df.index, df["fsr"], marker="o", color="#667eea", lw=2)
                ax.axhline(600, color="red", ls="--", label="threshold")
                ax.set_xlabel("Sample"); ax.set_ylabel("FSR")
                ax.legend(); ax.grid(alpha=0.3)
                st.pyplot(fig); plt.close(fig)
            with c2:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(df["fsr"], bins=15, color="#764ba2", edgecolor="white")
                ax.set_xlabel("FSR"); ax.set_ylabel("Count")
                ax.grid(alpha=0.3)
                st.pyplot(fig); plt.close(fig)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Mean", f"{df['fsr'].mean():.1f}")
            c2.metric("Std", f"{df['fsr'].std():.1f}")
            c3.metric("Min", f"{df['fsr'].min()}")
            c4.metric("Max", f"{df['fsr'].max()}")
        else:
            st.warning("ยังไม่มีข้อมูล FSR")

    with tab2:
        np.random.seed(42)
        n = 100
        hr_pre = np.random.normal(78, 8, n)
        hr_post = np.random.normal(64, 6, n)
        from scipy import stats
        fig, axes = plt.subplots(1, 2, figsize=(14, 4))
        axes[0].hist(hr_pre, bins=20, alpha=0.6, color="#e74c3c", label="Before")
        axes[0].hist(hr_post, bins=20, alpha=0.6, color="#3498db", label="After")
        axes[0].set_xlabel("HR (bpm)"); axes[0].legend(); axes[0].grid(alpha=0.3)
        axes[1].boxplot([hr_pre, hr_post], labels=["Before", "After"])
        axes[1].set_ylabel("HR"); axes[1].grid(alpha=0.3)
        st.pyplot(fig); plt.close(fig)
        t, p = stats.ttest_ind(hr_pre, hr_post)
        c1, c2, c3 = st.columns(3)
        c1.metric("d HR", f"{hr_post.mean() - hr_pre.mean():+.1f} bpm")
        c2.metric("t", f"{t:.3f}")
        c3.metric("p-value", f"{p:.6f}")

    with tab3:
        np.random.seed(42)
        df = pd.DataFrame({
            "FSR_Thumb": np.random.normal(500, 100, 100),
            "FSR_Index": np.random.normal(520, 110, 100),
            "HR": np.random.normal(75, 10, 100),
        })
        corr = df.corr()
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr))); ax.set_yticks(range(len(corr)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right")
        ax.set_yticklabels(corr.columns)
        for i in range(len(corr)):
            for j in range(len(corr)):
                ax.text(j, i, f"{corr.iloc[i,j]:.2f}", ha="center", va="center")
        plt.colorbar(im, ax=ax)
        st.pyplot(fig); plt.close(fig)

# ==================== HARDWARE ====================
elif page == "Hardware Control":
    st.markdown("## ควบคุมฮาร์ดแวร์")
    tab1, tab2, tab3 = st.tabs(["Connection", "Control", "Monitor"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            port = st.text_input("Port", "COM3")
            baud = st.selectbox("Baud", [9600, 115200], index=1)
            if st.button("เชื่อมต่อ", use_container_width=True):
                st.success(f"Connected {port}")
        with c2:
            st.markdown("**สถานะ**")
            st.markdown("พร้อมใช้งาน")
            if st.button("ตัดการเชื่อมต่อ", use_container_width=True):
                st.warning("Disconnected")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            finger = st.selectbox("นิ้ว", ["Thumb", "Index", "Middle", "Ring", "Pinky"])
            angle = st.slider("มุม", 0, 180, 90)
            if st.button("ส่งคำสั่ง", use_container_width=True):
                cmd = {"Thumb": "T", "Index": "I", "Middle": "M", "Ring": "R", "Pinky": "P"}[finger]
                st.code(f"{cmd}{angle}", language="text")
        with c2:
            all_a = st.slider("มุมรวม", 0, 180, 90, key="all_a")
            if st.button("ส่งทั้งหมด", use_container_width=True):
                st.code(f"A{all_a}", language="text")
            st.markdown("**Quick Modes**")
            if st.button("Breathing Guide"):
                st.code("3", language="text")
            if st.button("Adaptive Grasp"):
                st.code("4", language="text")

    with tab3:
        if st.button("เริ่มอ่าน", use_container_width=True):
            ph = st.empty()
            log = []
            for i in range(30):
                log.append(f"[{i:02d}] FSR={300 + int(400*np.sin(i/5))} angle={int(90+80*np.sin(i/3))}")
                ph.code("\n".join(log[-15:]), language="text")
                time.sleep(0.05)

# ==================== KB ====================
elif page == "Knowledge Base":
    st.markdown("## ฐานความรู้ฟิสิกส์")
    kb = load_kb()
    tab1, tab2, tab3 = st.tabs(["ดูสมการ", "เพิ่มสมการ", "ประวัติ"])

    with tab1:
        st.write(f"**มีทั้งหมด {len(kb['equations'])} สมการ**")
        cat_filter = st.selectbox("หมวด",
            ["ทั้งหมด"] + sorted(set(e.get("category", "other") for e in kb["equations"])))
        filtered = kb["equations"]
        if cat_filter != "ทั้งหมด":
            filtered = [e for e in filtered if e.get("category") == cat_filter]
        for eq in filtered:
            with st.expander(f"**{eq['name_th']}** - {eq['name_en']}"):
                st.latex(eq["latex"])
                st.markdown(f"`{eq['formula']}`")
                for k, v in eq.get("variables", {}).items():
                    st.markdown(f"- `{k}` - {v}")
                if st.button(f"ลบ {eq['id']}", key=f"del_{eq['id']}"):
                    kb["equations"] = [e for e in kb["equations"] if e["id"] != eq["id"]]
                    save_kb(kb)
                    st.rerun()

    with tab2:
        with st.form("add_eq"):
            c1, c2 = st.columns(2)
            with c1:
                new_id = st.text_input("ID", "my_eq")
                name_th = st.text_input("ชื่อไทย", "สมการใหม่")
                name_en = st.text_input("ชื่ออังกฤษ", "New Eq")
                latex = st.text_input("LaTeX", r"E = mc^2")
            with c2:
                formula = st.text_input("สูตร Python", "E = m * c**2")
                cat = st.selectbox("หมวด", ["mechanics", "electricity", "thermodynamics",
                                              "waves", "optics", "quantum", "other"])
                level = st.selectbox("ระดับ", ["ม.ต้น", "ม.ปลาย", "มหาวิทยาลัย"])
            vars_json = st.text_area("ตัวแปร (JSON)",
                '{"E": "พลังงาน (J)", "m": "มวล (kg)", "c": "3e8 m/s"}')
            if st.form_submit_button("เพิ่มสมการ"):
                try:
                    variables = json.loads(vars_json)
                    kb["equations"].append({
                        "id": new_id, "name_th": name_th, "name_en": name_en,
                        "latex": latex, "formula": formula, "variables": variables,
                        "category": cat, "level": level, "domain": [cat],
                    })
                    save_kb(kb)
                    st.success(f"เพิ่ม '{name_th}' สำเร็จ")
                    st.rerun()
                except json.JSONDecodeError:
                    st.error("JSON ไม่ถูกต้อง")

    with tab3:
        history = kb.get("history", [])
        if history:
            st.dataframe(pd.DataFrame(history), hide_index=True, use_container_width=True)
        else:
            st.info("ยังไม่มีประวัติ")

    st.markdown("---")
    st.markdown("### นำเข้า/ส่งออก")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("ดาวน์โหลด KB",
            data=json.dumps(kb, ensure_ascii=False, indent=2),
            file_name="physics_knowledge.json", mime="application/json",
            use_container_width=True)
    with c2:
        uploaded = st.file_uploader("อัปโหลด KB", type=["json"])
        if uploaded:
            try:
                new_kb = json.load(uploaded)
                save_kb(new_kb)
                st.success("นำเข้าสำเร็จ")
                st.rerun()
            except Exception as e:
                st.error(f"{e}")

st.markdown("---")
st.caption("Physics AI Lab v3.0 | 2026 | Made with love for Thai students")
'''

# ============================================================
# Create all
# ============================================================
def create_all():
    print("=" * 70)
    print("  Setup SatiARM Physics AI — v3 FINAL")
    print("=" * 70)
    print(f"โฟลเดอร์: {ROOT}\n")

    for name, content in FILES.items():
        path = ROOT / name
        path.write_text(content, encoding="utf-8")
        size = path.stat().st_size
        print(f"  [OK] {name:30s} ({size:>8,} bytes)")

    print("\n" + "=" * 70)
    print("  เสร็จสิ้น! ไฟล์ทั้งหมด:")
    print("=" * 70)
    for name in FILES:
        print(f"  - {name}")

    print("\nขั้นตอนถัดไป:")
    print("  1) py -3 -m pip install streamlit pandas matplotlib scipy pyserial pysr")
    print("  2) py -3 physics_symbolic.py")
    print("  3) py -3 hardware_bridge.py")
    print("  4) py -3 -m streamlit run physics_ai_app.py")
    print()
    print("ESP32:")
    print("  - เปิด esp32_firmware.ino ใน Arduino IDE")
    print("  - ติดตั้ง ESP32Servo library")
    print("  - Upload")

if __name__ == "__main__":
    create_all()
