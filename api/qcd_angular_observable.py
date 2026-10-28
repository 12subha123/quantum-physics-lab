from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.qcd_angular_observables import (
    integrate_qcd_angular_cross_section,
)


router = APIRouter(
    prefix="/api/quantum/field-theory",
    tags=["Quantum Chromodynamics"],
)


class QCDAngularObservableRequest(BaseModel):
    sqrt_s: float = Field(default=10.0, gt=0.0)
    alpha_s: float = Field(default=0.118, gt=0.0)
    angular_cut: float = Field(default=0.1, gt=0.0)
    points: int = Field(default=200, ge=2, le=2000)


@router.post("/qcd/angular-observable")
def qcd_angular_observable(
    request: QCDAngularObservableRequest,
):
    try:
        result = integrate_qcd_angular_cross_section(
            sqrt_s=request.sqrt_s,
            alpha_s=request.alpha_s,
            angular_cut=request.angular_cut,
            points=request.points,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    if not result.valid:
        raise HTTPException(
            status_code=400,
            detail=list(result.errors),
        )

    return {
        "success": result.success,
        "valid": result.valid,
        "process": result.process,
        "sqrt_s": result.sqrt_s,
        "alpha_s": result.alpha_s,
        "angular_cut": result.angular_cut,
        "point_count": len(result.points),
        "total_cross_section": result.total_cross_section,
        "points": [
            {
                "theta": point.theta,
                "cos_theta": point.cos_theta,
                "s": point.s,
                "t": point.t,
                "u": point.u,
                "matrix_element_squared": point.matrix_element_squared,
                "differential_cross_section": point.differential_cross_section,
            }
            for point in result.points
        ],
        "errors": list(result.errors),
        "scientific_scope": result.scientific_scope,
    }
