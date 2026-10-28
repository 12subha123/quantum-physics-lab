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


def qubit_count(state):
    state = np.asarray(state, dtype=complex)

    dimension = len(state)

    if dimension < 2 or (
        dimension & (dimension - 1)
    ):
        raise ValueError(
            "Quantum-state dimension must be a power of two."
        )

    return int(np.log2(dimension))


def measurement_probabilities(state):
    state = normalize_state(state)

    probabilities = np.abs(state) ** 2

    number_of_qubits = qubit_count(state)

    return {
        format(
            index,
            f"0{number_of_qubits}b",
        ): float(probability)
        for index, probability in enumerate(
            probabilities
        )
    }


def create_state(amplitudes_real, amplitudes_imag=None):
    if amplitudes_imag is None:
        amplitudes_imag = [
            0.0
        ] * len(amplitudes_real)

    if len(amplitudes_real) != len(
        amplitudes_imag
    ):
        raise ValueError(
            "Real and imaginary amplitude lists "
            "must have the same length."
        )

    amplitudes = [
        complex(real, imag)
        for real, imag in zip(
            amplitudes_real,
            amplitudes_imag,
        )
    ]

    return normalize_state(amplitudes)


def tensor_product(state_a, state_b):
    state_a = normalize_state(state_a)
    state_b = normalize_state(state_b)

    return normalize_state(
        np.kron(state_a, state_b)
    )


def basis_state(bitstring):
    bitstring = str(bitstring).strip()

    if not bitstring:
        raise ValueError(
            "Bitstring cannot be empty."
        )

    if any(bit not in "01" for bit in bitstring):
        raise ValueError(
            "Basis-state bitstring must contain "
            "only 0 and 1."
        )

    dimension = 2 ** len(bitstring)

    state = np.zeros(
        dimension,
        dtype=complex,
    )

    index = int(bitstring, 2)

    state[index] = 1.0

    return state


def state_summary(state):
    state = normalize_state(state)

    probabilities = measurement_probabilities(
        state
    )

    number_of_qubits = qubit_count(state)

    return {
        "qubits": number_of_qubits,
        "dimension": len(state),
        "state": [
            {
                "real": float(value.real),
                "imag": float(value.imag),
            }
            for value in state
        ],
        "probabilities": probabilities,
    }
