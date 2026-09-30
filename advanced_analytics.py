"""advanced_analytics.py"""
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
    print(f'[FFT] Peak: {fft_result["peak_freq"]:.2f} Hz')
    wav = analyze_wavelet(sig, fs)
    if 'error' not in wav:
        print(f'[Wavelet] shape: {wav["coefficients"].shape}')
    else:
        print(f'[Wavelet] {wav["error"]}')
    X = np.random.randn(500, 3)
    y = X[:, 0]**2 + 2*X[:, 1] - X[:, 2] + 0.1*np.random.randn(500)
    ml = train_regressor(X, y, 'rf')
    print(f'[ML] R2: {ml["r2"]:.4f}')
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    axes[0,0].plot(t[:500], sig[:500]); axes[0,0].set_title('Signal'); axes[0,0].grid(alpha=0.3)
    axes[0,1].plot(fft_result['frequencies'], fft_result['magnitudes'])
    axes[0,1].set_title(f'FFT peak {fft_result["peak_freq"]:.2f} Hz')
    axes[0,1].set_xlim(0, 20); axes[0,1].grid(alpha=0.3)
    if 'coefficients' in wav:
        axes[1,0].imshow(np.abs(wav['coefficients']), aspect='auto', cmap='jet',
                         extent=[0, 10, wav['frequencies'][-1], wav['frequencies'][0]])
        axes[1,0].set_title('Wavelet'); axes[1,0].set_ylabel('Freq')
    axes[1,1].scatter(ml['y_test'], ml['y_pred'], alpha=0.5)
    axes[1,1].plot([ml['y_test'].min(), ml['y_test'].max()],
                   [ml['y_test'].min(), ml['y_test'].max()], 'r--')
    axes[1,1].set_title(f'ML R2={ml["r2"]:.3f}')
    plt.tight_layout()
    out = OUTPUT_DIR / 'advanced_analytics_demo.png'
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'[OK] {out}')

if __name__ == '__main__':
    demo()
