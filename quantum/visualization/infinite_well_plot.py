from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import numpy as np

from quantum.mechanics.infinite_well import InfinitePotentialWell


well = InfinitePotentialWell(length=1.0, mass=1.0)

x = np.linspace(0, well.length, 1000)

psi = well.wavefunction(1, x)
probability = well.probability_density(1, x)

fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

axes[0].plot(x, psi)
axes[0].set_ylabel("Wavefunction ψ(x)")
axes[0].set_title("Quantum Particle in a 1D Infinite Potential Well")
axes[0].grid(True)

axes[1].plot(x, probability)
axes[1].set_xlabel("Position x")
axes[1].set_ylabel("|ψ(x)|²")
axes[1].set_title("Probability Density")
axes[1].grid(True)

plt.tight_layout()
plt.show()
