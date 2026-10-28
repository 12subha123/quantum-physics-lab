from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.engine.solver.density_matrix_solver import (
    density_matrix_from_probabilities,
    density_matrix_summary,
    pure_state_density_matrix,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Density Matrices"],
)


class PureStateDensityRequest(BaseModel):
    state_real: list[float]
    state_imag: list[float] | None = None


class MixedStateRequest(BaseModel):
    states_real: list[list[float]]
    states_imag: list[list[float]] | None = None
    probabilities: list[float]


@router.post("/density-matrix/pure")
def create_pure_density_matrix(
    request: PureStateDensityRequest,
):
    try:
        state_imag = (
            request.state_imag
            if request.state_imag is not None
            else [0.0] * len(request.state_real)
        )

        if len(request.state_real) != len(state_imag):
            raise ValueError(
                "Real and imaginary state lists must have "
                "the same length."
            )

        state = [
            complex(real, imag)
            for real, imag in zip(
                request.state_real,
                state_imag,
            )
        ]

        density_matrix = pure_state_density_matrix(
            state
        )

        return {
            "success": True,
            "message": (
                "Pure-state density matrix "
                "calculated successfully."
            ),
            **density_matrix_summary(
                density_matrix
            ),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/density-matrix/mixed")
def create_mixed_density_matrix(
    request: MixedStateRequest,
):
    try:
        if len(request.states_real) == 0:
            raise ValueError(
                "At least one state is required."
            )

        if len(request.states_real) != len(
            request.probabilities
        ):
            raise ValueError(
                "States and probabilities must have "
                "the same length."
            )

        if request.states_imag is None:
            states_imag = [
                [0.0] * len(state)
                for state in request.states_real
            ]
        else:
            states_imag = request.states_imag

        if len(request.states_real) != len(
            states_imag
        ):
            raise ValueError(
                "Real and imaginary state lists must "
                "have the same number of states."
            )

        states = []

        for real_state, imag_state in zip(
            request.states_real,
            states_imag,
        ):
            if len(real_state) != len(imag_state):
                raise ValueError(
                    "Real and imaginary amplitudes must "
                    "have the same length for every state."
                )

            state = [
                complex(real, imag)
                for real, imag in zip(
                    real_state,
                    imag_state,
                )
            ]

            states.append(state)

        density_matrix = (
            density_matrix_from_probabilities(
                states,
                request.probabilities,
            )
        )

        return {
            "success": True,
            "message": (
                "Mixed-state density matrix "
                "calculated successfully."
            ),
            **density_matrix_summary(
                density_matrix
            ),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc