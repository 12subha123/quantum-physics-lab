from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from quantum.field_theory.fock_space import (
    fock_operator_action,
    fock_space_summary,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Field Theory"],
)


class FockSpaceRequest(BaseModel):
    mass: float = Field(default=1.0, ge=0.0)
    modes: int = Field(default=8, ge=1, le=32)
    box_length: float = Field(default=20.0, gt=0.0)
    occupation_numbers: list[int] | None = None
    operator: str | None = None
    operator_mode: int | None = Field(
        default=None,
        ge=0,
    )


@router.post("/field-theory/fock-space")
def calculate_fock_space(request: FockSpaceRequest):
    try:
        occupation_numbers = request.occupation_numbers

        if occupation_numbers is None:
            occupation_numbers = [0] * request.modes

        if len(occupation_numbers) != request.modes:
            raise ValueError(
                "The number of occupation values must equal "
                "the number of modes."
            )

        if any(
            n < 0 or int(n) != n
            for n in occupation_numbers
        ):
            raise ValueError(
                "Occupation numbers must be "
                "non-negative integers."
            )

        result = fock_space_summary(
            mass=request.mass,
            modes=request.modes,
            box_length=request.box_length,
            occupation_numbers=occupation_numbers,
        )

        if request.operator is not None:
            if request.operator_mode is None:
                raise ValueError(
                    "operator_mode is required when "
                    "an operator is selected."
                )

            result["operator_action"] = (
                fock_operator_action(
                    occupation_numbers=occupation_numbers,
                    mode=request.operator_mode,
                    operator=request.operator,
                )
            )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
