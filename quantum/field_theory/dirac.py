import numpy as np


def _validate_parameters(
    mass,
    amplitude,
    width,
    momentum,
    domain_length,
    duration,
    points,
    frames,
):
    mass = float(mass)
    amplitude = float(amplitude)
    width = float(width)
    momentum = float(momentum)
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
    if domain_length <= 0:
        raise ValueError("Domain length must be positive.")
    if duration <= 0:
        raise ValueError("Duration must be positive.")
    if points < 64 or points > 512:
        raise ValueError("Points must be between 64 and 512.")
    if frames < 20 or frames > 160:
        raise ValueError("Frames must be between 20 and 160.")

    return (
        mass,
        amplitude,
        width,
        momentum,
        domain_length,
        duration,
        points,
        frames,
    )


def gamma_matrices_1p1():
    gamma_0 = np.array(
        [
            [1, 0],
            [0, -1],
        ],
        dtype=complex,
    )

    gamma_1 = np.array(
        [
            [0, 1],
            [-1, 0],
        ],
        dtype=complex,
    )

    return {
        "gamma_0": gamma_0,
        "gamma_1": gamma_1,
    }


def dirac_hamiltonian_1p1(momentum, mass):
    momentum = float(momentum)
    mass = float(mass)

    if mass < 0:
        raise ValueError(
            "Mass must be non-negative."
        )

    matrices = gamma_matrices_1p1()

    gamma_0 = matrices["gamma_0"]
    gamma_1 = matrices["gamma_1"]

    beta = gamma_0
    alpha = gamma_0 @ gamma_1

    return (
        alpha * momentum
        + beta * mass
    )


def dirac_energy_levels(momentum, mass):
    hamiltonian = dirac_hamiltonian_1p1(
        momentum,
        mass,
    )

    eigenvalues, eigenvectors = np.linalg.eigh(
        hamiltonian
    )

    expected_energy = np.sqrt(
        momentum**2 + mass**2
    )

    return {
        "hamiltonian": hamiltonian,
        "eigenvalues": eigenvalues,
        "eigenvectors": eigenvectors,
        "expected_positive_energy": expected_energy,
        "expected_negative_energy": -expected_energy,
    }


def dirac_equation_summary(momentum, mass):
    result = dirac_energy_levels(
        momentum,
        mass,
    )

    eigenvalues = result["eigenvalues"]

    expected = np.array(
        [
            result["expected_negative_energy"],
            result["expected_positive_energy"],
        ]
    )

    numerical_error = float(
        np.max(
            np.abs(
                np.sort(eigenvalues.real)
                - expected
            )
        )
    )

    return {
        "momentum": float(momentum),
        "mass": float(mass),
        "units": "natural units (hbar = c = 1)",
        "dimension": "1+1",
        "equation": (
            "(i gamma^mu partial_mu - m) psi = 0"
        ),
        "dispersion_relation": (
            "E^2 = p^2 + m^2"
        ),
        "positive_energy": result[
            "expected_positive_energy"
        ],
        "negative_energy": result[
            "expected_negative_energy"
        ],
        "numerical_eigenvalues": [
            float(value.real)
            for value in eigenvalues
        ],
        "hamiltonian": [
            [
                [
                    float(value.real),
                    float(value.imag),
                ]
                for value in row
            ]
            for row in result["hamiltonian"]
        ],
        "eigenvalue_error": numerical_error,
        "validation_passed": (
            numerical_error < 1e-10
        ),
    }


def _positive_energy_spinor(momentum, mass):
    energy = np.sqrt(
        momentum**2 + mass**2
    )

    if energy < 1e-14:
        return np.array(
            [1.0, 0.0],
            dtype=complex,
        )

    upper = np.sqrt(
        (energy + mass)
        / (2.0 * energy)
    )

    lower = (
        momentum
        / (energy + mass)
        * upper
        if energy + mass > 1e-14
        else 0.0
    )

    spinor = np.array(
        [upper, lower],
        dtype=complex,
    )

    norm = np.sqrt(
        np.vdot(spinor, spinor).real
    )

    return spinor / norm


def _normalize_wavefunction(psi, dx):
    norm = np.sqrt(
        np.sum(
            np.abs(psi[0]) ** 2
            + np.abs(psi[1]) ** 2
        )
        * dx
    )

    if norm <= 1e-14:
        raise ValueError(
            "Wavefunction normalization failed."
        )

    return psi / norm


def _probability_density(psi):
    return (
        np.abs(psi[0]) ** 2
        + np.abs(psi[1]) ** 2
    )


