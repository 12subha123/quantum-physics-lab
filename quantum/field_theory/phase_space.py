from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Iterable


@dataclass(frozen=True)
class PhaseSpaceParticle:
    name: str
    mass: float
    momentum: tuple[float, float, float, float]

    @property
    def energy(self) -> float:
        return self.momentum[0]

    @property
    def spatial_squared(self) -> float:
        return sum(x * x for x in self.momentum[1:])

    @property
    def invariant_mass_squared(self) -> float:
        E, px, py, pz = self.momentum
        return E * E - px * px - py * py - pz * pz

    @property
    def on_shell_residual(self) -> float:
        return self.invariant_mass_squared - self.mass**2


@dataclass(frozen=True)
class PhaseSpacePoint:
    initial: tuple[PhaseSpaceParticle, ...]
    final: tuple[PhaseSpaceParticle, ...]
    total_initial: tuple[float, float, float, float]
    total_final: tuple[float, float, float, float]
    conservation_residual: tuple[float, float, float, float]
    max_conservation_error: float
    max_on_shell_error: float
    valid: bool
    errors: tuple[str, ...] = ()


def _validate_mass(mass: float) -> None:
    if not math.isfinite(mass) or mass < 0.0:
        raise ValueError("Particle masses must be finite and non-negative.")


def _validate_energy(energy: float) -> None:
    if not math.isfinite(energy) or energy <= 0.0:
        raise ValueError("Total COM energy must be finite and positive.")


