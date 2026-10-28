from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.path_integral import (
    simulate_euclidean_path_integral,
)

router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Field Theory"],
)


class PathIntegralRequest(BaseModel):
    mass: float = Field(default=1.0, ge=0.0)
    coupling: float = Field(default=1.0, ge=0.0)
    lattice_points: int = Field(default=32, ge=4, le=512)
    lattice_spacing: float = Field(default=0.25, gt=0.0)
    sweeps: int = Field(default=2000, ge=1, le=100000)
    thermalization: int = Field(default=500, ge=0)
    step_size: float = Field(default=1.0, gt=0.0)
    seed: int = Field(default=1234)


@router.post("/field-theory/path-integral")
def path_integral(request: PathIntegralRequest):
    if request.thermalization >= request.sweeps:
        raise HTTPException(
            status_code=400,
            detail="Thermalization must be smaller than sweeps.",
        )

    try:
        return simulate_euclidean_path_integral(
            mass=request.mass,
            coupling=request.coupling,
            lattice_points=request.lattice_points,
            lattice_spacing=request.lattice_spacing,
            sweeps=request.sweeps,
            thermalization=request.thermalization,
            step_size=request.step_size,
            seed=request.seed,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
