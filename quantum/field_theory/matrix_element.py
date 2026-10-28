from __future__ import annotations

from dataclasses import dataclass
from math import pi
from typing import Mapping


@dataclass(frozen=True)
class MatrixElementResult:
    process: str
    theory: str
    valid: bool
    ms_squared: float | None
    amplitude_squared_expression: str
    differential_cross_section_expression: str
    substitutions: dict[str, float]
    errors: tuple[str, ...] = ()
    scientific_scope: str = ""


ALPHA_EM = 1.0 / 137.035999084


def _validate_invariants(
    s: float,
    t: float,
    u: float,
    tolerance: float = 1e-8,
) -> list[str]:
    errors: list[str] = []

    if s <= 0.0:
        errors.append("s must be positive.")

    if not all(
        value == value and abs(value) != float("inf")
        for value in (s, t, u)
    ):
        errors.append("Mandelstam invariants must be finite.")

    return errors


def _electric_charge() -> float:
    from math import sqrt

    return sqrt(4.0 * pi * ALPHA_EM)


def electron_muon_annihilation(
    s: float,
    t: float,
    u: float,
) -> MatrixElementResult:
    errors = _validate_invariants(s, t, u)

    if errors:
        return MatrixElementResult(
            process="e- + e+ -> mu- + mu+",
            theory="QED",
            valid=False,
            ms_squared=None,
            amplitude_squared_expression="",
            differential_cross_section_expression="",
            substitutions={"s": s, "t": t, "u": u},
            errors=tuple(errors),
            scientific_scope="Tree-level QED.",
        )

    e = _electric_charge()

    ms_squared = (
        2.0
        * e**4
        * (u**2 + t**2)
        / s**2
    )

    return MatrixElementResult(
        process="e- + e+ -> mu- + mu+",
        theory="QED",
        valid=True,
        ms_squared=ms_squared,
        amplitude_squared_expression=(
            "2 e^4 (u^2 + t^2) / s^2"
        ),
        differential_cross_section_expression=(
            "dσ/dΩ = |M|² / (64 π² s)"
        ),
        substitutions={
            "s": s,
            "t": t,
            "u": u,
            "alpha_em": ALPHA_EM,
            "e": e,
        },
        errors=(),
        scientific_scope=(
            "Tree-level QED, massless external-fermion "
            "spin-summed and initial-spin-averaged result. "
            "No loops, radiative corrections, or "
            "dimensional regularization."
        ),
    )


def evaluate_spin_summed_matrix_element(
    process: str,
    s: float,
    t: float,
    u: float,
) -> MatrixElementResult:
    key = process.strip().lower()

    if key in {
        "electron_muon_annihilation",
        "e+e-->mu+mu-",
        "e-e+->mu-mu+",
        "e_mu_annihilation",
    }:
        return electron_muon_annihilation(
            s,
            t,
            u,
        )

    return MatrixElementResult(
        process=process,
        theory="Unknown",
        valid=False,
        ms_squared=None,
        amplitude_squared_expression="",
        differential_cross_section_expression="",
        substitutions={"s": s, "t": t, "u": u},
        errors=(
            f"No spin-summed evaluator registered for process: {process}",
        ),
        scientific_scope=(
            "The process must be connected to a validated "
            "Feynman-rule and trace evaluator before a "
            "numerical matrix element is returned."
        ),
    )


def matrix_element_summary(
    process: str,
    s: float,
    t: float,
    u: float,
) -> dict:
    result = evaluate_spin_summed_matrix_element(
        process,
        s,
        t,
        u,
    )

    return {
        "success": True,
        "valid": result.valid,
        "process": result.process,
        "theory": result.theory,
        "ms_squared": result.ms_squared,
        "amplitude_squared_expression": (
            result.amplitude_squared_expression
        ),
        "differential_cross_section_expression": (
            result.differential_cross_section_expression
        ),
        "substitutions": result.substitutions,
        "errors": list(result.errors),
        "scientific_scope": result.scientific_scope,
    }
