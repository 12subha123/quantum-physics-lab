from __future__ import annotations

from dataclasses import dataclass, asdict
from math import pi, sqrt
from typing import Any


@dataclass(frozen=True)
class TwoBodyPhaseSpace:
    s: float
    initial_mass_1: float
    initial_mass_2: float
    final_mass_1: float
    final_mass_2: float
    initial_momentum: float | None
    final_momentum: float | None
    beta_final: float | None
    status: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class DifferentialCrossSection:
    s: float
    matrix_element_squared: float | None
    final_momentum: float | None
    initial_momentum: float | None
    value: float | None
    units: str
    formula: str
    status: str
    reasons: tuple[str, ...]


def _kallen(x: float, y: float, z: float) -> float:
    return (
        x * x
        + y * y
        + z * z
        - 2.0 * x * y
        - 2.0 * x * z
        - 2.0 * y * z
    )


def _two_body_momentum(
    s: float,
    mass_1: float,
    mass_2: float,
) -> float | None:

    if s <= 0.0:
        return None

    root_s = sqrt(s)

    if root_s < mass_1 + mass_2:
        return None

    lam = _kallen(
        s,
        mass_1 * mass_1,
        mass_2 * mass_2,
    )

    if lam < 0.0:
        return None

    return sqrt(lam) / (2.0 * root_s)


def build_two_body_phase_space(
    s: float,
    initial_mass_1: float,
    initial_mass_2: float,
    final_mass_1: float,
    final_mass_2: float,
) -> TwoBodyPhaseSpace:

    reasons: list[str] = []

    if s <= 0.0:
        return TwoBodyPhaseSpace(
            s=s,
            initial_mass_1=initial_mass_1,
            initial_mass_2=initial_mass_2,
            final_mass_1=final_mass_1,
            final_mass_2=final_mass_2,
            initial_momentum=None,
            final_momentum=None,
            beta_final=None,
            status="UNDECIDABLE",
            reasons=("s must be positive.",),
        )

    p_initial = _two_body_momentum(
        s,
        initial_mass_1,
        initial_mass_2,
    )

    p_final = _two_body_momentum(
        s,
        final_mass_1,
        final_mass_2,
    )

    if p_initial is None:
        reasons.append(
            "Initial-state two-body kinematics are not physically available."
        )

    if p_final is None:
        reasons.append(
            "Final-state threshold is not kinematically accessible."
        )

    beta_final = None

    if p_final is not None:
        energy_final_1 = sqrt(
            p_final * p_final
            + final_mass_1 * final_mass_1
        )

        if energy_final_1 > 0.0:
            beta_final = p_final / energy_final_1

    if reasons:
        return TwoBodyPhaseSpace(
            s=s,
            initial_mass_1=initial_mass_1,
            initial_mass_2=initial_mass_2,
            final_mass_1=final_mass_1,
            final_mass_2=final_mass_2,
            initial_momentum=p_initial,
            final_momentum=p_final,
            beta_final=beta_final,
            status="FORBIDDEN_KINEMATICS",
            reasons=tuple(reasons),
        )

    return TwoBodyPhaseSpace(
        s=s,
        initial_mass_1=initial_mass_1,
        initial_mass_2=initial_mass_2,
        final_mass_1=final_mass_1,
        final_mass_2=final_mass_2,
        initial_momentum=p_initial,
        final_momentum=p_final,
        beta_final=beta_final,
        status="CALCULATED",
        reasons=(),
    )


def differential_cross_section(
    phase_space: TwoBodyPhaseSpace,
    matrix_element_squared: float | None,
) -> DifferentialCrossSection:

    formula = (
        "dσ/dΩ = "
        "|M|² p_f / "
        "(64π² s p_i)"
    )

    if phase_space.status != "CALCULATED":
        return DifferentialCrossSection(
            s=phase_space.s,
            matrix_element_squared=matrix_element_squared,
            final_momentum=phase_space.final_momentum,
            initial_momentum=phase_space.initial_momentum,
            value=None,
            units="natural units",
            formula=formula,
            status="UNDECIDABLE",
            reasons=phase_space.reasons,
        )

    if matrix_element_squared is None:
        return DifferentialCrossSection(
            s=phase_space.s,
            matrix_element_squared=None,
            final_momentum=phase_space.final_momentum,
            initial_momentum=phase_space.initial_momentum,
            value=None,
            units="natural units",
            formula=formula,
            status="UNDECIDABLE",
            reasons=(
                "A numerical spin-summed/averaged |M|² is required.",
            ),
        )

    if matrix_element_squared < 0.0:
        return DifferentialCrossSection(
            s=phase_space.s,
            matrix_element_squared=matrix_element_squared,
            final_momentum=phase_space.final_momentum,
            initial_momentum=phase_space.initial_momentum,
            value=None,
            units="natural units",
            formula=formula,
            status="INVALID_MATRIX_ELEMENT",
            reasons=(
                "Squared matrix element cannot be negative.",
            ),
        )

    pi_initial = phase_space.initial_momentum
    pi_final = phase_space.final_momentum

    if pi_initial is None or pi_final is None or pi_initial <= 0.0:
        return DifferentialCrossSection(
            s=phase_space.s,
            matrix_element_squared=matrix_element_squared,
            final_momentum=pi_final,
            initial_momentum=pi_initial,
            value=None,
            units="natural units",
            formula=formula,
            status="UNDECIDABLE",
            reasons=(
                "Nonzero initial-state momentum is required.",
            ),
        )

    value = (
        matrix_element_squared
        * pi_final
        / (
            64.0
            * pi
            * pi
            * phase_space.s
            * pi_initial
        )
    )

    return DifferentialCrossSection(
        s=phase_space.s,
        matrix_element_squared=matrix_element_squared,
        final_momentum=pi_final,
        initial_momentum=pi_initial,
        value=value,
        units="natural units",
        formula=formula,
        status="CALCULATED",
        reasons=(),
    )


def phase_space_dict(
    phase_space: TwoBodyPhaseSpace,
) -> dict[str, Any]:

    return asdict(phase_space)


def differential_cross_section_dict(
    result: DifferentialCrossSection,
) -> dict[str, Any]:

    return asdict(result)
