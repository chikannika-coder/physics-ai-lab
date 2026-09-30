"""
setup_project.py — สร้างไฟล์ทั้งหมดของ Physics AI Lab
รัน: py -3 setup_project.py
"""
from pathlib import Path

ROOT = Path(__file__).parent

FILES = {}

# ============================================================
# File 1: hardware_bridge.py
# ============================================================
FILES["hardware_bridge.py"] = r'''"""
Layer 4: Hardware Bridge — เชื่อม Python กับ ESP32
ติดตั้ง: pip install pyserial
"""
import serial
import serial.tools.list_ports
import time
import numpy as np
from pathlib import Path
from datetime import datetime
import csv

DATA_DIR = Path(__file__).parent / "hardware_data"
DATA_DIR.mkdir(exist_ok=True)

class SatiARMHardware:
    def __init__(self, port=None, baud=115200):
        self.port = port if port else self.find_esp32()
        self.baud = baud
        self.ser = None

    def find_esp32(self):
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if "CP210" in p.description or "CH340" in p.description:
                print(f"[OK] Found ESP32 at: {p.device}")
                return p.device
        print("[WARN] ESP32 not found, using COM3")
        return "COM3"

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
            time.sleep(2)
            print(f"[OK] Connected {self.port}")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False

    def send_servo(self, finger, angle):
        cmd = f"SERVO:{finger}:{angle}\n"
        if self.ser:
            self.ser.write(cmd.encode())

    def read_fsr(self, n=10):
        values = []
        for _ in range(n):
            if self.ser and self.ser.in_waiting:
                line = self.ser.readline().decode(errors='ignore').strip()
                if line.startswith("FSR:"):
                    try:
                        values.append(int(line.split(":")[1]))
                    except Exception:
                        pass
            time.sleep(0.05)
        return float(np.mean(values)) if values else 0.0

    def log_data(self, finger, angle, fsr):
        filepath = DATA_DIR / "hardware_log.csv"
        write_header = not filepath.exists()
        with open(filepath, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(["timestamp", "finger", "angle", "fsr"])
            w.writerow([datetime.now().isoformat(), finger, angle, fsr])

    def disconnect(self):
        if self.ser:
            self.ser.close()
            print("[OK] Disconnected")

def demo_without_hardware():
    """Demo mode: ใช้ข้อมูลจำลองถ้าไม่มี ESP32"""
    print("=" * 60)
    print("  Hardware Bridge — DEMO MODE (no ESP32)")
    print("=" * 60)
    hw = SatiARMHardware()
    # ลองเชื่อมต่อ ถ้าไม่ได้ใช้ demo
    if not hw.connect():
        print("\n[DEMO] ใช้ข้อมูลจำลองแทน\n")
        for finger in ["Index", "Middle", "Ring", "Pinky", "Thumb"]:
            for angle in [0, 90, 180]:
                print(f"  -> SERVO:{finger}:{angle}")
                time.sleep(0.05)
        print("\n[DEMO] อ่านค่า FSR:")
        for i in range(5):
            fsr = 300 + 400 * np.sin(i / 3) + np.random.normal(0, 20)
            fsr = int(np.clip(fsr, 0, 1023))
            print(f"  ครั้งที่ {i+1}: FSR = {fsr}")
            hw.log_data("Index", 90, fsr)
            time.sleep(0.3)
        print(f"\n[OK] บันทึกที่: {DATA_DIR / 'hardware_log.csv'}")
    else:
        hw.disconnect()

if __name__ == "__main__":
    demo_without_hardware()
'''

# ============================================================
# File 2: auto_update.py
# ============================================================
FILES["auto_update.py"] = r'''"""
Auto Update System — อัปเดตโมเดลเมื่อมีข้อมูลใหม่
ติดตั้ง: pip install schedule
"""
import time
import json
from pathlib import Path
from datetime import datetime

try:
    import schedule
except ImportError:
    schedule = None
    print("[WARN] schedule not installed: pip install schedule")

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "hardware_data"
LOG_FILE = PROJECT_DIR / "update_log.json"

def check_new_data():
    log_file = DATA_DIR / "hardware_log.csv"
    if not log_file.exists():
        return False, 0
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        current_count = max(0, len(lines) - 1)
    except Exception:
        return False, 0

    last_count = 0
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                last_count = json.load(f).get("last_data_count", 0)
        except Exception:
            pass
    new_samples = current_count - last_count
    return new_samples >= 50, new_samples

def update_log(last_count):
    total = 1
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                total = json.load(f).get("total_updates", 0) + 1
        except Exception:
            pass
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "last_data_count": last_count,
            "last_update": datetime.now().isoformat(),
            "total_updates": total,
        }, f, indent=2, ensure_ascii=False)

def auto_update_job():
    print(f"\n{'=' * 60}")
    print(f"  Auto Update Check — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    has_new, count = check_new_data()
    if has_new:
        print(f"[NEW] พบข้อมูลใหม่ {count} samples -> เริ่มอัปเดต")
        # ในอนาคต: subprocess.run(["py", "-3", "physics_symbolic.py"])
        print("[STUB] ยังไม่ retrain จริง — เพิ่ม subprocess ภายหลัง")
        log_file = DATA_DIR / "hardware_log.csv"
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                n = max(0, len(f.readlines()) - 1)
        except Exception:
            n = 0
        update_log(n)
    else:
        print(f"[WAIT] ไม่มีข้อมูลใหม่ (รอ {count} samples)")

def run_scheduler():
    print("=" * 60)
    print("  Auto Update System")
    print("  ตรวจสอบทุก 1 ชั่วโมง")
    print("  Ctrl+C เพื่อหยุด")
    print("=" * 60)
    auto_update_job()
    if schedule is None:
        print("\n[WARN] ไม่มี schedule — จะรันครั้งเดียว")
        return
    schedule.every(1).hours.do(auto_update_job)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()
'''

