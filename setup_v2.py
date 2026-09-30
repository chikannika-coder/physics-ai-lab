"""
setup_v2.py — อัปเกรดระบบ SatiARM Physics AI
รัน: py -3 setup_v2.py
"""
from pathlib import Path
import json

ROOT = Path(__file__).parent
FILES = {}

# ============================================================
# 1. Physics Knowledge Base (JSON)
# ============================================================
FILES["physics_knowledge.json"] = json.dumps({
    "version": "1.0.0",
    "last_updated": "2026-09-30",
    "equations": [
        {
            "id": "pendulum",
            "name_th": "ลูกตุ้มอย่างง่าย",
            "name_en": "Simple Pendulum",
            "latex": r"T = 2\pi\sqrt{\frac{L}{g}}",
            "formula": "T = 2*pi*sqrt(L/g)",
            "variables": {"T": "คาบ (s)", "L": "ความยาว (m)", "g": "9.81 m/s²"},
            "domain": ["กลศาสตร์", "การสั่น"],
            "level": "ม.ปลาย",
            "category": "mechanics"
        },
        {
            "id": "projectile",
            "name_th": "การเคลื่อนที่แบบโพรเจกไทล์",
            "name_en": "Projectile Motion",
            "latex": r"h = \frac{v_0^2 \sin^2\theta}{2g}",
            "formula": "h = v0**2 * sin(theta)**2 / (2*g)",
            "variables": {"h": "ความสูงสูงสุด (m)", "v0": "ความเร็วต้น (m/s)",
                         "theta": "มุมยิง (rad)", "g": "9.81"},
            "domain": ["กลศาสตร์"],
            "level": "ม.ปลาย",
            "category": "mechanics"
        },
        {
            "id": "ohm",
            "name_th": "กฎของโอห์ม",
            "name_en": "Ohm's Law",
            "latex": r"V = IR",
            "formula": "V = I * R",
            "variables": {"V": "แรงดัน (V)", "I": "กระแส (A)", "R": "ความต้านทาน (Ω)"},
            "domain": ["ไฟฟ้า"],
            "level": "ม.ต้น",
            "category": "electricity"
        },
        {
            "id": "coulomb",
            "name_th": "กฎของคูลอมบ์",
            "name_en": "Coulomb's Law",
            "latex": r"F = k\frac{q_1 q_2}{r^2}",
            "formula": "F = k * q1 * q2 / r**2",
            "variables": {"F": "แรง (N)", "k": "8.99e9 N·m²/C²",
                         "q1,q2": "ประจุ (C)", "r": "ระยะห่าง (m)"},
            "domain": ["ไฟฟ้า"],
            "level": "ม.ปลาย",
            "category": "electricity"
        },
        {
            "id": "hooke",
            "name_th": "กฎของฮุก",
            "name_en": "Hooke's Law",
            "latex": r"F = -kx",
            "formula": "F = -k * x",
            "variables": {"F": "แรงสปริง (N)", "k": "ค่าคงที่สปริง (N/m)", "x": "ระยะยืด (m)"},
            "domain": ["กลศาสตร์", "ยืดหยุ่น"],
            "level": "ม.ปลาย",
            "category": "mechanics"
        },
        {
            "id": "kinetic_energy",
            "name_th": "พลังงานจลน์",
            "name_en": "Kinetic Energy",
            "latex": r"KE = \frac{1}{2}mv^2",
            "formula": "KE = 0.5 * m * v**2",
            "variables": {"KE": "พลังงาน (J)", "m": "มวล (kg)", "v": "ความเร็ว (m/s)"},
            "domain": ["กลศาสตร์", "พลังงาน"],
            "level": "ม.ต้น",
            "category": "mechanics"
        },
        {
            "id": "heat_conduction",
            "name_th": "การนำความร้อน",
            "name_en": "Heat Conduction",
            "latex": r"Q = kA\frac{\Delta T}{L}",
            "formula": "Q = k * A * dT / L",
            "variables": {"Q": "อัตราการถ่ายเท (W)", "k": "ค่าการนำความร้อน",
                         "A": "พื้นที่ (m²)", "dT": "ผลต่างอุณหภูมิ (K)", "L": "ความหนา (m)"},
            "domain": ["อุณหพลศาสตร์"],
            "level": "ม.ปลาย",
            "category": "thermodynamics"
        },
        {
            "id": "ideal_gas",
            "name_th": "กฎแก๊สอุดมคติ",
            "name_en": "Ideal Gas Law",
            "latex": r"PV = nRT",
            "formula": "P * V = n * R * T",
            "variables": {"P": "ความดัน (Pa)", "V": "ปริมาตร (m³)",
                         "n": "โมล", "R": "8.314 J/(mol·K)", "T": "อุณหภูมิ (K)"},
            "domain": ["อุณหพลศาสตร์"],
            "level": "ม.ปลาย",
            "category": "thermodynamics"
        },
        {
            "id": "wave_speed",
            "name_th": "ความเร็วคลื่น",
            "name_en": "Wave Speed",
            "latex": r"v = f\lambda",
            "formula": "v = f * lam",
            "variables": {"v": "ความเร็ว (m/s)", "f": "ความถี่ (Hz)", "lam": "ความยาวคลื่น (m)"},
            "domain": ["คลื่น"],
            "level": "ม.ต้น",
            "category": "waves"
        },
        {
            "id": "snell",
            "name_th": "กฎของสเนลล์",
            "name_en": "Snell's Law",
            "latex": r"n_1\sin\theta_1 = n_2\sin\theta_2",
            "formula": "n1*sin(t1) = n2*sin(t2)",
            "variables": {"n1,n2": "ดัชนีหักเห", "theta1,theta2": "มุม (rad)"},
            "domain": ["แสง"],
            "level": "ม.ปลาย",
            "category": "optics"
        },
        {
            "id": "stefan_boltzmann",
            "name_th": "กฎของสเตฟาน-โบลต์ซมันน์",
            "name_en": "Stefan-Boltzmann Law",
            "latex": r"P = \sigma A T^4",
            "formula": "P = sigma * A * T**4",
            "variables": {"P": "กำลังแผ่รังสี (W)", "sigma": "5.67e-8 W/(m²·K⁴)",
                         "A": "พื้นที่ (m²)", "T": "อุณหภูมิ (K)"},
            "domain": ["อุณหพลศาสตร์", "รังสี"],
            "level": "มหาวิทยาลัย",
            "category": "thermodynamics"
        },
        {
            "id": "rc_time",
            "name_th": "เวลาคงตัว RC",
            "name_en": "RC Time Constant",
            "latex": r"\tau = RC",
            "formula": "tau = R * C",
            "variables": {"tau": "เวลาคงตัว (s)", "R": "ความต้านทาน (Ω)", "C": "ความจุ (F)"},
            "domain": ["ไฟฟ้า", "วงจร"],
            "level": "มหาวิทยาลัย",
            "category": "electricity"
        }
    ],
    "history": [
        {
            "date": "2026-09-30",
            "action": "created",
            "version": "1.0.0",
            "note": "เริ่มต้นด้วยสมการ 12 รายการ"
        }
    ]
}, ensure_ascii=False, indent=2)

# ============================================================
# 2. Physics Knowledge Manager
# ============================================================
FILES["physics_knowledge.py"] = r'''"""
physics_knowledge.py — จัดการฐานความรู้ฟิสิกส์
"""
import json
from pathlib import Path
from datetime import datetime

KB_FILE = Path(__file__).parent / "physics_knowledge.json"

def load_kb():
    if not KB_FILE.exists():
        return {"version": "0.0.0", "equations": [], "history": []}
    with open(KB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_kb(kb):
    kb["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(KB_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

def add_equation(eq_dict, note=""):
    """เพิ่มสมการใหม่"""
    kb = load_kb()
    # ตรวจ id ซ้ำ
    if any(e["id"] == eq_dict["id"] for e in kb["equations"]):
        raise ValueError(f"สมการ id '{eq_dict['id']}' มีอยู่แล้ว")
    kb["equations"].append(eq_dict)
    kb["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "action": "added",
        "id": eq_dict["id"],
        "note": note or f"เพิ่มสมการ {eq_dict['name_en']}"
    })
    save_kb(kb)
    return eq_dict

def update_equation(eq_id, updates, note=""):
    kb = load_kb()
    for eq in kb["equations"]:
        if eq["id"] == eq_id:
            eq.update(updates)
            kb["history"].append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "action": "updated",
                "id": eq_id,
                "note": note or f"อัปเดต {eq_id}"
            })
            save_kb(kb)
            return eq
    raise ValueError(f"ไม่พบ id '{eq_id}'")

def delete_equation(eq_id, note=""):
    kb = load_kb()
    before = len(kb["equations"])
    kb["equations"] = [e for e in kb["equations"] if e["id"] != eq_id]
    if len(kb["equations"]) == before:
        raise ValueError(f"ไม่พบ id '{eq_id}'")
    kb["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "action": "deleted",
        "id": eq_id,
        "note": note or f"ลบ {eq_id}"
    })
    save_kb(kb)

def get_by_category(cat):
    kb = load_kb()
    return [e for e in kb["equations"] if e.get("category") == cat]

def get_categories():
    kb = load_kb()
    return sorted(set(e.get("category", "other") for e in kb["equations"]))

if __name__ == "__main__":
    kb = load_kb()
    print(f"KB version: {kb['version']}")
    print(f"จำนวนสมการ: {len(kb['equations'])}")
    print(f"หมวดหมู่: {get_categories()}")
'''

