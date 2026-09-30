"""
Auto Update System — อัปเดตโมเดลเมื่อมีข้อมูลใหม่
ติดตั้ง: pip install schedule
"""
import time
import json
from pathlib import Path
from datetime import datetime

try:
    import schedule
except ImportError:
    schedule = None
    print("[WARN] schedule not installed: pip install schedule")

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "hardware_data"
LOG_FILE = PROJECT_DIR / "update_log.json"

def check_new_data():
    log_file = DATA_DIR / "hardware_log.csv"
    if not log_file.exists():
        return False, 0
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        current_count = max(0, len(lines) - 1)
    except Exception:
        return False, 0

    last_count = 0
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                last_count = json.load(f).get("last_data_count", 0)
        except Exception:
            pass
    new_samples = current_count - last_count
    return new_samples >= 50, new_samples

def update_log(last_count):
    total = 1
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                total = json.load(f).get("total_updates", 0) + 1
        except Exception:
            pass
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "last_data_count": last_count,
            "last_update": datetime.now().isoformat(),
            "total_updates": total,
        }, f, indent=2, ensure_ascii=False)

def auto_update_job():
    print(f"\n{'=' * 60}")
    print(f"  Auto Update Check — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    has_new, count = check_new_data()
    if has_new:
        print(f"[NEW] พบข้อมูลใหม่ {count} samples -> เริ่มอัปเดต")
        # ในอนาคต: subprocess.run(["py", "-3", "physics_symbolic.py"])
        print("[STUB] ยังไม่ retrain จริง — เพิ่ม subprocess ภายหลัง")
        log_file = DATA_DIR / "hardware_log.csv"
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                n = max(0, len(f.readlines()) - 1)
        except Exception:
            n = 0
        update_log(n)
    else:
        print(f"[WAIT] ไม่มีข้อมูลใหม่ (รอ {count} samples)")

def run_scheduler():
    print("=" * 60)
    print("  Auto Update System")
    print("  ตรวจสอบทุก 1 ชั่วโมง")
    print("  Ctrl+C เพื่อหยุด")
    print("=" * 60)
    auto_update_job()
    if schedule is None:
        print("\n[WARN] ไม่มี schedule — จะรันครั้งเดียว")
        return
    schedule.every(1).hours.do(auto_update_job)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()
