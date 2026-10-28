from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.propagator import (
    propagator_energy_scan,
    scalar_feynman_propagator,
)

router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Field Theory"],
)


class PropagatorRequest(BaseModel):
    mass: float = Field(default=1.0, ge=0.0)
    energy: float = Field(default=2.0)
    momentum: float = Field(default=1.0)
    epsilon: float = Field(default=1e-3, gt=0.0)


class PropagatorScanRequest(BaseModel):
    mass: float = Field(default=1.0, ge=0.0)
    momentum: float = Field(default=1.0)
    epsilon: float = Field(default=1e-3, gt=0.0)
    points: int = Field(default=101, ge=2, le=1000)
    energy_min: float = 0.0
    energy_max: float = Field(default=4.0, gt=0.0)


@router.post("/field-theory/propagator")
def calculate_propagator(request: PropagatorRequest):
    try:
        return scalar_feynman_propagator(
            mass=request.mass,
            energy=request.energy,
            momentum=request.momentum,
            epsilon=request.epsilon,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/field-theory/propagator/scan")
def calculate_propagator_scan(request: PropagatorScanRequest):
    try:
        return propagator_energy_scan(
            mass=request.mass,
            momentum=request.momentum,
            epsilon=request.epsilon,
            points=request.points,
            energy_min=request.energy_min,
            energy_max=request.energy_max,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
