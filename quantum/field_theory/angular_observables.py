from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable


@dataclass(frozen=True)
class AngularPoint:
    theta: float
    cos_theta: float
    s: float
    t: float
    u: float
    matrix_element_squared: float
    differential_cross_section: float


@dataclass(frozen=True)
class AngularIntegrationResult:
    valid: bool
    process: str
    sqrt_s: float
    points: tuple[AngularPoint, ...]
    total_cross_section: float | None
    integration_error_estimate: float | None
    errors: tuple[str, ...] = ()


def _validate(
    sqrt_s: float,
    number_of_points: int,
) -> list[str]:
    errors = []

    if not math.isfinite(sqrt_s) or sqrt_s <= 0.0:
        errors.append("sqrt_s must be finite and positive.")

    if number_of_points < 2:
        errors.append("number_of_points must be at least 2.")

    return errors


def _mandelstam_from_angle(
    sqrt_s: float,
    theta: float,
) -> tuple[float, float, float]:
    s = sqrt_s**2

    t = -s * math.sin(theta / 2.0)**2
    u = -s * math.cos(theta / 2.0)**2

    return s, t, u


def _default_qed_annihilation(
    s: float,
    t: float,
    u: float,
) -> float:
    from quantum.field_theory.matrix_element import (
        ALPHA_EM,
    )

    e = math.sqrt(4.0 * math.pi * ALPHA_EM)

    return (
        2.0
        * e**4
        * (u**2 + t**2)
        / s**2
    )


def differential_cross_section_from_msquared(
    matrix_element_squared: float,
    s: float,
) -> float:
    if matrix_element_squared < 0.0:
        raise ValueError(
            "Matrix element squared cannot be negative."
        )

    if s <= 0.0:
        raise ValueError("s must be positive.")

    return (
        matrix_element_squared
        / (64.0 * math.pi**2 * s)
    )


def integrate_2_to_2(
    sqrt_s: float,
    matrix_element_function: Callable[
        [float, float, float],
        float,
    ] = _default_qed_annihilation,
    process: str = "e- + e+ -> mu- + mu+",
    theta_min: float = 1e-5,
    theta_max: float = math.pi - 1e-5,
    number_of_points: int = 1000,
) -> AngularIntegrationResult:
    errors = _validate(
        sqrt_s,
        number_of_points,
    )

    if theta_min < 0.0:
        errors.append("theta_min must be non-negative.")

    if theta_max > math.pi:
        errors.append("theta_max must not exceed pi.")

    if theta_min >= theta_max:
        errors.append("theta_min must be smaller than theta_max.")

    if errors:
        return AngularIntegrationResult(
            valid=False,
            process=process,
            sqrt_s=sqrt_s,
            points=(),
            total_cross_section=None,
            integration_error_estimate=None,
            errors=tuple(errors),
        )

    step = (
        theta_max - theta_min
    ) / (number_of_points - 1)

    points = []

    # Trapezoidal integration over theta.
    # dOmega = 2*pi*sin(theta)dtheta.
    integral = 0.0
    previous_value = None

    for i in range(number_of_points):
        theta = theta_min + i * step

        s, t, u = _mandelstam_from_angle(
            sqrt_s,
            theta,
        )

        ms_squared = float(
            matrix_element_function(s, t, u)
        )

        if not math.isfinite(ms_squared):
            return AngularIntegrationResult(
                valid=False,
                process=process,
                sqrt_s=sqrt_s,
                points=tuple(points),
                total_cross_section=None,
                integration_error_estimate=None,
                errors=(
                    f"Non-finite |M|^2 at theta={theta}.",
                ),
            )

        if ms_squared < 0.0:
            return AngularIntegrationResult(
                valid=False,
                process=process,
                sqrt_s=sqrt_s,
                points=tuple(points),
                total_cross_section=None,
                integration_error_estimate=None,
                errors=(
                    f"Negative |M|^2 at theta={theta}.",
                ),
            )

        differential = (
            differential_cross_section_from_msquared(
                ms_squared,
                s,
            )
        )

        weighted = (
            differential
            * 2.0
            * math.pi
            * math.sin(theta)
        )

        if previous_value is not None:
            integral += (
                0.5
                * (previous_value + weighted)
                * step
            )

        previous_value = weighted

        points.append(
            AngularPoint(
                theta=theta,
                cos_theta=math.cos(theta),
                s=s,
                t=t,
                u=u,
                matrix_element_squared=ms_squared,
                differential_cross_section=differential,
            )
        )

    # Estimate integration error by comparing with
    # a coarser sampling of every second point.
    coarse = 0.0

    if len(points) >= 5:
        for i in range(2, len(points), 2):
            a = points[i - 2]
            b = points[i]

            fa = (
                a.differential_cross_section
                * 2.0
                * math.pi
                * math.sin(a.theta)
            )

            fb = (
                b.differential_cross_section
                * 2.0
                * math.pi
                * math.sin(b.theta)
            )

            coarse += 0.5 * (fa + fb) * (2.0 * step)

    error_estimate = abs(integral - coarse)

    return AngularIntegrationResult(
        valid=True,
        process=process,
        sqrt_s=sqrt_s,
        points=tuple(points),
        total_cross_section=integral,
        integration_error_estimate=error_estimate,
        errors=(),
    )


def angular_observable_summary(
    sqrt_s: float = 10.0,
    number_of_points: int = 1000,
) -> dict:
    result = integrate_2_to_2(
        sqrt_s=sqrt_s,
        number_of_points=number_of_points,
    )

    return {
        "success": True,
        "valid": result.valid,
        "process": result.process,
        "sqrt_s": result.sqrt_s,
        "point_count": len(result.points),
        "total_cross_section": result.total_cross_section,
        "integration_error_estimate": (
            result.integration_error_estimate
        ),
        "angular_scan": [
            {
                "theta": point.theta,
                "cos_theta": point.cos_theta,
                "s": point.s,
                "t": point.t,
                "u": point.u,
                "matrix_element_squared": (
                    point.matrix_element_squared
                ),
                "differential_cross_section": (
                    point.differential_cross_section
                ),
            }
            for point in result.points
        ],
        "errors": list(result.errors),
        "scientific_scope": (
            "Numerical angular integration of tree-level "
            "2-to-2 differential cross sections. Mandelstam "
            "variables are generated from the scattering angle "
            "in the massless COM limit. The matrix-element "
            "function is supplied independently, allowing the "
            "same integration layer to serve different "
            "interactions. Forward/backward singular limits "
            "must be regulated explicitly when a process has "
            "t- or u-channel poles."
        ),
    }
