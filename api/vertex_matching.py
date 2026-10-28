from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.vertex_matching import (
    find_matching_vertices,
    find_matching_vertices_for_process,
)

router = APIRouter(
    prefix="/api/quantum",
    tags=["Standard Model"],
)


class VertexMatchingRequest(BaseModel):
    particles: list[str] = Field(min_length=1)


class ProcessVertexMatchingRequest(BaseModel):
    initial_particles: list[str] = Field(min_length=1)
    final_particles: list[str] = Field(min_length=1)


@router.post("/field-theory/standard-model/match-vertices")
def match_vertices(request: VertexMatchingRequest):
    try:
        vertices = find_matching_vertices(request.particles)

        return {
            "success": True,
            "particles": request.particles,
            "vertices": vertices,
            "vertex_count": len(vertices),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/field-theory/standard-model/match-process-vertices")
def match_process_vertices(request: ProcessVertexMatchingRequest):
    try:
        vertices = find_matching_vertices_for_process(
            initial_particles=request.initial_particles,
            final_particles=request.final_particles,
        )

        return {
            "success": True,
            "initial_particles": request.initial_particles,
            "final_particles": request.final_particles,
            "vertices": vertices,
            "vertex_count": len(vertices),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
