from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import numpy as np

from quantum.mechanics.infinite_well import InfinitePotentialWell


well = InfinitePotentialWell(length=1.0, mass=1.0)

levels = np.arange(1, 11)
energies = np.array([well.energy(n) for n in levels])

plt.figure(figsize=(9, 6))

plt.plot(levels, energies, marker="o")

plt.xlabel("Quantum number n")
plt.ylabel("Energy Eₙ")
plt.title("Quantized Energy Levels — 1D Infinite Potential Well")
plt.xticks(levels)
plt.grid(True)

plt.tight_layout()
plt.show()
