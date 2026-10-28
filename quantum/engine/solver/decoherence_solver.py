import numpy as np

from quantum.engine.solver.density_matrix_solver import (
    validate_density_matrix,
)


def apply_dephasing(
    density_matrix,
    coherence_factor,
):
    """
    Apply a simple phase-damping/dephasing model to a density matrix.

    The diagonal populations remain unchanged while the off-diagonal
    coherence terms are multiplied by the supplied coherence factor.

    coherence_factor:
        1.0 -> no decoherence
        0.0 -> complete dephasing
    """

    rho = validate_density_matrix(
        density_matrix
    )

    if not 0.0 <= coherence_factor <= 1.0:
        raise ValueError(
            "Coherence factor must be between 0 and 1."
        )

    result = rho.copy()

    for row in range(result.shape[0]):
        for column in range(result.shape[1]):
            if row != column:
                result[row, column] *= coherence_factor

    return validate_density_matrix(result)


def dephasing_from_time(
    density_matrix,
    time,
    decoherence_rate,
):
    """
    Apply exponential dephasing:

        coherence_factor = exp(-gamma * t)

    where gamma is the decoherence rate.
    """

    rho = validate_density_matrix(
        density_matrix
    )

    if time < 0:
        raise ValueError(
            "Time cannot be negative."
        )

    if decoherence_rate < 0:
        raise ValueError(
            "Decoherence rate cannot be negative."
        )

    coherence_factor = np.exp(
        -decoherence_rate * time
    )

    return apply_dephasing(
        rho,
        float(coherence_factor),
    )


def simulate_dephasing(
    density_matrix,
    time_start,
    time_end,
    steps,
    decoherence_rate,
):
    """
    Simulate density-matrix dephasing over time.
    """

    rho = validate_density_matrix(
        density_matrix
    )

    if time_end < time_start:
        raise ValueError(
            "time_end must be greater than or equal to time_start."
        )

    if steps < 2:
        raise ValueError(
            "steps must be at least 2."
        )

    if decoherence_rate < 0:
        raise ValueError(
            "Decoherence rate cannot be negative."
        )

    times = np.linspace(
        time_start,
        time_end,
        steps,
    )

    coherence_factors = []
    purity_values = []
    entropy_values = []
    density_matrices = []

    for time in times:
        evolved = dephasing_from_time(
            rho,
            float(time),
            decoherence_rate,
        )

        factor = np.exp(
            -decoherence_rate * time
        )

        eigenvalues = np.linalg.eigvalsh(
            evolved
        )

        eigenvalues = eigenvalues[
            eigenvalues > 1e-12
        ]

        entropy = -np.sum(
            eigenvalues
            * np.log2(eigenvalues)
        )

        purity_value = np.trace(
            evolved @ evolved
        )

        coherence_factors.append(
            float(factor)
        )

        purity_values.append(
            float(np.real(purity_value))
        )

        entropy_values.append(
            float(np.real(entropy))
        )

        density_matrices.append(
            evolved
        )

    return {
        "times": [
            float(value)
            for value in times
        ],
        "coherence_factors": coherence_factors,
        "purity": purity_values,
        "von_neumann_entropy": entropy_values,
        "density_matrices": [
            [
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
                for row in matrix
            ]
            for matrix in density_matrices
        ],
    }


def decoherence_summary(
    density_matrix,
    time,
    decoherence_rate,
):
    """
    Return the density matrix and physical indicators
    after dephasing for a specified time.
    """

    evolved = dephasing_from_time(
        density_matrix,
        time,
        decoherence_rate,
    )

    eigenvalues = np.linalg.eigvalsh(
        evolved
    )

    eigenvalues = eigenvalues[
        eigenvalues > 1e-12
    ]

    entropy = -np.sum(
        eigenvalues
        * np.log2(eigenvalues)
    )

    purity_value = np.trace(
        evolved @ evolved
    )

    coherence_factor = np.exp(
        -decoherence_rate * time
    )

    return {
        "time": float(time),
        "decoherence_rate": float(
            decoherence_rate
        ),
        "coherence_factor": float(
            coherence_factor
        ),
        "purity": float(
            np.real(purity_value)
        ),
        "von_neumann_entropy": float(
            np.real(entropy)
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
            for row in evolved
        ],
    }