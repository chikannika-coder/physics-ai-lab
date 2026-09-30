"""equation_animator.py"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

OUT = Path(__file__).parent / "physics_ai_output" / "equations"
OUT.mkdir(parents=True, exist_ok=True)

def detect_type(f):
    fl = f.lower()
    if ("sin" in fl or "cos" in fl) and "*x" in fl and ("-t" in fl or "w*t" in fl):
        return "wave"
    if "exp" in fl and "-" in fl:
        return "decay"
    if "**" in fl:
        return "power"
    return "oscillation"

def _wave(name):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.set_xlim(0, 4*np.pi); ax.set_ylim(-1.5, 1.5)
    ax.grid(alpha=0.3); ax.axhline(0, color="gray", ls="--", lw=0.5)
    ax.set_title(name, fontsize=13, fontweight="bold")
    line, = ax.plot([], [], color="#764ba2", lw=2.5)
    x = np.linspace(0, 4*np.pi, 500)
    def u(f):
        t = f/25
        line.set_data(x, np.sin(x - 2*t) * np.exp(-0.05*t))
        return line,
    a = FuncAnimation(fig, u, frames=100, interval=40, blit=True)
    p = OUT / f"eq_{name}.gif"
    a.save(str(p), writer=PillowWriter(fps=25)); plt.close()
    print(f"[OK] {p}"); return str(p)

def _osc(name):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.set_xlim(0, 4); ax.set_ylim(-1.5, 1.5)
    ax.grid(alpha=0.3); ax.axhline(0, color="gray", ls="--", lw=0.5)
    ax.set_title(name, fontsize=13, fontweight="bold")
    line, = ax.plot([], [], color="#667eea", lw=2.5)
    dot, = ax.plot([], [], "o", color="#e74c3c", markersize=12)
    t = np.linspace(0, 4, 200); y = np.sin(2*np.pi*t)
    def u(f):
        tc = f/25
        line.set_data(t[t<=tc], y[t<=tc])
        i = np.argmin(np.abs(t-tc))
        dot.set_data([t[i]], [y[i]])
        return line, dot
    a = FuncAnimation(fig, u, frames=100, interval=40, blit=True)
    p = OUT / f"eq_{name}.gif"
    a.save(str(p), writer=PillowWriter(fps=25)); plt.close()
    print(f"[OK] {p}"); return str(p)

def _decay(name):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.set_xlim(0, 4); ax.set_ylim(-0.1, 1.2)
    ax.grid(alpha=0.3); ax.axhline(0, color="gray", ls="--", lw=0.5)
    ax.set_title(name, fontsize=13, fontweight="bold")
    line, = ax.plot([], [], color="#e74c3c", lw=2.5)
    dot, = ax.plot([], [], "o", color="darkred", markersize=12)
    t = np.linspace(0, 4, 200); y = np.exp(-t)
    def u(f):
        tc = f/25
        line.set_data(t[t<=tc], y[t<=tc])
        i = np.argmin(np.abs(t-tc))
        dot.set_data([t[i]], [y[i]])
        return line, dot
    a = FuncAnimation(fig, u, frames=100, interval=40, blit=True)
    p = OUT / f"eq_{name}.gif"
    a.save(str(p), writer=PillowWriter(fps=25)); plt.close()
    print(f"[OK] {p}"); return str(p)

def _power(name):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.set_xlim(0, 5); ax.set_ylim(-0.1, 5)
    ax.grid(alpha=0.3)
    ax.set_title(name, fontsize=13, fontweight="bold")
    line, = ax.plot([], [], color="#27ae60", lw=2.5)
    x = np.linspace(0, 5, 200); y = x**2
    def u(f):
        tc = f/25
        m = x <= tc
        line.set_data(x[m], y[m])
        return line,
    a = FuncAnimation(fig, u, frames=100, interval=40, blit=True)
    p = OUT / f"eq_{name}.gif"
    a.save(str(p), writer=PillowWriter(fps=25)); plt.close()
    print(f"[OK] {p}"); return str(p)

def animate_equation(formula, name, duration=4, fps=25):
    name = "".join(c for c in name if c.isalnum() or c in "_-")
    t = detect_type(formula)
    print(f"[{name}] type={t}")
    if t == "wave": return _wave(name)
    if t == "decay": return _decay(name)
    if t == "power": return _power(name)
    return _osc(name)

if __name__ == "__main__":
    print("="*60); print("  Equation Animator"); print("="*60)
    eqs = [
        ("y = A*sin(k*x - w*t)", "traveling_wave"),
        ("x = A*cos(w*t)", "SHM"),
        ("V = V0*(1-exp(-t/RC))", "RC_charging"),
        ("KE = 0.5*m*v**2", "kinetic_energy"),
        ("P = sigma*A*T**4", "stefan"),
        ("F = k*q1*q2/r**2", "coulomb"),
    ]
    for formula, name in eqs:
        try: animate_equation(formula, name, 3)
        except Exception as e: print(f"[ERR] {name}: {e}")
    print(f"\n[OK] saved to: {OUT}")
