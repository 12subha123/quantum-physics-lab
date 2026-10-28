from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(frozen=True)
class DiagramLine:
    line_id: str
    role: str
    particle: str
    symbol: str
    momentum: str
    direction: str
    field_type: str


@dataclass(frozen=True)
class DiagramVertex:
    vertex_id: str
    interaction: str
    theory: str
    position: str
    connected_lines: tuple[str, ...]
    factor: str


@dataclass(frozen=True)
class FeynmanDiagram:
    diagram_id: str
    topology: str
    channel: str
    theory: str
    process: str
    internal_particle: Optional[str]
    internal_symbol: Optional[str]
    lines: tuple[DiagramLine, ...]
    vertices: tuple[DiagramVertex, ...]
    amplitude_structure: str
    description: str


PARTICLE_SYMBOLS = {
    "electron": "e⁻",
    "positron": "e⁺",
    "muon": "μ⁻",
    "antimuon": "μ⁺",
    "tau": "τ⁻",
    "antitau": "τ⁺",
    "up_quark": "u",
    "anti_up_quark": "ū",
    "down_quark": "d",
    "anti_down_quark": "d̄",
    "strange_quark": "s",
    "anti_strange_quark": "s̄",
    "photon": "γ",
    "gluon": "g",
    "W_plus": "W⁺",
    "W_minus": "W⁻",
    "Z": "Z",
}


LEPTON_PAIRS = {
    ("electron", "positron"),
    ("muon", "antimuon"),
    ("tau", "antitau"),
}


CHARGED_LEPTONS = {
    "electron",
    "positron",
    "muon",
    "antimuon",
    "tau",
    "antitau",
}


def _symbol(particle: str) -> str:
    return PARTICLE_SYMBOLS.get(particle, particle)


def _is_particle_antiparticle_pair(a: str, b: str) -> bool:
    return (a, b) in LEPTON_PAIRS or (b, a) in LEPTON_PAIRS


def _same_fermion(a: str, b: str) -> bool:
    pairs = {
        frozenset(("electron", "electron")),
        frozenset(("muon", "muon")),
        frozenset(("tau", "tau")),
    }
    return frozenset((a, b)) in pairs


def _same_lepton_flavor_pair(
    initial: list[str],
    final: list[str],
) -> bool:
    return (
        set(initial) == set(final)
        and len(initial) == 2
        and len(final) == 2
    )


def _line(
    line_id: str,
    role: str,
    particle: str,
    momentum: str,
    direction: str,
    field_type: str = "fermion",
) -> DiagramLine:
    return DiagramLine(
        line_id=line_id,
        role=role,
        particle=particle,
        symbol=_symbol(particle),
        momentum=momentum,
        direction=direction,
        field_type=field_type,
    )


def _serialize(diagram: FeynmanDiagram) -> dict:
    return {
        "diagram_id": diagram.diagram_id,
        "topology": diagram.topology,
        "channel": diagram.channel,
        "theory": diagram.theory,
        "process": diagram.process,
        "internal_particle": diagram.internal_particle,
        "internal_symbol": diagram.internal_symbol,
        "lines": [asdict(line) for line in diagram.lines],
        "vertices": [asdict(vertex) for vertex in diagram.vertices],
        "amplitude_structure": diagram.amplitude_structure,
        "description": diagram.description,
    }


def _s_channel_annihilation(
    initial: list[str],
    final: list[str],
    diagram_id: str = "qed_s_channel",
) -> FeynmanDiagram:
    process = (
        f"{_symbol(initial[0])} + {_symbol(initial[1])} "
        f"→ {_symbol(final[0])} + {_symbol(final[1])}"
    )

    lines = (
        _line("i1", "incoming", initial[0], "p1", "toward_vertex"),
        _line("i2", "incoming", initial[1], "p2", "toward_vertex"),
        _line("x1", "internal", "photon", "q=p1+p2", "between_vertices", "boson"),
        _line("f1", "outgoing", final[0], "p3", "away_from_vertex"),
        _line("f2", "outgoing", final[1], "p4", "away_from_vertex"),
    )

    vertices = (
        DiagramVertex(
            vertex_id="V1",
            interaction="fermion-photon-fermion",
            theory="QED",
            position="left",
            connected_lines=("i1", "i2", "x1"),
            factor="-ie gamma^mu",
        ),
        DiagramVertex(
            vertex_id="V2",
            interaction="fermion-photon-fermion",
            theory="QED",
            position="right",
            connected_lines=("x1", "f1", "f2"),
            factor="-ie gamma^mu",
        ),
    )

    return FeynmanDiagram(
        diagram_id=diagram_id,
        topology="s-channel",
        channel="s",
        theory="QED",
        process=process,
        internal_particle="photon",
        internal_symbol="γ*",
        lines=lines,
        vertices=vertices,
        amplitude_structure=(
            "M_s = [vbar(p2)(-ie gamma^mu)u(p1)] "
            "[-i g_mu_nu / s] "
            "[ubar(p3)(-ie gamma^nu)v(p4)]"
        ),
        description=(
            "Particle-antiparticle annihilation through a virtual photon. "
            "The exchanged photon carries the total incoming four-momentum."
        ),
    )


