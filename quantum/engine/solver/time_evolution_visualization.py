import numpy as np

from quantum.engine.solver.time_evolution_solver import (
    normalize_state,
    validate_hamiltonian,
    evolve_state,
)


def simulate_time_evolution(
    state,
    hamiltonian,
    time_start,
    time_end,
    steps,
    hbar=1.0,
):
    state = normalize_state(state)
    H = validate_hamiltonian(hamiltonian)

    if H.shape[0] != len(state):
        raise ValueError(
            "Hamiltonian dimension must match quantum-state dimension."
        )

    if steps < 2:
        raise ValueError("steps must be at least 2.")

    if time_end <= time_start:
        raise ValueError("time_end must be greater than time_start.")

    times = np.linspace(
        float(time_start),
        float(time_end),
        int(steps),
    )

    probabilities = []

    for time in times:
        evolved = evolve_state(
            state,
            H,
            time,
            hbar,
        )

        probabilities.append(
            np.abs(evolved) ** 2
        )

    probabilities = np.asarray(probabilities)

    number_of_qubits = int(np.log2(len(state)))

    return {
        "times": [float(value) for value in times],
        "probabilities": [
            {
                format(index, f"0{number_of_qubits}b"): float(
                    probability
                )
                for index, probability in enumerate(row)
            }
            for row in probabilities
        ],
        "dimension": len(state),
        "qubits": number_of_qubits,
        "hbar": float(hbar),
    }
