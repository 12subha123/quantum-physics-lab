from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations


@dataclass(frozen=True)
class InteractionCandidate:
    candidate_id: str
    initial_particles: tuple[str, ...]
    final_particles: tuple[str, ...]
    matched_vertices: tuple[str, ...]
    status: str
    reason: str


def _normalise(value: str) -> str:
    return (
        value.strip()
        .lower()
        .replace("−", "-")
        .replace("–", "-")
    )


def _normalise_particles(
    particles: list[str] | tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(_normalise(p) for p in particles)


def _charge(particle: str) -> float:
    charges = {
        "electron": -1.0,
        "positron": 1.0,
        "muon": -1.0,
        "antimuon": 1.0,
        "tau": -1.0,
        "antitau": 1.0,

        "electron_neutrino": 0.0,
        "electron_antineutrino": 0.0,
        "muon_neutrino": 0.0,
        "muon_antineutrino": 0.0,
        "tau_neutrino": 0.0,
        "tau_antineutrino": 0.0,

        "up": 2.0 / 3.0,
        "anti-up": -2.0 / 3.0,
        "charm": 2.0 / 3.0,
        "anti-charm": -2.0 / 3.0,
        "top": 2.0 / 3.0,
        "anti-top": -2.0 / 3.0,

        "down": -1.0 / 3.0,
        "anti-down": 1.0 / 3.0,
        "strange": -1.0 / 3.0,
        "anti-strange": 1.0 / 3.0,
        "bottom": -1.0 / 3.0,
        "anti-bottom": 1.0 / 3.0,

        "photon": 0.0,
        "gluon": 0.0,
        "W+": 1.0,
        "W-": -1.0,
        "Z": 0.0,
        "Higgs": 0.0,
        "scalar": 0.0,
    }

    return charges.get(particle, 999.0)


def _charge_conservation_reason(
    initial: tuple[str, ...],
    final: tuple[str, ...],
) -> str | None:

    initial_charge = sum(_charge(p) for p in initial)
    final_charge = sum(_charge(p) for p in final)

    if initial_charge == 999.0 or final_charge == 999.0:
        return "Unknown particle charge."

    if abs(initial_charge - final_charge) > 1e-12:
        return (
            "Electric charge is not conserved: "
            f"Q_initial={initial_charge:g}, "
            f"Q_final={final_charge:g}."
        )

    return None


def _vertex_contains_particles(
    vertex: dict,
    particles: tuple[str, ...],
) -> bool:
    available = tuple(
        _normalise(p)
        for p in vertex["particles"]
    )

    requested = tuple(
        _normalise(p)
        for p in particles
    )

    remaining = list(available)

    for particle in requested:
        if particle not in remaining:
            return False

        remaining.remove(particle)

    return True


def _find_direct_vertices(
    particles: tuple[str, ...],
    vertices: list[dict],
) -> list[str]:

    matches = []

    for vertex in vertices:
        if len(vertex["particles"]) != len(particles):
            continue

        if _vertex_contains_particles(vertex, particles):
            matches.append(vertex["vertex_id"])

    return matches


def _particle_vertex_matches(
    particle: str,
    vertex: dict,
) -> bool:
    return _vertex_contains_particles(
        vertex,
        (particle,),
    )


def _find_particle_vertices(
    particle: str,
    vertices: list[dict],
) -> list[str]:

    return [
        vertex["vertex_id"]
        for vertex in vertices
        if _particle_vertex_matches(particle, vertex)
    ]


def explore_interaction_space(
    initial_particles: list[str] | tuple[str, ...],
    final_particles: list[str] | tuple[str, ...],
) -> dict:

    from quantum.field_theory.standard_model_vertices import (
        list_standard_model_vertices,
    )

    initial = _normalise_particles(initial_particles)
    final = _normalise_particles(final_particles)
    vertices = list_standard_model_vertices()

    process = (
        " + ".join(initial)
        + " -> "
        + " + ".join(final)
    )

    candidates: list[InteractionCandidate] = []

    # ---------------------------------------------------------------
    # Candidate 1:
    # Direct single-vertex interaction.
    # ---------------------------------------------------------------
    combined = initial + final

    direct_matches = _find_direct_vertices(
        combined,
        vertices,
    )

    if direct_matches:
        for index, vertex_id in enumerate(direct_matches):
            candidates.append(
                InteractionCandidate(
                    candidate_id=f"direct_{index + 1}",
                    initial_particles=initial,
                    final_particles=final,
                    matched_vertices=(vertex_id,),
                    status="candidate_allowed",
                    reason=(
                        "The complete process matches a registered "
                        "Standard Model interaction vertex."
                    ),
                )
            )

    # ---------------------------------------------------------------
    # Candidate 2:
    # Search for vertices touching every external particle.
    #
    # This intentionally does NOT claim the resulting combination
    # is a valid diagram. It identifies possible interaction-space
    # connections for later topology construction.
    # ---------------------------------------------------------------
    external = initial + final

    particle_vertex_sets = {
        particle: _find_particle_vertices(
            particle,
            vertices,
        )
        for particle in external
    }

    unknown_particles = [
        particle
        for particle, matches in particle_vertex_sets.items()
        if not matches
    ]

    if unknown_particles:
        candidates.append(
            InteractionCandidate(
                candidate_id="unmatched_external_fields",
                initial_particles=initial,
                final_particles=final,
                matched_vertices=(),
                status="undecidable",
                reason=(
                    "At least one external particle has no registered "
                    "interaction vertex: "
                    + ", ".join(unknown_particles)
                ),
            )
        )

    # ---------------------------------------------------------------
    # Candidate 3:
    # Look for pairs of vertices sharing a possible internal field.
    #
    # This is deliberately broad. It generates interaction-space
    # candidates before physical topology filtering.
    # ---------------------------------------------------------------
    pair_candidates = []

    for first, second in combinations(vertices, 2):
        shared = set(
            _normalise(p)
            for p in first["particles"]
        ) & set(
            _normalise(p)
            for p in second["particles"]
        )

        if not shared:
            continue

        external_match_count = 0

        for particle in external:
            if (
                _particle_vertex_matches(
                    particle,
                    first,
                )
                or _particle_vertex_matches(
                    particle,
                    second,
                )
            ):
                external_match_count += 1

        if external_match_count >= min(
            len(external),
            4,
        ):
            pair_candidates.append(
                (
                    first["vertex_id"],
                    second["vertex_id"],
                    tuple(sorted(shared)),
                )
            )

    for index, (v1, v2, shared) in enumerate(
        pair_candidates
    ):
        candidates.append(
            InteractionCandidate(
                candidate_id=f"vertex_pair_{index + 1}",
                initial_particles=initial,
                final_particles=final,
                matched_vertices=(v1, v2),
                status="topology_candidate",
                reason=(
                    "Two registered SM vertices share a possible "
                    f"internal field: {', '.join(shared)}. "
                    "Full topology and conservation validation "
                    "is required before this becomes a physical diagram."
                ),
            )
        )

    # ---------------------------------------------------------------
    # Impossible / forbidden classification.
    # ---------------------------------------------------------------

    charge_error = _charge_conservation_reason(
        initial,
        final,
    )

    if charge_error:
        candidates.append(
            InteractionCandidate(
                candidate_id="charge_conservation",
                initial_particles=initial,
                final_particles=final,
                matched_vertices=(),
                status="forbidden",
                reason=charge_error,
            )
        )

    if not candidates:
        candidates.append(
            InteractionCandidate(
                candidate_id="no_registered_connection",
                initial_particles=initial,
                final_particles=final,
                matched_vertices=(),
                status="no_registered_interaction",
                reason=(
                    "No direct vertex or registered two-vertex "
                    "interaction-space connection was found."
                ),
            )
        )

    allowed = [
        asdict(c)
        for c in candidates
        if c.status == "candidate_allowed"
    ]

    topology_candidates = [
        asdict(c)
        for c in candidates
        if c.status == "topology_candidate"
    ]

    forbidden = [
        asdict(c)
        for c in candidates
        if c.status == "forbidden"
    ]

    undecidable = [
        asdict(c)
        for c in candidates
        if c.status == "undecidable"
    ]

    return {
        "success": True,
        "process": process,
        "initial_particles": list(initial),
        "final_particles": list(final),
        "candidate_count": len(candidates),
        "allowed_candidate_count": len(allowed),
        "topology_candidate_count": len(
            topology_candidates
        ),
        "forbidden_count": len(forbidden),
        "undecidable_count": len(undecidable),
        "candidates": [
            asdict(c)
            for c in candidates
        ],
        "allowed_candidates": allowed,
        "topology_candidates": topology_candidates,
        "forbidden_candidates": forbidden,
        "undecidable_candidates": undecidable,
        "scientific_scope": (
            "Universal Standard Model interaction-space exploration. "
            "Candidates are intentionally broader than physically "
            "validated diagrams. Forbidden and undecidable states "
            "are preserved rather than discarded."
        ),
    }


def interaction_space_summary(
    initial_particles: list[str] | tuple[str, ...],
    final_particles: list[str] | tuple[str, ...],
) -> dict:

    result = explore_interaction_space(
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
        "topology_candidate_count": result[
            "topology_candidate_count"
        ],
        "forbidden_count": result[
            "forbidden_count"
        ],
        "undecidable_count": result[
            "undecidable_count"
        ],
        "scientific_scope": result[
            "scientific_scope"
        ],
    }
