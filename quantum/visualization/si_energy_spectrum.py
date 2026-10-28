from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import numpy as np

from quantum.mechanics.infinite_well import InfinitePotentialWell


ELECTRON_MASS = 9.1093837e-31
ONE_NANOMETER = 1e-9

well = InfinitePotentialWell(
    length=ONE_NANOMETER,
    mass=ELECTRON_MASS,
    use_si=True,
)

levels = np.arange(1, 11)
energies_ev = np.array([well.energy_ev(n) for n in levels])

plt.figure(figsize=(9, 6))

plt.plot(levels, energies_ev, marker="o")

plt.xlabel("Quantum number n")
plt.ylabel("Energy Eₙ (eV)")
plt.title("Electron Energy Spectrum — 1 nm Infinite Potential Well")
plt.xticks(levels)
plt.grid(True)

plt.tight_layout()
plt.show()
