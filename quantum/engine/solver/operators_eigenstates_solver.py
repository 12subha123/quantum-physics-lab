from dataclasses import dataclass

import numpy as np


@dataclass
class OperatorEigenstateResult:
    operator_name: str
    matrix: list
    eigenvalues: list
    eigenvectors: list
    verification: list


OPERATORS = {
    "pauli_x": np.array(
        [
            [0, 1],
            [1, 0],
        ],
        dtype=complex,
    ),
    "pauli_y": np.array(
        [
            [0, -1j],
            [1j, 0],
        ],
        dtype=complex,
    ),
    "pauli_z": np.array(
        [
            [1, 0],
            [0, -1],
        ],
        dtype=complex,
    ),
}


def get_operator(name: str) -> np.ndarray:
    key = name.strip().lower()

    if key not in OPERATORS:
        raise ValueError(
            "Unknown operator. "
            "Available operators: pauli_x, pauli_y, pauli_z."
        )

    return OPERATORS[key].copy()


def complex_to_dict(value: complex) -> dict:
    return {
        "real": float(value.real),
        "imag": float(value.imag),
    }


def matrix_to_list(matrix: np.ndarray) -> list:
    return [
        [
            complex_to_dict(value)
            for value in row
        ]
        for row in matrix
    ]


def vector_to_list(vector: np.ndarray) -> list:
    return [
        complex_to_dict(value)
        for value in vector
    ]


def calculate_operator_eigenstates(
    operator_name: str,
) -> OperatorEigenstateResult:

    matrix = get_operator(operator_name)

    return calculate_matrix_eigenstates(
        matrix=matrix,
        operator_name=operator_name,
    )


def calculate_custom_operator(
    a: float,
    b: float,
    c: float,
    d: float,
) -> OperatorEigenstateResult:

    matrix = np.array(
        [
            [a, b],
            [c, d],
        ],
        dtype=complex,
    )

    return calculate_matrix_eigenstates(
        matrix=matrix,
        operator_name="custom_operator",
    )


def calculate_matrix_eigenstates(
    matrix: np.ndarray,
    operator_name: str,
) -> OperatorEigenstateResult:

    if matrix.shape != (2, 2):
        raise ValueError(
            "The operator must be a 2x2 matrix."
        )

    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    verification = []

    for index, eigenvalue in enumerate(eigenvalues):
        eigenvector = eigenvectors[:, index]

        left_side = matrix @ eigenvector
        right_side = eigenvalue * eigenvector

        residual = np.linalg.norm(
            left_side - right_side
        )

        verification.append(
            {
                "eigenvalue": complex_to_dict(
                    eigenvalue
                ),
                "residual": float(residual),
                "verified": bool(
                    residual < 1e-10
                ),
            }
        )

    return OperatorEigenstateResult(
        operator_name=operator_name,
        matrix=matrix_to_list(matrix),
        eigenvalues=[
            complex_to_dict(value)
            for value in eigenvalues
        ],
        eigenvectors=[
            vector_to_list(
                eigenvectors[:, index]
            )
            for index in range(
                eigenvectors.shape[1]
            )
        ],
        verification=verification,
    )


if __name__ == "__main__":
    print("Quantum Operators & Eigenstates")
    print("================================")
    print()

    result = calculate_custom_operator(
        a=2,
        b=1,
        c=1,
        d=2,
    )

    print("Custom operator:")
    print(result.matrix)

    print()
    print("Eigenvalues:")

    for eigenvalue in result.eigenvalues:
        print(
            f"  {eigenvalue['real']:.6f}"
            f" + "
            f"{eigenvalue['imag']:.6f}i"
        )

    print()
    print("Verification:")

    for item in result.verification:
        print(
            f"  residual="
            f"{item['residual']:.6e}, "
            f"verified="
            f"{item['verified']}"
        )
