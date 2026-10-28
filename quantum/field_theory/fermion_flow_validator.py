from __future__ import annotations

from dataclasses import dataclass

from .oriented_vertex_graph import (
    TreeTopologyCandidate,
    _normalize_particle,
    conjugate,
    is_fermion,
)


@dataclass(frozen=True)
class FermionFlowResult:
    status: str
    reasons: tuple[str, ...]


def _external_attachment_map(candidate):
    return {
        attachment.leg_id: attachment
        for attachment in candidate.external_attachments
    }


def _same_fermion_family(
    physical_particle: str,
    family: str,
) -> bool:
    physical = _normalize_particle(physical_particle)
    family = _normalize_particle(family)

    if not is_fermion(physical):
        return False

    if physical == family:
        return True

    try:
        return conjugate(physical) == family
    except Exception:
        return False


def validate_fermion_flow(
    candidate: TreeTopologyCandidate,
) -> FermionFlowResult:

    attachments = _external_attachment_map(candidate)

    fermion_external_legs = {
        attachment.leg_id
        for attachment in candidate.external_attachments
        if is_fermion(
            _normalize_particle(
                attachment.physical_particle
            )
        )
    }

    represented_legs: list[str] = []
    forbidden: list[str] = []
    undecidable: list[str] = []

    for line in candidate.fermion_lines:

        if not is_fermion(
            _normalize_particle(line.family)
        ):
            forbidden.append(
                f"Fermion line {line.line_id} has non-fermionic "
                f"family {line.family}."
            )
            continue

        endpoints = [
            line.incoming_leg,
            line.outgoing_leg,
        ]

        endpoints = [
            leg
            for leg in endpoints
            if leg is not None
        ]

        if not endpoints:
            forbidden.append(
                f"Fermion line {line.line_id} has no external endpoint."
            )
            continue

        for leg_id in endpoints:

            if leg_id not in attachments:
                forbidden.append(
                    f"Fermion line {line.line_id} references missing "
                    f"external leg {leg_id}."
                )
                continue

            represented_legs.append(leg_id)

            attachment = attachments[leg_id]

            if not is_fermion(
                _normalize_particle(
                    attachment.physical_particle
                )
            ):
                forbidden.append(
                    f"Fermion line {line.line_id} terminates on "
                    f"non-fermionic external particle "
                    f"{attachment.physical_particle}."
                )
                continue

            if not _same_fermion_family(
                attachment.physical_particle,
                line.family,
            ):
                forbidden.append(
                    f"Fermion line {line.line_id} has family "
                    f"{line.family}, incompatible with external "
                    f"particle {attachment.physical_particle}."
                )

        if len(endpoints) == 1:
            undecidable.append(
                f"Fermion line {line.line_id} has only one external "
                "endpoint; complete fermion-flow orientation cannot "
                "yet be established."
            )

        elif len(endpoints) > 2:
            forbidden.append(
                f"Fermion line {line.line_id} has more than two "
                "external endpoints."
            )

        if (
            line.incoming_leg is not None
            and line.outgoing_leg is not None
        ):
            incoming = attachments.get(line.incoming_leg)
            outgoing = attachments.get(line.outgoing_leg)

            if incoming is None or outgoing is None:
                continue

            if incoming.role != "incoming":
                forbidden.append(
                    f"Fermion line {line.line_id} marks "
                    f"{line.incoming_leg} as incoming, but its "
                    "external attachment role disagrees."
                )

            if outgoing.role != "outgoing":
                forbidden.append(
                    f"Fermion line {line.line_id} marks "
                    f"{line.outgoing_leg} as outgoing, but its "
                    "external attachment role disagrees."
                )

    counts: dict[str, int] = {}

    for leg_id in represented_legs:
        counts[leg_id] = counts.get(leg_id, 0) + 1

    for leg_id in fermion_external_legs:

        count = counts.get(leg_id, 0)

        if count == 0:
            undecidable.append(
                f"External fermion leg {leg_id} is not yet represented "
                "by a constructed fermion line."
            )

        elif count > 1:
            forbidden.append(
                f"External fermion leg {leg_id} is represented by "
                "multiple fermion lines."
            )

    if forbidden:
        return FermionFlowResult(
            status="FORBIDDEN",
            reasons=tuple(forbidden),
        )

    if undecidable:
        return FermionFlowResult(
            status="UNDECIDABLE",
            reasons=tuple(undecidable),
        )

    return FermionFlowResult(
        status="ALLOWED",
        reasons=(),
    )


def candidate_fermion_flow_status(
    candidate: TreeTopologyCandidate,
) -> tuple[str, tuple[str, ...]]:

    result = validate_fermion_flow(candidate)

    return result.status, result.reasons


def validate_candidates_fermion_flow(
    candidates,
):
    return tuple(
        candidate_fermion_flow_status(candidate)
        for candidate in candidates
    )
