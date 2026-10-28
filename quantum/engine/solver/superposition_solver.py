import math
import random
from dataclasses import dataclass


@dataclass
class SuperpositionResult:
    alpha_real: float
    alpha_imag: float
    beta_real: float
    beta_imag: float

    alpha_magnitude: float
    beta_magnitude: float

    probability_zero: float
    probability_one: float

    normalized: bool


def calculate_superposition(
    alpha_real: float = 1 / math.sqrt(2),
    alpha_imag: float = 0.0,
    beta_real: float = 1 / math.sqrt(2),
    beta_imag: float = 0.0,
) -> SuperpositionResult:

    alpha_magnitude_squared = (
        alpha_real**2 + alpha_imag**2
    )

    beta_magnitude_squared = (
        beta_real**2 + beta_imag**2
    )

    total_probability = (
        alpha_magnitude_squared
        + beta_magnitude_squared
    )

    if total_probability <= 0:
        raise ValueError(
            "The quantum state cannot have zero total probability."
        )

    tolerance = 1e-9

    normalized = abs(
        total_probability - 1.0
    ) <= tolerance

    if not normalized:
        normalization_factor = math.sqrt(
            total_probability
        )

        alpha_real /= normalization_factor
        alpha_imag /= normalization_factor
        beta_real /= normalization_factor
        beta_imag /= normalization_factor

        alpha_magnitude_squared = (
            alpha_real**2 + alpha_imag**2
        )

        beta_magnitude_squared = (
            beta_real**2 + beta_imag**2
        )

        normalized = True

    return SuperpositionResult(
        alpha_real=alpha_real,
        alpha_imag=alpha_imag,
        beta_real=beta_real,
        beta_imag=beta_imag,
        alpha_magnitude=math.sqrt(
            alpha_magnitude_squared
        ),
        beta_magnitude=math.sqrt(
            beta_magnitude_squared
        ),
        probability_zero=alpha_magnitude_squared,
        probability_one=beta_magnitude_squared,
        normalized=normalized,
    )


def simulate_measurement(
    probability_zero: float,
    shots: int = 1000,
) -> dict:

    if shots < 1:
        raise ValueError(
            "Number of measurement shots must be at least 1."
        )

    if not 0.0 <= probability_zero <= 1.0:
        raise ValueError(
            "Probability of measuring |0> must be between 0 and 1."
        )

    probability_one = 1.0 - probability_zero

    outcomes = random.choices(
        population=[0, 1],
        weights=[
            probability_zero,
            probability_one,
        ],
        k=shots,
    )

    zero_count = outcomes.count(0)
    one_count = outcomes.count(1)

    return {
        "shots": shots,
        "zero_count": zero_count,
        "one_count": one_count,
        "observed_probability_zero": (
            zero_count / shots
        ),
        "observed_probability_one": (
            one_count / shots
        ),
        "theoretical_probability_zero": (
            probability_zero
        ),
        "theoretical_probability_one": (
            probability_one
        ),
    }


if __name__ == "__main__":
    result = calculate_superposition()

    print("Quantum Superposition")
    print("=====================")
    print()

    print("State:")
    print(
        f"  alpha = "
        f"{result.alpha_real:.6f} "
        f"+ {result.alpha_imag:.6f}i"
    )

    print(
        f"  beta  = "
        f"{result.beta_real:.6f} "
        f"+ {result.beta_imag:.6f}i"
    )

    print()

    print("Theoretical probabilities:")
    print(
        f"  P(0) = "
        f"{result.probability_zero:.6f}"
    )

    print(
        f"  P(1) = "
        f"{result.probability_one:.6f}"
    )

    print()

    measurement = simulate_measurement(
        probability_zero=result.probability_zero,
        shots=1000,
    )

    print("Random measurement simulation:")
    print(
        f"  |0> results: "
        f"{measurement['zero_count']}"
    )

    print(
        f"  |1> results: "
        f"{measurement['one_count']}"
    )

    print()

    print("Observed probabilities:")
    print(
        f"  P(0) observed = "
        f"{measurement['observed_probability_zero']:.6f}"
    )

    print(
        f"  P(1) observed = "
        f"{measurement['observed_probability_one']:.6f}"
    )