def _add(
    a: tuple[float, float, float, float],
    b: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    return tuple(x + y for x, y in zip(a, b))


def _subtract(
    a: tuple[float, float, float, float],
    b: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    return tuple(x - y for x, y in zip(a, b))


def _max_abs(
    vector: tuple[float, float, float, float],
) -> float:
    return max(abs(x) for x in vector)


def validate_phase_space(
    initial: Iterable[PhaseSpaceParticle],
    final: Iterable[PhaseSpaceParticle],
    tolerance: float = 1e-8,
) -> PhaseSpacePoint:
    initial = tuple(initial)
    final = tuple(final)

    if not initial:
        raise ValueError("At least one initial particle is required.")

    if not final:
        raise ValueError("At least one final particle is required.")

    total_initial = (0.0, 0.0, 0.0, 0.0)
    total_final = (0.0, 0.0, 0.0, 0.0)

    errors: list[str] = []

    for particle in initial:
        _validate_mass(particle.mass)
        total_initial = _add(total_initial, particle.momentum)

    for particle in final:
        _validate_mass(particle.mass)
        total_final = _add(total_final, particle.momentum)

    residual = _subtract(total_initial, total_final)
    max_conservation_error = _max_abs(residual)

    on_shell_errors = []

    for particle in (*initial, *final):
        error = abs(particle.on_shell_residual)
        on_shell_errors.append(error)

        if error > tolerance:
            errors.append(
                f"Off-shell particle {particle.name}: "
                f"residual={particle.on_shell_residual}"
            )

    if max_conservation_error > tolerance:
        errors.append(
            "Four-momentum conservation failed: "
            f"max residual={max_conservation_error}"
        )

    return PhaseSpacePoint(
        initial=initial,
        final=final,
        total_initial=total_initial,
        total_final=total_final,
        conservation_residual=residual,
        max_conservation_error=max_conservation_error,
        max_on_shell_error=max(on_shell_errors),
        valid=not errors,
        errors=tuple(errors),
    )


def generate_two_body_phase_space(
    sqrt_s: float,
    mass1: float,
    mass2: float,
    name1: str = "particle_1",
    name2: str = "particle_2",
    theta: float = math.pi / 3.0,
    phi: float = 0.0,
) -> PhaseSpacePoint:
    _validate_energy(sqrt_s)
    _validate_mass(mass1)
    _validate_mass(mass2)

    if sqrt_s < mass1 + mass2:
        raise ValueError(
            "COM energy is below the two-body production threshold."
        )

    if not 0.0 <= theta <= math.pi:
        raise ValueError("theta must satisfy 0 <= theta <= pi.")

    if not 0.0 <= phi <= 2.0 * math.pi:
        raise ValueError("phi must satisfy 0 <= phi <= 2*pi.")

    s = sqrt_s**2

    energy1 = (
        s + mass1**2 - mass2**2
    ) / (2.0 * sqrt_s)

    energy2 = (
        s + mass2**2 - mass1**2
    ) / (2.0 * sqrt_s)

    momentum_squared = (
        (s - (mass1 + mass2)**2)
        * (s - (mass1 - mass2)**2)
        / (4.0 * s)
    )

    momentum = math.sqrt(max(momentum_squared, 0.0))

    px = momentum * math.sin(theta) * math.cos(phi)
    py = momentum * math.sin(theta) * math.sin(phi)
    pz = momentum * math.cos(theta)

    p1 = PhaseSpaceParticle(
        name=name1,
        mass=mass1,
        momentum=(energy1, px, py, pz),
    )

    p2 = PhaseSpaceParticle(
        name=name2,
        mass=mass2,
        momentum=(energy2, -px, -py, -pz),
    )

    initial = (
        PhaseSpaceParticle(
            name="initial_1",
            mass=0.0,
            momentum=(sqrt_s / 2.0, 0.0, 0.0, sqrt_s / 2.0),
        ),
        PhaseSpaceParticle(
            name="initial_2",
            mass=0.0,
            momentum=(sqrt_s / 2.0, 0.0, 0.0, -sqrt_s / 2.0),
        ),
    )

    return validate_phase_space(
        initial,
        (p1, p2),
    )


def generate_massless_n_body_phase_space(
    sqrt_s: float,
    particle_names: Iterable[str],
    seed: int | None = 12345,
) -> PhaseSpacePoint:
    _validate_energy(sqrt_s)

    names = tuple(particle_names)

    if len(names) < 2:
        raise ValueError(
            "At least two final particles are required."
        )

    rng = random.Random(seed)
    n = len(names)

    vectors: list[list[float]] = []

    for _ in range(n):
        r1 = max(rng.random(), 1e-15)
        r2 = max(rng.random(), 1e-15)
        r3 = rng.random()
        r4 = rng.random()

        energy = -math.log(r1 * r2)

        cos_theta = 2.0 * r3 - 1.0
        sin_theta = math.sqrt(
            max(0.0, 1.0 - cos_theta**2)
        )
        phi = 2.0 * math.pi * r4

        px = energy * sin_theta * math.cos(phi)
        py = energy * sin_theta * math.sin(phi)
        pz = energy * cos_theta

        vectors.append([energy, px, py, pz])

    total = [0.0, 0.0, 0.0, 0.0]

    for vector in vectors:
        for i in range(4):
            total[i] += vector[i]

    spatial = total[1:]

    boost_x = spatial[0] / total[0]
    boost_y = spatial[1] / total[0]
    boost_z = spatial[2] / total[0]

    beta2 = (
        boost_x**2
        + boost_y**2
        + boost_z**2
    )

    if beta2 >= 1.0:
        raise RuntimeError(
            "Generated configuration has an invalid COM boost."
        )

    gamma = 1.0 / math.sqrt(1.0 - beta2)

    boosted: list[tuple[float, float, float, float]] = []

    for E, px, py, pz in vectors:
        bp = (
            boost_x * px
            + boost_y * py
            + boost_z * pz
        )

        factor = (
            (gamma - 1.0) * bp / beta2
            if beta2 > 1e-15
            else 0.0
        )

        new_px = px + factor * boost_x - gamma * boost_x * E
        new_py = py + factor * boost_y - gamma * boost_y * E
        new_pz = pz + factor * boost_z - gamma * boost_z * E
        new_E = gamma * (E - bp)

        boosted.append(
            (new_E, new_px, new_py, new_pz)
        )

    total_energy = sum(v[0] for v in boosted)

    scale = sqrt_s / total_energy

    final = tuple(
        PhaseSpaceParticle(
            name=name,
            mass=0.0,
            momentum=(
                vector[0] * scale,
                vector[1] * scale,
                vector[2] * scale,
                vector[3] * scale,
            ),
        )
        for name, vector in zip(names, boosted)
    )

    initial = (
        PhaseSpaceParticle(
            name="initial_1",
            mass=0.0,
            momentum=(
                sqrt_s / 2.0,
                0.0,
                0.0,
                sqrt_s / 2.0,
            ),
        ),
        PhaseSpaceParticle(
            name="initial_2",
            mass=0.0,
            momentum=(
                sqrt_s / 2.0,
                0.0,
                0.0,
                -sqrt_s / 2.0,
            ),
        ),
    )

    return validate_phase_space(
        initial,
        final,
    )


def phase_space_summary(
    point: PhaseSpacePoint,
) -> dict:
    return {
        "success": True,
        "valid": point.valid,
        "initial_count": len(point.initial),
        "final_count": len(point.final),
        "total_initial": point.total_initial,
        "total_final": point.total_final,
        "conservation_residual": point.conservation_residual,
        "max_conservation_error": point.max_conservation_error,
        "max_on_shell_error": point.max_on_shell_error,
        "initial_particles": [
            {
                "name": p.name,
                "mass": p.mass,
                "momentum": p.momentum,
            }
            for p in point.initial
        ],
        "final_particles": [
            {
                "name": p.name,
                "mass": p.mass,
                "momentum": p.momentum,
                "invariant_mass_squared": p.invariant_mass_squared,
                "on_shell_residual": p.on_shell_residual,
            }
            for p in point.final
        ],
        "errors": list(point.errors),
        "scientific_scope": (
            "Lorentz-invariant phase-space foundation for arbitrary "
            "initial and final multiplicities. Exact massive two-body "
            "kinematics and massless N-body COM phase-space generation "
            "are implemented. Matrix-element weighting, phase-space "
            "integration, massive N-body recursive generation, and "
            "cross-section normalization are separate later layers."
        ),
    }
