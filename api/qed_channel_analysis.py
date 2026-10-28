from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.qed_channel_analysis import (
    analyze_qed_channels,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Electrodynamics"],
)


class QEDChannelAnalysisRequest(BaseModel):
    process: str
    sqrt_s: float = Field(
        default=10.0,
        gt=0.0,
    )
    scattering_angle: float = Field(
        default=1.5707963267948966,
        gt=0.0,
        lt=3.141592653589793,
    )


@router.post("/field-theory/qed-channel-analysis")
def qed_channel_analysis(
    request: QEDChannelAnalysisRequest,
):
    try:
        return analyze_qed_channels(
            process=request.process,
            sqrt_s=request.sqrt_s,
            scattering_angle=request.scattering_angle,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
