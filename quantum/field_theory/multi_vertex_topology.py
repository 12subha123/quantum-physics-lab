from __future__ import annotations

from dataclasses import dataclass

from quantum.field_theory.particle_process import create_process
from quantum.field_theory.tree_diagram import (
    ExternalLeg,
    InternalLine,
    TreeDiagram,
    VertexConnection,
)


@dataclass(frozen=True)
class VertexTemplate:
    vertex_id: str
    interaction: str
    theory: str
    particle_pattern: tuple[str, ...]
    factor: str


@dataclass(frozen=True)
class TopologySearchResult:
    success: bool
    process: str
    topology: str
    candidate_count: int
    diagrams: tuple[TreeDiagram, ...]
    scientific_scope: str


QED_VERTEX_TEMPLATES = (
    VertexTemplate(
        vertex_id="qed_fermion_photon",
        interaction="qed_fermion_photon",
        theory="QED",
        particle_pattern=("fermion", "antifermion", "photon"),
        factor="-ieγ^μ",
    ),
)


def _normalise(value: str) -> str:
    return value.strip().lower().replace("_", "-")


def _category(particle: str) -> str:
    name = _normalise(particle)

    if name in {"electron", "muon", "tau"}:
        return "fermion"

    if name in {"positron", "antimuon", "antitau"}:
        return "antifermion"

    if name == "photon":
        return "photon"

    return name


def _contains_all(values: list[str], required: list[str]) -> bool:
    available = [_normalise(value) for value in values]
    return all(_normalise(value) in available for value in required)


def _is_qed_vertex_triplet(
    particles: list[str],
) -> bool:
    categories = sorted(_category(particle) for particle in particles)

    return categories == [
        "antifermion",
        "fermion",
        "photon",
    ]


def _external_leg(
    leg_id: str,
    particle: str,
    role: str,
) -> ExternalLeg:
    return ExternalLeg(
        leg_id=leg_id,
        particle=particle,
        role=role,
        momentum=leg_id,
    )


