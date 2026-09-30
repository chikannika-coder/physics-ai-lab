"""
╔══════════════════════════════════════════════════════════════╗
║  SatiARM — Simulation (Windows/Mac/Linux compatible)         ║
║  รันแล้วได้: dashboard PNG + animation GIF + popup แสดงผล     ║
╚══════════════════════════════════════════════════════════════╝

ติดตั้ง dependency ครั้งเดียว:
    pip install numpy matplotlib scipy pillow
"""

# ============================================================
# 0. จัดการ backend ก่อน import matplotlib.pyplot
# ============================================================
import matplotlib
# ใช้ TkAgg ถ้ามี (แสดงหน้าต่างได้) ไม่งั้น fallback
try:
    matplotlib.use('TkAgg')
except Exception:
    try:
        matplotlib.use('Qt5Agg')
    except Exception:
        matplotlib.use('Agg')  # ไม่มี GUI → บันทึกไฟล์อย่างเดียว

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from matplotlib.gridspec import GridSpec

import numpy as np
import os
import sys
from pathlib import Path
from scipy import stats
from scipy.signal import find_peaks

# ============================================================
# 1. โฟลเดอร์ปลายทาง — ใช้ได้ทุก OS
# ============================================================
def get_output_dir():
    """เลือกโฟลเดอร์บันทึก: ข้างไฟล์ .py ก่อน ถ้าเขียนไม่ได้ → Desktop → Home"""
    candidates = []
    try:
        candidates.append(Path(__file__).resolve().parent / "satiarm_output")
    except NameError:
        pass
    candidates.append(Path.home() / "Desktop" / "satiarm_output")
    candidates.append(Path.home() / "satiarm_output")
    candidates.append(Path.cwd() / "satiarm_output")

    for c in candidates:
        try:
            c.mkdir(parents=True, exist_ok=True)
            # ทดสอบเขียนได้
            test = c / ".write_test"
            test.write_text("ok", encoding="utf-8")
            test.unlink()
            return c
        except Exception:
            continue
    raise RuntimeError("ไม่พบโฟลเดอร์ที่เขียนได้")

OUTPUT_DIR = get_output_dir()
print(f"📁 โฟลเดอร์บันทึก: {OUTPUT_DIR}")

