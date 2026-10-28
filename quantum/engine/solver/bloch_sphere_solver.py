import math
import cmath
from dataclasses import dataclass


@dataclass
class BlochSphereResult:
    theta_degrees: float
    phi_degrees: float

    theta_radians: float
    phi_radians: float

    alpha_real: float
    alpha_imag: float

    beta_real: float
    beta_imag: float

    bloch_x: float
    bloch_y: float
    bloch_z: float

    probability_zero: float
    probability_one: float


def calculate_bloch_state(
    theta_degrees: float,
    phi_degrees: float,
) -> BlochSphereResult:

    if not 0.0 <= theta_degrees <= 180.0:
        raise ValueError(
            "Theta must be between 0 and 180 degrees."
        )

    if not 0.0 <= phi_degrees <= 360.0:
        raise ValueError(
            "Phi must be between 0 and 360 degrees."
        )

    theta = math.radians(theta_degrees)
    phi = math.radians(phi_degrees)

    alpha = math.cos(theta / 2)

    beta = (
        cmath.exp(1j * phi)
        * math.sin(theta / 2)
    )

    bloch_x = (
        math.sin(theta)
        * math.cos(phi)
    )

    bloch_y = (
        math.sin(theta)
        * math.sin(phi)
    )

    bloch_z = math.cos(theta)

    probability_zero = abs(alpha) ** 2
    probability_one = abs(beta) ** 2

    return BlochSphereResult(
        theta_degrees=theta_degrees,
        phi_degrees=phi_degrees,
        theta_radians=theta,
        phi_radians=phi,
        alpha_real=float(alpha.real),
        alpha_imag=float(alpha.imag),
        beta_real=float(beta.real),
        beta_imag=float(beta.imag),
        bloch_x=float(bloch_x),
        bloch_y=float(bloch_y),
        bloch_z=float(bloch_z),
        probability_zero=float(probability_zero),
        probability_one=float(probability_one),
    )


if __name__ == "__main__":
    result = calculate_bloch_state(
        theta_degrees=90.0,
        phi_degrees=0.0,
    )

    print("Spin-1/2 Bloch Sphere Solver")
    print("============================")
    print()

    print(
        f"Theta: {result.theta_degrees:.2f} degrees"
    )

    print(
        f"Phi:   {result.phi_degrees:.2f} degrees"
    )

    print()

    print("Quantum state:")

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

    print("Bloch coordinates:")

    print(
        f"  x = {result.bloch_x:.6f}"
    )

    print(
        f"  y = {result.bloch_y:.6f}"
    )

    print(
        f"  z = {result.bloch_z:.6f}"
    )

    print()

    print("Measurement probabilities:")

    print(
        f"  P(0) = "
        f"{result.probability_zero:.6f}"
    )

    print(
        f"  P(1) = "
        f"{result.probability_one:.6f}"
    )
