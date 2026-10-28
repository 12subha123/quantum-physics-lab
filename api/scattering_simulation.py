from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.scattering_simulation import (
    simulate_phi4_scattering,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Field Theory"],
)


class ScatteringSimulationRequest(BaseModel):
    mass: float = Field(default=1.0, ge=0.0)
    sqrt_s: float = Field(default=5.0, gt=0.0)
    lambda_coupling: float = Field(default=1.0, ge=0.0)
    angular_points: int = Field(default=73, ge=8, le=720)


@router.post("/field-theory/scattering-simulation")
def scattering_simulation(
    request: ScatteringSimulationRequest,
):
    try:
        return simulate_phi4_scattering(
            mass=request.mass,
            sqrt_s=request.sqrt_s,
            lam=request.lambda_coupling,
            angular_points=request.angular_points,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
