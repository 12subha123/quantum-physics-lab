from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UniversalExternalLeg:
    leg_id: str
    particle: str
    role: str
    momentum: str


@dataclass(frozen=True)
class UniversalInternalLine:
    line_id: str
    particle: str
    momentum: str
    from_vertex: str
    to_vertex: str


@dataclass(frozen=True)
class UniversalVertex:
    vertex_id: str
    interaction: str
    theory: str
    particles: tuple[str, ...]
    connected_lines: tuple[str, ...]
    factor: str


@dataclass(frozen=True)
class UniversalFeynmanDiagram:
    diagram_id: str
    process: str
    topology: str
    channel: str
    theory: str
    internal_particle: Optional[str]
    external_legs: tuple[UniversalExternalLeg, ...]
    internal_lines: tuple[UniversalInternalLine, ...]
    vertices: tuple[UniversalVertex, ...]
    amplitude_structure: str
    status: str
    errors: tuple[str, ...] = ()


FERMIONS = {
    "electron", "positron",
    "muon", "antimuon",
    "tau", "antitau",
    "electron_neutrino", "electron_antineutrino",
    "muon_neutrino", "muon_antineutrino",
    "tau_neutrino", "tau_antineutrino",
}

CHARGED_FERMIONS = {
    "electron", "positron",
    "muon", "antimuon",
    "tau", "antitau",
    "up", "anti-up",
    "down", "anti-down",
    "strange", "anti-strange",
    "charm", "anti-charm",
    "bottom", "anti-bottom",
    "top", "anti-top",
}

QUARKS = {
    "up", "anti-up",
    "down", "anti-down",
    "strange", "anti-strange",
    "charm", "anti-charm",
    "bottom", "anti-bottom",
    "top", "anti-top",
}

NEUTRAL_BOSONS = {"photon", "Z", "gluon"}


FERMION_ANTIFERMION = {
    ("electron", "positron"),
    ("positron", "electron"),
    ("muon", "antimuon"),
    ("antimuon", "muon"),
    ("tau", "antitau"),
    ("antitau", "tau"),
    ("electron_neutrino", "electron_antineutrino"),
    ("electron_antineutrino", "electron_neutrino"),
    ("muon_neutrino", "muon_antineutrino"),
    ("muon_antineutrino", "muon_neutrino"),
    ("tau_neutrino", "tau_antineutrino"),
    ("tau_antineutrino", "tau_neutrino"),
    ("up", "anti-up"),
    ("anti-up", "up"),
    ("down", "anti-down"),
    ("anti-down", "down"),
    ("strange", "anti-strange"),
    ("anti-strange", "strange"),
    ("charm", "anti-charm"),
    ("anti-charm", "charm"),
    ("bottom", "anti-bottom"),
    ("anti-bottom", "bottom"),
    ("top", "anti-top"),
    ("anti-top", "top"),
}


def _normalise(value: str) -> str:
    return (
        value.strip()
        .lower()
        .replace("−", "-")
        .replace("–", "-")
    )


def _display(value: str) -> str:
    names = {
        "electron": "e⁻",
        "positron": "e⁺",
        "muon": "μ⁻",
        "antimuon": "μ⁺",
        "tau": "τ⁻",
        "antitau": "τ⁺",
        "electron_neutrino": "νe",
        "electron_antineutrino": "ν̄e",
        "muon_neutrino": "νμ",
        "muon_antineutrino": "ν̄μ",
        "tau_neutrino": "ντ",
        "tau_antineutrino": "ν̄τ",
        "up": "u",
        "anti-up": "ū",
        "down": "d",
        "anti-down": "d̄",
        "strange": "s",
        "anti-strange": "s̄",
        "charm": "c",
        "anti-charm": "c̄",
        "bottom": "b",
        "anti-bottom": "b̄",
        "top": "t",
        "anti-top": "t̄",
        "photon": "γ",
        "gluon": "g",
        "W+": "W⁺",
        "W-": "W⁻",
        "Z": "Z",
        "Higgs": "H",
    }
    return names.get(value, value)


def _is_pair(a: str, b: str) -> bool:
    return (a, b) in FERMION_ANTIFERMION


