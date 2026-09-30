# create_app.py — สร้างไฟล์ app_fsr.py อัตโนมัติ
from pathlib import Path

CODE = r'''"""
SatiARM FSR Dashboard
รัน: py -3 -m streamlit run app_fsr.py
"""
import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

st.set_page_config(page_title="SatiARM FSR", page_icon="H", layout="wide")

@st.cache_resource
def setup_font():
    for f in ["Leelawadee UI", "Tahoma", "Sarabun", "Noto Sans Thai"]:
        if f in {x.name for x in fm.fontManager.ttflist}:
            plt.rcParams["font.family"] = f
            plt.rcParams["axes.unicode_minus"] = False
            return True
    plt.rcParams["family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False
    return False

HAS_THAI = setup_font()
def T(th, en): return th if HAS_THAI else en

st.title("SatiARM - FSR Simulation Dashboard")
st.caption(T("แบบจำลองแขนกล + เซ็นเซอร์วัดแรงกด",
             "Robotic hand + Force-Sensitive Resistor simulation"))

with st.sidebar:
    st.header(T("ตั้งค่า", "Settings"))
    T_BREATH = st.slider(T("คาบหายใจ (s)", "Breath period (s)"), 4, 12, 8)
    THRESHOLD = st.slider("FSR threshold", 200, 900, 600, 50)
    DURATION = st.slider(T("ระยะเวลา (s)", "Duration (s)"), 4, 24, 16)
    t_now = st.slider(T("เวลา (s)", "Time (s)"), 0.0, float(DURATION), 6.0, 0.1)

def simulate(t, T_BREATH, threshold):
    phase = 2 * np.pi * t / T_BREATH
    breath = np.sin(phase)
    u_val = np.exp(-0.25 * t)
    base_curl = 0.5 + 0.5 * breath
    if 4 <= t <= 10:
        user_force = np.sin(np.pi * (t - 4) / 6) * 0.9
    else:
        user_force = 0.0
    fsr = {}
    for name in ["Thumb", "Index", "Middle", "Ring", "Pinky"]:
        fsr[name] = float(np.clip(base_curl * user_force * 1023, 0, 1023))
    max_f = max(fsr.values())
    if max_f > threshold:
        excess = (max_f - threshold) / (1023 - threshold)
        curl = base_curl * (1 - 0.7 * excess)
        mode = "ADAPTIVE RELEASE"
    else:
        curl = base_curl
        mode = "INHALE" if breath >= 0 else "EXHALE"
    return breath, u_val, curl, fsr, mode, user_force

breath, u_val, curl, fsr, mode, user_force = simulate(t_now, T_BREATH, THRESHOLD)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(T("สถานะ", "State"))
    if mode == "ADAPTIVE RELEASE":
        st.error("WARNING: " + mode)
    elif mode == "INHALE":
        st.success("INHALE - " + T("กำมือ", "grasp"))
    else:
        st.info("EXHALE - " + T("แบมือ", "release"))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("curl", f"{curl:.2f}")
    c2.metric("u(t)", f"{u_val:.3f}")
    c3.metric("breath", f"{breath:+.2f}")
    c4.metric("user force", f"{user_force:.2f}")
    fsr_df = pd.DataFrame({
        "Finger": list(fsr.keys()),
        "FSR": [int(v) for v in fsr.values()],
        "Status": ["OVER" if v > THRESHOLD else "OK" for v in fsr.values()],
    })
    st.dataframe(fsr_df, hide_index=True, use_container_width=True)

with col2:
    st.subheader(T("กราฟ FSR", "FSR Readings"))
    fig, ax = plt.subplots(figsize=(6, 3.5))
    colors = ["#E74C3C", "#3498DB", "#2ECC71", "#F1C40F", "#9B59B6"]
    names = list(fsr.keys())
    vals = [fsr[n] for n in names]
    bar_colors = ["red" if v > THRESHOLD else c for v, c in zip(vals, colors)]
    ax.barh(names, vals, color=bar_colors, edgecolor="black")
    ax.axvline(THRESHOLD, color="red", ls="--", lw=2,
               label=f"threshold={THRESHOLD}")
    ax.set_xlim(0, 1023)
    ax.set_xlabel("FSR value (0-1023)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3, axis="x")
    st.pyplot(fig)
    plt.close(fig)

st.subheader(T("กราฟเวลา", "Time Series"))
t_arr = np.linspace(0, DURATION, 200)
breaths, curls, max_fsrs = [], [], []
for t in t_arr:
    b, _, c, f, _, _ = simulate(t, T_BREATH, THRESHOLD)
    breaths.append(b)
    curls.append(c)
    max_fsrs.append(max(f.values()))

fig, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(t_arr, breaths, color="#2E86AB", lw=2, label="breath")
ax1.plot(t_arr, curls, color="#27AE60", lw=2, label="curl (adaptive)")
ax1.axhline(0, color="gold", ls="--", alpha=0.5)
ax1.set_xlabel(T("เวลา (s)", "Time (s)"))
ax1.set_ylabel("breath / curl", color="#2E86AB")
ax1.tick_params(axis="y", labelcolor="#2E86AB")
ax1.grid(alpha=0.3)

ax2 = ax1.twinx()
ax2.plot(t_arr, max_fsrs, color="crimson", lw=2, label="max FSR")
ax2.axhline(THRESHOLD, color="red", ls="--", lw=2, alpha=0.7)
ax2.set_ylabel("max FSR", color="crimson")
ax2.tick_params(axis="y", labelcolor="crimson")

ax1.axvline(t_now, color="black", ls=":", lw=1.5, alpha=0.6,
            label=f"now = {t_now}s")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=9)
st.pyplot(fig)
plt.close(fig)
'''

out = Path(__file__).parent / "app_fsr.py"
out.write_text(CODE, encoding="utf-8")
print(f"Created: {out}")
print(f"Size: {out.stat().st_size} bytes")
print()
print("Next steps:")
print('  1) py -3 -m pip install streamlit pandas')
print('  2) py -3 -m streamlit run app_fsr.py')