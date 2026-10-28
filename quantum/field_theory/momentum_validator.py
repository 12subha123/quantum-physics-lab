from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .numerical_kinematics import FourVector


@dataclass(frozen=True)
class MomentumConservationResult:
    valid: bool
    numerical: bool
    total_incoming: tuple[float, float, float, float] | None
    total_outgoing: tuple[float, float, float, float] | None
    residual: tuple[float, float, float, float] | None
    max_residual: float | None
    symbolic_equation: str
    errors: tuple[str, ...]


def _vector_tuple(vector: FourVector) -> tuple[float, float, float, float]:
    return (
        float(vector.E),
        float(vector.px),
        float(vector.py),
        float(vector.pz),
    )


def _add_vectors(vectors: Sequence[FourVector]) -> FourVector:
    result = FourVector(0.0, 0.0, 0.0, 0.0)

    for vector in vectors:
        result = result + vector

    return result


def _residual(
    incoming: FourVector,
    outgoing: FourVector,
) -> tuple[float, float, float, float]:
    difference = incoming - outgoing
    return _vector_tuple(difference)


def validate_four_momentum_conservation(
    incoming: Sequence[FourVector],
    outgoing: Sequence[FourVector],
    tolerance: float = 1e-9,
) -> MomentumConservationResult:
    if tolerance <= 0:
        raise ValueError("Tolerance must be positive.")

    if not incoming:
        raise ValueError("At least one incoming four-vector is required.")

    if not outgoing:
        raise ValueError("At least one outgoing four-vector is required.")

    total_incoming = _add_vectors(incoming)
    total_outgoing = _add_vectors(outgoing)

    residual = _residual(total_incoming, total_outgoing)
    max_residual = max(abs(value) for value in residual)

    symbolic_equation = (
        "Σ p_in^μ = Σ p_out^μ"
    )

    return MomentumConservationResult(
        valid=max_residual <= tolerance,
        numerical=True,
        total_incoming=_vector_tuple(total_incoming),
        total_outgoing=_vector_tuple(total_outgoing),
        residual=residual,
        max_residual=max_residual,
        symbolic_equation=symbolic_equation,
        errors=()
        if max_residual <= tolerance
        else (
            "Four-momentum conservation failed within the supplied tolerance.",
        ),
    )


def build_symbolic_conservation_equation(
    incoming_labels: Sequence[str],
    outgoing_labels: Sequence[str],
) -> str:
    if not incoming_labels:
        raise ValueError("At least one incoming momentum label is required.")

    if not outgoing_labels:
        raise ValueError("At least one outgoing momentum label is required.")

    incoming = " + ".join(str(label) for label in incoming_labels)
    outgoing = " + ".join(str(label) for label in outgoing_labels)

    return f"{incoming} = {outgoing}"


def validate_symbolic_momentum_flow(
    incoming_labels: Sequence[str],
    outgoing_labels: Sequence[str],
) -> MomentumConservationResult:
    equation = build_symbolic_conservation_equation(
        incoming_labels,
        outgoing_labels,
    )

    return MomentumConservationResult(
        valid=True,
        numerical=False,
        total_incoming=None,
        total_outgoing=None,
        residual=None,
        max_residual=None,
        symbolic_equation=equation,
        errors=(),
    )


def momentum_conservation_summary(
    incoming: Sequence[FourVector] | None = None,
    outgoing: Sequence[FourVector] | None = None,
    incoming_labels: Sequence[str] | None = None,
    outgoing_labels: Sequence[str] | None = None,
    tolerance: float = 1e-9,
):
    if incoming is not None or outgoing is not None:
        if incoming is None or outgoing is None:
            raise ValueError(
                "Both incoming and outgoing four-vectors are required."
            )

        result = validate_four_momentum_conservation(
            incoming,
            outgoing,
            tolerance=tolerance,
        )
    else:
        if incoming_labels is None or outgoing_labels is None:
            raise ValueError(
                "Provide either numerical four-vectors or symbolic momentum labels."
            )

        result = validate_symbolic_momentum_flow(
            incoming_labels,
            outgoing_labels,
        )

    return {
        "success": True,
        "valid": result.valid,
        "numerical": result.numerical,
        "total_incoming": result.total_incoming,
        "total_outgoing": result.total_outgoing,
        "residual": result.residual,
        "max_residual": result.max_residual,
        "symbolic_equation": result.symbolic_equation,
        "errors": list(result.errors),
        "scientific_scope": (
            "Universal momentum-conservation validation for arbitrary "
            "N-to-M processes. Numerical validation checks four-vector "
            "conservation within tolerance; symbolic validation records "
            "the required conservation equation. This layer does not "
            "generate phase space or calculate matrix elements."
        ),
    }