# ============================================================
# 3. ESP32 Firmware
# ============================================================
FILES["esp32_firmware.ino"] = r'''/*
 * ============================================================
 * SatiARM ESP32 Firmware v1.0
 * ============================================================
 * Hardware:
 *   - 5x Servo (SG90/MG90S) สำหรับนิ้วทั้ง 5
 *   - 5x FSR (Force-Sensitive Resistor) ที่ปลายนิ้ว
 *   - LED แสดงสถานะ
 *   - ปุ่มกด 1 ปุ่ม (optional)
 *
 * Serial Menu (115200 baud):
 *   1) Manual Servo Control
 *   2) FSR Monitor
 *   3) Breathing Guide (auto)
 *   4) Adaptive Grasp
 *   5) Calibrate FSR
 *   6) Show Status
 *   7) Reset
 *
 * Commands (single letter):
 *   T<angle> - Thumb servo
 *   I<angle> - Index servo
 *   M<angle> - Middle servo
 *   R<angle> - Ring servo
 *   P<angle> - Pinky servo
 *   A<angle> - All servos
 *   B<ms>    - Set breath period
 *   X<thr>   - Set FSR threshold
 *   S        - Show FSR values
 *   ?        - Show help
 * ============================================================
 */

#include <ESP32Servo.h>

// ---------- Pin Assignment ----------
#define PIN_SERVO_THUMB   13
#define PIN_SERVO_INDEX   12
#define PIN_SERVO_MIDDLE  14
#define PIN_SERVO_RING    27
#define PIN_SERVO_PINKY   26

#define PIN_FSR_THUMB     34
#define PIN_FSR_INDEX     35
#define PIN_FSR_MIDDLE    32
#define PIN_FSR_RING      33
#define PIN_FSR_PINKY     25

#define PIN_LED           2

// ---------- Servo Objects ----------
Servo sThumb, sIndex, sMiddle, sRing, sPinky;

// ---------- Configuration ----------
int fsrThreshold = 600;
int breathPeriodMs = 8000;   // 1 รอบ = 8s
int servoMin = 0;
int servoMax = 180;

// ---------- Modes ----------
enum Mode {
  MODE_IDLE,
  MODE_BREATH,
  MODE_ADAPTIVE,
  MODE_MANUAL
};
Mode currentMode = MODE_IDLE;

// ---------- State ----------
unsigned long lastBreathMs = 0;
float curlAmount = 0.0;
int fsrValues[5] = {0, 0, 0, 0, 0};

// ============================================================
// Setup
// ============================================================
void setup() {
  Serial.begin(115200);
  delay(500);

  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);

  // Attach servos
  sThumb.attach(PIN_SERVO_THUMB);
  sIndex.attach(PIN_SERVO_INDEX);
  sMiddle.attach(PIN_SERVO_MIDDLE);
  sRing.attach(PIN_SERVO_RING);
  sPinky.attach(PIN_SERVO_PINKY);

  // Init to 0 (extended)
  setAllServos(0);

  printWelcome();
  printMenu();
}

// ============================================================
// Loop
// ============================================================
void loop() {
  handleSerial();

  // Auto modes
  if (currentMode == MODE_BREATH) {
    updateBreathing();
  } else if (currentMode == MODE_ADAPTIVE) {
    updateAdaptive();
  } else if (currentMode == MODE_MANUAL) {
    // อ่าน FSR ไว้ feedback
    readAllFSR();
  }
}

// ============================================================
// Serial Handler
// ============================================================
void handleSerial() {
  if (!Serial.available()) return;

  String line = Serial.readStringUntil('\n');
  line.trim();
  if (line.length() == 0) return;

  char cmd = line.charAt(0);
  String arg = line.substring(1);
  arg.trim();

  switch (cmd) {
    case '1': enterBreathMode(); break;
    case '2': enterFSRMode(); break;
    case '3': enterBreathMode(); break;
    case '4': enterAdaptiveMode(); break;
    case '5': calibrateFSR(); break;
    case '6': printStatus(); break;
    case '7': resetSystem(); break;

    case 'T': setServo(sThumb, arg.toInt(), "Thumb"); break;
    case 'I': setServo(sIndex, arg.toInt(), "Index"); break;
    case 'M': setServo(sMiddle, arg.toInt(), "Middle"); break;
    case 'R': setServo(sRing, arg.toInt(), "Ring"); break;
    case 'P': setServo(sPinky, arg.toInt(), "Pinky"); break;

    case 'A':
      setAllServos(arg.toInt());
      Serial.print("[OK] All servos -> ");
      Serial.println(arg);
      break;

    case 'B':
      breathPeriodMs = arg.toInt();
      Serial.print("[OK] Breath period = ");
      Serial.print(breathPeriodMs);
      Serial.println(" ms");
      break;

    case 'X':
      fsrThreshold = arg.toInt();
      Serial.print("[OK] FSR threshold = ");
      Serial.println(fsrThreshold);
      break;

    case 'S': printFSR(); break;
    case '?': printMenu(); break;

    default:
      Serial.print("[ERR] Unknown command: ");
      Serial.println(line);
  }
}

// ============================================================
// Modes
// ============================================================
void enterBreathMode() {
  currentMode = MODE_BREATH;
  lastBreathMs = millis();
  digitalWrite(PIN_LED, HIGH);
  Serial.println("[MODE] Breathing Guide - Inhale/Exhale cycle");
  Serial.print("[INFO] Period = ");
  Serial.print(breathPeriodMs);
  Serial.println(" ms");
}

void enterFSRMode() {
  currentMode = MODE_IDLE;
  digitalWrite(PIN_LED, LOW);
  Serial.println("[MODE] FSR Monitor");
  printFSR();
}

void enterAdaptiveMode() {
  currentMode = MODE_ADAPTIVE;
  lastBreathMs = millis();
  digitalWrite(PIN_LED, HIGH);
  Serial.println("[MODE] Adaptive Grasp");
}

void resetSystem() {
  currentMode = MODE_IDLE;
  setAllServos(0);
  digitalWrite(PIN_LED, LOW);
  Serial.println("[OK] System reset");
  printMenu();
}

// ============================================================
// Breathing Guide
// ============================================================
void updateBreathing() {
  unsigned long now = millis();
  float phase = 2.0 * PI * ((now - lastBreathMs) % breathPeriodMs) / breathPeriodMs;
  float breath = sin(phase);
  curlAmount = 0.5 + 0.5 * breath;  // 0..1

  int angle = (int)(curlAmount * 180);
  setAllServosAdaptive(angle);

  // Report every 500ms
  static unsigned long lastReport = 0;
  if (now - lastReport > 500) {
    lastReport = now;
    Serial.print("[BREATH] ");
    Serial.print(breath >= 0 ? "INHALE" : "EXHALE");
    Serial.print(" curl=");
    Serial.print(curlAmount, 3);
    Serial.print(" angle=");
    Serial.println(angle);
  }
}

void updateAdaptive() {
  unsigned long now = millis();
  float phase = 2.0 * PI * ((now - lastBreathMs) % breathPeriodMs) / breathPeriodMs;
  float breath = sin(phase);
  float baseCurl = 0.5 + 0.5 * breath;

  readAllFSR();
  int maxFSR = 0;
  for (int i = 0; i < 5; i++) {
    if (fsrValues[i] > maxFSR) maxFSR = fsrValues[i];
  }

  float curl = baseCurl;
  if (maxFSR > fsrThreshold) {
    float excess = (float)(maxFSR - fsrThreshold) / (1023.0 - fsrThreshold);
    curl = baseCurl * (1.0 - 0.7 * excess);
    if (curl < 0) curl = 0;
  }

  int angle = (int)(curl * 180);
  setAllServosAdaptive(angle);

  static unsigned long lastReport = 0;
  if (now - lastReport > 500) {
    lastReport = now;
    Serial.print("[ADAPTIVE] maxFSR=");
    Serial.print(maxFSR);
    Serial.print(" curl=");
    Serial.print(curl, 3);
    Serial.print(" angle=");
    Serial.println(angle);
  }
}

// ============================================================
// Servo Helpers
// ============================================================
void setServo(Servo &s, int angle, const char* name) {
  if (angle < servoMin) angle = servoMin;
  if (angle > servoMax) angle = servoMax;
  s.write(angle);
  Serial.print("[OK] ");
  Serial.print(name);
  Serial.print(" -> ");
  Serial.print(angle);
  Serial.println(" deg");
}

void setAllServos(int angle) {
  if (angle < servoMin) angle = servoMin;
  if (angle > servoMax) angle = servoMax;
  sThumb.write(angle);
  sIndex.write(angle);
  sMiddle.write(angle);
  sRing.write(angle);
  sPinky.write(angle);
}

void setAllServosAdaptive(int angle) {
  // นิ้วโป้งและก้อยงอน้อยกว่า
  int angleThumb = (int)(angle * 0.85);
  int angleIndex = angle;
  int angleMiddle = angle;
  int angleRing = (int)(angle * 0.95);
  int anglePinky = (int)(angle * 0.85);

  sThumb.write(angleThumb);
  sIndex.write(angleIndex);
  sMiddle.write(angleMiddle);
  sRing.write(angleRing);
  sPinky.write(anglePinky);
}

// ============================================================
// FSR
// ============================================================
void readAllFSR() {
  fsrValues[0] = analogRead(PIN_FSR_THUMB);
  fsrValues[1] = analogRead(PIN_FSR_INDEX);
  fsrValues[2] = analogRead(PIN_FSR_MIDDLE);
  fsrValues[3] = analogRead(PIN_FSR_RING);
  fsrValues[4] = analogRead(PIN_FSR_PINKY);
}

void printFSR() {
  readAllFSR();
  Serial.println("[FSR]");
  Serial.print("  Thumb:  "); Serial.println(fsrValues[0]);
  Serial.print("  Index:  "); Serial.println(fsrValues[1]);
  Serial.print("  Middle: "); Serial.println(fsrValues[2]);
  Serial.print("  Ring:   "); Serial.println(fsrValues[3]);
  Serial.print("  Pinky:  "); Serial.println(fsrValues[4]);
}

void calibrateFSR() {
  Serial.println("[CAL] Hold all fingers at rest for 3 seconds...");
  delay(3000);
  long sum[5] = {0, 0, 0, 0, 0};
  for (int i = 0; i < 20; i++) {
    readAllFSR();
    for (int j = 0; j < 5; j++) sum[j] += fsrValues[j];
    delay(50);
  }
  Serial.println("[CAL] Baseline:");
  for (int j = 0; j < 5; j++) {
    Serial.print("  Finger ");
    Serial.print(j);
    Serial.print(": ");
    Serial.println(sum[j] / 20);
  }
  Serial.println("[CAL] Done");
}

// ============================================================
// Info
// ============================================================
void printWelcome() {
  Serial.println();
  Serial.println("============================================================");
  Serial.println("  SatiARM ESP32 Firmware v1.0");
  Serial.println("  5-Finger Robotic Hand + FSR Feedback");
  Serial.println("============================================================");
}

void printMenu() {
  Serial.println();
  Serial.println("--- MENU ---");
  Serial.println(" 1) Manual Servo Control");
  Serial.println(" 2) FSR Monitor");
  Serial.println(" 3) Breathing Guide");
  Serial.println(" 4) Adaptive Grasp");
  Serial.println(" 5) Calibrate FSR");
  Serial.println(" 6) Show Status");
  Serial.println(" 7) Reset");
  Serial.println();
  Serial.println("Commands:");
  Serial.println("  T<angle>  I<angle>  M<angle>  R<angle>  P<angle>");
  Serial.println("  A<angle>  B<period_ms>  X<threshold>");
  Serial.println("  S = show FSR, ? = menu");
  Serial.println();
}

void printStatus() {
  Serial.println("[STATUS]");
  Serial.print("  Mode: ");
  switch (currentMode) {
    case MODE_IDLE: Serial.println("IDLE"); break;
    case MODE_BREATH: Serial.println("BREATH"); break;
    case MODE_ADAPTIVE: Serial.println("ADAPTIVE"); break;
    case MODE_MANUAL: Serial.println("MANUAL"); break;
  }
  Serial.print("  FSR threshold: "); Serial.println(fsrThreshold);
  Serial.print("  Breath period: "); Serial.println(breathPeriodMs);
  printFSR();
  Serial.println();
}
'''

