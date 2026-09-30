"""
Physics-Informed Neural Network (PINN) ด้วย PyTorch
แก้สมการ Burgers' 1D:
    u_t + u * u_x - (nu / pi) * u_xx = 0
    เงื่อนไข: u(0, x) = -sin(pi*x), u(t, -1) = u(t, 1) = 0

สมการนี้เป็น benchmark มาตรฐานของ PINNs (Raissi et al., 2019)
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# ============================================================
# 1. ตั้งค่า
# ============================================================
torch.manual_seed(42)
np.random.seed(42)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# พารามิเตอร์ของสมการ Burgers'
nu = 0.01 / np.pi  # ความหนืด (viscosity)

# ============================================================
# 2. นิยาม Neural Network
# ============================================================
class PINN(nn.Module):
    """
    Multilayer Perceptron (MLP) ที่ประมาณค่า u(t, x)
    input:  (t, x)  ->  output: u(t, x)
    """
    def __init__(self, layers=[2, 64, 64, 64, 64, 1]):
        super().__init__()
        modules = []
        for i in range(len(layers) - 1):
            modules.append(nn.Linear(layers[i], layers[i + 1]))
            if i < len(layers) - 2:
                modules.append(nn.Tanh())  # Tanh เหมาะกับ PINN เพราะ smooth
        self.net = nn.Sequential(*modules)

        # Xavier initialization
        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, t, x):
        # รวม t และ x เป็น input เดียว
        tx = torch.cat([t, x], dim=1)
        return self.net(tx)


# ============================================================
# 3. สร้างข้อมูล Collocation, Boundary, และ Initial points
# ============================================================
def generate_training_data(N_f=10000, N_bc=400, N_ic=400):
    """
    N_f  : จำนวน collocation points (สุ่มในโดเมน)
    N_bc : จำนวน boundary points (ที่ขอบเขต x = ±1)
    N_ic : จำนวน initial condition points (ที่ t = 0)
    """
    # --- Collocation points (สุ่มในโดเมน t ∈ [0,1], x ∈ [-1,1]) ---
    t_f = torch.rand(N_f, 1, device=device)        # t ∈ [0, 1)
    x_f = torch.rand(N_f, 1, device=device) * 2 - 1  # x ∈ [-1, 1)

    # --- Boundary condition points (x = ±1) ---
    t_bc = torch.rand(N_bc, 1, device=device)       # t ∈ [0, 1)
    x_bc = torch.where(
        torch.rand(N_bc, 1, device=device) > 0.5,
        torch.ones_like(torch.rand(N_bc, 1, device=device)),
        -torch.ones_like(torch.rand(N_bc, 1, device=device))
    )
    u_bc = torch.zeros(N_bc, 1, device=device)       # u(t, ±1) = 0

    # --- Initial condition points (t = 0) ---
    x_ic = torch.rand(N_ic, 1, device=device) * 2 - 1  # x ∈ [-1, 1)
    t_ic = torch.zeros(N_ic, 1, device=device)          # t = 0
    u_ic = -torch.sin(np.pi * x_ic)                     # u(0, x) = -sin(πx)

    return t_f, x_f, t_bc, x_bc, u_bc, t_ic, x_ic, u_ic


# ============================================================
# 4. ฟังก์ชันคำนวณ PDE Residual (หัวใจของ PINN)
# ============================================================
def compute_pde_residual(model, t, x, nu):
    """
    คำนวณ residual ของสมการ Burgers':
        f = u_t + u * u_x - (nu/pi) * u_xx
    โดยใช้ Automatic Differentiation (AD) หาอนุพันธ์
    """
    # ต้องเปิด requires_grad สำหรับ input
    t = t.clone().requires_grad_(True)
    x = x.clone().requires_grad_(True)

    # Forward pass
    u = model(t, x)

    # --- อนุพันธ์อันดับ 1 ---
    # u_t = ∂u/∂t
    u_t = torch.autograd.grad(
        outputs=u, inputs=t,
        grad_outputs=torch.ones_like(u),
        create_graph=True  # ต้องเป็น True เพื่อหาอนุพันธ์อันดับ 2 ต่อไป
    )[0]

    # u_x = ∂u/∂x
    u_x = torch.autograd.grad(
        outputs=u, inputs=x,
        grad_outputs=torch.ones_like(u),
        create_graph=True
    )[0]

    # --- อนุพันธ์อันดับ 2 ---
    # u_xx = ∂²u/∂x²
    u_xx = torch.autograd.grad(
        outputs=u_x, inputs=x,
        grad_outputs=torch.ones_like(u_x),
        create_graph=True
    )[0]

    # Residual ของสมการ Burgers'
    f = u_t + u * u_x - nu * u_xx

    return f


# ============================================================
# 5. Loss Function
# ============================================================
def compute_loss(model, t_f, x_f, t_bc, x_bc, u_bc,
                 t_ic, x_ic, u_ic, nu):
    """
    Loss รวม = Loss_physics + Loss_BC + Loss_IC

    L_physics: residual ของ PDE ที่ collocation points (unsupervised)
    L_BC:      ความคลาดเคลื่อนที่เงื่อนไขขอบเขต
    L_IC:      ความคลาดเคลื่อนที่เงื่อนไขเริ่มต้น
    """
    # --- Physics Loss (PDE residual) ---
    f = compute_pde_residual(model, t_f, x_f, nu)
    loss_physics = torch.mean(f ** 2)

    # --- Boundary Condition Loss ---
    u_pred_bc = model(t_bc, x_bc)
    loss_bc = torch.mean((u_pred_bc - u_bc) ** 2)

    # --- Initial Condition Loss ---
    u_pred_ic = model(t_ic, x_ic)
    loss_ic = torch.mean((u_pred_ic - u_ic) ** 2)

    # --- Loss รวม ---
    loss = loss_physics + loss_bc + loss_ic

    return loss, loss_physics, loss_bc, loss_ic


# ============================================================
# 6. Training Loop
# ============================================================
def train(model, optimizer, t_f, x_f, t_bc, x_bc, u_bc,
          t_ic, x_ic, u_ic, nu, epochs=5000, print_every=500):
    model.train()
    history = []

    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()

        loss, loss_p, loss_bc, loss_ic = compute_loss(
            model, t_f, x_f, t_bc, x_bc, u_bc,
            t_ic, x_ic, u_ic, nu
        )

        loss.backward()
        optimizer.step()

        history.append(loss.item())

        if epoch % print_every == 0 or epoch == 1:
            print(f"Epoch {epoch:5d}/{epochs} | "
                  f"Total: {loss.item():.6f} | "
                  f"Physics: {loss_p.item():.6f} | "
                  f"BC: {loss_bc.item():.6f} | "
                  f"IC: {loss_ic.item():.6f}")

    return history


# ============================================================
# 7. สร้างกราฟผลลัพธ์
# ============================================================
def plot_results(model, history, nu):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # --- (a) Training Loss ---
    axes[0].plot(history, linewidth=0.5, color='steelblue')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('(a) Training Loss')
    axes[0].set_yscale('log')

    # --- (b) ผลลัพธ์ u(t, x) เป็น heatmap ---
    t_test = torch.linspace(0, 1, 100, device=device).view(-1, 1)
    x_test = torch.linspace(-1, 1, 100, device=device).view(-1, 1)
    T, X = torch.meshgrid(t_test.squeeze(), x_test.squeeze(), indexing='ij')

    t_flat = T.reshape(-1, 1)
    x_flat = X.reshape(-1, 1)
    with torch.no_grad():
        u_pred = model(t_flat, x_flat)
    U = u_pred.reshape(100, 100).cpu().numpy()

    im = axes[1].imshow(
        U, extent=[-1, 1, 1, 0],
        aspect='auto', cmap='jet', vmin=-1, vmax=1
    )
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('t')
    axes[1].set_title('(b) PINN Solution u(t, x)')
    plt.colorbar(im, ax=axes[1], label='u(t,x)')

    # --- (c) เปรียบเทียบ u(t, x) ที่ t = 0, 0.25, 0.5, 0.75 ---
    t_snapshots = [0.0, 0.25, 0.5, 0.75]
    colors = ['black', 'red', 'green', 'blue']
    x_plot = torch.linspace(-1, 1, 200, device=device).view(-1, 1)

    for t_val, color in zip(t_snapshots, colors):
        t_col = torch.full_like(x_plot, t_val)
        with torch.no_grad():
            u_plot = model(t_col, x_plot)
        axes[2].plot(
            x_plot.cpu().numpy(), u_plot.cpu().numpy(),
            color=color, linewidth=2, label=f't = {t_val}'
        )

    axes[2].set_xlabel('x')
    axes[2].set_ylabel('u(t, x)')
    axes[2].set_title('(c) Snapshots at Different Times')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/user/workspace/pinn_burgers_result.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved plot to pinn_burgers_result.png")


# ============================================================
# 8. Main
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  PINN: Solving 1D Burgers' Equation")
    print("  u_t + u * u_x - (nu/pi) * u_xx = 0")
    print("  IC: u(0,x) = -sin(pi*x), BC: u(t,±1) = 0")
    print("=" * 60)

    # สร้างข้อมูล
    t_f, x_f, t_bc, x_bc, u_bc, t_ic, x_ic, u_ic = generate_training_data(N_f=5000, N_bc=200, N_ic=200)

    # สร้างโมเดล
    model = PINN(layers=[2, 64, 64, 64, 64, 1]).to(device)
    print(f"\nNetwork architecture:\n{model}")

    # นับจำนวนพารามิเตอร์
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {n_params}")

    # Optimizer: เริ่มด้วย Adam
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    # Training
    print("\n--- Training (Adam) ---")
    history = train(
        model, optimizer, t_f, x_f, t_bc, x_bc, u_bc,
        t_ic, x_ic, u_ic, nu, epochs=2000, print_every=200
    )

    # ปรับ fine-tune ด้วย L-BFGS
    print("\n--- Fine-tuning (L-BFGS) ---")
    optimizer_lbfgs = torch.optim.LBFGS(
        model.parameters(),
        lr=1.0,
        max_iter=200,
        history_size=50,
        tolerance_grad=1e-6,
        tolerance_change=1e-9,
        line_search_fn='strong_wolfe'
    )

    def lbfgs_closure():
        optimizer_lbfgs.zero_grad()
        loss, _, _, _ = compute_loss(
            model, t_f, x_f, t_bc, x_bc, u_bc,
            t_ic, x_ic, u_ic, nu
        )
        loss.backward()
        return loss

    optimizer_lbfgs.step(lbfgs_closure)
    final_loss, _, _, _ = compute_loss(
        model, t_f, x_f, t_bc, x_bc, u_bc,
        t_ic, x_ic, u_ic, nu
    )
    print(f"Final loss after L-BFGS: {final_loss.item():.6f}")

    # สร้างกราฟ
    plot_results(model, history, nu)

    print("\nDone!")
