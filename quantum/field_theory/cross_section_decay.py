from __future__ import annotations

from dataclasses import dataclass, asdict
from math import pi
from typing import Any


@dataclass(frozen=True)
class TotalCrossSection:
    differential_value: float | None
    total_value: float | None
    units: str
    integration: str
    status: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class DecayWidth:
    parent_mass: float
    final_mass_1: float
    final_mass_2: float
    matrix_element_squared: float | None
    final_momentum: float | None
    width: float | None
    units: str
    formula: str
    status: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class BranchingRatio:
    partial_width: float
    total_width: float
    branching_ratio: float | None
    status: str
    reasons: tuple[str, ...]


def integrate_isotropic_cross_section(
    differential_value: float | None,
) -> TotalCrossSection:

    if differential_value is None:
        return TotalCrossSection(
            differential_value=None,
            total_value=None,
            units="natural units",
            integration="∫dΩ = 4π",
            status="UNDECIDABLE",
            reasons=(
                "A numerical differential cross section is required.",
            ),
        )

    if differential_value < 0.0:
        return TotalCrossSection(
            differential_value=differential_value,
            total_value=None,
            units="natural units",
            integration="∫dΩ = 4π",
            status="INVALID_INPUT",
            reasons=(
                "Differential cross section cannot be negative.",
            ),
        )

    total = 4.0 * pi * differential_value

    return TotalCrossSection(
        differential_value=differential_value,
        total_value=total,
        units="natural units",
        integration="∫dΩ = 4π",
        status="CALCULATED",
        reasons=(),
    )


def build_decay_width(
    parent_mass: float,
    final_mass_1: float,
    final_mass_2: float,
    matrix_element_squared: float | None,
    final_momentum: float | None,
) -> DecayWidth:

    formula = (
        "Γ = |M|² p_f / "
        "(8π M²)"
    )

    if parent_mass <= 0.0:
        return DecayWidth(
            parent_mass=parent_mass,
            final_mass_1=final_mass_1,
            final_mass_2=final_mass_2,
            matrix_element_squared=matrix_element_squared,
            final_momentum=final_momentum,
            width=None,
            units="natural units",
            formula=formula,
            status="INVALID_INPUT",
            reasons=("Parent mass must be positive.",),
        )

    if parent_mass < final_mass_1 + final_mass_2:
        return DecayWidth(
            parent_mass=parent_mass,
            final_mass_1=final_mass_1,
            final_mass_2=final_mass_2,
            matrix_element_squared=matrix_element_squared,
            final_momentum=None,
            width=None,
            units="natural units",
            formula=formula,
            status="FORBIDDEN_KINEMATICS",
            reasons=(
                "Parent mass is below the two-body decay threshold.",
            ),
        )

    if final_momentum is None:
        return DecayWidth(
            parent_mass=parent_mass,
            final_mass_1=final_mass_1,
            final_mass_2=final_mass_2,
            matrix_element_squared=matrix_element_squared,
            final_momentum=None,
            width=None,
            units="natural units",
            formula=formula,
            status="UNDECIDABLE",
            reasons=(
                "Final-state momentum is required.",
            ),
        )

    if matrix_element_squared is None:
        return DecayWidth(
            parent_mass=parent_mass,
            final_mass_1=final_mass_1,
            final_mass_2=final_mass_2,
            matrix_element_squared=None,
            final_momentum=final_momentum,
            width=None,
            units="natural units",
            formula=formula,
            status="UNDECIDABLE",
            reasons=(
                "A numerical matrix element squared is required.",
            ),
        )

    if matrix_element_squared < 0.0:
        return DecayWidth(
            parent_mass=parent_mass,
            final_mass_1=final_mass_1,
            final_mass_2=final_mass_2,
            matrix_element_squared=matrix_element_squared,
            final_momentum=final_momentum,
            width=None,
            units="natural units",
            formula=formula,
            status="INVALID_INPUT",
            reasons=(
                "Squared matrix element cannot be negative.",
            ),
        )

    width = (
        matrix_element_squared
        * final_momentum
        / (
            8.0
            * pi
            * parent_mass
            * parent_mass
        )
    )

    return DecayWidth(
        parent_mass=parent_mass,
        final_mass_1=final_mass_1,
        final_mass_2=final_mass_2,
        matrix_element_squared=matrix_element_squared,
        final_momentum=final_momentum,
        width=width,
        units="natural units",
        formula=formula,
        status="CALCULATED",
        reasons=(),
    )


def build_branching_ratio(
    partial_width: float,
    total_width: float,
) -> BranchingRatio:

    if partial_width < 0.0:
        return BranchingRatio(
            partial_width=partial_width,
            total_width=total_width,
            branching_ratio=None,
            status="INVALID_INPUT",
            reasons=("Partial width cannot be negative.",),
        )

    if total_width <= 0.0:
        return BranchingRatio(
            partial_width=partial_width,
            total_width=total_width,
            branching_ratio=None,
            status="INVALID_INPUT",
            reasons=("Total width must be positive.",),
        )

    if partial_width > total_width:
        return BranchingRatio(
            partial_width=partial_width,
            total_width=total_width,
            branching_ratio=None,
            status="INVALID_INPUT",
            reasons=(
                "Partial width cannot exceed total width.",
            ),
        )

    return BranchingRatio(
        partial_width=partial_width,
        total_width=total_width,
        branching_ratio=partial_width / total_width,
        status="CALCULATED",
        reasons=(),
    )


def total_cross_section_dict(
    result: TotalCrossSection,
) -> dict[str, Any]:

    return asdict(result)


def decay_width_dict(
    result: DecayWidth,
) -> dict[str, Any]:

    return asdict(result)


def branching_ratio_dict(
    result: BranchingRatio,
) -> dict[str, Any]:

    return asdict(result)