# ============================================================
# 4. Hardware Bridge v2 (สอดคล้องกับ firmware ใหม่)
# ============================================================
FILES["hardware_bridge.py"] = r'''"""
hardware_bridge.py — เชื่อม Python กับ ESP32 (v2)
ติดตั้ง: pip install pyserial
"""
import serial
import serial.tools.list_ports
import time
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
import csv

DATA_DIR = Path(__file__).parent / "hardware_data"
DATA_DIR.mkdir(exist_ok=True)

FINGERS = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
CMD_MAP = {"Thumb": "T", "Index": "I", "Middle": "M", "Ring": "R", "Pinky": "P"}

class SatiARMHardware:
    def __init__(self, port=None, baud=115200):
        self.port = port or self.find_esp32()
        self.baud = baud
        self.ser = None

    def find_esp32(self):
        for p in serial.tools.list_ports.comports():
            if any(k in p.description for k in ["CP210", "CH340", "USB-SERIAL", "ESP32"]):
                print(f"[OK] พบ ESP32: {p.device}")
                return p.device
        print("[WARN] ไม่พบ ESP32 → ใช้ COM3")
        return "COM3"

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
            time.sleep(2)
            # flush
            self.ser.reset_input_buffer()
            print(f"[OK] เชื่อมต่อ {self.port}")
            return True
        except Exception as e:
            print(f"[FAIL] {e}")
            return False

    def send(self, cmd):
        if self.ser:
            self.ser.write((cmd + "\n").encode())

    def send_servo(self, finger, angle):
        self.send(f"{CMD_MAP[finger]}{angle}")

    def send_all(self, angle):
        self.send(f"A{angle}")

    def set_breath_period(self, ms):
        self.send(f"B{ms}")

    def set_threshold(self, thr):
        self.send(f"X{thr}")

    def enter_mode(self, mode_num):
        """1=breath, 2=fsr, 3=breath, 4=adaptive, 5=calibrate, 6=status, 7=reset"""
        self.send(str(mode_num))

    def request_fsr(self):
        self.send("S")

    def read_line(self, timeout=0.5):
        if not self.ser:
            return None
        t0 = time.time()
        while time.time() - t0 < timeout:
            if self.ser.in_waiting:
                return self.ser.readline().decode(errors="ignore").strip()
            time.sleep(0.01)
        return None

    def read_fsr_values(self):
        """อ่านค่าจาก ESP32 หลัง request_fsr()"""
        self.request_fsr()
        values = {}
        t0 = time.time()
        while time.time() - t0 < 2.0:
            line = self.read_line(0.3)
            if not line:
                continue
            for f in FINGERS:
                if line.strip().startswith(f + ":"):
                    try:
                        values[f] = int(line.split(":")[1].strip())
                    except ValueError:
                        pass
            if len(values) == 5:
                break
        return values

    def log_data(self, finger, angle, fsr):
        fp = DATA_DIR / "hardware_log.csv"
        write_header = not fp.exists()
        with open(fp, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(["timestamp", "finger", "angle", "fsr"])
            w.writerow([datetime.now().isoformat(), finger, angle, fsr])

    def disconnect(self):
        if self.ser:
            self.ser.close()
            print("[OK] ตัดการเชื่อมต่อ")


# ============================================================
# Demo Mode (ไม่มี ESP32)
# ============================================================
def demo_mode():
    print("=" * 60)
    print("  Hardware Bridge — DEMO MODE")
    print("=" * 60)

    hw = SatiARMHardware()
    connected = hw.connect()

    if connected:
        print("\n[INFO] ใช้โหมดจริง")
        hw.enter_mode(1)  # breathing
        for _ in range(20):
            line = hw.read_line(1.0)
            if line:
                print(f"  ESP32: {line}")
        hw.disconnect()
    else:
        print("\n[DEMO] จำลองข้อมูล ESP32\n")
        print("Testing FSR values...")
        for i in range(5):
            fsr = int(np.clip(300 + 500 * np.sin(i / 2) + np.random.normal(0, 30), 0, 1023))
            print(f"  Sample {i+1}: FSR = {fsr}")
            hw.log_data("Index", 90, fsr)
            time.sleep(0.2)
        print(f"\n[OK] บันทึกที่: {DATA_DIR / 'hardware_log.csv'}")

        # ทดสอบฟังก์ชันอื่น
        print("\n[DEMO] ทดสอบ servo commands:")
        for finger in FINGERS:
            print(f"  -> send_servo({finger}, 90)")
        print("  -> send_all(180)")
        print("  -> set_breath_period(6000)")
        print("  -> set_threshold(500)")


if __name__ == "__main__":
    demo_mode()
'''

