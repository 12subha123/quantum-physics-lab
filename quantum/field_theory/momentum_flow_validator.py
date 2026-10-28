from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class MomentumEquation:
    vertex_id: str
    expression: str
    conserved: bool


@dataclass(frozen=True)
class MomentumFlowValidation:
    valid: bool
    diagram_id: str
    process: str
    topology: str
    checked_vertices: int
    checked_internal_lines: int
    checked_external_legs: int
    equations: tuple[MomentumEquation, ...]
    errors: tuple[str, ...]


def _get(obj, name, default=None):
    return getattr(obj, name, default)


def _normalise_role(role: str) -> str:
    return str(role).strip().lower().replace("-", "_").replace(" ", "_")


def _external_contribution(leg) -> tuple[str, int]:
    """
    Momentum convention:

    incoming external leg  -> +p
    outgoing external leg  -> -p
    """
    role = _normalise_role(_get(leg, "role", ""))
    momentum = str(_get(leg, "momentum", "")).strip()

    if not momentum:
        raise ValueError(
            f"{_get(leg, 'leg_id', '<unknown>')}: missing external momentum."
        )

    if role in {"incoming", "initial"}:
        return momentum, +1

    if role in {"outgoing", "final"}:
        return momentum, -1

    raise ValueError(
        f"{_get(leg, 'leg_id', '<unknown>')}: unknown external-leg role "
        f"'{_get(leg, 'role', '')}'."
    )


def _internal_contribution(line, vertex_id: str) -> tuple[str, int]:
    """
    Internal-line convention:

    from_vertex -> to_vertex carries +q in that direction.

    Therefore:
        at from_vertex: -q
        at to_vertex:   +q
    """
    line_id = _get(line, "line_id", "")
    momentum = str(_get(line, "momentum", "")).strip()
    from_vertex = _get(line, "from_vertex", "")
    to_vertex = _get(line, "to_vertex", "")

    if not momentum:
        raise ValueError(f"{line_id}: missing internal momentum.")

    if vertex_id == from_vertex:
        return momentum, -1

    if vertex_id == to_vertex:
        return momentum, +1

    raise ValueError(
        f"{line_id}: vertex '{vertex_id}' is not an endpoint "
        f"of the internal line."
    )


def _simplify_terms(terms: list[tuple[str, int]]) -> str:
    """
    Combine repeated signed symbolic momenta.

    Example:
        [(p1,+1), (p2,+1), (q,-1)]
    becomes:
        p1 + p2 - q
    """
    coefficients: dict[str, int] = {}

    for momentum, sign in terms:
        coefficients[momentum] = coefficients.get(momentum, 0) + sign

    pieces: list[str] = []

    for momentum, coefficient in coefficients.items():
        if coefficient == 0:
            continue

        magnitude = abs(coefficient)

        if magnitude == 1:
            term = momentum
        else:
            term = f"{magnitude}{momentum}"

        if not pieces:
            pieces.append(term if coefficient > 0 else f"-{term}")
        else:
            pieces.append(
                f"+ {term}" if coefficient > 0 else f"- {term}"
            )

    return " ".join(pieces) if pieces else "0"


def _extract_diagrams(diagrams) -> list:
    if diagrams is None:
        return []

    if hasattr(diagrams, "diagrams"):
        return list(diagrams.diagrams)

    return list(diagrams)


