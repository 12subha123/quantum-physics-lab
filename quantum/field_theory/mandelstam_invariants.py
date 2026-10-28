from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class FourMomentum:
    name: str
    energy: float | None
    px: float | None
    py: float | None
    pz: float | None
    mass: float | None = None


@dataclass(frozen=True)
class MandelstamInvariants:
    s: float | None
    t: float | None
    u: float | None
    relation: str
    status: str
    reasons: tuple[str, ...]


def _dot(
    a: FourMomentum,
    b: FourMomentum,
) -> float | None:

    values = (
        a.energy,
        a.px,
        a.py,
        a.pz,
        b.energy,
        b.px,
        b.py,
        b.pz,
    )

    if any(value is None for value in values):
        return None

    return (
        a.energy * b.energy
        - a.px * b.px
        - a.py * b.py
        - a.pz * b.pz
    )


def _sum(
    a: FourMomentum,
    b: FourMomentum,
    name: str,
) -> FourMomentum:

    energy = (
        None
        if a.energy is None or b.energy is None
        else a.energy + b.energy
    )

    px = (
        None
        if a.px is None or b.px is None
        else a.px + b.px
    )

    py = (
        None
        if a.py is None or b.py is None
        else a.py + b.py
    )

    pz = (
        None
        if a.pz is None or b.pz is None
        else a.pz + b.pz
    )

    return FourMomentum(
        name=name,
        energy=energy,
        px=px,
        py=py,
        pz=pz,
    )


def _difference(
    a: FourMomentum,
    b: FourMomentum,
    name: str,
) -> FourMomentum:

    energy = (
        None
        if a.energy is None or b.energy is None
        else a.energy - b.energy
    )

    px = (
        None
        if a.px is None or b.px is None
        else a.px - b.px
    )

    py = (
        None
        if a.py is None or b.py is None
        else a.py - b.py
    )

    pz = (
        None
        if a.pz is None or b.pz is None
        else a.pz - b.pz
    )

    return FourMomentum(
        name=name,
        energy=energy,
        px=px,
        py=py,
        pz=pz,
    )


def invariant_square(
    momentum: FourMomentum,
) -> float | None:

    return _dot(momentum, momentum)


def compute_mandelstam(
    p1: FourMomentum,
    p2: FourMomentum,
    p3: FourMomentum,
    p4: FourMomentum,
) -> MandelstamInvariants:

    reasons = []

    s_momentum = _sum(p1, p2, "p1+p2")
    t_momentum = _difference(p1, p3, "p1-p3")
    u_momentum = _difference(p1, p4, "p1-p4")

    s = invariant_square(s_momentum)
    t = invariant_square(t_momentum)
    u = invariant_square(u_momentum)

    if s is None or t is None or u is None:
        reasons.append(
            "Complete four-momentum information is required "
            "to evaluate numerical Mandelstam invariants."
        )

        return MandelstamInvariants(
            s=s,
            t=t,
            u=u,
            relation="s + t + u = sum(m_i^2)",
            status="UNDECIDABLE",
            reasons=tuple(reasons),
        )

    return MandelstamInvariants(
        s=s,
        t=t,
        u=u,
        relation="s + t + u = m1^2 + m2^2 + m3^2 + m4^2",
        status="CALCULATED",
        reasons=(),
    )


def mandelstam_dict(
    invariants: MandelstamInvariants,
) -> dict[str, Any]:

    return asdict(invariants)


def symbolic_mandelstam() -> dict[str, str]:

    return {
        "s": "(p1 + p2)^2",
        "t": "(p1 - p3)^2",
        "u": "(p1 - p4)^2",
        "identity": (
            "s + t + u = "
            "m1^2 + m2^2 + m3^2 + m4^2"
        ),
    }
