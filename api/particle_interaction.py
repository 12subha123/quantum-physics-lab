from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.field_theory.interaction_engine import (
    find_allowed_interactions,
    get_particle,
    list_interactions,
    list_particles,
    particle_summary,
)

router = APIRouter(
    prefix="/api/quantum",
    tags=["Particle Interaction Engine"],
)


class InteractionRequest(BaseModel):
    initial_particles: list[str]
    final_particles: list[str]


@router.get("/field-theory/particles")
def particles():
    return {
        "success": True,
        "particles": list_particles(),
        "summary": particle_summary(),
    }


@router.get("/field-theory/interactions")
def interactions():
    return {
        "success": True,
        "interactions": list_interactions(),
    }


@router.get("/field-theory/particles/{particle_name}")
def particle(particle_name: str):
    try:
        return {
            "success": True,
            "particle": get_particle(particle_name).__dict__,
        }
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/field-theory/find-interactions")
def find_interactions(request: InteractionRequest):
    try:
        return {
            "success": True,
            **find_allowed_interactions(
                initial_particles=request.initial_particles,
                final_particles=request.final_particles,
            ),
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
