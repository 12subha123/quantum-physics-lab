from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations
from collections import Counter


@dataclass(frozen=True)
class VertexConnectionCandidate:
    candidate_id: str
    process: str
    vertex_ids: tuple[str, ...]
    internal_field: str | None
    external_assignment: tuple[tuple[str, str], ...]
    topology: str
    status: str
    reason: str


# ---------------------------------------------------------------------
# Particle-field helpers
# ---------------------------------------------------------------------

SELF_CONJUGATE = {
    "photon",
    "gluon",
    "Z",
    "Higgs",
    "scalar",
}

FERMION_PAIRS = {
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
}


def _normalise(value: str) -> str:
    return (
        value.strip()
        .lower()
        .replace("−", "-")
        .replace("–", "-")
    )


def _canonical(value: str) -> str:
    value = _normalise(value)

    aliases = {
        "w+": "W+",
        "w-": "W-",
        "z": "Z",
        "higgs": "Higgs",
        "photon": "photon",
        "gluon": "gluon",
        "scalar": "scalar",
    }

    return aliases.get(value, value)


def _particle_key(value: str) -> str:
    return _normalise(value)


def _is_self_conjugate(particle: str) -> bool:
    return _canonical(particle) in SELF_CONJUGATE


def _conjugate(particle: str) -> str | None:
    particle = _particle_key(particle)

    if particle in {
        _particle_key(x)
        for x in SELF_CONJUGATE
    }:
        return _canonical(particle)

    partner = FERMION_PAIRS.get(particle)

    if partner is not None:
        return _canonical(partner)

    if particle == "w+":
        return "W-"

    if particle == "w-":
        return "W+"

    return None


def _same_field(a: str, b: str) -> bool:
    ca = _canonical(a)
    cb = _canonical(b)

    if ca == cb:
        return True

    conjugate = _conjugate(ca)

    return conjugate == cb


def _particle_counter(
    particles: list[str] | tuple[str, ...],
) -> Counter[str]:
    return Counter(
        _particle_key(p)
        for p in particles
    )


def _process_text(
    initial: tuple[str, ...],
    final: tuple[str, ...],
) -> str:
    return (
        " + ".join(_canonical(x) for x in initial)
        + " -> "
        + " + ".join(_canonical(x) for x in final)
    )


# ---------------------------------------------------------------------
# Vertex utilities
# ---------------------------------------------------------------------

def _vertex_particles(vertex: dict) -> tuple[str, ...]:
    return tuple(
        _canonical(p)
        for p in vertex["particles"]
    )


def _shared_internal_fields(
    first: dict,
    second: dict,
) -> list[str]:
    result = []

    for a in _vertex_particles(first):
        for b in _vertex_particles(second):
            if _same_field(a, b):
                result.append(a)

    # Preserve order while removing duplicates.
    unique = []

    for field in result:
        if not any(_same_field(field, old) for old in unique):
            unique.append(field)

    return unique


def _remove_one_field(
    fields: tuple[str, ...],
    field: str,
) -> tuple[str, ...] | None:
    remaining = list(fields)

    for index, value in enumerate(remaining):
        if _same_field(value, field):
            remaining.pop(index)
            return tuple(remaining)

    return None


def _assign_external_particles(
    remaining_fields: tuple[str, ...],
    external_particles: tuple[str, ...],
) -> tuple[tuple[str, str], ...] | None:

    if len(remaining_fields) != len(external_particles):
        return None

    unused = list(remaining_fields)
    assignment = []

    # Exact/conjugate-compatible matching.
    for particle in external_particles:
        found_index = None

        for index, field in enumerate(unused):
            if _same_field(field, particle):
                found_index = index
                break

        if found_index is None:
            return None

        field = unused.pop(found_index)

        assignment.append(
            (
                _canonical(particle),
                _canonical(field),
            )
        )

    if unused:
        return None

    return tuple(assignment)


def _vertex_pair_assignments(
    first: dict,
    second: dict,
    initial: tuple[str, ...],
    final: tuple[str, ...],
) -> list[
    tuple[
        str,
        tuple[tuple[str, str], ...],
        str,
    ]
]:

    external = initial + final
    shared_fields = _shared_internal_fields(
        first,
        second,
    )

    results = []

    for internal in shared_fields:

        first_remaining = _remove_one_field(
            _vertex_particles(first),
            internal,
        )

        second_remaining = _remove_one_field(
            _vertex_particles(second),
            internal,
        )

        if first_remaining is None:
            continue

        if second_remaining is None:
            continue

        external_fields = (
            first_remaining
            + second_remaining
        )

        assignment = _assign_external_particles(
            external_fields,
            external,
        )

        if assignment is None:
            continue

        results.append(
            (
                _canonical(internal),
                assignment,
                "2-vertex-tree",
            )
        )

    return results


# ---------------------------------------------------------------------
# Physical external-particle constraints.
#
# These are deliberately conservative. A process that cannot yet be
# classified is returned as "undecidable", not silently forbidden.
# ---------------------------------------------------------------------

def _electric_charge(particle: str) -> float | None:
    charges = {
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
        "charm": 2 / 3,
        "anti-charm": -2 / 3,
        "top": 2 / 3,
        "anti-top": -2 / 3,

        "down": -1 / 3,
        "anti-down": 1 / 3,
        "strange": -1 / 3,
        "anti-strange": 1 / 3,
        "bottom": -1 / 3,
        "anti-bottom": 1 / 3,

        "photon": 0,
        "gluon": 0,
        "W+": 1,
        "W-": -1,
        "Z": 0,
        "Higgs": 0,
        "scalar": 0,
    }

    return charges.get(_canonical(particle))


def _charge_conserved(
    initial: tuple[str, ...],
    final: tuple[str, ...],
) -> bool | None:

    charges_initial = [
        _electric_charge(p)
        for p in initial
    ]

    charges_final = [
        _electric_charge(p)
        for p in final
    ]

    if any(x is None for x in charges_initial + charges_final):
        return None

    return abs(
        sum(charges_initial)
        - sum(charges_final)
    ) < 1e-12


def _external_status(
    initial: tuple[str, ...],
    final: tuple[str, ...],
) -> tuple[str, str]:

    charge_result = _charge_conserved(
        initial,
        final,
    )

    if charge_result is False:
        return (
            "forbidden",
            "Electric charge is not conserved.",
        )

    if charge_result is None:
        return (
            "undecidable",
            "Charge information is incomplete for at least one particle.",
        )

    return (
        "candidate",
        "External particle content passes the basic charge check.",
    )


# ---------------------------------------------------------------------
# Universal graph search
# ---------------------------------------------------------------------

