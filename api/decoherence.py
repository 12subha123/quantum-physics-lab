from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.engine.solver.decoherence_solver import (
    decoherence_summary,
    simulate_dephasing,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Decoherence"],
)


class DecoherenceRequest(BaseModel):
    density_matrix: list[list[complex]]
    time: float
    decoherence_rate: float


class DecoherenceSimulationRequest(BaseModel):
    density_matrix: list[list[complex]]
    time_start: float
    time_end: float
    steps: int
    decoherence_rate: float


@router.post("/decoherence")
def analyze_decoherence(
    request: DecoherenceRequest,
):
    try:
        density_matrix = [
            [
                complex(value)
                for value in row
            ]
            for row in request.density_matrix
        ]

        result = decoherence_summary(
            density_matrix,
            request.time,
            request.decoherence_rate,
        )

        return {
            "success": True,
            "message": (
                "Decoherence calculation "
                "completed successfully."
            ),
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/decoherence/simulation")
def simulate_decoherence(
    request: DecoherenceSimulationRequest,
):
    try:
        density_matrix = [
            [
                complex(value)
                for value in row
            ]
            for row in request.density_matrix
        ]

        result = simulate_dephasing(
            density_matrix,
            request.time_start,
            request.time_end,
            request.steps,
            request.decoherence_rate,
        )

        return {
            "success": True,
            "message": (
                "Decoherence simulation "
                "completed successfully."
            ),
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc