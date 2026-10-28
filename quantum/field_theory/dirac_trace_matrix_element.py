from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class DiracTrace:
    trace_id: str
    gamma_structure: tuple[str, ...]
    expression: str


@dataclass(frozen=True)
class SpinSummedMatrixElement:
    candidate_id: str
    topology: str
    process: str
    theory: str
    traces: tuple[DiracTrace, ...]
    expression: str
    status: str
    reasons: tuple[str, ...]


def dirac_trace(
    trace_id: str,
    gamma_structure: tuple[str, ...],
) -> DiracTrace:

    if not gamma_structure:
        return DiracTrace(
            trace_id=trace_id,
            gamma_structure=(),
            expression="UNRESOLVED_TRACE",
        )

    expression = (
        "Tr["
        + " ".join(gamma_structure)
        + "]"
    )

    return DiracTrace(
        trace_id=trace_id,
        gamma_structure=gamma_structure,
        expression=expression,
    )


def trace_two_gamma(
    trace_id: str,
    mu: str,
    nu: str,
) -> DiracTrace:

    return DiracTrace(
        trace_id=trace_id,
        gamma_structure=(
            f"gamma^{mu}",
            f"gamma^{nu}",
        ),
        expression=(
            f"Tr[gamma^{mu} gamma^{nu}] "
            f"= 4 g^{{{mu}{nu}}}"
        ),
    )


def trace_four_gamma(
    trace_id: str,
    mu: str,
    nu: str,
    rho: str,
    sigma: str,
) -> DiracTrace:

    return DiracTrace(
        trace_id=trace_id,
        gamma_structure=(
            f"gamma^{mu}",
            f"gamma^{nu}",
            f"gamma^{rho}",
            f"gamma^{sigma}",
        ),
        expression=(
            f"Tr[gamma^{mu} gamma^{nu} "
            f"gamma^{rho} gamma^{sigma}] = "
            f"4("
            f"g^{{{mu}{nu}}}g^{{{rho}{sigma}}}"
            f" - "
            f"g^{{{mu}{rho}}}g^{{{nu}{sigma}}}"
            f" + "
            f"g^{{{mu}{sigma}}}g^{{{nu}{rho}}}"
            f")"
        ),
    )


def trace_slash_gamma_slash_gamma(
    trace_id: str,
    p: str,
    mu: str,
    q: str,
    nu: str,
) -> DiracTrace:

    return DiracTrace(
        trace_id=trace_id,
        gamma_structure=(
            f"slash({p})",
            f"gamma^{mu}",
            f"slash({q})",
            f"gamma^{nu}",
        ),
        expression=(
            f"Tr[slash({p}) gamma^{mu} "
            f"slash({q}) gamma^{nu}] = "
            f"4("
            f"{p}^{mu}{q}^{nu}"
            f" + "
            f"{p}^{nu}{q}^{mu}"
            f" - "
            f"(p.q)g^{{{mu}{nu}}}"
            f")"
        ),
    )


def build_spin_summed_matrix_element(
    candidate_id: str,
    topology: str,
    process: str,
    theory: str,
    traces: tuple[DiracTrace, ...],
    amplitude_expression: str,
    status: str = "STRUCTURED",
    reasons: tuple[str, ...] = (),
) -> SpinSummedMatrixElement:

    if status == "FORBIDDEN":
        expression = "NOT_PHYSICALLY_ALLOWED"
    elif not traces:
        expression = (
            f"SpinSum[|M|^2]({amplitude_expression})"
        )
    else:
        expression = (
            f"SpinSum[|M|^2] = "
            + " * ".join(
                trace.expression
                for trace in traces
            )
        )

    return SpinSummedMatrixElement(
        candidate_id=candidate_id,
        topology=topology,
        process=process,
        theory=theory,
        traces=traces,
        expression=expression,
        status=status,
        reasons=reasons,
    )


def spin_summed_matrix_element_dict(
    result: SpinSummedMatrixElement,
) -> dict[str, Any]:

    return asdict(result)


def build_trace_for_vector_current(
    trace_id: str,
    incoming_momentum: str,
    outgoing_momentum: str,
) -> DiracTrace:

    return trace_slash_gamma_slash_gamma(
        trace_id=trace_id,
        p=incoming_momentum,
        mu="mu",
        q=outgoing_momentum,
        nu="nu",
    )
