from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class LorentzIndex:
    name: str
    position: str = "up"

    def __post_init__(self):
        if self.position not in {"up", "down"}:
            raise ValueError("Lorentz index position must be 'up' or 'down'.")

    def symbol(self) -> str:
        return f"{self.name}^{self.position}"


@dataclass(frozen=True)
class TensorFactor:
    name: str
    indices: tuple[LorentzIndex, ...] = ()
    coefficient: str = "1"

    def expression(self) -> str:
        index_text = "".join(
            f"^{{{index.name}}}" if index.position == "up"
            else f"_{{{index.name}}}"
            for index in self.indices
        )

        if self.coefficient == "1":
            return f"{self.name}{index_text}"

        return f"({self.coefficient}) {self.name}{index_text}"


@dataclass(frozen=True)
class Contraction:
    index_name: str
    upper_factor: str
    lower_factor: str


@dataclass(frozen=True)
class LorentzExpression:
    factors: tuple[TensorFactor, ...]
    contractions: tuple[Contraction, ...]
    expression: str
    valid: bool
    errors: tuple[str, ...]


def _index_counts(
    factors: Iterable[TensorFactor],
) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}

    for factor in factors:
        for index in factor.indices:
            if index.name not in counts:
                counts[index.name] = {"up": 0, "down": 0}

            counts[index.name][index.position] += 1

    return counts


def find_contractions(
    factors: Iterable[TensorFactor],
) -> tuple[Contraction, ...]:
    factors = tuple(factors)
    contractions: list[Contraction] = []

    for index_name, counts in _index_counts(factors).items():
        if counts["up"] == 1 and counts["down"] == 1:
            upper = next(
                factor.name
                for factor in factors
                if any(
                    index.name == index_name and index.position == "up"
                    for index in factor.indices
                )
            )

            lower = next(
                factor.name
                for factor in factors
                if any(
                    index.name == index_name and index.position == "down"
                    for index in factor.indices
                )
            )

            contractions.append(
                Contraction(
                    index_name=index_name,
                    upper_factor=upper,
                    lower_factor=lower,
                )
            )

    return tuple(contractions)


def validate_lorentz_indices(
    factors: Iterable[TensorFactor],
) -> tuple[bool, tuple[str, ...]]:
    factors = tuple(factors)
    errors: list[str] = []

    for index_name, counts in _index_counts(factors).items():
        total = counts["up"] + counts["down"]

        if total > 2:
            errors.append(
                f"Index '{index_name}' appears {total} times; "
                "a simple pairwise contraction is required."
            )

        if total == 2 and (
            counts["up"] != 1 or counts["down"] != 1
        ):
            errors.append(
                f"Index '{index_name}' does not have one upper "
                "and one lower occurrence."
            )

    return not errors, tuple(errors)


def build_lorentz_expression(
    factors: Iterable[TensorFactor],
) -> LorentzExpression:
    factors = tuple(factors)

    if not factors:
        return LorentzExpression(
            factors=(),
            contractions=(),
            expression="0",
            valid=False,
            errors=("No tensor factors supplied.",),
        )

    valid, errors = validate_lorentz_indices(factors)
    contractions = find_contractions(factors)

    expression = " ".join(
        factor.expression()
        for factor in factors
    )

    if contractions:
        contraction_text = ", ".join(
            f"{item.index_name}: "
            f"{item.upper_factor} ↔ {item.lower_factor}"
            for item in contractions
        )

        expression += f"  [contractions: {contraction_text}]"

    return LorentzExpression(
        factors=factors,
        contractions=contractions,
        expression=expression,
        valid=valid,
        errors=errors,
    )


def qed_photon_exchange_structure() -> LorentzExpression:
    """
    Educational symbolic structure for a photon-exchange amplitude.

    This represents:

        gamma^mu g_mu,nu gamma^nu

    without evaluating the gamma-matrix product.
    """

    factors = (
        TensorFactor(
            name="gamma",
            indices=(LorentzIndex("mu", "up"),),
        ),
        TensorFactor(
            name="g",
            indices=(
                LorentzIndex("mu", "down"),
                LorentzIndex("nu", "down"),
            ),
        ),
        TensorFactor(
            name="gamma",
            indices=(LorentzIndex("nu", "up"),),
        ),
    )

    return build_lorentz_expression(factors)


def lorentz_algebra_summary(
    factors: Iterable[TensorFactor],
):
    result = build_lorentz_expression(factors)

    return {
        "success": True,
        "valid": result.valid,
        "factor_count": len(result.factors),
        "factors": [
            {
                "name": factor.name,
                "indices": [
                    {
                        "name": index.name,
                        "position": index.position,
                    }
                    for index in factor.indices
                ],
                "coefficient": factor.coefficient,
                "expression": factor.expression(),
            }
            for factor in result.factors
        ],
        "contractions": [
            {
                "index": contraction.index_name,
                "upper_factor": contraction.upper_factor,
                "lower_factor": contraction.lower_factor,
            }
            for contraction in result.contractions
        ],
        "expression": result.expression,
        "errors": list(result.errors),
        "scientific_scope": (
            "Symbolic Lorentz-index bookkeeping and pairwise contraction "
            "detection for tree-level amplitudes. This layer does not "
            "yet evaluate gamma-matrix identities, spinor products, "
            "polarization sums, metric signatures, color algebra, or "
            "numerical matrix elements."
        ),
    }
