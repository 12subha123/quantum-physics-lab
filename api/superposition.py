from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.engine.solver.superposition_solver import (
    calculate_superposition,
    simulate_measurement,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Physics"],
)


class SuperpositionRequest(BaseModel):
    alpha_real: float = Field(default=0.70710678)
    alpha_imag: float = Field(default=0.0)

    beta_real: float = Field(default=0.70710678)
    beta_imag: float = Field(default=0.0)

    shots: int = Field(
        default=1000,
        ge=1,
        le=100000,
    )


@router.post("/superposition")
def superposition(
    request: SuperpositionRequest,
):
    try:
        result = calculate_superposition(
            alpha_real=request.alpha_real,
            alpha_imag=request.alpha_imag,
            beta_real=request.beta_real,
            beta_imag=request.beta_imag,
        )

        measurement = simulate_measurement(
            probability_zero=result.probability_zero,
            shots=request.shots,
        )

        return {
            "success": True,
            "message": (
                "Quantum superposition calculation "
                "completed successfully."
            ),
            "state": {
                "alpha_real": result.alpha_real,
                "alpha_imag": result.alpha_imag,
                "beta_real": result.beta_real,
                "beta_imag": result.beta_imag,
            },
            "magnitudes": {
                "alpha": result.alpha_magnitude,
                "beta": result.beta_magnitude,
            },
            "probabilities": {
                "zero": result.probability_zero,
                "one": result.probability_one,
            },
            "measurement": measurement,
            "normalized": result.normalized,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
