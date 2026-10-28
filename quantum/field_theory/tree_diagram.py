from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ExternalLeg:
    leg_id: str
    particle: str
    role: str
    momentum: str


@dataclass(frozen=True)
class InternalLine:
    line_id: str
    particle: str
    from_vertex: str
    to_vertex: str
    momentum: str


@dataclass(frozen=True)
class VertexConnection:
    vertex_id: str
    interaction: str
    theory: str
    external_legs: tuple[str, ...]
    internal_lines: tuple[str, ...]
    factor: str


@dataclass(frozen=True)
class TreeDiagram:
    diagram_id: str
    process: str
    topology: str
    theory: str
    external_legs: tuple[ExternalLeg, ...]
    internal_lines: tuple[InternalLine, ...]
    vertices: tuple[VertexConnection, ...]
    status: str = "candidate"

    @property
    def vertex_count(self) -> int:
        return len(self.vertices)

    @property
    def internal_line_count(self) -> int:
        return len(self.internal_lines)


def create_external_legs(
    initial_particles: list[str],
    final_particles: list[str],
) -> tuple[ExternalLeg, ...]:
    legs = []

    for index, particle in enumerate(initial_particles, start=1):
        legs.append(
            ExternalLeg(
                leg_id=f"in{index}",
                particle=particle.strip().lower(),
                role="initial",
                momentum=f"p{index}",
            )
        )

    offset = len(initial_particles)

    for index, particle in enumerate(final_particles, start=1):
        legs.append(
            ExternalLeg(
                leg_id=f"out{index}",
                particle=particle.strip().lower(),
                role="final",
                momentum=f"k{index + offset}",
            )
        )

    return tuple(legs)


def create_tree_diagram(
    *,
    diagram_id: str,
    initial_particles: list[str],
    final_particles: list[str],
    topology: str,
    theory: str,
    vertices: tuple[VertexConnection, ...],
    internal_lines: tuple[InternalLine, ...] = (),
) -> TreeDiagram:
    external_legs = create_external_legs(
        initial_particles,
        final_particles,
    )

    process = (
        " + ".join(initial_particles)
        + " → "
        + " + ".join(final_particles)
    )

    return TreeDiagram(
        diagram_id=diagram_id,
        process=process,
        topology=topology,
        theory=theory,
        external_legs=external_legs,
        internal_lines=internal_lines,
        vertices=vertices,
    )


def diagram_summary(diagram: TreeDiagram) -> dict:
    return {
        "diagram_id": diagram.diagram_id,
        "process": diagram.process,
        "topology": diagram.topology,
        "theory": diagram.theory,
        "vertex_count": diagram.vertex_count,
        "internal_line_count": diagram.internal_line_count,
        "external_leg_count": len(diagram.external_legs),
        "status": diagram.status,
    }
