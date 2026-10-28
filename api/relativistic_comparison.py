from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.relativistic_comparison import (
    relativistic_comparison,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Relativistic Quantum Mechanics"],
)


class RelativisticComparisonRequest(BaseModel):
    mass: float = Field(default=1.0, ge=0.0)
    momentum: float = 2.0
    amplitude: float = Field(default=1.0, gt=0.0)
    width: float = Field(default=1.5, gt=0.0)
    domain_length: float = Field(default=20.0, gt=0.0)
    duration: float = Field(default=8.0, gt=0.0)
    points: int = Field(default=128, ge=64, le=256)
    frames: int = Field(default=80, ge=20, le=120)


@router.post("/field-theory/relativistic-comparison")
def run_relativistic_comparison(
    request: RelativisticComparisonRequest,
):
    try:
        return relativistic_comparison(
            mass=request.mass,
            momentum=request.momentum,
            amplitude=request.amplitude,
            width=request.width,
            domain_length=request.domain_length,
            duration=request.duration,
            points=request.points,
            frames=request.frames,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