def search_connected_vertex_graph(
    initial_particles: list[str] | tuple[str, ...],
    final_particles: list[str] | tuple[str, ...],
) -> dict:

    from quantum.field_theory.standard_model_vertices import (
        list_standard_model_vertices,
    )

    initial = tuple(
        _canonical(p)
        for p in initial_particles
    )

    final = tuple(
        _canonical(p)
        for p in final_particles
    )

    process = _process_text(
        initial,
        final,
    )

    vertices = list_standard_model_vertices()

    candidates: list[VertexConnectionCandidate] = []

    external_status, external_reason = _external_status(
        initial,
        final,
    )

    # ---------------------------------------------------------------
    # Global impossible process.
    # ---------------------------------------------------------------

    if external_status == "forbidden":
        candidates.append(
            VertexConnectionCandidate(
                candidate_id="external_constraints",
                process=process,
                vertex_ids=(),
                internal_field=None,
                external_assignment=(),
                topology="none",
                status="forbidden",
                reason=external_reason,
            )
        )

    # ---------------------------------------------------------------
    # Direct interaction vertices.
    #
    # A direct vertex is possible when the requested process contains
    # exactly one registered vertex worth of external fields.
    # ---------------------------------------------------------------

    combined = initial + final

    for index, vertex in enumerate(vertices):
        fields = _vertex_particles(vertex)

        if len(fields) != len(combined):
            continue

        if _particle_counter(fields) == _particle_counter(combined):
            candidates.append(
                VertexConnectionCandidate(
                    candidate_id=f"direct_{index + 1}",
                    process=process,
                    vertex_ids=(vertex["vertex_id"],),
                    internal_field=None,
                    external_assignment=tuple(
                        (
                            _canonical(p),
                            _canonical(p),
                        )
                        for p in combined
                    ),
                    topology="single-vertex",
                    status="candidate",
                    reason=(
                        "External particle content exactly matches "
                        "a registered Standard Model vertex."
                    ),
                )
            )

    # ---------------------------------------------------------------
    # Connected two-vertex tree search.
    #
    # Every external particle must be supplied by one of the two
    # vertices. Exactly one shared field becomes the propagator.
    # ---------------------------------------------------------------

    for first, second in combinations(vertices, 2):

        assignments = _vertex_pair_assignments(
            first,
            second,
            initial,
            final,
        )

        for (
            assignment_index,
            (
                internal,
                assignment,
                topology,
            ),
        ) in enumerate(assignments):

            candidate_id = (
                f"pair_{len(candidates) + 1}"
            )

            candidates.append(
                VertexConnectionCandidate(
                    candidate_id=candidate_id,
                    process=process,
                    vertex_ids=(
                        first["vertex_id"],
                        second["vertex_id"],
                    ),
                    internal_field=internal,
                    external_assignment=assignment,
                    topology=topology,
                    status="candidate",
                    reason=(
                        "Both vertices can be connected by the "
                        "identified internal field while supplying "
                        "all requested external particles."
                    ),
                )
            )

    # ---------------------------------------------------------------
    # Deduplicate identical graph descriptions.
    # ---------------------------------------------------------------

    unique = []
    seen = set()

    for candidate in candidates:
        key = (
            candidate.vertex_ids,
            candidate.internal_field,
            candidate.external_assignment,
            candidate.topology,
            candidate.status,
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(candidate)

    candidates = unique

    # ---------------------------------------------------------------
    # If nothing connected, preserve that information.
    # ---------------------------------------------------------------

    if not candidates:
        if external_status == "candidate":
            candidates.append(
                VertexConnectionCandidate(
                    candidate_id="no_connected_vertex_graph",
                    process=process,
                    vertex_ids=(),
                    internal_field=None,
                    external_assignment=(),
                    topology="none",
                    status="undecidable",
                    reason=(
                        "No connected tree-level graph could be "
                        "constructed from the currently registered "
                        "Standard Model vertices."
                    ),
                )
            )

    allowed_candidates = [
        asdict(candidate)
        for candidate in candidates
        if candidate.status == "candidate"
    ]

    forbidden_candidates = [
        asdict(candidate)
        for candidate in candidates
        if candidate.status == "forbidden"
    ]

    undecidable_candidates = [
        asdict(candidate)
        for candidate in candidates
        if candidate.status == "undecidable"
    ]

    return {
        "success": True,
        "process": process,
        "initial_particles": list(initial),
        "final_particles": list(final),
        "candidate_count": len(candidates),
        "allowed_candidate_count": len(
            allowed_candidates
        ),
        "forbidden_count": len(
            forbidden_candidates
        ),
        "undecidable_count": len(
            undecidable_candidates
        ),
        "candidates": [
            asdict(candidate)
            for candidate in candidates
        ],
        "allowed_candidates": allowed_candidates,
        "forbidden_candidates": forbidden_candidates,
        "undecidable_candidates": undecidable_candidates,
        "scientific_scope": (
            "Field-connected tree-level graph search over the "
            "registered broken-phase Standard Model interaction "
            "vertices. Candidate status does not yet constitute "
            "complete proof of physical validity; momentum flow, "
            "fermion arrows, gauge structure, and full conservation "
            "constraints are validated in subsequent layers."
        ),
    }


def connected_graph_summary(
    initial_particles: list[str] | tuple[str, ...],
    final_particles: list[str] | tuple[str, ...],
) -> dict:

    result = search_connected_vertex_graph(
        initial_particles,
        final_particles,
    )

    return {
        "success": result["success"],
        "process": result["process"],
        "candidate_count": result["candidate_count"],
        "allowed_candidate_count": result[
            "allowed_candidate_count"
        ],
        "forbidden_count": result[
            "forbidden_count"
        ],
        "undecidable_count": result[
            "undecidable_count"
        ],
    }
