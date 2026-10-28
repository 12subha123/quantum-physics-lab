import sympy as sp

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.klein_gordon_simulation import (
    simulate_klein_gordon,
)
from quantum.field_theory.lagrangian import (
    klein_gordon_equation,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Field Theory"],
)


class KleinGordonRequest(BaseModel):
    mass: float


class KleinGordonSimulationRequest(BaseModel):
    mass: float = Field(default=1.0, ge=0.0)
    amplitude: float = Field(default=1.0, gt=0.0)
    width: float = Field(default=1.5, gt=0.0)
    wavenumber: float = Field(default=2.0, ge=0.0)
    domain_length: float = Field(default=20.0, gt=0.0)
    duration: float = Field(default=8.0, gt=0.0)
    points: int = Field(default=201, ge=51, le=401)
    frames: int = Field(default=100, ge=20, le=160)


@router.post("/field-theory/klein-gordon")
def calculate_klein_gordon(
    request: KleinGordonRequest,
):
    try:
        if request.mass < 0:
            raise ValueError(
                "Mass must be non-negative."
            )

        t, x = sp.symbols("t x")
        phi = sp.Function("phi")(t, x)

        equation = klein_gordon_equation(
            field=phi,
            mass=sp.Float(request.mass),
            time_symbol=t,
            space_symbol=x,
        )

        return {
            "success": True,
            "message": (
                "Klein-Gordon field calculation "
                "completed successfully."
            ),
            "mass": request.mass,
            "coordinates": ["t", "x"],
            "equation": str(equation),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/field-theory/klein-gordon/simulation")
def simulate_klein_gordon_field(
    request: KleinGordonSimulationRequest,
):
    try:
        result = simulate_klein_gordon(
            mass=request.mass,
            amplitude=request.amplitude,
            width=request.width,
            wavenumber=request.wavenumber,
            domain_length=request.domain_length,
            duration=request.duration,
            points=request.points,
            frames=request.frames,
        )

        return {
            "success": True,
            "message": (
                "Numerical Klein-Gordon field "
                "simulation completed successfully."
            ),
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
