from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.engine.solver.time_evolution_solver import (
    analyze_time_evolution,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Time Evolution"],
)


class TimeEvolutionRequest(BaseModel):
    state_real: list[float]
    state_imag: list[float] | None = None

    hamiltonian_real: list[list[float]]
    hamiltonian_imag: list[list[float]] | None = None

    time: float
    hbar: float = 1.0


@router.post("/time-evolution")
def time_evolution(request: TimeEvolutionRequest):
    try:
        if request.state_imag is None:
            state_imag = [0.0] * len(request.state_real)
        else:
            state_imag = request.state_imag

        if len(request.state_real) != len(state_imag):
            raise ValueError(
                "Real and imaginary state lists must have the same length."
            )

        if request.hamiltonian_imag is None:
            hamiltonian_imag = [
                [0.0] * len(row)
                for row in request.hamiltonian_real
            ]
        else:
            hamiltonian_imag = request.hamiltonian_imag

        if len(request.hamiltonian_real) != len(hamiltonian_imag):
            raise ValueError(
                "Real and imaginary Hamiltonian matrices must have "
                "the same number of rows."
            )

        for real_row, imag_row in zip(
            request.hamiltonian_real,
            hamiltonian_imag,
        ):
            if len(real_row) != len(imag_row):
                raise ValueError(
                    "Real and imaginary Hamiltonian rows must have "
                    "the same dimensions."
                )

        state = [
            complex(real, imag)
            for real, imag in zip(
                request.state_real,
                state_imag,
            )
        ]

        hamiltonian = [
            [
                complex(real, imag)
                for real, imag in zip(real_row, imag_row)
            ]
            for real_row, imag_row in zip(
                request.hamiltonian_real,
                hamiltonian_imag,
            )
        ]

        result = analyze_time_evolution(
            state=state,
            hamiltonian=hamiltonian,
            time=request.time,
            hbar=request.hbar,
        )

        return {
            "success": True,
            "message": (
                "Quantum time evolution calculated successfully."
            ),
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
