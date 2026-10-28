from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class InteractionVertex:
    vertex_id: str
    theory: str
    particles: tuple[str, ...]
    order: int
    factor: str
    description: str
    physical: bool = True


# ---------------------------------------------------------------------
# Standard Model physical tree-level interaction vertices.
#
# Scope:
#   - physical particles
#   - renormalizable SM interactions
#   - broken-phase representation
#   - tree-level diagram construction
#
# Ghost and gauge-fixing vertices are intentionally excluded from the
# physical-particle tree-level catalog. They become necessary for
# gauge-fixed loop calculations.
# ---------------------------------------------------------------------

STANDARD_MODEL_VERTICES: tuple[InteractionVertex, ...] = (

    # ================================================================
    # QED
    # ================================================================

    InteractionVertex(
        "qed_electron_photon",
        "QED",
        ("electron", "positron", "photon"),
        3,
        "-i e gamma^mu",
        "Electron-photon interaction.",
    ),
    InteractionVertex(
        "qed_muon_photon",
        "QED",
        ("muon", "antimuon", "photon"),
        3,
        "-i e gamma^mu",
        "Muon-photon interaction.",
    ),
    InteractionVertex(
        "qed_tau_photon",
        "QED",
        ("tau", "antitau", "photon"),
        3,
        "-i e gamma^mu",
        "Tau-photon interaction.",
    ),

    InteractionVertex(
        "qed_up_photon",
        "QED",
        ("up", "anti-up", "photon"),
        3,
        "-i e Q_u gamma^mu",
        "Up-quark photon interaction.",
    ),
    InteractionVertex(
        "qed_down_photon",
        "QED",
        ("down", "anti-down", "photon"),
        3,
        "-i e Q_d gamma^mu",
        "Down-quark photon interaction.",
    ),
    InteractionVertex(
        "qed_strange_photon",
        "QED",
        ("strange", "anti-strange", "photon"),
        3,
        "-i e Q_d gamma^mu",
        "Strange-quark photon interaction.",
    ),
    InteractionVertex(
        "qed_charm_photon",
        "QED",
        ("charm", "anti-charm", "photon"),
        3,
        "-i e Q_u gamma^mu",
        "Charm-quark photon interaction.",
    ),
    InteractionVertex(
        "qed_bottom_photon",
        "QED",
        ("bottom", "anti-bottom", "photon"),
        3,
        "-i e Q_d gamma^mu",
        "Bottom-quark photon interaction.",
    ),
    InteractionVertex(
        "qed_top_photon",
        "QED",
        ("top", "anti-top", "photon"),
        3,
        "-i e Q_u gamma^mu",
        "Top-quark photon interaction.",
    ),

    # ================================================================
    # QCD: quark-gluon
    # ================================================================

    InteractionVertex(
        "qcd_up_gluon",
        "QCD",
        ("up", "anti-up", "gluon"),
        3,
        "-i g_s gamma^mu T^a",
        "Up-quark gluon interaction.",
    ),
    InteractionVertex(
        "qcd_down_gluon",
        "QCD",
        ("down", "anti-down", "gluon"),
        3,
        "-i g_s gamma^mu T^a",
        "Down-quark gluon interaction.",
    ),
    InteractionVertex(
        "qcd_strange_gluon",
        "QCD",
        ("strange", "anti-strange", "gluon"),
        3,
        "-i g_s gamma^mu T^a",
        "Strange-quark gluon interaction.",
    ),
    InteractionVertex(
        "qcd_charm_gluon",
        "QCD",
        ("charm", "anti-charm", "gluon"),
        3,
        "-i g_s gamma^mu T^a",
        "Charm-quark gluon interaction.",
    ),
    InteractionVertex(
        "qcd_bottom_gluon",
        "QCD",
        ("bottom", "anti-bottom", "gluon"),
        3,
        "-i g_s gamma^mu T^a",
        "Bottom-quark gluon interaction.",
    ),
    InteractionVertex(
        "qcd_top_gluon",
        "QCD",
        ("top", "anti-top", "gluon"),
        3,
        "-i g_s gamma^mu T^a",
        "Top-quark gluon interaction.",
    ),

    # QCD gauge self interactions
    InteractionVertex(
        "qcd_three_gluon",
        "QCD",
        ("gluon", "gluon", "gluon"),
        3,
        "g_s f^{abc} Gamma^{mu nu rho}",
        "Three-gluon gauge interaction.",
    ),
    InteractionVertex(
        "qcd_four_gluon",
        "QCD",
        ("gluon", "gluon", "gluon", "gluon"),
        4,
        "g_s^2 f^{abe}f^{cde} tensor structure",
        "Four-gluon gauge interaction.",
    ),

    # ================================================================
    # Charged-current weak interactions
    # ================================================================

    InteractionVertex(
        "cc_electron_neutrino_w",
        "Electroweak",
        ("electron", "electron_neutrino", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L",
        "Charged-current electron-neutrino interaction.",
    ),
    InteractionVertex(
        "cc_muon_neutrino_w",
        "Electroweak",
        ("muon", "muon_neutrino", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L",
        "Charged-current muon-neutrino interaction.",
    ),
    InteractionVertex(
        "cc_tau_neutrino_w",
        "Electroweak",
        ("tau", "tau_neutrino", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L",
        "Charged-current tau-neutrino interaction.",
    ),

    # Quark charged-current vertices.
    # CKM matrix elements are retained symbolically.
    InteractionVertex(
        "cc_up_down_w",
        "Electroweak",
        ("up", "down", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L V_ud",
        "Up/down charged-current interaction.",
    ),
    InteractionVertex(
        "cc_up_strange_w",
        "Electroweak",
        ("up", "strange", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L V_us",
        "Up/strange charged-current interaction.",
    ),
    InteractionVertex(
        "cc_up_bottom_w",
        "Electroweak",
        ("up", "bottom", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L V_ub",
        "Up/bottom charged-current interaction.",
    ),
    InteractionVertex(
        "cc_charm_down_w",
        "Electroweak",
        ("charm", "down", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L V_cd",
        "Charm/down charged-current interaction.",
    ),
    InteractionVertex(
        "cc_charm_strange_w",
        "Electroweak",
        ("charm", "strange", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L V_cs",
        "Charm/strange charged-current interaction.",
    ),
    InteractionVertex(
        "cc_charm_bottom_w",
        "Electroweak",
        ("charm", "bottom", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L V_cb",
        "Charm/bottom charged-current interaction.",
    ),
    InteractionVertex(
        "cc_top_down_w",
        "Electroweak",
        ("top", "down", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L V_td",
        "Top/down charged-current interaction.",
    ),
    InteractionVertex(
        "cc_top_strange_w",
        "Electroweak",
        ("top", "strange", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L V_ts",
        "Top/strange charged-current interaction.",
    ),
    InteractionVertex(
        "cc_top_bottom_w",
        "Electroweak",
        ("top", "bottom", "W+"),
        3,
        "-i g/sqrt(2) gamma^mu P_L V_tb",
        "Top/bottom charged-current interaction.",
    ),

    # ================================================================
    # Neutral-current Z interactions
    # ================================================================

    InteractionVertex(
        "nc_neutrino_z",
        "Electroweak",
        ("electron_neutrino", "electron_antineutrino", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Electron-neutrino neutral-current interaction.",
    ),
    InteractionVertex(
        "nc_muon_neutrino_z",
        "Electroweak",
        ("muon_neutrino", "muon_antineutrino", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Muon-neutrino neutral-current interaction.",
    ),
    InteractionVertex(
        "nc_tau_neutrino_z",
        "Electroweak",
        ("tau_neutrino", "tau_antineutrino", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Tau-neutrino neutral-current interaction.",
    ),

    InteractionVertex(
        "nc_electron_z",
        "Electroweak",
        ("electron", "positron", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Electron-Z interaction.",
    ),
    InteractionVertex(
        "nc_muon_z",
        "Electroweak",
        ("muon", "antimuon", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Muon-Z interaction.",
    ),
    InteractionVertex(
        "nc_tau_z",
        "Electroweak",
        ("tau", "antitau", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Tau-Z interaction.",
    ),

    InteractionVertex(
        "nc_up_z",
        "Electroweak",
        ("up", "anti-up", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Up-quark Z interaction.",
    ),
    InteractionVertex(
        "nc_down_z",
        "Electroweak",
        ("down", "anti-down", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Down-quark Z interaction.",
    ),
    InteractionVertex(
        "nc_strange_z",
        "Electroweak",
        ("strange", "anti-strange", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Strange-quark Z interaction.",
    ),
    InteractionVertex(
        "nc_charm_z",
        "Electroweak",
        ("charm", "anti-charm", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Charm-quark Z interaction.",
    ),
    InteractionVertex(
        "nc_bottom_z",
        "Electroweak",
        ("bottom", "anti-bottom", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Bottom-quark Z interaction.",
    ),
    InteractionVertex(
        "nc_top_z",
        "Electroweak",
        ("top", "anti-top", "Z"),
        3,
        "-i g/cos(theta_W) gamma^mu (g_V-g_A gamma^5)",
        "Top-quark Z interaction.",
    ),

    # ================================================================
    # Triple gauge vertices
    # ================================================================

    InteractionVertex(
        "triple_w_w_photon",
        "Electroweak",
        ("W+", "W-", "photon"),
        3,
        "i e Gamma^{mu nu rho}",
        "W+ W- photon triple-gauge interaction.",
    ),
    InteractionVertex(
        "triple_w_w_z",
        "Electroweak",
        ("W+", "W-", "Z"),
        3,
        "i g cos(theta_W) Gamma^{mu nu rho}",
        "W+ W- Z triple-gauge interaction.",
    ),

    # ================================================================
    # Quartic gauge vertices
    # ================================================================

    InteractionVertex(
        "quartic_w_w_photon_photon",
        "Electroweak",
        ("W+", "W-", "photon", "photon"),
        4,
        "i e^2 Gamma^{mu nu rho sigma}",
        "W+ W- photon photon quartic interaction.",
    ),
    InteractionVertex(
        "quartic_w_w_photon_z",
        "Electroweak",
        ("W+", "W-", "photon", "Z"),
        4,
        "i e g cos(theta_W) Gamma^{mu nu rho sigma}",
        "W+ W- photon Z quartic interaction.",
    ),
    InteractionVertex(
        "quartic_w_w_z_z",
        "Electroweak",
        ("W+", "W-", "Z", "Z"),
        4,
        "i g^2 cos(theta_W)^2 Gamma^{mu nu rho sigma}",
        "W+ W- Z Z quartic interaction.",
    ),

    # ================================================================
    # Higgs-fermion Yukawa interactions
    # ================================================================

    InteractionVertex(
        "yukawa_electron_higgs",
        "Higgs",
        ("electron", "positron", "Higgs"),
        3,
        "-i y_e",
        "Electron Yukawa interaction.",
    ),
    InteractionVertex(
        "yukawa_muon_higgs",
        "Higgs",
        ("muon", "antimuon", "Higgs"),
        3,
        "-i y_mu",
        "Muon Yukawa interaction.",
    ),
    InteractionVertex(
        "yukawa_tau_higgs",
        "Higgs",
        ("tau", "antitau", "Higgs"),
        3,
        "-i y_tau",
        "Tau Yukawa interaction.",
    ),
    InteractionVertex(
        "yukawa_up_higgs",
        "Higgs",
        ("up", "anti-up", "Higgs"),
        3,
        "-i y_u",
        "Up-quark Yukawa interaction.",
    ),
    InteractionVertex(
        "yukawa_down_higgs",
        "Higgs",
        ("down", "anti-down", "Higgs"),
        3,
        "-i y_d",
        "Down-quark Yukawa interaction.",
    ),
    InteractionVertex(
        "yukawa_strange_higgs",
        "Higgs",
        ("strange", "anti-strange", "Higgs"),
        3,
        "-i y_s",
        "Strange-quark Yukawa interaction.",
    ),
    InteractionVertex(
        "yukawa_charm_higgs",
        "Higgs",
        ("charm", "anti-charm", "Higgs"),
        3,
        "-i y_c",
        "Charm-quark Yukawa interaction.",
    ),
    InteractionVertex(
        "yukawa_bottom_higgs",
        "Higgs",
        ("bottom", "anti-bottom", "Higgs"),
        3,
        "-i y_b",
        "Bottom-quark Yukawa interaction.",
    ),
    InteractionVertex(
        "yukawa_top_higgs",
        "Higgs",
        ("top", "anti-top", "Higgs"),
        3,
        "-i y_t",
        "Top-quark Yukawa interaction.",
    ),

    # ================================================================
    # Higgs-gauge interactions
    # ================================================================

    InteractionVertex(
        "higgs_w_w",
        "Higgs",
        ("Higgs", "W+", "W-"),
        3,
        "i g m_W g^{mu nu}",
        "Higgs-W-W interaction.",
    ),
    InteractionVertex(
        "higgs_z_z",
        "Higgs",
        ("Higgs", "Z", "Z"),
        3,
        "i g m_Z/cos(theta_W) g^{mu nu}",
        "Higgs-Z-Z interaction.",
    ),
    InteractionVertex(
        "higgs_higgs_w_w",
        "Higgs",
        ("Higgs", "Higgs", "W+", "W-"),
        4,
        "i g^2/2 g^{mu nu}",
        "Higgs-Higgs-W-W interaction.",
    ),
    InteractionVertex(
        "higgs_higgs_z_z",
        "Higgs",
        ("Higgs", "Higgs", "Z", "Z"),
        4,
        "i g^2/(2 cos(theta_W)^2) g^{mu nu}",
        "Higgs-Higgs-Z-Z interaction.",
    ),

    # ================================================================
    # Higgs self interactions
    # ================================================================

    InteractionVertex(
        "higgs_three",
        "Higgs",
        ("Higgs", "Higgs", "Higgs"),
        3,
        "-i lambda_3",
        "Triple-Higgs self interaction.",
    ),
    InteractionVertex(
        "higgs_four",
        "Higgs",
        ("Higgs", "Higgs", "Higgs", "Higgs"),
        4,
        "-i lambda_4",
        "Quartic-Higgs self interaction.",
    ),
)


def list_standard_model_vertices() -> list[dict]:
    return [asdict(vertex) for vertex in STANDARD_MODEL_VERTICES]


def get_vertex(vertex_id: str) -> dict:
    for vertex in STANDARD_MODEL_VERTICES:
        if vertex.vertex_id == vertex_id:
            return asdict(vertex)

    raise ValueError(
        f"Unknown Standard Model vertex: {vertex_id}"
    )


def list_vertices_by_theory(theory: str) -> list[dict]:
    target = theory.strip().lower()

    return [
        asdict(vertex)
        for vertex in STANDARD_MODEL_VERTICES
        if vertex.theory.lower() == target
    ]


def find_vertices_containing(
    particle_type: str,
) -> list[dict]:
    target = particle_type.strip().lower()

    return [
        asdict(vertex)
        for vertex in STANDARD_MODEL_VERTICES
        if any(
            particle.lower() == target
            for particle in vertex.particles
        )
    ]


def standard_model_vertex_summary() -> dict:
    by_theory: dict[str, int] = {}

    for vertex in STANDARD_MODEL_VERTICES:
        by_theory[vertex.theory] = (
            by_theory.get(vertex.theory, 0) + 1
        )

    return {
        "success": True,
        "vertex_count": len(STANDARD_MODEL_VERTICES),
        "by_theory": by_theory,
        "three_point_vertices": sum(
            vertex.order == 3
            for vertex in STANDARD_MODEL_VERTICES
        ),
        "four_point_vertices": sum(
            vertex.order == 4
            for vertex in STANDARD_MODEL_VERTICES
        ),
        "physical_vertices": sum(
            vertex.physical
            for vertex in STANDARD_MODEL_VERTICES
        ),
        "scientific_scope": (
            "Physical broken-phase Standard Model tree-level "
            "interaction vertices. Ghost and gauge-fixing "
            "vertices are excluded from this physical catalog."
        ),
    }
