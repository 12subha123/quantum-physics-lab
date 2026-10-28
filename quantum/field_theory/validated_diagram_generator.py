from __future__ import annotations

from quantum.field_theory.universal_diagram_generator import (
    generate_universal_2_to_2_diagrams,
)
from quantum.field_theory.physical_topology_validator import (
    filter_valid_diagrams,
)


def generate_valid_universal_2_to_2_diagrams(
    initial_particles: list[str],
    final_particles: list[str],
) -> dict:
    """
    Generate candidate tree-level 2->2 diagrams and immediately
    apply the physical topology validator.

    The raw generator remains available independently. This layer
    is the authoritative filtered result for downstream consumers.
    """

    raw = generate_universal_2_to_2_diagrams(
        initial_particles,
        final_particles,
    )

    raw_diagrams = raw.get("diagrams", [])

    valid_diagrams, validation = filter_valid_diagrams(
        initial_particles,
        final_particles,
        raw_diagrams,
    )

    rejected_diagrams = [
        diagram
        for diagram in raw_diagrams
        if diagram not in valid_diagrams
    ]

    return {
        "success": True,
        "status": (
            "valid_diagrams"
            if valid_diagrams
            else "no_valid_diagrams"
        ),
        "process": raw.get("process"),
        "candidate_diagram_count": len(raw_diagrams),
        "valid_diagram_count": len(valid_diagrams),
        "rejected_diagram_count": len(rejected_diagrams),
        "candidate_diagrams": raw_diagrams,
        "valid_diagrams": valid_diagrams,
        "rejected_diagrams": rejected_diagrams,
        "accepted_channels": [
            diagram.get("channel")
            for diagram in valid_diagrams
        ],
        "rejected_ids": validation.get(
            "rejected_ids",
            [],
        ),
        "validation_errors": validation.get(
            "errors",
            [],
        ),
        "scientific_scope": (
            "Tree-level candidate topology generation followed by "
            "process-specific physical topology filtering. "
            "This is not yet a complete Standard Model amplitude "
            "engine and does not include loops, renormalization, "
            "gauge fixing, or full spin/color algebra."
        ),
    }


def universal_diagram_summary(
    initial_particles: list[str],
    final_particles: list[str],
) -> dict:
    result = generate_valid_universal_2_to_2_diagrams(
        initial_particles,
        final_particles,
    )

    return {
        "success": result["success"],
        "process": result["process"],
        "candidate_diagram_count": result[
            "candidate_diagram_count"
        ],
        "valid_diagram_count": result[
            "valid_diagram_count"
        ],
        "rejected_diagram_count": result[
            "rejected_diagram_count"
        ],
        "accepted_channels": result[
            "accepted_channels"
        ],
        "rejected_ids": result[
            "rejected_ids"
        ],
        "validation_errors": result[
            "validation_errors"
        ],
    }
