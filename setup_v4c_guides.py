"""setup_v4c_guides.py"""
from pathlib import Path
ROOT = Path(__file__).parent

PROJECTS = """\"\"\"example_projects.py\"\"\"
EXAMPLE_PROJECTS = [
    {'id': 'pendulum_ai', 'title': 'AI ค้นพบสมการลูกตุ้ม', 'level': 'ม.ปลาย',
     'duration': '4 สัปดาห์',
     'description': 'ใช้ PySR ค้นหาสมการ T = 2*pi*sqrt(L/g)',
     'objectives': ['เข้าใจกระบวนการวิทยาศาสตร์', 'ใช้ Symbolic Regression', 'เปรียบเทียบสมการ'],
     'equations': ['pendulum'], 'animations': ['pendulum'],
     'deliverable': 'รายงาน + วิดีโอ 2 นาที'},
    {'id': 'heat_dhamma', 'title': 'สมการความร้อนกับอนิจจัง', 'level': 'ม.ปลาย',
     'duration': '6 สัปดาห์',
     'description': 'ใช้ PINN แก้สมการความร้อน เปรียบเทียบกับอนิจจัง',
     'objectives': ['เข้าใจสมการความร้อน', 'ใช้ PINN', 'เชื่อมโยงวิทยาศาสตร์กับพุทธ'],
     'equations': ['heat_conduction'], 'animations': ['heat'],
     'deliverable': 'รายงาน + animation'},
    {'id': 'quantum_packet', 'title': 'Quantum Wave Packet', 'level': 'มหาวิทยาลัย',
     'duration': '8 สัปดาห์',
     'description': 'ใช้ Symbolic Regression ค้นหา wave packet',
     'objectives': ['เข้าใจ Schrodinger', 'ใช้ PySR', 'Visualize'],
     'equations': ['schrodinger'], 'animations': ['quantum'],
     'deliverable': 'รายงาน + poster'},
    {'id': 'satiarm_bio', 'title': 'SatiARM วัด HRV', 'level': 'ม.ปลาย',
     'duration': '10 สัปดาห์',
     'description': 'ใช้แขนกลนำการฝึกสติ วัด HRV',
     'objectives': ['ออกแบบการทดลอง', 'ใช้ FSR + PPG', 'วิเคราะห์สถิติ'],
     'equations': ['heat_conduction'], 'animations': ['robot_hand'],
     'deliverable': 'รายงานวิจัย + GitHub'},
    {'id': 'fluid_flow', 'title': 'AI วิเคราะห์การไหล', 'level': 'มหาวิทยาลัย',
     'duration': '8 สัปดาห์',
     'description': 'ใช้ Symbolic Regression ค้นหา Poiseuille',
     'objectives': ['เข้าใจ Navier-Stokes', 'ใช้ PySR', 'ประยุกต์'],
     'equations': ['navier_stokes'], 'animations': ['wave'],
     'deliverable': 'รายงาน + กราฟ'},
]

def get_project(pid):
    for p in EXAMPLE_PROJECTS:
        if p['id'] == pid: return p
    return None

if __name__ == '__main__':
    for p in EXAMPLE_PROJECTS:
        print('=' * 60)
        print(f\"  {p['title']}\")
        print(f\"  ระดับ: {p['level']}  |  เวลา: {p['duration']}\")
        print('=' * 60)
        print(f\"  {p['description']}\")
        for o in p['objectives']: print(f'    - {o}')
        print()
"""

ESP32 = """# ESP32 Firmware Upload Guide

## อุปกรณ์
- ESP32 DevKit
- Servo 5 ตัว (SG90/MG90S)
- FSR 5 ตัว

## 1. Arduino IDE
https://www.arduino.cc/en/software

## 2. ESP32 Board
File > Preferences > Additional Boards URLs:
https://espressif.github.io/arduino-esp32/package_esp32_index.json

Tools > Board > Boards Manager > esp32 > Install

## 3. Library
Tools > Manage Libraries > ESP32Servo

## 4. Pinout
| Servo | Pin | FSR | Pin |
|-------|-----|-----|-----|
| Thumb | 13 | Thumb | 34 |
| Index | 12 | Index | 35 |
| Middle | 14 | Middle | 32 |
| Ring | 27 | Ring | 33 |
| Pinky | 26 | Pinky | 25 |

## 5. Power
- Servo VCC -> 5V ภายนอก
- GND ร่วมกัน
- FSR: 3.3V - FSR - GPIO - 10k - GND

## 6. Upload
Tools > Board: ESP32 Dev Module > Port: COM_X > Upload

## 7. Serial Monitor 115200
เมนู 1-7 + commands: T/I/M/R/P/A/B/X/S/?
"""

DEPLOY = """# Deploy Streamlit Cloud

## 1. GitHub
- https://github.com/signup
- สร้าง repo: physics-ai-lab
- อัปโหลด: physics_ai_app.py, physics_knowledge.json, physics_knowledge.py,
  physics_symbolic_v4.py, advanced_analytics.py, animation_engine.py,
  example_projects.py, requirements.txt

## 2. requirements.txt
streamlit
pandas
numpy
matplotlib
scipy
scikit-learn
PyWavelets
pysr
pyserial

## 3. Streamlit Cloud
https://streamlit.io/cloud > New app > เลือก repo > Deploy

## 4. รอ build 3-5 นาที
URL: https://your-app.streamlit.app

## 5. Update
git add . && git commit -m 'Update' && git push
"""

REQ = """streamlit
pandas
numpy
matplotlib
scipy
scikit-learn
PyWavelets
pysr
pyserial
"""

(ROOT / "example_projects.py").write_text(PROJECTS, encoding="utf-8")
print("[OK] example_projects.py")
(ROOT / "ESP32_UPLOAD_GUIDE.md").write_text(ESP32, encoding="utf-8")
print("[OK] ESP32_UPLOAD_GUIDE.md")
(ROOT / "DEPLOY_GUIDE.md").write_text(DEPLOY, encoding="utf-8")
print("[OK] DEPLOY_GUIDE.md")
(ROOT / "requirements.txt").write_text(REQ, encoding="utf-8")
print("[OK] requirements.txt")
print()
print("Next:")
print("  py -3 example_projects.py")
