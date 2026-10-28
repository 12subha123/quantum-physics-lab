from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.engine.solver.entanglement_solver import (
    BELL_STATES,
    analyze_bell_state,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Entanglement"],
)


class EntanglementRequest(BaseModel):
    state_name: str = "phi_plus"


@router.get("/entanglement/states")
def available_bell_states():
    return {
        "success": True,
        "states": [
            {
                "name": name,
                "label": label,
            }
            for name, label in BELL_STATES.items()
        ],
    }


@router.post("/entanglement")
def analyze_entanglement(request: EntanglementRequest):
    try:
        result = analyze_bell_state(
            request.state_name
        )

        return {
            "success": True,
            "message": "Bell-state entanglement analysis completed successfully.",
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
