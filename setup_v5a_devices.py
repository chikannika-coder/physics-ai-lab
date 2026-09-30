"""setup_v5a_devices.py — สร้าง physics_devices.py"""
from pathlib import Path
ROOT = Path(__file__).parent

CODE = r'''"""
physics_devices.py - อุปกรณ์ฟิสิกส์จาก ทบ. + Animation
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import (Circle, Rectangle, FancyArrowPatch,
                                 FancyBboxPatch, Polygon, Arc, Wedge)
from pathlib import Path

OUT_DIR = Path(__file__).parent / "physics_ai_output" / "devices"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. ลูกตุ้มอย่างง่าย (Simple Pendulum)
# ============================================================
def anim_pendulum_device():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.6, 0.3)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Simple Pendulum", fontsize=13, fontweight="bold")
    ax.plot([-0.3, 0.3], [0, 0], color="black", lw=3)
    line, = ax.plot([], [], "o-", color="#667eea", lw=3,
                    markersize=18, markerfacecolor="navy")
    angle_text = ax.text(0, -1.5, "", ha="center", fontsize=11)
    L = 1.0; g = 9.81
    # แก้สมการ: theta(t) = theta0 * cos(sqrt(g/L) * t)
    ax2.set_xlim(0, 4); ax2.set_ylim(-1.2, 1.2)
    ax2.set_xlabel("t (s)"); ax2.set_ylabel("theta (rad)")
    ax2.set_title("T = 2*pi*sqrt(L/g)", fontsize=12)
    ax2.grid(alpha=0.3); ax2.axhline(0, color="gray", ls="--", lw=0.5)
    curve, = ax2.plot([], [], color="#764ba2", lw=2)
    t_arr = np.linspace(0, 4, 200)
    theta_arr = 0.5 * np.cos(np.sqrt(g/L) * t_arr)
    def update(frame):
        t = frame / 25
        theta = 0.5 * np.cos(np.sqrt(g/L) * t)
        x = L * np.sin(theta); y = -L * np.cos(theta)
        line.set_data([0, x], [0, y])
        angle_text.set_text(f"t = {t:.2f}s | theta = {theta:.3f} rad")
        curve.set_data(t_arr[t_arr <= t], theta_arr[t_arr <= t])
        return line, angle_text, curve
    anim = FuncAnimation(fig, update, frames=100, interval=40, blit=True)
    out = OUT_DIR / "device_pendulum.gif"
    anim.save(str(out), writer=PillowWriter(fps=25)); plt.close()
    print(f"[OK] {out}")
    return str(out)

# ============================================================
# 2. มวลติดสปริง (Mass-Spring)
# ============================================================
def anim_spring_device():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax.set_xlim(-0.5, 2.5); ax.set_ylim(-1.5, 1.5); ax.axis("off")
    ax.set_title("Mass-Spring (SHM)", fontsize=13, fontweight="bold")
    ax.plot([-0.3, 0.2], [0, 0], "k-", lw=3)
    # spring
    def spring_path(x0, x1, y, n=10, amp=0.1):
        xs = np.linspace(x0, x1, n*4)
        ys = y + amp * np.sin(np.linspace(0, n*2*np.pi, len(xs)))
        return xs, ys
    spring_line, = ax.plot([], [], "k-", lw=1.5)
    box = Rectangle((0, -0.3), 0.5, 0.6, facecolor="#3498db",
                    edgecolor="black", lw=2)
    ax.add_patch(box)
    eq_text = ax.text(1.0, -1.2, "", ha="center", fontsize=11)
    # right panel
    ax2.set_xlim(0, 4); ax2.set_ylim(-1.2, 1.2)
    ax2.set_xlabel("t (s)"); ax2.set_ylabel("x (m)")
    ax2.set_title("x(t) = A*cos(omega*t)", fontsize=12)
    ax2.grid(alpha=0.3); ax2.axhline(0, color="gray", ls="--", lw=0.5)
    curve, = ax2.plot([], [], color="#e74c3c", lw=2)
    omega = 3.0; A = 0.8
    t_arr = np.linspace(0, 4, 200)
    x_arr = A * np.cos(omega * t_arr)
    def update(frame):
        t = frame / 25
        x = A * np.cos(omega * t)
        xs, ys = spring_path(0.2, 1.0 + x, 0)
        spring_line.set_data(xs, ys)
        box.set_xy((1.0 + x, -0.3))
        eq_text.set_text(f"t = {t:.2f}s | x = {x:.3f} m")
        curve.set_data(t_arr[t_arr <= t], x_arr[t_arr <= t])
        return spring_line, box, eq_text, curve
    anim = FuncAnimation(fig, update, frames=100, interval=40, blit=True)
    out = OUT_DIR / "device_spring.gif"
    anim.save(str(out), writer=PillowWriter(fps=25)); plt.close()
    print(f"[OK] {out}")
    return str(out)

# ============================================================
# 3. วงจร RC (RC Circuit)
# ============================================================
def anim_rc_circuit():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax.set_xlim(-0.5, 3.5); ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("RC Circuit (Charging)", fontsize=13, fontweight="bold")
    # circuit box
    ax.add_patch(FancyBboxPatch((0, -1), 3, 2, boxstyle="round,pad=0.05",
                                 facecolor="#f9f9f9", edgecolor="black", lw=2))
    # battery symbol
    ax.plot([0.3, 0.3], [0.3, -0.3], "k-", lw=3)
    ax.plot([0.4, 0.4], [0.6, -0.6], "k-", lw=2)
    ax.text(0.35, -0.9, "V", ha="center", fontsize=11, fontweight="bold")
    # resistor (zigzag)
    rx = np.linspace(1.0, 2.0, 9)
    ry = 1.0 + 0.1 * np.array([0, 1, -1, 1, -1, 1, -1, 1, 0])
    ax.plot(rx, ry, "k-", lw=2)
    ax.text(1.5, 1.25, "R", ha="center", fontsize=11, fontweight="bold")
    # capacitor
    ax.plot([2.5, 2.5], [1.0, 0.7], "k-", lw=2)
    ax.plot([2.35, 2.65], [0.7, 0.7], "k-", lw=3)
    ax.plot([2.35, 2.65], [0.5, 0.5], "k-", lw=3)
    ax.plot([2.5, 2.5], [0.5, -1.0], "k-", lw=2)
    ax.text(2.7, 0.6, "C", ha="left", fontsize=11, fontweight="bold")
    # wires
    ax.plot([0.3, 0.3, 1.0], [0.3, 1.0, 1.0], "k-", lw=2)
    ax.plot([0.3, 0.3, 0.3], [-0.3, -1.0, -1.0], "k-", lw=2)
    ax.plot([2.0, 2.5], [1.0, 1.0], "k-", lw=2)
    ax.plot([3.0, 3.0, 0.3], [-1.0, -1.0, -1.0], "k-", lw=2)
    ax.plot([2.5, 3.0], [-1.0, -1.0], "k-", lw=2)
    # electron dot
    dot, = ax.plot([], [], "o", color="#e74c3c", markersize=12)
    info = ax.text(1.5, -1.3, "", ha="center", fontsize=10)
    # right: V_c(t)
    ax2.set_xlim(0, 5); ax2.set_ylim(-0.1, 1.2)
    ax2.set_xlabel("t (tau)"); ax2.set_ylabel("V_c / V0")
    ax2.set_title("V_c(t) = V0*(1 - exp(-t/RC))", fontsize=12)
    ax2.grid(alpha=0.3); ax2.axhline(1, color="gray", ls="--", lw=0.5)
    curve, = ax2.plot([], [], color="#27ae60", lw=2)
    t_arr = np.linspace(0, 5, 200)
    v_arr = 1 - np.exp(-t_arr)
    def update(frame):
        t = frame / 40  # tau units
        vc = 1 - np.exp(-t)
        # electron moves around
        path = [(0.3, 0.3), (0.3, 1.0), (1.0, 1.0), (2.0, 1.0),
                (2.5, 1.0), (2.5, 0.7), (2.5, 0.5), (2.5, -1.0),
                (3.0, -1.0), (0.3, -1.0), (0.3, -0.3)]
        prog = (t * 1.5) % 1.0
        idx = int(prog * (len(path)-1))
        frac = prog * (len(path)-1) - idx
        p1 = np.array(path[idx]); p2 = np.array(path[(idx+1) % len(path)])
        pos = p1 + frac * (p2 - p1)
        dot.set_data([pos[0]], [pos[1]])
        info.set_text(f"t = {t:.2f}*RC | V_c = {vc*100:.1f}%")
        curve.set_data(t_arr[t_arr <= t], v_arr[t_arr <= t])
        return dot, info, curve
    anim = FuncAnimation(fig, update, frames=200, interval=40, blit=True)
    out = OUT_DIR / "device_rc_circuit.gif"
    anim.save(str(out), writer=PillowWriter(fps=25)); plt.close()
    print(f"[OK] {out}")
    return str(out)

# ============================================================
# 4. แท่งนำความร้อน (Heat Conduction Rod)
# ============================================================
def anim_heat_rod():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    ax.set_xlim(-0.5, 10.5); ax.set_ylim(-1, 2)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Heat Conduction in Metal Rod", fontsize=13, fontweight="bold")
    # rod gradient
    rod = Rectangle((0, 0), 10, 1, facecolor="gray", edgecolor="black", lw=2)
    ax.add_patch(rod)
    # flame
    ax.add_patch(Wedge((0, 0.5), 0.6, -60, 60, facecolor="#e74c3c",
                       edgecolor="darkred"))
    ax.text(0, -0.6, "Flame (T_hot)", ha="center", fontsize=11, color="red")
    ax.text(10, -0.6, "Cold end (T_cold)", ha="center", fontsize=11, color="blue")
    ax.text(5, 1.5, "Q = k*A*dT/L", ha="center", fontsize=12, fontweight="bold",
            bbox=dict(boxstyle="round", facecolor="lightyellow"))
    # temperature colorbar-like display
    x_arr = np.linspace(0, 10, 100)
    ax2.set_xlim(0, 10); ax2.set_ylim(20, 120)
    ax2.set_xlabel("x (cm)"); ax2.set_ylabel("T (Celsius)")
    ax2.set_title("T(x) - Steady state", fontsize=12)
    ax2.grid(alpha=0.3)
    line, = ax2.plot([], [], color="#e74c3c", lw=2.5, label="T(x,t)")
    ax2.legend()
    # animate approach to steady state
    def update(frame):
        t = frame / 25
        # T(x,t) = T_cold + (T_hot - T_cold) * (1 - x/L) * (1 - exp(-alpha*t))
        alpha = 0.5
        factor = 1 - np.exp(-alpha * t)
        T_arr = 20 + 100 * (1 - x_arr/10) * factor
        line.set_data(x_arr, T_arr)
        return line,
    anim = FuncAnimation(fig, update, frames=100, interval=40, blit=True)
    out = OUT_DIR / "device_heat_rod.gif"
    anim.save(str(out), writer=PillowWriter(fps=25)); plt.close()
    print(f"[OK] {out}")
    return str(out)

# ============================================================
# 5. เลนส์นูน (Convex Lens - Ray Tracing)
# ============================================================
def anim_convex_lens():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-10, 10); ax.set_ylim(-6, 6)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Convex Lens - Ray Tracing", fontsize=13, fontweight="bold")
    # optical axis
    ax.plot([-10, 10], [0, 0], "k--", lw=0.5, alpha=0.5)
    # lens (two arcs)
    y = np.linspace(-3, 3, 50)
    x_lens = 0.8 * (1 - (y/3)**2)**0.5
    ax.plot(x_lens, y, "b-", lw=3)
    ax.plot(-x_lens, y, "b-", lw=3)
    ax.text(0, -3.5, "Lens", ha="center", fontsize=11, color="blue")
    # focal points
    f = 4
    ax.plot(-f, 0, "kx", markersize=12); ax.text(-f, -0.6, "F", fontsize=11)
    ax.plot(f, 0, "kx", markersize=12); ax.text(f, -0.6, "F'", fontsize=11)
    # object (arrow)
    obj_h = 2.5
    ax.annotate("", xy=(-6, obj_h), xytext=(-6, 0),
                arrowprops=dict(arrowstyle="->", color="green", lw=3))
    ax.text(-6, obj_h + 0.3, "Object", ha="center", fontsize=11, color="green")
    # rays (3 principal rays)
    ray1, = ax.plot([], [], "r-", lw=1.5, alpha=0.8, label="Parallel ray")
    ray2, = ax.plot([], [], "orange", lw=1.5, alpha=0.8, label="Center ray")
    ray3, = ax.plot([], [], "purple", lw=1.5, alpha=0.8, label="Focal ray")
    # image position (thin lens: 1/f = 1/do + 1/di)
    do = 6
    di = 1 / (1/f - 1/do)
    m = -di/do
    # animate
    def update(frame):
        prog = min(frame / 60, 1.0)
        # ray 1: parallel to axis, then through F'
        x1 = np.linspace(-6, 0, 20)
        ray1_x = list(x1) + list(np.linspace(0, 10, 20))
        ray1_y = [obj_h] * 20 + list(np.linspace(obj_h, obj_h - obj_h/2*prog*2, 20))
        ray1.set_data(ray1_x[:int(len(ray1_x)*prog)],
                       ray1_y[:int(len(ray1_y)*prog)])
        # ray 2: through center
        x2 = np.linspace(-6, 10, 40)
        y2 = obj_h * (1 - (x2 + 6)/16)
        ray2.set_data(x2[:int(len(x2)*prog)], y2[:int(len(y2)*prog)])
        # ray 3: through F then parallel
        x3a = np.linspace(-6, 0, 20)
        y3a = np.linspace(obj_h, 0, 20)
        x3b = np.linspace(0, 10, 20)
        y3b = np.linspace(0, 0, 20)
        ray3_x = list(x3a) + list(x3b)
        ray3_y = list(y3a) + list(y3b)
        ray3.set_data(ray3_x[:int(len(ray3_x)*prog)],
                       ray3_y[:int(len(ray3_y)*prog)])
        return ray1, ray2, ray3
    anim = FuncAnimation(fig, update, frames=60, interval=50, blit=True)
    out = OUT_DIR / "device_convex_lens.gif"
    anim.save(str(out), writer=PillowWriter(fps=20)); plt.close()
    print(f"[OK] {out}")
    return str(out)

# ============================================================
# 6. พื้นเอียง (Inclined Plane with Forces)
# ============================================================
def anim_inclined_plane():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-1, 8); ax.set_ylim(-1, 5)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Inclined Plane - Force Diagram", fontsize=13, fontweight="bold")
    # incline (triangle)
    angle = np.deg2rad(30)
    L = 7
    tri = Polygon([(0, 0), (L*np.cos(angle), 0), (L*np.cos(angle), L*np.sin(angle))],
                  closed=True, facecolor="#dfe6e9", edgecolor="black", lw=2)
    ax.add_patch(tri)
    # angle arc
    ax.add_patch(Arc((L*np.cos(angle), 0), 2, 2, angle=0, theta1=180,
                     theta2=180-30, color="black"))
    ax.text(L*np.cos(angle) - 1.2, 0.2, "30°", fontsize=11)
    # block on incline
    dist = 4.5
    bx = dist * np.cos(angle) - 0.4
    by = dist * np.sin(angle)
    # draw block rotated
    block = Rectangle((bx, by), 0.8, 0.6, facecolor="#e74c3c",
                      edgecolor="black", lw=2)
    ax.add_patch(block)
    # force arrows
    g_arrow = ax.annotate("", xy=(bx+0.4, by-0.2), xytext=(bx+0.4, by+0.7),
                          arrowprops=dict(arrowstyle="->", color="blue", lw=2.5))
    ax.text(bx+0.6, by+0.5, "W=mg", color="blue", fontsize=11)
    n_arrow = ax.annotate("", xy=(bx-0.3, by+1.0), xytext=(bx+0.4, by+0.3),
                          arrowprops=dict(arrowstyle="->", color="green", lw=2.5))
    ax.text(bx-0.5, by+1.0, "N", color="green", fontsize=11)
    f_arrow = ax.annotate("", xy=(bx-0.6, by-0.1), xytext=(bx+0.4, by+0.3),
                          arrowprops=dict(arrowstyle="->", color="red", lw=2.5))
    ax.text(bx-1.2, by-0.3, "f", color="red", fontsize=11)
    # equations
    ax.text(4, 4.3, "Along incline: mg*sin(theta) - f = ma",
            fontsize=12, bbox=dict(boxstyle="round", facecolor="lightyellow"))
    # animate block sliding down
    a = 1.5
    def update(frame):
        t = frame / 25
        s = 0.5 * a * t**2
        new_dist = max(dist - s, 1.0)
        nbx = new_dist * np.cos(angle) - 0.4
        nby = new_dist * np.sin(angle)
        block.set_xy((nbx, nby))
        g_arrow.set_position((nbx+0.4, nby+0.7))
        g_arrow.xy = (nbx+0.4, nby-0.2)
        n_arrow.set_position((nbx+0.4, nby+0.3))
        n_arrow.xy = (nbx-0.3, nby+1.0)
        f_arrow.set_position((nbx+0.4, nby+0.3))
        f_arrow.xy = (nbx-0.6, nby-0.1)
        return block, g_arrow, n_arrow, f_arrow
    anim = FuncAnimation(fig, update, frames=60, interval=50, blit=False)
    out = OUT_DIR / "device_inclined_plane.gif"
    anim.save(str(out), writer=PillowWriter(fps=20)); plt.close()
    print(f"[OK] {out}")
    return str(out)

# ============================================================
# 7. โพรเจกไทล์ (Projectile Motion)
# ============================================================
def anim_projectile_device():
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    ax.set_xlim(0, 25); ax.set_ylim(0, 15); ax.set_aspect("equal")
    ax.set_title("Projectile Motion", fontsize=13, fontweight="bold")
    ax.grid(alpha=0.3)
    ax.plot([0, 25], [0, 0], "k-", lw=3)
    # initial velocity arrow
    v0 = 20; theta = np.deg2rad(45)
    v0x = v0 * np.cos(theta); v0y = v0 * np.sin(theta)
    g = 9.81
    t_total = 2 * v0y / g
    t_arr = np.linspace(0, t_total, 100)
    x_arr = v0x * t_arr; y_arr = v0y * t_arr - 0.5 * g * t_arr**2
    traj, = ax.plot([], [], "-", color="#667eea", lw=2, alpha=0.6)
    ball, = ax.plot([], [], "o", color="#e74c3c", markersize=14, zorder=5)
    vx_arrow = ax.annotate("", xy=(0, 0), xytext=(0, 0),
                           arrowprops=dict(arrowstyle="->", color="green", lw=2))
    vy_arrow = ax.annotate("", xy=(0, 0), xytext=(0, 0),
                           arrowprops=dict(arrowstyle="->", color="blue", lw=2))
    info = ax.text(12, 13, "", ha="center", fontsize=11,
                   bbox=dict(boxstyle="round", facecolor="white"))
    # right: height vs x
    ax2.set_xlim(0, 25); ax2.set_ylim(0, 12)
    ax2.set_xlabel("x (m)"); ax2.set_ylabel("y (m)")
    ax2.set_title("Trajectory", fontsize=12)
    ax2.grid(alpha=0.3)
    def update(frame):
        i = min(frame, len(t_arr)-1)
        t = t_arr[i]
        ball.set_data([x_arr[i]], [y_arr[i]])
        traj.set_data(x_arr[:i+1], y_arr[:i+1])
        vx = v0x; vy = v0y - g * t
        vx_arrow.xy = (x_arr[i] + vx*0.3, y_arr[i])
        vx_arrow.set_position((x_arr[i], y_arr[i]))
        vy_arrow.xy = (x_arr[i], y_arr[i] + vy*0.3)
        vy_arrow.set_position((x_arr[i], y_arr[i]))
        info.set_text(f"t={t:.2f}s  vx={vx:.1f}  vy={vy:.1f}")
        return ball, traj, vx_arrow, vy_arrow, info
    anim = FuncAnimation(fig, update, frames=100, interval=50, blit=False)
    out = OUT_DIR / "device_projectile.gif"
    anim.save(str(out), writer=PillowWriter(fps=20)); plt.close()
    print(f"[OK] {out}")
    return str(out)

# ============================================================
# 8. รอก (Pulley System)
# ============================================================
def anim_pulley_device():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-2, 4); ax.set_ylim(-1, 6); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Pulley - Atwood Machine", fontsize=13, fontweight="bold")
    # ceiling
    ax.plot([-2, 4], [5.5, 5.5], "k-", lw=3)
    # pulley (circle)
    ax.add_patch(Circle((1, 5), 0.5, facecolor="#95a5a6", edgecolor="black", lw=2))
    ax.add_patch(Circle((1, 5), 0.1, facecolor="black"))
    # two masses
    m1 = 2; m2 = 3  # kg
    a = (m2 - m1) * 9.81 / (m1 + m2)
    # strings
    s1_line, = ax.plot([], [], "k-", lw=2)
    s2_line, = ax.plot([], [], "k-", lw=2)
    box1 = Rectangle((-1.3, 0), 0.8, 0.8, facecolor="#3498db", edgecolor="black", lw=2)
    box2 = Rectangle((1.5, 0), 0.8, 0.8, facecolor="#e74c3c", edgecolor="black", lw=2)
    ax.add_patch(box1); ax.add_patch(box2)
    ax.text(-0.9, 0.35, f"m1={m1}kg", ha="center", fontsize=10)
    ax.text(1.9, 0.35, f"m2={m2}kg", ha="center", fontsize=10)
    info = ax.text(1, -0.7, "", ha="center", fontsize=12, fontweight="bold",
                   bbox=dict(boxstyle="round", facecolor="lightyellow"))
    # animate
    def update(frame):
        t = frame / 25
        d = 0.5 * a * t**2
        y1 = 4.0 + d; y2 = 4.0 - d
        y1 = min(y1, 4.8); y2 = max(y2, 0.5)
        box1.set_y(y1); box2.set_y(y2)
        s1_line.set_data([-0.9, -0.9, 1], [5, y1+0.8, 5])
        s2_line.set_data([1.9, 1.9, 1], [5, y2+0.8, 5])
        info.set_text(f"t={t:.2f}s  a={a:.2f} m/s²")
        return s1_line, s2_line, box1, box2, info
    anim = FuncAnimation(fig, update, frames=80, interval=50, blit=False)
    out = OUT_DIR / "device_pulley.gif"
    anim.save(str(out), writer=PillowWriter(fps=20)); plt.close()
    print(f"[OK] {out}")
    return str(out)

# ============================================================
# Registry
# ============================================================
DEVICES = {
    "pendulum": {
        "name_th": "ลูกตุ้มอย่างง่าย",
        "name_en": "Simple Pendulum",
        "category": "mechanics",
        "equations": ["pendulum"],
        "principle": "การแกว่งของมวลที่แขวนด้วยเชือกยาว L ภายใต้แรงโน้มถ่วง",
        "formula": "T = 2*pi*sqrt(L/g)",
        "real_use": "นาฬิกาลูกตุ้ม, เครื่องวัดค่า g, เซ็นเซอร์แผ่นดินไหว",
        "anim": anim_pendulum_device,
    },
    "spring": {
        "name_th": "มวลติดสปริง",
        "name_en": "Mass-Spring System",
        "category": "mechanics",
        "equations": ["hooke", "kinetic_energy"],
        "principle": "การสั่นแบบ Simple Harmonic Motion (SHM) ของมวลติดสปริง",
        "formula": "F = -kx,  x(t) = A*cos(omega*t)",
        "real_use": "ระบบกันสะเทือนรถ, เครื่องชั่งสปริง, seismic sensor",
        "anim": anim_spring_device,
    },
    "rc_circuit": {
        "name_th": "วงจร RC",
        "name_en": "RC Circuit (Charging)",
        "category": "electricity",
        "equations": ["rc_time", "ohm"],
        "principle": "การประจุตัวเก็บประจุผ่านตัวต้านทาน ตามฟังก์ชันเอกซ์โพเนนเชียล",
        "formula": "V_c(t) = V0 * (1 - exp(-t/RC))",
        "real_use": "ไฟกะพริบ, time delay, ตัวกรองสัญญาณ, วงจร 555 timer",
        "anim": anim_rc_circuit,
    },
    "heat_rod": {
        "name_th": "แท่งนำความร้อน",
        "name_en": "Heat Conduction Rod",
        "category": "thermodynamics",
        "equations": ["heat_conduction", "stefan"],
        "principle": "การนำความร้อนผ่านแท่งโลหะจากปลายร้อนไปยังปลายเย็น",
        "formula": "Q/t = k*A*dT/L",
        "real_use": "หม้อน้ำรถยนต์, heat sink CPU, ฉนวนกันความร้อน",
        "anim": anim_heat_rod,
    },
    "convex_lens": {
        "name_th": "เลนส์นูน",
        "name_en": "Convex Lens",
        "category": "optics",
        "equations": ["snell"],
        "principle": "การหักเหของแสงผ่านเลนส์นูน เกิดภาพจริงหรือภาพเสมือน",
        "formula": "1/f = 1/do + 1/di",
        "real_use": "แว่นขยาย, กล้อง, กล้องโทรทรรศน์, กล้องจุลทรรศน์",
        "anim": anim_convex_lens,
    },
    "inclined_plane": {
        "name_th": "พื้นเอียง",
        "name_en": "Inclined Plane",
        "category": "mechanics",
        "equations": ["hooke", "kinetic_energy"],
        "principle": "การเคลื่อนที่ของวัตถุบนพื้นเอียงภายใต้แรงโน้มถ่วง แรงตั้งฉาก แรงเสียดทาน",
        "formula": "mg*sin(theta) - f = ma",
        "real_use": "ทางลาด, รถบรรทุกขึ้นเขา, เครื่องบินขึ้น runway",
        "anim": anim_inclined_plane,
    },
    "projectile": {
        "name_th": "การเคลื่อนที่โพรเจกไทล์",
        "name_en": "Projectile Motion",
        "category": "mechanics",
        "equations": ["projectile", "kinetic_energy"],
        "principle": "การเคลื่อนที่แบบ 2 มิติ: แกน x ความเร็วคงที่, แกน y ความเร่งคงที่ g",
        "formula": "x=v0*cos(theta)*t,  y=v0*sin(theta)*t - 0.5*g*t^2",
        "real_use": "การยิงปืนใหญ่, การโยนบาส, การยิงขีปนาวุธ",
        "anim": anim_projectile_device,
    },
    "pulley": {
        "name_th": "รอก (Atwood Machine)",
        "name_en": "Pulley / Atwood Machine",
        "category": "mechanics",
        "equations": ["kinetic_energy"],
        "principle": "ระบบรอกและมวลสองก้อน ใช้ทดสอบกฎข้อที่ 2 ของนิวตัน",
        "formula": "a = (m2 - m1)*g / (m1 + m2)",
        "real_use": "ลิฟต์, เครน, ระบบรอกในโรงงาน, fitness equipment",
        "anim": anim_pulley_device,
    },
}

def generate_all_devices():
    """สร้าง GIF ทั้งหมด"""
    results = {}
    for key, dev in DEVICES.items():
        print(f"[{key}] {dev['name_th']}...")
        try:
            path = dev["anim"]()
            results[key] = path
        except Exception as e:
            print(f"  [ERR] {e}")
    return results

if __name__ == "__main__":
    print("=" * 60)
    print("  Physics Devices - Animation Generator")
    print("=" * 60)
    results = generate_all_devices()
    print(f"\n[OK] สร้างเสร็จ {len(results)} อุปกรณ์")
    print(f"[OK] บันทึกที่: {OUT_DIR}")
'''

out = ROOT / "physics_devices.py"
out.write_text(CODE, encoding="utf-8")
print(f"[OK] {out} ({out.stat().st_size} bytes)")
print("\nทดสอบ: py -3 physics_devices.py")