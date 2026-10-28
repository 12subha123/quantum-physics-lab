import numpy as np


# ============================================================
# BASIC SINGLE-QUBIT STATES
# ============================================================

ket0 = np.array(
    [1, 0],
    dtype=complex,
)

ket1 = np.array(
    [0, 1],
    dtype=complex,
)


# ============================================================
# COMMON SINGLE-QUBIT STATES
# ============================================================

ket_plus = (
    1 / np.sqrt(2)
) * np.array(
    [1, 1],
    dtype=complex,
)

ket_minus = (
    1 / np.sqrt(2)
) * np.array(
    [1, -1],
    dtype=complex,
)

ket_plus_i = (
    1 / np.sqrt(2)
) * np.array(
    [1, 1j],
    dtype=complex,
)

ket_minus_i = (
    1 / np.sqrt(2)
) * np.array(
    [1, -1j],
    dtype=complex,
)


# ============================================================
# SINGLE-QUBIT GATES
# ============================================================

I = np.array(
    [
        [1, 0],
        [0, 1],
    ],
    dtype=complex,
)

X = np.array(
    [
        [0, 1],
        [1, 0],
    ],
    dtype=complex,
)

Y = np.array(
    [
        [0, -1j],
        [1j, 0],
    ],
    dtype=complex,
)

Z = np.array(
    [
        [1, 0],
        [0, -1],
    ],
    dtype=complex,
)

H = (
    1 / np.sqrt(2)
) * np.array(
    [
        [1, 1],
        [1, -1],
    ],
    dtype=complex,
)

S = np.array(
    [
        [1, 0],
        [0, 1j],
    ],
    dtype=complex,
)

T = np.array(
    [
        [1, 0],
        [0, np.exp(1j * np.pi / 4)],
    ],
    dtype=complex,
)


# ============================================================
# TWO-QUBIT BASIS STATES
# Basis ordering:
# |00>, |01>, |10>, |11>
# ============================================================

ket00 = np.array(
    [1, 0, 0, 0],
    dtype=complex,
)

ket01 = np.array(
    [0, 1, 0, 0],
    dtype=complex,
)

ket10 = np.array(
    [0, 0, 1, 0],
    dtype=complex,
)

ket11 = np.array(
    [0, 0, 0, 1],
    dtype=complex,
)


# ============================================================
# BELL STATES
# ============================================================

bell_phi_plus = (
    1 / np.sqrt(2)
) * np.array(
    [1, 0, 0, 1],
    dtype=complex,
)

bell_phi_minus = (
    1 / np.sqrt(2)
) * np.array(
    [1, 0, 0, -1],
    dtype=complex,
)

bell_psi_plus = (
    1 / np.sqrt(2)
) * np.array(
    [0, 1, 1, 0],
    dtype=complex,
)

bell_psi_minus = (
    1 / np.sqrt(2)
) * np.array(
    [0, 1, -1, 0],
    dtype=complex,
)


# ============================================================
# TWO-QUBIT GATES
# ============================================================

CNOT = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)

CZ = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1],
    ],
    dtype=complex,
)

SWAP = np.array(
    [
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ],
    dtype=complex,
)


# ============================================================
# GATE REGISTRY
# ============================================================

SINGLE_QUBIT_GATES = {
    "I": I,
    "X": X,
    "Y": Y,
    "Z": Z,
    "H": H,
    "S": S,
    "T": T,
}

TWO_QUBIT_GATES = {
    "CNOT": CNOT,
    "CX": CNOT,
    "CZ": CZ,
    "SWAP": SWAP,
}


# ============================================================
# STATE REGISTRY
# ============================================================

STANDARD_STATES = {
    "ket0": ket0,
    "ket1": ket1,
    "0": ket0,
    "1": ket1,

    "plus": ket_plus,
    "minus": ket_minus,
    "plus_i": ket_plus_i,
    "minus_i": ket_minus_i,

    "ket00": ket00,
    "ket01": ket01,
    "ket10": ket10,
    "ket11": ket11,

    "phi_plus": bell_phi_plus,
    "phi_minus": bell_phi_minus,
    "psi_plus": bell_psi_plus,
    "psi_minus": bell_psi_minus,
}


