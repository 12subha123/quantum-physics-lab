import numpy as np
import matplotlib.pyplot as plt

# Spatial grid
x = np.linspace(-5, 5, 1000)

# Normalized harmonic oscillator states
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
    factorial = np.math.factorial(n) if hasattr(np, "math") else __import__("math").factorial(n)

    normalization = (
        1
        / np.sqrt(2**n * factorial)
        * np.pi**(-0.25)
    )

    return (
        normalization
        * hermite_polynomial(n, x)
        * np.exp(-x**2 / 2)
    )


# Ground state and first excited state
psi_0 = wavefunction(0, x)
psi_1 = wavefunction(1, x)

# Superposition:
# |psi> = (|0> + |1>) / sqrt(2)
psi = (psi_0 + psi_1) / np.sqrt(2)

# Probability density
probability = np.abs(psi)**2

# Normalize numerically
probability /= np.trapezoid(probability, x)

# Measurement probabilities
c0 = 1 / np.sqrt(2)
c1 = 1 / np.sqrt(2)

p0 = abs(c0)**2
p1 = abs(c1)**2

print("Quantum Superposition")
print("---------------------")
print(f"Probability of measuring n=0: {p0:.2f}")
print(f"Probability of measuring n=1: {p1:.2f}")
print(f"Total measurement probability: {p0 + p1:.2f}")

# Visualization
plt.figure(figsize=(11, 7))

plt.plot(
    x,
    psi,
    label=r"Superposition $\psi(x)$"
)

plt.plot(
    x,
    probability,
    label=r"Probability density $|\psi(x)|^2$"
)

plt.xlabel("Position x")
plt.ylabel("Amplitude / Probability")
plt.title(r"Quantum Superposition: $\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$")
plt.axhline(0, linewidth=0.8)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
