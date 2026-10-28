import numpy as np


def normalize_state(state):
    """Normalize a quantum state vector."""
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


def measurement_probabilities(state):
    """
    Calculate computational-basis measurement probabilities.

    For a state:
        |psi> = sum_i c_i |i>

    the probability of measuring |i> is |c_i|^2.
    """
    state = normalize_state(state)

    probabilities = np.abs(state) ** 2

    probabilities = probabilities / np.sum(probabilities)

    number_of_qubits = int(np.log2(len(state)))

    return {
        format(index, f"0{number_of_qubits}b"): float(probability)
        for index, probability in enumerate(probabilities)
    }


def sample_measurement(state, shots=1, seed=None):
    """
    Simulate repeated quantum measurements.

    The quantum state is unchanged by this educational
    repeated-measurement model; each shot is sampled
    according to the Born probabilities.
    """
    state = normalize_state(state)

    if shots < 1:
        raise ValueError("Number of shots must be at least 1.")

    if not isinstance(shots, int):
        raise ValueError("Number of shots must be an integer.")

    probabilities = np.abs(state) ** 2
    probabilities = probabilities / np.sum(probabilities)

    number_of_qubits = int(np.log2(len(state)))

    basis_states = [
        format(index, f"0{number_of_qubits}b")
        for index in range(len(state))
    ]

    rng = np.random.default_rng(seed)

    samples = rng.choice(
        basis_states,
        size=shots,
        p=probabilities,
    )

    counts = {
        basis_state: int(np.sum(samples == basis_state))
        for basis_state in basis_states
    }

    return {
        "shots": int(shots),
        "counts": counts,
        "probabilities": {
            basis_state: float(probability)
            for basis_state, probability in zip(
                basis_states,
                probabilities,
            )
        },
    }


def expectation_value(state, observable):
    """
    Calculate the expectation value:

        <A> = <psi|A|psi>

    for a Hermitian observable.
    """
    state = normalize_state(state)

    observable = np.asarray(observable, dtype=complex)

    dimension = len(state)

    if observable.shape != (dimension, dimension):
        raise ValueError(
            "Observable dimension must match the quantum-state dimension."
        )

    if not np.allclose(
        observable,
        observable.conjugate().T,
        atol=1e-10,
    ):
        raise ValueError("Observable must be Hermitian.")

    value = np.vdot(state, observable @ state)

    return float(np.real(value))


def measurement_summary(state, observable=None):
    """
    Return a complete measurement summary.
    """
    state = normalize_state(state)

    probabilities = measurement_probabilities(state)

    result = {
        "dimension": int(len(state)),
        "qubits": int(np.log2(len(state))),
        "normalization": float(np.sum(np.abs(state) ** 2)),
        "measurement_probabilities": probabilities,
    }

    if observable is not None:
        result["expectation_value"] = expectation_value(
            state,
            observable,
        )

    return result