from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ExternalSpinor:
    particle: str
    momentum: str
    role: str
    object: str


@dataclass(frozen=True)
class SymbolicFactor:
    kind: str
    expression: str


@dataclass(frozen=True)
class SymbolicAmplitudeTerm:
    diagram_id: str
    topology: str
    theory: str
    external_spinors: tuple[ExternalSpinor, ...]
    factors: tuple[SymbolicFactor, ...]
    expression: str


@dataclass(frozen=True)
class SymbolicAmplitudeResult:
    process: str
    theory: str
    terms: tuple[SymbolicAmplitudeTerm, ...]
    total_expression: str
    valid: bool
    errors: tuple[str, ...]


def _get(obj, name, default=None):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _normalise(value: str) -> str:
    return str(value).strip().lower().replace("_", "-")


_FERMIONS = {
    "electron",
    "positron",
    "muon",
    "antimuon",
    "tau",
    "antitau",
    "up",
    "anti-up",
    "down",
    "anti-down",
    "strange",
    "anti-strange",
}


def _is_fermion(particle: str) -> bool:
    return _normalise(particle) in _FERMIONS


def _spinor_object(particle: str, role: str) -> str:
    particle = _normalise(particle)
    role = _normalise(role)

    if particle.startswith("anti-") or particle in {
        "positron",
        "antimuon",
        "antitau",
    }:
        return "v" if role == "initial" else "vbar"

    return "ubar" if role == "outgoing" else "u"


def _build_spinor(leg) -> ExternalSpinor | None:
    particle = str(_get(leg, "particle", ""))
    role = str(_get(leg, "role", ""))
    momentum = str(_get(leg, "momentum", "p"))

    if not _is_fermion(particle):
        return None

    obj = _spinor_object(particle, role)

    if obj in {"ubar", "vbar"}:
        expression = f"{obj}({momentum})"
    else:
        expression = f"{obj}({momentum})"

    return ExternalSpinor(
        particle=particle,
        momentum=momentum,
        role=role,
        object=expression,
    )


def _factor_kind(factor: str) -> str:
    text = factor.lower()

    if "gamma" in text:
        return "vertex"

    if "propagator" in text or "q^2" in text:
        return "propagator"

    if "epsilon" in text:
        return "regulator"

    if "g_" in text:
        return "lorentz_metric"

    return "vertex_or_coupling"


def _build_factors(assignment) -> tuple[SymbolicFactor, ...]:
    result: list[SymbolicFactor] = []

    vertices = _get(assignment, "vertices", ()) or ()
    propagators = _get(assignment, "propagators", ()) or ()

    for vertex in vertices:
        factor = str(_get(vertex, "factor", "")).strip()
        if factor:
            result.append(
                SymbolicFactor(
                    kind=_factor_kind(factor),
                    expression=factor,
                )
            )

    for propagator in propagators:
        factor = str(_get(propagator, "factor", "")).strip()
        if factor:
            result.append(
                SymbolicFactor(
                    kind="propagator",
                    expression=factor,
                )
            )

    return tuple(result)


def _spinor_chain(spinors: tuple[ExternalSpinor, ...]) -> str:
    if not spinors:
        return ""

    return " ".join(spinor.object for spinor in spinors)


def _construct_expression(
    spinors: tuple[ExternalSpinor, ...],
    factors: tuple[SymbolicFactor, ...],
) -> str:
    pieces: list[str] = []

    spinor_text = _spinor_chain(spinors)

    if spinor_text:
        pieces.append(spinor_text)

    pieces.extend(
        f"({factor.expression})"
        for factor in factors
    )

    if not pieces:
        return "0"

    return " ".join(pieces)


def construct_symbolic_amplitude_term(assignment) -> SymbolicAmplitudeTerm:
    diagram_id = str(_get(assignment, "diagram_id", "unknown"))
    topology = str(_get(assignment, "topology", "unknown"))
    theory = str(_get(assignment, "theory", "unknown"))

    external_legs = _get(assignment, "external_legs", ()) or ()

    spinors = tuple(
        spinor
        for leg in external_legs
        if (spinor := _build_spinor(leg)) is not None
    )

    factors = _build_factors(assignment)
    expression = _construct_expression(spinors, factors)

    return SymbolicAmplitudeTerm(
        diagram_id=diagram_id,
        topology=topology,
        theory=theory,
        external_spinors=spinors,
        factors=factors,
        expression=expression,
    )


def _extract_assignments(assignments) -> list:
    if hasattr(assignments, "assignments"):
        return list(assignments.assignments)

    return list(assignments)


def construct_symbolic_amplitude(assignments) -> SymbolicAmplitudeResult:
    assignments = _extract_assignments(assignments)

    if not assignments:
        return SymbolicAmplitudeResult(
            process="",
            theory="",
            terms=(),
            total_expression="0",
            valid=False,
            errors=("No Feynman-rule assignments supplied.",),
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

    errors: list[str] = []

    if len(process_values) > 1:
        errors.append("Assignments contain multiple processes.")

    if len(theory_values) > 1:
        errors.append("Assignments contain multiple theories.")

    terms: list[SymbolicAmplitudeTerm] = []

    for assignment in assignments:
        if not bool(_get(assignment, "valid", False)):
            errors.append(
                f"Diagram {_get(assignment, 'diagram_id', 'unknown')} "
                "has an invalid Feynman-rule assignment."
            )
            continue

        terms.append(
            construct_symbolic_amplitude_term(assignment)
        )

    process = next(iter(process_values), "")
    theory = next(iter(theory_values), "")

    if not terms:
        errors.append("No valid symbolic amplitude terms were constructed.")

    if errors:
        total = "0"
    elif len(terms) == 1:
        total = terms[0].expression
    else:
        total = " + ".join(
            f"M_{index + 1} = {term.expression}"
            for index, term in enumerate(terms)
        )

    return SymbolicAmplitudeResult(
        process=process,
        theory=theory,
        terms=tuple(terms),
        total_expression=total,
        valid=not errors,
        errors=tuple(errors),
    )


def symbolic_amplitude_summary(assignments):
    result = construct_symbolic_amplitude(assignments)

    return {
        "success": True,
        "valid": result.valid,
        "process": result.process,
        "theory": result.theory,
        "term_count": len(result.terms),
        "terms": [
            {
                "diagram_id": term.diagram_id,
                "topology": term.topology,
                "theory": term.theory,
                "external_spinors": [
                    {
                        "particle": spinor.particle,
                        "momentum": spinor.momentum,
                        "role": spinor.role,
                        "object": spinor.object,
                    }
                    for spinor in term.external_spinors
                ],
                "factors": [
                    {
                        "kind": factor.kind,
                        "expression": factor.expression,
                    }
                    for factor in term.factors
                ],
                "expression": term.expression,
            }
            for term in result.terms
        ],
        "total_expression": result.total_expression,
        "errors": list(result.errors),
        "scientific_scope": (
            "Tree-level symbolic amplitude representation with external "
            "fermion spinors and assigned vertex/propagator factors. "
            "This is an intermediate symbolic layer: explicit Lorentz "
            "index contraction, spinor multiplication, polarization "
            "sums, color algebra, and numerical matrix-element "
            "evaluation are not yet performed."
        ),
    }
