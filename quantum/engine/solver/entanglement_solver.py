import numpy as np

from quantum.computing.quantum_gates import (
    STANDARD_STATES,
    measurement_probabilities,
)


BELL_STATES = {
    "phi_plus": "Φ+",
    "phi_minus": "Φ−",
    "psi_plus": "Ψ+",
    "psi_minus": "Ψ−",
}


def analyze_bell_state(state_name):
    name = state_name.strip().lower()

    if name not in BELL_STATES:
        raise ValueError(
            f"Unknown Bell state '{state_name}'."
        )

    state = STANDARD_STATES[name].copy()

    probabilities = measurement_probabilities(state)

    density_matrix = np.outer(
        state,
        np.conjugate(state),
    )

    reduced_density_matrix = np.zeros(
        (2, 2),
        dtype=complex,
    )

    for a in range(2):
        for b in range(2):
            for b2 in range(2):
                index_1 = 2 * a + b
                index_2 = 2 * a + b2

                reduced_density_matrix[b, b2] += (
                    density_matrix[index_1, index_2]
                )

    purity = float(
        np.real(
            np.trace(
                reduced_density_matrix
                @ reduced_density_matrix
            )
        )
    )

    entangled = purity < 1.0 - 1e-10

    return {
        "state_name": name,
        "label": BELL_STATES[name],
        "dimension": len(state),
        "state": [
            {
                "real": float(value.real),
                "imag": float(value.imag),
            }
            for value in state
        ],
        "probabilities": probabilities,
        "reduced_density_matrix": [
            [
                {
                    "real": float(value.real),
                    "imag": float(value.imag),
                }
                for value in row
            ]
            for row in reduced_density_matrix
        ],
        "reduced_state_purity": purity,
        "is_entangled": entangled,
    }
