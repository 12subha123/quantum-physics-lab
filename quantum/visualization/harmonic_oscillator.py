import numpy as np
import math
import matplotlib.pyplot as plt

# Physical parameters
hbar = 1.0
m = 1.0
omega = 1.0

# Spatial grid
x = np.linspace(-5, 5, 1000)

# Harmonic oscillator potential
V = 0.5 * m * omega**2 * x**2

# Energy eigenvalues
def energy(n):
    return hbar * omega * (n + 0.5)

# Normalized harmonic oscillator wavefunctions
def hermite_polynomial(n, x):
    if n == 0:
        return np.ones_like(x)

    if n == 1:
        return 2 * x

    h0 = np.ones_like(x)
    h1 = 2 * x

    for k in range(2, n + 1):
        h2 = 2 * x * h1 - 2 * (k - 1) * h0
        h0, h1 = h1, h2

    return h1


def wavefunction(n, x):
    prefactor = (
        1
        / np.sqrt(
            2**n
            * math.factorial(n)
        )
        * np.pi**(-0.25)
    )

    gaussian = np.exp(-x**2 / 2)

    return prefactor * hermite_polynomial(n, x) * gaussian


# Number of states to display
num_states = 5

plt.figure(figsize=(11, 8))

# Plot potential
plt.plot(x, V, label="Harmonic Potential V(x)")

# Plot energy levels and wavefunctions
scale = 0.7

for n in range(num_states):
    E = energy(n)
    psi = wavefunction(n, x)

    # Energy level
    plt.axhline(E, linestyle="--", linewidth=0.8)

    # Shift wavefunction to its energy level
    plt.plot(
        x,
        E + scale * psi,
        label=f"n={n}, E={E:.2f}"
    )

    # Probability density
    probability = psi**2

    plt.plot(
        x,
        E + scale * probability,
        linewidth=1.0
    )

plt.xlabel("Position x")
plt.ylabel("Energy / Wavefunction")
plt.title("Quantum Harmonic Oscillator")
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
