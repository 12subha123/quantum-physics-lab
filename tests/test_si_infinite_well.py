from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from quantum.mechanics.infinite_well import InfinitePotentialWell


ELECTRON_MASS = 9.1093837e-31
ONE_NANOMETER = 1e-9

well = InfinitePotentialWell(
    length=ONE_NANOMETER,
    mass=ELECTRON_MASS,
    use_si=True,
)

print("Quantum Infinite Well — SI Mode")
print("--------------------------------")
print("Particle: electron")
print("Well width:", well.length, "m")
print("Mass:", well.mass, "kg")
print()

for n in range(1, 6):
    energy_j = well.energy(n)
    energy_ev = well.energy_ev(n)

    print(
        f"n={n}: "
        f"{energy_j:.6e} J  =  "
        f"{energy_ev:.6f} eV"
    )
