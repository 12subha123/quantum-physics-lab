from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from quantum.engine.solver.operators_eigenstates_solver import (
    calculate_custom_operator,
    calculate_operator_eigenstates,
)


router = APIRouter(
    prefix="/api/quantum",
    tags=["Quantum Physics"],
)


class OperatorRequest(BaseModel):
    operator: str = "pauli_z"


class CustomOperatorRequest(BaseModel):
    a: float
    b: float
    c: float
    d: float


def format_result(result):
    return {
        "success": True,
        "message": (
            "Operator eigenstate calculation "
            "completed successfully."
        ),
        "operator": result.operator_name,
        "matrix": result.matrix,
        "eigenvalues": result.eigenvalues,
        "eigenvectors": result.eigenvectors,
        "verification": result.verification,
    }


@router.post("/operators-eigenstates")
def operators_eigenstates(
    request: OperatorRequest,
):
    try:
        result = calculate_operator_eigenstates(
            request.operator
        )

        return format_result(result)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/operators-eigenstates/custom")
def custom_operator(
    request: CustomOperatorRequest,
):
    try:
        result = calculate_custom_operator(
            a=request.a,
            b=request.b,
            c=request.c,
            d=request.d,
        )

        return format_result(result)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
