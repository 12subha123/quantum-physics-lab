from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.field_theory.feynman_diagram_generator import (
    generate_feynman_diagrams,
)

router = APIRouter(
    prefix="/api/quantum",
    tags=["Feynman Diagram Generator"],
)


class FeynmanDiagramRequest(BaseModel):
    initial_particles: list[str]
    final_particles: list[str]


@router.post("/field-theory/feynman-diagrams")
def generate_diagrams(request: FeynmanDiagramRequest):
    try:
        return generate_feynman_diagrams(
            initial_particles=request.initial_particles,
            final_particles=request.final_particles,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
