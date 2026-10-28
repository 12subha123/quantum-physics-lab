import math

from quantum.field_theory.klein_gordon_simulation import simulate_klein_gordon
from quantum.field_theory.dirac import simulate_dirac


def relativistic_comparison(
    mass=1.0,
    momentum=2.0,
    amplitude=1.0,
    width=1.5,
    domain_length=20.0,
    duration=8.0,
    points=128,
    frames=80,
):
    if mass < 0:
        raise ValueError("Mass must be non-negative.")
    if amplitude <= 0:
        raise ValueError("Amplitude must be positive.")
    if width <= 0:
        raise ValueError("Width must be positive.")
    if domain_length <= 0:
        raise ValueError("Domain length must be positive.")
    if duration <= 0:
        raise ValueError("Duration must be positive.")
    if points < 64 or points > 256:
        raise ValueError("Points must be between 64 and 256.")
    if frames < 20 or frames > 120:
        raise ValueError("Frames must be between 20 and 120.")

    energy = math.sqrt(momentum**2 + mass**2)
    group_velocity = momentum / energy if energy != 0 else 0.0

    kg = simulate_klein_gordon(
        mass=mass,
        amplitude=amplitude,
        width=width,
        wavenumber=momentum,
        domain_length=domain_length,
        duration=duration,
        points=points,
        frames=frames,
    )

    dirac = simulate_dirac(
        mass=mass,
        amplitude=amplitude,
        width=width,
        momentum=momentum,
        domain_length=domain_length,
        duration=duration,
        points=points,
        frames=frames,
    )

    return {
        "success": True,
        "model": "1+1D relativistic free-field comparison",
        "units": "Natural units: hbar = c = 1",
        "shared_parameters": {
            "mass": mass,
            "momentum": momentum,
            "amplitude": amplitude,
            "width": width,
            "domain_length": domain_length,
            "duration": duration,
            "points": points,
            "frames": frames,
        },
        "relativistic_kinematics": {
            "energy": energy,
            "rest_energy": mass,
            "group_velocity": group_velocity,
            "dispersion_relation": "E = sqrt(p^2 + m^2)",
            "group_velocity_relation": "v_g = p / E",
        },
        "klein_gordon": kg,
        "dirac": dirac,
        "comparison_notes": [
            "Klein-Gordon describes a relativistic scalar field.",
            "Dirac describes a relativistic spin-1/2 fermion field.",
            "The Klein-Gordon simulation displays scalar-field amplitude.",
            "The Dirac simulation displays probability density and spinor components.",
            "These observables are not directly identical and should not be compared as the same physical quantity.",
            "Both simulations use the same mass, momentum, spatial scale, duration, and numerical resolution.",
            "The numerical boundary conditions differ between the educational solvers, so this is a conceptual relativistic comparison rather than a precision matched-boundary experiment.",
            "Both free relativistic models have the same dispersion relation E = sqrt(p^2 + m^2).",
        ],
    }
