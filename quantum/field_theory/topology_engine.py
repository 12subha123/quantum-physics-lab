from dataclasses import asdict, dataclass

from quantum.field_theory.particle_process import (
    ParticleProcess,
    create_process,
)
from quantum.field_theory.vertex_matching import _particle_category


@dataclass(frozen=True)
class TopologyCandidate:
    topology_id: str
    theory: str
    channel: str
    internal_particle: str
    initial_vertex: str
    final_vertex: str
    process: str
    description: str
    status: str = "candidate"


def _normalize(name: str) -> str:
    return name.strip().lower()


def _is_antiparticle_pair(a: str, b: str) -> bool:
    pairs = {
        ("electron", "positron"),
        ("muon", "antimuon"),
        ("tau", "antitau"),
        ("up", "anti-up"),
        ("down", "anti-down"),
        ("strange", "anti-strange"),
        ("charm", "anti-charm"),
        ("top", "anti-top"),
        ("bottom", "anti-bottom"),
    }

    return (
        (_normalize(a), _normalize(b)) in pairs
        or (_normalize(b), _normalize(a)) in pairs
    )


def _is_charged_lepton(name: str) -> bool:
    return _normalize(name) in {
        "electron",
        "positron",
        "muon",
        "antimuon",
        "tau",
        "antitau",
    }


def _is_quark(name: str) -> bool:
    return _normalize(name) in {
        "up",
        "down",
        "strange",
        "charm",
        "top",
        "bottom",
    }


def _is_antiquark(name: str) -> bool:
    return _normalize(name) in {
        "anti-up",
        "anti-down",
        "anti-strange",
        "anti-charm",
        "anti-top",
        "anti-bottom",
    }


def _is_gluon(name: str) -> bool:
    return _normalize(name) == "gluon"


def _same_flavor(a: str, b: str) -> bool:
    return _normalize(a) == _normalize(b)


def _qed_s_channel(process: ParticleProcess):
    if (
        process.initial_count != 2
        or process.final_count != 2
    ):
        return None

    i1, i2 = process.initial_particles
    f1, f2 = process.final_particles

    if not _is_antiparticle_pair(i1, i2):
        return None

    if not _is_antiparticle_pair(f1, f2):
        return None

    if not all(
        _is_charged_lepton(p)
        for p in (
            i1,
            i2,
            f1,
            f2,
        )
    ):
        return None

    return TopologyCandidate(
        topology_id="qed_s_channel",
        theory="QED",
        channel="s",
        internal_particle="photon",
        initial_vertex="qed_fermion_photon",
        final_vertex="qed_fermion_photon",
        process=process.notation,
        description=(
            "Tree-level s-channel annihilation "
            "through an internal photon."
        ),
    )


def _qed_t_channel(process: ParticleProcess):
    if (
        process.initial_count != 2
        or process.final_count != 2
    ):
        return None

    i1, i2 = process.initial_particles
    f1, f2 = process.final_particles

    if not all(
        _is_charged_lepton(p)
        for p in (
            i1,
            i2,
            f1,
            f2,
        )
    ):
        return None

    if not _same_flavor(i1, f1):
        return None

    if not _same_flavor(i2, f2):
        return None

    return TopologyCandidate(
        topology_id="qed_t_channel",
        theory="QED",
        channel="t",
        internal_particle="photon",
        initial_vertex="qed_fermion_photon",
        final_vertex="qed_fermion_photon",
        process=process.notation,
        description=(
            "Tree-level t-channel scattering "
            "through an internal photon."
        ),
    )


def _qed_u_channel(process: ParticleProcess):
    if (
        process.initial_count != 2
        or process.final_count != 2
    ):
        return None

    i1, i2 = process.initial_particles
    f1, f2 = process.final_particles

    if not all(
        _is_charged_lepton(p)
        for p in (
            i1,
            i2,
            f1,
            f2,
        )
    ):
        return None

    if not _same_flavor(i1, f2):
        return None

    if not _same_flavor(i2, f1):
        return None

    return TopologyCandidate(
        topology_id="qed_u_channel",
        theory="QED",
        channel="u",
        internal_particle="photon",
        initial_vertex="qed_fermion_photon",
        final_vertex="qed_fermion_photon",
        process=process.notation,
        description=(
            "Tree-level u-channel exchange "
            "through an internal photon."
        ),
    )


