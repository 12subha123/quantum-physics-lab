from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import numpy as np

from quantum.mechanics.quantum_barrier import QuantumBarrier
from quantum.utils.constants import ELECTRON_VOLT


ELECTRON_MASS = 9.1093837e-31

barrier = QuantumBarrier(
    mass=ELECTRON_MASS,
    barrier_height=1.0 * ELECTRON_VOLT,
    width=0.5e-9,
)

energies_ev = np.linspace(0.05, 2.0, 500)
transmission = np.array([
    barrier.transmission_probability(
        energy_ev * ELECTRON_VOLT
    )
    for energy_ev in energies_ev
])

plt.figure(figsize=(10, 6))

plt.plot(energies_ev, transmission)

plt.axvline(
    1.0,
    linestyle="--",
    label="Barrier height = 1 eV",
)

plt.xlabel("Particle energy (eV)")
plt.ylabel("Transmission probability T")
plt.title("Quantum Tunneling — Electron Through a 0.5 nm Barrier")
plt.ylim(0, 1.05)
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
