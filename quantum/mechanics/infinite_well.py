import numpy as np

from quantum.utils.constants import HBAR, ELECTRON_VOLT, joules_to_ev


class InfinitePotentialWell:
    """
    One-dimensional infinite potential well.

    The particle is confined to 0 <= x <= L.

    SI mode:
        length -> meters
        mass   -> kilograms
        energy -> joules

    The optional dimensionless mode keeps hbar = 1.
    """

    def __init__(self, length=1.0, mass=1.0, use_si=False):
        if length <= 0:
            raise ValueError("Well length must be positive.")

        if mass <= 0:
            raise ValueError("Particle mass must be positive.")

        self.length = float(length)
        self.mass = float(mass)
        self.use_si = bool(use_si)

        self.hbar = HBAR if self.use_si else 1.0

    def energy(self, n):
        """Return the nth allowed energy level in joules."""
        if n < 1 or int(n) != n:
            raise ValueError("Quantum number n must be a positive integer.")

        n = int(n)

        return (
            n**2
            * np.pi**2
            * self.hbar**2
            / (2 * self.mass * self.length**2)
        )

    def energy_ev(self, n):
        """Return the nth energy level in electronvolts."""
        if not self.use_si:
            raise ValueError("energy_ev requires SI mode.")

        return joules_to_ev(self.energy(n))

    def wavefunction(self, n, x):
        """Return the normalized nth stationary-state wavefunction."""
        if n < 1 or int(n) != n:
            raise ValueError("Quantum number n must be a positive integer.")

        n = int(n)
        x = np.asarray(x, dtype=float)

        psi = np.sqrt(2 / self.length) * np.sin(
            n * np.pi * x / self.length
        )

        outside = (x < 0) | (x > self.length)
        psi = np.where(outside, 0.0, psi)

        return psi

    def probability_density(self, n, x):
        """Return |psi(x)|^2 for the nth state."""
        psi = self.wavefunction(n, x)
        return np.abs(psi) ** 2