def _external_qed_radiation_candidates(
    initial_particles: list[str],
    final_particles: list[str],
) -> list[TreeDiagram]:
    initial = [_normalise(p) for p in initial_particles]
    final = [_normalise(p) for p in final_particles]

    if not _contains_all(initial, ["electron", "positron"]):
        return []

    if not _contains_all(final, ["muon", "antimuon", "photon"]):
        return []

    if len(initial) != 2 or len(final) != 3:
        return []

    diagrams: list[TreeDiagram] = []

    # ------------------------------------------------------------
    # Candidate 1:
    #
    # e- + e+ -> gamma* -> mu- + mu+,
    # with photon radiation from the outgoing mu- line.
    #
    # v1 -- l1(photon) -- v2 -- l2(muon) -- v3
    # ------------------------------------------------------------

    legs_1 = (
        _external_leg("in1", "electron", "incoming"),
        _external_leg("in2", "positron", "incoming"),
        _external_leg("out1", "muon", "outgoing"),
        _external_leg("out2", "antimuon", "outgoing"),
        _external_leg("out3", "photon", "outgoing"),
    )

    lines_1 = (
        InternalLine(
            line_id="l1",
            particle="photon",
            from_vertex="v1",
            to_vertex="v2",
            momentum="q",
        ),
        InternalLine(
            line_id="l2",
            particle="muon",
            from_vertex="v2",
            to_vertex="v3",
            momentum="k1",
        ),
    )

    vertices_1 = (
        VertexConnection(
            vertex_id="v1",
            interaction="qed_fermion_photon",
            theory="QED",
            external_legs=("in1", "in2"),
            internal_lines=("l1",),
            factor="-ieγ^μ",
        ),
        VertexConnection(
            vertex_id="v2",
            interaction="qed_fermion_photon",
            theory="QED",
            external_legs=("out2",),
            internal_lines=("l1", "l2"),
            factor="-ieγ^ν",
        ),
        VertexConnection(
            vertex_id="v3",
            interaction="qed_fermion_photon",
            theory="QED",
            external_legs=("out1", "out3"),
            internal_lines=("l2",),
            factor="-ieγ^ρ",
        ),
    )

    diagrams.append(
        TreeDiagram(
            diagram_id="qed_annihilation_final_radiation_out1",
            process="electron + positron → muon + antimuon + photon",
            topology="s-channel-final-state-radiation",
            theory="QED",
            external_legs=legs_1,
            internal_lines=lines_1,
            vertices=vertices_1,
            status="candidate",
        )
    )

    # ------------------------------------------------------------
    # Candidate 2:
    #
    # Same production topology, but photon radiation from the
    # outgoing antimuon line.
    #
    # v1 -- l1(photon) -- v2 -- l2(antimuon) -- v3
    # ------------------------------------------------------------

    legs_2 = (
        _external_leg("in1", "electron", "incoming"),
        _external_leg("in2", "positron", "incoming"),
        _external_leg("out1", "muon", "outgoing"),
        _external_leg("out2", "antimuon", "outgoing"),
        _external_leg("out3", "photon", "outgoing"),
    )

    lines_2 = (
        InternalLine(
            line_id="l1",
            particle="photon",
            from_vertex="v1",
            to_vertex="v2",
            momentum="q",
        ),
        InternalLine(
            line_id="l2",
            particle="antimuon",
            from_vertex="v2",
            to_vertex="v3",
            momentum="k2",
        ),
    )

    vertices_2 = (
        VertexConnection(
            vertex_id="v1",
            interaction="qed_fermion_photon",
            theory="QED",
            external_legs=("in1", "in2"),
            internal_lines=("l1",),
            factor="-ieγ^μ",
        ),
        VertexConnection(
            vertex_id="v2",
            interaction="qed_fermion_photon",
            theory="QED",
            external_legs=("out1",),
            internal_lines=("l1", "l2"),
            factor="-ieγ^ν",
        ),
        VertexConnection(
            vertex_id="v3",
            interaction="qed_fermion_photon",
            theory="QED",
            external_legs=("out2", "out3"),
            internal_lines=("l2",),
            factor="-ieγ^ρ",
        ),
    )

    diagrams.append(
        TreeDiagram(
            diagram_id="qed_annihilation_final_radiation_out2",
            process="electron + positron → muon + antimuon + photon",
            topology="s-channel-final-state-radiation",
            theory="QED",
            external_legs=legs_2,
            internal_lines=lines_2,
            vertices=vertices_2,
            status="candidate",
        )
    )

    return diagrams


def search_tree_level_topologies(
    initial_particles: list[str],
    final_particles: list[str],
) -> TopologySearchResult:
    process = create_process(
        initial_particles,
        final_particles,
    )

    diagrams = _external_qed_radiation_candidates(
        list(process.initial_particles),
        list(process.final_particles),
    )

    topology = (
        diagrams[0].topology
        if diagrams
        else "not_yet_supported"
    )

    return TopologySearchResult(
        success=True,
        process=process.notation,
        topology=topology,
        candidate_count=len(diagrams),
        diagrams=tuple(diagrams),
        scientific_scope=(
            "Tree-level candidate topology generation for selected "
            "QED multi-vertex processes. Candidates must pass "
            "vertex-flow, field-content, charge, momentum-flow, and "
            "kinematic validation before being treated as physical "
            "Feynman diagrams. This layer does not yet calculate "
            "complete amplitudes or cross sections."
        ),
    )


def topology_search_summary(
    initial_particles: list[str],
    final_particles: list[str],
) -> dict:
    result = search_tree_level_topologies(
        initial_particles,
        final_particles,
    )

    return {
        "success": result.success,
        "process": result.process,
        "topology": result.topology,
        "candidate_count": result.candidate_count,
        "diagrams": [
            {
                "diagram_id": diagram.diagram_id,
                "process": diagram.process,
                "topology": diagram.topology,
                "theory": diagram.theory,
                "external_leg_count": len(diagram.external_legs),
                "internal_line_count": len(diagram.internal_lines),
                "vertex_count": len(diagram.vertices),
                "status": diagram.status,
            }
            for diagram in result.diagrams
        ],
        "scientific_scope": result.scientific_scope,
    }
