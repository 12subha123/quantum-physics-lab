from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from .feynman_rule_assignment import (
    AssignedFeynmanRules,
)


@dataclass(frozen=True)
class SymbolicAmplitude:
    candidate_id: str
    topology: str
    process: str
    theory: str
    expression: str
    vertex_factors: tuple[str, ...]
    propagator_factors: tuple[str, ...]
    status: str
    reasons: tuple[str, ...]


def _combine_factors(
    vertex_factors: tuple[str, ...],
    propagator_factors: tuple[str, ...],
) -> str:

    factors = [
        factor
        for factor in (
            *vertex_factors,
            *propagator_factors,
        )
        if factor
    ]

    if not factors:
        return "UNRESOLVED_AMPLITUDE"

    return " ".join(
        f"({factor})"
        for factor in factors
    )


def build_symbolic_amplitude(
    rules: AssignedFeynmanRules,
) -> SymbolicAmplitude:

    vertex_factors = tuple(
        vertex.factor
        for vertex in rules.vertices
    )

    propagator_factors = tuple(
        propagator.factor
        for propagator in rules.propagators
    )

    unresolved = [
        factor
        for factor in vertex_factors
        if factor.startswith("UNRESOLVED_VERTEX")
    ]

    if rules.validation_status == "FORBIDDEN":
        return SymbolicAmplitude(
            candidate_id=rules.candidate_id,
            topology=rules.topology,
            process=rules.process,
            theory=rules.theory,
            expression="NOT_PHYSICALLY_ALLOWED",
            vertex_factors=vertex_factors,
            propagator_factors=propagator_factors,
            status="FORBIDDEN",
            reasons=rules.validation_reasons,
        )

    if unresolved:
        return SymbolicAmplitude(
            candidate_id=rules.candidate_id,
            topology=rules.topology,
            process=rules.process,
            theory=rules.theory,
            expression="UNRESOLVED_AMPLITUDE",
            vertex_factors=vertex_factors,
            propagator_factors=propagator_factors,
            status="UNDECIDABLE",
            reasons=(
                "One or more Feynman vertex factors "
                "are not resolved by the Standard Model "
                "vertex catalog.",
            ),
        )

    expression = _combine_factors(
        vertex_factors,
        propagator_factors,
    )

    status = (
        "ALLOWED"
        if rules.validation_status in {None, "ALLOWED"}
        else rules.validation_status
    )

    return SymbolicAmplitude(
        candidate_id=rules.candidate_id,
        topology=rules.topology,
        process=rules.process,
        theory=rules.theory,
        expression=expression,
        vertex_factors=vertex_factors,
        propagator_factors=propagator_factors,
        status=status,
        reasons=rules.validation_reasons,
    )


def symbolic_amplitude_dict(
    amplitude: SymbolicAmplitude,
) -> dict[str, Any]:

    return asdict(amplitude)


def build_symbolic_amplitudes(
    rules_batch,
) -> tuple[SymbolicAmplitude, ...]:

    return tuple(
        build_symbolic_amplitude(rules)
        for rules in rules_batch
    )
