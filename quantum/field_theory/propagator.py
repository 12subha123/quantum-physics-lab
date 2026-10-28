import cmath
import math


def _validate(mass, energy, momentum, epsilon):
    if mass < 0:
        raise ValueError("Mass must be non-negative.")
    if epsilon <= 0:
        raise ValueError("Epsilon must be positive.")


def scalar_feynman_propagator(
    mass=1.0,
    energy=2.0,
    momentum=1.0,
    epsilon=1e-3,
):
    _validate(mass, energy, momentum, epsilon)

    p_squared = energy**2 - momentum**2
    denominator = complex(
        p_squared - mass**2,
        epsilon,
    )

    propagator = 1j / denominator

    return {
        "success": True,
        "model": "Free scalar Feynman propagator",
        "units": "Natural units: hbar = c = 1",
        "parameters": {
            "mass": mass,
            "energy": energy,
            "momentum": momentum,
            "epsilon": epsilon,
        },
        "kinematics": {
            "p_squared": p_squared,
            "mass_squared": mass**2,
            "on_shell_condition": (
                abs(p_squared - mass**2) < 1e-10
            ),
        },
        "propagator": {
            "real": propagator.real,
            "imaginary": propagator.imag,
            "magnitude": abs(propagator),
            "phase": cmath.phase(propagator),
            "complex": {
                "real": propagator.real,
                "imaginary": propagator.imag,
            },
        },
        "formula": "D_F(p) = i / (p^2 - m^2 + i epsilon)",
        "interpretation": [
            "The propagator describes the free scalar-field propagation amplitude in momentum space.",
            "The denominator becomes small near the mass shell p^2 = m^2.",
            "The small positive epsilon implements the Feynman prescription.",
            "This is the free-field propagator used as a building block for perturbative QFT.",
        ],
    }


def propagator_energy_scan(
    mass=1.0,
    momentum=1.0,
    epsilon=1e-3,
    points=101,
    energy_min=0.0,
    energy_max=4.0,
):
    if points < 2 or points > 1000:
        raise ValueError("Points must be between 2 and 1000.")
    if energy_max <= energy_min:
        raise ValueError("Energy maximum must exceed energy minimum.")

    values = []

    for i in range(points):
        energy = energy_min + (
            (energy_max - energy_min) * i / (points - 1)
        )

        result = scalar_feynman_propagator(
            mass=mass,
            energy=energy,
            momentum=momentum,
            epsilon=epsilon,
        )

        values.append(
            {
                "energy": energy,
                "real": result["propagator"]["real"],
                "imaginary": result["propagator"]["imaginary"],
                "magnitude": result["propagator"]["magnitude"],
            }
        )

    return {
        "success": True,
        "model": "Free scalar Feynman propagator energy scan",
        "units": "Natural units: hbar = c = 1",
        "parameters": {
            "mass": mass,
            "momentum": momentum,
            "epsilon": epsilon,
            "points": points,
            "energy_min": energy_min,
            "energy_max": energy_max,
        },
        "data": values,
        "interpretation": (
            "The propagator magnitude is enhanced near the relativistic "
            "mass-shell energy E = sqrt(p^2 + m^2)."
        ),
    }
