from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class TwoBodyKinematics:
    sqrt_s: float
    initial_mass_1: float
    initial_mass_2: float
    final_mass_1: float
    final_mass_2: float
    initial_momentum: float
    final_momentum: float
    threshold: bool
    valid: bool
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class CrossSectionResult:
    valid: bool
    process: str
    s: float
    matrix_element_squared: float
    initial_momentum: float
    final_momentum: float
    differential_cross_section: float | None
    total_cross_section: float | None
    symmetry_factor: float
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class DecayRateResult:
    valid: bool
    process: str
    parent_mass: float
    matrix_element_squared: float
    final_momentum: float
    decay_width: float | None
    symmetry_factor: float
    errors: tuple[str, ...] = ()


def _validate_mass(mass: float, name: str) -> None:
    if not math.isfinite(mass) or mass < 0.0:
        raise ValueError(
            f"{name} must be finite and non-negative."
        )


def _validate_positive(value: float, name: str) -> None:
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(
            f"{name} must be finite and positive."
        )


def _kallen(
    x: float,
    y: float,
    z: float,
) -> float:
    return (
        x * x
        + y * y
        + z * z
        - 2.0 * x * y
        - 2.0 * x * z
        - 2.0 * y * z
    )


def two_body_kinematics(
    sqrt_s: float,
    initial_mass_1: float,
    initial_mass_2: float,
    final_mass_1: float,
    final_mass_2: float,
) -> TwoBodyKinematics:
    _validate_positive(sqrt_s, "sqrt_s")

    _validate_mass(initial_mass_1, "initial_mass_1")
    _validate_mass(initial_mass_2, "initial_mass_2")
    _validate_mass(final_mass_1, "final_mass_1")
    _validate_mass(final_mass_2, "final_mass_2")

    s = sqrt_s**2

    initial_lambda = _kallen(
        s,
        initial_mass_1**2,
        initial_mass_2**2,
    )

    final_lambda = _kallen(
        s,
        final_mass_1**2,
        final_mass_2**2,
    )

    if initial_lambda < -1e-10:
        return TwoBodyKinematics(
            sqrt_s=sqrt_s,
            initial_mass_1=initial_mass_1,
            initial_mass_2=initial_mass_2,
            final_mass_1=final_mass_1,
            final_mass_2=final_mass_2,
            initial_momentum=0.0,
            final_momentum=0.0,
            threshold=False,
            valid=False,
            errors=(
                "Initial state is kinematically inaccessible.",
            ),
        )

    if final_lambda < -1e-10:
        return TwoBodyKinematics(
            sqrt_s=sqrt_s,
            initial_mass_1=initial_mass_1,
            initial_mass_2=initial_mass_2,
            final_mass_1=final_mass_1,
            final_mass_2=final_mass_2,
            initial_momentum=math.sqrt(
                max(initial_lambda, 0.0)
            ) / (2.0 * sqrt_s),
            final_momentum=0.0,
            threshold=True,
            valid=False,
            errors=(
                "Final-state production threshold is not reached.",
            ),
        )

    initial_momentum = (
        math.sqrt(max(initial_lambda, 0.0))
        / (2.0 * sqrt_s)
    )

    final_momentum = (
        math.sqrt(max(final_lambda, 0.0))
        / (2.0 * sqrt_s)
    )

    return TwoBodyKinematics(
        sqrt_s=sqrt_s,
        initial_mass_1=initial_mass_1,
        initial_mass_2=initial_mass_2,
        final_mass_1=final_mass_1,
        final_mass_2=final_mass_2,
        initial_momentum=initial_momentum,
        final_momentum=final_momentum,
        threshold=False,
        valid=True,
        errors=(),
    )


def differential_cross_section_2_to_2(
    matrix_element_squared: float,
    sqrt_s: float,
    initial_mass_1: float = 0.0,
    initial_mass_2: float = 0.0,
    final_mass_1: float = 0.0,
    final_mass_2: float = 0.0,
    symmetry_factor: float = 1.0,
) -> CrossSectionResult:
    _validate_positive(
        matrix_element_squared,
        "matrix_element_squared",
    )

    _validate_positive(
        symmetry_factor,
        "symmetry_factor",
    )

    kin = two_body_kinematics(
        sqrt_s,
        initial_mass_1,
        initial_mass_2,
        final_mass_1,
        final_mass_2,
    )

    if not kin.valid:
        return CrossSectionResult(
            valid=False,
            process="2 -> 2",
            s=sqrt_s**2,
            matrix_element_squared=matrix_element_squared,
            initial_momentum=kin.initial_momentum,
            final_momentum=kin.final_momentum,
            differential_cross_section=None,
            total_cross_section=None,
            symmetry_factor=symmetry_factor,
            errors=kin.errors,
        )

    if kin.initial_momentum <= 0.0:
        return CrossSectionResult(
            valid=False,
            process="2 -> 2",
            s=sqrt_s**2,
            matrix_element_squared=matrix_element_squared,
            initial_momentum=kin.initial_momentum,
            final_momentum=kin.final_momentum,
            differential_cross_section=None,
            total_cross_section=None,
            symmetry_factor=symmetry_factor,
            errors=(
                "Initial-state momentum is zero; "
                "the scattering flux is singular.",
            ),
        )

    s = sqrt_s**2

    differential = (
        matrix_element_squared
        / (64.0 * math.pi**2 * s)
        * kin.final_momentum
        / kin.initial_momentum
        / symmetry_factor
    )

    total = (
        matrix_element_squared
        / (16.0 * math.pi * s)
        * kin.final_momentum
        / kin.initial_momentum
        / symmetry_factor
    )

    return CrossSectionResult(
        valid=True,
        process="2 -> 2",
        s=s,
        matrix_element_squared=matrix_element_squared,
        initial_momentum=kin.initial_momentum,
        final_momentum=kin.final_momentum,
        differential_cross_section=differential,
        total_cross_section=total,
        symmetry_factor=symmetry_factor,
        errors=(),
    )


