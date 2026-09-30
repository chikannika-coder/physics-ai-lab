"""setup_v4b_analytics.py"""
from pathlib import Path
ROOT = Path(__file__).parent

ANALYTICS = """\"\"\"advanced_analytics.py\"\"\"
import numpy as np
from pathlib import Path
from scipy.fft import fft, fftfreq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUTPUT_DIR = Path(__file__).parent / 'physics_ai_output'
OUTPUT_DIR.mkdir(exist_ok=True)

def analyze_fft(signal_data, fs=100):
    n = len(signal_data)
    yf = fft(signal_data)
    xf = fftfreq(n, 1/fs)[:n//2]
    mag = 2.0/n * np.abs(yf[:n//2])
    peak_idx = np.argmax(mag)
    return {'frequencies': xf, 'magnitudes': mag,
            'peak_freq': float(xf[peak_idx]), 'peak_mag': float(mag[peak_idx])}

def analyze_wavelet(signal_data, fs=100):
    try:
        import pywt
        scales = np.arange(1, 128)
        coeffs, freqs = pywt.cwt(signal_data, scales, 'morl', sampling_period=1/fs)
        return {'coefficients': coeffs, 'frequencies': freqs, 'scales': scales}
    except ImportError:
        return {'error': 'pip install PyWavelets'}

def train_regressor(X, y, model_type='rf'):
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score, mean_squared_error
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.neural_network import MLPRegressor
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    if model_type == 'rf':
        model = RandomForestRegressor(n_estimators=100, random_state=42)
    elif model_type == 'linear':
        model = LinearRegression()
    elif model_type == 'mlp':
        model = MLPRegressor(hidden_layer_sizes=(64, 64), max_iter=1000, random_state=42)
    else:
        raise ValueError(model_type)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return {'model': model, 'r2': float(r2_score(y_test, y_pred)),
            'rmse': float(np.sqrt(mean_squared_error(y_test, y_pred))),
            'y_pred': y_pred, 'y_test': y_test}

def demo():
    fs = 100
    t = np.linspace(0, 10, fs*10)
    sig = np.sin(2*np.pi*2*t) + 0.5*np.sin(2*np.pi*5*t) + 0.1*np.random.randn(len(t))
    fft_result = analyze_fft(sig, fs)
    print(f'[FFT] Peak: {fft_result[\"peak_freq\"]:.2f} Hz')
    wav = analyze_wavelet(sig, fs)
    if 'error' not in wav:
        print(f'[Wavelet] shape: {wav[\"coefficients\"].shape}')
    else:
        print(f'[Wavelet] {wav[\"error\"]}')
    X = np.random.randn(500, 3)
    y = X[:, 0]**2 + 2*X[:, 1] - X[:, 2] + 0.1*np.random.randn(500)
    ml = train_regressor(X, y, 'rf')
    print(f'[ML] R2: {ml[\"r2\"]:.4f}')
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    axes[0,0].plot(t[:500], sig[:500]); axes[0,0].set_title('Signal'); axes[0,0].grid(alpha=0.3)
    axes[0,1].plot(fft_result['frequencies'], fft_result['magnitudes'])
    axes[0,1].set_title(f'FFT peak {fft_result[\"peak_freq\"]:.2f} Hz')
    axes[0,1].set_xlim(0, 20); axes[0,1].grid(alpha=0.3)
    if 'coefficients' in wav:
        axes[1,0].imshow(np.abs(wav['coefficients']), aspect='auto', cmap='jet',
                         extent=[0, 10, wav['frequencies'][-1], wav['frequencies'][0]])
        axes[1,0].set_title('Wavelet'); axes[1,0].set_ylabel('Freq')
    axes[1,1].scatter(ml['y_test'], ml['y_pred'], alpha=0.5)
    axes[1,1].plot([ml['y_test'].min(), ml['y_test'].max()],
                   [ml['y_test'].min(), ml['y_test'].max()], 'r--')
    axes[1,1].set_title(f'ML R2={ml[\"r2\"]:.3f}')
    plt.tight_layout()
    out = OUTPUT_DIR / 'advanced_analytics_demo.png'
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'[OK] {out}')

if __name__ == '__main__':
    demo()
"""

ANIM = """\"\"\"animation_engine.py\"\"\"
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
"""

(ROOT / "advanced_analytics.py").write_text(ANALYTICS, encoding="utf-8")
print("[OK] advanced_analytics.py")
(ROOT / "animation_engine.py").write_text(ANIM, encoding="utf-8")
print("[OK] animation_engine.py")
print()
print("Next: py -3 advanced_analytics.py")
print("      py -3 animation_engine.py")