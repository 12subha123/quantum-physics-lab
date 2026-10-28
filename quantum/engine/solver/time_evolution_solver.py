import numpy as np

DEFAULT_HBAR = 1.0


def normalize_state(state):
    state = np.asarray(state, dtype=complex)

    if state.ndim != 1:
        raise ValueError("Quantum state must be a one-dimensional vector.")

    if len(state) < 2:
        raise ValueError("Quantum state must contain at least two amplitudes.")

    dimension = len(state)

    if dimension & (dimension - 1):
        raise ValueError(
            "Quantum-state dimension must be a power of two."
        )

    norm = np.linalg.norm(state)

    if norm <= 1e-12:
        raise ValueError("Quantum state cannot be the zero vector.")

    return state / norm


def validate_hamiltonian(hamiltonian, tolerance=1e-10):
    H = np.asarray(hamiltonian, dtype=complex)

    if H.ndim != 2:
        raise ValueError("Hamiltonian must be a two-dimensional matrix.")

    if H.shape[0] != H.shape[1]:
        raise ValueError("Hamiltonian must be a square matrix.")

    dimension = H.shape[0]

    if dimension < 2:
        raise ValueError("Hamiltonian must have dimension at least 2.")

    if dimension & (dimension - 1):
        raise ValueError(
            "Hamiltonian dimension must be a power of two."
        )

    if not np.allclose(H, H.conjugate().T, atol=tolerance):
        raise ValueError(
            "Hamiltonian must be Hermitian."
        )

    return H


def measurement_probabilities(state):
    state = normalize_state(state)

    probabilities = np.abs(state) ** 2
    number_of_qubits = int(np.log2(len(state)))

    return {
        format(index, f"0{number_of_qubits}b"): float(probability)
        for index, probability in enumerate(probabilities)
    }


def expectation_value(state, operator):
    state = normalize_state(state)
    operator = np.asarray(operator, dtype=complex)

    value = np.vdot(state, operator @ state)

    return float(np.real(value))


def evolve_state(
    state,
    hamiltonian,
    time,
    hbar=DEFAULT_HBAR,
):
    state = normalize_state(state)
    H = validate_hamiltonian(hamiltonian)

    if H.shape[0] != len(state):
        raise ValueError(
            "Hamiltonian dimension must match quantum-state dimension."
        )

    if hbar <= 0:
        raise ValueError("hbar must be greater than zero.")

    time = float(time)

    # H is Hermitian, so eigh gives real eigenvalues
    # and an orthonormal eigenvector basis.
    eigenvalues, eigenvectors = np.linalg.eigh(H)

    # Spectral form of exp(-iHt/hbar).
    phases = np.exp(
        -1j * eigenvalues * time / hbar
    )

    initial_coordinates = (
        eigenvectors.conjugate().T @ state
    )

    evolved_coordinates = phases * initial_coordinates

    evolved_state = (
        eigenvectors @ evolved_coordinates
    )

    return normalize_state(evolved_state)


def analyze_time_evolution(
    state,
    hamiltonian,
    time,
    hbar=DEFAULT_HBAR,
):
    initial_state = normalize_state(state)
    H = validate_hamiltonian(hamiltonian)

    if H.shape[0] != len(initial_state):
        raise ValueError(
            "Hamiltonian dimension must match quantum-state dimension."
        )

    evolved_state = evolve_state(
        initial_state,
        H,
        time,
        hbar,
    )

    initial_energy = expectation_value(
        initial_state,
        H,
    )

    final_energy = expectation_value(
        evolved_state,
        H,
    )

    return {
        "time": float(time),
        "hbar": float(hbar),
        "dimension": len(initial_state),
        "initial_state": [
            {
                "real": float(value.real),
                "imag": float(value.imag),
            }
            for value in initial_state
        ],
        "evolved_state": [
            {
                "real": float(value.real),
                "imag": float(value.imag),
            }
            for value in evolved_state
        ],
        "initial_probabilities": measurement_probabilities(
            initial_state
        ),
        "evolved_probabilities": measurement_probabilities(
            evolved_state
        ),
        "initial_energy": initial_energy,
        "final_energy": final_energy,
        "normalization": float(
            np.real(np.vdot(evolved_state, evolved_state))
        ),
    }
