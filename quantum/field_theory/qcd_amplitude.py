from dataclasses import dataclass


@dataclass(frozen=True)
class QCDAmplitudeTerm:
    channel: str
    interaction: str
    color_factor: str
    kinematic_factor: str
    expression: str


@dataclass(frozen=True)
class QCDAmplitudeResult:
    valid: bool
    process: str
    theory: str
    terms: tuple[QCDAmplitudeTerm, ...]
    total_expression: str
    errors: tuple[str, ...] = ()
    scientific_scope: str = ""


def _validate_channel(channel: str) -> None:
    if channel not in {"s", "t", "u"}:
        raise ValueError(
            f"Unsupported QCD channel: {channel}"
        )


def _build_term(channel: str) -> QCDAmplitudeTerm:
    _validate_channel(channel)

    if channel == "s":
        return QCDAmplitudeTerm(
            channel="s",
            interaction="q-qbar-gluon + three-gluon",
            color_factor="T^a_{ij} f^{abc}",
            kinematic_factor="1/s",
            expression=(
                "M_s = g_s^2 "
                "[T^a_{ij} f^{abc}] "
                "[J_mu V^{mu nu rho}] "
                "epsilon*_nu(k1) epsilon*_rho(k2) / s"
            ),
        )

    if channel == "t":
        return QCDAmplitudeTerm(
            channel="t",
            interaction="q-qbar-gluon + q-qbar-gluon",
            color_factor="(T^b T^c)_{ij}",
            kinematic_factor="1/t",
            expression=(
                "M_t = g_s^2 "
                "[(T^b T^c)_{ij}] "
                "[qbar(p2) gamma^nu "
                "(slash(p1)-slash(k1)+m_q) "
                "gamma^mu q(p1)] "
                "epsilon*_mu(k1) epsilon*_nu(k2) / t"
            ),
        )

    return QCDAmplitudeTerm(
        channel="u",
        interaction="q-qbar-gluon + q-qbar-gluon",
        color_factor="(T^c T^b)_{ij}",
        kinematic_factor="1/u",
        expression=(
            "M_u = g_s^2 "
            "[(T^c T^b)_{ij}] "
            "[qbar(p2) gamma^mu "
            "(slash(p1)-slash(k2)+m_q) "
            "gamma^nu q(p1)] "
            "epsilon*_mu(k1) epsilon*_nu(k2) / u"
        ),
    )


def qcd_qqbar_to_gg_amplitude(
    channels: tuple[str, ...] = ("s", "t", "u"),
) -> QCDAmplitudeResult:
    if not channels:
        return QCDAmplitudeResult(
            valid=False,
            process="q + anti-q -> g + g",
            theory="QCD",
            terms=(),
            total_expression="",
            errors=("At least one channel is required.",),
            scientific_scope=(
                "Tree-level QCD symbolic amplitude construction."
            ),
        )

    unique_channels = tuple(dict.fromkeys(channels))

    try:
        terms = tuple(
            _build_term(channel)
            for channel in unique_channels
        )
    except ValueError as exc:
        return QCDAmplitudeResult(
            valid=False,
            process="q + anti-q -> g + g",
            theory="QCD",
            terms=(),
            total_expression="",
            errors=(str(exc),),
            scientific_scope=(
                "Tree-level QCD symbolic amplitude construction."
            ),
        )

    total = " + ".join(
        term.expression
        for term in terms
    )

    return QCDAmplitudeResult(
        valid=True,
        process="q + anti-q -> g + g",
        theory="QCD",
        terms=terms,
        total_expression=total,
        errors=(),
        scientific_scope=(
            "Tree-level QCD amplitude structure for "
            "q-qbar -> g-g. Includes s-, t-, and u-channel "
            "diagram structures and explicit color factors. "
            "This is not yet a numerical spin/color-summed "
            "matrix-element evaluator."
        ),
    )


def qcd_amplitude_summary(
    channels: tuple[str, ...] = ("s", "t", "u"),
) -> dict:
    result = qcd_qqbar_to_gg_amplitude(channels)

    return {
        "success": True,
        "valid": result.valid,
        "process": result.process,
        "theory": result.theory,
        "channel_count": len(result.terms),
        "channels": [
            term.channel
            for term in result.terms
        ],
        "terms": [
            {
                "channel": term.channel,
                "interaction": term.interaction,
                "color_factor": term.color_factor,
                "kinematic_factor": term.kinematic_factor,
                "expression": term.expression,
            }
            for term in result.terms
        ],
        "total_expression": result.total_expression,
        "errors": list(result.errors),
        "scientific_scope": result.scientific_scope,
    }
