from quantum.field_theory.particle_database import (
    INTERACTIONS,
    PARTICLES,
    Interaction,
    Particle,
    get_particle,
    list_interactions,
    list_particles,
    particle_summary,
)


def _is_charged_fermion(particle: Particle) -> bool:
    return (
        particle.category in {"lepton", "quark"}
        and particle.electric_charge != 0
    )


def _is_quark(particle: Particle) -> bool:
    return particle.category == "quark"


def _is_gluon(particle: Particle) -> bool:
    return particle.name.lower() == "gluon"


def _is_fermion(particle: Particle) -> bool:
    return particle.spin == 0.5


def find_allowed_interactions(
    initial_particles: list[str],
    final_particles: list[str],
) -> list[dict]:
    if len(initial_particles) != 2:
        raise ValueError("Exactly two initial particles are currently required.")

    if len(final_particles) != 2:
        raise ValueError("Exactly two final particles are currently required.")

    initial = [get_particle(name) for name in initial_particles]
    final = [get_particle(name) for name in final_particles]

    total_initial_charge = sum(
        particle.electric_charge for particle in initial
    )
    total_final_charge = sum(
        particle.electric_charge for particle in final
    )

    charge_conserved = abs(
        total_initial_charge - total_final_charge
    ) < 1e-12

    candidates = []

    if all(_is_charged_fermion(p) for p in initial + final):
        if charge_conserved:
            candidates.append({
                "interaction": "QED fermion-photon exchange",
                "theory": "QED",
                "mediators": ["photon"],
                "topologies": ["s-channel", "t-channel"],
                "status": "candidate",
            })

    if all(_is_quark(p) for p in initial + final):
        if charge_conserved:
            candidates.append({
                "interaction": "QCD quark-gluon interaction",
                "theory": "QCD",
                "mediators": ["gluon"],
                "topologies": ["s-channel", "t-channel", "u-channel"],
                "status": "candidate",
            })

    if (
        any(_is_gluon(p) for p in initial + final)
        and any(_is_quark(p) for p in initial + final)
    ):
        candidates.append({
            "interaction": "QCD quark-gluon process",
            "theory": "QCD",
            "mediators": ["gluon"],
            "topologies": ["s-channel", "t-channel", "u-channel"],
            "status": "candidate",
        })

    if all(_is_fermion(p) for p in initial + final):
        if charge_conserved:
            candidates.append({
                "interaction": "Electroweak fermion interaction",
                "theory": "Electroweak",
                "mediators": ["photon", "Z", "W"],
                "topologies": ["s-channel", "t-channel", "u-channel"],
                "status": "candidate",
            })

    if not candidates:
        candidates.append({
            "interaction": "No implemented interaction model found",
            "theory": "Unknown",
            "mediators": [],
            "topologies": [],
            "status": "unsupported",
        })

    return {
        "initial_particles": initial_particles,
        "final_particles": final_particles,
        "charge_conservation": {
            "initial_total": total_initial_charge,
            "final_total": total_final_charge,
            "conserved": charge_conserved,
        },
        "candidates": candidates,
        "note": (
            "Candidate generation is intentionally conservative. "
            "A candidate interaction is not yet a complete proof that "
            "the corresponding process is physically allowed."
        ),
    }


__all__ = [
    "PARTICLES",
    "INTERACTIONS",
    "Particle",
    "Interaction",
    "get_particle",
    "list_particles",
    "list_interactions",
    "particle_summary",
    "find_allowed_interactions",
]
