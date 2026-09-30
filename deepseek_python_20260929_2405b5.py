#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PINN Burgers' Equation (PyTorch)
u_t + u * u_x - (nu/pi) * u_xx = 0
IC: u(0, x) = -sin(pi*x), BC: u(t, -1) = u(t, 1) = 0
"""

import os
from pathlib import Path

import torch
import torch.nn as nn
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ============================================================
# ตั้งค่าโฟลเดอร์บันทึก — ใช้ได้ทุก OS
# ============================================================
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
print(f"📁 บันทึกที่: {OUTPUT_DIR}")

# ตั้งฟอนต์
for f in ["Leelawadee UI", "Tahoma", "Sarabun", "Noto Sans Thai"]:
    if f in {x.name for x in fm.fontManager.ttflist}:
        plt.rcParams['font.family'] = f
        break
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# ตั้งค่า
# ============================================================
torch.manual_seed(42)
np.random.seed(42)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

nu = 0.01 / np.pi

# ============================================================
# Neural Network
# ============================================================
class PINN(nn.Module):
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
        return self.net(torch.cat([t, x], dim=1))

# ============================================================
# สร้างข้อมูล
# ============================================================
def generate_training_data(N_f=10000, N_bc=400, N_ic=400):
    t_f = torch.rand(N_f, 1, device=device)
    x_f = torch.rand(N_f, 1, device=device) * 2 - 1

    t_bc = torch.rand(N_bc, 1, device=device)
    x_bc = torch.where(
        torch.rand(N_bc, 1, device=device) > 0.5,
        torch.ones_like(torch.rand(N_bc, 1, device=device)),
        -torch.ones_like(torch.rand(N_bc, 1, device=device))
    )
    u_bc = torch.zeros(N_bc, 1, device=device)

    x_ic = torch.rand(N_ic, 1, device=device) * 2 - 1
    t_ic = torch.zeros(N_ic, 1, device=device)
    u_ic = -torch.sin(np.pi * x_ic)

    return t_f, x_f, t_bc, x_bc, u_bc, t_ic, x_ic, u_ic

# ============================================================
# PDE Residual
# ============================================================
def compute_pde_residual(model, t, x, nu):
    t = t.clone().requires_grad_(True)
    x = x.clone().requires_grad_(True)
    u = model(t, x)

    u_t = torch.autograd.grad(u, t, torch.ones_like(u), create_graph=True)[0]
    u_x = torch.autograd.grad(u, x, torch.ones_like(u), create_graph=True)[0]
    u_xx = torch.autograd.grad(u_x, x, torch.ones_like(u_x), create_graph=True)[0]

    return u_t + u * u_x - nu * u_xx

# ============================================================
# Loss
# ============================================================
def compute_loss(model, t_f, x_f, t_bc, x_bc, u_bc,
                 t_ic, x_ic, u_ic, nu):
    f = compute_pde_residual(model, t_f, x_f, nu)
    loss_physics = torch.mean(f ** 2)

    u_pred_bc = model(t_bc, x_bc)
    loss_bc = torch.mean((u_pred_bc - u_bc) ** 2)

    u_pred_ic = model(t_ic, x_ic)
    loss_ic = torch.mean((u_pred_ic - u_ic) ** 2)

    return loss_physics + loss_bc + loss_ic, loss_physics, loss_bc, loss_ic

# ============================================================
# Training
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
# Plot
# ============================================================
def plot_results(model, history, nu):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # (a) Loss
    axes[0].plot(history, linewidth=0.5, color='steelblue')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('(a) Training Loss')
    axes[0].set_yscale('log')
    axes[0].grid(alpha=0.3)

    # (b) Heatmap
    t_test = torch.linspace(0, 1, 100, device=device).view(-1, 1)
    x_test = torch.linspace(-1, 1, 100, device=device).view(-1, 1)
    T, X = torch.meshgrid(t_test.squeeze(), x_test.squeeze(), indexing='ij')
    t_flat = T.reshape(-1, 1)
    x_flat = X.reshape(-1, 1)
    with torch.no_grad():
        U = model(t_flat, x_flat).reshape(100, 100).cpu().numpy()

    im = axes[1].imshow(U, extent=[-1, 1, 1, 0],
                        aspect='auto', cmap='jet', vmin=-1, vmax=1)
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('t')
    axes[1].set_title('(b) PINN Solution u(t, x)')
    plt.colorbar(im, ax=axes[1], label='u(t,x)')

    # (c) Snapshots
    for t_val, color in zip([0.0, 0.25, 0.5, 0.75],
                             ['black', 'red', 'green', 'blue']):
        x_plot = torch.linspace(-1, 1, 200, device=device).view(-1, 1)
        t_col = torch.full_like(x_plot, t_val)
        with torch.no_grad():
            u_plot = model(t_col, x_plot)
        axes[2].plot(x_plot.cpu().numpy(), u_plot.cpu().numpy(),
                     color=color, linewidth=2, label=f't = {t_val}')

    axes[2].set_xlabel('x')
    axes[2].set_ylabel('u(t, x)')
    axes[2].set_title('(c) Snapshots at Different Times')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    out_path = OUTPUT_DIR / 'pinn_burgers_result.png'
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✓ บันทึกภาพ: {out_path}")

# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  PINN: Solving 1D Burgers' Equation")
    print("=" * 60)

    t_f, x_f, t_bc, x_bc, u_bc, t_ic, x_ic, u_ic = generate_training_data(
        N_f=5000, N_bc=200, N_ic=200
    )

    model = PINN(layers=[2, 64, 64, 64, 64, 1]).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {n_params}")

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    print("\n--- Training (Adam) ---")
    history = train(model, optimizer, t_f, x_f, t_bc, x_bc, u_bc,
                    t_ic, x_ic, u_ic, nu, epochs=2000, print_every=200)

    print("\n--- Fine-tuning (L-BFGS) ---")
    optimizer_lbfgs = torch.optim.LBFGS(
        model.parameters(), lr=1.0, max_iter=200,
        history_size=50, tolerance_grad=1e-6,
        tolerance_change=1e-9, line_search_fn='strong_wolfe'
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
    print(f"Final loss: {final_loss.item():.6f}")

    plot_results(model, history, nu)

    print(f"\n✅ เสร็จสิ้น! ไฟล์อยู่ที่: {OUTPUT_DIR}")