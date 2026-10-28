from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from quantum.mechanics.quantum_barrier import QuantumBarrier
from quantum.utils.constants import ELECTRON_VOLT


ELECTRON_MASS = 9.1093837e-31

barrier = QuantumBarrier(
    mass=ELECTRON_MASS,
    barrier_height=1.0 * ELECTRON_VOLT,
    width=0.5e-9,
)

print("Quantum Tunneling Test")
print("----------------------")
print("Particle: electron")
print("Barrier height: 1.0 eV")
print("Barrier width: 0.5 nm")
print()

for energy_ev in [0.1, 0.2, 0.4, 0.6, 0.8]:
    energy_j = energy_ev * ELECTRON_VOLT

    transmission = barrier.transmission_probability(energy_j)

    print(
        f"E = {energy_ev:.1f} eV"
        f" -> T = {transmission:.6e}"
        f" ({transmission * 100:.6f}%)"
    )