def two_body_decay_width(
    matrix_element_squared: float,
    parent_mass: float,
    final_mass_1: float,
    final_mass_2: float,
    symmetry_factor: float = 1.0,
) -> DecayRateResult:
    _validate_positive(
        matrix_element_squared,
        "matrix_element_squared",
    )

    _validate_positive(
        parent_mass,
        "parent_mass",
    )

    _validate_mass(final_mass_1, "final_mass_1")
    _validate_mass(final_mass_2, "final_mass_2")

    _validate_positive(
        symmetry_factor,
        "symmetry_factor",
    )

    if parent_mass < final_mass_1 + final_mass_2:
        return DecayRateResult(
            valid=False,
            process="1 -> 2",
            parent_mass=parent_mass,
            matrix_element_squared=matrix_element_squared,
            final_momentum=0.0,
            decay_width=None,
            symmetry_factor=symmetry_factor,
            errors=(
                "Parent mass is below the decay threshold.",
            ),
        )

    s = parent_mass**2

    lam = _kallen(
        s,
        final_mass_1**2,
        final_mass_2**2,
    )

    final_momentum = (
        math.sqrt(max(lam, 0.0))
        / (2.0 * parent_mass)
    )

    width = (
        matrix_element_squared
        * final_momentum
        / (8.0 * math.pi * parent_mass**2)
        / symmetry_factor
    )

    return DecayRateResult(
        valid=True,
        process="1 -> 2",
        parent_mass=parent_mass,
        matrix_element_squared=matrix_element_squared,
        final_momentum=final_momentum,
        decay_width=width,
        symmetry_factor=symmetry_factor,
        errors=(),
    )


def cross_section_summary(
    matrix_element_squared: float,
    sqrt_s: float,
    final_mass_1: float = 0.0,
    final_mass_2: float = 0.0,
    symmetry_factor: float = 1.0,
) -> dict:
    result = differential_cross_section_2_to_2(
        matrix_element_squared=matrix_element_squared,
        sqrt_s=sqrt_s,
        final_mass_1=final_mass_1,
        final_mass_2=final_mass_2,
        symmetry_factor=symmetry_factor,
    )

    return {
        "success": True,
        "valid": result.valid,
        "process": result.process,
        "s": result.s,
        "matrix_element_squared": result.matrix_element_squared,
        "initial_momentum": result.initial_momentum,
        "final_momentum": result.final_momentum,
        "differential_cross_section": (
            result.differential_cross_section
        ),
        "total_cross_section": result.total_cross_section,
        "symmetry_factor": result.symmetry_factor,
        "errors": list(result.errors),
        "scientific_scope": (
            "Tree-level 2-to-2 scattering observables using "
            "Lorentz-invariant two-body phase space. "
            "The implementation assumes an angle-independent "
            "matrix element for the integrated total cross "
            "section. Angularly dependent amplitudes require "
            "explicit angular integration in a later layer."
        ),
    }


def decay_rate_summary(
    matrix_element_squared: float,
    parent_mass: float,
    final_mass_1: float,
    final_mass_2: float,
    symmetry_factor: float = 1.0,
) -> dict:
    result = two_body_decay_width(
        matrix_element_squared=matrix_element_squared,
        parent_mass=parent_mass,
        final_mass_1=final_mass_1,
        final_mass_2=final_mass_2,
        symmetry_factor=symmetry_factor,
    )

    return {
        "success": True,
        "valid": result.valid,
        "process": result.process,
        "parent_mass": result.parent_mass,
        "matrix_element_squared": (
            result.matrix_element_squared
        ),
        "final_momentum": result.final_momentum,
        "decay_width": result.decay_width,
        "symmetry_factor": result.symmetry_factor,
        "errors": list(result.errors),
        "scientific_scope": (
            "Tree-level two-body decay width using exact "
            "two-body phase space. Matrix elements are assumed "
            "spin-summed/averaged as appropriate before entering "
            "this layer."
        ),
    }
