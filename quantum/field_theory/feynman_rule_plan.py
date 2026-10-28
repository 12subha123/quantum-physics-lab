from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from .oriented_vertex_graph import TreeTopologyCandidate


@dataclass(frozen=True)
class FeynmanVertexRule:
    vertex_instance: str
    catalog_vertex_id: str
    particles: tuple[str, ...]
    theory: str


@dataclass(frozen=True)
class FeynmanPropagatorRule:
    line_id: str
    particle: str
    field_type: str
    vertex_a: str
    vertex_b: str
    orientation: str | None


@dataclass(frozen=True)
class FeynmanRulePlan:
    candidate_id: str
    topology: str
    process: str
    theory: str
    vertices: tuple[FeynmanVertexRule, ...]
    propagators: tuple[FeynmanPropagatorRule, ...]
    fermion_lines: tuple[dict[str, Any], ...]
    validation_status: str | None = None
    validation_reasons: tuple[str, ...] = ()


def build_feynman_rule_plan(
    candidate: TreeTopologyCandidate,
    validation_status: str | None = None,
    validation_reasons: tuple[str, ...] = (),
) -> FeynmanRulePlan:

    vertices = tuple(
        FeynmanVertexRule(
            vertex_instance=vertex.instance_id,
            catalog_vertex_id=vertex.catalog_vertex_id,
            particles=vertex.particles,
            theory=vertex.theory,
        )
        for vertex in candidate.vertices
    )

    propagators = tuple(
        FeynmanPropagatorRule(
            line_id=propagator.line_id,
            particle=propagator.particle,
            field_type=propagator.field_type,
            vertex_a=propagator.vertex_a,
            vertex_b=propagator.vertex_b,
            orientation=propagator.orientation,
        )
        for propagator in candidate.internal_propagators
    )

    fermion_lines = tuple(
        {
            "line_id": line.line_id,
            "family": line.family,
            "incoming_leg": line.incoming_leg,
            "outgoing_leg": line.outgoing_leg,
            "start_vertex": line.start_vertex,
            "end_vertex": line.end_vertex,
            "orientation": line.orientation,
        }
        for line in candidate.fermion_lines
    )

    return FeynmanRulePlan(
        candidate_id=candidate.candidate_id,
        topology=candidate.topology,
        process=candidate.process,
        theory=candidate.theory,
        vertices=vertices,
        propagators=propagators,
        fermion_lines=fermion_lines,
        validation_status=validation_status,
        validation_reasons=validation_reasons,
    )


def feynman_rule_plan_dict(
    plan: FeynmanRulePlan,
) -> dict[str, Any]:
    return asdict(plan)


def build_feynman_rule_plans(
    candidates,
    validation_results=None,
) -> tuple[FeynmanRulePlan, ...]:

    if validation_results is None:
        return tuple(
            build_feynman_rule_plan(candidate)
            for candidate in candidates
        )

    return tuple(
        build_feynman_rule_plan(
            candidate,
            validation_status=result.status,
            validation_reasons=tuple(result.reasons),
        )
        for candidate, result in zip(
            candidates,
            validation_results,
        )
    )