# ============================================================
# 2. ตั้งค่าฟอนต์ — ตรวจสอบว่ามีไทยหรือไม่
# ============================================================
def setup_font():
    """หาฟอนต์ไทย ถ้าไม่มี → คืน False เพื่อให้ใช้ภาษาอังกฤษ"""
    thai_fonts = [
        "Leelawadee UI", "Leelawadee", "Tahoma",
        "Sarabun", "Noto Sans Thai", "Angsana New",
        "TH Sarabun New", "Cordia New",
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in thai_fonts:
        if name in available:
            plt.rcParams['font.family'] = name
            print(f"✓ ฟอนต์ไทย: {name}")
            return True

    # ลองหาฟอนต์ที่มี glyph ไทย
    print("⚠ ไม่พบฟอนต์ไทยในระบบ → ใช้ภาษาอังกฤษแทน")
    plt.rcParams['font.family'] = 'DejaVu Sans'
    return False

HAS_THAI = setup_font()
plt.rcParams['axes.unicode_minus'] = False

# ตัวช่วยเลือกข้อความ ไทย/อังกฤษ
def T(th, en):
    return th if HAS_THAI else en

# ============================================================
# 3. Seed
# ============================================================
np.random.seed(42)

# ============================================================
# 4. Inverse Kinematics
# ============================================================
def ik_2link(x, y, L1, L2, elbow_up=True):
    r2 = x*x + y*y
    r = min(np.sqrt(r2), L1 + L2 - 1e-6)
    c2 = np.clip((r2 - L1**2 - L2**2) / (2*L1*L2), -1, 1)
    sign = 1 if elbow_up else -1
    theta2 = sign * np.arccos(c2)
    theta1 = np.arctan2(y, x) - np.arctan2(
        L2*np.sin(theta2), L1 + L2*np.cos(theta2)
    )
    return theta1, theta2

def fk_2link(t1, t2, L1, L2, origin=(0, 0)):
    x0, y0 = origin
    x1 = x0 + L1*np.cos(t1);  y1 = y0 + L1*np.sin(t1)
    x2 = x1 + L2*np.cos(t1+t2); y2 = y1 + L2*np.sin(t1+t2)
    return (x0, y0), (x1, y1), (x2, y2)

# ============================================================
# 5. สัญญาณ PPG จำลอง
# ============================================================
def simulate_ppg(duration_sec, hr_bpm, fs=100, noise=0.05):
    t = np.linspace(0, duration_sec, int(duration_sec*fs))
    f = hr_bpm/60.0
    s = (np.sin(2*np.pi*f*t)
         + 0.4*np.sin(4*np.pi*f*t)
         + 0.15*np.sin(6*np.pi*f*t))
    s += noise * np.random.randn(len(t))
    return t, s

def estimate_hrv(ppg, fs=100):
    peaks, _ = find_peaks(ppg, distance=fs*0.5)
    if len(peaks) < 3:
        return 0.0
    rr = np.diff(peaks) / fs * 1000
    return float(np.sqrt(np.mean(np.diff(rr)**2)))

# ============================================================
# 6. ข้อมูลทดลองจำลอง
# ============================================================
def simulate_experiment(n=30):
    pre_c  = np.random.normal(42, 10, n)
    pre_e  = np.random.normal(42, 10, n)
    post_c = pre_c + np.random.normal(2, 3, n)
    post_e = pre_e + np.random.normal(10, 4, n)
    return pre_c, post_c, pre_e, post_e

# ============================================================
# 7. Dashboard
# ============================================================
def plot_dashboard():
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

    # --- (A) System Architecture ---
    ax_a = fig.add_subplot(gs[0, :2])
    ax_a.set_xlim(0, 10); ax_a.set_ylim(0, 5)
    ax_a.axis('off')
    ax_a.set_title(T('(A) สถาปัตยกรรมระบบ', '(A) System Architecture'),
                   fontsize=13, fontweight='bold')

    boxes = [
        (0.3, 3.5, 2.4, 1.0, T('เซนเซอร์ชีพจร\n(MAX30102)', 'PPG Sensor\n(MAX30102)'), '#FFE0B2'),
        (0.3, 1.5, 2.4, 1.0, T('เซอร์โวมอเตอร์\n(x4-6)', 'Servo Motors\n(x4-6)'), '#B3E5FC'),
        (3.6, 2.5, 2.4, 1.6, T('ESP32\n(เรียลไทม์)', 'ESP32\n(Real-time MCU)'), '#C8E6C9'),
        (6.9, 2.5, 2.8, 1.6, T('Raspberry Pi 5\n(UI + AI + Data)', 'Raspberry Pi 5\n(UI + AI + Data)'), '#F8BBD0'),
    ]
    for x, y, w, h, label, color in boxes:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                             facecolor=color, edgecolor='black', lw=1.5)
        ax_a.add_patch(box)
        ax_a.text(x+w/2, y+h/2, label, ha='center', va='center',
                  fontsize=10, fontweight='bold')

    arrows = [
        (2.7, 4.0, 3.6, 3.6, 'I2C'),
        (6.0, 3.3, 6.9, 3.3, 'USB/Serial'),
        (3.6, 3.0, 2.7, 2.0, 'PWM'),
    ]
    for x1, y1, x2, y2, label in arrows:
        ax_a.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                       arrowstyle='->', mutation_scale=20,
                       color='black', lw=1.8))
        ax_a.text((x1+x2)/2 + 0.1, (y1+y2)/2 + 0.1, label,
                  fontsize=9, style='italic')

    ax_a.text(5, 0.5,
              T("การไหลข้อมูล: PPG → ESP32 → Pi 5 → (วิเคราะห์, UI)  ||  Pi 5 → ESP32 → Servo (นำจังหวะหายใจ)",
                "Data flow: PPG → ESP32 → Pi 5 → (analysis, UI)  ||  Pi 5 → ESP32 → Servo (breathing guide)"),
              ha='center', fontsize=10, style='italic', color='dimgray')

    # --- (B) PPG Signal ---
    ax_b = fig.add_subplot(gs[0, 2])
    t, ppg_pre = simulate_ppg(10, 75)
    _, ppg_post = simulate_ppg(10, 62)
    ax_b.plot(t[:500], ppg_pre[:500], color='crimson', lw=1,
              label=T('ก่อนฝึก (75 bpm)', 'Before (75 bpm)'))
    ax_b.plot(t[:500], ppg_post[:500] + 3, color='steelblue', lw=1,
              label=T('หลังฝึก (62 bpm)', 'After (62 bpm)'))
    ax_b.set_xlabel(T('เวลา (s)', 'Time (s)'))
    ax_b.set_ylabel('PPG (a.u.)')
    ax_b.set_title(T('(B) สัญญาณชีพ (จำลอง)', '(B) PPG Signal (simulated)'),
                   fontsize=12, fontweight='bold')
    ax_b.legend(fontsize=8); ax_b.grid(alpha=0.3)

    # --- (C) HRV Bar Chart ---
    ax_c = fig.add_subplot(gs[1, 0])
    pre_c, post_c, pre_e, post_e = simulate_experiment()
    means = [pre_c.mean(), post_c.mean(), pre_e.mean(), post_e.mean()]
    stds  = [pre_c.std(), post_c.std(), pre_e.std(), post_e.std()]
    labels = [T('ควบคุม\nก่อน', 'Ctrl\nPre'), T('ควบคุม\nหลัง', 'Ctrl\nPost'),
              T('SatiARM\nก่อน', 'SatiARM\nPre'), T('SatiARM\nหลัง', 'SatiARM\nPost')]
    colors = ['#FFCDD2', '#EF9A9A', '#BBDEFB', '#64B5F6']

    ax_c.bar(labels, means, yerr=stds, capsize=8,
             color=colors, edgecolor='black', lw=1.2)
    ax_c.set_ylabel('HRV (RMSSD, ms)')
    ax_c.set_title(T('(C) ผล HRV ก่อน-หลัง', '(C) HRV Before-After'),
                   fontsize=12, fontweight='bold')
    ax_c.grid(axis='y', alpha=0.3)
    for i, (m, s) in enumerate(zip(means, stds)):
        ax_c.text(i, m + s + 1, f'{m:.1f}', ha='center', fontsize=9)

    # --- (D) Statistics ---
    ax_d = fig.add_subplot(gs[1, 1])
    diff_ctrl = post_c - pre_c
    diff_exp  = post_e - pre_e
    t_c, p_c = stats.ttest_rel(post_c, pre_c)
    t_e, p_e = stats.ttest_rel(post_e, pre_e)
    d_c = diff_ctrl.mean() / diff_ctrl.std(ddof=1)
    d_e = diff_exp.mean()  / diff_exp.std(ddof=1)
    t_bg, p_bg = stats.ttest_ind(diff_exp, diff_ctrl)

    text = (
        f"Paired t-test (within):\n\n"
        f"Control:\n"
        f"  d = {diff_ctrl.mean():+.2f} ms\n"
        f"  t = {t_c:.2f}, p = {p_c:.3f}\n"
        f"  Cohen's d = {d_c:.2f}\n\n"
        f"SatiARM:\n"
        f"  d = {diff_exp.mean():+.2f} ms\n"
        f"  t = {t_e:.2f}, p = {p_e:.4f}\n"
        f"  Cohen's d = {d_e:.2f}\n\n"
        f"Between-group:\n"
        f"  t = {t_bg:.2f}, p = {p_bg:.4f}"
    )
    ax_d.text(0.02, 0.5, text, fontsize=10, family='monospace',
              va='center', transform=ax_d.transAxes)
    ax_d.axis('off')
    ax_d.set_title(T('(D) การวิเคราะห์ทางสถิติ', '(D) Statistical Analysis'),
                   fontsize=12, fontweight='bold')

    # --- (E) Concept Mock-up ---
    ax_e = fig.add_subplot(gs[1, 2])
    ax_e.set_xlim(0, 1); ax_e.set_ylim(0, 1)
    ax_e.axis('off')
    ax_e.set_title(T('(E) แนวคิด SatiARM', '(E) SatiARM Concept'),
                   fontsize=12, fontweight='bold')

    L1, L2 = 0.30, 0.24
    base = (0.2, 0.15)
    t1, t2 = ik_2link(0.55, 0.65, L1, L2)
    p0, p1, p2 = fk_2link(t1, t2, L1, L2, base)

    ax_e.plot([p0[0], p1[0]], [p0[1], p1[1]], 'o-',
              color='steelblue', lw=10, markersize=18,
              markerfacecolor='navy', zorder=3)
    ax_e.plot([p1[0], p2[0]], [p1[1], p2[1]], 'o-',
              color='steelblue', lw=8, markersize=14,
              markerfacecolor='navy', zorder=3)
    ax_e.plot(p2[0], p2[1], 'o', color='gold', markersize=22,
              markeredgecolor='orange', markeredgewidth=2.5, zorder=4)

    for r, alpha in [(0.20, 0.15), (0.13, 0.25)]:
        ax_e.add_patch(Circle(p2, r, color='skyblue', alpha=alpha, zorder=1))

    ax_e.text(0.5, 0.97,
              T('หายใจเข้า 4s → หยุด → หายใจออก 4s',
                'Inhale 4s → hold → Exhale 4s'),
              ha='center', fontsize=9, style='italic')

    out_png = OUTPUT_DIR / 'satiarm_dashboard.png'
    plt.savefig(out_png, dpi=150, bbox_inches='tight')
    print(f"✓ บันทึก dashboard: {out_png}")

    return fig  # ส่งกลับเพื่อ show ได้