def _same_fermion_species(a: str, b: str) -> bool:
    return a == b and a in FERMIONS


def _qed_vertex(f1: str, f2: str, boson: str) -> bool:
    return (
        boson == "photon"
        and f1 in CHARGED_FERMIONS
        and f2 in CHARGED_FERMIONS
        and (_is_pair(f1, f2) or _same_fermion_species(f1, f2))
    )


def _qcd_quark_gluon_vertex(f1: str, f2: str, boson: str) -> bool:
    return (
        boson == "gluon"
        and f1 in QUARKS
        and f2 in QUARKS
        and (_is_pair(f1, f2) or _same_fermion_species(f1, f2))
    )


def _qcd_three_gluon_vertex(a: str, b: str, c: str) -> bool:
    return a == "gluon" and b == "gluon" and c == "gluon"


def _neutral_weak_vertex(f1: str, f2: str, boson: str) -> bool:
    return (
        boson == "Z"
        and f1 in FERMIONS
        and f2 in FERMIONS
        and (_is_pair(f1, f2) or _same_fermion_species(f1, f2))
    )


def _charged_weak_vertex(f1: str, f2: str, boson: str) -> bool:
    if boson not in {"W+", "W-"}:
        return False

    allowed = {
        ("electron", "electron_neutrino"),
        ("electron_neutrino", "electron"),
        ("positron", "electron_antineutrino"),
        ("electron_antineutrino", "positron"),
        ("muon", "muon_neutrino"),
        ("muon_neutrino", "muon"),
        ("antimuon", "muon_antineutrino"),
        ("muon_antineutrino", "antimuon"),
        ("tau", "tau_neutrino"),
        ("tau_neutrino", "tau"),
        ("antitau", "tau_antineutrino"),
        ("tau_antineutrino", "antitau"),
        ("up", "down"),
        ("down", "up"),
        ("up", "strange"),
        ("strange", "up"),
        ("up", "bottom"),
        ("bottom", "up"),
        ("charm", "down"),
        ("down", "charm"),
        ("charm", "strange"),
        ("strange", "charm"),
        ("charm", "bottom"),
        ("bottom", "charm"),
        ("top", "down"),
        ("down", "top"),
        ("top", "strange"),
        ("strange", "top"),
        ("top", "bottom"),
        ("bottom", "top"),
    }

    return (f1, f2) in allowed


def _find_fermion_boson_vertex(
    f1: str,
    f2: str,
    boson: str,
) -> Optional[dict]:

    if _qed_vertex(f1, f2, boson):
        return {
            "interaction": "qed_fermion_photon",
            "theory": "QED",
            "factor": "-ie gamma^mu",
        }

    if _qcd_quark_gluon_vertex(f1, f2, boson):
        return {
            "interaction": "qcd_quark_gluon",
            "theory": "QCD",
            "factor": "-ig_s gamma^mu T^a",
        }

    if _neutral_weak_vertex(f1, f2, boson):
        return {
            "interaction": "weak_neutral_fermion",
            "theory": "Electroweak",
            "factor": "-ig/cos(theta_W) gamma^mu(g_V-g_A gamma^5)",
        }

    if _charged_weak_vertex(f1, f2, boson):
        if f1 in QUARKS or f2 in QUARKS:
            return {
                "interaction": "weak_charged_quark",
                "theory": "Electroweak",
                "factor": "-ig/sqrt(2) gamma^mu P_L V_ij",
            }

        return {
            "interaction": "weak_charged_lepton",
            "theory": "Electroweak",
            "factor": "-ig/sqrt(2) gamma^mu P_L",
        }

    return None


def _s_channel(initial: tuple[str, str], final: tuple[str, str]):
    i1, i2 = initial
    f1, f2 = final

    if not _is_pair(i1, i2):
        return []

    if not _is_pair(f1, f2):
        return []

    result = []

    for boson in ("photon", "Z"):
        left = _find_fermion_boson_vertex(i1, i2, boson)
        right = _find_fermion_boson_vertex(f1, f2, boson)

        if left and right:
            result.append((boson, left, right))

    return result


def _t_channel(initial: tuple[str, str], final: tuple[str, str]):
    i1, i2 = initial
    f1, f2 = final

    result = []

    for boson in ("photon", "gluon", "Z", "W+", "W-"):
        left = _find_fermion_boson_vertex(i1, f1, boson)
        right = _find_fermion_boson_vertex(i2, f2, boson)

        if left and right:
            result.append((boson, left, right))

    return result


def _u_channel(initial: tuple[str, str], final: tuple[str, str]):
    i1, i2 = initial
    f1, f2 = final

    # Bhabha scattering is e- e+ -> e- e+.
    # Its tree-level QED topology is s + t, not u.
    if (
        i1 == "electron"
        and i2 == "positron"
        and f1 == "electron"
        and f2 == "positron"
    ):
        return []

    result = []

    for boson in ("photon", "gluon", "Z", "W+", "W-"):
        left = _find_fermion_boson_vertex(i1, f2, boson)
        right = _find_fermion_boson_vertex(i2, f1, boson)

        if left and right:
            result.append((boson, left, right))

    return result


def _qcd_qqbar_to_gg(
    initial: tuple[str, str],
    final: tuple[str, str],
):
    i1, i2 = initial
    f1, f2 = final

    if not _is_pair(i1, i2):
        return []

    if f1 != "gluon" or f2 != "gluon":
        return []

    if i1 not in QUARKS or i2 not in QUARKS:
        return []

    diagrams = []

    q_vertex = {
        "interaction": "qcd_quark_gluon",
        "theory": "QCD",
        "factor": "-ig_s gamma^mu T^a",
    }

    triple_gluon = {
        "interaction": "qcd_three_gluon",
        "theory": "QCD",
        "factor": "g_s Gamma^(mu nu rho)",
    }

    # s-channel gluon.
    diagrams.append(
        (
            "gluon",
            "s",
            triple_gluon,
            q_vertex,
        )
    )

    # t-channel quark.
    diagrams.append(
        (
            i1,
            "t",
            q_vertex,
            q_vertex,
        )
    )

    # u-channel quark.
    diagrams.append(
        (
            i1,
            "u",
            q_vertex,
            q_vertex,
        )
    )

    return diagrams


def _make_two_vertex_diagram(
    initial: tuple[str, str],
    final: tuple[str, str],
    channel: str,
    internal_particle: str,
    left_rule: dict,
    right_rule: dict,
    index: int,
) -> UniversalFeynmanDiagram:

    process = (
        f"{_display(initial[0])} + {_display(initial[1])} "
        f"→ {_display(final[0])} + {_display(final[1])}"
    )

    external = (
        UniversalExternalLeg("p1", initial[0], "incoming", "p1"),
        UniversalExternalLeg("p2", initial[1], "incoming", "p2"),
        UniversalExternalLeg("p3", final[0], "outgoing", "p3"),
        UniversalExternalLeg("p4", final[1], "outgoing", "p4"),
    )

    internal = UniversalInternalLine(
        line_id="k",
        particle=internal_particle,
        momentum="q",
        from_vertex="v1",
        to_vertex="v2",
    )

    v1 = UniversalVertex(
        vertex_id="v1",
        interaction=left_rule["interaction"],
        theory=left_rule["theory"],
        particles=(initial[0], initial[1], internal_particle),
        connected_lines=("p1", "p2", "k"),
        factor=left_rule["factor"],
    )

    v2 = UniversalVertex(
        vertex_id="v2",
        interaction=right_rule["interaction"],
        theory=right_rule["theory"],
        particles=(final[0], final[1], internal_particle),
        connected_lines=("p3", "p4", "k"),
        factor=right_rule["factor"],
    )

    theory = (
        left_rule["theory"]
        if left_rule["theory"] == right_rule["theory"]
        else "Mixed"
    )

    amplitude = (
        f"({left_rule['factor']}) · "
        f"Propagator[{internal_particle}] · "
        f"({right_rule['factor']})"
    )

    return UniversalFeynmanDiagram(
        diagram_id=f"{channel}_{internal_particle}_{index}",
        process=process,
        topology=f"{channel}-channel",
        channel=channel,
        theory=theory,
        internal_particle=internal_particle,
        external_legs=external,
        internal_lines=(internal,),
        vertices=(v1, v2),
        amplitude_structure=amplitude,
        status="candidate",
    )


