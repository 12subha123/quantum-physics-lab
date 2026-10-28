from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class FeynmanRuleVertex:
    vertex_id: str
    interaction: str
    theory: str
    factor: str
    particles: tuple[str, ...]


@dataclass(frozen=True)
class FeynmanRulePropagator:
    line_id: str
    particle: str
    momentum: str
    factor: str


@dataclass(frozen=True)
class DiagramRuleAssignment:
    diagram_id: str
    process: str
    topology: str
    theory: str
    vertices: tuple[FeynmanRuleVertex, ...]
    propagators: tuple[FeynmanRulePropagator, ...]
    amplitude_expression: str
    valid: bool
    errors: tuple[str, ...]


def _get(obj, name, default=None):
    return getattr(obj, name, default)


def _normalise(value: str) -> str:
    return (
        str(value)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


# ------------------------------------------------------------------
# Universal Standard Model vertex rules
# ------------------------------------------------------------------

VERTEX_RULES = {
    "qed_fermion_photon": {
        "theory": "QED",
        "factor": "-ie gamma^mu",
    },
    "qcd_quark_gluon": {
        "theory": "QCD",
        "factor": "-ig_s gamma^mu T^a",
    },
    "qcd_three_gluon": {
        "theory": "QCD",
        "factor": "g_s Gamma^(mu nu rho)",
    },
    "qcd_four_gluon": {
        "theory": "QCD",
        "factor": "g_s^2 Gamma^(mu nu rho sigma)",
    },
    "weak_charged_lepton": {
        "theory": "Electroweak",
        "factor": "-ig/sqrt(2) gamma^mu P_L",
    },
    "weak_charged_quark": {
        "theory": "Electroweak",
        "factor": "-ig/sqrt(2) gamma^mu P_L V_ij",
    },
    "weak_neutral_fermion": {
        "theory": "Electroweak",
        "factor": "-ig/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
    },
    "higgs_fermion_yukawa": {
        "theory": "Electroweak",
        "factor": "-iy_f",
    },
    "higgs_vector_w": {
        "theory": "Electroweak",
        "factor": "ig m_W/cos? ",
    },
    "higgs_vector_z": {
        "theory": "Electroweak",
        "factor": "ig m_Z/cos? ",
    },
    "higgs_three": {
        "theory": "Electroweak",
        "factor": "-i lambda_3",
    },
    "higgs_four": {
        "theory": "Electroweak",
        "factor": "-i lambda_4",
    },
    "phi4_scalar": {
        "theory": "Scalar phi4",
        "factor": "-i lambda",
    },
}


# Propagator rules are represented symbolically.
# Exact gauge choices and tensor structures will be expanded later.
PROPAGATOR_RULES = {
    "photon": "(-i g_mu_nu)/(q^2+i epsilon)",
    "gluon": "(-i g_mu_nu delta_ab)/(q^2+i epsilon)",
    "electron": "i( slash(q)+m_f )/(q^2-m_f^2+i epsilon)",
    "positron": "i( slash(q)+m_f )/(q^2-m_f^2+i epsilon)",
    "muon": "i( slash(q)+m_f )/(q^2-m_f^2+i epsilon)",
    "antimuon": "i( slash(q)+m_f )/(q^2-m_f^2+i epsilon)",
    "tau": "i( slash(q)+m_f )/(q^2-m_f^2+i epsilon)",
    "antitau": "i( slash(q)+m_f )/(q^2-m_f^2+i epsilon)",
    "up": "i( slash(q)+m_q )/(q^2-m_q^2+i epsilon)",
    "anti_up": "i( slash(q)+m_q )/(q^2-m_q^2+i epsilon)",
    "down": "i( slash(q)+m_q )/(q^2-m_q^2+i epsilon)",
    "anti_down": "i( slash(q)+m_q )/(q^2-m_q^2+i epsilon)",
    "strange": "i( slash(q)+m_q )/(q^2-m_q^2+i epsilon)",
    "anti_strange": "i( slash(q)+m_q )/(q^2-m_q^2+i epsilon)",
    "gluon_internal": "(-i g_mu_nu delta_ab)/(q^2+i epsilon)",
    "w+": "(-i g_mu_nu)/(q^2-m_W^2+i epsilon)",
    "w-": "(-i g_mu_nu)/(q^2-m_W^2+i epsilon)",
    "z": "(-i g_mu_nu)/(q^2-m_Z^2+i epsilon)",
    "higgs": "i/(q^2-m_H^2+i epsilon)",
    "scalar": "i/(q^2-m^2+i epsilon)",
}


def _vertex_rule(interaction: str) -> tuple[str, str]:
    key = _normalise(interaction)

    rule = VERTEX_RULES.get(key)

    if rule is None:
        return "", ""

    return rule["theory"], rule["factor"]


def _propagator_rule(particle: str) -> str:
    key = _normalise(particle)

    if key in PROPAGATOR_RULES:
        return PROPAGATOR_RULES[key]

    # Generic particle categories.
    if "photon" in key:
        return PROPAGATOR_RULES["photon"]

    if "gluon" in key:
        return PROPAGATOR_RULES["gluon_internal"]

    if "higgs" in key:
        return PROPAGATOR_RULES["higgs"]

    if key in {"w", "w_plus", "w_minus"}:
        return PROPAGATOR_RULES["w+"]

    if key == "z":
        return PROPAGATOR_RULES["z"]

    return ""


def _extract_diagrams(diagrams) -> list:
    if diagrams is None:
        return []

    if hasattr(diagrams, "diagrams"):
        return list(diagrams.diagrams)

    return list(diagrams)


def assign_feynman_rules(diagram) -> DiagramRuleAssignment:
    diagram_id = str(_get(diagram, "diagram_id", "unknown"))
    process = str(_get(diagram, "process", ""))
    topology = str(_get(diagram, "topology", ""))
    theory = str(_get(diagram, "theory", ""))

    errors: list[str] = []
    assigned_vertices: list[FeynmanRuleVertex] = []
    assigned_propagators: list[FeynmanRulePropagator] = []

    # --------------------------------------------------------------
    # Vertices
    # --------------------------------------------------------------

    for vertex in _get(diagram, "vertices", ()) or ():
        vertex_id = str(_get(vertex, "vertex_id", ""))
        interaction = str(_get(vertex, "interaction", ""))
        vertex_theory = str(_get(vertex, "theory", ""))

        rule_theory, factor = _vertex_rule(interaction)

        if not factor:
            errors.append(
                f"{vertex_id}: no Feynman rule registered "
                f"for interaction '{interaction}'."
            )
            continue

        if vertex_theory and rule_theory:
            if _normalise(vertex_theory) != _normalise(rule_theory):
                errors.append(
                    f"{vertex_id}: theory mismatch. "
                    f"Diagram says '{vertex_theory}', "
                    f"rule belongs to '{rule_theory}'."
                )

        external_legs = tuple(
            _get(vertex, "external_legs", ()) or ()
        )

        internal_lines = tuple(
            _get(vertex, "internal_lines", ()) or ()
        )

        particles = tuple(
            list(external_legs) + list(internal_lines)
        )

        assigned_vertices.append(
            FeynmanRuleVertex(
                vertex_id=vertex_id,
                interaction=interaction,
                theory=vertex_theory or rule_theory,
                factor=factor,
                particles=particles,
            )
        )

    # --------------------------------------------------------------
    # Internal propagators
    # --------------------------------------------------------------

    for line in _get(diagram, "internal_lines", ()) or ():
        line_id = str(_get(line, "line_id", ""))
        particle = str(_get(line, "particle", ""))
        momentum = str(_get(line, "momentum", "")).strip()

        factor = _propagator_rule(particle)

        if not factor:
            errors.append(
                f"{line_id}: no propagator rule registered "
                f"for internal particle '{particle}'."
            )
            continue

        if not momentum:
            errors.append(
                f"{line_id}: missing internal momentum."
            )

        assigned_propagators.append(
            FeynmanRulePropagator(
                line_id=line_id,
                particle=particle,
                momentum=momentum,
                factor=factor,
            )
        )

    # --------------------------------------------------------------
    # Symbolic amplitude
    # --------------------------------------------------------------

    factors: list[str] = []

    for vertex in assigned_vertices:
        factors.append(
            f"[V:{vertex.vertex_id}={vertex.factor}]"
        )

    for propagator in assigned_propagators:
        factors.append(
            f"[P:{propagator.line_id}({propagator.momentum})="
            f"{propagator.factor}]"
        )

    if factors:
        amplitude_expression = " ".join(factors)
    else:
        amplitude_expression = "UNASSIGNED"

    valid = not errors

    return DiagramRuleAssignment(
        diagram_id=diagram_id,
        process=process,
        topology=topology,
        theory=theory,
        vertices=tuple(assigned_vertices),
        propagators=tuple(assigned_propagators),
        amplitude_expression=amplitude_expression,
        valid=valid,
        errors=tuple(errors),
    )


def assign_feynman_rules_to_diagrams(
    diagrams: Iterable,
) -> list[DiagramRuleAssignment]:
    return [
        assign_feynman_rules(diagram)
        for diagram in _extract_diagrams(diagrams)
    ]


def feynman_rule_assignment_summary(diagrams) -> dict:
    assignments = assign_feynman_rules_to_diagrams(diagrams)

    valid_count = sum(
        1 for assignment in assignments
        if assignment.valid
    )

    invalid_count = len(assignments) - valid_count

    return {
        "success": True,
        "valid": all(
            assignment.valid
            for assignment in assignments
        ),
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "total_count": len(assignments),
        "assignments": [
            {
                "diagram_id": assignment.diagram_id,
                "process": assignment.process,
                "topology": assignment.topology,
                "theory": assignment.theory,
                "valid": assignment.valid,
                "vertices": [
                    {
                        "vertex_id": vertex.vertex_id,
                        "interaction": vertex.interaction,
                        "theory": vertex.theory,
                        "factor": vertex.factor,
                        "particles": list(vertex.particles),
                    }
                    for vertex in assignment.vertices
                ],
                "propagators": [
                    {
                        "line_id": propagator.line_id,
                        "particle": propagator.particle,
                        "momentum": propagator.momentum,
                        "factor": propagator.factor,
                    }
                    for propagator in assignment.propagators
                ],
                "amplitude_expression": assignment.amplitude_expression,
                "errors": list(assignment.errors),
            }
            for assignment in assignments
        ],
        "supported_theories": [
            "QED",
            "QCD",
            "Electroweak",
            "Scalar phi4",
        ],
        "scientific_scope": (
            "Universal tree-level symbolic Feynman-rule assignment "
            "layer. It maps validated interaction vertices and "
            "internal particles to registered vertex and propagator "
            "factors. The amplitude is currently a symbolic factor "
            "structure; spinor contractions, polarization sums, "
            "color algebra, gauge fixing, loop corrections, "
            "renormalization, and numerical amplitude evaluation "
            "are separate later layers."
        ),
    }