# ============================================================
# 8. Animation
# ============================================================
def animate_arm(duration=16, fps=30, show=False):
    """
    สร้าง GIF แสดงแขนกลขยับตามจังหวะหายใจ
    1 รอบ = 8 วินาที (เข้า 4s, ออก 4s)
    """
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(-0.5, 1.8)
    ax.set_ylim(-0.3, 2.0)
    ax.set_aspect('equal')
    ax.axis('off')

    L1, L2 = 1.0, 0.8
    base = (0, 0)

    # พื้น
    ax.add_patch(plt.Rectangle((-0.5, -0.15), 2.3, 0.15,
                                color='#4A4A4A', zorder=0))
    # ฐาน
    ax.plot(base[0], base[1], 's', color='black', markersize=22, zorder=5)

    # วงกลมหายใจ
    breathing_circle = Circle((1.0, 1.0), 0.30,
                              fill=False, color='skyblue',
                              lw=2.5, alpha=0.7, zorder=1)
    ax.add_patch(breathing_circle)

    # แขนกล
    arm_line, = ax.plot([], [], 'o-', color='steelblue',
                        lw=10, markersize=20,
                        markerfacecolor='navy', zorder=3)
    effector, = ax.plot([], [], 'o', color='gold',
                        markersize=24, markeredgecolor='orange',
                        markeredgewidth=3, zorder=4)

    phase_text = ax.text(0.65, 1.88, '', ha='center',
                         fontsize=16, fontweight='bold')
    countdown = ax.text(0.65, 1.70, '', ha='center',
                        fontsize=12, color='dimgray')

    T_BREATH = 8.0
    INHALE_TXT  = T('🫁 หายใจเข้า (Inhale)',  '🫁 Inhale')
    EXHALE_TXT  = T('💨 หายใจออก (Exhale)',   '💨 Exhale')
    REMAIN_TXT  = T('อีก {:.1f} วินาที',       'next phase in {:.1f}s')

    def update(frame):
        t = frame / fps
        phase = 2 * np.pi * t / T_BREATH

        y_target = 1.0 + 0.45 * np.sin(phase)
        x_target = 1.0

        t1, t2 = ik_2link(x_target, y_target, L1, L2)
        p0, p1, p2 = fk_2link(t1, t2, L1, L2, base)

        arm_line.set_data([p0[0], p1[0], p2[0]],
                          [p0[1], p1[1], p2[1]])
        effector.set_data([p2[0]], [p2[1]])

        r = 0.25 + 0.18 * np.sin(phase)
        breathing_circle.set_radius(r)
        breathing_circle.center = (p2[0], p2[1])

        half = t % T_BREATH
        if half < 4:
            phase_text.set_text(INHALE_TXT)
            phase_text.set_color('seagreen')
            remaining = 4 - half
        else:
            phase_text.set_text(EXHALE_TXT)
            phase_text.set_color('steelblue')
            remaining = 8 - half

        countdown.set_text(REMAIN_TXT.format(remaining))
        return arm_line, effector, breathing_circle, phase_text, countdown

    n_frames = duration * fps
    anim = FuncAnimation(fig, update, frames=n_frames,
                         interval=1000/fps, blit=True, repeat=True)

    # บันทึก GIF
    out_gif = OUTPUT_DIR / 'satiarm_animation.gif'
    print(f"⏳ กำลังสร้าง GIF ({n_frames} frames)... (ใช้เวลาสักครู่)")
    anim.save(str(out_gif), writer=PillowWriter(fps=fps))
    print(f"✓ บันทึก animation: {out_gif}")

    # แสดง popup ถ้าต้องการ
    if show:
        try:
            plt.show()
        except Exception as e:
            print(f"⚠ ไม่สามารถแสดงหน้าต่างได้: {e}")

    plt.close(fig)
    return anim

