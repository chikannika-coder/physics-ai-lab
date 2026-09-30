"""
╔══════════════════════════════════════════════════════════════╗
║  PINN + ธรรมะ: สมการแห่งความดับสนิท                            ║
║  สมการแพร่ความร้อน ผ่านเลนส์พุทธ                               ║
╚══════════════════════════════════════════════════════════════╝

หลักธรรมที่สอดคล้องกับสมการแพร่:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ติลักขณ์ ๓ (ลักษณะทั้ง ๓ ของสรรพสิ่ง):
    อนิจจัง (Anicca)  — ทุกสิ่งไม่เที่ยง ทุกค่าที่เกิดขึ้นย่อมสลาย
    ทุกขัง (Dukkha)   — การยึดมั่นในสิ่งที่ไม่เที่ยงนำมาซึ่งความทุกข์
    อนัตตา (Anatta)   — ไม่มีสิ่งใดเป็นของตน ค่าทั้งหมดละลายไป

  นิพพาน (Nibbana):
    ความดับสนิทแห่งกิเลส ตัณหา และอุปาทาน
    สถานะที่เป็นศูนย์ สงบ ปลงสงบ หมดความวุ่นวาย

  อริยสัจ ๔ (ความจริงอันประเสริฐ ๔ ประการ):
    ทุกข์      — สภาวะที่ไม่สงบ (u ไม่เป็นศูนย์)
    สมุทัย    — เหตุแห่งทุกข์ = ตัณหา/กิเลส (เงื่อนไขเริ่มต้น)
    นิโรธ     — ความดับแห่งทุกข์ (u -> 0)
    มรรค      — ทางนำสู่ความดับ (กระบวนการฝึก PINN)

สมการแพร่ความร้อน (Heat Equation):
    ส่วน u ที่เปลี่ยนไปตามกาลเวลา = อัตราการแพร่กระจาย x ความโค้งของสภาวะ

สมการนี้บรรยายธรรมชาติของสรรพสิ่ง:
  • u(t, x)          = สภาวะ/ปรากฏการณ์ ณ เวลา t และตำแหน่ง x
  • du/dt            = การเปลี่ยนแปลงตามกาลเวลา (ความไม่เที่ยง)
  • alpha            = ปัจจัยแห่งการสลาย (กฎแห่งอนิจจัง)
  • u ลู่เข้าสู่ 0    = ทุกสิ่งย่อมดับสนิท (นิพพาน)

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

# ตั้งค่าฟอนต์ไทย+ละตินสำหรับ matplotlib
fm.fontManager.addfont('/home/user/workspace/NotoSansMerged.ttf')
plt.rcParams['font.family'] = 'Noto ThaiLatin'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# ๑. ตั้งค่า
# ============================================================
torch.manual_seed(42)
np.random.seed(42)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"อุปกรณ์ที่ใช้: {device}")

# alpha = ค่าการแพร่กระจาย (Diffusivity)
# ในบริบทธรรม: อัตราแห่งการสลายของสังขาร
ALPHA = 0.1


# ============================================================
# ๒. โครงข่ายประสาทเทียม — "ตัวประมาณสภาวะ"
# ============================================================
class DhammaPINN(nn.Module):
    """ประมาณสภาวะ u(t, x) — ปรากฏการณ์ที่เกิดขึ้นแล้วดับไป"""
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
# ๓. สร้างข้อมูลฝึก
# ============================================================
def generate_training_data(N_f=5000, N_bc=200, N_ic=200):
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
# ๔. คำนวณเศษเหลือของสมการ — "กฎแห่งอนิจจัง"
# ============================================================
def compute_dhamma_residual(model, t, x, alpha):
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
# ๕. ฟังก์ชันความสูญเสีย — "เส้นทางสู่ความดับสนิท"
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
# ๖. การฝึกฝน — "การปฏิบัติธรรม"
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
                  f"ค่าคลาดเคลื่อนรวม: {loss.item():.6f} | "
                  f"อนิจจัง: {loss_p.item():.6f} | "
                  f"ปล่อยวาง: {loss_bc.item():.6f} | "
                  f"ตั้งต้น: {loss_ic.item():.6f} | "
                  f"u(1, pi/2)={u_check.item():.4f}")

    return history


# ============================================================
# ๗. กราฟผลลัพธ์ — แสดงหลักธรรมเป็นภาษาไทยทั้งหมด
# ============================================================
def plot_results(model, history, alpha):
    """
    กราฟที่อธิบายหลักธรรมด้วยภาษาไทยอย่างละเอียด
    ประกอบด้วย ๔ กราฟย่อย + ตารางสรุป + ส่วนอธิบายธรรม
    """
    fig = plt.figure(figsize=(20, 36))

    # สีธีม — ใช้สีที่สอดคล้องกับธรรม
    C_ANICCA = '#2E86AB'   # น้ำเงิน — อนิจจัง (ความไม่เที่ยง)
    C_DUKKHA = '#A23B72'   # ม่วงแดง — ทุกขัง (ความทุกข์)
    C_ANATTA = '#F18F01'   # ส้ม — อนัตตา (ความไม่ใช่ตน)
    C_NIBBANA = '#C5A572'  # ทอง — นิพพาน (ความดับสนิท)
    C_ZERO = '#D4A017'     # ทองเข้ม — เส้นศูนย์ (สภาวะดับสนิท)
    C_DARK = '#333333'

    # จัดวางกราฟ: ๔ กราฟย่อย + ตารางสรุป + กล่องอธิบายธรรม
    gs = fig.add_gridspec(
        4, 2,
        height_ratios=[1, 1, 0.30, 0.75],
        hspace=0.60, wspace=0.28,
        left=0.06, right=0.96, top=0.87, bottom=0.03
    )
    ax_loss = fig.add_subplot(gs[0, 0])
    ax_heat = fig.add_subplot(gs[0, 1])
    ax_snap = fig.add_subplot(gs[1, 0])
    ax_dec = fig.add_subplot(gs[1, 1])
    ax_table = fig.add_subplot(gs[2, :])
    ax_table.axis('off')
    ax_dhamma = fig.add_subplot(gs[3, :])
    ax_dhamma.axis('off')

    # หัวเรื่องใหญ่
    fig.suptitle(
        "สมการแห่งความดับสนิท\n"
        r"$\partial u/\partial t = \alpha \nabla^2 u$"
        "  —  ทุกสิ่งย่อมเกิดขึ้น ตั้งอยู่ แล้วดับสนิท",
        fontsize=20, fontweight='bold', y=0.95
    )

    L = np.pi
    T_max = 2.0

    # ==========================================================
    # (ก) กราฟค่าความสูญเสีย — การปฏิบัติสมาธิ
    # ==========================================================
    ax_loss.plot(history, linewidth=0.6, color=C_ANICCA, alpha=0.8)
    ax_loss.set_xlabel('กาล (รอบการฝึก)', fontsize=11)
    ax_loss.set_ylabel('ค่าความคลาดเคลื่อน (ความไม่สงบของจิต)', fontsize=11)
    ax_loss.set_title(
        '(ก) การปฏิบัติสมาธิ\nค่าความสูญเสียลดลง = จิตค่อย ๆ สงบ',
        fontsize=13, fontweight='bold', color=C_ANICCA
    )
    ax_loss.set_yscale('log')
    ax_loss.grid(True, alpha=0.2)

    # กล่องคำอธิบายธรรม
    ax_loss.text(
        0.50, 0.50,
        'การฝึกฝนโครงข่ายประสาทเทียม\n'
        'เปรียบดั่งการปฏิบัติธรรมของผู้ฝึกจิต\n'
        '\n'
        'เริ่มต้น: จิตวุ่นวาย (ค่าสูญเสียสูง)\n'
        'ค่อย ๆ สงบลงเรื่อย ๆ (ค่าสูญเสียลดลง)\n'
        'จนกระทั่งเข้าสู่สมาธิ (ค่าสูญเสียเข้าใกล้ศูนย์)\n'
        '\n'
        'เหมือนผู้ฝึกสมาธิที่เริ่มจากจิตฟุ้งซ่าน\n'
        'แล้วค่อย ๆ รวบรวมสงบลงจนเป็นสมาธิ',
        transform=ax_loss.transAxes, fontsize=9, va='center', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8F0FE',
                  edgecolor=C_ANICCA, alpha=0.92)
    )

    # ==========================================================
    # (ข) แผนภาพความร้อน — อนิจจัง
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
    ax_heat.set_xlabel('ตำแหน่ง x', fontsize=11)
    ax_heat.set_ylabel('กาลเวลา t', fontsize=11)
    ax_heat.set_title(
        '(ข) อนิจจัง — ความไม่เที่ยง\nสภาวะเกิดขึ้น ตั้งอยู่ แล้วสลายไป',
        fontsize=13, fontweight='bold', color=C_ANICCA
    )
    cbar = plt.colorbar(im, ax=ax_heat, shrink=0.8)
    cbar.set_label('สภาวะ u(t, x)', fontsize=10)

    # เส้นศูนย์ (นิพพาน)
    ax_heat.axhline(y=0, color=C_ZERO, linewidth=2, linestyle='--', alpha=0.6)
    ax_heat.text(
        0.02, 0.08, 'u = 0\n(นิพพาน)',
        transform=ax_heat.transAxes, fontsize=10, color=C_DARK,
        fontweight='bold', va='bottom',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor=C_ZERO, alpha=0.9)
    )

    # กล่องอธิบายธรรมใต้กราฟ (ข)
    ax_heat.text(
        0.50, -0.12,
        'สีเข้ม = สภาวะที่เกิดขึ้น ยังไม่สงบ\n'
        'สีอ่อนขึ้น = สลายไปตามกาลเวลา\n'
        'สพฺพ สงฺขารา อนิจฺจาติ — สรรพสังขารไม่เที่ยง',
        transform=ax_heat.transAxes, fontsize=8, va='top', ha='center',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8E1',
                  edgecolor=C_ZERO, alpha=0.92)
    )

    # ==========================================================
    # (ค) ภาพรวมสภาวะ — ทุกขัง + อนัตตา
    # ==========================================================
    t_snapshots = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0]
    colors_snap = plt.cm.viridis(np.linspace(0, 0.9, len(t_snapshots)))
    x_plot = torch.linspace(0, L, 200, device=device).view(-1, 1)

    for t_val, color in zip(t_snapshots, colors_snap):
        t_col = torch.full_like(x_plot, t_val)
        with torch.no_grad():
            u_plot = model(t_col, x_plot)
        label = f'กาล t = {t_val}'
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
    ax_snap.set_xlabel('ตำแหน่ง x', fontsize=11)
    ax_snap.set_ylabel('สภาวะ u(t, x)', fontsize=11)
    ax_snap.set_title(
        '(ค) ทุกขัง + อนัตตา\nสภาวะเกิดขึ้น ไม่เที่ยง ไม่ใช่ตัวตน',
        fontsize=13, fontweight='bold', color=C_DUKKHA
    )
    ax_snap.legend(fontsize=8, loc='upper right')
    ax_snap.grid(True, alpha=0.2)

    # กล่องอธิบายธรรม
    ax_snap.text(
        0.02, 0.02,
        'กาลเริ่มต้น: กิเลสเกิดขึ้น (สภาวะรุนแรง)\n'
        'กาลผ่านไป: สลายไป ไม่มีสิ่งใดยึดได้\n'
        '\n'
        'สพฺพ สงฺขารา ทุกฺขาติ\n'
        '  สังขารทั้งหลายเป็นทุกข์\n'
        '  เพราะไม่เที่ยง ทนอยู่ไม่ได้\n'
        '\n'
        'สพฺพ ธมฺมา อนตฺตาติ\n'
        '  ธรรมทั้งปวงเป็นอนัตตา\n'
        '  ไม่ใช่ตัวตน ไม่ใช่ของตน\n'
        '  สลายไปในที่สุด',
        transform=ax_snap.transAxes, fontsize=8, va='bottom', ha='left',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FCE4EC',
                  edgecolor=C_DUKKHA, alpha=0.92)
    )

    # ==========================================================
    # (ง) กราฟการสลาย — นิพพาน
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
    ax_dec.set_xlabel('กาลเวลา t', fontsize=11)
    ax_dec.set_ylabel('|u| ค่าสูงสุด (ความรุนแรงของสภาวะ)', fontsize=11)
    ax_dec.set_title(
        '(ง) นิพพาน — ความดับสนิท\nทุกสิ่งย่อมสลายสู่ศูนย์',
        fontsize=13, fontweight='bold', color=C_NIBBANA
    )
    ax_dec.grid(True, alpha=0.2)

    # ลูกศรชี้จากกิเลส -> นิพพาน
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
        fontsize=12, fontweight='bold', color=C_NIBBANA,
        ha='center',
        arrowprops=dict(arrowstyle='->', color=C_NIBBANA, lw=1.5)
    )
    ax_dec.text(
        T_max * 0.05, max_u_np[10] * 0.9,
        'กิเลส\n(เริ่มต้น)',
        fontsize=10, color=C_ANATTA, fontweight='bold', va='top'
    )

    # กล่องอธิบายธรรมใต้กราฟ (ง)
    ax_dec.text(
        0.50, -0.12,
        'นิพพาน = ความดับสนิทแห่งกิเลส ตัณหา อุปาทาน\n'
        'นิโรธ คือความดับแห่งทุกข์ สภาวะเป็นศูนย์ สงบ ปลงสงบ',
        transform=ax_dec.transAxes, fontsize=8, va='top', ha='center',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF3E0',
                  edgecolor=C_NIBBANA, alpha=0.92)
    )

    # ==========================================================
    # ตารางสรุป — แผนที่เชื่อม ฟิสิกส์กับธรรม
    # ==========================================================
    ax_table.text(
        0.50, 1.05,
        'แผนที่เชื่อม: สมการฟิสิกส์กับหลักธรรม',
        transform=ax_table.transAxes, fontsize=15, fontweight='bold',
        ha='center', va='top', color=C_DARK
    )

    col_labels = [
        'ส่วนของสมการ',
        'ความหมายทางฟิสิกส์',
        'หลักธรรมที่สอดคล้อง',
        'คำอธิบายตามหลักธรรม'
    ]
    table_data = [
        [
            'u(t, x)',
            'สภาวะของระบบ ณ เวลาและตำแหน่ง',
            'สังขาร',
            'สิ่งที่ประกอบขึ้นจากเหตุปัจจัย เกิดขึ้นแล้วดับไป'
        ],
        [
            'du/dt',
            'อัตราการเปลี่ยนแปลงตามกาลเวลา',
            'อนิจจัง',
            'ทุกสิ่งไม่เที่ยง มีการเกิดขึ้น ตั้งอยู่ แล้วดับไป'
        ],
        [
            'alpha',
            'ค่าการแพร่กระจาย อัตราการสลาย',
            'กฎแห่งธรรมชาติ',
            'กฎที่บังคับให้สังขารต้องสลายไปตามกาลเวลา'
        ],
        [
            'u ลู่เข้าสู่ 0',
            'สภาวะคงตัว ไม่เปลี่ยนแปลง',
            'นิพพาน',
            'ความดับสนิท ปลงสงบ หมดกิเลส ตัณหา อุปาทาน'
        ],
        [
            'เงื่อนไขเริ่มต้น',
            'ค่า u ที่เวลา t = 0',
            'กิเลส/ตัณหา',
            'สภาพเริ่มต้นแห่งความไม่สงบ ที่ต้องฝึกฝนเพื่อสลาย'
        ],
        [
            'เงื่อนไขขอบเขต',
            'ค่า u ที่ขอบเขตของโดเมน',
            'การปล่อยวาง',
            'การปล่อยวางยึดเหนี่ยว ณ ขอบเขตแห่งโลก'
        ],
        [
            'การฝึกฝนโครงข่าย',
            'กระบวนการลดค่าความสูญเสีย',
            'มรรค (ทาง)',
            'ข้อปฏิบัติสู่ความดับแห่งทุกข์ คืออริยมรรคมีองค์แปด'
        ],
    ]
    table = ax_table.table(
        cellText=table_data, colLabels=col_labels,
        loc='center', cellLoc='center',
        colWidths=[0.12, 0.20, 0.15, 0.38]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.7)

    # สี header และ cells
    for j in range(4):
        table[0, j].set_facecolor(C_ANICCA)
        table[0, j].set_text_props(color='white', fontweight='bold')
    for i in range(1, len(table_data) + 1):
        for j in range(4):
            if i % 2 == 0:
                table[i, j].set_facecolor('#F0F4F8')
            else:
                table[i, j].set_facecolor('#FFFFFF')
            table[i, j].set_edgecolor('#CCCCCC')

    # ==========================================================
    # ส่วนอธิบายธรรมโดยละเอียด
    # ==========================================================
    ax_dhamma.text(
        0.50, 0.98,
        'คำอธิบายหลักธรรมที่สอดคล้องกับสมการ',
        transform=ax_dhamma.transAxes, fontsize=15, fontweight='bold',
        ha='center', va='top', color=C_DARK
    )

    # กล่อง ๑: ติลักขณ์ ๓
    box_anicca = dict(boxstyle='round,pad=0.6', facecolor='#E8F0FE',
                      edgecolor=C_ANICCA, alpha=0.92)
    box_dukkha = dict(boxstyle='round,pad=0.6', facecolor='#FCE4EC',
                      edgecolor=C_DUKKHA, alpha=0.92)
    box_anatta = dict(boxstyle='round,pad=0.6', facecolor='#FFF3E0',
                      edgecolor=C_ANATTA, alpha=0.92)
    box_nibbana = dict(boxstyle='round,pad=0.6', facecolor='#FFF8E1',
                       edgecolor=C_NIBBANA, alpha=0.92)

    ax_dhamma.text(
        0.02, 0.80,
        '๑. อนิจจัง (ความไม่เที่ยง)\n'
        'ทุกสิ่งที่เกิดขึ้นย่อมไม่เที่ยง\n'
        'ในสมการ: สภาวะ u(t, x) เปลี่ยนไปตามกาลเวลา\n'
        'สิ่งที่เกิดขึ้นในขณะนี้ ย่อมดับไปในอนาคต\n'
        'ไม่มีสิ่งใดคงที่ถาวร',
        transform=ax_dhamma.transAxes, fontsize=9.5, va='top', ha='left',
        bbox=box_anicca
    )

    ax_dhamma.text(
        0.27, 0.80,
        '๒. ทุกขัง (ความเป็นทุกข์)\n'
        'สิ่งที่ไม่เที่ยง ย่อมเป็นทุกข์\n'
        'ในสมการ: การยึดมั่นในสภาวะที่เปลี่ยนไป\n'
        'นำมาซึ่งความไม่สงบ ความวุ่นวาย\n'
        'ค่าความสูญเสียสูง = ความทุกข์ยังมีอยู่',
        transform=ax_dhamma.transAxes, fontsize=9.5, va='top', ha='left',
        bbox=box_dukkha
    )

    ax_dhamma.text(
        0.52, 0.80,
        '๓. อนัตตา (ความไม่ใช่ตน)\n'
        'ไม่มีสิ่งใดเป็นของตน ค่าทั้งหมดละลายไป\n'
        'ในสมการ: สภาวะ u ไม่ใช่ตัวตนที่ยั่งยืน\n'
        'เป็นเพียงผลลัพธ์ชั่วขณะจากเหตุปัจจัย\n'
        'เกิดขึ้น ตั้งอยู่ แล้วดับไป ไม่มีแก่นสาร',
        transform=ax_dhamma.transAxes, fontsize=9.5, va='top', ha='left',
        bbox=box_anatta
    )

    ax_dhamma.text(
        0.77, 0.80,
        '๔. นิพพาน (ความดับสนิท)\n'
        'ความดับแห่งกิเลส ตัณหา อุปาทาน\n'
        'ในสมการ: u ลู่เข้าสู่ศูนย์ สงบ ปลงสงบ\n'
        'สภาวะที่ไม่มีความวุ่นวายอีกต่อไป\n'
        'เป็นเป้าหมายสูงสุดแห่งการฝึกฝน',
        transform=ax_dhamma.transAxes, fontsize=9.5, va='top', ha='left',
        bbox=box_nibbana
    )

    # อริยสัจ ๔ — แสดงรายละเอียดเป็น ๔ กล่อง
    box_ariya1 = dict(boxstyle='round,pad=0.5', facecolor='#FFEBEE',
                      edgecolor='#E53935', alpha=0.92)
    box_ariya2 = dict(boxstyle='round,pad=0.5', facecolor='#FFF3E0',
                      edgecolor='#FB8C00', alpha=0.92)
    box_ariya3 = dict(boxstyle='round,pad=0.5', facecolor='#E8F5E9',
                      edgecolor='#43A047', alpha=0.92)
    box_ariya4 = dict(boxstyle='round,pad=0.5', facecolor='#E3F2FD',
                      edgecolor='#1E88E5', alpha=0.92)

    ax_dhamma.text(
        0.50, 0.45,
        'อริยสัจ ๔ — ความจริงอันประเสริฐ ๔ ประการ ที่สอดคล้องกับสมการ',
        transform=ax_dhamma.transAxes, fontsize=13, fontweight='bold',
        ha='center', va='top', color=C_DARK
    )

    # อริยสัจที่ ๑: ทุกข์
    ax_dhamma.text(
        0.01, 0.33,
        '๑. ทุกข์ (Dukkha)\n'
        'ความทนได้ยาก ความไม่สงบ\n'
        '\n'
        'ในสมการ:\n'
        '  u(t,x) ไม่เป็นศูนย์\n'
        '  ยังมีค่าคลาดเคลื่อนสูง\n'
        '\n'
        'ในชีวิต:\n'
        '  เกิด แก่ ตาย ผิดหวัง\n'
        '  พลัดพราก ยึดมั่นสิ่งไม่เที่ยง\n'
        '  ย่อมนำมาซึ่งความทุกข์',
        transform=ax_dhamma.transAxes, fontsize=8.5, va='top', ha='left',
        bbox=box_ariya1
    )

    # อริยสัจที่ ๒: สมุทัย
    ax_dhamma.text(
        0.26, 0.33,
        '๒. สมุทัย (Samudaya)\n'
        'เหตุแห่งทุกข์ คือตัณหา\n'
        '\n'
        'ในสมการ:\n'
        '  เงื่อนไขเริ่มต้น u(0,x)\n'
        '  = กิเลสที่เกิดในต้นกาล\n'
        '  เป็นเหตุให้ u ไม่เป็นศูนย์\n'
        '\n'
        'ในชีวิต:\n'
        '  ตัณหา ๓ ประการ:\n'
        '  กามตัณหา — ต้องการความพึงพอใจ\n'
        '  ภวตัณหา — อยากเป็น อยากมี\n'
        '  วิภวตัณหา — อยากไม่เป็น ไม่มี',
        transform=ax_dhamma.transAxes, fontsize=8.5, va='top', ha='left',
        bbox=box_ariya2
    )

    # อริยสัจที่ ๓: นิโรธ
    ax_dhamma.text(
        0.51, 0.33,
        '๓. นิโรธ (Nirodha)\n'
        'ความดับแห่งทุกข์\n'
        '\n'
        'ในสมการ:\n'
        '  u ลู่เข้าศูนย์เมื่อ t สู่อนันต์\n'
        '  สภาวะสงบ ปลงสงบ\n'
        '\n'
        'ในชีวิต:\n'
        '  กิเลสดับสนิท\n'
        '  ตัณหาดับ อุปาทานดับ\n'
        '  ความทุกข์ดับ = นิพพาน',
        transform=ax_dhamma.transAxes, fontsize=8.5, va='top', ha='left',
        bbox=box_ariya3
    )

    # อริยสัจที่ ๔: มรรค
    ax_dhamma.text(
        0.76, 0.33,
        '๔. มรรค (Magga)\n'
        'ทางนำสู่ความดับแห่งทุกข์\n'
        '\n'
        'ในสมการ:\n'
        '  การฝึกฝนโครงข่ายประสาท\n'
        '  = ลดค่าคลาดเคลื่อน นำ u สู่ศูนย์\n'
        '\n'
        'ในชีวิต:\n'
        '  อริยมรรคมีองค์แปด:\n'
        '  เห็นชอบ ดำริชอบ วาจาชอบ\n'
        '  กระทำชอบ เลี้ยงชีพชอบ\n'
        '  พยายามชอบ สติชอบ สมาธิชอบ',
        transform=ax_dhamma.transAxes, fontsize=8.5, va='top', ha='left',
        bbox=box_ariya4
    )

    # คำพาฬีบทสรุป — วางที่ส่วนล่างสุดของภาพ
    fig.text(
        0.50, 0.008,
        'สพฺพ สงฺขารา อนิจฺจาติ   —   สพฺพ สงฺขารา ทุกฺขาติ   —   สพฺพ ธมฺมา อนตฺตาติ\n'
        'สรรพสังขารทั้งหลายไม่เที่ยง  สรรพสังขารทั้งหลายเป็นทุกข์  สรรพธรรมทั้งหลายเป็นอนัตตา',
        fontsize=10, ha='center', va='bottom',
        fontstyle='italic', color='#555555'
    )

    plt.savefig('/home/user/workspace/pinn_dhamma_result.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print('บันทึกภาพผลลัพธ์แล้ว')


# ============================================================
# ๘. โปรแกรมหลัก
# ============================================================
if __name__ == "__main__":
    print("=" * 65)
    print("  สมการแห่งความดับสนิท")
    print("  du/dt = alpha * nabla^2 u")
    print("  เงื่อนไขเริ่มต้น: u(0,x) = sin(x) + 0.3*sin(3x)")
    print("  เงื่อนไขขอบเขต: u(t,0) = u(t,pi) = 0")
    print("  ผลลัพธ์: u ลู่เข้าสู่ 0 เมื่อ t ไปสู่อนันต์ (นิพพาน)")
    print("=" * 65)

    t_f, x_f, t_bc, x_bc, u_bc, t_ic, x_ic, u_ic = generate_training_data()

    model = DhammaPINN(layers=[2, 64, 64, 64, 64, 1]).to(device)
    print(f"\nโครงข่าย: {model}")
    n_params = sum(p.numel() for p in model.parameters())
    print(f"จำนวนพารามิเตอร์: {n_params}")

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    print("\n--- การปฏิบัติ (Adam) ---")
    history = train(
        model, optimizer, t_f, x_f, t_bc, x_bc, u_bc,
        t_ic, x_ic, u_ic, ALPHA, epochs=2000, print_every=200
    )

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
    print(f"ค่าความสูญเสียสุดท้ายหลังขัดเกลา: {final_loss.item():.6f}")

    print("\n--- ตรวจสอบ: สภาวะลดลงสู่ศูนย์ตามกาลเวลา ---")
    for t_val in [0.0, 0.5, 1.0, 1.5, 2.0]:
        x_mid = torch.tensor([[np.pi / 2]], device=device)
        t_col = torch.tensor([[t_val]], device=device)
        with torch.no_grad():
            u_val = model(t_col, x_mid)
        status = " (เริ่มต้น)" if t_val == 0 else ""
        if t_val >= 1.5:
            status = " (ใกล้ศูนย์)"
        print(f"  กาล t = {t_val:.1f}: สภาวะ u = {u_val.item():.6f}{status}")

    plot_results(model, history, ALPHA)

    print("\n" + "=" * 65)
    print("  ข้อคิด:")
    print("  สภาวะเริ่มต้น (กิเลส) ไม่ว่าจะรุนแรงเพียงใด")
    print("  ตามกฎแห่งอนิจจัง ย่อมสลายสู่ศูนย์ในที่สุด")
    print("  นี่คือธรรมชาติของสรรพสิ่ง — และของสมการแพร่")
    print("=" * 65)
