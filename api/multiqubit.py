from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.engine.solver.multiqubit_solver import (
    create_state,
    state_summary,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Multi-Qubit Systems"],
)


class MultiQubitRequest(BaseModel):
    amplitudes_real: list[float]
    amplitudes_imag: list[float] | None = None


@router.post("/multiqubit")
def analyze_multiqubit(request: MultiQubitRequest):
    try:
        state = create_state(
            request.amplitudes_real,
            request.amplitudes_imag,
        )

        result = state_summary(state)

        return {
            "success": True,
            "message": (
                "Multi-qubit state analysis "
                "completed successfully."
            ),
            **result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
