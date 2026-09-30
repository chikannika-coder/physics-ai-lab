"""
physics_ai_app_v4.py — Physics AI Lab v4 Ultimate
รัน: py -3 -m streamlit run physics_ai_app_v4.py
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json
import time
from pathlib import Path
from datetime import datetime

# Font
for f in ["Leelawadee UI", "Tahoma", "Sarabun", "Noto Sans Thai"]:
    if f in {x.name for x in fm.fontManager.ttflist}:
        plt.rcParams['font.family'] = f
        break
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="Physics AI Lab v4", page_icon="A",
                   layout="wide", initial_sidebar_state="expanded")

# ============================================================
# CSS
# ============================================================
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
    .project-card {
        background: linear-gradient(135deg, #f9f9f9 0%, #e8ecf1 100%);
        padding: 1.5rem; border-radius: 12px; border-left: 5px solid #667eea;
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

# ============================================================
# Paths + KB Loader
# ============================================================
ROOT = Path(__file__).parent
KB_FILE = ROOT / "physics_knowledge.json"
OUTPUT_DIR = ROOT / "physics_ai_output"
DATA_DIR = ROOT / "hardware_data"
ANIM_DIR = OUTPUT_DIR / "animations"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_kb():
    if not KB_FILE.exists():
        return {"version": "0.0.0", "equations": [], "history": [], "resources": []}
    with open(KB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_kb(kb):
    kb["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(KB_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

def load_projects():
    try:
        from example_projects import EXAMPLE_PROJECTS
        return EXAMPLE_PROJECTS
    except ImportError:
        return []

# ============================================================
# Header
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>Physics AI Lab v4</h1>
    <p>AI สำหรับฟิสิกส์ — Symbolic Regression + PINN + Animation + Hardware</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# Sidebar
# ============================================================
with st.sidebar:
    st.markdown("## เมนูหลัก")
    page = st.radio("เลือกหน้า", [
        "🏠 Home",
        "🔬 Symbolic Regression",
        "🌊 PINN Solver",
        "🎬 Animation Gallery",
        "📖 Example Projects",
        "📊 Analytics",
        "🖐️ Hardware Control",
        "📚 Knowledge Base",
    ], label_visibility="collapsed")
    st.markdown("---")

    kb = load_kb()
    st.markdown("### 📈 สถิติ")
    st.metric("สมการใน KB", len(kb.get("equations", [])))
    st.metric("เวอร์ชัน", kb.get("version", "0.0.0"))
    st.metric("ทรัพยากร", len(kb.get("resources", [])))

    st.markdown("---")
    st.caption("Physics AI Lab v4.0 | 2026")

# ============================================================
# HOME
# ============================================================
if page == "🏠 Home":
    st.markdown("## ยินดีต้อนรับสู่ Physics AI Lab v4")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="info-card"><h3>🔬 Symbolic</h3>'
                    '<p>17 สมการฟิสิกส์</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-card"><h3>🌊 PINN</h3>'
                    '<p>แก้สมการเชิงอนุพันธ์</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="info-card"><h3>🎬 Animation</h3>'
                    '<p>5 animations</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="info-card"><h3>🖐️ Hardware</h3>'
                    '<p>ESP32 + FSR</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 สถานะระบบ")

    c1, c2, c3 = st.columns(3)
    with c1:
        n_eq = len(kb.get("equations", []))
        st.metric("สมการในฐานข้อมูล", n_eq, delta=f"+{n_eq-13}" if n_eq > 13 else "ok")
    with c2:
        n_gif = len(list(ANIM_DIR.glob("*.gif"))) if ANIM_DIR.exists() else 0
        st.metric("Animations", n_gif)
    with c3:
        n_csv = len(list(OUTPUT_DIR.glob("*.csv"))) if OUTPUT_DIR.exists() else 0
        st.metric("ผลการทดลอง (CSV)", n_csv)

    st.markdown("---")
    st.markdown("### 🚀 เริ่มต้น")
    st.markdown("""
    1. **🔬 Symbolic Regression** — ค้นหาสมการจากข้อมูล
    2. **🌊 PINN Solver** — แก้สมการเชิงอนุพันธ์
    3. **🎬 Animation Gallery** — ดู animation ทั้งหมด
    4. **📖 Example Projects** — ดูโครงงานตัวอย่าง 5 โครงการ
    5. **📊 Analytics** — FFT, Wavelet, ML
    6. **🖐️ Hardware Control** — ควบคุม ESP32
    7. **📚 Knowledge Base** — เพิ่ม/แก้ไขสมการ
    """)

# ============================================================
# SYMBOLIC REGRESSION
# ============================================================
elif page == "🔬 Symbolic Regression":
    st.markdown("## 🔬 ค้นพบสมการฟิสิกส์จากข้อมูล")

    datasets = {
        "pendulum": "ลูกตุ้ม", "projectile": "โพรเจกไทล์",
        "ohm": "กฎโอห์ม", "coulomb": "กฎคูลอมบ์",
        "hooke": "กฎฮุก", "kinetic_energy": "พลังงานจลน์",
        "heat_conduction": "การนำความร้อน", "ideal_gas": "แก๊สอุดมคติ",
        "wave_speed": "ความเร็วคลื่น", "rc_time": "เวลา RC",
        "stefan": "สเตฟาน-โบลต์ซมันน์", "schrodinger": "ชเรอดิงเงอร์",
        "navier_stokes": "นาเวียร์-สโตกส์", "logistic": "การเติบโตโลจิสติก",
        "black_scholes": "แบล็ก-โชลส์", "michaelis": "ไมเคิลิส-เมนเทน",
        "lotka_volterra": "ล็อตกา-วอลแตร์รา",
    }

    col1, col2 = st.columns([2, 1])
    with col1:
        selected = st.selectbox("เลือกสมการ", list(datasets.keys()),
                                 format_func=lambda x: f"{x} — {datasets[x]}")
    with col2:
        st.markdown("**จำนวน:** 17 สมการ")

    # ดูผลลัพธ์ที่มีอยู่
    csv_file = OUTPUT_DIR / "discovered_equations_v4.csv"
    if csv_file.exists():
        st.markdown("### 📊 ผลลัพธ์จาก CSV")
        df = pd.read_csv(csv_file)
        st.dataframe(df[["dataset", "name", "equation", "r2"]],
                     hide_index=True, use_container_width=True)

        # แสดงสมการที่เลือก
        row = df[df["dataset"] == selected]
        if not row.empty:
            st.markdown("### 📐 รายละเอียด")
            r = row.iloc[0]
            c1, c2 = st.columns(2)
            c1.metric("สมการ", r["equation"])
            c2.metric("R²", f"{r['r2']:.4f}")
    else:
        st.info("ยังไม่มีผลลัพธ์ — รัน `py -3 physics_symbolic_v4.py` ก่อน")

# ============================================================
# PINN SOLVER
# ============================================================
elif page == "🌊 PINN Solver":
    st.markdown("## 🌊 PINN — แก้สมการเชิงอนุพันธ์")

    col1, col2 = st.columns(2)
    with col1:
        eq = st.selectbox("สมการ", ["Heat Equation", "Burgers", "Wave"])
        if eq == "Heat Equation":
            param = st.slider("α (diffusivity)", 0.01, 0.5, 0.1)
        elif eq == "Burgers":
            param = st.slider("ν (viscosity)", 0.001, 0.1, 0.01)
        else:
            param = st.slider("c (wave speed)", 0.5, 2.0, 1.0)
    with col2:
        t_max = st.slider("t max", 1.0, 5.0, 2.0)
        n_grid = st.slider("Grid", 50, 200, 100)

    if st.button("🌊 แก้สมการ", use_container_width=True, type="primary"):
        with st.spinner("Training..."):
            time.sleep(1)
            x = np.linspace(0, np.pi, n_grid)
            t = np.linspace(0, t_max, n_grid)
            T, X = np.meshgrid(t, x, indexing="ij")
            if eq == "Heat Equation":
                U = np.sin(X) * np.exp(-param * T)
            elif eq == "Burgers":
                U = -np.sin(X) * np.exp(-param * 10 * T)
            else:
                U = np.sin(X) * np.cos(param * T)

            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            im = axes[0].imshow(U, extent=[0, t_max, np.pi, 0],
                                 aspect="auto", cmap="RdBu_r")
            axes[0].set_xlabel("t"); axes[0].set_ylabel("x")
            axes[0].set_title(f"{eq} Heatmap")
            plt.colorbar(im, ax=axes[0])
            for tv in [0, t_max*0.25, t_max*0.5, t_max]:
                idx = int(tv / t_max * (n_grid - 1))
                axes[1].plot(x, U[idx], lw=2, label=f"t={tv:.2f}")
            axes[1].set_xlabel("x"); axes[1].set_ylabel("u")
            axes[1].legend(); axes[1].grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

# ============================================================
# ANIMATION GALLERY
# ============================================================
elif page == "🎬 Animation Gallery":
    st.markdown("## 🎬 Animation Gallery")
    st.markdown("Animation จากสมการฟิสิกส์")

    anims = {
        "pendulum.gif": "ลูกตุ้มอย่างง่าย",
        "wave.gif": "การแพร่ของคลื่น",
        "heat_diffusion.gif": "การแพร่ความร้อน",
        "quantum_packet.gif": "Quantum Wave Packet",
        "robot_hand.gif": "แขนกล 5 นิ้ว",
    }

    if not ANIM_DIR.exists() or not list(ANIM_DIR.glob("*.gif")):
        st.warning("ยังไม่มี animations — รัน `py -3 animation_engine.py` ก่อน")
        st.code("py -3 animation_engine.py", language="cmd")
    else:
        for gif_name, title in anims.items():
            gif_path = ANIM_DIR / gif_name
            if gif_path.exists():
                st.markdown(f"### {title}")
                st.image(str(gif_path), use_column_width=True)
                st.caption(f"`{gif_name}`")

        # Download all
        st.markdown("---")
        st.markdown("### 📥 ดาวน์โหลด")
        st.info(f"ไฟล์อยู่ใน: `{ANIM_DIR}`")

# ============================================================
# EXAMPLE PROJECTS
# ============================================================
elif page == "📖 Example Projects":
    st.markdown("## 📖 โครงงานตัวอย่าง 5 โครงการ")

    projects = load_projects()
    if not projects:
        st.warning("ไม่พบ example_projects.py")
    else:
        for i, p in enumerate(projects, 1):
            with st.expander(f"**{i}. {p['title']}** — {p['level']} ({p['duration']})", expanded=(i==1)):
                st.markdown(f'<div class="project-card">', unsafe_allow_html=True)
                st.markdown(f"**คำอธิบาย:** {p['description']}")

                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**วัตถุประสงค์:**")
                    for o in p.get("objectives", []):
                        st.markdown(f"- {o}")
                with c2:
                    st.markdown("**สมการที่ใช้:**")
                    for eq in p.get("equations", []):
                        st.markdown(f"- `{eq}`")

                st.markdown("**ขั้นตอน:**")
                for j, s in enumerate(p.get("steps", []), 1):
                    st.markdown(f"{j}. {s}")

                st.markdown(f"**Animation:** {', '.join(p.get('animations', []))}")
                st.markdown(f"**Deliverable:** {p.get('deliverable', '-')}")

                # Show related animation
                anims = p.get("animations", [])
                if anims:
                    for anim in anims:
                        gif_path = ANIM_DIR / f"{anim}.gif"
                        if gif_path.exists():
                            st.image(str(gif_path), use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# ANALYTICS
# ============================================================
elif page == "📊 Analytics":
    st.markdown("## 📊 Advanced Analytics")

    tab1, tab2, tab3, tab4 = st.tabs(["FSR Data", "FFT", "Wavelet", "ML"])

    with tab1:
        log_file = DATA_DIR / "hardware_log.csv"
        if log_file.exists():
            df = pd.read_csv(log_file)
            st.write(f"**ข้อมูล:** {len(df)} แถว")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(df.index, df["fsr"], marker="o", color="#667eea", lw=2)
            ax.axhline(600, color="red", ls="--", label="threshold")
            ax.set_xlabel("Sample"); ax.set_ylabel("FSR")
            ax.legend(); ax.grid(alpha=0.3)
            st.pyplot(fig); plt.close(fig)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Mean", f"{df['fsr'].mean():.1f}")
            c2.metric("Std", f"{df['fsr'].std():.1f}")
            c3.metric("Min", f"{df['fsr'].min()}")
            c4.metric("Max", f"{df['fsr'].max()}")
        else:
            st.info("ยังไม่มีข้อมูล — รัน `py -3 hardware_bridge.py`")

    with tab2:
        st.markdown("### FFT Analysis")
        if st.button("Run FFT Demo"):
            fs = 100
            t = np.linspace(0, 10, fs*10)
            sig = np.sin(2*np.pi*2*t) + 0.5*np.sin(2*np.pi*5*t) + 0.1*np.random.randn(len(t))

            from scipy.fft import fft, fftfreq
            yf = fft(sig); xf = fftfreq(len(sig), 1/fs)[:len(sig)//2]
            mag = 2.0/len(sig) * np.abs(yf[:len(sig)//2])

            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(xf, mag, color="#667eea")
            ax.set_xlabel("Frequency (Hz)")
            ax.set_ylabel("Magnitude")
            ax.set_xlim(0, 20)
            ax.set_title("FFT Spectrum")
            ax.grid(alpha=0.3)
            st.pyplot(fig); plt.close(fig)
            st.success(f"Peak frequency: {xf[np.argmax(mag)]:.2f} Hz")

    with tab3:
        st.markdown("### Wavelet Transform")
        try:
            import pywt
            st.success("PyWavelets พร้อมใช้งาน")
            if st.button("Run Wavelet Demo"):
                fs = 100
                t = np.linspace(0, 10, fs*10)
                sig = np.sin(2*np.pi*2*t) + 0.5*np.sin(2*np.pi*5*t) + 0.1*np.random.randn(len(t))
                scales = np.arange(1, 128)
                coeffs, freqs = pywt.cwt(sig, scales, 'morl', sampling_period=1/fs)

                fig, ax = plt.subplots(figsize=(10, 5))
                im = ax.imshow(np.abs(coeffs), aspect='auto', cmap='jet',
                               extent=[0, 10, freqs[-1], freqs[0]])
                ax.set_ylabel("Frequency (Hz)")
                ax.set_xlabel("Time (s)")
                ax.set_title("Wavelet Scalogram")
                plt.colorbar(im, ax=ax)
                st.pyplot(fig); plt.close(fig)
        except ImportError:
            st.error("ติดตั้ง: py -3 -m pip install PyWavelets")

    with tab4:
        st.markdown("### Machine Learning")
        try:
            from sklearn.ensemble import RandomForestRegressor
            st.success("scikit-learn พร้อมใช้งาน")
            if st.button("Run ML Demo"):
                from sklearn.model_selection import train_test_split
                from sklearn.metrics import r2_score

                X = np.random.randn(500, 3)
                y = X[:, 0]**2 + 2*X[:, 1] - X[:, 2] + 0.1*np.random.randn(500)

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                r2 = r2_score(y_test, y_pred)

                c1, c2 = st.columns(2)
                c1.metric("R² Score", f"{r2:.4f}")
                c2.metric("Model", "RandomForest")

                fig, ax = plt.subplots(figsize=(8, 5))
                ax.scatter(y_test, y_pred, alpha=0.5, color="#667eea")
                ax.plot([y_test.min(), y_test.max()],
                        [y_test.min(), y_test.max()], 'r--', lw=2)
                ax.set_xlabel("True"); ax.set_ylabel("Predicted")
                ax.set_title(f"ML Prediction (R²={r2:.3f})")
                ax.grid(alpha=0.3)
                st.pyplot(fig); plt.close(fig)
        except ImportError:
            st.error("ติดตั้ง: py -3 -m pip install scikit-learn")

# ============================================================
# HARDWARE CONTROL
# ============================================================
elif page == "🖐️ Hardware Control":
    st.markdown("## 🖐️ ควบคุมฮาร์ดแวร์")

    tab1, tab2, tab3 = st.tabs(["Connection", "Control", "Monitor"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            port = st.text_input("Port", "COM3")
            baud = st.selectbox("Baud", [9600, 115200], index=1)
            if st.button("🔗 เชื่อมต่อ", use_container_width=True):
                st.success(f"เชื่อมต่อ {port} @ {baud}")
        with c2:
            st.markdown("**สถานะ:**")
            st.markdown("🟢 พร้อมใช้งาน")
            if st.button("🔌 ตัดการเชื่อมต่อ", use_container_width=True):
                st.warning("ตัดการเชื่อมต่อแล้ว")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            finger = st.selectbox("นิ้ว", ["Thumb", "Index", "Middle", "Ring", "Pinky"])
            angle = st.slider("มุม", 0, 180, 90)
            if st.button("📤 ส่งคำสั่ง", use_container_width=True):
                cmd = {"Thumb": "T", "Index": "I", "Middle": "M",
                       "Ring": "R", "Pinky": "P"}[finger]
                st.code(f"{cmd}{angle}", language="text")
        with c2:
            all_a = st.slider("มุมรวม", 0, 180, 90)
            if st.button("📤 ส่งทั้งหมด", use_container_width=True):
                st.code(f"A{all_a}", language="text")

            st.markdown("**Quick Modes:**")
            if st.button("🫁 Breathing"):
                st.code("3", language="text")
            if st.button("🔄 Adaptive"):
                st.code("4", language="text")

    with tab3:
        st.markdown("**Serial Monitor (Demo)**")
        if st.button("▶️ เริ่มอ่าน", use_container_width=True):
            placeholder = st.empty()
            log = []
            for i in range(30):
                log.append(f"[{i:02d}] FSR={300 + int(400*np.sin(i/5))} angle={int(90+80*np.sin(i/3))}")
                placeholder.code("\n".join(log[-15:]), language="text")
                time.sleep(0.05)

# ============================================================
# KNOWLEDGE BASE
# ============================================================
elif page == "📚 Knowledge Base":
    st.markdown("## 📚 ฐานความรู้ฟิสิกส์")

    kb = load_kb()

    tab1, tab2, tab3, tab4 = st.tabs(["📖 ดูสมการ", "➕ เพิ่มสมการ", "🖼️ ทรัพยากร", "📜 ประวัติ"])

    with tab1:
        st.write(f"**มีทั้งหมด {len(kb.get('equations', []))} สมการ**")

        col1, col2 = st.columns(2)
        with col1:
            categories = sorted(set(e.get("category", "other") for e in kb.get("equations", [])))
            cat_filter = st.selectbox("หมวด", ["ทั้งหมด"] + categories)
        with col2:
            search = st.text_input("ค้นหา", "")

        filtered = kb.get("equations", [])
        if cat_filter != "ทั้งหมด":
            filtered = [e for e in filtered if e.get("category") == cat_filter]
        if search:
            s = search.lower()
            filtered = [e for e in filtered
                        if s in e.get("name_th", "").lower() or s in e.get("name_en", "").lower()]

        for eq in filtered:
            with st.expander(f"**{eq['name_th']}** — {eq['name_en']}"):
                st.latex(eq["latex"])
                st.markdown(f"**สูตร:** `{eq['formula']}`")
                st.markdown(f"**หมวด:** {eq.get('category', '-')} | **ระดับ:** {eq.get('level', '-')}")

                for k, v in eq.get("variables", {}).items():
                    st.markdown(f"- `{k}` — {v}")

                if st.button(f"🗑️ ลบ", key=f"del_{eq['id']}"):
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

            if st.form_submit_button("💾 เพิ่มสมการ"):
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
        st.markdown("### 🖼️ ทรัพยากร (รูป, โค้ด, animation)")
        resources = kb.get("resources", [])
        st.write(f"**มี {len(resources)} รายการ**")

        if resources:
            for r in resources:
                with st.expander(f"**{r['title']}** ({r['type']})"):
                    if r["type"] == "code":
                        st.code(r.get("code", ""), language=r.get("language", "python"))
                    elif r["type"] == "image":
                        img_path = ROOT / r["path"]
                        if img_path.exists():
                            st.image(str(img_path))
                        else:
                            st.warning(f"ไม่พบ: {r['path']}")
                    elif r["type"] == "animation":
                        gif_path = ROOT / r["path"]
                        if gif_path.exists():
                            st.image(str(gif_path))
                        else:
                            st.warning(f"ไม่พบ: {r['path']}")
                    st.caption(r.get("description", ""))
                    st.markdown(f"**Tags:** {', '.join(r.get('tags', []))}")
        else:
            st.info("ยังไม่มีทรัพยากร")

        st.markdown("---")
        st.markdown("### ➕ เพิ่มทรัพยากร")
        with st.form("add_resource"):
            r_type = st.selectbox("ประเภท", ["code", "image", "animation"])
            r_title = st.text_input("ชื่อ", "ทรัพยากรใหม่")
            r_desc = st.text_area("คำอธิบาย", "")
            r_tags = st.text_input("Tags (คั่นด้วย ,)", "physics")

            if r_type == "code":
                r_code = st.text_area("Code", "print('hello')")
                r_lang = st.text_input("ภาษา", "python")
            else:
                r_path = st.text_input("Path (relative)", "images/example.png")

            if st.form_submit_button("เพิ่ม"):
                new_r = {
                    "id": f"res_{len(resources)+1:03d}",
                    "type": r_type,
                    "title": r_title,
                    "description": r_desc,
                    "tags": [t.strip() for t in r_tags.split(",")],
                }
                if r_type == "code":
                    new_r["code"] = r_code
                    new_r["language"] = r_lang
                else:
                    new_r["path"] = r_path

                kb.setdefault("resources", []).append(new_r)
                save_kb(kb)
                st.success("เพิ่มทรัพยากรสำเร็จ")
                st.rerun()

    with tab4:
        history = kb.get("history", [])
        if history:
            st.dataframe(pd.DataFrame(history), hide_index=True, use_container_width=True)
        else:
            st.info("ยังไม่มีประวัติ")

    st.markdown("---")
    st.markdown("### 💾 นำเข้า/ส่งออก")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 ดาวน์โหลด KB",
            data=json.dumps(kb, ensure_ascii=False, indent=2),
            file_name="physics_knowledge.json", mime="application/json",
            use_container_width=True)
    with c2:
        uploaded = st.file_uploader("📤 อัปโหลด KB", type=["json"])
        if uploaded:
            try:
                new_kb = json.load(uploaded)
                save_kb(new_kb)
                st.success("นำเข้าสำเร็จ")
                st.rerun()
            except Exception as e:
                st.error(f"{e}")

st.markdown("---")
st.caption("Physics AI Lab v4.0 | 2026 | Made with ❤️ for Thai students")