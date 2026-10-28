from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.engine.solver.time_evolution_visualization import (
    simulate_time_evolution,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Time Evolution"],
)


class TimeEvolutionVisualizationRequest(BaseModel):
    state_real: list[float]
    state_imag: list[float] | None = None

    hamiltonian_real: list[list[float]]
    hamiltonian_imag: list[list[float]] | None = None

    time_start: float = 0.0
    time_end: float = 10.0
    steps: int = 100
    hbar: float = 1.0


@router.post("/time-evolution/simulation")
def time_evolution_simulation(
    request: TimeEvolutionVisualizationRequest,
):
    try:
        state_imag = (
            request.state_imag
            if request.state_imag is not None
            else [0.0] * len(request.state_real)
        )

        if len(request.state_real) != len(state_imag):
            raise ValueError(
                "Real and imaginary state lists must have the same length."
            )

        hamiltonian_imag = (
            request.hamiltonian_imag
            if request.hamiltonian_imag is not None
            else [
                [0.0] * len(row)
                for row in request.hamiltonian_real
            ]
        )

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

        result = simulate_time_evolution(
            state=state,
            hamiltonian=hamiltonian,
            time_start=request.time_start,
            time_end=request.time_end,
            steps=request.steps,
            hbar=request.hbar,
        )

        return {
            "success": True,
            "message": (
                "Quantum time-evolution simulation completed successfully."
            ),
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