# ============================================================
# 9. Main
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("  SatiARM Simulation")
    print("=" * 65)

    # --- Dashboard ---
    print("\n[1/2] สร้าง Dashboard...")
    fig_dash = plot_dashboard()

    # --- Animation ---
    print("\n[2/2] สร้าง Animation...")
    animate_arm(duration=16, fps=30, show=False)

    print("\n" + "=" * 65)
    print("  ✅ เสร็จแล้ว! ไฟล์อยู่ในโฟลเดอร์:")
    print(f"     {OUTPUT_DIR}")
    print("=" * 65)

    # แสดง dashboard popup
    try:
        print("\n💡 กำลังเปิดหน้าต่าง dashboard... (ปิดเพื่อจบโปรแกรม)")
        plt.figure(fig_dash.number)
        plt.show()
    except Exception as e:
        print(f"⚠ ไม่สามารถแสดงหน้าต่างได้: {e}")
        print(f"   เปิดไฟล์เอง: {OUTPUT_DIR / 'satiarm_dashboard.png'}")
        print(f"   เปิด GIF:   {OUTPUT_DIR / 'satiarm_animation.gif'}")

    print("\n📂 ไฟล์ที่ได้:")
    for f in sorted(OUTPUT_DIR.iterdir()):
        print(f"   • {f.name}")