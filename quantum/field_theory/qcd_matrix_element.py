from dataclasses import dataclass


@dataclass(frozen=True)
class QCDMatrixElementResult:
    valid: bool
    process: str
    theory: str
    expression: str
    color_average: str
    spin_average: str
    coupling: str
    substitutions: dict[str, float]
    ms_squared: float | None
    errors: tuple[str, ...] = ()
    scientific_scope: str = ""


def _validate_invariants(
    s: float,
    t: float,
    u: float,
) -> None:
    if s <= 0.0:
        raise ValueError("s must be positive.")

    if t >= 0.0:
        raise ValueError("For physical massless 2->2 scattering, t must be negative.")

    if u >= 0.0:
        raise ValueError("For physical massless 2->2 scattering, u must be negative.")

    residual = s + t + u

    scale = max(abs(s), abs(t), abs(u), 1.0)

    if abs(residual) > 1e-9 * scale:
        raise ValueError(
            "Massless Mandelstam invariants must satisfy s + t + u = 0."
        )


def qcd_qqbar_to_gg_matrix_element(
    s: float,
    t: float,
    u: float,
    alpha_s: float,
) -> QCDMatrixElementResult:
    try:
        _validate_invariants(s, t, u)

        if alpha_s <= 0.0:
            raise ValueError("alpha_s must be positive.")

        # g_s^2 = 4 pi alpha_s
        # The following is the standard tree-level,
        # spin-averaged and color-averaged q qbar -> g g
        # invariant structure used by this educational engine.
        #
        # |M|^2 =
        # (32/27) g_s^4 (u^2+t^2)/(u t)
        # - (8/3) g_s^4 (u^2+t^2)/s^2
        #
        # Physical region: s > 0, t < 0, u < 0,
        # and s+t+u=0.

        gs_squared = 4.0 * 3.141592653589793 * alpha_s
        gs_fourth = gs_squared**2

        ms_squared = (
            (32.0 / 27.0)
            * gs_fourth
            * (u**2 + t**2)
            / (u * t)
            - (8.0 / 3.0)
            * gs_fourth
            * (u**2 + t**2)
            / s**2
        )

        if ms_squared < -1e-12:
            raise ValueError(
                "Computed |M|^2 is negative; check the kinematic region."
            )

        ms_squared = max(ms_squared, 0.0)

        return QCDMatrixElementResult(
            valid=True,
            process="q + anti-q -> g + g",
            theory="QCD",
            expression=(
                "|M|^2 = (32/27) g_s^4 "
                "(u^2+t^2)/(u t) "
                "- (8/3) g_s^4 "
                "(u^2+t^2)/s^2"
            ),
            color_average="Average over initial quark and antiquark colors.",
            spin_average="Average over initial quark and antiquark spins.",
            coupling="g_s^2 = 4 pi alpha_s",
            substitutions={
                "s": s,
                "t": t,
                "u": u,
                "alpha_s": alpha_s,
                "g_s^2": gs_squared,
            },
            ms_squared=ms_squared,
            errors=(),
            scientific_scope=(
                "Tree-level massless QCD q-qbar -> g-g matrix element. "
                "Spin-averaged and color-averaged initial state. "
                "No loop corrections, running-coupling evolution, "
                "hadronization, or higher-order QCD corrections."
            ),
        )

    except ValueError as exc:
        return QCDMatrixElementResult(
            valid=False,
            process="q + anti-q -> g + g",
            theory="QCD",
            expression="",
            color_average="",
            spin_average="",
            coupling="",
            substitutions={},
            ms_squared=None,
            errors=(str(exc),),
            scientific_scope=(
                "Tree-level QCD matrix-element evaluation."
            ),
        )


def qcd_matrix_element_summary(
    s: float = 100.0,
    t: float = -50.0,
    u: float = -50.0,
    alpha_s: float = 0.118,
) -> dict:
    result = qcd_qqbar_to_gg_matrix_element(
        s=s,
        t=t,
        u=u,
        alpha_s=alpha_s,
    )

    return {
        "success": True,
        "valid": result.valid,
        "process": result.process,
        "theory": result.theory,
        "expression": result.expression,
        "color_average": result.color_average,
        "spin_average": result.spin_average,
        "coupling": result.coupling,
        "substitutions": result.substitutions,
        "ms_squared": result.ms_squared,
        "errors": list(result.errors),
        "scientific_scope": result.scientific_scope,
    }
