from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

from quantum.mechanics.infinite_well import InfinitePotentialWell


well = InfinitePotentialWell(length=1.0, mass=1.0)

x = np.linspace(0, 1, 1000)

print("Quantum Infinite Well")
print("--------------------")
print("Length:", well.length)
print("Mass:", well.mass)

for n in range(1, 4):
    print(f"Energy E_{n}:", well.energy(n))

psi = well.wavefunction(1, x)
probability = well.probability_density(1, x)

print("Wavefunction samples:", len(psi))
print(
    "Probability density integral:",
    np.trapezoid(probability, x),
)
