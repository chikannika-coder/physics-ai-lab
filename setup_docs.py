"""setup_docs.py — สร้างเอกสาร 7 ไฟล์ + โครงสร้าง"""
from pathlib import Path
import json

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
IMGS = DOCS / "images"
DOCS.mkdir(exist_ok=True)
IMGS.mkdir(exist_ok=True)

FILES = {}

# ============================================================
# README.md — หน้าแรก GitHub
# ============================================================
FILES["README.md"] = """# Physics AI Lab v5

> **ระบบ AI ด้านฟิสิกส์สำหรับนักเรียน** — Symbolic Regression + PINN + Animation + Hardware

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## เกี่ยวกับโครงการ

Physics AI Lab เป็นระบบที่ผสาน **ปัญญาประดิษฐ์** เข้ากับ **ฟิสิกส์** เพื่อให้นักเรียน:

- ค้นพบสมการฟิสิกส์จากข้อมูลจริงด้วย AI
- แก้สมการเชิงอนุพันธ์ด้วย PINN (Physics-Informed Neural Networks)
- ดู animation ของสมการและอุปกรณ์ฟิสิกส์
- ควบคุมฮาร์ดแวร์ (ESP32 + แขนกล + FSR)
- เพิ่มความรู้ใหม่ได้ตลอดเวลา

---

## ฟีเจอร์หลัก

| ส่วน | รายละเอียด |
|------|-----------|
| 🔬 **Symbolic Regression** | 17 สมการฟิสิกส์ (ลูกตุ้ม, Schrödinger, Navier-Stokes, ฯลฯ) |
| 🌊 **PINN Solver** | แก้สมการ Heat, Burgers, Wave |
| 🎬 **Animation Gallery** | 5+ animation จากสมการ |
| 🔧 **Physics Devices** | 8 อุปกรณ์จาก ทบ. พร้อม animation |
| 🎥 **Equation Animator** | สร้าง animation จากสมการอัตโนมัติ |
| 📊 **Analytics** | FFT, Wavelet, Machine Learning |
| 🖐️ **Hardware Control** | ESP32 + Servo + FSR |
| 📚 **Knowledge Base** | เพิ่ม/แก้สมการ, รูป, โค้ด |
| ➕ **Add Knowledge** | เมนูเพิ่มความรู้ใหม่ |

---

## เริ่มต้นอย่างรวดเร็ว

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/physics-ai-lab.git
cd physics-ai-lab

# 2. ติดตั้ง dependencies
pip install -r requirements.txt

# 3. รันโปรแกรม
streamlit run physics_ai_app_v5.py