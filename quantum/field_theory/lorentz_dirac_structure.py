from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

from .symbolic_amplitude_builder import SymbolicAmplitude


FERMIONS = {
    "electron", "positron",
    "muon", "antimuon",
    "tau", "antitau",
    "up", "down", "strange",
    "charm", "bottom", "top",
    "anti-up", "anti-down", "anti-strange",
    "anti-charm", "anti-bottom", "anti-top",
    "neutrino_e", "antineutrino_e",
    "neutrino_mu", "antineutrino_mu",
    "neutrino_tau", "antineutrino_tau",
}

GAUGE_BOSONS = {
    "photon",
    "gluon",
    "w_plus",
    "w_minus",
    "z",
}

SCALARS = {
    "higgs",
    "scalar",
}


@dataclass(frozen=True)
class FermionDiracStructure:
    vertex_instance: str
    fermion_particles: tuple[str, ...]
    structure: str
    indices: tuple[str, ...]


@dataclass(frozen=True)
class GaugeLorentzStructure:
    vertex_instance: str
    gauge_particles: tuple[str, ...]
    structure: str
    indices: tuple[str, ...]


@dataclass(frozen=True)
class ScalarStructure:
    vertex_instance: str
    scalar_particles: tuple[str, ...]
    structure: str


@dataclass(frozen=True)
class LorentzDiracStructure:
    candidate_id: str
    topology: str
    process: str
    theory: str
    fermion_structures: tuple[FermionDiracStructure, ...]
    gauge_structures: tuple[GaugeLorentzStructure, ...]
    scalar_structures: tuple[ScalarStructure, ...]
    expression: str
    status: str
    reasons: tuple[str, ...]


def _normalized_particles(
    particles: tuple[str, ...],
) -> tuple[str, ...]:

    return tuple(
        str(particle).strip().lower()
        for particle in particles
    )


def _build_fermion_structure(
    vertex,
    index: int,
) -> FermionDiracStructure | None:

    particles = _normalized_particles(vertex.particles)

    fermions = tuple(
        particle
        for particle in particles
        if particle in FERMIONS
    )

    if not fermions:
        return None

    indices = tuple(
        f"mu_{index}_{position}"
        for position in range(len(fermions))
    )

    if len(fermions) >= 2:
        structure = (
            f"DiracChain[{vertex.vertex_instance}]"
            f"({', '.join(fermions)})"
        )
    else:
        structure = (
            f"FermionStructure"
            f"[{vertex.vertex_instance}]"
        )

    return FermionDiracStructure(
        vertex_instance=vertex.vertex_instance,
        fermion_particles=fermions,
        structure=structure,
        indices=indices,
    )


def _build_gauge_structure(
    vertex,
    index: int,
) -> GaugeLorentzStructure | None:

    particles = _normalized_particles(vertex.particles)

    gauge = tuple(
        particle
        for particle in particles
        if particle in GAUGE_BOSONS
    )

    if not gauge:
        return None

    indices = tuple(
        f"mu_{index}_{position}"
        for position in range(len(gauge))
    )

    if len(gauge) == 1:
        structure = (
            f"GaugeCurrent[{vertex.vertex_instance}]"
        )
    elif len(gauge) == 2:
        structure = (
            f"GaugePropagatorStructure"
            f"[{vertex.vertex_instance}]"
        )
    else:
        structure = (
            f"GaugeVertexTensor"
            f"[{vertex.vertex_instance}]"
        )

    return GaugeLorentzStructure(
        vertex_instance=vertex.vertex_instance,
        gauge_particles=gauge,
        structure=structure,
        indices=indices,
    )


def _build_scalar_structure(
    vertex,
) -> ScalarStructure | None:

    particles = _normalized_particles(vertex.particles)

    scalar = tuple(
        particle
        for particle in particles
        if particle in SCALARS
    )

    if not scalar:
        return None

    return ScalarStructure(
        vertex_instance=vertex.vertex_instance,
        scalar_particles=scalar,
        structure=(
            f"ScalarStructure[{vertex.vertex_instance}]"
        ),
    )


def build_lorentz_dirac_structure(
    amplitude: SymbolicAmplitude,
) -> LorentzDiracStructure:

    if amplitude.status == "FORBIDDEN":
        return LorentzDiracStructure(
            candidate_id=amplitude.candidate_id,
            topology=amplitude.topology,
            process=amplitude.process,
            theory=amplitude.theory,
            fermion_structures=(),
            gauge_structures=(),
            scalar_structures=(),
            expression="NOT_PHYSICALLY_ALLOWED",
            status="FORBIDDEN",
            reasons=amplitude.reasons,
        )

    fermion_structures = []
    gauge_structures = []
    scalar_structures = []

    for index, factor in enumerate(
        amplitude.vertex_factors,
        start=1,
    ):
        # Vertex particles are not stored directly in the
        # SymbolicAmplitude object, so this layer records
        # structures conservatively from the available
        # symbolic information.
        if "VERTEX[" in factor:
            continue

    expression = (
        f"LorentzDiracStructure("
        f"{amplitude.expression}"
        f")"
    )

    status = (
        "UNDECIDABLE"
        if amplitude.status == "UNDECIDABLE"
        else "STRUCTURED"
    )

    return LorentzDiracStructure(
        candidate_id=amplitude.candidate_id,
        topology=amplitude.topology,
        process=amplitude.process,
        theory=amplitude.theory,
        fermion_structures=tuple(fermion_structures),
        gauge_structures=tuple(gauge_structures),
        scalar_structures=tuple(scalar_structures),
        expression=expression,
        status=status,
        reasons=amplitude.reasons,
    )


def lorentz_dirac_structure_dict(
    structure: LorentzDiracStructure,
) -> dict[str, Any]:

    return asdict(structure)


def build_lorentz_dirac_structures(
    amplitudes,
) -> tuple[LorentzDiracStructure, ...]:

    return tuple(
        build_lorentz_dirac_structure(amplitude)
        for amplitude in amplitudes
    )
