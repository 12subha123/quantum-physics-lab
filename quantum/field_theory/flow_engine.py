from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class FermionFlow:
    line_id: str
    particle: str
    arrow_direction: str
    from_vertex: str
    to_vertex: str
    momentum: str
    flow_type: str


@dataclass(frozen=True)
class BosonFlow:
    line_id: str
    particle: str
    from_vertex: str
    to_vertex: str
    momentum: str
    field_type: str


@dataclass(frozen=True)
class ExternalMomentum:
    leg_id: str
    particle: str
    role: str
    momentum: str
    arrow_direction: str


@dataclass(frozen=True)
class FlowAssignment:
    diagram_id: str
    process: str
    topology: str
    fermion_flows: tuple[FermionFlow, ...]
    boson_flows: tuple[BosonFlow, ...]
    external_momenta: tuple[ExternalMomentum, ...]
    valid: bool
    errors: tuple[str, ...]


_FERMION_BASES = {
    "electron": "electron",
    "positron": "electron",
    "muon": "muon",
    "antimuon": "muon",
    "tau": "tau",
    "antitau": "tau",
    "up": "up",
    "anti-up": "up",
    "down": "down",
    "anti-down": "down",
    "strange": "strange",
    "anti-strange": "strange",
}


def _get(obj, name, default=None):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _normalise(value: str) -> str:
    return str(value).strip().lower().replace("_", "-")


def _is_fermion(particle: str) -> bool:
    return _normalise(particle) in _FERMION_BASES


def _is_antifermion(particle: str) -> bool:
    return _normalise(particle) in {
        "positron",
        "antimuon",
        "antitau",
        "anti-up",
        "anti-down",
        "anti-strange",
    }


def _fermion_flow_type(particle: str) -> str:
    return "antifermion" if _is_antifermion(particle) else "fermion"


def _external_arrow(role: str, particle: str) -> str:
    role = _normalise(role)

    if _is_antifermion(particle):
        return "outgoing" if role == "initial" else "incoming"

    return "incoming" if role == "initial" else "outgoing"


def _build_external_momentum(leg) -> ExternalMomentum:
    particle = str(_get(leg, "particle", "unknown"))
    role = str(_get(leg, "role", "unknown"))
    momentum = str(_get(leg, "momentum", "p"))

    return ExternalMomentum(
        leg_id=str(_get(leg, "leg_id", "unknown")),
        particle=particle,
        role=role,
        momentum=momentum,
        arrow_direction=_external_arrow(role, particle)
        if _is_fermion(particle)
        else "none",
    )


def _build_internal_flow(line) -> tuple[FermionFlow | None, BosonFlow | None]:
    particle = str(_get(line, "particle", "unknown"))
    line_id = str(_get(line, "line_id", "unknown"))
    from_vertex = str(_get(line, "from_vertex", ""))
    to_vertex = str(_get(line, "to_vertex", ""))
    momentum = str(_get(line, "momentum", "q"))

    if _is_fermion(particle):
        return (
            FermionFlow(
                line_id=line_id,
                particle=particle,
                arrow_direction="from_vertex_to_vertex",
                from_vertex=from_vertex,
                to_vertex=to_vertex,
                momentum=momentum,
                flow_type=_fermion_flow_type(particle),
            ),
            None,
        )

    return (
        None,
        BosonFlow(
            line_id=line_id,
            particle=particle,
            from_vertex=from_vertex,
            to_vertex=to_vertex,
            momentum=momentum,
            field_type="boson",
        ),
    )


def assign_flow(diagram) -> FlowAssignment:
    errors: list[str] = []

    diagram_id = str(_get(diagram, "diagram_id", "unknown"))
    process = str(_get(diagram, "process", ""))
    topology = str(_get(diagram, "topology", ""))

    external_legs = _get(diagram, "external_legs", ()) or ()
    internal_lines = _get(diagram, "internal_lines", ()) or ()

    external_momenta = tuple(
        _build_external_momentum(leg)
        for leg in external_legs
    )

    fermion_flows: list[FermionFlow] = []
    boson_flows: list[BosonFlow] = []

    for line in internal_lines:
        fermion_flow, boson_flow = _build_internal_flow(line)

        if fermion_flow is not None:
            fermion_flows.append(fermion_flow)

        if boson_flow is not None:
            boson_flows.append(boson_flow)

    if not external_legs and not internal_lines:
        errors.append("Diagram contains no legs or internal lines.")

    for flow in fermion_flows:
        if not flow.from_vertex or not flow.to_vertex:
            errors.append(
                f"Fermion line {flow.line_id} has incomplete vertex connectivity."
            )

        if not flow.momentum:
            errors.append(
                f"Fermion line {flow.line_id} has no momentum label."
            )

    for flow in boson_flows:
        if not flow.from_vertex or not flow.to_vertex:
            errors.append(
                f"Boson line {flow.line_id} has incomplete vertex connectivity."
            )

        if not flow.momentum:
            errors.append(
                f"Boson line {flow.line_id} has no momentum label."
            )

    return FlowAssignment(
        diagram_id=diagram_id,
        process=process,
        topology=topology,
        fermion_flows=tuple(fermion_flows),
        boson_flows=tuple(boson_flows),
        external_momenta=external_momenta,
        valid=not errors,
        errors=tuple(errors),
    )


def assign_flow_to_diagrams(diagrams: Iterable) -> tuple[FlowAssignment, ...]:
    return tuple(assign_flow(diagram) for diagram in diagrams)


def flow_assignment_summary(diagrams: Iterable):
    assignments = assign_flow_to_diagrams(diagrams)

    return {
        "success": True,
        "valid": all(item.valid for item in assignments),
        "diagram_count": len(assignments),
        "valid_count": sum(item.valid for item in assignments),
        "invalid_count": sum(not item.valid for item in assignments),
        "assignments": [
            {
                "diagram_id": item.diagram_id,
                "process": item.process,
                "topology": item.topology,
                "fermion_flows": [
                    {
                        "line_id": flow.line_id,
                        "particle": flow.particle,
                        "arrow_direction": flow.arrow_direction,
                        "from_vertex": flow.from_vertex,
                        "to_vertex": flow.to_vertex,
                        "momentum": flow.momentum,
                        "flow_type": flow.flow_type,
                    }
                    for flow in item.fermion_flows
                ],
                "boson_flows": [
                    {
                        "line_id": flow.line_id,
                        "particle": flow.particle,
                        "from_vertex": flow.from_vertex,
                        "to_vertex": flow.to_vertex,
                        "momentum": flow.momentum,
                        "field_type": flow.field_type,
                    }
                    for flow in item.boson_flows
                ],
                "external_momenta": [
                    {
                        "leg_id": leg.leg_id,
                        "particle": leg.particle,
                        "role": leg.role,
                        "momentum": leg.momentum,
                        "arrow_direction": leg.arrow_direction,
                    }
                    for leg in item.external_momenta
                ],
                "valid": item.valid,
                "errors": list(item.errors),
            }
            for item in assignments
        ],
        "scientific_scope": (
            "Universal tree-level fermion and boson flow representation. "
            "The layer records directed fermion flow and momentum labels "
            "but does not yet perform momentum conservation, spinor "
            "contractions, polarization sums, color algebra, or loop "
            "calculations."
        ),
    }
