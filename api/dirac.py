from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.dirac import (
    dirac_equation_summary,
    simulate_dirac,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Field Theory"],
)


class DiracRequest(BaseModel):
    momentum: float
    mass: float


class DiracSimulationRequest(BaseModel):
    mass: float = Field(default=1.0, ge=0.0)
    amplitude: float = Field(default=1.0, gt=0.0)
    width: float = Field(default=1.5, gt=0.0)
    momentum: float = 2.0
    domain_length: float = Field(default=20.0, gt=0.0)
    duration: float = Field(default=8.0, gt=0.0)
    points: int = Field(default=256, ge=64, le=512)
    frames: int = Field(default=100, ge=20, le=160)


@router.post("/field-theory/dirac")
def calculate_dirac(
    request: DiracRequest,
):
    try:
        if request.mass < 0:
            raise ValueError(
                "Mass must be non-negative."
            )

        result = dirac_equation_summary(
            momentum=request.momentum,
            mass=request.mass,
        )

        return {
            "success": True,
            "message": (
                "Dirac equation calculation "
                "completed successfully."
            ),
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/field-theory/dirac/simulation")
def simulate_dirac_field(
    request: DiracSimulationRequest,
):
    try:
        result = simulate_dirac(
            mass=request.mass,
            amplitude=request.amplitude,
            width=request.width,
            momentum=request.momentum,
            domain_length=request.domain_length,
            duration=request.duration,
            points=request.points,
            frames=request.frames,
        )

        return {
            "success": True,
            "message": (
                "Numerical Dirac wave-packet "
                "simulation completed successfully."
            ),
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
