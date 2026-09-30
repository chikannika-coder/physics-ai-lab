"""
Auto Update System — อัปเดตโมเดลเมื่อมีข้อมูลใหม่
"""
import time
import schedule
from pathlib import Path
import pandas as pd
from datetime import datetime
import subprocess
import json

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "hardware_data"
MODEL_DIR = PROJECT_DIR / "physics_ai_output" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = PROJECT_DIR / "update_log.json"

def check_new_data():
    """ตรวจสอบว่ามีข้อมูลใหม่หรือไม่"""
    log_file = DATA_DIR / "hardware_log.csv"
    if not log_file.exists():
        return False, 0

    df = pd.read_csv(log_file)
    current_count = len(df)

    # โหลดประวัติ
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            history = json.load(f)
        last_count = history.get("last_data_count", 0)
    else:
        last_count = 0

    new_samples = current_count - last_count
    return new_samples > 50, new_samples

def retrain_models():
    """Retrain โมเดลทั้งหมด"""
    print(f"\n{'='*60}")
    print(f"  🔄 Auto Update — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")

    # 1. Retrain Symbolic Regression
    print("\n[1/2] Retraining Symbolic Regression...")
    try:
        subprocess.run(
            ["py", "-3", "physics_symbolic.py"],
            cwd=PROJECT_DIR, timeout=600,
        )
        print("  ✓ Symbolic Regression เสร็จ")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # 2. Retrain PINN
    print("\n[2/2] Retraining PINN...")
    try:
        subprocess.run(
            ["py", "-3", "physics_pinn.py"],
            cwd=PROJECT_DIR, timeout=600,
        )
        print("  ✓ PINN เสร็จ")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # อัปเดต log
    log_file = DATA_DIR / "hardware_log.csv"
    if log_file.exists():
        df = pd.read_csv(log_file)
        history = {
            "last_data_count": len(df),
            "last_update": datetime.now().isoformat(),
            "total_updates": (json.load(open(LOG_FILE)).get("total_updates", 0) + 1
                              if LOG_FILE.exists() else 1),
        }
        with open(LOG_FILE, "w") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    print(f"\n✓ อัปเดตเสร็จ: {datetime.now().strftime('%H:%M')}")

def auto_update_job():
    """ตรวจสอบและอัปเดตอัตโนมัติ"""
    has_new, count = check_new_data()
    if has_new:
        print(f"📊 พบข้อมูลใหม่ {count} samples → เริ่มอัปเดต")
        retrain_models()
    else:
        print(f"  ไม่มีข้อมูลใหม่ (รอ {count} samples)")

# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  🔄 Auto Update System")
    print("  ตรวจสอบข้อมูลใหม่ทุก 1 ชั่วโมง")
    print("=" * 60)

    # ตรวจสอบทันทีครั้งแรก
    auto_update_job()

    # ตั้งเวลา
    schedule.every(1).hours.do(auto_update_job)
    schedule.every().day.at("02:00").do(retrain_models)  # full retrain ทุกคืน

    print("\n⏰ รอการอัปเดตถัดไป... (Ctrl+C เพื่อหยุด)")
    while True:
        schedule.run_pending()
        time.sleep(60)