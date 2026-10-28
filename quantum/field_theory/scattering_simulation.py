import math


def _validate(mass, sqrt_s, lam, angular_points):
    if mass < 0:
        raise ValueError("Mass must be non-negative.")

    if sqrt_s <= 0:
        raise ValueError("Center-of-mass energy must be positive.")

    if sqrt_s < 2.0 * mass:
        raise ValueError(
            "Center-of-mass energy is below the two-particle threshold."
        )

    if lam < 0:
        raise ValueError("Coupling lambda must be non-negative.")

    if angular_points < 8 or angular_points > 720:
        raise ValueError(
            "Angular points must be between 8 and 720."
        )


def simulate_phi4_scattering(
    mass=1.0,
    sqrt_s=5.0,
    lam=1.0,
    angular_points=73,
):
    _validate(
        mass=mass,
        sqrt_s=sqrt_s,
        lam=lam,
        angular_points=angular_points,
    )

    s = sqrt_s ** 2

    # Elastic two-body center-of-mass momentum.
    momentum_squared = max(
        0.0,
        s / 4.0 - mass ** 2,
    )

    momentum = math.sqrt(momentum_squared)

    # Tree-level phi^4 contact amplitude:
    #
    # M = -i lambda
    #
    # Therefore |M|^2 = lambda^2.
    amplitude_magnitude_squared = lam ** 2

    # For identical scalar final-state particles:
    #
    # d sigma / d Omega =
    # |M|^2 / (128 pi^2 s)
    #
    # The factor 1/2 accounts for identical final particles.
    differential_cross_section = (
        amplitude_magnitude_squared
        / (128.0 * math.pi ** 2 * s)
    )

    # Integrating over the full solid angle:
    total_cross_section = (
        amplitude_magnitude_squared
        / (32.0 * math.pi * s)
    )

    angles = []
    for index in range(angular_points):
        theta = math.pi * index / (angular_points - 1)

        angles.append(
            {
                "theta_radians": theta,
                "theta_degrees": math.degrees(theta),
                "differential_cross_section": differential_cross_section,
            }
        )

    return {
        "success": True,
        "model": (
            "Tree-level identical-scalar scattering "
            "in real phi^4 theory"
        ),
        "process": "phi + phi -> phi + phi",
        "units": "Natural units: hbar = c = 1",
        "parameters": {
            "mass": mass,
            "sqrt_s": sqrt_s,
            "s": s,
            "lambda": lam,
            "angular_points": angular_points,
        },
        "kinematics": {
            "center_of_mass_energy": sqrt_s,
            "incoming_momentum": momentum,
            "outgoing_momentum": momentum,
            "threshold_energy": 2.0 * mass,
        },
        "amplitude": {
            "formula": "M = -i lambda",
            "real": 0.0,
            "imaginary": -lam,
            "magnitude": lam,
            "squared_magnitude": amplitude_magnitude_squared,
        },
        "cross_section": {
            "differential_formula": (
                "d sigma/d Omega = |M|^2/(128 pi^2 s)"
            ),
            "differential_value": differential_cross_section,
            "total_formula": (
                "sigma = |M|^2/(32 pi s)"
            ),
            "total_value": total_cross_section,
        },
        "angular_distribution": angles,
        "interpretation": [
            "The interaction is a single four-point contact vertex.",
            "The tree-level amplitude is independent of scattering angle.",
            "Therefore the differential cross section is isotropic.",
            "The final-state identical-particle factor of 1/2 is included.",
            "This calculation excludes loop corrections and renormalization.",
            "The result is a perturbative educational model.",
        ],
    }
