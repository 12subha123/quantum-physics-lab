from dataclasses import asdict
from typing import Iterable

from quantum.field_theory.standard_model_vertices import (
    STANDARD_MODEL_VERTICES,
    InteractionVertex,
)


def _normalize_particle(name: str) -> str:
    return name.strip().lower()


def _particle_category(name: str) -> str:
    particle = _normalize_particle(name)

    if particle in {"electron", "muon", "tau"}:
        return "fermion"

    if particle in {"positron", "antimuon", "antitau"}:
        return "antifermion"

    if particle in {
        "electron neutrino",
        "muon neutrino",
        "tau neutrino",
    }:
        return "neutrino"

    if particle in {
        "electron antineutrino",
        "muon antineutrino",
        "tau antineutrino",
    }:
        return "antineutrino"

    if particle in {
        "up",
        "down",
        "strange",
        "charm",
        "top",
        "bottom",
    }:
        return "quark"

    if particle in {
        "anti-up",
        "anti-down",
        "anti-strange",
        "anti-charm",
        "anti-top",
        "anti-bottom",
    }:
        return "antiquark"

    if particle == "photon":
        return "photon"

    if particle == "gluon":
        return "gluon"

    if particle in {"w+", "w-"}:
        return "W"

    if particle == "z":
        return "Z"

    if particle == "higgs":
        return "Higgs"

    if particle in {"scalar", "phi"}:
        return "scalar"

    return "unknown"


def _vertex_can_contain_categories(
    categories: Iterable[str],
    vertex: InteractionVertex,
) -> bool:
    available = list(categories)
    required = list(vertex.particles)

    if len(available) != len(required):
        return False

    remaining = required.copy()

    for category in available:
        if category not in remaining:
            return False

        remaining.remove(category)

    return not remaining


def find_matching_vertices(particles: list[str]) -> list[dict]:
    """
    Match concrete particle names against the generic interaction
    vertex catalog.

    This is a vertex-identification layer, not a complete
    Standard Model amplitude validator.
    """
    if not particles:
        raise ValueError("At least one particle is required.")

    categories = [_particle_category(particle) for particle in particles]

    if "unknown" in categories:
        return []

    matches = [
        vertex
        for vertex in STANDARD_MODEL_VERTICES
        if _vertex_can_contain_categories(categories, vertex)
    ]

    return [asdict(vertex) for vertex in matches]


def find_matching_vertices_for_process(
    initial_particles: list[str],
    final_particles: list[str],
) -> list[dict]:
    """
    Find interaction vertices that can participate in the supplied
    process.

    Returned vertices are candidates only. Charge, flavor, color,
    momentum conservation, gauge constraints, and complete topology
    must be checked separately.
    """
    all_particles = initial_particles + final_particles

    if not all_particles:
        raise ValueError(
            "At least one initial or final particle is required."
        )

    categories = [_particle_category(particle) for particle in all_particles]

    if "unknown" in categories:
        return []

    results = []

    for vertex in STANDARD_MODEL_VERTICES:
        subsets = _candidate_vertex_subsets(
            categories,
            len(vertex.particles),
        )

        if any(
            _vertex_can_contain_categories(subset, vertex)
            for subset in subsets
        ):
            results.append(asdict(vertex))

    return results


def _candidate_vertex_subsets(
    categories: list[str],
    size: int,
) -> list[list[str]]:
    if size <= 0 or size > len(categories):
        return []

    results: list[list[str]] = []

    def backtrack(start: int, current: list[str]) -> None:
        if len(current) == size:
            candidate = current.copy()

            if candidate not in results:
                results.append(candidate)

            return

        remaining_needed = size - len(current)

        for index in range(
            start,
            len(categories) - remaining_needed + 1,
        ):
            current.append(categories[index])
            backtrack(index + 1, current)
            current.pop()

    backtrack(0, [])

    return results