def _make_qcd_s_diagram(
    initial: tuple[str, str],
    final: tuple[str, str],
    index: int,
) -> UniversalFeynmanDiagram:

    process = (
        f"{_display(initial[0])} + {_display(initial[1])} "
        f"→ g + g"
    )

    external = (
        UniversalExternalLeg("p1", initial[0], "incoming", "p1"),
        UniversalExternalLeg("p2", initial[1], "incoming", "p2"),
        UniversalExternalLeg("p3", "gluon", "outgoing", "k1"),
        UniversalExternalLeg("p4", "gluon", "outgoing", "k2"),
    )

    internal = UniversalInternalLine(
        line_id="k",
        particle="gluon",
        momentum="q",
        from_vertex="v1",
        to_vertex="v2",
    )

    v1 = UniversalVertex(
        vertex_id="v1",
        interaction="qcd_quark_gluon",
        theory="QCD",
        particles=(initial[0], initial[1], "gluon"),
        connected_lines=("p1", "p2", "k"),
        factor="-ig_s gamma^mu T^a",
    )

    v2 = UniversalVertex(
        vertex_id="v2",
        interaction="qcd_three_gluon",
        theory="QCD",
        particles=("gluon", "gluon", "gluon"),
        connected_lines=("k", "p3", "p4"),
        factor="g_s Gamma^(mu nu rho)",
    )

    return UniversalFeynmanDiagram(
        diagram_id=f"s-gluon_{index}",
        process=process,
        topology="s-channel",
        channel="s",
        theory="QCD",
        internal_particle="gluon",
        external_legs=external,
        internal_lines=(internal,),
        vertices=(v1, v2),
        amplitude_structure=(
            "(-ig_s gamma^mu T^a) · "
            "D_gluon(q) · "
            "(g_s Gamma^(mu nu rho))"
        ),
        status="candidate",
    )


def _make_qcd_exchange_diagram(
    initial: tuple[str, str],
    final: tuple[str, str],
    channel: str,
    index: int,
) -> UniversalFeynmanDiagram:

    process = (
        f"{_display(initial[0])} + {_display(initial[1])} "
        f"→ g + g"
    )

    external = (
        UniversalExternalLeg("p1", initial[0], "incoming", "p1"),
        UniversalExternalLeg("p2", initial[1], "incoming", "p2"),
        UniversalExternalLeg("p3", "gluon", "outgoing", "k1"),
        UniversalExternalLeg("p4", "gluon", "outgoing", "k2"),
    )

    exchanged_quark = initial[0]

    internal = UniversalInternalLine(
        line_id="k",
        particle=exchanged_quark,
        momentum="q",
        from_vertex="v1",
        to_vertex="v2",
    )

    v1 = UniversalVertex(
        vertex_id="v1",
        interaction="qcd_quark_gluon",
        theory="QCD",
        particles=(initial[0], "gluon", exchanged_quark),
        connected_lines=("p1", "p3", "k"),
        factor="-ig_s gamma^mu T^a",
    )

    v2 = UniversalVertex(
        vertex_id="v2",
        interaction="qcd_quark_gluon",
        theory="QCD",
        particles=(initial[1], "gluon", exchanged_quark),
        connected_lines=("p2", "p4", "k"),
        factor="-ig_s gamma^nu T^b",
    )

    return UniversalFeynmanDiagram(
        diagram_id=f"{channel}-{exchanged_quark}_{index}",
        process=process,
        topology=f"{channel}-channel",
        channel=channel,
        theory="QCD",
        internal_particle=exchanged_quark,
        external_legs=external,
        internal_lines=(internal,),
        vertices=(v1, v2),
        amplitude_structure=(
            "(-ig_s gamma^mu T^a) · "
            "S_quark(q) · "
            "(-ig_s gamma^nu T^b)"
        ),
        status="candidate",
    )


