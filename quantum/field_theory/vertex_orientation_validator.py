from __future__ import annotations

from dataclasses import dataclass

from .oriented_vertex_graph import (
    TreeTopologyCandidate,
    _normalize_particle,
    conjugate,
    is_self_conjugate,
)


@dataclass(frozen=True)
class VertexOrientationResult:
    status: str
    reasons: tuple[str, ...]


def _normalized_fields(fields) -> tuple[str, ...]:
    return tuple(
        _normalize_particle(field)
        for field in fields
    )


def _field_matches(
    physical_particle: str,
    crossed_field: str,
) -> bool:
    physical = _normalize_particle(physical_particle)
    crossed = _normalize_particle(crossed_field)

    if physical == crossed:
        return True

    try:
        return conjugate(physical) == crossed
    except Exception:
        return False


def _attachments_for_vertex(
    candidate: TreeTopologyCandidate,
    vertex_id: str,
):
    return tuple(
        attachment
        for attachment in candidate.external_attachments
        if attachment.vertex_instance == vertex_id
    )


def _propagators_for_vertex(
    candidate: TreeTopologyCandidate,
    vertex_id: str,
):
    return tuple(
        propagator
        for propagator in candidate.internal_propagators
        if (
            propagator.vertex_a == vertex_id
            or propagator.vertex_b == vertex_id
        )
    )


def _w_charge_requirements(fields) -> set[str]:
    normalized = _normalized_fields(fields)

    requirements: set[str] = set()

    if "w_plus" in normalized:
        requirements.add("w_plus")

    if "w_minus" in normalized:
        requirements.add("w_minus")

    return requirements


def _required_internal_w_field(
    candidate: TreeTopologyCandidate,
    vertex,
    propagator,
) -> str | None:
    """
    Determine which W field is required at this endpoint.

    The catalog vertex tells us whether this endpoint contains W+ or W-.
    The propagator connects two vertices, so the opposite endpoint must
    carry the conjugate W field.
    """

    fields = _normalized_fields(vertex.particles)

    if "w_plus" in fields:
        return "w_plus"

    if "w_minus" in fields:
        return "w_minus"

    return None


def _validate_internal_w_orientation(
    candidate: TreeTopologyCandidate,
    propagator,
) -> tuple[str, str | None]:

    particle = _normalize_particle(
        propagator.particle
    )

    if particle not in {"w_plus", "w_minus"}:
        return "ALLOWED", None

    vertex_a = next(
        (
            vertex
            for vertex in candidate.vertices
            if vertex.instance_id == propagator.vertex_a
        ),
        None,
    )

    vertex_b = next(
        (
            vertex
            for vertex in candidate.vertices
            if vertex.instance_id == propagator.vertex_b
        ),
        None,
    )

    if vertex_a is None or vertex_b is None:
        return (
            "FORBIDDEN",
            "W propagator references a missing vertex.",
        )

    required_a = _required_internal_w_field(
        candidate,
        vertex_a,
        propagator,
    )

    required_b = _required_internal_w_field(
        candidate,
        vertex_b,
        propagator,
    )

    if required_a is None or required_b is None:
        return (
            "UNDECIDABLE",
            (
                f"Internal propagator {propagator.line_id} is a W field, "
                "but one connected vertex does not explicitly expose "
                "a W+ or W- catalog field."
            ),
        )

    # A charged W propagator must connect conjugate charged fields.
    if required_a == required_b:
        return (
            "FORBIDDEN",
            (
                f"Internal propagator {propagator.line_id} requires "
                f"conjugate W fields, but both endpoints require "
                f"{required_a}."
            ),
        )

    expected_pair = {
        required_a,
        required_b,
    }

    if expected_pair != {"w_plus", "w_minus"}:
        return (
            "FORBIDDEN",
            (
                f"Internal propagator {propagator.line_id} has an "
                "inconsistent W+ / W- endpoint assignment."
            ),
        )

    return "ALLOWED", None


def validate_vertex_orientation(
    candidate: TreeTopologyCandidate,
    vertex,
) -> VertexOrientationResult:

    reasons: list[str] = []

    fields = _normalized_fields(vertex.particles)

    # External physical particles must be compatible with the crossed
    # fields represented by their catalog vertex.
    for attachment in _attachments_for_vertex(
        candidate,
        vertex.instance_id,
    ):
        if not _field_matches(
            attachment.physical_particle,
            attachment.crossed_field,
        ):
            reasons.append(
                f"External leg {attachment.leg_id} has physical particle "
                f"{attachment.physical_particle} incompatible with crossed "
                f"field {attachment.crossed_field} at vertex "
                f"{vertex.instance_id}."
            )

    # Self-conjugate internal fields require no orientation.
    #
    # photon, gluon, Z and Higgs are all self-conjugate.
    for propagator in _propagators_for_vertex(
        candidate,
        vertex.instance_id,
    ):
        particle = _normalize_particle(
            propagator.particle
        )

        if is_self_conjugate(particle):
            continue

    if reasons:
        return VertexOrientationResult(
            status="FORBIDDEN",
            reasons=tuple(reasons),
        )

    return VertexOrientationResult(
        status="ALLOWED",
        reasons=(),
    )


def validate_candidate_vertex_orientations(
    candidate: TreeTopologyCandidate,
) -> tuple[VertexOrientationResult, ...]:

    results = []

    for vertex in candidate.vertices:
        results.append(
            validate_vertex_orientation(
                candidate,
                vertex,
            )
        )

    return tuple(results)


def candidate_orientation_status(
    candidate: TreeTopologyCandidate,
) -> tuple[str, tuple[str, ...]]:

    forbidden: list[str] = []
    undecidable: list[str] = []

    # Validate external-field orientation at every vertex.
    for result in validate_candidate_vertex_orientations(candidate):

        if result.status == "FORBIDDEN":
            forbidden.extend(result.reasons)

        elif result.status == "UNDECIDABLE":
            undecidable.extend(result.reasons)

    # Validate every internal W propagator using both connected
    # catalog vertices.
    for propagator in candidate.internal_propagators:

        particle = _normalize_particle(
            propagator.particle
        )

        if particle not in {"w_plus", "w_minus"}:
            continue

        status, reason = _validate_internal_w_orientation(
            candidate,
            propagator,
        )

        if status == "FORBIDDEN" and reason:
            forbidden.append(reason)

        elif status == "UNDECIDABLE" and reason:
            undecidable.append(reason)

    if forbidden:
        return "FORBIDDEN", tuple(forbidden)

    if undecidable:
        return "UNDECIDABLE", tuple(undecidable)

    return "ALLOWED", ()


def validate_candidates_orientation(
    candidates,
):
    return tuple(
        candidate_orientation_status(candidate)
        for candidate in candidates
    )
