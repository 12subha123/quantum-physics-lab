from __future__ import annotations

from dataclasses import dataclass
from math import sqrt, sin, cos, pi


EPS = 1e-9


@dataclass(frozen=True)
class FourVector:
    E: float
    px: float
    py: float
    pz: float

    @property
    def spatial_squared(self) -> float:
        return self.px**2 + self.py**2 + self.pz**2

    @property
    def invariant_mass_squared(self) -> float:
        return self.E**2 - self.spatial_squared

    @property
    def invariant_mass(self) -> float:
        value = self.invariant_mass_squared
        return sqrt(max(0.0, value))

    def __add__(self, other: "FourVector") -> "FourVector":
        return FourVector(
            self.E + other.E,
            self.px + other.px,
            self.py + other.py,
            self.pz + other.pz,
        )

    def __sub__(self, other: "FourVector") -> "FourVector":
        return FourVector(
            self.E - other.E,
            self.px - other.px,
            self.py - other.py,
            self.pz - other.pz,
        )

    def scale(self, factor: float) -> "FourVector":
        return FourVector(
            self.E * factor,
            self.px * factor,
            self.py * factor,
            self.pz * factor,
        )

    def as_dict(self) -> dict:
        return {
            "E": self.E,
            "px": self.px,
            "py": self.py,
            "pz": self.pz,
            "mass_squared": self.invariant_mass_squared,
            "mass": self.invariant_mass,
        }


@dataclass(frozen=True)
class ParticleKinematics:
    particle: str
    mass: float
    momentum: FourVector
    role: str


@dataclass(frozen=True)
class KinematicsValidation:
    valid: bool
    energy_error: float
    px_error: float
    py_error: float
    pz_error: float
    on_shell_errors: tuple[str, ...]
    errors: tuple[str, ...]


def _validate_sqrt_s(sqrt_s: float) -> float:
    sqrt_s = float(sqrt_s)

    if sqrt_s <= 0.0:
        raise ValueError("sqrt_s must be positive.")

    return sqrt_s


def _validate_mass(mass: float, name: str) -> float:
    mass = float(mass)

    if mass < 0.0:
        raise ValueError(f"{name} must be non-negative.")

    return mass


def _boost_z(vector: FourVector, beta: float) -> FourVector:
    if abs(beta) >= 1.0:
        raise ValueError("Lorentz boost requires |beta| < 1.")

    gamma = 1.0 / sqrt(1.0 - beta**2)

    return FourVector(
        gamma * (vector.E + beta * vector.pz),
        vector.px,
        vector.py,
        gamma * (vector.pz + beta * vector.E),
    )


