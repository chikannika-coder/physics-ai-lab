"""animation_engine.py"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / 'physics_ai_output' / 'animations'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def anim_pendulum():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 0.5); ax.set_aspect('equal')
    ax.axis('off'); ax.set_title('Simple Pendulum', fontsize=14, fontweight='bold')
    line, = ax.plot([], [], 'o-', color='#667eea', lw=3, markersize=15, markerfacecolor='navy')
    trail, = ax.plot([], [], '-', color='orange', alpha=0.3, lw=1)
    tx, ty = [], []
    def update(f):
        theta = f/20
        x = np.sin(theta); y = -np.cos(theta)
        line.set_data([0, x], [0, y])
        tx.append(x); ty.append(y)
        if len(tx) > 50: tx.pop(0); ty.pop(0)
        trail.set_data(tx, ty)
        return line, trail
    anim = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
    out = OUTPUT_DIR / 'pendulum.gif'
    anim.save(str(out), writer=PillowWriter(fps=20)); plt.close()
    print(f'[OK] {out}')

def anim_wave():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 4*np.pi); ax.set_ylim(-1.5, 1.5)
    ax.set_title('Wave', fontsize=14, fontweight='bold'); ax.grid(alpha=0.3)
    x = np.linspace(0, 4*np.pi, 500)
    l1, = ax.plot([], [], color='#764ba2', lw=2)
    l2, = ax.plot([], [], color='#667eea', lw=2, alpha=0.6)
    def update(f):
        t = f/20
        l1.set_data(x, np.sin(x - t) * np.exp(-0.05*t))
        l2.set_data(x, np.sin(x - t + 0.5) * np.exp(-0.05*t))
        return l1, l2
    anim = FuncAnimation(fig, update, frames=100, interval=50, blit=True)
    out = OUTPUT_DIR / 'wave.gif'
    anim.save(str(out), writer=PillowWriter(fps=20)); plt.close()
    print(f'[OK] {out}')

def anim_heat():
    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.linspace(0, np.pi, 100)
    U_all = [np.sin(x) * np.exp(-0.1*tv) for tv in np.linspace(0, 2.0, 60)]
    line, = ax.plot([], [], color='#e74c3c', lw=2)
    ax.set_xlim(0, np.pi); ax.set_ylim(-0.1, 1.1)
    ax.set_title('Heat Diffusion', fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    tt = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    def update(f):
        line.set_data(x, U_all[f])
        tt.set_text(f't={f*0.034:.2f}')
        return line, tt
    anim = FuncAnimation(fig, update, frames=len(U_all), interval=80, blit=True)
    out = OUTPUT_DIR / 'heat_diffusion.gif'
    anim.save(str(out), writer=PillowWriter(fps=15)); plt.close()
    print(f'[OK] {out}')

def anim_quantum():
    fig, ax = plt.subplots(figsize=(10, 4))
    x = np.linspace(-10, 10, 500)
    l1, = ax.plot([], [], color='#667eea', lw=2, label='Re(psi)')
    l2, = ax.plot([], [], color='#e74c3c', lw=2, label='|psi|^2')
    ax.set_xlim(-10, 10); ax.set_ylim(-1.2, 1.2)
    ax.set_title('Quantum Wave Packet', fontsize=14, fontweight='bold')
    ax.legend(); ax.grid(alpha=0.3)
    def update(f):
        t = f/10
        env = np.exp(-(x-2*t)**2 / (2*1.5**2))
        psi = env * np.cos(2*x - t)
        l1.set_data(x, psi); l2.set_data(x, np.abs(psi)**2)
        return l1, l2
    anim = FuncAnimation(fig, update, frames=100, interval=50, blit=True)
    out = OUTPUT_DIR / 'quantum_packet.gif'
    anim.save(str(out), writer=PillowWriter(fps=20)); plt.close()
    print(f'[OK] {out}')

def anim_robot():
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(-2.5, 2.5); ax.set_ylim(-1, 3); ax.set_aspect('equal')
    ax.axis('off'); ax.set_title('Robotic Hand', fontsize=14, fontweight='bold')
    ax.add_patch(FancyBboxPatch((-1.5, -0.4), 3.0, 0.5,
                                 boxstyle='round,pad=0.08', facecolor='#333'))
    cfg = [(-1.1, 0.2, (0.6,0.4,0.3), '#e74c3c'),
           (-0.55, 0.1, (0.7,0.5,0.35), '#3498db'),
           (0.0, 0.1, (0.8,0.55,0.4), '#2ecc71'),
           (0.55, 0.1, (0.7,0.5,0.35), '#f1c40f'),
           (1.1, 0.1, (0.55,0.4,0.28), '#9b59b6')]
    lines = []
    for bx, by, L, c in cfg:
        ln, = ax.plot([], [], 'o-', color=c, lw=5, markersize=10,
                       markerfacecolor='white', markeredgecolor=c, markeredgewidth=2)
        lines.append((ln, bx, by, L))
    txt = ax.text(0, 2.7, '', ha='center', fontsize=16, fontweight='bold')
    def fpos(bx, by, L, curl):
        md = np.radians([80,70,60]) * curl
        x, y = bx, by; pts = [(x,y)]; cum = 0
        for i in range(3):
            cum += md[i]
            x += L[i]*np.cos(cum); y += L[i]*np.sin(cum)
            pts.append((x, y))
        return pts
    def update(f):
        t = f/20
        br = np.sin(2*np.pi*t/8)
        curl = 0.5 + 0.5*br
        for ln, bx, by, L in lines:
            pts = fpos(bx, by, L, curl)
            ln.set_data([p[0] for p in pts], [p[1] for p in pts])
        txt.set_text('INHALE' if br >= 0 else 'EXHALE')
        txt.set_color('seagreen' if br >= 0 else 'steelblue')
        return [ln for ln, _, _, _ in lines] + [txt]
    anim = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
    out = OUTPUT_DIR / 'robot_hand.gif'
    anim.save(str(out), writer=PillowWriter(fps=20)); plt.close()
    print(f'[OK] {out}')

if __name__ == '__main__':
    for fn in [anim_pendulum, anim_wave, anim_heat, anim_quantum, anim_robot]:
        try: fn()
        except Exception as e: print(f'[ERR] {fn.__name__}: {e}')