def simulate_dirac(
    mass=1.0,
    amplitude=1.0,
    width=1.5,
    momentum=2.0,
    domain_length=20.0,
    duration=8.0,
    points=256,
    frames=100,
):
    """
    Numerically evolve a 1+1D free Dirac wave packet.

    The evolution is performed spectrally in momentum space.

    The Hamiltonian is:

        H = alpha p + beta m

    and each momentum mode is evolved exactly over
    a finite time step using the 2x2 matrix exponential
    in closed form:

        exp(-i H dt)
          = cos(E dt) I
            - i sin(E dt) H / E

    Natural units:
        hbar = c = 1

    This is an educational free-fermion simulation,
    not an interacting QFT calculation.
    """

    (
        mass,
        amplitude,
        width,
        momentum,
        domain_length,
        duration,
        points,
        frames,
    ) = _validate_parameters(
        mass,
        amplitude,
        width,
        momentum,
        domain_length,
        duration,
        points,
        frames,
    )

    dx = domain_length / points

    x = (
        np.arange(points) - points / 2.0
    ) * dx

    # Periodic Fourier grid.
    k = (
        2.0
        * np.pi
        * np.fft.fftfreq(
            points,
            d=dx,
        )
    )

    # Initial localized wave packet.
    envelope = np.exp(
        -0.5
        * (x / width) ** 2
    )

    carrier = np.exp(
        1j * momentum * x
    )

    scalar_packet = (
        amplitude
        * envelope
        * carrier
    )

    spinor = _positive_energy_spinor(
        momentum,
        mass,
    )

    psi = np.vstack(
        [
            spinor[0] * scalar_packet,
            spinor[1] * scalar_packet,
        ]
    )

    psi = _normalize_wavefunction(
        psi,
        dx,
    )

    # Stability-safe time step.
    maximum_energy = np.sqrt(
        np.max(k**2) + mass**2
    )

    if maximum_energy <= 1e-14:
        dt = duration
    else:
        dt = min(
            0.15,
            0.8 / maximum_energy,
        )

    steps = max(
        1,
        int(np.ceil(duration / dt)),
    )

    dt = duration / steps

    if steps > 5000:
        raise ValueError(
            "Simulation requires too many time steps. "
            "Reduce duration or spatial resolution."
        )

    frame_indices = np.unique(
        np.linspace(
            0,
            steps,
            min(frames, steps + 1),
            dtype=int,
        )
    )

    frame_set = set(
        int(value)
        for value in frame_indices
    )

    probability_frames = []
    upper_frames = []
    lower_frames = []
    times = []

    def store_frame(step):
        probability = _probability_density(
            psi
        )

        probability_frames.append(
            probability.copy()
        )

        upper_frames.append(
            np.abs(psi[0]) ** 2
        )

        lower_frames.append(
            np.abs(psi[1]) ** 2
        )

        times.append(
            float(step * dt)
        )

    store_frame(0)

    for step in range(1, steps + 1):
        psi_k = np.fft.fft(
            psi,
            axis=1,
        )

        energy = np.sqrt(
            k**2 + mass**2
        )

        safe_energy = np.where(
            energy > 1e-14,
            energy,
            1.0,
        )

        cosine = np.cos(
            energy * dt
        )

        sine_over_energy = (
            np.sin(energy * dt)
            / safe_energy
        )

        upper_k = psi_k[0]
        lower_k = psi_k[1]

        next_upper_k = (
            cosine * upper_k
            - 1j
            * sine_over_energy
            * (
                mass * upper_k
                + k * lower_k
            )
        )

        next_lower_k = (
            cosine * lower_k
            - 1j
            * sine_over_energy
            * (
                k * upper_k
                - mass * lower_k
            )
        )

        psi = np.vstack(
            [
                np.fft.ifft(
                    next_upper_k
                ),
                np.fft.ifft(
                    next_lower_k
                ),
            ]
        )

        if step in frame_set:
            store_frame(step)

    probability_frames = np.asarray(
        probability_frames,
        dtype=float,
    )

    upper_frames = np.asarray(
        upper_frames,
        dtype=float,
    )

    lower_frames = np.asarray(
        lower_frames,
        dtype=float,
    )

    initial_norm = float(
        np.sum(probability_frames[0])
        * dx
    )

    final_norm = float(
        np.sum(probability_frames[-1])
        * dx
    )

    norm_drift = (
        final_norm - initial_norm
    ) / initial_norm

    expectation_x = []

    for probability in probability_frames:
        expectation_x.append(
            float(
                np.sum(
                    x * probability
                )
                * dx
            )
        )

    return {
        "x": x.tolist(),
        "times": times,
        "probability_density": (
            probability_frames.tolist()
        ),
        "upper_component_density": (
            upper_frames.tolist()
        ),
        "lower_component_density": (
            lower_frames.tolist()
        ),
        "expectation_x": expectation_x,
        "parameters": {
            "mass": mass,
            "amplitude": amplitude,
            "width": width,
            "momentum": momentum,
            "domain_length": domain_length,
            "duration": duration,
            "points": points,
            "frames": len(times),
            "time_step": dt,
            "spatial_step": dx,
            "time_steps": steps,
        },
        "diagnostics": {
            "initial_norm": initial_norm,
            "final_norm": final_norm,
            "relative_norm_drift": float(
                norm_drift
            ),
            "initial_expectation_x": (
                expectation_x[0]
            ),
            "final_expectation_x": (
                expectation_x[-1]
            ),
            "positive_energy": float(
                np.sqrt(
                    momentum**2
                    + mass**2
                )
            ),
            "negative_energy": float(
                -np.sqrt(
                    momentum**2
                    + mass**2
                )
            ),
        },
        "model": (
            "1+1D free Dirac wave-packet "
            "Fourier-spectral simulation"
        ),
        "units": "natural units (hbar = c = 1)",
        "boundary_condition": (
            "periodic spatial boundary"
        ),
    }
