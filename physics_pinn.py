"""
Layer 2: PINN — แก้สมการฟิสิกส์
ติดตั้ง: pip install torch
"""
import torch
import torch.nn as nn
import numpy as np
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "physics_ai_output"
OUTPUT_DIR.mkdir(exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class PINN(nn.Module):
    def __init__(self, layers=[2, 32, 32, 32, 1]):
        super().__init__()
        modules = []
        for i in range(len(layers) - 1):
            modules.append(nn.Linear(layers[i], layers[i + 1]))
            if i < len(layers) - 2:
                modules.append(nn.Tanh())
        self.net = nn.Sequential(*modules)

    def forward(self, t, x):
        return self.net(torch.cat([t, x], dim=1))

def compute_heat_residual(model, t, x, alpha=0.1):
    t = t.clone().requires_grad_(True)
    x = x.clone().requires_grad_(True)
    u = model(t, x)
    u_t = torch.autograd.grad(u, t, torch.ones_like(u), create_graph=True)[0]
    u_x = torch.autograd.grad(u, x, torch.ones_like(u), create_graph=True)[0]
    u_xx = torch.autograd.grad(u_x, x, torch.ones_like(u_x), create_graph=True)[0]
    return u_t - alpha * u_xx

def train(model, epochs=1000):
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    history = []
    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()
        t_f = torch.rand(1000, 1, device=device)
        x_f = torch.rand(1000, 1, device=device)
        f = compute_heat_residual(model, t_f, x_f)
        loss = torch.mean(f ** 2)

        # IC: u(0,x) = sin(pi*x)
        x_ic = torch.rand(200, 1, device=device)
        t_ic = torch.zeros_like(x_ic)
        u_ic = torch.sin(np.pi * x_ic)
        loss += torch.mean((model(t_ic, x_ic) - u_ic) ** 2)

        loss.backward()
        optimizer.step()
        history.append(loss.item())
        if epoch % 200 == 0:
            print(f"  Epoch {epoch}: Loss = {loss.item():.6f}")
    return history

if __name__ == "__main__":
    print("=" * 60)
    print("  PINN — Heat Equation Solver")
    print("=" * 60)
    model = PINN().to(device)
    history = train(model, epochs=1000)
    print(f"\n[OK] Final Loss: {history[-1]:.6f}")
