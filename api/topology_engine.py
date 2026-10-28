from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.field_theory.topology_engine import topology_summary


router = APIRouter(
    prefix="/api/quantum/field-theory",
    tags=["Quantum Field Theory"],
)


class TopologyRequest(BaseModel):
    initial_particles: list[str]
    final_particles: list[str]


@router.post("/topologies")
def generate_topologies(request: TopologyRequest):
    try:
        return topology_summary(
            request.initial_particles,
            request.final_particles,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
