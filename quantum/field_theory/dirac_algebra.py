from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class Spinor:
    particle: str
    momentum: str
    kind: str
    index: str


@dataclass(frozen=True)
class GammaMatrix:
    lorentz_index: str
    matrix_index_left: str
    matrix_index_right: str


@dataclass(frozen=True)
class ChiralProjector:
    chirality: str
    expression: str


@dataclass(frozen=True)
class DiracChain:
    chain_id: str
    particles: tuple[str, ...]
    spinors: tuple[Spinor, ...]
    gamma_matrices: tuple[GammaMatrix, ...]
    projectors: tuple[ChiralProjector, ...]
    expression: str


@dataclass(frozen=True)
class SpinSum:
    particle: str
    momentum: str
    expression: str


@dataclass(frozen=True)
class DiracAlgebraResult:
    candidate_id: str
    topology: str
    process: str
    theory: str
    chains: tuple[DiracChain, ...]
    spin_sums: tuple[SpinSum, ...]
    expression: str
    status: str
    reasons: tuple[str, ...]


def _is_fermion(name: str) -> bool:
    return name.lower() in {
        "electron", "positron",
        "muon", "antimuon",
        "tau", "antitau",
        "up", "down", "strange",
        "charm", "bottom", "top",
        "anti-up", "anti-down",
        "anti-strange", "anti-charm",
        "anti-bottom", "anti-top",
        "neutrino_e", "antineutrino_e",
        "neutrino_mu", "antineutrino_mu",
        "neutrino_tau", "antineutrino_tau",
    }


def _spinor_kind(particle: str) -> str:
    name = particle.lower()

    if name.startswith("anti") or name in {
        "positron",
        "antimuon",
        "antitau",
        "anti-up",
        "anti-down",
        "anti-strange",
        "anti-charm",
        "anti-bottom",
        "anti-top",
        "antineutrino_e",
        "antineutrino_mu",
        "antineutrino_tau",
    }:
        return "v"

    return "u"


def _spinor_expression(spinor: Spinor) -> str:
    if spinor.kind == "u":
        return f"u({spinor.momentum})"

    return f"v({spinor.momentum})"


def build_spinor(
    particle: str,
    momentum: str,
    index: str,
) -> Spinor:

    return Spinor(
        particle=particle,
        momentum=momentum,
        kind=_spinor_kind(particle),
        index=index,
    )


def gamma(
    lorentz_index: str,
    left: str,
    right: str,
) -> GammaMatrix:

    return GammaMatrix(
        lorentz_index=lorentz_index,
        matrix_index_left=left,
        matrix_index_right=right,
    )


def P_L() -> ChiralProjector:
    return ChiralProjector(
        chirality="L",
        expression="P_L = (1 - gamma^5)/2",
    )


def P_R() -> ChiralProjector:
    return ChiralProjector(
        chirality="R",
        expression="P_R = (1 + gamma^5)/2",
    )


def build_dirac_chain(
    chain_id: str,
    particles: tuple[str, ...],
    momenta: tuple[str, ...],
) -> DiracChain:

    fermions = tuple(
        particle
        for particle in particles
        if _is_fermion(particle)
    )

    spinors = tuple(
        build_spinor(
            particle,
            momenta[index] if index < len(momenta) else f"p{index + 1}",
            f"s{index + 1}",
        )
        for index, particle in enumerate(fermions)
    )

    if len(spinors) >= 2:
        matrices = (
            gamma("mu", "a", "b"),
        )

        expression = (
            f"bar({ _spinor_expression(spinors[0]) }) "
            f"gamma^mu "
            f"{_spinor_expression(spinors[1])}"
        )
    else:
        matrices = ()
        expression = "UNRESOLVED_DIRAC_CHAIN"

    return DiracChain(
        chain_id=chain_id,
        particles=fermions,
        spinors=spinors,
        gamma_matrices=matrices,
        projectors=(),
        expression=expression,
    )


def spin_sum(
    particle: str,
    momentum: str,
) -> SpinSum:

    kind = _spinor_kind(particle)

    if kind == "u":
        expression = (
            f"sum_s u({momentum},s) "
            f"bar(u({momentum},s)) = "
            f"slash({momentum}) + m"
        )
    else:
        expression = (
            f"sum_s v({momentum},s) "
            f"bar(v({momentum},s)) = "
            f"slash({momentum}) - m"
        )

    return SpinSum(
        particle=particle,
        momentum=momentum,
        expression=expression,
    )


def build_dirac_algebra(
    candidate_id: str,
    topology: str,
    process: str,
    theory: str,
    fermion_chains: tuple[DiracChain, ...] = (),
    spin_sums: tuple[SpinSum, ...] = (),
    expression: str = "",
    status: str = "STRUCTURED",
    reasons: tuple[str, ...] = (),
) -> DiracAlgebraResult:

    return DiracAlgebraResult(
        candidate_id=candidate_id,
        topology=topology,
        process=process,
        theory=theory,
        chains=fermion_chains,
        spin_sums=spin_sums,
        expression=expression or "UNRESOLVED_DIRAC_ALGEBRA",
        status=status,
        reasons=reasons,
    )


def dirac_algebra_dict(
    result: DiracAlgebraResult,
) -> dict[str, Any]:

    return asdict(result)
