import numpy as np


def _validate_parameters(
    mass,
    amplitude,
    width,
    wavenumber,
    domain_length,
    duration,
    points,
    frames,
):
    mass = float(mass)
    amplitude = float(amplitude)
    width = float(width)
    wavenumber = float(wavenumber)
    domain_length = float(domain_length)
    duration = float(duration)
    points = int(points)
    frames = int(frames)

    if mass < 0:
        raise ValueError("Mass must be non-negative.")
    if amplitude <= 0:
        raise ValueError("Amplitude must be positive.")
    if width <= 0:
        raise ValueError("Width must be positive.")
    if wavenumber < 0:
        raise ValueError("Wavenumber must be non-negative.")
    if domain_length <= 0:
        raise ValueError("Domain length must be positive.")
    if duration <= 0:
        raise ValueError("Duration must be positive.")
    if points < 51 or points > 401:
        raise ValueError("Points must be between 51 and 401.")
    if frames < 20 or frames > 160:
        raise ValueError("Frames must be between 20 and 160.")
    if width >= domain_length / 2:
        raise ValueError(
            "Width must be smaller than half the domain length."
        )

    return (
        mass,
        amplitude,
        width,
        wavenumber,
        domain_length,
        duration,
        points,
        frames,
    )


def _discrete_energy(field, previous_field, dx, dt, mass):
    velocity = np.zeros_like(field)

    if previous_field is not None:
        velocity[1:-1] = (
            field[1:-1] - previous_field[1:-1]
        ) / dt

    gradient = np.zeros_like(field)
    gradient[1:-1] = (
        field[2:] - field[:-2]
    ) / (2.0 * dx)

    density = 0.5 * (
        velocity**2
        + gradient**2
        + mass**2 * field**2
    )

    return float(np.sum(density) * dx)


def simulate_klein_gordon(
    mass=1.0,
    amplitude=1.0,
    width=1.5,
    wavenumber=2.0,
    domain_length=20.0,
    duration=8.0,
    points=201,
    frames=100,
):
    """
    Numerically evolve the 1+1D Klein-Gordon equation:

        d²phi/dt² = d²phi/dx² - m² phi

    using a second-order finite-difference scheme.

    Natural units are used:

        hbar = c = 1

    Boundary condition:

        phi = 0

    at both ends of the spatial domain.

    This is an educational numerical field simulation,
    not a full 3+1D research-grade QFT calculation.
    """

    (
        mass,
        amplitude,
        width,
        wavenumber,
        domain_length,
        duration,
        points,
        frames,
    ) = _validate_parameters(
        mass,
        amplitude,
        width,
        wavenumber,
        domain_length,
        duration,
        points,
        frames,
    )

    x = np.linspace(
        -domain_length / 2.0,
        domain_length / 2.0,
        points,
    )

    dx = float(x[1] - x[0])

    # Stability-safe time step for the explicit finite-difference scheme.
    dt_max = 2.0 / np.sqrt(
        mass**2 + 4.0 / dx**2
    )

    dt = 0.8 * dt_max

    steps = int(np.ceil(duration / dt))
    dt = duration / steps

    if steps > 5000:
        raise ValueError(
            "Simulation requires too many time steps. "
            "Reduce duration or increase the spatial spacing."
        )

    # Gaussian-modulated carrier wave.
    initial_field = (
        amplitude
        * np.exp(
            -0.5
            * (x / width) ** 2
        )
        * np.cos(wavenumber * x)
    )

    # Initial field velocity is zero.
    previous_field = initial_field.copy()

    acceleration = np.zeros_like(initial_field)

    acceleration[1:-1] = (
        (
            initial_field[2:]
            - 2.0 * initial_field[1:-1]
            + initial_field[:-2]
        )
        / dx**2
        - mass**2 * initial_field[1:-1]
    )

    # Second-order Taylor initialization.
    current_field = (
        initial_field
        + 0.5 * dt**2 * acceleration
    )

    current_field[0] = 0.0
    current_field[-1] = 0.0

    frame_indices = np.unique(
        np.linspace(
            0,
            steps,
            min(frames, steps + 1),
            dtype=int,
        )
    )

    frame_index_set = set(
        int(value) for value in frame_indices
    )

    field_frames = []
    time_frames = []

    # Frame at t = 0.
    if 0 in frame_index_set:
        field_frames.append(
            initial_field.copy()
        )
        time_frames.append(0.0)

    if steps >= 1 and 1 in frame_index_set:
        field_frames.append(
            current_field.copy()
        )
        time_frames.append(dt)

    for step in range(1, steps):
        next_field = np.zeros_like(
            current_field
        )

        laplacian = (
            current_field[2:]
            - 2.0 * current_field[1:-1]
            + current_field[:-2]
        ) / dx**2

        next_field[1:-1] = (
            2.0 * current_field[1:-1]
            - previous_field[1:-1]
            + dt**2
            * (
                laplacian
                - mass**2 * current_field[1:-1]
            )
        )

        next_field[0] = 0.0
        next_field[-1] = 0.0

        next_step = step + 1

        if next_step in frame_index_set:
            field_frames.append(
                next_field.copy()
            )
            time_frames.append(
                next_step * dt
            )

        previous_field = current_field
        current_field = next_field

    fields = np.asarray(
        field_frames,
        dtype=float,
    )

    times = np.asarray(
        time_frames,
        dtype=float,
    )

    initial_energy = _discrete_energy(
        initial_field,
        None,
        dx,
        dt,
        mass,
    )

    final_energy = _discrete_energy(
        current_field,
        previous_field,
        dx,
        dt,
        mass,
    )

    if abs(initial_energy) > 1e-14:
        energy_drift = (
            (final_energy - initial_energy)
            / initial_energy
        )
    else:
        energy_drift = 0.0

    return {
        "x": x.tolist(),
        "times": times.tolist(),
        "field": fields.tolist(),
        "parameters": {
            "mass": mass,
            "amplitude": amplitude,
            "width": width,
            "wavenumber": wavenumber,
            "domain_length": domain_length,
            "duration": duration,
            "points": points,
            "frames": len(fields),
            "time_step": dt,
            "spatial_step": dx,
            "time_steps": steps,
        },
        "diagnostics": {
            "initial_max_abs_field": float(
                np.max(np.abs(initial_field))
            ),
            "final_max_abs_field": float(
                np.max(np.abs(current_field))
            ),
            "maximum_abs_field": float(
                np.max(np.abs(fields))
            ),
            "discrete_energy_initial": initial_energy,
            "discrete_energy_final": final_energy,
            "discrete_energy_relative_drift": float(
                energy_drift
            ),
        },
        "model": "1+1D Klein-Gordon finite-difference simulation",
        "units": "natural units (hbar = c = 1)",
        "boundary_condition": "Dirichlet: phi = 0 at both spatial boundaries",
    }