def generate_ee_to_mumu_gamma(
    sqrt_s: float = 10.0,
    electron_mass: float = 0.0,
    muon_mass: float = 0.1056583755,
    pair_mass_fraction: float = 0.65,
    decay_theta: float = pi / 3.0,
    decay_phi: float = pi / 4.0,
) -> dict:
    """
    Generate one physically consistent center-of-mass event:

        e- + e+ -> mu- + mu+ + gamma

    Construction:

        P_initial -> gamma + Q
        Q -> mu- + mu+

    Natural units with c = 1.

    The event is not sampled according to the QED matrix element.
    It is a kinematically valid phase-space point.
    """

    sqrt_s = _validate_sqrt_s(sqrt_s)
    electron_mass = _validate_mass(
        electron_mass,
        "electron_mass",
    )
    muon_mass = _validate_mass(
        muon_mass,
        "muon_mass",
    )

    if sqrt_s < 2.0 * electron_mass:
        raise ValueError(
            "sqrt_s is below the e+e- production threshold."
        )

    if sqrt_s < 2.0 * muon_mass:
        raise ValueError(
            "sqrt_s is below the mu+mu- threshold."
        )

    pair_mass_fraction = float(pair_mass_fraction)

    minimum_pair_mass = 2.0 * muon_mass
    maximum_pair_mass = sqrt_s

    if not 0.0 < pair_mass_fraction < 1.0:
        raise ValueError(
            "pair_mass_fraction must be between 0 and 1."
        )

    pair_mass = (
        minimum_pair_mass
        + pair_mass_fraction
        * (maximum_pair_mass - minimum_pair_mass)
    )

    if pair_mass >= sqrt_s:
        pair_mass = sqrt_s * (1.0 - 1e-8)

    s = sqrt_s**2
    q2 = pair_mass**2

    # Initial e-/e+ momenta in the center-of-mass frame.
    initial_energy = sqrt_s / 2.0

    initial_p_squared = (
        initial_energy**2 - electron_mass**2
    )

    if initial_p_squared < -EPS:
        raise ValueError(
            "Initial-state momentum is not real."
        )

    initial_p = sqrt(max(0.0, initial_p_squared))

    electron_in = FourVector(
        initial_energy,
        0.0,
        0.0,
        initial_p,
    )

    positron_in = FourVector(
        initial_energy,
        0.0,
        0.0,
        -initial_p,
    )

    # First stage:
    #
    # P = gamma + Q
    #
    # In the COM frame the photon travels +z and Q travels -z.
    photon_energy = (s - q2) / (2.0 * sqrt_s)

    if photon_energy <= 0.0:
        raise ValueError(
            "Generated photon energy is not positive."
        )

    photon = FourVector(
        photon_energy,
        0.0,
        0.0,
        photon_energy,
    )

    q_energy = (s + q2) / (2.0 * sqrt_s)

    q_momentum = photon_energy

    q = FourVector(
        q_energy,
        0.0,
        0.0,
        -q_momentum,
    )

    # Second stage:
    #
    # Q -> mu- + mu+
    #
    # Work first in the Q rest frame.
    mu_energy_star = pair_mass / 2.0

    mu_momentum_squared_star = (
        mu_energy_star**2 - muon_mass**2
    )

    if mu_momentum_squared_star < -EPS:
        raise ValueError(
            "Muon decay momentum is not real."
        )

    mu_momentum_star = sqrt(
        max(0.0, mu_momentum_squared_star)
    )

    theta = float(decay_theta)
    phi = float(decay_phi)

    px_star = (
        mu_momentum_star
        * sin(theta)
        * cos(phi)
    )

    py_star = (
        mu_momentum_star
        * sin(theta)
        * sin(phi)
    )

    pz_star = (
        mu_momentum_star
        * cos(theta)
    )

    mu_minus_star = FourVector(
        mu_energy_star,
        px_star,
        py_star,
        pz_star,
    )

    mu_plus_star = FourVector(
        mu_energy_star,
        -px_star,
        -py_star,
        -pz_star,
    )

    # Q moves in the -z direction in the COM frame.
    beta_q = q.pz / q.E

    mu_minus = _boost_z(
        mu_minus_star,
        beta_q,
    )

    mu_plus = _boost_z(
        mu_plus_star,
        beta_q,
    )

    particles = (
        ParticleKinematics(
            particle="electron",
            mass=electron_mass,
            momentum=electron_in,
            role="incoming",
        ),
        ParticleKinematics(
            particle="positron",
            mass=electron_mass,
            momentum=positron_in,
            role="incoming",
        ),
        ParticleKinematics(
            particle="muon",
            mass=muon_mass,
            momentum=mu_minus,
            role="outgoing",
        ),
        ParticleKinematics(
            particle="antimuon",
            mass=muon_mass,
            momentum=mu_plus,
            role="outgoing",
        ),
        ParticleKinematics(
            particle="photon",
            mass=0.0,
            momentum=photon,
            role="outgoing",
        ),
    )

    validation = validate_event_kinematics(
        particles
    )

    return {
        "success": True,
        "process": (
            "electron + positron -> "
            "muon + antimuon + photon"
        ),
        "sqrt_s": sqrt_s,
        "pair_invariant_mass": pair_mass,
        "particles": [
            {
                "particle": item.particle,
                "mass": item.mass,
                "role": item.role,
                "momentum": item.momentum.as_dict(),
            }
            for item in particles
        ],
        "validation": {
            "valid": validation.valid,
            "energy_error": validation.energy_error,
            "px_error": validation.px_error,
            "py_error": validation.py_error,
            "pz_error": validation.pz_error,
            "on_shell_errors": list(
                validation.on_shell_errors
            ),
            "errors": list(validation.errors),
        },
        "scientific_scope": (
            "Numerical center-of-mass kinematics for the "
            "tree-level process e- e+ -> mu- mu+ gamma. "
            "The generated point satisfies energy-momentum "
            "conservation and on-shell constraints. "
            "It is a kinematically valid phase-space point, "
            "not a matrix-element-weighted event sample."
        ),
    }


def validate_event_kinematics(
    particles: tuple[ParticleKinematics, ...],
    tolerance: float = 1e-8,
) -> KinematicsValidation:

    errors: list[str] = []
    on_shell_errors: list[str] = []

    incoming = [
        item
        for item in particles
        if item.role == "incoming"
    ]

    outgoing = [
        item
        for item in particles
        if item.role == "outgoing"
    ]

    if not incoming:
        errors.append(
            "No incoming particles were supplied."
        )

    if not outgoing:
        errors.append(
            "No outgoing particles were supplied."
        )

    initial_total = FourVector(0.0, 0.0, 0.0, 0.0)
    final_total = FourVector(0.0, 0.0, 0.0, 0.0)

    for item in incoming:
        initial_total = initial_total + item.momentum

    for item in outgoing:
        final_total = final_total + item.momentum

    delta = initial_total - final_total

    energy_error = abs(delta.E)
    px_error = abs(delta.px)
    py_error = abs(delta.py)
    pz_error = abs(delta.pz)

    if energy_error > tolerance:
        errors.append(
            f"Energy conservation error: {energy_error:.6e}"
        )

    if px_error > tolerance:
        errors.append(
            f"px conservation error: {px_error:.6e}"
        )

    if py_error > tolerance:
        errors.append(
            f"py conservation error: {py_error:.6e}"
        )

    if pz_error > tolerance:
        errors.append(
            f"pz conservation error: {pz_error:.6e}"
        )

    for item in particles:
        actual = item.momentum.invariant_mass_squared
        expected = item.mass**2

        error = abs(actual - expected)

        if error > tolerance:
            on_shell_errors.append(
                f"{item.particle}: "
                f"|p^2-m^2|={error:.6e}"
            )

    errors.extend(on_shell_errors)

    return KinematicsValidation(
        valid=not errors,
        energy_error=energy_error,
        px_error=px_error,
        py_error=py_error,
        pz_error=pz_error,
        on_shell_errors=tuple(on_shell_errors),
        errors=tuple(errors),
    )


def generate_kinematics_summary(
    sqrt_s: float = 10.0,
) -> dict:
    event = generate_ee_to_mumu_gamma(
        sqrt_s=sqrt_s
    )

    return event
