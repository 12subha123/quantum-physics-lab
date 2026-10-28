from dataclasses import dataclass
from math import cos, pi, sin

from quantum.field_theory.qcd_matrix_element import (
    qcd_qqbar_to_gg_matrix_element,
)


@dataclass(frozen=True)
class QCDAngularPoint:
    theta: float
    cos_theta: float
    s: float
    t: float
    u: float
    matrix_element_squared: float
    differential_cross_section: float


@dataclass(frozen=True)
class QCDAngularIntegrationResult:
    success: bool
    valid: bool
    process: str
    sqrt_s: float
    alpha_s: float
    angular_cut: float
    points: tuple[QCDAngularPoint, ...]
    total_cross_section: float | None
    errors: tuple[str, ...]
    scientific_scope: str


def _validate(
    sqrt_s: float,
    alpha_s: float,
    angular_cut: float,
    points: int,
) -> None:
    if sqrt_s <= 0.0:
        raise ValueError("sqrt_s must be positive.")

    if alpha_s <= 0.0:
        raise ValueError("alpha_s must be positive.")

    if not (0.0 < angular_cut < pi / 2.0):
        raise ValueError(
            "angular_cut must satisfy 0 < angular_cut < pi/2."
        )

    if points < 2:
        raise ValueError("points must be at least 2.")


def _mandelstam_from_angle(
    sqrt_s: float,
    theta: float,
) -> tuple[float, float, float]:
    s = sqrt_s * sqrt_s

    c = cos(theta)

    t = -0.5 * s * (1.0 - c)
    u = -0.5 * s * (1.0 + c)

    return s, t, u


def differential_cross_section(
    sqrt_s: float,
    theta: float,
    alpha_s: float = 0.118,
) -> QCDAngularPoint:

    if not (0.0 < theta < pi):
        raise ValueError("theta must satisfy 0 < theta < pi.")

    s, t, u = _mandelstam_from_angle(
        sqrt_s,
        theta,
    )

    result = qcd_qqbar_to_gg_matrix_element(
        s,
        t,
        u,
        alpha_s,
    )

    if not result.valid or result.ms_squared is None:
        raise ValueError(
            "; ".join(result.errors)
            if result.errors
            else "QCD matrix element evaluation failed."
        )

    dsigma_domega = result.ms_squared / (
        64.0 * pi * pi * s
    )

    return QCDAngularPoint(
        theta=theta,
        cos_theta=cos(theta),
        s=s,
        t=t,
        u=u,
        matrix_element_squared=result.ms_squared,
        differential_cross_section=dsigma_domega,
    )


def integrate_qcd_angular_cross_section(
    sqrt_s: float,
    alpha_s: float = 0.118,
    angular_cut: float = 0.1,
    points: int = 200,
) -> QCDAngularIntegrationResult:

    try:
        _validate(
            sqrt_s,
            alpha_s,
            angular_cut,
            points,
        )
    except ValueError as exc:
        return QCDAngularIntegrationResult(
            success=True,
            valid=False,
            process="q + anti-q -> g + g",
            sqrt_s=sqrt_s,
            alpha_s=alpha_s,
            angular_cut=angular_cut,
            points=(),
            total_cross_section=None,
            errors=(str(exc),),
            scientific_scope="",
        )

    theta_min = angular_cut
    theta_max = pi - angular_cut

    step = (theta_max - theta_min) / (points - 1)

    angular_points = []

    for i in range(points):
        theta = theta_min + i * step

        point = differential_cross_section(
            sqrt_s=sqrt_s,
            theta=theta,
            alpha_s=alpha_s,
        )

        angular_points.append(point)

    total = 0.0

    for i in range(len(angular_points) - 1):
        p1 = angular_points[i]
        p2 = angular_points[i + 1]

        f1 = 2.0 * pi * sin(p1.theta) * p1.differential_cross_section
        f2 = 2.0 * pi * sin(p2.theta) * p2.differential_cross_section

        total += 0.5 * (f1 + f2) * step

    return QCDAngularIntegrationResult(
        success=True,
        valid=True,
        process="q + anti-q -> g + g",
        sqrt_s=sqrt_s,
        alpha_s=alpha_s,
        angular_cut=angular_cut,
        points=tuple(angular_points),
        total_cross_section=total,
        errors=(),
        scientific_scope=(
            "Leading-order massless QCD q + anti-q -> g + g. "
            "Spin-averaged and color-averaged initial state. "
            "Numerical angular integration uses an explicit "
            "forward/backward angular cut because the massless "
            "t/u-channel structure is singular at the endpoints. "
            "No loop corrections, running-coupling evolution, "
            "hadronization, or detector effects."
        ),
    )


def qcd_angular_observable_summary(
    sqrt_s: float = 10.0,
    alpha_s: float = 0.118,
    angular_cut: float = 0.1,
    points: int = 200,
) -> dict:

    result = integrate_qcd_angular_cross_section(
        sqrt_s=sqrt_s,
        alpha_s=alpha_s,
        angular_cut=angular_cut,
        points=points,
    )

    return {
        "success": result.success,
        "valid": result.valid,
        "process": result.process,
        "sqrt_s": result.sqrt_s,
        "alpha_s": result.alpha_s,
        "angular_cut": result.angular_cut,
        "point_count": len(result.points),
        "total_cross_section": result.total_cross_section,
        "errors": list(result.errors),
        "scientific_scope": result.scientific_scope,
    }
