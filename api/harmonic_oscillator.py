from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.engine.solver.harmonic_oscillator_solver import (
    calculate_harmonic_oscillator,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Physics"],
)


class HarmonicOscillatorRequest(BaseModel):
    hbar: float = 1.0
    mass: float = 1.0
    omega: float = 1.0
    x_min: float = -5.0
    x_max: float = 5.0
    points: int = 1000
    num_states: int = 5


@router.post("/harmonic-oscillator")
def harmonic_oscillator(
    request: HarmonicOscillatorRequest,
):
    try:
        result = calculate_harmonic_oscillator(
            hbar=request.hbar,
            mass=request.mass,
            omega=request.omega,
            x_min=request.x_min,
            x_max=request.x_max,
            points=request.points,
            num_states=request.num_states,
        )

        return {
            "success": True,
            "message": (
                "Quantum harmonic oscillator calculation "
                "completed successfully."
            ),
            "simulation_parameters": {
                "hbar": result.hbar,
                "mass": result.mass,
                "omega": result.omega,
                "x_min": result.x_min,
                "x_max": result.x_max,
                "points": result.points,
                "num_states": result.num_states,
            },
            "position": result.position,
            "potential": result.potential,
            "energy_levels": result.energy_levels,
            "wavefunctions": result.wavefunctions,
            "probability_densities": (
                result.probability_densities
            ),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