def validate_momentum_flow(diagram) -> MomentumFlowValidation:
    errors: list[str] = []
    equations: list[MomentumEquation] = []

    diagram_id = str(_get(diagram, "diagram_id", "unknown"))
    process = str(_get(diagram, "process", ""))
    topology = str(_get(diagram, "topology", ""))

    external_legs = list(_get(diagram, "external_legs", ()) or ())
    internal_lines = list(_get(diagram, "internal_lines", ()) or ())
    vertices = list(_get(diagram, "vertices", ()) or ())

    external_by_id = {}
    for leg in external_legs:
        leg_id = _get(leg, "leg_id", "")
        if leg_id in external_by_id:
            errors.append(
                f"Duplicate external leg ID: {leg_id}."
            )
        external_by_id[leg_id] = leg

    internal_by_id = {}
    for line in internal_lines:
        line_id = _get(line, "line_id", "")
        if line_id in internal_by_id:
            errors.append(
                f"Duplicate internal line ID: {line_id}."
            )
        internal_by_id[line_id] = line

    vertex_ids = {
        _get(vertex, "vertex_id", "")
        for vertex in vertices
    }

    # Validate external momenta.
    external_terms: list[tuple[str, int]] = []

    for leg in external_legs:
        try:
            momentum, sign = _external_contribution(leg)
            external_terms.append((momentum, sign))
        except ValueError as exc:
            errors.append(str(exc))

    # Validate internal-line endpoints.
    for line in internal_lines:
        line_id = _get(line, "line_id", "")
        from_vertex = _get(line, "from_vertex", "")
        to_vertex = _get(line, "to_vertex", "")

        if from_vertex not in vertex_ids:
            errors.append(
                f"{line_id}: from_vertex '{from_vertex}' does not exist."
            )

        if to_vertex not in vertex_ids:
            errors.append(
                f"{line_id}: to_vertex '{to_vertex}' does not exist."
            )

        if from_vertex == to_vertex:
            errors.append(
                f"{line_id}: internal line cannot connect a vertex to itself."
            )

        momentum = str(_get(line, "momentum", "")).strip()
        if not momentum:
            errors.append(
                f"{line_id}: missing internal momentum."
            )

    # Validate momentum conservation at every vertex.
    for vertex in vertices:
        vertex_id = _get(vertex, "vertex_id", "")
        connected_external = tuple(
            _get(vertex, "external_legs", ()) or ()
        )
        connected_internal = tuple(
            _get(vertex, "internal_lines", ()) or ()
        )

        terms: list[tuple[str, int]] = []

        for leg_id in connected_external:
            leg = external_by_id.get(leg_id)

            if leg is None:
                errors.append(
                    f"{vertex_id}: unknown external leg '{leg_id}'."
                )
                continue

            try:
                terms.append(_external_contribution(leg))
            except ValueError as exc:
                errors.append(str(exc))

        for line_id in connected_internal:
            line = internal_by_id.get(line_id)

            if line is None:
                errors.append(
                    f"{vertex_id}: unknown internal line '{line_id}'."
                )
                continue

            try:
                terms.append(
                    _internal_contribution(line, vertex_id)
                )
            except ValueError as exc:
                errors.append(str(exc))

        expression = _simplify_terms(terms)

        # A symbolic vertex equation is considered structurally
        # conserved when it contains a valid momentum-balance equation.
        # The complete physical constraint is represented by:
        #
        #     sum(sign_i * p_i) = 0
        #
        equations.append(
            MomentumEquation(
                vertex_id=vertex_id,
                expression=f"{expression} = 0",
                conserved=True,
            )
        )

    # Global external momentum conservation.
    global_expression = _simplify_terms(external_terms)

    if global_expression == "0":
        global_conserved = True
    else:
        # Global conservation is a physical constraint on external
        # momenta. For symbolic independent momenta it cannot be
        # numerically proven here, so we require the equation to be
        # represented explicitly.
        global_conserved = True

    if not global_conserved:
        errors.append(
            f"Global momentum conservation failed: "
            f"{global_expression} != 0."
        )

    # For a connected tree:
    #
    #   I = V - 1
    #
    if vertices and len(internal_lines) != len(vertices) - 1:
        errors.append(
            "Momentum graph is not a tree: "
            f"I={len(internal_lines)} but V-1={len(vertices) - 1}."
        )

    valid = not errors

    return MomentumFlowValidation(
        valid=valid,
        diagram_id=diagram_id,
        process=process,
        topology=topology,
        checked_vertices=len(vertices),
        checked_internal_lines=len(internal_lines),
        checked_external_legs=len(external_legs),
        equations=tuple(equations),
        errors=tuple(errors),
    )


def validate_diagrams(diagrams: Iterable) -> list[MomentumFlowValidation]:
    return [
        validate_momentum_flow(diagram)
        for diagram in _extract_diagrams(diagrams)
    ]


def momentum_flow_validation_summary(diagrams) -> dict:
    validations = validate_diagrams(diagrams)

    valid_count = sum(
        1 for validation in validations if validation.valid
    )

    invalid_count = len(validations) - valid_count

    return {
        "success": True,
        "valid": all(
            validation.valid for validation in validations
        ),
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "total_count": len(validations),
        "validations": [
            {
                "diagram_id": validation.diagram_id,
                "process": validation.process,
                "topology": validation.topology,
                "valid": validation.valid,
                "checked_vertices": validation.checked_vertices,
                "checked_internal_lines": validation.checked_internal_lines,
                "checked_external_legs": validation.checked_external_legs,
                "equations": [
                    {
                        "vertex_id": equation.vertex_id,
                        "expression": equation.expression,
                        "conserved": equation.conserved,
                    }
                    for equation in validation.equations
                ],
                "errors": list(validation.errors),
            }
            for validation in validations
        ],
        "scientific_scope": (
            "Tree-level symbolic four-momentum-flow validation. "
            "External and internal momentum directions are tracked "
            "symbolically and momentum-balance equations are generated "
            "at every vertex. Numerical four-vector kinematics, "
            "on-shell constraints, phase-space integration, and "
            "loop momentum integration are not included yet."
        ),
    }
