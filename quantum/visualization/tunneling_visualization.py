from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def plot_tunneling(
    particle_energy_ev: float,
    barrier_height_ev: float,
    barrier_width_nm: float,
    output_path: str | Path,
) -> str:

    if particle_energy_ev <= 0:
        raise ValueError("Particle energy must be positive.")

    if barrier_height_ev <= particle_energy_ev:
        raise ValueError(
            "Barrier height must be greater than particle energy."
        )

    if barrier_width_nm <= 0:
        raise ValueError("Barrier width must be positive.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    barrier_start = 1.5
    barrier_end = barrier_start + barrier_width_nm

    x_end = max(4.0, barrier_end + 1.5)
    x = np.linspace(0.0, x_end, 1200)

    wavelength_scale = 0.8 / np.sqrt(particle_energy_ev)
    k = 2 * np.pi / wavelength_scale

    wave_amplitude = 0.22

    incident_wave = (
        particle_energy_ev
        + wave_amplitude * np.sin(k * x)
    )

    decay_strength = np.sqrt(
        max(barrier_height_ev - particle_energy_ev, 0.0)
    )

    inside_distance = np.maximum(
        x - barrier_start,
        0.0,
    )

    barrier_decay = np.exp(
        -1.4 * decay_strength * inside_distance
    )

    transmitted_wave = (
        particle_energy_ev
        + wave_amplitude
        * barrier_decay
        * np.sin(k * x)
    )

    wave = np.where(
        x < barrier_start,
        incident_wave,
        transmitted_wave,
    )

    potential = np.where(
        (x >= barrier_start) & (x <= barrier_end),
        barrier_height_ev,
        0.0,
    )

    fig, ax = plt.subplots(figsize=(10, 5.5))

    ax.plot(
        x,
        wave,
        label="Conceptual wavefunction",
        linewidth=1.5,
    )

    ax.plot(
        x,
        potential,
        label="Potential barrier",
        linewidth=2.5,
    )

    ax.axhline(
        particle_energy_ev,
        linestyle="--",
        linewidth=1.2,
        label="Particle energy",
    )

    ax.axvspan(
        barrier_start,
        barrier_end,
        alpha=0.15,
    )

    ax.text(
        (barrier_start + barrier_end) / 2,
        barrier_height_ev * 0.5,
        "Barrier",
        ha="center",
        va="center",
    )

    ax.set_title(
        "Quantum Tunneling - Rectangular Barrier"
    )

    ax.set_xlabel("Position (nm)")
    ax.set_ylabel("Energy / Wave amplitude")
    ax.grid(True, alpha=0.25)
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    return str(output_path)


if __name__ == "__main__":
    output = Path(
        "quantum/visualization/outputs/tunneling_visualization_test.png"
    )

    path = plot_tunneling(
        particle_energy_ev=2.0,
        barrier_height_ev=5.0,
        barrier_width_nm=0.5,
        output_path=output,
    )

    print(f"Visualization created: {path}")
