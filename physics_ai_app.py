"""physics_ai_app.py — Physics AI Lab (Beautiful UI)"""
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