# ============================================================
# VALIDATION
# ============================================================

def normalize_state(state):
    state = np.asarray(
        state,
        dtype=complex,
    )

    norm = np.linalg.norm(state)

    if norm <= 1e-12:
        raise ValueError(
            "Quantum state cannot be the zero vector."
        )

    return state / norm


def validate_state(state):
    state = np.asarray(
        state,
        dtype=complex,
    )

    if state.ndim != 1:
        raise ValueError(
            "Quantum state must be a one-dimensional vector."
        )

    dimension = len(state)

    if dimension < 2:
        raise ValueError(
            "Quantum state must contain at least two amplitudes."
        )

    if dimension & (dimension - 1):
        raise ValueError(
            "Quantum-state dimension must be a power of two."
        )

    return state


# ============================================================
# STATE UTILITIES
# ============================================================

def get_standard_state(name):
    key = name.strip().lower()

    if key not in STANDARD_STATES:
        raise ValueError(
            f"Unknown state: {name}"
        )

    return STANDARD_STATES[key].copy()


def probabilities(state):
    state = validate_state(state)

    state = normalize_state(state)

    return np.abs(state) ** 2


def measurement_probabilities(state):
    probs = probabilities(state)

    return {
        format(index, f"0{int(np.log2(len(probs)))}b"):
        float(probability)
        for index, probability in enumerate(probs)
    }


# ============================================================
# GATE APPLICATION
# ============================================================

def apply_gate(gate, state):
    gate = np.asarray(
        gate,
        dtype=complex,
    )

    state = validate_state(state)

    state = normalize_state(state)

    if gate.ndim != 2:
        raise ValueError(
            "Quantum gate must be a matrix."
        )

    if gate.shape[1] != len(state):
        raise ValueError(
            "Gate dimensions do not match the quantum state."
        )

    result = gate @ state

    return normalize_state(result)


def apply_named_gate(gate_name, state):
    name = gate_name.strip().upper()

    state = validate_state(state)

    if len(state) == 2:
        gate = SINGLE_QUBIT_GATES.get(name)

    elif len(state) == 4:
        gate = TWO_QUBIT_GATES.get(name)

    else:
        gate = None

    if gate is None:
        raise ValueError(
            f"Gate '{gate_name}' is not compatible "
            f"with a {len(state)}-dimensional state."
        )

    return apply_gate(
        gate,
        state,
    )


# ============================================================
# ARBITRARY COMPLEX STATE
# ============================================================

def create_complex_state(amplitudes):
    state = np.asarray(
        amplitudes,
        dtype=complex,
    )

    validate_state(state)

    return normalize_state(state)


# ============================================================
# SIMPLE TWO-QUBIT TENSOR PRODUCT
# ============================================================

def tensor_product(state_a, state_b):
    state_a = validate_state(state_a)
    state_b = validate_state(state_b)

    return normalize_state(
        np.kron(
            state_a,
            state_b,
        )
    )


# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":

    print("QUANTUM GATE ENGINE")
    print("===================")
    print()

    print("1. Hadamard on |0>")

    result = apply_named_gate(
        "H",
        ket0,
    )

    print(result)
    print(measurement_probabilities(result))
    print()

    print("2. Bell state |Phi+>")

    print(bell_phi_plus)
    print(measurement_probabilities(bell_phi_plus))
    print()

    print("3. CNOT on |10>")

    result = apply_named_gate(
        "CNOT",
        ket10,
    )

    print(result)
    print(measurement_probabilities(result))
    print()

    print("4. Arbitrary complex state")

    custom = create_complex_state(
        [
            1 + 1j,
            2 - 1j,
        ]
    )

    print(custom)
    print(measurement_probabilities(custom))
    print()

    print("Quantum gate engine test completed.")
