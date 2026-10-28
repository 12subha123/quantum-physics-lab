from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.feynman_rules import (
    interaction_summary,
    phi4_tree_level_2_to_2,
    phi4_vertex,
)

router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Field Theory"],
)


class FeynmanRuleRequest(BaseModel):
    lambda_coupling: float = Field(
        default=1.0,
        ge=0.0,
    )


@router.post("/field-theory/feynman-rules")
def calculate_feynman_rules(request: FeynmanRuleRequest):
    try:
        return interaction_summary(
            lam=request.lambda_coupling,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/field-theory/feynman-rules/vertex")
def calculate_phi4_vertex(request: FeynmanRuleRequest):
    try:
        return phi4_vertex(
            lam=request.lambda_coupling,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/field-theory/feynman-rules/scattering")
def calculate_phi4_scattering(request: FeynmanRuleRequest):
    try:
        return phi4_tree_level_2_to_2(
            lam=request.lambda_coupling,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
