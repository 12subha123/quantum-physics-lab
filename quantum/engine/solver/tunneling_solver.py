import math
from dataclasses import dataclass


HBAR = 1.054571817e-34
ELECTRON_MASS = 9.1093837015e-31
EV_TO_JOULE = 1.602176634e-19


@dataclass
class TunnelingResult:
    particle_energy_ev: float
    barrier_height_ev: float
    barrier_width_nm: float
    particle_mass_kg: float
    kappa_per_meter: float
    transmission_probability: float
    reflection_probability: float
    transmission_percentage: float
    reflection_percentage: float


def calculate_tunneling_probability(
    particle_energy_ev: float,
    barrier_height_ev: float,
    barrier_width_nm: float,
    particle_mass_kg: float = ELECTRON_MASS,
) -> TunnelingResult:

    if particle_energy_ev < 0:
        raise ValueError("Particle energy cannot be negative.")

    if barrier_height_ev <= particle_energy_ev:
        raise ValueError(
            "Barrier height must be greater than particle energy "
            "for this tunneling model."
        )

    if barrier_width_nm <= 0:
        raise ValueError("Barrier width must be positive.")

    if particle_mass_kg <= 0:
        raise ValueError("Particle mass must be positive.")

    energy_j = particle_energy_ev * EV_TO_JOULE
    barrier_j = barrier_height_ev * EV_TO_JOULE
    width_m = barrier_width_nm * 1e-9

    kappa = math.sqrt(
        2 * particle_mass_kg * (barrier_j - energy_j)
    ) / HBAR

    transmission = math.exp(-2 * kappa * width_m)

    transmission = min(max(transmission, 0.0), 1.0)

    reflection = 1.0 - transmission

    return TunnelingResult(
        particle_energy_ev=particle_energy_ev,
        barrier_height_ev=barrier_height_ev,
        barrier_width_nm=barrier_width_nm,
        particle_mass_kg=particle_mass_kg,
        kappa_per_meter=kappa,
        transmission_probability=transmission,
        reflection_probability=reflection,
        transmission_percentage=transmission * 100,
        reflection_percentage=reflection * 100,
    )


if __name__ == "__main__":
    result = calculate_tunneling_probability(
        particle_energy_ev=2.0,
        barrier_height_ev=5.0,
        barrier_width_nm=0.5,
    )

    print("Quantum Tunneling Solver")
    print("========================")
    print()

    print(f"Particle energy: {result.particle_energy_ev} eV")
    print(f"Barrier height: {result.barrier_height_ev} eV")
    print(f"Barrier width: {result.barrier_width_nm} nm")
    print(f"Particle mass: {result.particle_mass_kg:.6e} kg")
    print(f"Kappa: {result.kappa_per_meter:.6e} 1/m")

    print(
        "Transmission probability: "
        f"{result.transmission_probability:.8e}"
    )

    print(
        "Reflection probability: "
        f"{result.reflection_probability:.8e}"
    )

    print(
        "Transmission percentage: "
        f"{result.transmission_percentage:.8e}%"
    )

    print(
        "Reflection percentage: "
        f"{result.reflection_percentage:.8e}%"
    )
