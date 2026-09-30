"""
╔══════════════════════════════════════════════════════════════╗
║  PINN + ธรรมะ: สมการแห่งความดับสนิท                            ║
║  Heat/Diffusion Equation ผ่านเลนส์พุทธ                        ║
╚══════════════════════════════════════════════════════════════╝

หลักธรรมที่สอดคล้องกับสมการ:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  อนิจจัง (Anicca)  — ทุกสิ่งไม่เที่ยง ทุกค่าที่เกิดขึ้นย่อมสลาย
  ทุกขัง (Dukkha)   — การยึดมั่นในสิ่งที่ไม่เที่ยงนำมาซึ่งความทุกข์
  อนัตตา (Anatta)   — ไม่มีสิ่งใดเป็นของตน ค่าทั้งหมดละลายไป
  นิพพาน (Nibbana) — ความดับสนิท สถานะที่เป็นศูนย์ สงบ ปลงสงบ

สมการแพร่ความร้อน (Heat Equation):
    ∂u/∂t = α ∇²u

สมการนี้บรรยายธรรมชาติของสรรพสิ่ง:
  • u(t, x)     = สภาวะ/ปรากฏการณ์ ณ เวลา t และตำแหน่ง x
  • ∂u/∂t       = การเปลี่ยนแปลงตามกาลเวลา (ความไม่เที่ยง)
  • α (diffusivity) = ปัจจัยแห่งการสลาย (กฎแห่งอนิจจัง)
  • u → 0 เมื่อ t → ∞ = ทุกสิ่งย่อมดับสนิท (นิพพาน)

ไม่ว่าเงื่อนไขเริ่มต้น (กิเลส/ตัณหา) จะรุนแรงเพียงใด
สมการแห่งธรรมชาติจะนำทุกสิ่งกลับสู่ความสงบ — ศูนย์

"สพฺพ สงฺขารา อนิจฺจาติ" — สรรพสังขารทั้งหลายไม่เที่ยง
"สพฺพ สงฺขารา ทุกฺขาติ" — สรรพสังขารทั้งหลายเป็นทุกข์
"สพฺพ ธมฺมา อนตฺตาติ" — สรรพธรรมทั้งหลายเป็นอนัตตา
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ตั้งค่าฟอนต์ไทย+ละตินสำหรับ matplotlib (รวมฟอนต์ Noto Sans + Noto Sans Thai)
fm.fontManager.addfont('/home/user/workspace/NotoSansMerged.ttf')
plt.rcParams['font.family'] = 'Noto ThaiLatin'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 1. ตั้งค่า
# ============================================================
torch.manual_seed(42)
np.random.seed(42)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"อุปกรณ์ที่ใช้: {device}")

# α = ค่าการแพร่กระจาย (Diffusivity)
# ในบริบทธรรม: อัตราแห่งการสลายของสังขาร
ALPHA = 0.1  # ยิ่งสูง สิ่งต่าง ๆ สลายเร็วขึ้น


# ============================================================
# 2. Neural Network — "ตัวประมาณสภาวะ"
# ============================================================
class DhammaPINN(nn.Module):
    """
    โครงข่ายประสาทเทียมที่ประมาณสภาวะ u(t, x)
    ในบริบทธรรม: เป็นตัวแทนของ "ปรากฏการณ์ที่เกิดขึ้นแล้วดับไป"
    """
    def __init__(self, layers=[2, 64, 64, 64, 64, 1]):
        super().__init__()
        modules = []
        for i in range(len(layers) - 1):
            modules.append(nn.Linear(layers[i], layers[i + 1]))
            if i < len(layers) - 2:
                modules.append(nn.Tanh())
        self.net = nn.Sequential(*modules)

        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, t, x):
        tx = torch.cat([t, x], dim=1)
        return self.net(tx)


# ============================================================
# 3. ข้อมูลฝึก
# ============================================================
def generate_training_data(N_f=5000, N_bc=200, N_ic=200):
    """
    N_f : Collocation points — จุดที่สังเกตว่าสมการธรรมชาติเป็นจริง
    N_bc: Boundary points — ขอบเขต (สิ่งที่ยึดเหนี่ยว)
    N_ic: Initial condition — สภาวะเริ่มต้น (กิเลส/ตัณหา)
    """
    # Collocation: สุ่มในโดเมน t ∈ [0, T], x ∈ [0, L]
    T_max = 2.0   # เวลาสูงสุดที่สังเกต
    L = np.pi      # ขอบเขตเชิงพื้นที่

    t_f = torch.rand(N_f, 1, device=device) * T_max
    x_f = torch.rand(N_f, 1, device=device) * L

    # Boundary: ที่ขอบเขต x=0 และ x=L สภาวะต้องเป็นศูนย์
    # (ที่ขอบเขตแห่งโลก สิ่งทั้งหลายดับสนิท)
    t_bc = torch.rand(N_bc, 1, device=device) * T_max
    x_bc = torch.where(
        torch.rand(N_bc, 1, device=device) > 0.5,
        torch.full((N_bc, 1), float(L), device=device),
        torch.zeros((N_bc, 1), device=device)
    )
    u_bc = torch.zeros(N_bc, 1, device=device)  # u = 0 (ดับสนิท)

    # Initial condition: สภาวะเริ่มต้น — แทน "กิเลส/ตัณหา" ที่เกิดขึ้น
    # ใช้ฟังก์ชัน sin หลายความถี่ เพื่อแทนความซับซ้อนของกิเลส
    x_ic = torch.rand(N_ic, 1, device=device) * L
    t_ic = torch.zeros(N_ic, 1, device=device)
    # u(0, x) = sin(x) + 0.3*sin(3x) — สภาวะเริ่มต้นที่ "ไม่สงบ"
    u_ic = torch.sin(x_ic) + 0.3 * torch.sin(3 * x_ic)

    return t_f, x_f, t_bc, x_bc, u_bc, t_ic, x_ic, u_ic


# ============================================================
# 4. PDE Residual — "กฎแห่งอนิจจัง"
# ============================================================
def compute_dhamma_residual(model, t, x, alpha):
    """
    คำนวณ residual ของสมการแพร่:
        f = u_t - α * u_xx

    สมการนี้คือกฎแห่งธรรมชาติ:
        "การเปลี่ยนแปลงของสภาวะ = การแพร่กระจาย (สลาย) ตามกาลเวลา"

    ไม่ว่า u จะเป็นอะไร สมการนี้บังคับให้ทุกสิ่งสลายไปสู่ศูนย์
    """
    t = t.clone().requires_grad_(True)
    x = x.clone().requires_grad_(True)

    u = model(t, x)

    # ∂u/∂t = การเปลี่ยนแปลงตามกาลเวลา (อนิจจัง)
    u_t = torch.autograd.grad(
        u, t, grad_outputs=torch.ones_like(u), create_graph=True
    )[0]

    # ∂u/∂x
    u_x = torch.autograd.grad(
        u, x, grad_outputs=torch.ones_like(u), create_graph=True
    )[0]

    # ∂²u/∂x² = ความโค้งของสภาวะ (ความไม่สม่ำเสมอ)
    u_xx = torch.autograd.grad(
        u_x, x, grad_outputs=torch.ones_like(u_x), create_graph=True
    )[0]

    # Residual: u_t - α * u_xx = 0
    # ถ้า residual = 0 แปลว่าเป็นไปตามกฎธรรมชาติ
    f = u_t - alpha * u_xx

    return f, u_t, u_xx


# ============================================================
# 5. Loss Function — "เส้นทางสู่ความดับสนิท"
# ============================================================
def compute_loss(model, t_f, x_f, t_bc, x_bc, u_bc,
                 t_ic, x_ic, u_ic, alpha):
    """
    Loss รวม = Loss_ธรรมชาติ + Loss_ขอบเขต + Loss_เริ่มต้น

    แต่ละส่วนแทน:
    - Physics: ความเป็นไปตามกฎแห่งอนิจจัง
    - BC: การปล่อยวางที่ขอบเขต (สภาวะเป็นศูนย์)
    - IC: ยอมรับสภาพเริ่มต้น (กิเลสที่มีอยู่จริง)
    """

    # --- กฎแห่งอนิจจัง (Physics Loss) ---
    f, _, _ = compute_dhamma_residual(model, t_f, x_f, alpha)
    loss_physics = torch.mean(f ** 2)

    # --- การปล่อยวางที่ขอบเขต (BC Loss) ---
    u_pred_bc = model(t_bc, x_bc)
    loss_bc = torch.mean((u_pred_bc - u_bc) ** 2)

    # --- ยอมรับสภาพเริ่มต้น (IC Loss) ---
    u_pred_ic = model(t_ic, x_ic)
    loss_ic = torch.mean((u_pred_ic - u_ic) ** 2)

    loss = loss_physics + loss_bc + loss_ic

    return loss, loss_physics, loss_bc, loss_ic


# ============================================================
# 6. Training — "การปฏิบัติธรรม"
# ============================================================
def train(model, optimizer, t_f, x_f, t_bc, x_bc, u_bc,
          t_ic, x_ic, u_ic, alpha, epochs=2000, print_every=200):
    model.train()
    history = []

    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()

        loss, loss_p, loss_bc, loss_ic = compute_loss(
            model, t_f, x_f, t_bc, x_bc, u_bc,
            t_ic, x_ic, u_ic, alpha
        )

        loss.backward()
        optimizer.step()

        history.append(loss.item())

        if epoch % print_every == 0 or epoch == 1:
            # ตรวจสอบว่าสภาวะกำลังลดลงสู่ศูนย์หรือไม่
            t_check = torch.tensor([[1.0]], device=device)
            x_check = torch.tensor([[np.pi / 2]], device=device)
            with torch.no_grad():
                u_check = model(t_check, x_check)
            print(f"กาลที่ {epoch:5d}/{epochs} | "
                  f"Loss รวม: {loss.item():.6f} | "
                  f"อนิจจัง: {loss_p.item():.6f} | "
                  f"ปล่อยวาง: {loss_bc.item():.6f} | "
                  f"ตั้งต้น: {loss_ic.item():.6f} | "
                  f"u(1, π/2)={u_check.item():.4f}")

    return history


# ============================================================
# 7. กราฟผลลัพธ์
# ============================================================
def plot_results(model, history, alpha):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("PINN + ธรรมะ: สมการแห่งความดับสนิท\n"
                 r"$\partial u/\partial t = \alpha \nabla^2 u$"
                 " — ทุกสิ่งย่อมสลายสู่ศูนย์",
                 fontsize=14, fontweight='bold')

    L = np.pi
    T_max = 2.0

    # --- (a) Training Loss ---
    axes[0, 0].plot(history, linewidth=0.5, color='steelblue')
    axes[0, 0].set_xlabel('กาล (Epoch)')
    axes[0, 0].set_ylabel('Loss')
    axes[0, 0].set_title('(a) การปฏิบัติ — Loss ลดลง')
    axes[0, 0].set_yscale('log')
    axes[0, 0].grid(True, alpha=0.3)

    # --- (b) Heatmap u(t, x) ---
    t_test = torch.linspace(0, T_max, 100, device=device).view(-1, 1)
    x_test = torch.linspace(0, L, 100, device=device).view(-1, 1)
    T, X = torch.meshgrid(t_test.squeeze(), x_test.squeeze(), indexing='ij')
    t_flat = T.reshape(-1, 1)
    x_flat = X.reshape(-1, 1)
    with torch.no_grad():
        u_pred = model(t_flat, x_flat)
    U = u_pred.reshape(100, 100).cpu().numpy()

    im = axes[0, 1].imshow(
        U, extent=[0, L, T_max, 0],
        aspect='auto', cmap='RdBu_r', vmin=-1.3, vmax=1.3
    )
    axes[0, 1].set_xlabel('x (ตำแหน่ง)')
    axes[0, 1].set_ylabel('t (กาลเวลา)')
    axes[0, 1].set_title('(b) สภาวะ u(t, x) สลายสู่ศูนย์')
    cbar = plt.colorbar(im, ax=axes[0, 1])
    cbar.set_label('สภาวะ u(t, x)')

    # แสดงเส้น u=0 (นิพพาน)
    axes[0, 1].axhline(y=0, color='gold', linewidth=1.5, linestyle='--', alpha=0.7)

    # --- (c) Snapshots ที่เวลาต่าง ๆ ---
    t_snapshots = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0]
    colors = plt.cm.viridis(np.linspace(0, 0.9, len(t_snapshots)))
    x_plot = torch.linspace(0, L, 200, device=device).view(-1, 1)

    for t_val, color in zip(t_snapshots, colors):
        t_col = torch.full_like(x_plot, t_val)
        with torch.no_grad():
            u_plot = model(t_col, x_plot)
        label = f't = {t_val}'
        if t_val == 0:
            label += ' (เริ่มต้น)'
        elif t_val == T_max:
            label += ' (ใกล้ศูนย์)'
        axes[1, 0].plot(
            x_plot.cpu().numpy(), u_plot.cpu().numpy(),
            color=color, linewidth=2, label=label
        )

    axes[1, 0].axhline(y=0, color='gold', linewidth=1.5, linestyle='--',
                      alpha=0.7, label='นิพพาน (u = 0)')
    axes[1, 0].set_xlabel('x (ตำแหน่ง)')
    axes[1, 0].set_ylabel('สภาวะ u(t, x)')
    axes[1, 0].set_title('(c) สภาวะลดลงตามกาลเวลา')
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].grid(True, alpha=0.3)

    # --- (d) ค่าสูงสุด |u| เทียบกับเวลา (แสดงการสลายสู่ศูนย์) ---
    t_dec = torch.linspace(0, T_max, 200, device=device).view(-1, 1)
    max_u = []
    for t_val in t_dec:
        x_scan = torch.linspace(0, L, 200, device=device).view(-1, 1)
        t_scan = torch.full_like(x_scan, t_val.item())
        with torch.no_grad():
            u_scan = model(t_scan, x_scan)
        max_u.append(torch.max(torch.abs(u_scan)).item())

    axes[1, 1].plot(t_dec.cpu().numpy(), max_u, linewidth=2, color='crimson')
    axes[1, 1].fill_between(t_dec.cpu().numpy().flatten(), max_u, alpha=0.2, color='crimson')
    axes[1, 1].axhline(y=0, color='gold', linewidth=2, linestyle='--', alpha=0.8)
    axes[1, 1].set_xlabel('t (กาลเวลา)')
    axes[1, 1].set_ylabel('|u| ค่าสูงสุด')
    axes[1, 1].set_title('(d) ทุกสิ่งดับสนิทสู่ศูนย์')
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].annotate(
        'นิพพาน\n(ดับสนิท)',
        xy=(1.8, max_u[-1] if max_u else 0),
        xytext=(1.5, 0.5),
        fontsize=10, fontstyle='italic',
        arrowprops=dict(arrowstyle='->', color='gold'),
        color='goldenrod'
    )

    plt.tight_layout()
    plt.savefig('/home/user/workspace/pinn_dhamma_result.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("บันทึกภาพผลลัพธ์แล้ว")


# ============================================================
# 8. Main
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("  PINN + ธรรมะ: สมการแห่งความดับสนิท")
    print("  ∂u/∂t = α ∇²u")
    print("  IC: u(0,x) = sin(x) + 0.3·sin(3x)  [กิเลสเริ่มต้น]")
    print("  BC: u(t,0) = u(t,π) = 0              [ดับสนิทที่ขอบเขต]")
    print("  ผลลัพธ์: u → 0 เมื่อ t → ∞           [นิพพาน]")
    print("=" * 65)

    # สร้างข้อมูล
    t_f, x_f, t_bc, x_bc, u_bc, t_ic, x_ic, u_ic = generate_training_data()

    # สร้างโมเดล
    model = DhammaPINN(layers=[2, 64, 64, 64, 64, 1]).to(device)
    print(f"\nโครงข่าย: {model}")
    n_params = sum(p.numel() for p in model.parameters())
    print(f"จำนวนพารามิเตอร์: {n_params}")

    # Optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    # Training (การปฏิบัติธรรม)
    print("\n--- การปฏิบัติ (Adam) ---")
    history = train(
        model, optimizer, t_f, x_f, t_bc, x_bc, u_bc,
        t_ic, x_ic, u_ic, ALPHA, epochs=2000, print_every=200
    )

    # Fine-tuning (การขัดเกลา)
    print("\n--- การขัดเกลา (L-BFGS) ---")
    optimizer_lbfgs = torch.optim.LBFGS(
        model.parameters(), lr=1.0, max_iter=200,
        history_size=50, tolerance_grad=1e-6,
        tolerance_change=1e-9, line_search_fn='strong_wolfe'
    )

    def lbfgs_closure():
        optimizer_lbfgs.zero_grad()
        loss, _, _, _ = compute_loss(
            model, t_f, x_f, t_bc, x_bc, u_bc,
            t_ic, x_ic, u_ic, ALPHA
        )
        loss.backward()
        return loss

    optimizer_lbfgs.step(lbfgs_closure)
    final_loss, _, _, _ = compute_loss(
        model, t_f, x_f, t_bc, x_bc, u_bc,
        t_ic, x_ic, u_ic, ALPHA
    )
    print(f"Loss สุดท้ายหลังขัดเกลา: {final_loss.item():.6f}")

    # ตรวจสอบการสลายสู่ศูนย์
    print("\n--- ตรวจสอบ: สภาวะลดลงสู่ศูนย์ตามกาลเวลา ---")
    for t_val in [0.0, 0.5, 1.0, 1.5, 2.0]:
        x_mid = torch.tensor([[np.pi / 2]], device=device)
        t_col = torch.tensor([[t_val]], device=device)
        with torch.no_grad():
            u_val = model(t_col, x_mid)
        status = " (เริ่มต้น)" if t_val == 0 else ""
        if t_val >= 1.5:
            status = " (ใกล้ศูนย์)"
        print(f"  t = {t_val:.1f}: u = {u_val.item():.6f}{status}")

    # กราฟ
    plot_results(model, history, ALPHA)

    print("\n" + "=" * 65)
    print("  ข้อคิด:")
    print("  สภาวะเริ่มต้น (กิเลส) ไม่ว่าจะรุนแรงเพียงใด")
    print("  ตามกฎแห่งอนิจจัง ย่อมสลายสู่ศูนย์ในที่สุด")
    print("  นี่คือธรรมชาติของสรรพสิ่ง — และของสมการแพร่")
    print("=" * 65)
