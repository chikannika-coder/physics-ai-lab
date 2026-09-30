"""
SatiARM Simulation — Windows-compatible version
"""

import os
from pathlib import Path

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
from matplotlib.gridspec import GridSpec
from scipy import stats
from scipy.signal import find_peaks
import matplotlib.font_manager as fm

# ============================================================
# 1. ตั้งค่าโฟลเดอร์ปลายทาง (ใช้ได้ทั้ง Windows / Mac / Linux)
# ============================================================
# ทางเลือก A: บันทึกที่โฟลเดอร์เดียวกับไฟล์ .py
OUTPUT_DIR = Path(__file__).parent / "satiarm_output"

# ทางเลือก B: บันทึกที่ Desktop (เปิดคอมเมนต์ถ้าต้องการ)
# OUTPUT_DIR = Path.home() / "Desktop" / "satiarm_output"

# ทางเลือก C: ระบุเอง
# OUTPUT_DIR = Path(r"D:\ai ด้านฟิสิกส์\satiarm_output")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
print(f"📁 โฟลเดอร์บันทึก: {OUTPUT_DIR.resolve()}")

# ============================================================
# 2. ตั้งค่าฟอนต์ไทย
# ============================================================
def setup_thai_font():
    """เลือกฟอนต์ที่มีตัวอักษรไทย — ใช้ได้บน Windows"""
    # ลองฟอนต์ที่มาพร้อม Windows ก่อน (เรียงตามความสวย)
    candidates = [
        "Leelawadee UI",   # Windows 8+ ดูสวย
        "Tahoma",          # Windows ทุกเวอร์ชัน มีไทย
        "Leelawadee",      # Windows เก่า
        "Sarabun",         # ถ้าติดตั้งเพิ่ม
        "Noto Sans Thai",  # ถ้าติดตั้งเพิ่ม
        "Angsana New",     # ฟอนต์ไทยคลาสสิก
    ]

    available = {f.name for f in fm.fontManager.ttflist}
    chosen = None
    for name in candidates:
        if name in available:
            chosen = name
            break

    if chosen:
        plt.rcParams['font.family'] = chosen
        plt.rcParams['font.sans-serif'] = [chosen] + plt.rcParams['font.sans-serif']
        print(f"✓ ใช้ฟอนต์: {chosen}")
    else:
        print("⚠ ไม่พบฟอนต์ไทย — ข้อความไทยจะแสดงเป็น □")
        print("  วิธีแก้: ดาวน์โหลดฟอนต์ Sarabun หรือ Noto Sans Thai")
        print("  แล้วติดตั้งใน Windows (คลิกขวา → Install for all users)")

    plt.rcParams['axes.unicode_minus'] = False

setup_thai_font()

# ============================================================
# 3. ตั้งค่า seed
# ============================================================
np.random.seed(42)