def _t_channel_scattering(
    initial: list[str],
    final: list[str],
    diagram_id: str = "qed_t_channel",
) -> FeynmanDiagram:
    process = (
        f"{_symbol(initial[0])} + {_symbol(initial[1])} "
        f"→ {_symbol(final[0])} + {_symbol(final[1])}"
    )

    lines = (
        _line("i1", "incoming", initial[0], "p1", "toward_vertex"),
        _line("i2", "incoming", initial[1], "p2", "toward_vertex"),
        _line("x1", "internal", "photon", "q=p1-p3", "between_vertices", "boson"),
        _line("f1", "outgoing", final[0], "p3", "away_from_vertex"),
        _line("f2", "outgoing", final[1], "p4", "away_from_vertex"),
    )

    vertices = (
        DiagramVertex(
            vertex_id="V1",
            interaction="fermion-photon-fermion",
            theory="QED",
            position="upper",
            connected_lines=("i1", "f1", "x1"),
            factor="-ie gamma^mu",
        ),
        DiagramVertex(
            vertex_id="V2",
            interaction="fermion-photon-fermion",
            theory="QED",
            position="lower",
            connected_lines=("i2", "f2", "x1"),
            factor="-ie gamma^mu",
        ),
    )

    return FeynmanDiagram(
        diagram_id=diagram_id,
        topology="t-channel",
        channel="t",
        theory="QED",
        process=process,
        internal_particle="photon",
        internal_symbol="γ*",
        lines=lines,
        vertices=vertices,
        amplitude_structure=(
            "M_t = [ubar(p3)(-ie gamma^mu)u(p1)] "
            "[-i g_mu_nu / t] "
            "[ubar(p4)(-ie gamma^nu)u(p2)]"
        ),
        description=(
            "Elastic charged-fermion scattering through virtual-photon "
            "exchange. The photon transfers four-momentum between the fermion lines."
        ),
    )


def _u_channel_scattering(
    initial: list[str],
    final: list[str],
    diagram_id: str = "qed_u_channel",
) -> FeynmanDiagram:
    process = (
        f"{_symbol(initial[0])} + {_symbol(initial[1])} "
        f"→ {_symbol(final[0])} + {_symbol(final[1])}"
    )

    lines = (
        _line("i1", "incoming", initial[0], "p1", "toward_vertex"),
        _line("i2", "incoming", initial[1], "p2", "toward_vertex"),
        _line("x1", "internal", "photon", "q=p1-p4", "between_vertices", "boson"),
        _line("f1", "outgoing", final[0], "p3", "away_from_vertex"),
        _line("f2", "outgoing", final[1], "p4", "away_from_vertex"),
    )

    vertices = (
        DiagramVertex(
            vertex_id="V1",
            interaction="fermion-photon-fermion",
            theory="QED",
            position="upper",
            connected_lines=("i1", "f2", "x1"),
            factor="-ie gamma^mu",
        ),
        DiagramVertex(
            vertex_id="V2",
            interaction="fermion-photon-fermion",
            theory="QED",
            position="lower",
            connected_lines=("i2", "f1", "x1"),
            factor="-ie gamma^mu",
        ),
    )

    return FeynmanDiagram(
        diagram_id=diagram_id,
        topology="u-channel",
        channel="u",
        theory="QED",
        process=process,
        internal_particle="photon",
        internal_symbol="γ*",
        lines=lines,
        vertices=vertices,
        amplitude_structure=(
            "M_u = [ubar(p4)(-ie gamma^mu)u(p1)] "
            "[-i g_mu_nu / u] "
            "[ubar(p3)(-ie gamma^nu)u(p2)]"
        ),
        description=(
            "Crossed elastic-scattering contribution. It is required when "
            "identical fermions make the final-state assignments physically indistinguishable."
        ),
    )


