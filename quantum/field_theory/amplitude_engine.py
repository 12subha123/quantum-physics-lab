from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class AmplitudeTerm:
    diagram_id: str
    topology: str
    theory: str
    factors: tuple[str, ...]
    expression: str


@dataclass(frozen=True)
class AmplitudeConstructionResult:
    process: str
    theory: str
    terms: tuple[AmplitudeTerm, ...]
    total_expression: str
    diagram_count: int
    valid: bool
    errors: tuple[str, ...]


def _get(obj, name, default=None):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _normalise_factors(factors: Iterable[str]) -> tuple[str, ...]:
    return tuple(
        str(factor).strip()
        for factor in factors
        if str(factor).strip()
    )


def _extract_assignments(assignments):
    if hasattr(assignments, "assignments"):
        return list(assignments.assignments)
    return list(assignments)


def _build_term(assignment) -> AmplitudeTerm:
    diagram_id = str(_get(assignment, "diagram_id", "unknown_diagram"))
    topology = str(_get(assignment, "topology", "unknown"))
    theory = str(_get(assignment, "theory", "unknown"))

    vertices = _get(assignment, "vertices", ()) or ()
    propagators = _get(assignment, "propagators", ()) or ()

    factors: list[str] = []

    for vertex in vertices:
        factor = _get(vertex, "factor")
        if factor:
            factors.append(str(factor))

    for propagator in propagators:
        factor = _get(propagator, "factor")
        if factor:
            factors.append(str(factor))

    factors_tuple = _normalise_factors(factors)

    if not factors_tuple:
        expression = "0"
    elif len(factors_tuple) == 1:
        expression = factors_tuple[0]
    else:
        expression = " ".join(f"({factor})" for factor in factors_tuple)

    return AmplitudeTerm(
        diagram_id=diagram_id,
        topology=topology,
        theory=theory,
        factors=factors_tuple,
        expression=expression,
    )


def construct_amplitudes(assignments) -> AmplitudeConstructionResult:
    assignments = _extract_assignments(assignments)

    errors: list[str] = []
    terms: list[AmplitudeTerm] = []

    if not assignments:
        return AmplitudeConstructionResult(
            process="",
            theory="",
            terms=(),
            total_expression="0",
            diagram_count=0,
            valid=False,
            errors=("No diagram rule assignments were supplied.",),
        )

    process_values = {
        str(_get(item, "process", "")).strip()
        for item in assignments
        if str(_get(item, "process", "")).strip()
    }

    theory_values = {
        str(_get(item, "theory", "")).strip()
        for item in assignments
        if str(_get(item, "theory", "")).strip()
    }

    if len(process_values) > 1:
        errors.append("Assignments contain multiple processes.")

    if len(theory_values) > 1:
        errors.append("Assignments contain multiple theories.")

    for assignment in assignments:
        assignment_valid = bool(_get(assignment, "valid", False))

        if not assignment_valid:
            errors.append(
                f"Diagram {_get(assignment, 'diagram_id', 'unknown')} "
                "has invalid Feynman-rule assignment."
            )
            continue

        terms.append(_build_term(assignment))

    process = next(iter(process_values), "")
    theory = next(iter(theory_values), "")

    if not terms:
        errors.append("No valid amplitude terms could be constructed.")

    if errors:
        valid = False
    else:
        valid = True

    if terms:
        total_expression = " + ".join(
            f"M_{index + 1}[{term.expression}]"
            for index, term in enumerate(terms)
        )
    else:
        total_expression = "0"

    return AmplitudeConstructionResult(
        process=process,
        theory=theory,
        terms=tuple(terms),
        total_expression=total_expression,
        diagram_count=len(assignments),
        valid=valid,
        errors=tuple(errors),
    )


def amplitude_construction_summary(assignments):
    result = construct_amplitudes(assignments)

    return {
        "success": True,
        "valid": result.valid,
        "process": result.process,
        "theory": result.theory,
        "diagram_count": result.diagram_count,
        "term_count": len(result.terms),
        "terms": [
            {
                "diagram_id": term.diagram_id,
                "topology": term.topology,
                "theory": term.theory,
                "factors": list(term.factors),
                "expression": term.expression,
            }
            for term in result.terms
        ],
        "total_expression": result.total_expression,
        "errors": list(result.errors),
        "scientific_scope": (
            "Tree-level symbolic amplitude construction from validated "
            "Feynman diagrams. This layer constructs diagram contributions "
            "and their sum but does not yet perform spinor contractions, "
            "polarization sums, color algebra, phase-space integration, "
            "loop corrections, or renormalization."
        ),
    }