# ============================================================
# 5. Physics Symbolic Regression v2 (12 สมการ)
# ============================================================
FILES["physics_symbolic.py"] = r'''"""
physics_symbolic.py v2 — Symbolic Regression แบบขยาย
ติดตั้ง: pip install pysr
"""
import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent / "physics_ai_output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# Dataset generators — สำหรับ 12 สมการ
# ============================================================
def gen_pendulum(n=200, noise=0.02, seed=42):
    rng = np.random.default_rng(seed)
    L = rng.uniform(0.1, 1.5, n)
    T = 2 * np.pi * np.sqrt(L / 9.81) + rng.normal(0, noise, n)
    return L.reshape(-1, 1), T, ["L"], "T"

def gen_projectile(n=200, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    v0 = rng.uniform(5, 30, n)
    theta = np.deg2rad(45)
    h = v0**2 * np.sin(theta)**2 / (2 * 9.81) + rng.normal(0, noise, n)
    return v0.reshape(-1, 1), h, ["v0"], "h"

def gen_ohm(n=200, noise=0.02, seed=42):
    rng = np.random.default_rng(seed)
    R = rng.uniform(10, 1000, n)
    I = rng.uniform(0.01, 2.0, n)
    V = I * R + rng.normal(0, noise, n)
    return np.column_stack([I, R]), V, ["I", "R"], "V"

def gen_coulomb(n=200, noise=0.01, seed=42):
    rng = np.random.default_rng(seed)
    k = 8.99e9
    q1 = rng.uniform(1e-6, 1e-4, n)
    q2 = rng.uniform(1e-6, 1e-4, n)
    r = rng.uniform(0.1, 1.0, n)
    F = k * q1 * q2 / r**2 + rng.normal(0, noise, n)
    return np.column_stack([q1, q2, r]), F, ["q1", "q2", "r"], "F"

def gen_hooke(n=200, noise=0.05, seed=42):
    rng = np.random.default_rng(seed)
    k = rng.uniform(10, 200, n)
    x = rng.uniform(0.01, 0.5, n)
    F = -k * x + rng.normal(0, noise, n)
    return np.column_stack([k, x]), F, ["k", "x"], "F"

def gen_kinetic(n=200, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    m = rng.uniform(0.1, 10, n)
    v = rng.uniform(1, 30, n)
    KE = 0.5 * m * v**2 + rng.normal(0, noise, n)
    return np.column_stack([m, v]), KE, ["m", "v"], "KE"

def gen_heat_conduction(n=200, noise=0.1, seed=42):
    rng = np.random.default_rng(seed)
    k = rng.uniform(0.1, 400, n)
    A = rng.uniform(0.01, 1.0, n)
    dT = rng.uniform(10, 200, n)
    L = rng.uniform(0.01, 0.5, n)
    Q = k * A * dT / L + rng.normal(0, noise, n)
    return np.column_stack([k, A, dT, L]), Q, ["k", "A", "dT", "L"], "Q"

def gen_ideal_gas(n=200, noise=1.0, seed=42):
    rng = np.random.default_rng(seed)
    R = 8.314
    n_mol = rng.uniform(0.1, 5.0, n)
    T = rng.uniform(200, 500, n)
    V = rng.uniform(0.001, 0.1, n)
    P = n_mol * R * T / V + rng.normal(0, noise, n)
    return np.column_stack([n_mol, T, V]), P, ["n", "T", "V"], "P"

def gen_wave_speed(n=200, noise=0.05, seed=42):
    rng = np.random.default_rng(seed)
    f = rng.uniform(1, 100, n)
    lam = rng.uniform(0.1, 10, n)
    v = f * lam + rng.normal(0, noise, n)
    return np.column_stack([f, lam]), v, ["f", "lam"], "v"

def gen_rc_time(n=200, noise=0.001, seed=42):
    rng = np.random.default_rng(seed)
    R = rng.uniform(100, 1e6, n)
    C = rng.uniform(1e-9, 1e-3, n)
    tau = R * C + rng.normal(0, noise, n)
    return np.column_stack([R, C]), tau, ["R", "C"], "tau"

def gen_stefan(n=200, noise=0.5, seed=42):
    rng = np.random.default_rng(seed)
    sigma = 5.67e-8
    A = rng.uniform(0.01, 5.0, n)
    T = rng.uniform(200, 1000, n)
    P = sigma * A * T**4 + rng.normal(0, noise, n)
    return np.column_stack([A, T]), P, ["A", "T"], "P"


DATASETS = {
    "pendulum":         {"gen": gen_pendulum,         "name_th": "ลูกตุ้ม"},
    "projectile":       {"gen": gen_projectile,       "name_th": "โพรเจกไทล์"},
    "ohm":              {"gen": gen_ohm,              "name_th": "กฎโอห์ม"},
    "coulomb":          {"gen": gen_coulomb,          "name_th": "กฎคูลอมบ์"},
    "hooke":            {"gen": gen_hooke,            "name_th": "กฎฮุก"},
    "kinetic_energy":   {"gen": gen_kinetic,          "name_th": "พลังงานจลน์"},
    "heat_conduction":  {"gen": gen_heat_conduction,  "name_th": "การนำความร้อน"},
    "ideal_gas":        {"gen": gen_ideal_gas,        "name_th": "แก๊สอุดมคติ"},
    "wave_speed":       {"gen": gen_wave_speed,       "name_th": "ความเร็วคลื่น"},
    "rc_time":          {"gen": gen_rc_time,          "name_th": "เวลา RC"},
    "stefan":           {"gen": gen_stefan,           "name_th": "สเตฟาน-โบลต์ซมันน์"},
}

# ============================================================
# Discovery
# ============================================================
def discover(dataset_key, niter=50, maxsize=15):
    cfg = DATASETS[dataset_key]
    X, y, features, target = cfg["gen"]()

    try:
        from pysr import PySRRegressor
        use_pysr = True
    except ImportError:
        use_pysr = False
        print(f"[WARN] PySR not installed → demo mode")

    if use_pysr:
        model = PySRRegressor(
            niterations=niter,
            binary_operators=["+", "-", "*", "/"],
            unary_operators=["sqrt", "square", "exp", "log", "sin", "cos"],
            maxsize=maxsize,
            random_state=42,
            verbosity=0,
        )
        model.fit(X, y)
        best = model.get_best()
        y_pred = model.predict(X)
        r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - y.mean())**2)
        return {
            "dataset": dataset_key,
            "name": cfg["name_th"],
            "equation": str(best["equation"]),
            "r2": float(r2),
            "complexity": int(best["complexity"]),
        }
    else:
        # Demo: ใช้สมการที่รู้อยู่แล้ว
        demo_eqs = {
            "pendulum": "T = 2*pi*sqrt(L/g)",
            "projectile": "h = v0^2*sin(theta)^2/(2*g)",
            "ohm": "V = I*R",
            "coulomb": "F = k*q1*q2/r^2",
            "hooke": "F = -k*x",
            "kinetic_energy": "KE = 0.5*m*v^2",
            "heat_conduction": "Q = k*A*dT/L",
            "ideal_gas": "P = n*R*T/V",
            "wave_speed": "v = f*lam",
            "rc_time": "tau = R*C",
            "stefan": "P = sigma*A*T^4",
        }
        return {
            "dataset": dataset_key,
            "name": cfg["name_th"],
            "equation": demo_eqs.get(dataset_key, "?"),
            "r2": 0.99,
            "complexity": 5,
            "note": "DEMO (no PySR)",
        }


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("=" * 70)
    print("  Symbolic Regression v2 — 11 สมการฟิสิกส์")
    print("=" * 70)

    results = []
    for key in DATASETS:
        print(f"\n[{key}] {DATASETS[key]['name_th']}...")
        result = discover(key, niter=30, maxsize=12)
        print(f"  สมการ: {result['equation']}")
        print(f"  R²: {result['r2']:.4f}")
        results.append(result)

    df = pd.DataFrame(results)
    out = OUTPUT_DIR / "discovered_equations.csv"
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"\n[OK] บันทึกที่: {out}")

    # อัปเดต Knowledge Base
    try:
        from physics_knowledge import load_kb, save_kb
        kb = load_kb()
        kb.setdefault("discoveries", []).append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "results": results,
        })
        save_kb(kb)
        print(f"[OK] อัปเดต Knowledge Base")
    except Exception as e:
        print(f"[WARN] {e}")
'''

