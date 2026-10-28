from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.canonical_quantization import (
    scalar_mode_quantization,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Field Theory"],
)


class CanonicalQuantizationRequest(BaseModel):
    mass: float = Field(default=1.0, ge=0.0)
    modes: int = Field(default=8, ge=1, le=32)
    box_length: float = Field(default=20.0, gt=0.0)
    occupation_numbers: list[int] | None = None


@router.post("/field-theory/canonical-quantization")
def canonical_quantization(
    request: CanonicalQuantizationRequest,
):
    try:
        occupations = request.occupation_numbers

        if occupations is None:
            occupations = [0] * request.modes

        return scalar_mode_quantization(
            mass=request.mass,
            modes=request.modes,
            box_length=request.box_length,
            occupation_numbers=occupations,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
