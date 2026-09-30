# Physics AI Lab v5

> ระบบ AI ด้านฟิสิกส์สำหรับนักเรียน — Symbolic Regression + PINN + Animation + Hardware

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)
![License](https://img.shields.io/badge/License-MIT-green)

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
| 🔬 Symbolic Regression | 17 สมการฟิสิกส์ |
| 🌊 PINN Solver | แก้สมการ Heat, Burgers, Wave |
| 🎬 Animation Gallery | 5+ animation |
| 🔧 Physics Devices | 8 อุปกรณ์จาก ทบ. |
| 🎥 Equation Animator | สร้าง animation อัตโนมัติ |
| 📊 Analytics | FFT, Wavelet, ML |
| 🖐️ Hardware Control | ESP32 + Servo + FSR |
| 📚 Knowledge Base | ฐานความรู้ |
| ➕ Add Knowledge | เพิ่มความรู้ใหม่ |

---

## เริ่มต้นอย่างรวดเร็ว

```bash
git clone https://github.com/chikannika/physics-ai-lab.git
cd physics-ai-lab
pip install -r requirements.txt
streamlit run physics_ai_app_v5.py
```

เปิด browser: http://localhost:8501

---

## เอกสาร

| เอกสาร | สำหรับ |
|--------|-------|
| [คู่มือนักเรียน](docs/01_คู่มือนักเรียน.md) | นักเรียนทั่วไป |
| [คู่มือนักเรียน (ภาพ)](docs/02_คู่มือนักเรียน_ภาพ.md) | นักเรียนหูหนวก |
| [คู่มือติดตั้ง](docs/03_คู่มือติดตั้ง.md) | ผู้ติดตั้ง |
| [คู่มือติดตั้ง (ภาพ)](docs/04_คู่มือติดตั้ง_ภาพ.md) | นักเรียนหูหนวก |
| [วิธี upload GitHub](docs/05_GitHub_Upload.md) | ผู้เผยแพร่ |

---

## ตัวอย่างการใช้งาน

### ค้นพบสมการลูกตุ้ม

```python
from physics_symbolic_v4 import discover
result = discover('pendulum')
print(result['equation'])  # 6.2832 * sqrt(L)
```

### สร้าง animation จากสมการ

```python
from equation_animator import animate_equation
animate_equation('y = A*sin(k*x - w*t)', 'my_wave')
```

### ควบคุมแขนกล

```python
from hardware_bridge import SatiARMHardware
hw = SatiARMHardware(port='COM3')
hw.connect()
hw.send_servo('Index', 90)
```

---

## License

MIT License — ดูรายละเอียดใน [LICENSE](LICENSE)

---

⭐ ถ้าชอบโครงการนี้ ฝาก star ด้วยนะครับ!"# physics-ai-lab-" 
"# physics-ai-lab-" 
