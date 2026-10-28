from fastapi import APIRouter, HTTPException
from quantum.field_theory.standard_model_vertices import (
    find_vertices_containing,
    get_vertex,
    list_standard_model_vertices,
    list_vertices_by_theory,
    standard_model_vertex_summary,
)

router = APIRouter(
    prefix="/api/quantum",
    tags=["Standard Model"],
)


@router.get("/field-theory/standard-model/vertices")
def standard_model_vertices():
    return {
        "success": True,
        "vertices": list_standard_model_vertices(),
    }


@router.get("/field-theory/standard-model/vertices/summary")
def standard_model_vertices_summary():
    return standard_model_vertex_summary()


@router.get("/field-theory/standard-model/vertices/theory/{theory}")
def standard_model_vertices_by_theory(theory: str):
    vertices = list_vertices_by_theory(theory)

    if not vertices:
        raise HTTPException(
            status_code=404,
            detail=f"No vertices found for theory: {theory}",
        )

    return {
        "success": True,
        "theory": theory,
        "vertices": vertices,
    }


@router.get("/field-theory/standard-model/vertices/{vertex_id}")
def standard_model_vertex(vertex_id: str):
    try:
        return {
            "success": True,
            "vertex": get_vertex(vertex_id),
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get("/field-theory/standard-model/vertices/particle/{particle_type}")
def standard_model_vertices_by_particle(particle_type: str):
    return {
        "success": True,
        "particle_type": particle_type,
        "vertices": find_vertices_containing(particle_type),
    }
