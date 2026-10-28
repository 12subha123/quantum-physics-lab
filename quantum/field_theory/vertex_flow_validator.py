from __future__ import annotations

from dataclasses import dataclass

from quantum.field_theory.tree_diagram import TreeDiagram


@dataclass(frozen=True)
class VertexFlowValidation:
    valid: bool
    diagram_id: str
    process: str
    topology: str
    checked_vertices: int
    checked_internal_lines: int
    checked_external_legs: int
    errors: tuple[str, ...]

    def summary(self) -> dict:
        return {
            "valid": self.valid,
            "diagram_id": self.diagram_id,
            "process": self.process,
            "topology": self.topology,
            "checked_vertices": self.checked_vertices,
            "checked_internal_lines": self.checked_internal_lines,
            "checked_external_legs": self.checked_external_legs,
            "errors": list(self.errors),
        }


def _extract_diagrams(source) -> list[TreeDiagram]:
    if isinstance(source, list):
        return source

    diagrams = getattr(source, "diagrams", None)

    if diagrams is None:
        raise TypeError(
            "Expected a list of TreeDiagram objects or an object "
            "with a 'diagrams' attribute."
        )

    return list(diagrams)


def validate_tree_diagram(diagram: TreeDiagram) -> VertexFlowValidation:
    errors: list[str] = []

    external_ids = {
        leg.leg_id
        for leg in diagram.external_legs
    }

    internal_ids = {
        line.line_id
        for line in diagram.internal_lines
    }

    if len(external_ids) != len(diagram.external_legs):
        errors.append("Duplicate external-leg IDs detected.")

    if len(internal_ids) != len(diagram.internal_lines):
        errors.append("Duplicate internal-line IDs detected.")

    vertex_ids: set[str] = set()

    for vertex in diagram.vertices:
        if vertex.vertex_id in vertex_ids:
            errors.append(
                f"Duplicate vertex ID: {vertex.vertex_id}"
            )

        vertex_ids.add(vertex.vertex_id)

        for leg_id in vertex.external_legs:
            if leg_id not in external_ids:
                errors.append(
                    f"Vertex {vertex.vertex_id} references unknown "
                    f"external leg {leg_id}."
                )

        for line_id in vertex.internal_lines:
            if line_id not in internal_ids:
                errors.append(
                    f"Vertex {vertex.vertex_id} references unknown "
                    f"internal line {line_id}."
                )

    external_usage = {
        leg_id: 0
        for leg_id in external_ids
    }

    for vertex in diagram.vertices:
        for leg_id in vertex.external_legs:
            if leg_id in external_usage:
                external_usage[leg_id] += 1

    for leg_id, count in external_usage.items():
        if count != 1:
            errors.append(
                f"External leg {leg_id} is connected {count} times; "
                "expected exactly once."
            )

    internal_usage = {
        line_id: 0
        for line_id in internal_ids
    }

    for vertex in diagram.vertices:
        for line_id in vertex.internal_lines:
            if line_id in internal_usage:
                internal_usage[line_id] += 1

    for line_id, count in internal_usage.items():
        if count != 2:
            errors.append(
                f"Internal line {line_id} is connected to {count} vertices; "
                "expected exactly two."
            )

    vertex_map = {
        vertex.vertex_id: vertex
        for vertex in diagram.vertices
    }

    for line in diagram.internal_lines:
        if line.from_vertex not in vertex_map:
            errors.append(
                f"Internal line {line.line_id} references missing "
                f"from_vertex {line.from_vertex}."
            )

        if line.to_vertex not in vertex_map:
            errors.append(
                f"Internal line {line.line_id} references missing "
                f"to_vertex {line.to_vertex}."
            )

        if line.from_vertex == line.to_vertex:
            errors.append(
                f"Internal line {line.line_id} connects a vertex to itself."
            )

        if line.from_vertex in vertex_map:
            if line.line_id not in vertex_map[line.from_vertex].internal_lines:
                errors.append(
                    f"Internal line {line.line_id} is missing from "
                    f"{line.from_vertex}'s connection list."
                )

        if line.to_vertex in vertex_map:
            if line.line_id not in vertex_map[line.to_vertex].internal_lines:
                errors.append(
                    f"Internal line {line.line_id} is missing from "
                    f"{line.to_vertex}'s connection list."
                )

    vertex_count = len(diagram.vertices)
    internal_count = len(diagram.internal_lines)

    if vertex_count > 0 and internal_count != vertex_count - 1:
        errors.append(
            "Tree topology condition failed: "
            f"{vertex_count} vertices require {vertex_count - 1} "
            f"internal lines, but found {internal_count}."
        )

    if vertex_count > 1:
        connected_vertex_ids: set[str] = set()

        for line in diagram.internal_lines:
            connected_vertex_ids.add(line.from_vertex)
            connected_vertex_ids.add(line.to_vertex)

        for vertex in diagram.vertices:
            if vertex.vertex_id not in connected_vertex_ids:
                errors.append(
                    f"Vertex {vertex.vertex_id} is disconnected "
                    "from the internal graph."
                )

    return VertexFlowValidation(
        valid=not errors,
        diagram_id=diagram.diagram_id,
        process=diagram.process,
        topology=diagram.topology,
        checked_vertices=vertex_count,
        checked_internal_lines=internal_count,
        checked_external_legs=len(diagram.external_legs),
        errors=tuple(errors),
    )


def validate_diagrams(source) -> list[VertexFlowValidation]:
    diagrams = _extract_diagrams(source)

    return [
        validate_tree_diagram(diagram)
        for diagram in diagrams
    ]


def validation_summary(source) -> dict:
    validations = validate_diagrams(source)

    return {
        "success": True,
        "diagram_count": len(validations),
        "valid_count": sum(item.valid for item in validations),
        "invalid_count": sum(not item.valid for item in validations),
        "valid": all(item.valid for item in validations),
        "validations": [
            item.summary()
            for item in validations
        ],
        "scientific_scope": (
            "Graph-level tree-diagram connectivity validation. "
            "This validates graph structure and external/internal leg "
            "connectivity; it does not by itself prove complete physical "
            "kinematic validity, gauge invariance, or amplitude correctness."
        ),
    }
