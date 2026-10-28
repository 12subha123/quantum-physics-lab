from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from .feynman_rule_plan import FeynmanRulePlan
from .standard_model_vertices import STANDARD_MODEL_VERTICES


@dataclass(frozen=True)
class AssignedVertexRule:
    vertex_instance: str
    catalog_vertex_id: str
    particles: tuple[str, ...]
    theory: str
    factor: str
    coupling: str | None = None


@dataclass(frozen=True)
class AssignedPropagatorRule:
    line_id: str
    particle: str
    field_type: str
    factor: str


@dataclass(frozen=True)
class AssignedFeynmanRules:
    candidate_id: str
    topology: str
    process: str
    theory: str
    vertices: tuple[AssignedVertexRule, ...]
    propagators: tuple[AssignedPropagatorRule, ...]
    validation_status: str | None
    validation_reasons: tuple[str, ...]


def _catalog_rule_map() -> dict[str, Any]:
    return {
        vertex.vertex_id: vertex
        for vertex in STANDARD_MODEL_VERTICES
    }


def _vertex_factor(vertex: Any) -> str:
    for attribute in (
        "factor",
        "feynman_rule",
        "rule",
        "interaction",
    ):
        value = getattr(vertex, attribute, None)

        if value is not None:
            return str(value)

    return f"VERTEX[{vertex.vertex_id}]"


def _vertex_coupling(vertex: Any) -> str | None:
    for attribute in (
        "coupling",
        "coupling_constant",
        "g",
    ):
        value = getattr(vertex, attribute, None)

        if value is not None:
            return str(value)

    return None


def _propagator_factor(
    particle: str,
    field_type: str,
) -> str:

    particle_name = str(particle).lower()
    field_name = str(field_type).lower()

    if particle_name in {"photon", "gluon", "z"}:
        return f"i D_{{{particle_name}}}(q)"

    if particle_name in {"w_plus", "w_minus"}:
        return f"i D_{{{particle_name}}}(q)"

    if particle_name == "higgs":
        return "i D_H(q)"

    if "fermion" in field_name or particle_name in {
        "electron",
        "positron",
        "muon",
        "antimuon",
        "tau",
        "antitau",
        "up",
        "down",
        "strange",
        "charm",
        "bottom",
        "top",
        "anti-up",
        "anti-down",
        "anti-strange",
        "anti-charm",
        "anti-bottom",
        "anti-top",
    }:
        return f"i S_{{{particle_name}}}(q)"

    return f"i D_{{{particle_name}}}(q)"


def assign_feynman_rules(
    plan: FeynmanRulePlan,
) -> AssignedFeynmanRules:

    catalog = _catalog_rule_map()

    assigned_vertices = []

    for vertex in plan.vertices:

        catalog_vertex = catalog.get(
            vertex.catalog_vertex_id
        )

        if catalog_vertex is None:
            factor = (
                f"UNRESOLVED_VERTEX"
                f"[{vertex.catalog_vertex_id}]"
            )
            coupling = None
        else:
            factor = _vertex_factor(catalog_vertex)
            coupling = _vertex_coupling(catalog_vertex)

        assigned_vertices.append(
            AssignedVertexRule(
                vertex_instance=vertex.vertex_instance,
                catalog_vertex_id=vertex.catalog_vertex_id,
                particles=vertex.particles,
                theory=vertex.theory,
                factor=factor,
                coupling=coupling,
            )
        )

    assigned_propagators = tuple(
        AssignedPropagatorRule(
            line_id=propagator.line_id,
            particle=propagator.particle,
            field_type=propagator.field_type,
            factor=_propagator_factor(
                propagator.particle,
                propagator.field_type,
            ),
        )
        for propagator in plan.propagators
    )

    return AssignedFeynmanRules(
        candidate_id=plan.candidate_id,
        topology=plan.topology,
        process=plan.process,
        theory=plan.theory,
        vertices=tuple(assigned_vertices),
        propagators=assigned_propagators,
        validation_status=plan.validation_status,
        validation_reasons=plan.validation_reasons,
    )


def assigned_feynman_rules_dict(
    rules: AssignedFeynmanRules,
) -> dict[str, Any]:

    return asdict(rules)


def assign_feynman_rules_batch(
    plans,
) -> tuple[AssignedFeynmanRules, ...]:

    return tuple(
        assign_feynman_rules(plan)
        for plan in plans
    )
