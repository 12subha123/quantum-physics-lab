from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.engine.solver.measurement_solver import (
    measurement_summary,
    sample_measurement,
)

router = APIRouter(
    prefix="/api/quantum",
    tags=["Measurement"],
)


class MeasurementRequest(BaseModel):
    state_real: list[float]
    state_imag: list[float] | None = None
    shots: int = 100
    seed: int | None = None


@router.post("/measurement")
def perform_measurement(request: MeasurementRequest):
    try:
        if request.state_imag is None:
            state_imag = [0.0] * len(request.state_real)
        else:
            state_imag = request.state_imag

        if len(request.state_real) != len(state_imag):
            raise ValueError(
                "Real and imaginary state vectors must have the same length."
            )

        state = [
            complex(real, imag)
            for real, imag in zip(
                request.state_real,
                state_imag,
            )
        ]

        summary = measurement_summary(state)

        simulation = sample_measurement(
            state,
            shots=request.shots,
            seed=request.seed,
        )

        return {
            "success": True,
            "message": "Quantum measurement completed successfully.",
            **summary,
            "measurement": simulation,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc