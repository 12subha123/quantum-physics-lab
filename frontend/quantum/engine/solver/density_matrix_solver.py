import numpy as np


def normalize_state(state):
    state = np.asarray(state, dtype=complex)

    if state.ndim != 1:
        raise ValueError(
            "Quantum state must be a one-dimensional vector."
        )

    if len(state) < 2:
        raise ValueError(
            "Quantum state must contain at least two amplitudes."
        )

    dimension = len(state)

    if dimension & (dimension - 1):
        raise ValueError(
            "Quantum-state dimension must be a power of two."
        )

    norm = np.linalg.norm(state)

    if norm <= 1e-12:
        raise ValueError(
            "Quantum state cannot be the zero vector."
        )

    return state / norm


def pure_state_density_matrix(state):
    state = normalize_state(state)

    return np.outer(
        state,
        np.conjugate(state),
    )


def validate_density_matrix(
    density_matrix,
    tolerance=1e-10,
):
    rho = np.asarray(
        density_matrix,
        dtype=complex,
    )

    if rho.ndim != 2:
        raise ValueError(
            "Density matrix must be two-dimensional."
        )

    if rho.shape[0] != rho.shape[1]:
        raise ValueError(
            "Density matrix must be square."
        )

    dimension = rho.shape[0]

    if dimension < 2:
        raise ValueError(
            "Density matrix must have dimension at least 2."
        )

    if dimension & (dimension - 1):
        raise ValueError(
            "Density-matrix dimension must be a power of two."
        )

    if not np.allclose(
        rho,
        rho.conjugate().T,
        atol=tolerance,
    ):
        raise ValueError(
            "Density matrix must be Hermitian."
        )

    trace = np.trace(rho)

    if not np.isclose(
        trace.real,
        1.0,
        atol=tolerance,
    ) or abs(trace.imag) > tolerance:
        raise ValueError(
            "Density matrix must have trace equal to 1."
        )

    eigenvalues = np.linalg.eigvalsh(rho)

    if np.min(eigenvalues) < -tolerance:
        raise ValueError(
            "Density matrix must be positive semidefinite."
        )

    return rho


def density_matrix_from_probabilities(
    states,
    probabilities,
):
    if len(states) != len(probabilities):
        raise ValueError(
            "States and probabilities must have the same length."
        )

    if len(states) == 0:
        raise ValueError(
            "At least one state is required."
        )

    probabilities = np.asarray(
        probabilities,
        dtype=float,
    )

    if np.any(probabilities < 0):
        raise ValueError(
            "Probabilities cannot be negative."
        )

    total = np.sum(probabilities)

    if total <= 1e-12:
        raise ValueError(
            "Probability sum must be greater than zero."
        )

    probabilities = probabilities / total

    density_matrix = np.zeros(
        (
            len(states[0]),
            len(states[0]),
        ),
        dtype=complex,
    )

    for state, probability in zip(
        states,
        probabilities,
    ):
        normalized = normalize_state(state)

        density_matrix += (
            probability
            * pure_state_density_matrix(normalized)
        )

    return validate_density_matrix(
        density_matrix
    )


def measurement_probabilities(
    density_matrix,
):
    rho = validate_density_matrix(
        density_matrix
    )

    probabilities = np.real(
        np.diag(rho)
    )

    number_of_qubits = int(
        np.log2(len(probabilities))
    )

    return {
        format(
            index,
            f"0{number_of_qubits}b",
        ): float(probability)
        for index, probability in enumerate(
            probabilities
        )
    }


def purity(density_matrix):
    rho = validate_density_matrix(
        density_matrix
    )

    value = np.trace(
        rho @ rho
    )

    return float(
        np.real(value)
    )


def von_neumann_entropy(
    density_matrix,
):
    rho = validate_density_matrix(
        density_matrix
    )

    eigenvalues = np.linalg.eigvalsh(rho)

    eigenvalues = eigenvalues[
        eigenvalues > 1e-12
    ]

    entropy = -np.sum(
        eigenvalues
        * np.log2(eigenvalues)
    )

    return float(
        np.real(entropy)
    )


def density_matrix_summary(
    density_matrix,
):
    rho = validate_density_matrix(
        density_matrix
    )

    eigenvalues = np.linalg.eigvalsh(rho)

    return {
        "dimension": int(rho.shape[0]),
        "qubits": int(
            np.log2(rho.shape[0])
        ),
        "trace": float(
            np.real(np.trace(rho))
        ),
        "purity": purity(rho),
        "von_neumann_entropy": (
            von_neumann_entropy(rho)
        ),
        "eigenvalues": [
            float(np.real(value))
            for value in eigenvalues
        ],
        "measurement_probabilities": (
            measurement_probabilities(rho)
        ),
        "density_matrix": [
            [
                {
                    "real": float(
                        value.real
                    ),
                    "imag": float(
                        value.imag
                    ),
                }
                for value in row
            ]
            for row in rho
        ],
    }