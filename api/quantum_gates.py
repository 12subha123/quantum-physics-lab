from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import numpy as np

from quantum.computing.quantum_gates import (
    STANDARD_STATES,
    SINGLE_QUBIT_GATES,
    TWO_QUBIT_GATES,
    apply_named_gate,
    create_complex_state,
    measurement_probabilities,
)

router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Computing"],
)


class QuantumGateRequest(BaseModel):
    state_name: str = "ket0"
    amplitudes_real: list[float] | None = None
    amplitudes_imag: list[float] | None = None
    gate: str = "H"


def vector_to_list(vector):
    return [
        {
            "real": float(value.real),
            "imag": float(value.imag),
        }
        for value in vector
    ]


def calculate_bloch_coordinates(state):
    if len(state) != 2:
        return None

    alpha = complex(state[0])
    beta = complex(state[1])

    x = 2.0 * float(np.real(np.conjugate(alpha) * beta))
    y = 2.0 * float(np.imag(np.conjugate(alpha) * beta))
    z = float(abs(alpha) ** 2 - abs(beta) ** 2)

    x = float(np.clip(x, -1.0, 1.0))
    y = float(np.clip(y, -1.0, 1.0))
    z = float(np.clip(z, -1.0, 1.0))

    theta = float(np.arccos(z))
    phi = float(np.arctan2(y, x))

    return {
        "x": x,
        "y": y,
        "z": z,
        "theta": theta,
        "phi": phi,
        "theta_degrees": float(np.degrees(theta)),
        "phi_degrees": float(np.degrees(phi)),
    }


def get_state(request: QuantumGateRequest):
    if request.amplitudes_real is not None:
        real = request.amplitudes_real
        imag = request.amplitudes_imag or [0.0] * len(real)

        if len(real) != len(imag):
            raise ValueError(
                "Real and imaginary amplitude lists must have the same length."
            )

        amplitudes = [
            complex(r, i)
            for r, i in zip(real, imag)
        ]

        return create_complex_state(amplitudes)

    name = request.state_name.strip().lower()

    if name not in STANDARD_STATES:
        raise ValueError(
            f"Unknown state '{request.state_name}'."
        )

    return STANDARD_STATES[name].copy()


@router.get("/gates/states")
def available_states():
    return {
        "success": True,
        "single_qubit_states": [
            "ket0",
            "ket1",
            "plus",
            "minus",
            "plus_i",
            "minus_i",
        ],
        "two_qubit_states": [
            "ket00",
            "ket01",
            "ket10",
            "ket11",
        ],
        "bell_states": [
            "phi_plus",
            "phi_minus",
            "psi_plus",
            "psi_minus",
        ],
    }


@router.get("/gates")
def available_gates():
    return {
        "success": True,
        "single_qubit_gates": list(
            SINGLE_QUBIT_GATES.keys()
        ),
        "two_qubit_gates": list(
            TWO_QUBIT_GATES.keys()
        ),
    }


@router.post("/gates")
def quantum_gate(request: QuantumGateRequest):
    try:
        state = get_state(request)

        gate_name = request.gate.strip().upper()

        result = apply_named_gate(
            gate_name,
            state,
        )

        bloch_coordinates = calculate_bloch_coordinates(result)

        return {
            "success": True,
            "message": "Quantum gate calculation completed successfully.",
            "state_name": request.state_name,
            "gate": gate_name,
            "dimension": len(state),
            "input_state": vector_to_list(state),
            "output_state": vector_to_list(result),
            "probabilities": measurement_probabilities(result),
            "bloch_coordinates": bloch_coordinates,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