def _bhabha_diagrams(
    initial: list[str],
    final: list[str],
) -> list[FeynmanDiagram]:
    return [
        _s_channel_annihilation(
            initial,
            final,
            "bhabha_s_channel",
        ),
        _t_channel_scattering(
            initial,
            final,
            "bhabha_t_channel",
        ),
    ]


def _moller_diagrams(
    initial: list[str],
    final: list[str],
) -> list[FeynmanDiagram]:
    return [
        _t_channel_scattering(
            initial,
            final,
            "moller_t_channel",
        ),
        _u_channel_scattering(
            initial,
            final,
            "moller_u_channel",
        ),
    ]


def generate_feynman_diagrams(
    initial_particles: list[str],
    final_particles: list[str],
) -> dict:
    if len(initial_particles) != 2:
        raise ValueError("This engine currently requires exactly two initial particles.")

    if len(final_particles) != 2:
        raise ValueError("This engine currently requires exactly two final particles.")

    initial = list(initial_particles)
    final = list(final_particles)

    supported = CHARGED_LEPTONS

    if not all(p in supported for p in initial + final):
        return {
            "success": True,
            "process": (
                f"{', '.join(initial)} → {', '.join(final)}"
            ),
            "initial_particles": initial,
            "final_particles": final,
            "diagram_count": 0,
            "diagrams": [],
            "interaction_analysis": {
                "theory": "QED",
                "status": "not_yet_supported",
            },
            "limitations": [
                "This topology engine currently generates elementary charged-lepton QED diagrams.",
                "Quarks, gluons, weak interactions and composite hadrons are handled by later layers.",
                "No loop diagrams are generated.",
                "No renormalization is included.",
            ],
        }

    diagrams = []

    # e- e+ -> mu- mu+ and analogous different-flavor annihilation.
    if (
        _is_particle_antiparticle_pair(initial[0], initial[1])
        and _is_particle_antiparticle_pair(final[0], final[1])
        and set(initial) != set(final)
    ):
        diagrams.append(
            _s_channel_annihilation(
                initial,
                final,
                "qed_s_channel_annihilation",
            )
        )

    # Bhabha scattering:
    # e- e+ -> e- e+, and analogous same-flavor lepton scattering.
    elif (
        _is_particle_antiparticle_pair(initial[0], initial[1])
        and _same_lepton_flavor_pair(initial, final)
    ):
        diagrams.extend(_bhabha_diagrams(initial, final))

    # Moller scattering:
    # e- e- -> e- e-, mu- mu- -> mu- mu-, etc.
    elif (
        initial[0] == initial[1]
        and final[0] == final[1]
        and _same_fermion(initial[0], initial[1])
        and initial[0] == final[0]
    ):
        diagrams.extend(_moller_diagrams(initial, final))

    # Ordinary elastic scattering with distinguishable charged leptons.
    elif (
        initial[0] in supported
        and initial[1] in supported
        and final[0] in supported
        and final[1] in supported
        and initial == final
    ):
        diagrams.append(
            _t_channel_scattering(
                initial,
                final,
                "qed_t_channel_elastic",
            )
        )

    return {
        "success": True,
        "process": (
            f"{_symbol(initial[0])} + {_symbol(initial[1])} "
            f"→ {_symbol(final[0])} + {_symbol(final[1])}"
        ),
        "initial_particles": initial,
        "final_particles": final,
        "diagram_count": len(diagrams),
        "diagrams": [_serialize(diagram) for diagram in diagrams],
        "interaction_analysis": {
            "theory": "QED",
            "channels": [diagram.channel for diagram in diagrams],
            "internal_particles": [
                diagram.internal_particle
                for diagram in diagrams
            ],
            "interference_required": len(diagrams) > 1,
        },
        "limitations": [
            "This is the first topology-aware elementary QED layer.",
            "The amplitudes are represented symbolically; spinor contractions are not yet numerically evaluated.",
            "The next layer will construct numerical amplitudes from the generated diagrams.",
            "Loop corrections and renormalization are not included.",
            "Composite proton/neutron interactions require a separate hadronic model.",
        ],
    }
