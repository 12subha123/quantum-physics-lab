from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.qed_amplitude import (
    calculate_qed_amplitude,
    calculate_qed_angular_scan,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Electrodynamics"],
)


class QEDAmplitudeRequest(BaseModel):
    process: str
    sqrt_s: float = Field(default=10.0, gt=0.0)
    scattering_angle: float = Field(
        default=1.5707963267948966,
        gt=0.0,
        lt=3.141592653589793,
    )


class QEDAngularScanRequest(BaseModel):
    process: str
    sqrt_s: float = Field(default=10.0, gt=0.0)
    points: int = Field(default=91, ge=8, le=721)


@router.post("/field-theory/qed-amplitude")
def qed_amplitude(request: QEDAmplitudeRequest):
    try:
        return calculate_qed_amplitude(
            process=request.process,
            sqrt_s=request.sqrt_s,
            scattering_angle=request.scattering_angle,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/field-theory/qed-amplitude/scan")
def qed_amplitude_scan(request: QEDAngularScanRequest):
    try:
        return calculate_qed_angular_scan(
            process=request.process,
            sqrt_s=request.sqrt_s,
            points=request.points,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
