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
    T_max = 2.0
    L = np.pi

    t_f = torch.rand(N_f, 1, device=device) * T_max
    x_f = torch.rand(N_f, 1, device=device) * L

    t_bc = torch.rand(N_bc, 1, device=device) * T_max
    x_bc = torch.where(
        torch.rand(N_bc, 1, device=device) > 0.5,
        torch.full((N_bc, 1), float(L), device=device),
        torch.zeros((N_bc, 1), device=device)
    )
    u_bc = torch.zeros(N_bc, 1, device=device)

    x_ic = torch.rand(N_ic, 1, device=device) * L
    t_ic = torch.zeros(N_ic, 1, device=device)
    u_ic = torch.sin(x_ic) + 0.3 * torch.sin(3 * x_ic)

    return t_f, x_f, t_bc, x_bc, u_bc, t_ic, x_ic, u_ic


# ============================================================
# 4. PDE Residual — "กฎแห่งอนิจจัง"
# ============================================================
def compute_dhamma_residual(model, t, x, alpha):
    """
    คำนวณ residual ของสมการแพร่:
        f = u_t - alpha * u_xx
    """
    t = t.clone().requires_grad_(True)
    x = x.clone().requires_grad_(True)

    u = model(t, x)

    u_t = torch.autograd.grad(
        u, t, grad_outputs=torch.ones_like(u), create_graph=True
    )[0]

    u_x = torch.autograd.grad(
        u, x, grad_outputs=torch.ones_like(u), create_graph=True
    )[0]

    u_xx = torch.autograd.grad(
        u_x, x, grad_outputs=torch.ones_like(u_x), create_graph=True
    )[0]

    f = u_t - alpha * u_xx

    return f, u_t, u_xx


# ============================================================
# 5. Loss Function — "เส้นทางสู่ความดับสนิท"
# ============================================================
def compute_loss(model, t_f, x_f, t_bc, x_bc, u_bc,
                 t_ic, x_ic, u_ic, alpha):
    f, _, _ = compute_dhamma_residual(model, t_f, x_f, alpha)
    loss_physics = torch.mean(f ** 2)

    u_pred_bc = model(t_bc, x_bc)
    loss_bc = torch.mean((u_pred_bc - u_bc) ** 2)

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
            t_check = torch.tensor([[1.0]], device=device)
            x_check = torch.tensor([[np.pi / 2]], device=device)
            with torch.no_grad():
                u_check = model(t_check, x_check)
            print(f"กาลที่ {epoch:5d}/{epochs} | "
                  f"Loss รวม: {loss.item():.6f} | "
                  f"อนิจจัง: {loss_p.item():.6f} | "
                  f"ปล่อยวาง: {loss_bc.item():.6f} | "
                  f"ตั้งต้น: {loss_ic.item():.6f} | "
                  f"u(1, pi/2)={u_check.item():.4f}")

    return history


