import math
import random


def _validate_parameters(
    mass,
    coupling,
    lattice_points,
    lattice_spacing,
    sweeps,
    thermalization,
    step_size,
):
    if mass < 0:
        raise ValueError("Mass must be non-negative.")

    if coupling < 0:
        raise ValueError("Phi^4 coupling must be non-negative.")

    if lattice_points < 4 or lattice_points > 512:
        raise ValueError("Lattice points must be between 4 and 512.")

    if lattice_spacing <= 0:
        raise ValueError("Lattice spacing must be positive.")

    if sweeps < 1 or sweeps > 100000:
        raise ValueError("Sweeps must be between 1 and 100000.")

    if thermalization < 0 or thermalization >= sweeps:
        raise ValueError(
            "Thermalization must be non-negative and smaller than sweeps."
        )

    if step_size <= 0:
        raise ValueError("Metropolis step size must be positive.")


def euclidean_action(
    field,
    mass=1.0,
    coupling=1.0,
    lattice_spacing=0.25,
):
    n = len(field)

    if n < 2:
        raise ValueError("At least two lattice points are required.")

    kinetic = 0.0
    potential = 0.0

    for i in range(n):
        next_i = (i + 1) % n
        difference = field[next_i] - field[i]

        kinetic += 0.5 * (difference / lattice_spacing) ** 2

        potential += (
            0.5 * mass**2 * field[i] ** 2
            + coupling / 24.0 * field[i] ** 4
        )

    return lattice_spacing * (kinetic + potential)


def _local_action_change(
    field,
    index,
    proposed_value,
    mass,
    coupling,
    lattice_spacing,
):
    old_value = field[index]

    left = field[(index - 1) % len(field)]
    right = field[(index + 1) % len(field)]

    old_kinetic = (
        0.5 * ((old_value - left) / lattice_spacing) ** 2
        + 0.5 * ((right - old_value) / lattice_spacing) ** 2
    )

    new_kinetic = (
        0.5 * ((proposed_value - left) / lattice_spacing) ** 2
        + 0.5 * ((right - proposed_value) / lattice_spacing) ** 2
    )

    old_potential = (
        0.5 * mass**2 * old_value**2
        + coupling / 24.0 * old_value**4
    )

    new_potential = (
        0.5 * mass**2 * proposed_value**2
        + coupling / 24.0 * proposed_value**4
    )

    return lattice_spacing * (
        new_kinetic
        + new_potential
        - old_kinetic
        - old_potential
    )


def simulate_euclidean_path_integral(
    mass=1.0,
    coupling=1.0,
    lattice_points=32,
    lattice_spacing=0.25,
    sweeps=2000,
    thermalization=500,
    step_size=1.0,
    seed=1234,
):
    _validate_parameters(
        mass,
        coupling,
        lattice_points,
        lattice_spacing,
        sweeps,
        thermalization,
        step_size,
    )

    rng = random.Random(seed)
    field = [0.0] * lattice_points

    accepted = 0
    attempted = 0

    measurements = []

    for sweep in range(sweeps):
        for index in range(lattice_points):
            proposed = field[index] + rng.uniform(
                -step_size,
                step_size,
            )

            delta_action = _local_action_change(
                field,
                index,
                proposed,
                mass,
                coupling,
                lattice_spacing,
            )

            attempted += 1

            if delta_action <= 0.0 or rng.random() < math.exp(-delta_action):
                field[index] = proposed
                accepted += 1

        if sweep >= thermalization:
            action = euclidean_action(
                field,
                mass=mass,
                coupling=coupling,
                lattice_spacing=lattice_spacing,
            )

            phi2 = sum(value**2 for value in field) / lattice_points
            phi4 = sum(value**4 for value in field) / lattice_points
            mean_phi = sum(field) / lattice_points

            measurements.append(
                {
                    "sweep": sweep + 1,
                    "action": action,
                    "mean_phi": mean_phi,
                    "mean_phi_squared": phi2,
                    "mean_phi_fourth": phi4,
                }
            )

    if not measurements:
        raise RuntimeError("No measurements were produced.")

    mean_action = sum(
        item["action"] for item in measurements
    ) / len(measurements)

    mean_phi = sum(
        item["mean_phi"] for item in measurements
    ) / len(measurements)

    mean_phi_squared = sum(
        item["mean_phi_squared"] for item in measurements
    ) / len(measurements)

    mean_phi_fourth = sum(
        item["mean_phi_fourth"] for item in measurements
    ) / len(measurements)

    acceptance_rate = (
        accepted / attempted
        if attempted
        else 0.0
    )

    return {
        "success": True,
        "model": (
            "Euclidean lattice path integral for a 0+1D "
            "real scalar phi^4 theory"
        ),
        "units": "Natural units: hbar = c = 1",
        "parameters": {
            "mass": mass,
            "coupling": coupling,
            "lattice_points": lattice_points,
            "lattice_spacing": lattice_spacing,
            "sweeps": sweeps,
            "thermalization": thermalization,
            "step_size": step_size,
            "seed": seed,
        },
        "path_integral": {
            "formal_expression": (
                "Z = integral Dphi exp(-S_E[phi])"
            ),
            "weight": "exp(-S_E)",
            "action": (
                "S_E = integral d tau ["
                "1/2 (dphi/dtau)^2 + "
                "1/2 m^2 phi^2 + "
                "lambda/4! phi^4]"
            ),
        },
        "observables": {
            "mean_action": mean_action,
            "mean_phi": mean_phi,
            "mean_phi_squared": mean_phi_squared,
            "mean_phi_fourth": mean_phi_fourth,
        },
        "monte_carlo": {
            "accepted_updates": accepted,
            "attempted_updates": attempted,
            "acceptance_rate": acceptance_rate,
            "measurement_count": len(measurements),
        },
        "measurements": measurements,
        "final_field": field,
        "scientific_scope": [
            "Euclidean rather than real-time formulation.",
            "Finite one-dimensional Euclidean lattice.",
            "Periodic boundary conditions.",
            "Metropolis Monte-Carlo sampling.",
            "Real scalar phi^4 theory.",
            "Educational numerical approximation.",
            "Not a continuum-limit calculation.",
            "No renormalization or continuum extrapolation.",
            "No Minkowski-signature oscillatory integral.",
        ],
    }
