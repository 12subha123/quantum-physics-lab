from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.engine.solver.bloch_sphere_solver import (
    calculate_bloch_state,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Physics"],
)


class BlochSphereRequest(BaseModel):
    theta_degrees: float = Field(
        default=90.0,
        ge=0.0,
        le=180.0,
        description="Polar angle theta in degrees.",
    )

    phi_degrees: float = Field(
        default=0.0,
        ge=0.0,
        le=360.0,
        description="Azimuthal angle phi in degrees.",
    )


@router.post("/bloch-sphere")
def bloch_sphere(
    request: BlochSphereRequest,
):
    try:
        result = calculate_bloch_state(
            theta_degrees=request.theta_degrees,
            phi_degrees=request.phi_degrees,
        )

        return {
            "success": True,
            "message": (
                "Spin-1/2 Bloch sphere calculation "
                "completed successfully."
            ),
            "angles": {
                "theta_degrees": result.theta_degrees,
                "phi_degrees": result.phi_degrees,
                "theta_radians": result.theta_radians,
                "phi_radians": result.phi_radians,
            },
            "quantum_state": {
                "alpha": {
                    "real": result.alpha_real,
                    "imag": result.alpha_imag,
                },
                "beta": {
                    "real": result.beta_real,
                    "imag": result.beta_imag,
                },
            },
            "bloch_coordinates": {
                "x": result.bloch_x,
                "y": result.bloch_y,
                "z": result.bloch_z,
            },
            "measurement_probabilities": {
                "zero": result.probability_zero,
                "one": result.probability_one,
            },
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