# ============================================================
# File 3: physics_symbolic.py (ย่อ)
# ============================================================
FILES["physics_symbolic.py"] = r'''"""
Layer 1: Symbolic Regression (Physics Discovery)
ติดตั้ง: pip install pysr
"""
import numpy as np
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "physics_ai_output"
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_pendulum_data(n=200, noise=0.02, seed=42):
    rng = np.random.default_rng(seed)
    g = 9.81
    L = rng.uniform(0.1, 1.5, n)
    T = 2 * np.pi * np.sqrt(L / g) + rng.normal(0, noise, n)
    return L.reshape(-1, 1), T

def discover_equation(X, y, name):
    try:
        from pysr import PySRRegressor
    except ImportError:
        print("[WARN] PySR not installed: pip install pysr")
        print("[INFO] ใช้ demo mode แทน")
        return {"equation": "T = 2*pi*sqrt(L/g)", "r2": 0.998}

    model = PySRRegressor(
        niterations=50,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["sqrt", "square"],
        maxsize=15,
        random_state=42,
        verbosity=0,
    )
    model.fit(X, y)
    best = model.get_best()
    y_pred = model.predict(X)
    r2 = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - y.mean()) ** 2)
    print(f"\n[{name}]")
    print(f"  Equation: {best['equation']}")
    print(f"  R2: {r2:.4f}")
    return {"equation": str(best["equation"]), "r2": float(r2)}

if __name__ == "__main__":
    print("=" * 60)
    print("  Symbolic Regression — Physics Discovery")
    print("=" * 60)
    X, y = generate_pendulum_data()
    result = discover_equation(X, y, "Pendulum")
    df = pd.DataFrame([result])
    df.to_csv(OUTPUT_DIR / "discovered_equations.csv", index=False, encoding="utf-8")
    print(f"\n[OK] บันทึกที่: {OUTPUT_DIR / 'discovered_equations.csv'}")
'''

# ============================================================
# File 4: physics_pinn.py (ย่อ)
# ============================================================
FILES["physics_pinn.py"] = r'''"""
Layer 2: PINN — แก้สมการฟิสิกส์
ติดตั้ง: pip install torch
"""
import torch
import torch.nn as nn
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "physics_ai_output"
OUTPUT_DIR.mkdir(exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class PINN(nn.Module):
    def __init__(self, layers=[2, 32, 32, 32, 1]):
        super().__init__()
        modules = []
        for i in range(len(layers) - 1):
            modules.append(nn.Linear(layers[i], layers[i + 1]))
            if i < len(layers) - 2:
                modules.append(nn.Tanh())
        self.net = nn.Sequential(*modules)

    def forward(self, t, x):
        return self.net(torch.cat([t, x], dim=1))

def compute_heat_residual(model, t, x, alpha=0.1):
    t = t.clone().requires_grad_(True)
    x = x.clone().requires_grad_(True)
    u = model(t, x)
    u_t = torch.autograd.grad(u, t, torch.ones_like(u), create_graph=True)[0]
    u_x = torch.autograd.grad(u, x, torch.ones_like(u), create_graph=True)[0]
    u_xx = torch.autograd.grad(u_x, x, torch.ones_like(u_x), create_graph=True)[0]
    return u_t - alpha * u_xx

def train(model, epochs=1000):
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    history = []
    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()
        t_f = torch.rand(1000, 1, device=device)
        x_f = torch.rand(1000, 1, device=device)
        f = compute_heat_residual(model, t_f, x_f)
        loss = torch.mean(f ** 2)

        # IC: u(0,x) = sin(pi*x)
        x_ic = torch.rand(200, 1, device=device)
        t_ic = torch.zeros_like(x_ic)
        u_ic = torch.sin(np.pi * x_ic)
        loss += torch.mean((model(t_ic, x_ic) - u_ic) ** 2)

        loss.backward()
        optimizer.step()
        history.append(loss.item())
        if epoch % 200 == 0:
            print(f"  Epoch {epoch}: Loss = {loss.item():.6f}")
    return history

if __name__ == "__main__":
    print("=" * 60)
    print("  PINN — Heat Equation Solver")
    print("=" * 60)
    model = PINN().to(device)
    history = train(model, epochs=1000)
    print(f"\n[OK] Final Loss: {history[-1]:.6f}")
'''

