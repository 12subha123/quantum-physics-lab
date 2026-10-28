from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class FourMomentumSymbol:
    label: str
    mass: str = "m"


@dataclass(frozen=True)
class SpinorCompleteness:
    particle: str
    momentum: str
    relation: str
    slash_sign: str
    mass_sign: str


@dataclass(frozen=True)
class SpinSumChain:
    factors: tuple[str, ...]
    trace_expression: str
    valid: bool
    errors: tuple[str, ...]


@dataclass(frozen=True)
class SpinSumResult:
    valid: bool
    relations: tuple[SpinorCompleteness, ...]
    chains: tuple[SpinSumChain, ...]
    errors: tuple[str, ...]


_FERMIONS = {
    "electron",
    "positron",
    "muon",
    "antimuon",
    "tau",
    "antitau",
    "up",
    "anti-up",
    "down",
    "anti-down",
    "strange",
    "anti-strange",
}


def _normalise(value: str) -> str:
    return str(value).strip().lower().replace("_", "-")


def _is_antifermion(particle: str) -> bool:
    return _normalise(particle) in {
        "positron",
        "antimuon",
        "antitau",
        "anti-up",
        "anti-down",
        "anti-strange",
    }


def _is_fermion(particle: str) -> bool:
    return _normalise(particle) in _FERMIONS


def completeness_relation(
    particle: str,
    momentum: str = "p",
    mass: str = "m",
) -> SpinorCompleteness:
    particle = str(particle)

    if not _is_fermion(particle):
        raise ValueError(
            f"Unsupported fermion species: {particle}"
        )

    if _is_antifermion(particle):
        slash_sign = "+"
        mass_sign = "-"
        relation = (
            f"sum_s v({momentum},s) vbar({momentum},s) "
            f"= slash({momentum}) - {mass}"
        )
    else:
        slash_sign = "+"
        mass_sign = "+"
        relation = (
            f"sum_s u({momentum},s) ubar({momentum},s) "
            f"= slash({momentum}) + {mass}"
        )

    return SpinorCompleteness(
        particle=particle,
        momentum=momentum,
        relation=relation,
        slash_sign=slash_sign,
        mass_sign=mass_sign,
    )


def build_spin_sum_trace(
    particle: str,
    momentum: str,
    mass: str = "m",
    left_chain: Iterable[str] = (),
    right_chain: Iterable[str] = (),
) -> SpinSumChain:
    if not _is_fermion(particle):
        return SpinSumChain(
            factors=(),
            trace_expression="0",
            valid=False,
            errors=(f"Unsupported fermion species: {particle}",),
        )

    completeness = completeness_relation(
        particle,
        momentum,
        mass,
    )

    slash_term = (
        f"slash({momentum})"
        f" {'+' if completeness.mass_sign == '+' else '-'} "
        f"{mass}"
    )

    factors = (
        *tuple(left_chain),
        slash_term,
        *tuple(right_chain),
    )

    trace_expression = (
        "Tr["
        + " ".join(factors)
        + "]"
    )

    return SpinSumChain(
        factors=factors,
        trace_expression=trace_expression,
        valid=True,
        errors=(),
    )


def construct_spin_sum(
    fermions: Iterable[tuple[str, str, str]],
) -> SpinSumResult:
    relations: list[SpinorCompleteness] = []
    errors: list[str] = []

    for particle, momentum, mass in fermions:
        try:
            relations.append(
                completeness_relation(
                    particle,
                    momentum,
                    mass,
                )
            )
        except ValueError as exc:
            errors.append(str(exc))

    chains: list[SpinSumChain] = []

    for relation in relations:
        chains.append(
            build_spin_sum_trace(
                relation.particle,
                relation.momentum,
                relation.relation.split()[-1]
                if relation.relation
                else "m",
            )
        )

    return SpinSumResult(
        valid=not errors and bool(relations),
        relations=tuple(relations),
        chains=tuple(chains),
        errors=tuple(errors),
    )


def spin_sum_summary(
    fermions: Iterable[tuple[str, str, str]],
):
    result = construct_spin_sum(fermions)

    return {
        "success": True,
        "valid": result.valid,
        "relation_count": len(result.relations),
        "relations": [
            {
                "particle": relation.particle,
                "momentum": relation.momentum,
                "relation": relation.relation,
                "slash_sign": relation.slash_sign,
                "mass_sign": relation.mass_sign,
            }
            for relation in result.relations
        ],
        "trace_chains": [
            {
                "factors": list(chain.factors),
                "trace_expression": chain.trace_expression,
                "valid": chain.valid,
                "errors": list(chain.errors),
            }
            for chain in result.chains
        ],
        "errors": list(result.errors),
        "scientific_scope": (
            "Tree-level fermion spinor completeness and symbolic spin-sum "
            "construction. The engine converts external spin sums into "
            "Dirac-trace structures but does not yet evaluate the traces, "
            "perform numerical spinor calculations, include polarization "
            "sums, or calculate a numerical matrix element."
        ),
    }