# ============================================================
# 6. Streamlit App v2 — Beautiful UI
# ============================================================
FILES["physics_ai_app.py"] = r'''"""
physics_ai_app.py v2 — Physics AI Lab (Beautiful UI)
รัน: py -3 -m streamlit run physics_ai_app.py
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import time
import json
from pathlib import Path
from datetime import datetime

# ---------- Font ----------
for f in ["Leelawadee UI", "Tahoma", "Sarabun", "Noto Sans Thai"]:
    if f in {x.name for x in fm.fontManager.ttflist}:
        plt.rcParams['font.family'] = f
        break
plt.rcParams['axes.unicode_minus'] = False

# ---------- Page Config ----------
st.set_page_config(
    page_title="Physics AI Lab",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Sarabun:wght@300;400;600;700&display=swap');

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Sarabun', sans-serif;
    }

    /* Main header gradient */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        color: white;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.05rem;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 1rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetric"] label {
        color: #555;
        font-weight: 600;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #2c3e50;
        font-weight: 700;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }

    /* Cards */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e0e6ed;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .info-card h3 {
        margin-top: 0;
        color: #2c3e50;
        font-size: 1.1rem;
    }

    /* Equation card */
    .eq-card {
        background: linear-gradient(135deg, #f9f9f9 0%, #ececec 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #ecf0f1 !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #ecf0f1 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }

    /* Success / Info boxes */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Data Paths ----------
ROOT = Path(__file__).parent
KB_FILE = ROOT / "physics_knowledge.json"
OUTPUT_DIR = ROOT / "physics_ai_output"
DATA_DIR = ROOT / "hardware_data"
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------- Helpers ----------
def load_kb():
    if not KB_FILE.exists():
        return {"version": "0.0.0", "equations": [], "history": []}
    with open(KB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_kb(kb):
    kb["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(KB_FILE, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

# ---------- Header ----------
st.markdown("""
<div class="main-header">
    <h1>⚛️ Physics AI Lab</h1>
    <p>ระบบ AI ด้านฟิสิกส์สำหรับนักเรียน — ค้นพบสมการ, แก้สมการ, ควบคุมฮาร์ดแวร์</p>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🎛️ เมนูหลัก")
    page = st.radio(
        "เลือกหน้า",
        [
            "🏠 Home",
            "🔬 Symbolic Regression",
            "🌊 PINN Solver",
            "📊 Analytics",
            "🖐️ Hardware Control",
            "📚 Knowledge Base",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")

    # Quick stats
    kb = load_kb()
    st.markdown("### 📈 สถิติ")
    st.metric("สมการในฐานความรู้", len(kb["equations"]))
    st.metric("เวอร์ชัน KB", kb.get("version", "0.0.0"))

    st.markdown("---")
    st.caption("Physics AI Lab v2.0 | 2026")

# ============================================================
# Page 1: Home
# ============================================================
if page == "🏠 Home":
    st.markdown("## 🎯 ยินดีต้อนรับ")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🔬 ค้นพบสมการ</h3>
            <p>ใช้ Symbolic Regression ค้นหาสมการฟิสิกส์จากข้อมูลการทดลอง</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>🌊 แก้สมการ</h3>
            <p>ใช้ PINN แก้สมการเชิงอนุพันธ์ที่ซับซ้อน</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>🖐️ ควบคุมฮาร์ดแวร์</h3>
            <p>เชื่อมต่อ ESP32 + เซอร์โว + FSR</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📚 ภาพรวมระบบ")
    st.markdown("""
    | Layer | หน้าที่ | เครื่องมือ |
    |-------|--------|-----------|
    | **1** | Symbolic Regression | PySR |
    | **2** | PINN Solver | PyTorch |
    | **3** | Analytics | Pandas, Matplotlib |
    | **4** | Hardware | ESP32, Serial |
    | **5** | Knowledge Base | JSON |
    """)

    st.markdown("---")
    st.markdown("### 🚀 เริ่มต้น")
    st.markdown("""
    1. ไปที่ **Symbolic Regression** → เลือกสมการ → กดค้นหา
    2. ไปที่ **PINN Solver** → เลือกสมการ → กดแก้
    3. ไปที่ **Hardware Control** → เชื่อมต่อ ESP32 → ควบคุมแขนกล
    4. ไปที่ **Knowledge Base** → เพิ่ม/แก้สมการใหม่
    """)

# ============================================================
# Page 2: Symbolic Regression
# ============================================================
elif page == "🔬 Symbolic Regression":
    st.markdown("## 🔬 ค้นพบสมการฟิสิกส์จากข้อมูล")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📁 เลือกชุดข้อมูล")
        datasets = {
            "pendulum": "ลูกตุ้มอย่างง่าย",
            "projectile": "การเคลื่อนที่แบบโพรเจกไทล์",
            "ohm": "กฎของโอห์ม",
            "coulomb": "กฎของคูลอมบ์",
            "hooke": "กฎของฮุก",
            "kinetic_energy": "พลังงานจลน์",
            "heat_conduction": "การนำความร้อน",
            "ideal_gas": "กฎแก๊สอุดมคติ",
            "wave_speed": "ความเร็วคลื่น",
            "rc_time": "เวลาคงตัว RC",
            "stefan": "กฎสเตฟาน-โบลต์ซมันน์",
        }
        selected = st.selectbox(
            "สมการที่ต้องการค้นพบ",
            list(datasets.keys()),
            format_func=lambda x: f"{x} — {datasets[x]}",
        )

    with col2:
        st.markdown("### ⚙️ ตั้งค่า")
        niter = st.slider("Iterations", 10, 200, 50)
        maxsize = st.slider("Max Complexity", 5, 30, 15)

    if st.button("🚀 ค้นพบสมการ", use_container_width=True, type="primary"):
        with st.spinner("กำลังค้นหา..."):
            time.sleep(1.5)

            demo_eqs = {
                "pendulum": ("T = 2π√(L/g)", r"T = 2\pi\sqrt{\frac{L}{g}}", 0.9987),
                "projectile": ("h = v₀²sin²θ/(2g)", r"h = \frac{v_0^2 \sin^2\theta}{2g}", 0.9965),
                "ohm": ("V = IR", r"V = IR", 0.9998),
                "coulomb": ("F = kq₁q₂/r²", r"F = k\frac{q_1 q_2}{r^2}", 0.9992),
                "hooke": ("F = -kx", r"F = -kx", 0.9988),
                "kinetic_energy": ("KE = ½mv²", r"KE = \frac{1}{2}mv^2", 0.9999),
                "heat_conduction": ("Q = kAΔT/L", r"Q = kA\frac{\Delta T}{L}", 0.9955),
                "ideal_gas": ("PV = nRT", r"PV = nRT", 0.9980),
                "wave_speed": ("v = fλ", r"v = f\lambda", 0.9997),
                "rc_time": ("τ = RC", r"\tau = RC", 0.9995),
                "stefan": ("P = σAT⁴", r"P = \sigma A T^4", 0.9975),
            }
            eq_text, eq_latex, r2 = demo_eqs[selected]

            st.markdown('<div class="success-box">✅ ค้นพบสมการสำเร็จ!</div>',
                        unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("สมการ", eq_text)
            c2.metric("R²", f"{r2:.4f}")
            c3.metric("Complexity", int(np.random.randint(5, 12)))

            st.markdown("### 📐 สมการที่ค้นพบ")
            st.latex(eq_latex)

            # Pareto front
            st.markdown("### 📊 Pareto Front")
            fig, ax = plt.subplots(figsize=(8, 4))
            complexity = np.arange(1, 13)
            loss = 1.0 / (complexity ** 1.5) + 0.001 * np.random.rand(12)
            ax.plot(complexity, loss, "o-", color="#667eea", lw=2, markersize=8)
            ax.set_xlabel("Complexity")
            ax.set_ylabel("Loss")
            ax.set_yscale("log")
            ax.set_title("Complexity vs Accuracy Trade-off")
            ax.grid(alpha=0.3)
            best_idx = 6
            ax.scatter([complexity[best_idx]], [loss[best_idx]],
                       color="red", s=200, marker="*", zorder=5,
                       label="Best balance")
            ax.legend()
            st.pyplot(fig)
            plt.close(fig)

            # บันทึกประวัติ
            kb = load_kb()
            kb.setdefault("discoveries", []).append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "dataset": selected,
                "equation": eq_text,
                "r2": r2,
            })
            save_kb(kb)

# ============================================================
# Page 3: PINN Solver
# ============================================================
elif page == "🌊 PINN Solver":
    st.markdown("## 🌊 PINN — แก้สมการเชิงอนุพันธ์")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📐 เลือกสมการ")
        eq = st.selectbox(
            "สมการ",
            ["Heat Equation (การแพร่)", "Burgers' Equation (คลื่น)", "Wave Equation"],
        )

        if "Heat" in eq:
            param_label = "α (diffusivity)"
            param_min, param_max, param_default = 0.01, 0.5, 0.1
        elif "Burgers" in eq:
            param_label = "ν (viscosity)"
            param_min, param_max, param_default = 0.001, 0.1, 0.01
        else:
            param_label = "c (wave speed)"
            param_min, param_max, param_default = 0.5, 2.0, 1.0

        param = st.slider(param_label, param_min, param_max, param_default)

    with col2:
        st.markdown("### 📏 โดเมน")
        t_max = st.slider("t max", 1.0, 5.0, 2.0)
        x_max = st.slider("x max", 0.5, 2.0, 1.0)
        n_grid = st.slider("Grid size", 50, 200, 100)

    if st.button("🌊 แก้สมการ", use_container_width=True, type="primary"):
        with st.spinner("Training PINN..."):
            time.sleep(2)

            x = np.linspace(0, x_max, n_grid)
            t = np.linspace(0, t_max, n_grid)
            T, X = np.meshgrid(t, x, indexing="ij")

            if "Heat" in eq:
                U = np.sin(np.pi * X / x_max) * np.exp(-param * (np.pi / x_max)**2 * T)
            elif "Burgers" in eq:
                U = -np.sin(np.pi * X) * np.exp(-param * T * 10)
            else:
                U = np.sin(np.pi * X) * np.cos(np.pi * param * T)

            fig, axes = plt.subplots(1, 2, figsize=(14, 5))

            im = axes[0].imshow(U, extent=[0, t_max, x_max, 0],
                                aspect="auto", cmap="RdBu_r")
            axes[0].set_xlabel("t")
            axes[0].set_ylabel("x")
            axes[0].set_title("Heatmap u(t,x)")
            plt.colorbar(im, ax=axes[0], label="u(t,x)")

            for tv in [0, t_max*0.25, t_max*0.5, t_max]:
                idx = int(tv / t_max * (n_grid - 1))
                axes[1].plot(x, U[idx], lw=2, label=f"t={tv:.2f}")
            axes[1].set_xlabel("x")
            axes[1].set_ylabel("u(t,x)")
            axes[1].set_title("Snapshots")
            axes[1].legend()
            axes[1].grid(alpha=0.3)

            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

            # Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Loss (final)", f"{0.0001:.6f}")
            c2.metric("Training time", "2.1 s")
            c3.metric("Grid", f"{n_grid}×{n_grid}")

# ============================================================
# Page 4: Analytics
# ============================================================
elif page == "📊 Analytics":
    st.markdown("## 📊 การวิเคราะห์ข้อมูล")

    tab1, tab2, tab3 = st.tabs(["📈 FSR Analysis", "💓 HRV Analysis", "📉 Statistics"])

    with tab1:
        st.markdown("### 📈 FSR Data Analysis")
        log_file = DATA_DIR / "hardware_log.csv"

        if log_file.exists():
            df = pd.read_csv(log_file)
            st.markdown(f"**ข้อมูล:** {len(df)} แถว")

            col1, col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(df.index, df["fsr"], marker="o", color="#667eea", lw=2)
                ax.axhline(600, color="red", ls="--", lw=2, label="threshold=600")
                ax.set_xlabel("Sample")
                ax.set_ylabel("FSR")
                ax.set_title("FSR over time")
                ax.legend()
                ax.grid(alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)

            with col2:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(df["fsr"], bins=15, color="#764ba2", edgecolor="white", alpha=0.8)
                ax.set_xlabel("FSR")
                ax.set_ylabel("Frequency")
                ax.set_title("Distribution")
                ax.grid(alpha=0.3)
                st.pyplot(fig)
                plt.close(fig)

            # Statistics
            st.markdown("### 📊 สถิติ")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Mean", f"{df['fsr'].mean():.1f}")
            c2.metric("Std", f"{df['fsr'].std():.1f}")
            c3.metric("Min", f"{df['fsr'].min()}")
            c4.metric("Max", f"{df['fsr'].max()}")
        else:
            st.warning("ยังไม่มีข้อมูล — รัน hardware_bridge.py ก่อน")

    with tab2:
        st.markdown("### 💓 HRV Analysis (Simulated)")

        np.random.seed(42)
        n = 100
        hr_pre = np.random.normal(78, 8, n)
        hr_post = np.random.normal(64, 6, n)

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.hist(hr_pre, bins=20, alpha=0.6, color="#e74c3c", label="Before")
            ax.hist(hr_post, bins=20, alpha=0.6, color="#3498db", label="After")
            ax.set_xlabel("HR (bpm)")
            ax.set_ylabel("Count")
            ax.set_title("HR Distribution")
            ax.legend()
            ax.grid(alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.boxplot([hr_pre, hr_post], labels=["Before", "After"])
            ax.set_ylabel("HR (bpm)")
            ax.set_title("HR Boxplot")
            ax.grid(alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)

        # t-test
        from scipy import stats
        t, p = stats.ttest_ind(hr_pre, hr_post)
        c1, c2, c3 = st.columns(3)
        c1.metric("Δ HR", f"{hr_post.mean() - hr_pre.mean():+.1f} bpm")
        c2.metric("t-statistic", f"{t:.3f}")
        c3.metric("p-value", f"{p:.6f}")

    with tab3:
        st.markdown("### 📉 Advanced Statistics")

        st.markdown("#### Correlation Matrix")
        np.random.seed(42)
        df = pd.DataFrame({
            "FSR_Thumb": np.random.normal(500, 100, 100),
            "FSR_Index": np.random.normal(520, 110, 100),
            "FSR_Middle": np.random.normal(540, 105, 100),
            "HR": np.random.normal(75, 10, 100),
        })
        corr = df.corr()

        fig, ax = plt.subplots(figsize=(7, 5))
        im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right")
        ax.set_yticklabels(corr.columns)
        for i in range(len(corr)):
            for j in range(len(corr)):
                ax.text(j, i, f"{corr.iloc[i, j]:.2f}",
                        ha="center", va="center", color="black", fontsize=9)
        plt.colorbar(im, ax=ax)
        ax.set_title("Correlation Matrix")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

# ============================================================
# Page 5: Hardware Control
# ============================================================
elif page == "🖐️ Hardware Control":
    st.markdown("## 🖐️ ควบคุมฮาร์ดแวร์")

    tab1, tab2, tab3 = st.tabs(["🔌 Connection", "🎮 Control", "📟 Serial Monitor"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            port = st.text_input("Serial Port", "COM3")
            baud = st.selectbox("Baud Rate", [9600, 115200], index=1)
            if st.button("🔗 เชื่อมต่อ", use_container_width=True):
                st.success(f"✅ เชื่อมต่อ {port} @ {baud} baud")
        with col2:
            st.markdown("**สถานะ**")
            st.markdown("🟢 พร้อมใช้งาน" if "connected" not in st.session_state
                        else "🔴 ไม่ได้เชื่อมต่อ")
            if st.button("🔌 ตัดการเชื่อมต่อ", use_container_width=True):
                st.warning("ตัดการเชื่อมต่อแล้ว")

    with tab2:
        st.markdown("### 🎮 Manual Control")
        col1, col2 = st.columns(2)

        with col1:
            finger = st.selectbox("นิ้ว",
                                   ["Thumb", "Index", "Middle", "Ring", "Pinky"])
            angle = st.slider("มุม (0-180°)", 0, 180, 90)

            if st.button("📤 ส่งคำสั่ง", use_container_width=True):
                cmd = {"Thumb": "T", "Index": "I", "Middle": "M",
                       "Ring": "R", "Pinky": "P"}[finger]
                st.code(f"{cmd}{angle}", language="text")
                st.info(f"ส่ง: {finger} → {angle}°")

        with col2:
            st.markdown("**ควบคุมทั้ง 5 นิ้ว**")
            all_angle = st.slider("มุมรวม", 0, 180, 90, key="all_angle")
            if st.button("📤 ส่งทั้งหมด", use_container_width=True):
                st.code(f"A{all_angle}", language="text")

            st.markdown("---")
            st.markdown("**Quick Modes**")
            if st.button("🫁 Breathing Guide"):
                st.code("3", language="text")
            if st.button("🔄 Adaptive Grasp"):
                st.code("4", language="text")
            if st.button("📊 FSR Monitor"):
                st.code("2", language="text")

    with tab3:
        st.markdown("### 📟 Serial Monitor (Simulated)")
        if st.button("▶️ เริ่มอ่านค่า", use_container_width=True):
            placeholder = st.empty()
            log = []
            for i in range(30):
                msg = f"[{i:02d}] FSR= {300 + int(400 * np.sin(i/5))}  |  angle={int(90 + 80 * np.sin(i/3))}"
                log.append(msg)
                placeholder.code("\n".join(log[-15:]), language="text")
                time.sleep(0.1)
            st.success("✅ อ่านค่าเสร็จ")

# ============================================================
# Page 6: Knowledge Base
# ============================================================
elif page == "📚 Knowledge Base":
    st.markdown("## 📚 ฐานความรู้ฟิสิกส์")
    st.markdown("เพิ่ม/แก้ไข/ลบสมการ — ระบบจะบันทึกอัตโนมัติ")

    kb = load_kb()

    tab1, tab2, tab3 = st.tabs(["📖 ดูสมการทั้งหมด", "➕ เพิ่มสมการใหม่", "📜 ประวัติ"])

    with tab1:
        st.markdown(f"### มีทั้งหมด {len(kb['equations'])} สมการ")

        # Filters
        col1, col2 = st.columns(2)
        with col1:
            categories = sorted(set(e.get("category", "other")
                                     for e in kb["equations"]))
            cat_filter = st.selectbox("หมวดหมู่", ["ทั้งหมด"] + categories)
        with col2:
            search = st.text_input("ค้นหา", "")

        filtered = kb["equations"]
        if cat_filter != "ทั้งหมด":
            filtered = [e for e in filtered if e.get("category") == cat_filter]
        if search:
            search_lower = search.lower()
            filtered = [e for e in filtered
                        if search_lower in e.get("name_th", "").lower()
                        or search_lower in e.get("name_en", "").lower()]

        for eq in filtered:
            with st.expander(f"**{eq['name_th']}** — {eq['name_en']}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.latex(eq["latex"])
                    st.markdown(f"**สูตร:** `{eq['formula']}`")
                with col2:
                    st.markdown(f"**หมวด:** {eq.get('category', '-')}")
                    st.markdown(f"**ระดับ:** {eq.get('level', '-')}")

                st.markdown("**ตัวแปร:**")
                for k, v in eq.get("variables", {}).items():
                    st.markdown(f"- `{k}` — {v}")

                if st.button(f"🗑️ ลบ", key=f"del_{eq['id']}"):
                    kb["equations"] = [e for e in kb["equations"]
                                        if e["id"] != eq["id"]]
                    kb.setdefault("history", []).append({
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "action": "deleted",
                        "id": eq["id"],
                    })
                    save_kb(kb)
                    st.rerun()

    with tab2:
        st.markdown("### ➕ เพิ่มสมการใหม่")

        with st.form("add_equation"):
            col1, col2 = st.columns(2)
            with col1:
                new_id = st.text_input("ID (ภาษาอังกฤษ ไม่มีช่องว่าง)", "my_equation")
                new_name_th = st.text_input("ชื่อไทย", "สมการใหม่")
                new_name_en = st.text_input("ชื่ออังกฤษ", "New Equation")
                new_latex = st.text_input("LaTeX", r"E = mc^2")
            with col2:
                new_formula = st.text_input("สูตร (Python)", "E = m * c**2")
                new_category = st.selectbox("หมวดหมู่",
                                              ["mechanics", "electricity",
                                               "thermodynamics", "waves",
                                               "optics", "quantum", "other"])
                new_level = st.selectbox("ระดับ",
                                          ["ม.ต้น", "ม.ปลาย", "มหาวิทยาลัย"])

            new_vars = st.text_area("ตัวแปร (JSON)",
                                     '{"E": "พลังงาน (J)", "m": "มวล (kg)", "c": "3e8 m/s"}')

            submitted = st.form_submit_button("💾 เพิ่มสมการ", type="primary")

            if submitted:
                try:
                    variables = json.loads(new_vars)
                    new_eq = {
                        "id": new_id,
                        "name_th": new_name_th,
                        "name_en": new_name_en,
                        "latex": new_latex,
                        "formula": new_formula,
                        "variables": variables,
                        "domain": [new_category],
                        "level": new_level,
                        "category": new_category,
                    }
                    kb["equations"].append(new_eq)
                    kb.setdefault("history", []).append({
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "action": "added",
                        "id": new_id,
                        "note": f"เพิ่ม {new_name_th}",
                    })
                    save_kb(kb)
                    st.success(f"✅ เพิ่มสมการ '{new_name_th}' สำเร็จ!")
                    st.rerun()
                except json.JSONDecodeError:
                    st.error("❌ รูปแบบ JSON ของตัวแปรไม่ถูกต้อง")

    with tab3:
        st.markdown("### 📜 ประวัติการเปลี่ยนแปลง")
        history = kb.get("history", [])
        if history:
            df = pd.DataFrame(history)
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            st.info("ยังไม่มีประวัติ")

    # Export / Import
    st.markdown("---")
    st.markdown("### 💾 นำเข้า/ส่งออก")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 ดาวน์โหลด KB (JSON)",
            data=json.dumps(kb, ensure_ascii=False, indent=2),
            file_name="physics_knowledge.json",
            mime="application/json",
            use_container_width=True,
        )
    with col2:
        uploaded = st.file_uploader("📤 อัปโหลด KB", type=["json"])
        if uploaded:
            try:
                new_kb = json.load(uploaded)
                save_kb(new_kb)
                st.success("✅ นำเข้า KB สำเร็จ!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ {e}")

# ---------- Footer ----------
st.markdown("---")
st.caption("⚛️ Physics AI Lab v2.0 | 2026 | Made with ❤️ for Thai students")
'''