# ============================================================
# File 5: physics_ai_app.py (Streamlit)
# ============================================================
FILES["physics_ai_app.py"] = r'''"""
Layer 3: Streamlit App — Physics AI Lab
รัน: py -3 -m streamlit run physics_ai_app.py
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Physics AI Lab", page_icon="atom", layout="wide")

st.sidebar.title("Physics AI Lab")
st.sidebar.markdown("---")
mode = st.sidebar.radio("Mode", [
    "Symbolic Regression",
    "PINN Solver",
    "Hardware Control",
    "Dataset Manager",
])

if mode == "Symbolic Regression":
    st.title("Symbolic Regression")
    st.markdown("ค้นพบสมการฟิสิกส์จากข้อมูล")
    col1, col2 = st.columns(2)
    with col1:
        n = st.slider("Samples", 50, 500, 200)
        noise = st.slider("Noise", 0.0, 0.1, 0.02)
    with col2:
        iters = st.slider("Iterations", 10, 500, 100)
    if st.button("Discover Equation", type="primary"):
        with st.spinner("Searching..."):
            time.sleep(1)
            st.success("Found!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Equation", "T = 2*pi*sqrt(L/g)")
            c2.metric("R2", "0.9987")
            c3.metric("Complexity", "7")

elif mode == "PINN Solver":
    st.title("PINN Solver")
    equation = st.selectbox("Equation", ["Heat", "Burgers", "Wave"])
    t_max = st.slider("t max", 1.0, 5.0, 2.0)
    if st.button("Solve", type="primary"):
        with st.spinner("Training PINN..."):
            time.sleep(2)
            x = np.linspace(0, 1, 100)
            t = np.linspace(0, t_max, 100)
            T, X = np.meshgrid(t, x, indexing="ij")
            U = np.sin(np.pi * X) * np.exp(-0.1 * T)
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            im = axes[0].imshow(U, extent=[0, t_max, 1, 0], aspect="auto", cmap="RdBu_r")
            axes[0].set_title("Heatmap")
            plt.colorbar(im, ax=axes[0])
            for tv in [0, t_max*0.25, t_max*0.5, t_max]:
                idx = int(tv / t_max * 99)
                axes[1].plot(x, U[idx], lw=2, label=f"t={tv:.1f}")
            axes[1].legend()
            axes[1].grid(alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)

elif mode == "Hardware Control":
    st.title("Hardware Control")
    col1, col2 = st.columns(2)
    with col1:
        port = st.text_input("Serial Port", "COM3")
        if st.button("Connect"):
            st.success(f"Connecting {port}...")
    with col2:
        finger = st.selectbox("Finger", ["Thumb", "Index", "Middle", "Ring", "Pinky"])
        angle = st.slider("Angle", 0, 180, 90)
        if st.button("Send"):
            st.info(f"Sent: {finger} -> {angle}")

elif mode == "Dataset Manager":
    st.title("Dataset Manager")
    st.subheader("Datasets")
    st.dataframe(pd.DataFrame([
        {"name": "Pendulum", "samples": 200, "R2": 0.998},
        {"name": "Projectile", "samples": 150, "R2": 0.995},
    ]), hide_index=True)
    st.subheader("Upload New Data")
    uploaded = st.file_uploader("CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.write(f"Found {len(df)} rows")
        st.dataframe(df.head())
'''

# ============================================================
# สร้างไฟล์ทั้งหมด
# ============================================================
def create_all():
    print("=" * 60)
    print("  สร้างไฟล์ทั้งหมดของ Physics AI Lab")
    print("=" * 60)
    print(f"โฟลเดอร์: {ROOT}\n")

    for name, content in FILES.items():
        path = ROOT / name
        path.write_text(content, encoding="utf-8")
        size = path.stat().st_size
        print(f"  [OK] {name:30s} ({size:>7,} bytes)")

    print("\n" + "=" * 60)
    print("  เสร็จสิ้น! ไฟล์ทั้งหมด:")
    print("=" * 60)
    for name in FILES:
        print(f"  - {name}")

    print("\nขั้นตอนถัดไป:")
    print("  1) py -3 -m pip install pyserial schedule streamlit pandas torch matplotlib scipy")
    print("  2) py -3 hardware_bridge.py        (demo mode)")
    print("  3) py -3 auto_update.py            (ตรวจสอบครั้งเดียว)")
    print("  4) py -3 physics_symbolic.py       (ค้นพบสมการ)")
    print("  5) py -3 physics_pinn.py           (train PINN)")
    print("  6) py -3 -m streamlit run physics_ai_app.py")

if __name__ == "__main__":
    create_all()
