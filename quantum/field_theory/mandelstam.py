from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class FourMomentum:
    label: str
    E: float
    px: float
    py: float
    pz: float
    mass: float = 0.0

    @property
    def vector(self) -> tuple[float, float, float, float]:
        return (self.E, self.px, self.py, self.pz)

    @property
    def squared(self) -> float:
        return (
            self.E**2
            - self.px**2
            - self.py**2
            - self.pz**2
        )

    @property
    def on_shell_error(self) -> float:
        return abs(self.squared - self.mass**2)


@dataclass(frozen=True)
class MandelstamInvariants:
    s: float
    t: float
    u: float
    s_symbolic: str
    t_symbolic: str
    u_symbolic: str
    identity_residual: float
    expected_identity: float
    valid: bool
    errors: tuple[str, ...] = ()


def _dot(
    a: FourMomentum,
    b: FourMomentum,
) -> float:
    return (
        a.E * b.E
        - a.px * b.px
        - a.py * b.py
        - a.pz * b.pz
    )


def lorentz_scalar_product(
    a: FourMomentum,
    b: FourMomentum,
) -> float:
    return _dot(a, b)


def _sum_momentum(
    a: FourMomentum,
    b: FourMomentum,
) -> FourMomentum:
    return FourMomentum(
        label=f"({a.label}+{b.label})",
        E=a.E + b.E,
        px=a.px + b.px,
        py=a.py + b.py,
        pz=a.pz + b.pz,
        mass=0.0,
    )


def _difference_momentum(
    a: FourMomentum,
    b: FourMomentum,
) -> FourMomentum:
    return FourMomentum(
        label=f"({a.label}-{b.label})",
        E=a.E - b.E,
        px=a.px - b.px,
        py=a.py - b.py,
        pz=a.pz - b.pz,
        mass=0.0,
    )


def compute_mandelstam(
    p1: FourMomentum,
    p2: FourMomentum,
    p3: FourMomentum,
    p4: FourMomentum,
    tolerance: float = 1e-8,
) -> MandelstamInvariants:
    errors: list[str] = []

    momenta = (p1, p2, p3, p4)

    for momentum in momenta:
        if not all(
            value == value
            and abs(value) != float("inf")
            for value in momentum.vector
        ):
            errors.append(
                f"Non-finite four-momentum: {momentum.label}"
            )

        if momentum.on_shell_error > tolerance:
            errors.append(
                f"Off-shell momentum: {momentum.label} "
                f"(error={momentum.on_shell_error})"
            )

    p12 = _sum_momentum(p1, p2)
    p13 = _difference_momentum(p1, p3)
    p14 = _difference_momentum(p1, p4)

    s = p12.squared
    t = p13.squared
    u = p14.squared

    expected_identity = (
        p1.mass**2
        + p2.mass**2
        + p3.mass**2
        + p4.mass**2
    )

    identity_residual = (
        s + t + u - expected_identity
    )

    if abs(identity_residual) > tolerance:
        errors.append(
            "Mandelstam identity violation: "
            f"s+t+u={s+t+u}, "
            f"expected={expected_identity}"
        )

    return MandelstamInvariants(
        s=s,
        t=t,
        u=u,
        s_symbolic="s = (p1 + p2)^2",
        t_symbolic="t = (p1 - p3)^2",
        u_symbolic="u = (p1 - p4)^2",
        identity_residual=identity_residual,
        expected_identity=expected_identity,
        valid=not errors,
        errors=tuple(errors),
    )


def build_mandelstam_substitution(
    invariants: MandelstamInvariants,
) -> dict[str, float]:
    return {
        "s": invariants.s,
        "t": invariants.t,
        "u": invariants.u,
    }


def scalar_product_from_mandelstam(
    pair: str,
    invariants: MandelstamInvariants,
    masses: Mapping[str, float] | None = None,
) -> float:
    pair = pair.replace(" ", "").lower()

    masses = masses or {}

    m1 = masses.get("p1", 0.0)
    m2 = masses.get("p2", 0.0)
    m3 = masses.get("p3", 0.0)
    m4 = masses.get("p4", 0.0)

    lookup = {
        "p1.p2": (
            invariants.s - m1**2 - m2**2
        ) / 2.0,
        "p1.p3": (
            m1**2 + m3**2 - invariants.t
        ) / 2.0,
        "p1.p4": (
            m1**2 + m4**2 - invariants.u
        ) / 2.0,
        "p2.p3": (
            m2**2 + m3**2 - invariants.u
        ) / 2.0,
        "p2.p4": (
            m2**2 + m4**2 - invariants.t
        ) / 2.0,
        "p3.p4": (
            invariants.s - m3**2 - m4**2
        ) / 2.0,
    }

    if pair not in lookup:
        raise ValueError(
            f"Unsupported momentum pair: {pair}"
        )

    return lookup[pair]


def mandelstam_summary(
    p1: FourMomentum,
    p2: FourMomentum,
    p3: FourMomentum,
    p4: FourMomentum,
) -> dict:
    result = compute_mandelstam(
        p1,
        p2,
        p3,
        p4,
    )

    return {
        "success": True,
        "valid": result.valid,
        "invariants": {
            "s": result.s,
            "t": result.t,
            "u": result.u,
        },
        "symbolic_definitions": {
            "s": result.s_symbolic,
            "t": result.t_symbolic,
            "u": result.u_symbolic,
        },
        "identity": {
            "s_plus_t_plus_u": (
                result.s + result.t + result.u
            ),
            "expected": result.expected_identity,
            "residual": result.identity_residual,
        },
        "errors": list(result.errors),
        "scientific_scope": (
            "Lorentz-invariant four-momentum products and "
            "Mandelstam variables for 2-to-2 relativistic "
            "scattering. Supports arbitrary external masses "
            "and exact invariant identities. This layer does "
            "not yet perform phase-space integration, matrix-"
            "element evaluation, or cross-section calculations."
        ),
    }
