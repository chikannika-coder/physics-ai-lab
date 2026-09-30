"""hardware_bridge.py — เชื่อม Python กับ ESP32 (v2)"""
import serial
import serial.tools.list_ports
import time
import numpy as np
import csv
from pathlib import Path
from datetime import datetime

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
        print("[WARN] ไม่พบ ESP32 -> ใช้ COM3")
        return "COM3"

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=1)
            time.sleep(2)
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

def demo_mode():
    print("=" * 60)
    print("  Hardware Bridge — DEMO MODE")
    print("=" * 60)

    hw = SatiARMHardware()
    connected = hw.connect()

    if connected:
        print("\n[INFO] ใช้โหมดจริง")
        hw.enter_mode(1)
        for _ in range(20):
            line = hw.read_line(1.0)
            if line:
                print(f"  ESP32: {line}")
        hw.disconnect()
    else:
        print("\n[DEMO] จำลองข้อมูล ESP32\n")
        for i in range(5):
            fsr = int(np.clip(300 + 500 * np.sin(i / 2) + np.random.normal(0, 30), 0, 1023))
            print(f"  Sample {i+1}: FSR = {fsr}")
            hw.log_data("Index", 90, fsr)
            time.sleep(0.2)
        print(f"\n[OK] บันทึกที่: {DATA_DIR / 'hardware_log.csv'}")
        print("\n[DEMO] ทดสอบ commands:")
        for finger in FINGERS:
            print(f"  -> send_servo({finger}, 90)")
        print("  -> send_all(180)")
        print("  -> set_breath_period(6000)")
        print("  -> set_threshold(500)")

if __name__ == "__main__":
    demo_mode()