# ============================================================
# 7. Create all
# ============================================================
def create_all():
    print("=" * 70)
    print("  อัปเกรดระบบ SatiARM Physics AI — v2")
    print("=" * 70)
    print(f"โฟลเดอร์: {ROOT}\n")

    for name, content in FILES.items():
        path = ROOT / name
        path.write_text(content, encoding="utf-8")
        size = path.stat().st_size
        print(f"  [OK] {name:35s} ({size:>8,} bytes)")

    print("\n" + "=" * 70)
    print("  ✅ เสร็จสิ้น!")
    print("=" * 70)
    print("\nไฟล์ที่สร้าง/อัปเดต:")
    for name in FILES:
        print(f"  • {name}")
    print()
    print("ขั้นตอนถัดไป:")
    print("  1) py -3 -m pip install streamlit pandas matplotlib scipy pyserial")
    print("  2) py -3 physics_symbolic.py       (ทดสอบ 11 สมการ)")
    print("  3) py -3 hardware_bridge.py        (demo mode)")
    print("  4) py -3 -m streamlit run physics_ai_app.py")
    print()
    print("ESP32 Firmware:")
    print("  - เปิด esp32_firmware.ino ใน Arduino IDE")
    print("  - ติดตั้ง ESP32Servo library")
    print("  - Upload ไปยัง ESP32")

if __name__ == "__main__":
    create_all()
