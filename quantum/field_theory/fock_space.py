import math


def _validate(mass, modes, box_length, occupation_numbers):
    if mass < 0:
        raise ValueError("Mass must be non-negative.")

    if modes < 1 or modes > 32:
        raise ValueError("Modes must be between 1 and 32.")

    if box_length <= 0:
        raise ValueError("Box length must be positive.")

    if len(occupation_numbers) != modes:
        raise ValueError(
            "The number of occupation values must equal the number of modes."
        )

    for n in occupation_numbers:
        if n < 0 or int(n) != n:
            raise ValueError(
                "Occupation numbers must be non-negative integers."
            )


def _mode_data(mass, modes, box_length, occupation_numbers):
    data = []

    for mode in range(modes):
        momentum = 2.0 * math.pi * mode / box_length
        omega = math.sqrt(momentum**2 + mass**2)
        occupation = occupation_numbers[mode]

        data.append(
            {
                "mode": mode,
                "momentum": momentum,
                "frequency": omega,
                "occupation_number": occupation,
                "particle_energy": occupation * omega,
                "zero_point_energy": 0.5 * omega,
                "total_mode_energy": (occupation + 0.5) * omega,
            }
        )

    return data


def fock_space_summary(
    mass=1.0,
    modes=8,
    box_length=20.0,
    occupation_numbers=None,
):
    if occupation_numbers is None:
        occupation_numbers = [0] * modes

    occupation_numbers = [int(n) for n in occupation_numbers]

    _validate(
        mass,
        modes,
        box_length,
        occupation_numbers,
    )

    modes_data = _mode_data(
        mass,
        modes,
        box_length,
        occupation_numbers,
    )

    total_particles = sum(occupation_numbers)

    excitation_energy = sum(
        item["particle_energy"]
        for item in modes_data
    )

    vacuum_energy = sum(
        item["zero_point_energy"]
        for item in modes_data
    )

    total_energy = (
        excitation_energy
        + vacuum_energy
    )

    occupied_modes = [
        item
        for item in modes_data
        if item["occupation_number"] > 0
    ]

    ket = "|" + ",".join(
        map(str, occupation_numbers)
    ) + "⟩"

    return {
        "success": True,
        "model": (
            "Finite-mode bosonic Fock space "
            "for a real scalar field"
        ),
        "units": "Natural units: hbar = c = 1",
        "parameters": {
            "mass": mass,
            "modes": modes,
            "box_length": box_length,
            "occupation_numbers": occupation_numbers,
        },
        "fock_state": {
            "ket": ket,
            "total_particle_number": total_particles,
            "occupied_modes": [
                item["mode"]
                for item in occupied_modes
            ],
        },
        "energies": {
            "vacuum_energy": vacuum_energy,
            "excitation_energy": excitation_energy,
            "total_energy": total_energy,
        },
        "modes_data": modes_data,
        "operator_rules": {
            "annihilation": (
                "a_k |..., n_k, ...⟩ = sqrt(n_k) "
                "|..., n_k - 1, ...⟩"
            ),
            "creation": (
                "a†_k |..., n_k, ...⟩ = sqrt(n_k + 1) "
                "|..., n_k + 1, ...⟩"
            ),
            "commutator": "[a_k, a†_q] = delta_kq",
        },
        "interpretation": [
            "The occupation number n_k counts bosonic quanta in mode k.",
            "The vacuum has zero particles in every mode.",
            "A one-particle state has exactly one occupied mode.",
            "Multiple nonzero occupation numbers represent a multiparticle state.",
            "Creation adds one quantum to a selected mode.",
            "Annihilation removes one quantum from a selected mode.",
            (
                "The finite number of modes is an educational "
                "approximation to continuum Fock space."
            ),
        ],
    }


def apply_creation_operator(
    occupation_numbers,
    mode,
):
    state = [int(n) for n in occupation_numbers]

    if mode < 0 or mode >= len(state):
        raise ValueError("Mode index is out of range.")

    coefficient = math.sqrt(
        state[mode] + 1
    )

    state[mode] += 1

    return {
        "operator": "creation",
        "mode": mode,
        "coefficient": coefficient,
        "input_occupation_numbers": occupation_numbers,
        "output_occupation_numbers": state,
        "input_ket": (
            "|"
            + ",".join(map(str, occupation_numbers))
            + "⟩"
        ),
        "output_ket": (
            "|"
            + ",".join(map(str, state))
            + "⟩"
        ),
        "rule": (
            "a†_k |..., n_k, ...⟩ = sqrt(n_k + 1) "
            "|..., n_k + 1, ...⟩"
        ),
    }


def apply_annihilation_operator(
    occupation_numbers,
    mode,
):
    state = [int(n) for n in occupation_numbers]

    if mode < 0 or mode >= len(state):
        raise ValueError("Mode index is out of range.")

    if state[mode] == 0:
        return {
            "operator": "annihilation",
            "mode": mode,
            "coefficient": 0.0,
            "input_occupation_numbers": occupation_numbers,
            "output_occupation_numbers": state,
            "input_ket": (
                "|"
                + ",".join(map(str, occupation_numbers))
                + "⟩"
            ),
            "output_ket": "0",
            "rule": "a_k |..., 0, ...⟩ = 0",
        }

    coefficient = math.sqrt(
        state[mode]
    )

    state[mode] -= 1

    return {
        "operator": "annihilation",
        "mode": mode,
        "coefficient": coefficient,
        "input_occupation_numbers": occupation_numbers,
        "output_occupation_numbers": state,
        "input_ket": (
            "|"
            + ",".join(map(str, occupation_numbers))
            + "⟩"
        ),
        "output_ket": (
            "|"
            + ",".join(map(str, state))
            + "⟩"
        ),
        "rule": (
            "a_k |..., n_k, ...⟩ = sqrt(n_k) "
            "|..., n_k - 1, ...⟩"
        ),
    }


def fock_operator_action(
    occupation_numbers,
    mode,
    operator,
):
    if any(
        n < 0 or int(n) != n
        for n in occupation_numbers
    ):
        raise ValueError(
            "Occupation numbers must be non-negative integers."
        )

    if operator == "creation":
        return apply_creation_operator(
            occupation_numbers,
            mode,
        )

    if operator == "annihilation":
        return apply_annihilation_operator(
            occupation_numbers,
            mode,
        )

    raise ValueError(
        "Operator must be 'creation' or 'annihilation'."
    )
