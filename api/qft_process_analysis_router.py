from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from quantum.field_theory.qft_process_analysis_engine import (
    analyze_process,
    process_analysis_dict,
)


router = APIRouter(
    prefix="/api/quantum/field-theory",
    tags=["Quantum Field Theory"],
)


class QFTProcessRequest(BaseModel):
    incoming: list[str] = Field(
        min_length=1,
        description="Incoming particles."
    )
    outgoing: list[str] = Field(
        min_length=1,
        description="Outgoing particles."
    )
    max_vertices: int = Field(
        default=4,
        ge=1,
        le=6,
    )


@router.post("/analyze-process")
def analyze_qft_process(
    request: QFTProcessRequest,
):
    result = analyze_process(
        incoming=tuple(request.incoming),
        outgoing=tuple(request.outgoing),
        max_vertices=request.max_vertices,
    )

    return process_analysis_dict(result)
