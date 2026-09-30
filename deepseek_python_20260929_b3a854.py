# download_datasets.py
"""
ดึงชุดข้อมูล PPG/HRV สาธารณะสำหรับ SatiARM
"""
import urllib.request
import zipfile
from pathlib import Path
import pandas as pd
import numpy as np

DATA_DIR = Path(__file__).parent / "datasets"
DATA_DIR.mkdir(exist_ok=True)

# ============================================================
# 1. GalaxyPPG Dataset (จาก Scientific Data / Springer Nature)
# ============================================================
print("=" * 60)
print("GalaxyPPG Dataset")
print("=" * 60)
print("Paper: https://www.nature.com/articles/s41597-025-05152-z")
print("ค้นหา 'GalaxyPPG' บน figshare หรือ Zenodo เพื่อดาวน์โหลด")
print("หรือใช้ลิงก์จาก paper โดยตรง")
print()

# ============================================================
# 2. PPG-DaLiA Dataset (จาก UCI / Edge Impulse)
# ============================================================
print("=" * 60)
print("PPG-DaLiA Dataset")
print("=" * 60)

# ลิงก์ตัวอย่างสำหรับ subset S1_E4
# (ลิงก์จริงต้องดาวน์โหลดจาก https://archive.ics.uci.edu/dataset/495/ppg+dalia)
PPG_DALIA_URL = "https://archive.ics.uci.edu/static/public/495/ppg+dalia.zip"

try:
    zip_path = DATA_DIR / "ppg_dalia.zip"
    if not zip_path.exists():
        print(f"กำลังดาวน์โหลดจาก: {PPG_DALIA_URL}")
        urllib.request.urlretrieve(PPG_DALIA_URL, zip_path)
        print(f"ดาวน์โหลดเสร็จ: {zip_path}")

    # แตกไฟล์
    extract_dir = DATA_DIR / "ppg_dalia"
    if not extract_dir.exists():
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(extract_dir)
        print(f"แตกไฟล์ที่: {extract_dir}")

    # แสดงรายการไฟล์
    for f in extract_dir.rglob("*.csv"):
        print(f"  พบไฟล์: {f.name}")
except Exception as e:
    print(f"ไม่สามารถดาวน์โหลดอัตโนมัติได้: {e}")
    print("ให้ดาวน์โหลด manual จาก: https://archive.ics.uci.edu/dataset/495/ppg+dalia")

# ============================================================
# 3. ตัวอย่างการอ่านข้อมูล PPG-DaLiA
# ============================================================
def load_ppg_sample(filepath):
    """อ่านไฟล์ CSV ของ PPG-DaLiA"""
    df = pd.read_csv(filepath)
    print(f"\nข้อมูลจาก: {filepath}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  จำนวนแถว: {len(df)}")
    if 'hr' in df.columns:
        print(f"  HR range: {df['hr'].min():.1f} - {df['hr'].max():.1f} bpm")
    if 'ppg' in df.columns:
        print(f"  PPG range: {df['ppg'].min():.4f} - {df['ppg'].max():.4f}")
    return df

# ลองอ่านไฟล์ตัวอย่าง (ถ้ามี)
sample_files = list((DATA_DIR / "ppg_dalia").rglob("*S1_E4*.csv")) if (DATA_DIR / "ppg_dalia").exists() else []
if sample_files:
    df = load_ppg_sample(sample_files[0])
    print(f"\nตัวอย่าง 5 แถวแรก:")
    print(df.head())

# ============================================================
# 4. ฟังก์ชันคำนวณ HRV (RMSSD) จาก PPG
# ============================================================
from scipy.signal import find_peaks

def compute_hrv_from_ppg(ppg_signal, fs=64):
    """
    คำนวณ HRV (RMSSD) จากสัญญาณ PPG
    fs: sampling frequency (Hz) — PPG-DaLiA ใช้ 64 Hz
    """
    peaks, _ = find_peaks(ppg_signal, distance=fs*0.5)
    if len(peaks) < 3:
        return 0.0
    rr_ms = np.diff(peaks) / fs * 1000
    rmssd = np.sqrt(np.mean(np.diff(rr_ms)**2))
    return rmssd

if sample_files:
    ppg_col = 'ppg' if 'ppg' in df.columns else df.columns[4]
    ppg_data = df[ppg_col].values
    hrv = compute_hrv_from_ppg(ppg_data)
    print(f"\nHRV (RMSSD) จากข้อมูลจริง: {hrv:.2f} ms")

print("\n" + "=" * 60)
print("เสร็จสิ้น! ข้อมูลอยู่ในโฟลเดอร์:", DATA_DIR)
print("=" * 60)