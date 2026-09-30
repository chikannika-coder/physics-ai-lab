"""
╔══════════════════════════════════════════════════════════════╗
║  SatiARM Hand Simulation                                     ║
║  จำลองการทำงานของแขนกล 5 นิ้ว (Tendon-driven)                ║
║  เชื่อมกับจังหวะการหายใจ และค่าความสงบ (u) จาก PINN           ║
╚══════════════════════════════════════════════════════════════╝
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle, FancyBboxPatch
from pathlib import Path
import matplotlib.font_manager as fm

# ============================================================
# 1. ตั้งค่าฟอนต์และ Path
# ============================================================
def setup_font():
    thai_fonts = ["Leelawadee UI", "Leelawadee", "Tahoma", "Sarabun", "Noto Sans Thai"]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in thai_fonts:
        if name in available:
            plt.rcParams['font.family'] = name
            return True
    return False

HAS_THAI = setup_font()
plt.rcParams['axes.unicode_minus'] = False

def T(th, en):
    return th if HAS_THAI else en

OUTPUT_DIR = Path(__file__).parent / "satiarm_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 2. โมเดลจลนศาสตร์ของนิ้ว (Finger Kinematics)
# ============================================================
class Finger:
    """จำลองนิ้ว 1 นิ้ว มี 3 ข้อต่อ"""
    def __init__(self, base_x, base_y, lengths=(0.8, 0.6, 0.4)):
        self.base_x = base_x
        self.base_y = base_y
        self.L = lengths
        # มุมสูงสุดที่นิ้วจะงอได้ (องศา)
        self.max_angles = np.radians([80, 70, 60]) 
        
    def get_joint_positions(self, curl_amount):
        """
        คำนวณตำแหน่งข้อต่อทั้ง 4 จุด (โคน -> ปลาย)
        curl_amount: 0 = เหยียดตรง, 1 = งอเต็มที่
        """
        angles = self.max_angles * curl_amount
        x, y = self.base_x, self.base_y
        positions = [(x, y)]
        
        current_angle = 0
        for i in range(3):
            current_angle += angles[i]
            x += self.L[i] * np.cos(current_angle)
            y += self.L[i] * np.sin(current_angle)
            positions.append((x, y))
            
        return positions

# ============================================================
# 3. จำลองแขนกลทั้งมือ
# ============================================================
class RoboticHand:
    def __init__(self):
        # ตำแหน่งฐานของนิ้วทั้ง 5 (เรียงจากซ้ายไปขวา)
        # นิ้วโป้งจะอยู่ด้านข้าง
        self.fingers = {
            'thumb':  Finger(-1.2, 0.2, lengths=(0.7, 0.5, 0.4)),
            'index':  Finger(-0.6, 0.0, lengths=(0.8, 0.6, 0.4)),
            'middle': Finger( 0.0, 0.0, lengths=(0.9, 0.7, 0.4)),
            'ring':   Finger( 0.6, 0.0, lengths=(0.8, 0.6, 0.4)),
            'pinky':  Finger( 1.1, 0.0, lengths=(0.6, 0.5, 0.3)),
        }
        # ค่าเริ่มต้นของแต่ละนิ้ว (0 = เหยียด, 1 = กำ)
        self.curls = {name: 0.0 for name in self.fingers}
        
    def set_curls(self, curls_dict):
        for name, val in curls_dict.items():
            self.curls[name] = np.clip(val, 0, 1)
            
    def get_all_positions(self):
        return {name: finger.get_joint_positions(self.curls[name]) 
                for name, finger in self.fingers.items()}

# ============================================================
# 4. ฟังก์ชัน Animation
# ============================================================
def animate_hand(duration=16, fps=20):
    fig, (ax_hand, ax_graph) = plt.subplots(1, 2, figsize=(14, 7))
    
    hand = RoboticHand()
    
    # ตั้งค่าแกน
    ax_hand.set_xlim(-2, 2)
    ax_hand.set_ylim(-0.5, 2.5)
    ax_hand.set_aspect('equal')
    ax_hand.axis('off')
    ax_hand.set_title(T('จำลองแขนกล SatiARM', 'SatiARM Hand Simulation'), 
                      fontsize=14, fontweight='bold')
    
    # วาดฝ่ามือ
    palm = FancyBboxPatch((-1.5, -0.3), 3.0, 0.5, boxstyle="round,pad=0.1",
                          facecolor='#333333', edgecolor='black', lw=2)
    ax_hand.add_patch(palm)
    
    # วาดเส้นสาย (Tendon strings) และนิ้ว
    finger_lines = {}
    finger_joints = {}
    colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F1C40F', '#9B59B6']
    
    for i, (name, finger) in enumerate(hand.fingers.items()):
        line, = ax_hand.plot([], [], 'o-', color=colors[i], lw=6, 
                             markersize=10, markerfacecolor='white', 
                             markeredgecolor=colors[i], markeredgewidth=2,
                             label=name.capitalize())
        finger_lines[name] = line
        
        # จุดที่ปลายนิ้วสำหรับดึงสาย
        joint, = ax_hand.plot([], [], 'o', color='red', markersize=8)
        finger_joints[name] = joint
    
    ax_hand.legend(loc='upper right', fontsize=9)
    
    # กราฟแสดงค่าความสงบ (u) และการหายใจ
    ax_graph.set_xlim(0, duration)
    ax_graph.set_ylim(-1.2, 1.2)
    ax_graph.set_xlabel(T('เวลา (วินาที)', 'Time (s)'))
    ax_graph.set_ylabel(T('ค่าความสงบ (u) / การหายใจ', 'Calmness (u) / Breathing'))
    ax_graph.set_title(T('จังหวะการหายใจและค่าความสงบ', 'Breathing Rhythm & Calmness'), 
                       fontweight='bold')
    ax_graph.grid(True, alpha=0.3)
    ax_graph.axhline(y=0, color='gold', linestyle='--', label='Nibbana (u=0)')
    
    breath_line, = ax_graph.plot([], [], color='#2E86AB', lw=2, label='Breathing')
    calm_line, = ax_graph.plot([], [], color='#E74C3C', lw=2, label='Calmness (u)')
    ax_graph.legend(loc='upper right', fontsize=9)
    
    phase_text = ax_hand.text(0, 2.3, '', ha='center', fontsize=14, 
                              fontweight='bold')
    servo_text = ax_hand.text(0, -0.5, '', ha='center', fontsize=10, 
                              family='monospace', color='#555555')

    T_BREATH = 8.0 # 8 วินาทีต่อรอบหายใจ (เข้า 4s, ออก 4s)
    
    def update(frame):
        t = frame / fps
        
        # คำนวณจังหวะหายใจ (Sine wave)
        breath = np.sin(2 * np.pi * t / T_BREATH)
        
        # คำนวณค่าความสงบ (u) จากสมการแพร่ (ประมาณ)
        # u เริ่มสูง แล้วค่อยๆ ลดลงตามเวลา
        u_val = 1.0 * np.exp(-0.3 * t)
        
        # แปลงเป็นค่าการกำมือ (Curl)
        # หายใจเข้า -> กำมือ (curl = 1), หายใจออก -> แบมือ (curl = 0)
        # แต่ให้เชื่อมกับ u ด้วย: ถ้า u สูง (วุ่นวาย) -> กำมือแน่น
        curl_target = 0.5 + 0.5 * breath
        # ผสมกับ u เพื่อให้เห็นว่าความสงบลดลงเรื่อยๆ
        curl_amount = np.clip(curl_target * (0.5 + 0.5 * u_val), 0, 1)
        
        # อัปเดตนิ้ว
        curls_dict = {
            'thumb':  curl_amount * 0.8, # นิ้วโป้งงอน้อยกว่า
            'index':  curl_amount,
            'middle': curl_amount * 1.0,
            'ring':   curl_amount * 0.95,
            'pinky':  curl_amount * 0.85,
        }
        hand.set_curls(curls_dict)
        
        # วาดนิ้ว
        positions = hand.get_all_positions()
        for name, pos in positions.items():
            xs = [p[0] for p in pos]
            ys = [p[1] for p in pos]
            finger_lines[name].set_data(xs, ys)
            finger_joints[name].set_data([xs[-1]], [ys[-1]]) # จุดปลายนิ้ว
            
        # อัปเดตกราฟ
        t_arr = np.linspace(0, t, max(2, int(t * fps)))
        breath_arr = np.sin(2 * np.pi * t_arr / T_BREATH)
        u_arr = 1.0 * np.exp(-0.3 * t_arr)
        
        breath_line.set_data(t_arr, breath_arr)
        calm_line.set_data(t_arr, u_arr)
        
        # ข้อความ
        if breath >= 0:
            phase_text.set_text(T('🫁 หายใจเข้า (กำมือ)', '🫁 Inhale (Grasp)'))
            phase_text.set_color('seagreen')
        else:
            phase_text.set_text(T('💨 หายใจออก (แบมือ)', '💨 Exhale (Release)'))
            phase_text.set_color('steelblue')
            
        # แสดงค่ามุมเซอร์โว (0-180 องศา) เพื่อนำไปใช้กับ Arduino/ESP32
        servo_angles = {name: int(val * 180) for name, val in curls_dict.items()}
        servo_str = "Servo Angles: " + " | ".join([f"{k[:3]}:{v:3d}" for k, v in servo_angles.items()])
        servo_text.set_text(servo_str)
        
        return list(finger_lines.values()) + list(finger_joints.values()) + \
               [breath_line, calm_line, phase_text, servo_text]
    
    n_frames = duration * fps
    print(f"กำลังสร้าง Animation ({n_frames} frames)...")
    anim = FuncAnimation(fig, update, frames=n_frames, interval=1000/fps, blit=True)
    
    out_gif = OUTPUT_DIR / 'satiarm_hand_animation.gif'
    anim.save(str(out_gif), writer=PillowWriter(fps=fps))
    print(f"✓ บันทึก Animation: {out_gif}")
    plt.close()

# ============================================================
# 5. Main
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("  SatiARM Hand Simulation")
    print("=" * 65)
    animate_hand(duration=16, fps=20)
    print("\n✅ เสร็จแล้ว! ไฟล์อยู่ในโฟลเดอร์:", OUTPUT_DIR)