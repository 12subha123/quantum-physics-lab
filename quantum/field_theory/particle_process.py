from dataclasses import dataclass


@dataclass(frozen=True)
class ParticleProcess:
    initial_particles: tuple[str, ...]
    final_particles: tuple[str, ...]

    @property
    def initial_count(self) -> int:
        return len(self.initial_particles)

    @property
    def final_count(self) -> int:
        return len(self.final_particles)

    @property
    def notation(self) -> str:
        initial = " + ".join(self.initial_particles)
        final = " + ".join(self.final_particles)
        return f"{initial} → {final}"

    @property
    def topology_label(self) -> str:
        return f"{self.initial_count} → {self.final_count}"


def create_process(
    initial_particles: list[str],
    final_particles: list[str],
) -> ParticleProcess:
    if not initial_particles:
        raise ValueError("At least one initial-state particle is required.")

    if not final_particles:
        raise ValueError("At least one final-state particle is required.")

    normalized_initial = tuple(
        particle.strip().lower()
        for particle in initial_particles
    )

    normalized_final = tuple(
        particle.strip().lower()
        for particle in final_particles
    )

    if any(not particle for particle in normalized_initial):
        raise ValueError("Initial-state particles cannot be empty.")

    if any(not particle for particle in normalized_final):
        raise ValueError("Final-state particles cannot be empty.")

    return ParticleProcess(
        initial_particles=normalized_initial,
        final_particles=normalized_final,
    )


def process_summary(
    initial_particles: list[str],
    final_particles: list[str],
) -> dict:
    process = create_process(
        initial_particles,
        final_particles,
    )

    return {
        "success": True,
        "process": process.notation,
        "topology": process.topology_label,
        "initial_count": process.initial_count,
        "final_count": process.final_count,
        "initial_particles": list(process.initial_particles),
        "final_particles": list(process.final_particles),
        "supports_general_multiplicity": True,
        "scientific_scope": (
            "General N-to-M particle-process representation. "
            "This layer defines process multiplicity only; it does not "
            "claim that every N-to-M process is physically allowed."
        ),
    }
