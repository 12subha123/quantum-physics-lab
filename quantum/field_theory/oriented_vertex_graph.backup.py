from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations
from collections import Counter


@dataclass(frozen=True)
class ExternalLeg:
    leg_id: str
    particle: str
    role: str


@dataclass(frozen=True)
class InternalPropagator:
    particle: str
    propagator_kind: str
    vertex_a: str
    vertex_b: str


@dataclass(frozen=True)
class FermionLine:
    incoming_leg: str | None
    outgoing_leg: str | None
    vertex_a: str
    vertex_b: str
    flavor: str


@dataclass(frozen=True)
class OrientedTopologyCandidate:
    candidate_id: str
    process: str
    topology: str
    theory: str
    vertex_ids: tuple[str, ...]
    external_assignments: tuple[tuple[str, str], ...]
    internal_propagator: InternalPropagator | None
    fermion_lines: tuple[FermionLine, ...]
    status: str
    reason: str


SELF_CONJUGATE = {
    "photon",
    "gluon",
    "z",
    "higgs",
    "scalar",
}

CONJUGATES = {
    "electron": "positron",
    "positron": "electron",
    "muon": "antimuon",
    "antimuon": "muon",
    "tau": "antitau",
    "antitau": "tau",

    "electron_neutrino": "electron_antineutrino",
    "electron_antineutrino": "electron_neutrino",
    "muon_neutrino": "muon_antineutrino",
    "muon_antineutrino": "muon_neutrino",
    "tau_neutrino": "tau_antineutrino",
    "tau_antineutrino": "tau_neutrino",

    "up": "anti-up",
    "anti-up": "up",
    "down": "anti-down",
    "anti-down": "down",
    "strange": "anti-strange",
    "anti-strange": "strange",
    "charm": "anti-charm",
    "anti-charm": "charm",
    "bottom": "anti-bottom",
    "anti-bottom": "bottom",
    "top": "anti-top",
    "anti-top": "top",

    "w+": "w-",
    "w-": "w+",
}

FERMIONS = set(CONJUGATES)


def _normalise(value: str) -> str:
    return (
        str(value)
        .strip()
        .lower()
        .replace("−", "-")
        .replace("–", "-")
    )


def _canonical(value: str) -> str:
    key = _normalise(value)

    aliases = {
        "z": "Z",
        "h": "Higgs",
        "higgs": "Higgs",
        "w+": "W+",
        "w-": "W-",
        "photon": "photon",
        "gluon": "gluon",
        "scalar": "scalar",
    }

    return aliases.get(key, str(value).strip())


def _key(value: str) -> str:
    return _normalise(value)


def _is_fermion(value: str) -> bool:
    return _key(value) in FERMIONS


def _conjugate(value: str) -> str | None:
    key = _key(value)

    if key in {_key(x) for x in SELF_CONJUGATE}:
        return _canonical(value)

    partner = CONJUGATES.get(key)

    if partner is None:
        return None

    return _canonical(partner)


def _same_field(a: str, b: str) -> bool:
    ca = _canonical(a)
    cb = _canonical(b)

    return (
        ca == cb
        or _conjugate(ca) == cb
    )


def _field_kind(particle: str) -> str:
    key = _key(particle)

    if key in FERMIONS:
        return "fermion"

    if key in {
        "photon",
        "gluon",
        "z",
        "w+",
        "w-",
    }:
        return "gauge"

    if key in {
        "higgs",
        "scalar",
    }:
        return "scalar"

    return "unknown"


def _vertex_data(vertex) -> dict:
    if isinstance(vertex, dict):
        return vertex

    if hasattr(vertex, "__dict__"):
        return dict(vertex.__dict__)

    raise TypeError("Unsupported vertex object.")


def _vertex_id(vertex: dict) -> str:
    for key in ("vertex_id", "id", "name"):
        if key in vertex:
            return str(vertex[key])

    raise KeyError("Vertex has no identifier.")


def _vertex_theory(vertex: dict) -> str:
    for key in ("theory", "sector", "model"):
        if key in vertex:
            return str(vertex[key])

    return "Standard Model"


def _vertex_particles(vertex: dict) -> tuple[str, ...]:
    particles = (
        vertex.get("particles")
        or vertex.get("fields")
        or vertex.get("legs")
    )

    if particles is None:
        raise KeyError(
            f"Vertex {_vertex_id(vertex)} has no particles."
        )

    result = []

    for item in particles:

        if isinstance(item, str):
            result.append(_canonical(item))
            continue

        if isinstance(item, dict):
            particle = (
                item.get("particle")
                or item.get("name")
                or item.get("field")
            )

            if particle is None:
                raise KeyError(
                    f"Invalid port in {_vertex_id(vertex)}."
                )

            result.append(_canonical(particle))
            continue

        result.append(_canonical(str(item)))

    return tuple(result)


def _external_legs(
    initial: tuple[str, ...],
    final: tuple[str, ...],
) -> tuple[ExternalLeg, ...]:

    result = []

    for index, particle in enumerate(initial):
        result.append(
            ExternalLeg(
                leg_id=f"in{index + 1}",
                particle=_canonical(particle),
                role="incoming",
            )
        )

    for index, particle in enumerate(final):
        result.append(
            ExternalLeg(
                leg_id=f"out{index + 1}",
                particle=_canonical(particle),
                role="outgoing",
            )
        )

    return tuple(result)


def _process_text(
    initial: tuple[str, ...],
    final: tuple[str, ...],
) -> str:

    return (
        " + ".join(_canonical(x) for x in initial)
        + " -> "
        + " + ".join(_canonical(x) for x in final)
    )


# ------------------------------------------------------------------
# External fermion crossing.
#
# We keep the PHYSICAL particle on the external leg. Crossing is
# handled only when matching the field representation at a vertex.
# ------------------------------------------------------------------

def _crossed_field(
    leg: ExternalLeg,
) -> str:

    if not _is_fermion(leg.particle):
        return leg.particle

    if leg.role == "outgoing":
        partner = _conjugate(leg.particle)

        if partner is not None:
            return partner

    return leg.particle


# ------------------------------------------------------------------
# Vertex classification.
#
# The Standard Model catalog is intentionally allowed to contain
# vertices in canonical particle/antiparticle form.
# ------------------------------------------------------------------

def _fermion_content(
    particles: tuple[str, ...],
) -> tuple[str, ...]:

    return tuple(
        particle
        for particle in particles
        if _is_fermion(particle)
    )


def _boson_content(
    particles: tuple[str, ...],
) -> tuple[str, ...]:

    return tuple(
        particle
        for particle in particles
        if not _is_fermion(particle)
    )


def _fermion_flavor(particle: str) -> str:
    key = _key(particle)

    if key in {"electron", "positron"}:
        return "electron"

    if key in {"muon", "antimuon"}:
        return "muon"

    if key in {"tau", "antitau"}:
        return "tau"

    if "electron_neutrino" in key:
        return "electron_neutrino"

    if "muon_neutrino" in key:
        return "muon_neutrino"

    if "tau_neutrino" in key:
        return "tau_neutrino"

    for flavor in (
        "up",
        "down",
        "strange",
        "charm",
        "bottom",
        "top",
    ):
        if key == flavor or key == f"anti-{flavor}":
            return flavor

    return key


def _fermion_pair_compatible(
    particle_a: str,
    particle_b: str,
) -> bool:

    return (
        _fermion_flavor(particle_a)
        == _fermion_flavor(particle_b)
    )


# ------------------------------------------------------------------
# Internal propagator compatibility.
# ------------------------------------------------------------------

def _internal_compatible(
    particle_a: str,
    particle_b: str,
) -> bool:

    kind_a = _field_kind(particle_a)
    kind_b = _field_kind(particle_b)

    if kind_a != kind_b:
        return False

    if kind_a == "fermion":
        return (
            _conjugate(particle_a)
            == _canonical(particle_b)
        )

    return _same_field(
        particle_a,
        particle_b,
    )


def _propagator_kind(
    particle: str,
) -> str:

    kind = _field_kind(particle)

    if kind == "fermion":
        return "fermion-propagator"

    if kind == "gauge":
        return "gauge-boson-propagator"

    if kind == "scalar":
        return "scalar-propagator"

    return "unknown-propagator"


# ------------------------------------------------------------------
# External assignment.
#
# For a QED-like fermion-antifermion vertex, an external pair must
# form the appropriate fermion line. We don't permit arbitrary
# independent fermion assignments.
# ------------------------------------------------------------------

def _match_external_ports(
    vertex_particles: tuple[str, ...],
    legs: tuple[ExternalLeg, ...],
) -> list[tuple[tuple[str, str], ...]]:

    if len(vertex_particles) != len(legs):
        return []

    # Backtracking over the small vertex. This preserves identical
    # particle possibilities without accepting arbitrary flavor
    # substitutions.
    results = []

    def recurse(
        remaining_particles: tuple[str, ...],
        remaining_legs: tuple[ExternalLeg, ...],
        assignments: list[tuple[str, str]],
    ):

        if not remaining_legs:
            results.append(tuple(assignments))
            return

        leg = remaining_legs[0]
        field = _crossed_field(leg)

        for index, particle in enumerate(
            remaining_particles
        ):

            if not _same_field(
                particle,
                field,
            ):
                continue

            next_particles = (
                remaining_particles[:index]
                + remaining_particles[index + 1:]
            )

            assignments.append(
                (
                    leg.leg_id,
                    particle,
                )
            )

            recurse(
                next_particles,
                remaining_legs[1:],
                assignments,
            )

            assignments.pop()

    recurse(
        vertex_particles,
        legs,
        [],
    )

    return results


# ------------------------------------------------------------------
# External leg partitions.
# ------------------------------------------------------------------

def _partitions(
    legs: tuple[ExternalLeg, ...],
):

    n = len(legs)

    for mask in range(
        1,
        (1 << n) - 1,
    ):

        left = tuple(
            legs[i]
            for i in range(n)
            if mask & (1 << i)
        )

        right = tuple(
            legs[i]
            for i in range(n)
            if not (mask & (1 << i))
        )

        # Remove complementary duplicate.
        if len(left) > len(right):
            continue

        yield left, right


# ------------------------------------------------------------------
# Determine physical channel from external-line connectivity.
# ------------------------------------------------------------------

def _channel(
    left: tuple[ExternalLeg, ...],
    right: tuple[ExternalLeg, ...],
) -> str:

    left_ids = {
        leg.leg_id
        for leg in left
    }

    right_ids = {
        leg.leg_id
        for leg in right
    }

    left_in = {
        leg.leg_id
        for leg in left
        if leg.role == "incoming"
    }

    left_out = {
        leg.leg_id
        for leg in left
        if leg.role == "outgoing"
    }

    right_in = {
        leg.leg_id
        for leg in right
        if leg.role == "incoming"
    }

    right_out = {
        leg.leg_id
        for leg in right
        if leg.role == "outgoing"
    }

    if len(left_in) == 2 and len(right_out) == 2:
        return "s"

    if len(right_in) == 2 and len(left_out) == 2:
        return "s"

    # t-channel preserves incoming/outgoing identity.
    if (
        {"in1", "out1"} <= left_ids
        and {"in2", "out2"} <= right_ids
    ):
        return "t"

    if (
        {"in2", "out2"} <= left_ids
        and {"in1", "out1"} <= right_ids
    ):
        return "t"

    # u-channel crosses the outgoing assignments.
    if (
        {"in1", "out2"} <= left_ids
        and {"in2", "out1"} <= right_ids
    ):
        return "u"

    if (
        {"in2", "out1"} <= left_ids
        and {"in1", "out2"} <= right_ids
    ):
        return "u"

    return "connected"


# ------------------------------------------------------------------
# Fermion-line validation.
# ------------------------------------------------------------------

def _build_fermion_lines(
    process_legs: tuple[ExternalLeg, ...],
    left_vertex: str,
    right_vertex: str,
    left_group: tuple[ExternalLeg, ...],
    right_group: tuple[ExternalLeg, ...],
) -> tuple[FermionLine, ...] | None:

    initial = [
        leg
        for leg in process_legs
        if leg.role == "incoming"
        and _is_fermion(leg.particle)
    ]

    final = [
        leg
        for leg in process_legs
        if leg.role == "outgoing"
        and _is_fermion(leg.particle)
    ]

    # For each initial fermion, find the physically matching final
    # fermion on the same flavor line. An initial antifermion pairs
    # with the corresponding outgoing antifermion.
    used_final = set()
    lines = []

    for incoming in initial:

        incoming_key = _key(
            incoming.particle
        )

        is_antiparticle = incoming_key in {
            _key(x)
            for x in CONJUGATES.values()
        }

        desired_flavor = _fermion_flavor(
            incoming.particle
        )

        candidates = [
            leg
            for leg in final
            if leg.leg_id not in used_final
            and _fermion_flavor(
                leg.particle
            ) == desired_flavor
        ]

        if not candidates:
            continue

        outgoing = candidates[0]
        used_final.add(outgoing.leg_id)

        incoming_vertex = (
            left_vertex
            if incoming in left_group
            else right_vertex
        )

        outgoing_vertex = (
            left_vertex
            if outgoing in left_group
            else right_vertex
        )

        lines.append(
            FermionLine(
                incoming_leg=incoming.leg_id,
                outgoing_leg=outgoing.leg_id,
                vertex_a=incoming_vertex,
                vertex_b=outgoing_vertex,
                flavor=desired_flavor,
            )
        )

    return tuple(lines)


def _canonical_assignment(
    assignments: tuple[tuple[str, str], ...],
) -> tuple[tuple[str, str], ...]:

    return tuple(
        sorted(
            assignments,
            key=lambda x: x[0],
        )
    )


def _canonical_graph_key(
    candidate: OrientedTopologyCandidate,
) -> tuple:

    propagator = candidate.internal_propagator

    return (
        candidate.topology,
        tuple(
            sorted(candidate.vertex_ids)
        ),
        tuple(
            sorted(candidate.external_assignments)
        ),
        (
            propagator.particle
            if propagator
            else None
        ),
    )


def _charge(
    particle: str,
) -> float | None:

    values = {
        "electron": -1,
        "positron": 1,
        "muon": -1,
        "antimuon": 1,
        "tau": -1,
        "antitau": 1,

        "electron_neutrino": 0,
        "electron_antineutrino": 0,
        "muon_neutrino": 0,
        "muon_antineutrino": 0,
        "tau_neutrino": 0,
        "tau_antineutrino": 0,

        "up": 2 / 3,
        "anti-up": -2 / 3,
        "down": -1 / 3,
        "anti-down": 1 / 3,
        "strange": -1 / 3,
        "anti-strange": 1 / 3,
        "charm": 2 / 3,
        "anti-charm": -2 / 3,
        "bottom": -1 / 3,
        "anti-bottom": 1 / 3,
        "top": 2 / 3,
        "anti-top": -2 / 3,

        "photon": 0,
        "gluon": 0,
        "w+": 1,
        "w-": -1,
        "z": 0,
        "higgs": 0,
        "scalar": 0,
    }

    return values.get(
        _key(particle)
    )


def _charge_conserved(
    initial: tuple[str, ...],
    final: tuple[str, ...],
) -> bool | None:

    incoming = [
        _charge(x)
        for x in initial
    ]

    outgoing = [
        _charge(x)
        for x in final
    ]

    if any(
        x is None
        for x in incoming + outgoing
    ):
        return None

    return abs(
        sum(incoming)
        - sum(outgoing)
    ) < 1e-12


def search_oriented_two_vertex_graphs(
    initial_particles: list[str] | tuple[str, ...],
    final_particles: list[str] | tuple[str, ...],
) -> dict:

    from quantum.field_theory.standard_model_vertices import (
        list_standard_model_vertices,
    )

    initial = tuple(
        _canonical(x)
        for x in initial_particles
    )

    final = tuple(
        _canonical(x)
        for x in final_particles
    )

    process = _process_text(
        initial,
        final,
    )

    charge = _charge_conserved(
        initial,
        final,
    )

    if charge is False:
        return {
            "success": True,
            "process": process,
            "candidate_count": 0,
            "allowed_count": 0,
            "forbidden_count": 1,
            "undecidable_count": 0,
            "candidates": [],
            "forbidden": [
                {
                    "status": "forbidden",
                    "reason": (
                        "Electric charge is not conserved."
                    ),
                }
            ],
        }

    vertices = [
        _vertex_data(vertex)
        for vertex in list_standard_model_vertices()
    ]

    legs = _external_legs(
        initial,
        final,
    )

    candidates = []

    # A physical tree diagram may contain two instances of
    # the same interaction vertex.
    #
    # Examples:
    #   e- e+ -> e- e+ : QED t-channel
    #   e- e- -> e- e- : QED t/u-channel
    #   u ubar -> g g  : quark t/u-channel
    #
    # Repeated vertex definitions are therefore allowed.
    for first_index in range(len(vertices)):
        for second_index in range(
            first_index,
            len(vertices),
        ):
            first = vertices[first_index]
            second = vertices[second_index]

            first_id = _vertex_id(first)
            second_id = _vertex_id(second)

            first_particles = _vertex_particles(first)
            second_particles = _vertex_particles(second)

            for first_port_index, first_internal in enumerate(
                first_particles
            ):
                for second_port_index, second_internal in enumerate(
                    second_particles
                ):

                    if not _internal_compatible(
                        first_internal,
                        second_internal,
                    ):
                        continue

                    first_remaining = (
                        first_particles[:first_port_index]
                        + first_particles[first_port_index + 1:]
                    )

                    second_remaining = (
                        second_particles[:second_port_index]
                        + second_particles[second_port_index + 1:]
                    )

                    for left, right in _partitions(legs):

                        if len(first_remaining) != len(left):
                            continue

                        if len(second_remaining) != len(right):
                            continue

                        first_matches = _match_external_ports(
                            first_remaining,
                            left,
                        )

                        second_matches = _match_external_ports(
                            second_remaining,
                            right,
                        )

                        if not first_matches or not second_matches:
                            continue

                        channel = _channel(
                            left,
                            right,
                        )

                        if channel == "connected":
                            continue

                        fermion_lines = _build_fermion_lines(
                            legs,
                            first_id,
                            second_id,
                            left,
                            right,
                        )

                        assignments = tuple(
                            sorted(
                                [
                                    (leg_id, first_id)
                                    for match in first_matches
                                    for leg_id, _ in match
                                ]
                                + [
                                    (leg_id, second_id)
                                    for match in second_matches
                                    for leg_id, _ in match
                                ]
                            )
                        )

                        propagator = InternalPropagator(
                            particle=_canonical(first_internal),
                            propagator_kind=_propagator_kind(
                                first_internal
                            ),
                            vertex_a=first_id,
                            vertex_b=second_id,
                        )

                        candidate = OrientedTopologyCandidate(
                            candidate_id=f"graph_{len(candidates) + 1}",
                            process=process,
                            topology=channel,
                            theory=(
                                _vertex_theory(first)
                                + " / "
                                + _vertex_theory(second)
                            ),
                            vertex_ids=(
                                first_id,
                                second_id,
                            ),
                            external_assignments=(
                                _canonical_assignment(
                                    assignments
                                ),
                            ),
                            internal_propagator=propagator,
                            fermion_lines=fermion_lines or (),
                            status="candidate",
                            reason=(
                                "Connected two-vertex graph passes "
                                "external crossing, internal propagator, "
                                "and channel checks."
                            ),
                        )

                        candidates.append(candidate)

    # --------------------------------------------------------------
    # Canonical graph deduplication.
    # --------------------------------------------------------------

    unique = []
    seen = set()

    for candidate in candidates:

        key = _canonical_graph_key(
            candidate
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(candidate)

    candidates = unique

    return {
        "success": True,
        "process": process,
        "candidate_count": len(candidates),
        "allowed_count": len(candidates),
        "forbidden_count": 0,
        "undecidable_count": (
            1 if not candidates else 0
        ),
        "candidates": [
            asdict(candidate)
            for candidate in candidates
        ],
        "scientific_scope": (
            "Generic two-vertex Standard Model graph discovery "
            "with external fermion crossing, internal propagator "
            "compatibility, fermion-line continuity, channel "
            "classification, and canonical graph deduplication. "
            "This remains a candidate topology layer; complete "
            "momentum conservation, gauge consistency, spin/color "
            "algebra, and higher-vertex graphs are separate layers."
        ),
    }


def oriented_graph_summary(
    initial_particles: list[str] | tuple[str, ...],
    final_particles: list[str] | tuple[str, ...],
) -> dict:

    result = search_oriented_two_vertex_graphs(
        initial_particles,
        final_particles,
    )

    return {
        "success": result["success"],
        "process": result["process"],
        "candidate_count": result["candidate_count"],
        "allowed_count": result["allowed_count"],
        "forbidden_count": result["forbidden_count"],
        "undecidable_count": result[
            "undecidable_count"
        ],
    }


