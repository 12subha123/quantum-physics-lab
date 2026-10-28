from dataclasses import dataclass


@dataclass(frozen=True)
class ColorAlgebraResult:
    valid: bool
    expression: str
    value: float | None
    n_c: int
    errors: tuple[str, ...] = ()


def _validate_n_c(n_c: int) -> None:
    if not isinstance(n_c, int):
        raise TypeError("n_c must be an integer.")

    if n_c < 2:
        raise ValueError("n_c must be at least 2.")


def fundamental_casimir(n_c: int = 3) -> ColorAlgebraResult:
    _validate_n_c(n_c)

    value = (n_c**2 - 1) / (2.0 * n_c)

    return ColorAlgebraResult(
        valid=True,
        expression="C_F = (N_c^2 - 1)/(2 N_c)",
        value=value,
        n_c=n_c,
    )


def generator_trace_normalization(
    n_c: int = 3,
) -> ColorAlgebraResult:
    _validate_n_c(n_c)

    return ColorAlgebraResult(
        valid=True,
        expression="Tr(T^a T^b) = (1/2) delta^(ab)",
        value=0.5,
        n_c=n_c,
    )


def color_algebra_summary(n_c: int = 3) -> dict:
    casimir = fundamental_casimir(n_c)
    normalization = generator_trace_normalization(n_c)

    return {
        "success": True,
        "valid": casimir.valid and normalization.valid,
        "n_c": n_c,
        "fundamental_casimir": {
            "expression": casimir.expression,
            "value": casimir.value,
        },
        "generator_trace_normalization": {
            "expression": normalization.expression,
            "value": normalization.value,
        },
        "errors": list(
            casimir.errors + normalization.errors
        ),
        "scientific_scope": (
            "Educational SU(N_c) color-algebra foundation for "
            "tree-level QCD calculations. This layer does not "
            "yet perform full color-index contractions."
        ),
    }