def _qcd_quark_antiquark_to_gluon_pair(process: ParticleProcess):
    if (
        process.initial_count != 2
        or process.final_count != 2
    ):
        return None

    i1, i2 = process.initial_particles
    f1, f2 = process.final_particles

    if not _is_quark(i1) or not _is_antiquark(i2):
        return None

    if not (
        _is_gluon(f1)
        and _is_gluon(f2)
    ):
        return None

    return TopologyCandidate(
        topology_id="qcd_quark_antiquark_s_channel",
        theory="QCD",
        channel="s",
        internal_particle="gluon",
        initial_vertex="qcd_quark_gluon",
        final_vertex="qcd_three_gluon",
        process=process.notation,
        description=(
            "Tree-level quark-antiquark annihilation "
            "through an internal gluon."
        ),
    )


def _qcd_gluon_to_quark_pair(process: ParticleProcess):
    if (
        process.initial_count != 2
        or process.final_count != 2
    ):
        return None

    i1, i2 = process.initial_particles
    f1, f2 = process.final_particles

    if not (
        _is_gluon(i1)
        and _is_gluon(i2)
    ):
        return None

    if not _is_quark(f1) or not _is_antiquark(f2):
        return None

    return TopologyCandidate(
        topology_id="qcd_gluon_fusion_quark_pair",
        theory="QCD",
        channel="s",
        internal_particle="gluon",
        initial_vertex="qcd_three_gluon",
        final_vertex="qcd_quark_gluon",
        process=process.notation,
        description=(
            "Tree-level gluon-fusion candidate "
            "producing a quark-antiquark pair."
        ),
    )


def _qcd_three_gluon_channel(process: ParticleProcess):
    if (
        process.initial_count != 2
        or process.final_count != 2
    ):
        return None

    if not all(
        _is_gluon(particle)
        for particle in (
            *process.initial_particles,
            *process.final_particles,
        )
    ):
        return None

    return TopologyCandidate(
        topology_id="qcd_three_gluon_exchange",
        theory="QCD",
        channel="t/u",
        internal_particle="gluon",
        initial_vertex="qcd_three_gluon",
        final_vertex="qcd_three_gluon",
        process=process.notation,
        description=(
            "Tree-level four-gluon scattering candidate "
            "involving three-gluon vertices."
        ),
    )


def generate_tree_level_topologies(
    initial_particles,
    final_particles,
):
    process = create_process(
        initial_particles,
        final_particles,
    )

    if any(
        _particle_category(particle) == "unknown"
        for particle in (
            *process.initial_particles,
            *process.final_particles,
        )
    ):
        return []

    candidates = []

    builders = (
        _qed_s_channel,
        _qed_t_channel,
        _qed_u_channel,
        _qcd_quark_antiquark_to_gluon_pair,
        _qcd_gluon_to_quark_pair,
        _qcd_three_gluon_channel,
    )

    for builder in builders:
        candidate = builder(process)

        if candidate is not None:
            candidates.append(asdict(candidate))

    return candidates


def topology_summary(
    initial_particles,
    final_particles,
):
    process = create_process(
        initial_particles,
        final_particles,
    )

    candidates = generate_tree_level_topologies(
        process.initial_particles,
        process.final_particles,
    )

    return {
        "success": True,
        "process": process.notation,
        "topology": process.topology_label,
        "initial_count": process.initial_count,
        "final_count": process.final_count,
        "candidate_count": len(candidates),
        "channels": [
            candidate["channel"]
            for candidate in candidates
        ],
        "candidates": candidates,
        "supports_general_multiplicity": True,
        "scientific_scope": (
            "General N-to-M process representation with "
            "selected tree-level QED and QCD topology rules. "
            "The process layer supports arbitrary multiplicity, "
            "while individual topology builders currently "
            "support selected 2-to-2 reactions."
        ),
    }
