import math
from dataclasses import dataclass

import numpy as np


@dataclass
class HarmonicOscillatorResult:
    hbar: float
    mass: float
    omega: float
    x_min: float
    x_max: float
    points: int
    num_states: int
    position: list
    potential: list
    energy_levels: list
    wavefunctions: list
    probability_densities: list


def energy(n: int, hbar: float, omega: float) -> float:
    return hbar * omega * (n + 0.5)


def hermite_polynomial(n: int, x: np.ndarray) -> np.ndarray:
    if n < 0:
        raise ValueError("Quantum number n cannot be negative.")

    if n == 0:
        return np.ones_like(x)

    if n == 1:
        return 2 * x

    h0 = np.ones_like(x)
    h1 = 2 * x

    for k in range(2, n + 1):
        h2 = 2 * x * h1 - 2 * (k - 1) * h0
        h0, h1 = h1, h2

    return h1


def wavefunction(
    n: int,
    x: np.ndarray,
    hbar: float,
    mass: float,
    omega: float,
) -> np.ndarray:

    if mass <= 0:
        raise ValueError("Mass must be positive.")

    if omega <= 0:
        raise ValueError("Angular frequency must be positive.")

    alpha = math.sqrt(mass * omega / hbar)

    xi = alpha * x

    prefactor = (
        (mass * omega / (math.pi * hbar)) ** 0.25
        / math.sqrt(2**n * math.factorial(n))
    )

    gaussian = np.exp(-(xi**2) / 2)

    return (
        prefactor
        * hermite_polynomial(n, xi)
        * gaussian
    )


def calculate_harmonic_oscillator(
    hbar: float = 1.0,
    mass: float = 1.0,
    omega: float = 1.0,
    x_min: float = -5.0,
    x_max: float = 5.0,
    points: int = 1000,
    num_states: int = 5,
) -> HarmonicOscillatorResult:

    if hbar <= 0:
        raise ValueError("hbar must be positive.")

    if mass <= 0:
        raise ValueError("Mass must be positive.")

    if omega <= 0:
        raise ValueError("Angular frequency must be positive.")

    if x_max <= x_min:
        raise ValueError("x_max must be greater than x_min.")

    if points < 100:
        raise ValueError("At least 100 spatial points are required.")

    if num_states < 1:
        raise ValueError("At least one quantum state is required.")

    x = np.linspace(x_min, x_max, points)

    potential = 0.5 * mass * omega**2 * x**2

    energy_levels = []
    wavefunctions = []
    probability_densities = []

    for n in range(num_states):
        energy_value = energy(
            n=n,
            hbar=hbar,
            omega=omega,
        )

        psi = wavefunction(
            n=n,
            x=x,
            hbar=hbar,
            mass=mass,
            omega=omega,
        )

        probability = psi**2

        energy_levels.append(float(energy_value))
        wavefunctions.append(psi.tolist())
        probability_densities.append(probability.tolist())

    return HarmonicOscillatorResult(
        hbar=hbar,
        mass=mass,
        omega=omega,
        x_min=x_min,
        x_max=x_max,
        points=points,
        num_states=num_states,
        position=x.tolist(),
        potential=potential.tolist(),
        energy_levels=energy_levels,
        wavefunctions=wavefunctions,
        probability_densities=probability_densities,
    )


if __name__ == "__main__":
    result = calculate_harmonic_oscillator()

    print("Quantum Harmonic Oscillator")
    print("===========================")
    print()

    print("Parameters:")
    print(f"  hbar: {result.hbar}")
    print(f"  mass: {result.mass}")
    print(f"  omega: {result.omega}")
    print(f"  states: {result.num_states}")
    print()

    print("Energy levels:")

    for n, energy_value in enumerate(result.energy_levels):
        print(f"  n={n}: E={energy_value}")

    print()
    print(f"Spatial points: {result.points}")
    print(f"Position range: {result.x_min} to {result.x_max}")
