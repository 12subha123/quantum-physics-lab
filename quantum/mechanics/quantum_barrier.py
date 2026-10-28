import numpy as np


class QuantumBarrier:
    """
    One-dimensional rectangular quantum barrier.

    Uses the analytic transmission probability for a particle
    encountering a finite rectangular potential barrier.

    SI quantities:
        particle energy E -> joules
        barrier height V0 -> joules
        barrier width a -> meters
        particle mass m -> kilograms
    """

    def __init__(self, mass, barrier_height, width):
        if mass <= 0:
            raise ValueError("Particle mass must be positive.")

        if barrier_height < 0:
            raise ValueError("Barrier height cannot be negative.")

        if width <= 0:
            raise ValueError("Barrier width must be positive.")

        self.mass = float(mass)
        self.barrier_height = float(barrier_height)
        self.width = float(width)

        self.hbar = 1.054571817e-34

    def transmission_probability(self, energy):
        """
        Calculate transmission probability T.

        Handles both E < V0 and E > V0.
        """

        if energy < 0:
            raise ValueError("Particle energy cannot be negative.")

        energy = float(energy)

        if energy == self.barrier_height:
            return 1.0

        if energy < self.barrier_height:
            kappa = np.sqrt(
                2 * self.mass * (self.barrier_height - energy)
            ) / self.hbar

            numerator = 1.0

            denominator = 1.0 + (
                self.barrier_height**2
                * np.sinh(kappa * self.width)**2
                / (4 * energy * (self.barrier_height - energy))
            )

            return float(numerator / denominator)

        k = np.sqrt(
            2 * self.mass * energy
        ) / self.hbar

        q = np.sqrt(
            2 * self.mass * (energy - self.barrier_height)
        ) / self.hbar

        numerator = 1.0

        denominator = 1.0 + (
            self.barrier_height**2
            * np.sin(q * self.width)**2
            / (4 * energy * (energy - self.barrier_height))
        )

        return float(numerator / denominator)
