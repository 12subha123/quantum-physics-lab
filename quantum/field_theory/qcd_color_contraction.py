from dataclasses import dataclass


@dataclass(frozen=True)
class ColorContraction:
    expression: str
    value: float | None
    valid: bool
    errors: tuple[str, ...] = ()


def _validate_n_c(n_c: int) -> None:
    if not isinstance(n_c, int):
        raise TypeError("n_c must be an integer.")

    if n_c < 2:
        raise ValueError("n_c must be at least 2.")


def delta_contraction(
    n_c: int = 3,
) -> ColorContraction:
    _validate_n_c(n_c)

    return ColorContraction(
        expression="delta^(a a) = N_c^2 - 1",
        value=float(n_c**2 - 1),
        valid=True,
    )


def fundamental_trace_squared(
    n_c: int = 3,
) -> ColorContraction:
    _validate_n_c(n_c)

    value = (n_c**2 - 1) / 2.0

    return ColorContraction(
        expression="sum_a Tr(T^a T^a) = C_F N_c",
        value=value,
        valid=True,
    )


def color_generator_contraction(
    n_c: int = 3,
) -> ColorContraction:
    _validate_n_c(n_c)

    value = (n_c**2 - 1) / (2.0 * n_c)

    return ColorContraction(
        expression="sum_a T^a T^a = C_F I",
        value=value,
        valid=True,
    )


def color_contraction_summary(
    n_c: int = 3,
) -> dict:
    delta = delta_contraction(n_c)
    trace = fundamental_trace_squared(n_c)
    generator = color_generator_contraction(n_c)

    errors = (
        delta.errors
        + trace.errors
        + generator.errors
    )

    return {
        "success": True,
        "valid": (
            delta.valid
            and trace.valid
            and generator.valid
        ),
        "n_c": n_c,
        "contractions": [
            {
                "expression": delta.expression,
                "value": delta.value,
            },
            {
                "expression": trace.expression,
                "value": trace.value,
            },
            {
                "expression": generator.expression,
                "value": generator.value,
            },
        ],
        "errors": list(errors),
        "scientific_scope": (
            "Educational SU(N_c) contraction identities for "
            "tree-level QCD. This layer evaluates selected "
            "fundamental color contractions but does not yet "
            "perform arbitrary indexed tensor reduction."
        ),
    }
