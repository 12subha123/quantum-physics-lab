from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TraceResult:
    valid: bool
    input_expression: str
    simplified_expression: str
    trace_type: str
    errors: tuple[str, ...] = ()


def _normalise_index(value: str) -> str:
    return str(value).strip()


def trace_two_gamma(
    mu: str = "mu",
    nu: str = "nu",
) -> TraceResult:
    mu = _normalise_index(mu)
    nu = _normalise_index(nu)

    return TraceResult(
        valid=True,
        input_expression=f"Tr(gamma^{mu} gamma^{nu})",
        simplified_expression=f"4 g^{{{mu}{nu}}}",
        trace_type="two_gamma",
    )


def trace_four_gamma(
    mu: str = "mu",
    nu: str = "nu",
    rho: str = "rho",
    sigma: str = "sigma",
) -> TraceResult:
    mu = _normalise_index(mu)
    nu = _normalise_index(nu)
    rho = _normalise_index(rho)
    sigma = _normalise_index(sigma)

    expression = (
        f"4("
        f"g^{{{mu}{nu}}}g^{{{rho}{sigma}}}"
        f" - "
        f"g^{{{mu}{rho}}}g^{{{nu}{sigma}}}"
        f" + "
        f"g^{{{mu}{sigma}}}g^{{{nu}{rho}}}"
        f")"
    )

    return TraceResult(
        valid=True,
        input_expression=(
            f"Tr(gamma^{mu} gamma^{nu} "
            f"gamma^{rho} gamma^{sigma})"
        ),
        simplified_expression=expression,
        trace_type="four_gamma",
    )


def trace_slash_gamma_slash_gamma(
    p1: str = "p1",
    mu: str = "mu",
    p2: str = "p2",
    nu: str = "nu",
) -> TraceResult:
    p1 = str(p1).strip()
    p2 = str(p2).strip()
    mu = _normalise_index(mu)
    nu = _normalise_index(nu)

    expression = (
        f"4("
        f"{p1}^{mu} {p2}^{nu}"
        f" + "
        f"{p1}^{nu} {p2}^{mu}"
        f" - "
        f"g^{{{mu}{nu}}}({p1}·{p2})"
        f")"
    )

    return TraceResult(
        valid=True,
        input_expression=(
            f"Tr(slash({p1}) gamma^{mu} "
            f"slash({p2}) gamma^{nu})"
        ),
        simplified_expression=expression,
        trace_type="slash_gamma_slash_gamma",
    )


def trace_gamma5_two_gamma(
    mu: str = "mu",
    nu: str = "nu",
) -> TraceResult:
    mu = _normalise_index(mu)
    nu = _normalise_index(nu)

    return TraceResult(
        valid=True,
        input_expression=(
            f"Tr(gamma5 gamma^{mu} gamma^{nu})"
        ),
        simplified_expression="0",
        trace_type="gamma5_two_gamma",
    )


def trace_odd_gamma_count(count: int) -> TraceResult:
    if count < 0:
        return TraceResult(
            valid=False,
            input_expression="",
            simplified_expression="",
            trace_type="odd_gamma_count",
            errors=("Gamma count must be non-negative.",),
        )

    return TraceResult(
        valid=True,
        input_expression=f"Tr[product of {count} gamma matrices]",
        simplified_expression="0",
        trace_type="odd_gamma_count",
    )


def evaluate_trace(
    trace_type: str,
    **kwargs,
) -> TraceResult:
    trace_type = str(trace_type).strip().lower()

    if trace_type == "two_gamma":
        return trace_two_gamma(
            kwargs.get("mu", "mu"),
            kwargs.get("nu", "nu"),
        )

    if trace_type == "four_gamma":
        return trace_four_gamma(
            kwargs.get("mu", "mu"),
            kwargs.get("nu", "nu"),
            kwargs.get("rho", "rho"),
            kwargs.get("sigma", "sigma"),
        )

    if trace_type == "slash_gamma_slash_gamma":
        return trace_slash_gamma_slash_gamma(
            kwargs.get("p1", "p1"),
            kwargs.get("mu", "mu"),
            kwargs.get("p2", "p2"),
            kwargs.get("nu", "nu"),
        )

    if trace_type == "gamma5_two_gamma":
        return trace_gamma5_two_gamma(
            kwargs.get("mu", "mu"),
            kwargs.get("nu", "nu"),
        )

    if trace_type == "odd_gamma_count":
        return trace_odd_gamma_count(
            int(kwargs.get("count", 1))
        )

    return TraceResult(
        valid=False,
        input_expression="",
        simplified_expression="",
        trace_type=trace_type,
        errors=(f"Unsupported trace type: {trace_type}",),
    )


def dirac_trace_summary():
    results = {
        "two_gamma": trace_two_gamma(),
        "four_gamma": trace_four_gamma(),
        "slash_gamma_slash_gamma": trace_slash_gamma_slash_gamma(),
        "gamma5_two_gamma": trace_gamma5_two_gamma(),
        "odd_gamma": trace_odd_gamma_count(3),
    }

    return {
        "success": True,
        "valid": all(result.valid for result in results.values()),
        "results": {
            name: {
                "valid": result.valid,
                "input_expression": result.input_expression,
                "simplified_expression": result.simplified_expression,
                "trace_type": result.trace_type,
                "errors": list(result.errors),
            }
            for name, result in results.items()
        },
        "scientific_scope": (
            "Symbolic Dirac trace identities for tree-level "
            "relativistic quantum field theory. Supports two-gamma, "
            "four-gamma, slash-gamma-slash-gamma, gamma5 two-gamma, "
            "and odd-gamma traces. This layer performs symbolic "
            "trace reduction only; it does not yet perform complete "
            "noncommutative gamma-string reduction, dimensional "
            "regularization, loop traces, or numerical matrix-element "
            "evaluation."
        ),
    }
