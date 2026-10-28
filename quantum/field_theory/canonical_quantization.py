import math


def _validate(mass, modes, box_length, occupation_numbers):
    if mass < 0:
        raise ValueError("Mass must be non-negative.")

    if modes < 1 or modes > 32:
        raise ValueError("Modes must be between 1 and 32.")

    if box_length <= 0:
        raise ValueError("Box length must be positive.")

    if any(n < 0 or int(n) != n for n in occupation_numbers):
        raise ValueError("Occupation numbers must be non-negative integers.")


def scalar_mode_quantization(
    mass=1.0,
    modes=8,
    box_length=20.0,
    occupation_numbers=None,
):
    if occupation_numbers is None:
        occupation_numbers = [0] * modes

    occupation_numbers = [int(n) for n in occupation_numbers]

    if len(occupation_numbers) != modes:
        raise ValueError(
            "The number of occupation values must equal the number of modes."
        )

    _validate(
        mass,
        modes,
        box_length,
        occupation_numbers,
    )

    mode_data = []

    vacuum_energy = 0.0
    excitation_energy = 0.0

    for mode_index in range(modes):
        integer_mode = mode_index

        momentum = (
            2.0 * math.pi * integer_mode / box_length
        )

        omega = math.sqrt(
            momentum**2 + mass**2
        )

        occupation = occupation_numbers[mode_index]

        zero_point = 0.5 * omega
        particle_energy = occupation * omega
        total_mode_energy = (
            occupation + 0.5
        ) * omega

        vacuum_energy += zero_point
        excitation_energy += particle_energy

        mode_data.append(
            {
                "mode": mode_index,
                "integer_mode": integer_mode,
                "momentum": momentum,
                "frequency": omega,
                "occupation_number": occupation,
                "zero_point_energy": zero_point,
                "excitation_energy": particle_energy,
                "total_mode_energy": total_mode_energy,
            }
        )

    total_energy = vacuum_energy + excitation_energy

    return {
        "success": True,
        "model": "Finite-mode canonical quantization of a real scalar field",
        "units": "Natural units: hbar = c = 1",
        "parameters": {
            "mass": mass,
            "modes": modes,
            "box_length": box_length,
            "occupation_numbers": occupation_numbers,
        },
        "commutation_relation": "[a_k, a?_q] = delta_kq",
        "field_operator_structure": (
            "phi(x,t) = sum_k [a_k u_k(x,t) + "
            "a?_k u*_k(x,t)]"
        ),
        "hamiltonian_structure": (
            "H = sum_k omega_k (a?_k a_k + 1/2)"
        ),
        "vacuum_energy": vacuum_energy,
        "excitation_energy": excitation_energy,
        "total_energy": total_energy,
        "modes_data": mode_data,
        "interpretation": [
            "Each normal mode behaves like a quantum harmonic oscillator.",
            "The occupation number counts quanta in that mode.",
            "a? creates one quantum and a annihilates one quantum.",
            "The 1/2 term represents the zero-point contribution of each mode.",
            "The finite-mode cutoff is an educational approximation to the continuum field.",
        ],
    }