def generate_universal_2_to_2_diagrams(
    initial_particles: list[str] | tuple[str, ...],
    final_particles: list[str] | tuple[str, ...],
) -> dict:

    if len(initial_particles) != 2:
        return {
            "success": True,
            "status": "not_yet_supported",
            "reason": "Universal 2→2 generator requires exactly two initial particles.",
            "diagram_count": 0,
            "diagrams": [],
        }

    if len(final_particles) != 2:
        return {
            "success": True,
            "status": "not_yet_supported",
            "reason": "Universal 2→2 generator requires exactly two final particles.",
            "diagram_count": 0,
            "diagrams": [],
        }

    initial = tuple(_normalise(p) for p in initial_particles)
    final = tuple(_normalise(p) for p in final_particles)

    diagrams = []
    counter = 1

    # Special QCD process: q qbar -> g g.
    qcd = _qcd_qqbar_to_gg(initial, final)

    if qcd:
        for internal, channel, left, right in qcd:
            if channel == "s":
                diagrams.append(
                    _make_qcd_s_diagram(
                        initial,
                        final,
                        counter,
                    )
                )
            else:
                diagrams.append(
                    _make_qcd_exchange_diagram(
                        initial,
                        final,
                        channel,
                        counter,
                    )
                )
            counter += 1

    else:
        # Generic electroweak/QED/QCD 2→2 candidates.
        for channel, candidates in (
            ("s", _s_channel(initial, final)),
            ("t", _t_channel(initial, final)),
            ("u", _u_channel(initial, final)),
        ):
            for internal_particle, left_rule, right_rule in candidates:
                diagrams.append(
                    _make_two_vertex_diagram(
                        initial,
                        final,
                        channel,
                        internal_particle,
                        left_rule,
                        right_rule,
                        counter,
                    )
                )
                counter += 1

    if not diagrams:
        process = (
            f"{_display(initial[0])} + {_display(initial[1])} "
            f"→ {_display(final[0])} + {_display(final[1])}"
        )

        return {
            "success": True,
            "status": "not_yet_supported",
            "reason": (
                "No registered Standard Model tree-level topology "
                "was found for this process."
            ),
            "process": process,
            "diagram_count": 0,
            "diagrams": [],
        }

    return {
        "success": True,
        "status": "candidate_diagrams",
        "process": diagrams[0].process,
        "diagram_count": len(diagrams),
        "diagrams": [_diagram_to_dict(d) for d in diagrams],
    }


def _diagram_to_dict(diagram: UniversalFeynmanDiagram) -> dict:
    return {
        "diagram_id": diagram.diagram_id,
        "process": diagram.process,
        "topology": diagram.topology,
        "channel": diagram.channel,
        "theory": diagram.theory,
        "internal_particle": diagram.internal_particle,
        "external_legs": [
            {
                "leg_id": x.leg_id,
                "particle": x.particle,
                "role": x.role,
                "momentum": x.momentum,
            }
            for x in diagram.external_legs
        ],
        "internal_lines": [
            {
                "line_id": x.line_id,
                "particle": x.particle,
                "momentum": x.momentum,
                "from_vertex": x.from_vertex,
                "to_vertex": x.to_vertex,
            }
            for x in diagram.internal_lines
        ],
        "vertices": [
            {
                "vertex_id": x.vertex_id,
                "interaction": x.interaction,
                "theory": x.theory,
                "particles": list(x.particles),
                "connected_lines": list(x.connected_lines),
                "factor": x.factor,
            }
            for x in diagram.vertices
        ],
        "amplitude_structure": diagram.amplitude_structure,
        "status": diagram.status,
        "errors": list(diagram.errors),
    }


def universal_diagram_summary(
    initial_particles: list[str] | tuple[str, ...],
    final_particles: list[str] | tuple[str, ...],
) -> dict:

    result = generate_universal_2_to_2_diagrams(
        initial_particles,
        final_particles,
    )

    return {
        "success": result["success"],
        "status": result["status"],
        "process": result.get("process"),
        "diagram_count": result["diagram_count"],
        "channels": [
            diagram["channel"]
            for diagram in result["diagrams"]
        ],
        "theories": sorted(
            {
                diagram["theory"]
                for diagram in result["diagrams"]
            }
        ),
        "scientific_scope": (
            "Candidate tree-level 2→2 diagrams constructed from "
            "explicitly registered Standard Model interactions. "
            "Physical validation, momentum conservation, gauge "
            "invariance and complete matrix-element evaluation "
            "remain separate calculation layers."
        ),
    }
