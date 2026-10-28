from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import numpy as np

from quantum.mechanics.infinite_well import InfinitePotentialWell


well = InfinitePotentialWell(length=1.0, mass=1.0)

x = np.linspace(0, well.length, 1000)

fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

for n in range(1, 6):
    psi = well.wavefunction(n, x)
    probability = well.probability_density(n, x)

    axes[0].plot(x, psi, label=f"n={n}")
    axes[1].plot(x, probability, label=f"n={n}")

axes[0].set_title("Quantum Infinite Well — Wavefunctions")
axes[0].set_ylabel("ψ(x)")
axes[0].grid(True)
axes[0].legend()

axes[1].set_title("Probability Densities")
axes[1].set_xlabel("Position x")
axes[1].set_ylabel("|ψ(x)|²")
axes[1].grid(True)
axes[1].legend()

plt.tight_layout()
plt.show()