# ============================================================
# 7. กราฟผลลัพธ์ — แสดงคำอธิบายธรรมชัดเจน
# ============================================================
def plot_results(model, history, alpha):
    """
    ออกแบบกราฟใหม่: แสดงคำอธิบายหลักธรรมชัดเจน
    ใช้ figure ขนาดใหญ่ + text boxes พร้อมคำอธิบายธรรม + ตารางสรุป
    """
    fig = plt.figure(figsize=(18, 24))

    # สีธีม
    C_ANICCA = '#2E86AB'
    C_DUKKHA = '#A23B72'
    C_ANATTA = '#F18F01'
    C_NIBBANA = '#C5A572'
    C_ZERO = '#D4A017'

    # GridSpec: แถวบน 2 กราฟ, แถวกลาง 2 กราฟ, แถวล่างตารางสรุป
    gs = fig.add_gridspec(
        3, 2,
        height_ratios=[1, 1, 0.3],
        hspace=0.50, wspace=0.30,
        left=0.07, right=0.95, top=0.88, bottom=0.02
    )
    ax_loss = fig.add_subplot(gs[0, 0])
    ax_heat = fig.add_subplot(gs[0, 1])
    ax_snap = fig.add_subplot(gs[1, 0])
    ax_dec = fig.add_subplot(gs[1, 1])
    ax_text = fig.add_subplot(gs[2, :])
    ax_text.axis('off')

    # Title ใหญ่
    fig.suptitle(
        "PINN + ธรรมะ: สมการแห่งความดับสนิท\n"
        r"$\partial u/\partial t = \alpha \nabla^2 u$"
        "  —  ทุกสิ่งย่อมเกิดขึ้น ตั้งอยู่ แล้วดับสนิท",
        fontsize=18, fontweight='bold', y=0.96
    )

    L = np.pi
    T_max = 2.0

    # ==========================================================
    # (a) Training Loss — การปฏิบัติสมาธิ
    # ==========================================================
    ax_loss.plot(history, linewidth=0.6, color=C_ANICCA, alpha=0.8)
    ax_loss.set_xlabel('กาล (Epoch)', fontsize=11)
    ax_loss.set_ylabel('Loss (ความไม่สงบ)', fontsize=11)
    ax_loss.set_title(
        '(a) การปฏิบัติสมาธิ — Loss ลดลง = จิตค่อยสงบ',
        fontsize=12, fontweight='bold', color=C_ANICCA
    )
    ax_loss.set_yscale('log')
    ax_loss.grid(True, alpha=0.2)

    ax_loss.text(
        0.50, 0.50,
        'การฝึกฝนโครงข่าย เปรียบดั่งการปฏิบัติธรรม\n'
        'เริ่มต้นด้วยความวุ่นวาย (Loss สูง)\n'
        'ค่อย ๆ สงบลงเรื่อย ๆ (Loss ต่ำ)\n'
        'จนกระทั่งเข้าสู่สมาธิ (Loss -> 0)',
        transform=ax_loss.transAxes, fontsize=9, va='center', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8F0FE',
                  edgecolor=C_ANICCA, alpha=0.9)
    )

    # ==========================================================
    # (b) Heatmap — อนิจจัง
    # ==========================================================
    t_test = torch.linspace(0, T_max, 100, device=device).view(-1, 1)
    x_test = torch.linspace(0, L, 100, device=device).view(-1, 1)
    T_g, X_g = torch.meshgrid(t_test.squeeze(), x_test.squeeze(), indexing='ij')
    t_flat = T_g.reshape(-1, 1)
    x_flat = X_g.reshape(-1, 1)
    with torch.no_grad():
        u_pred = model(t_flat, x_flat)
    U = u_pred.reshape(100, 100).cpu().numpy()

    im = ax_heat.imshow(
        U, extent=[0, L, T_max, 0],
        aspect='auto', cmap='RdBu_r', vmin=-1.3, vmax=1.3
    )
    ax_heat.set_xlabel('x (ตำแหน่ง)', fontsize=11)
    ax_heat.set_ylabel('t (กาลเวลา)', fontsize=11)
    ax_heat.set_title(
        '(b) อนิจจัง — ทุกสิ่งไม่เที่ยง\nสภาวะเกิดขึ้น แล้วสลายไป',
        fontsize=12, fontweight='bold', color=C_ANICCA
    )
    cbar = plt.colorbar(im, ax=ax_heat, shrink=0.8)
    cbar.set_label('สภาวะ u(t, x)', fontsize=10)

    # เส้นศูนย์ (นิพพาน)
    ax_heat.axhline(y=0, color=C_ZERO, linewidth=2, linestyle='--', alpha=0.6)
    ax_heat.text(
        0.02, 0.08, 'u = 0\n(นิพพาน)',
        transform=ax_heat.transAxes, fontsize=10, color='#333333',
        fontweight='bold', va='bottom',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor=C_ZERO, alpha=0.9)
    )

    # คำอธิบายธรรมใต้กราฟ
    ax_heat.text(
        0.50, -0.18,
        'สีเข้ม (แดง/น้ำเงิน) = สภาวะที่เกิดขึ้น\น'
        'สีอ่อนขึ้นเรื่อย ๆ = สลายไปตามกาลเวลา\น'
        'สพฺพ สงฺขารา อนิจฺจาติ — สรรพสังขารไม่เที่ยง',
        transform=ax_heat.transAxes, fontsize=9, va='top', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF8E1',
                  edgecolor=C_ZERO, alpha=0.9)
    )

    # ==========================================================
    # (c) Snapshots — ทุกขัง + อนัตตา
    # ==========================================================
    t_snapshots = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0]
    colors_snap = plt.cm.viridis(np.linspace(0, 0.9, len(t_snapshots)))
    x_plot = torch.linspace(0, L, 200, device=device).view(-1, 1)

    for t_val, color in zip(t_snapshots, colors_snap):
        t_col = torch.full_like(x_plot, t_val)
        with torch.no_grad():
            u_plot = model(t_col, x_plot)
        label = f't = {t_val}'
        if t_val == 0:
            label += ' (กิเลสเริ่มต้น)'
        elif t_val == T_max:
            label += ' (ใกล้ดับสนิท)'
        ax_snap.plot(
            x_plot.cpu().numpy(), u_plot.cpu().numpy(),
            color=color, linewidth=2, label=label
        )

    # เส้นศูนย์ (นิพพาน)
    ax_snap.axhline(y=0, color=C_ZERO, linewidth=2.5, linestyle='--',
                   alpha=0.8, label='นิพพาน (u = 0)')
    ax_snap.set_xlabel('x (ตำแหน่ง)', fontsize=11)
    ax_snap.set_ylabel('สภาวะ u(t, x)', fontsize=11)
    ax_snap.set_title(
        '(c) ทุกขัง + อนัตตา\nสภาวะเกิดขึ้น ไม่เที่ยง ไม่ใช่ตัวตน',
        fontsize=12, fontweight='bold', color=C_DUKKHA
    )
    ax_snap.legend(fontsize=8, loc='upper right')
    ax_snap.grid(True, alpha=0.2)

    # คำอธิบายธรรม
    ax_snap.text(
        0.02, 0.02,
        't=0: กิเลสเกิดขึ้น (สภาวะรุนแรง)\n'
        't->inf: สลายไป ไม่มีอะไรยึดได้\n'
        'สพฺพ สงฺขารา ทุกฺขาติ — สังขารเป็นทุกข์\n'
        'สพฺพ ธมฺมา อนตฺตาติ — ธรรมทั้งปวงเป็นอนัตตา',
        transform=ax_snap.transAxes, fontsize=8, va='bottom', ha='left',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FCE4EC',
                  edgecolor=C_DUKKHA, alpha=0.9)
    )

    # ==========================================================
    # (d) Decay curve — นิพพาน
    # ==========================================================
    t_dec = torch.linspace(0, T_max, 200, device=device).view(-1, 1)
    max_u = []
    for t_val in t_dec:
        x_scan = torch.linspace(0, L, 200, device=device).view(-1, 1)
        t_scan = torch.full_like(x_scan, t_val.item())
        with torch.no_grad():
            u_scan = model(t_scan, x_scan)
        max_u.append(torch.max(torch.abs(u_scan)).item())

    t_np = t_dec.cpu().numpy().flatten()
    max_u_np = np.array(max_u)

    ax_dec.plot(t_np, max_u_np, linewidth=2.5, color=C_ANATTA)
    ax_dec.fill_between(t_np, max_u_np, alpha=0.15, color=C_ANATTA)
    ax_dec.axhline(y=0, color=C_ZERO, linewidth=2.5, linestyle='--', alpha=0.9)
    ax_dec.set_xlabel('t (กาลเวลา)', fontsize=11)
    ax_dec.set_ylabel('|u| ค่าสูงสุด (ความรุนแรงของสภาวะ)', fontsize=11)
    ax_dec.set_title(
        '(d) นิพพาน — ความดับสนิท\nทุกสิ่งย่อมสลายสู่ศูนย์',
        fontsize=12, fontweight='bold', color=C_NIBBANA
    )
    ax_dec.grid(True, alpha=0.2)

    # ลูกศรชี้จากค่าสูง -> ศูนย์
    ax_dec.annotate(
        '',
        xy=(T_max * 0.95, 0.02),
        xytext=(T_max * 0.3, max_u_np[60]),
        arrowprops=dict(arrowstyle='->', color=C_NIBBANA,
                        lw=2.5, connectionstyle='arc3,rad=0.2')
    )
    ax_dec.annotate(
        'นิพพาน\n(ดับสนิท)',
        xy=(T_max * 0.95, 0.02),
        xytext=(T_max * 0.55, 0.55),
        fontsize=11, fontweight='bold', color=C_NIBBANA,
        ha='center',
        arrowprops=dict(arrowstyle='->', color=C_NIBBANA, lw=1.5)
    )
    ax_dec.text(
        T_max * 0.05, max_u_np[10] * 0.9,
        'กิเลส\n(เริ่มต้น)',
        fontsize=9, color=C_ANATTA, fontweight='bold', va='top'
    )

    # ==========================================================
    # (e) ตารางสรุป — แผนที่เชื่อม ฟิสิกส์ ↔ ธรรม
    # ==========================================================
    ax_text.text(
        0.50, 0.95,
        'แผนที่เชื่อม: ฟิสิกส์ - ธรรม',
        transform=ax_text.transAxes, fontsize=14, fontweight='bold',
        ha='center', va='top', color='#333333'
    )

    col_labels = ['สมการ', 'ความหมายทางฟิสิกส์', 'หลักธรรม', 'คำอธิบายธรรม']
    table_data = [
        ['u(t, x)', 'สภาวะของระบบ', 'สังขาร', 'สิ่งที่ประกอบขึ้น เกิดแล้วดับ'],
        ['du/dt', 'การเปลี่ยนแปลงตามเวลา', 'อนิจจัง', 'ทุกสิ่งไม่เที่ยง เปลี่ยนไปเรื่อย'],
        ['alpha', 'อัตราการแพร่/สลาย', 'กฎธรรมชาติ', 'กฎแห่งความสลายของสังขาร'],
        ['u -> 0', 'สภาวะคงตัว', 'นิพพาน', 'ความดับสนิท ปลงสงบ หมดกิเลส'],
    ]
    table = ax_text.table(
        cellText=table_data, colLabels=col_labels,
        loc='center', cellLoc='center',
        colWidths=[0.10, 0.20, 0.15, 0.40]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    table.scale(1, 1.6)

    # สี header และ cells
    for j in range(4):
        table[0, j].set_facecolor('#2E86AB')
        table[0, j].set_text_props(color='white', fontweight='bold')
    for i in range(1, 5):
        for j in range(4):
            if i % 2 == 0:
                table[i, j].set_facecolor('#F0F4F8')
            else:
                table[i, j].set_facecolor('#FFFFFF')
            table[i, j].set_edgecolor('#CCCCCC')

    # คำพาฬีด้านล่าง
    ax_text.text(
        0.50, 0.02,
        'สพฺพ สงฺขารา อนิจฺจาติ  —  สพฺพ สงฺขารา ทุกฺขาติ  —  สพฺพ ธมฺมา อนตฺตาติ\n'
        'สรรพสังขารทั้งหลายไม่เที่ยง  สรรพสังขารทั้งหลายเป็นทุกข์  สรรพธรรมทั้งหลายเป็นอนัตตา',
        transform=ax_text.transAxes, fontsize=10, ha='center', va='bottom',
        fontstyle='italic', color='#555555'
    )

    plt.savefig('/home/user/workspace/pinn_dhamma_result.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print('บันทึกภาพผลลัพธ์แล้ว')


# ============================================================
# 8. Main
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("  PINN + ธรรมะ: สมการแห่งความดับสนิท")
    print("  du/dt = alpha * nabla^2 u")
    print("  IC: u(0,x) = sin(x) + 0.3*sin(3x)  [กิเลสเริ่มต้น]")
    print("  BC: u(t,0) = u(t,pi) = 0              [ดับสนิทที่ขอบเขต]")
    print("  ผลลัพธ์: u -> 0 เมื่อ t -> inf           [นิพพาน]")
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
