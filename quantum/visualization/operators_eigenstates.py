import numpy as np
import matplotlib.pyplot as plt

# Spatial grid
x = np.linspace(-5, 5, 1000)
dx = x[1] - x[0]

# Ground-state harmonic oscillator wavefunction
psi = np.pi**(-0.25) * np.exp(-x**2 / 2)

# Normalize numerically
psi /= np.sqrt(np.trapezoid(np.abs(psi)**2, x))

# Position operator
x_operator = x * psi

# Momentum operator:
# p = -i hbar d/dx
hbar = 1.0
dpsi_dx = np.gradient(psi, dx)
momentum_operator = -1j * hbar * dpsi_dx

# Hamiltonian:
# H = -(hbar^2 / 2m)d²/dx² + V(x)
m = 1.0
omega = 1.0

second_derivative = np.gradient(
    np.gradient(psi, dx),
    dx
)

kinetic = -(hbar**2 / (2 * m)) * second_derivative
potential = 0.5 * m * omega**2 * x**2 * psi

hamiltonian_psi = kinetic + potential

# Expected ground-state energy
expected_energy = hbar * omega * 0.5

print("Quantum Operators and Eigenstates")
print("----------------------------------")
print(f"Expected ground-state energy: {expected_energy:.4f}")

# Numerical expectation value
energy_numerical = np.trapezoid(
    np.conjugate(psi) * hamiltonian_psi,
    x
).real

print(f"Numerical energy expectation: {energy_numerical:.4f}")

# Visualization
plt.figure(figsize=(11, 7))

plt.plot(
    x,
    psi,
    label=r"Eigenstate $\psi_0(x)$"
)

plt.plot(
    x,
    hamiltonian_psi,
    label=r"$\hat{H}\psi_0(x)$"
)

plt.plot(
    x,
    expected_energy * psi,
    linestyle="--",
    label=r"$E_0\psi_0(x)$"
)

plt.xlabel("Position x")
plt.ylabel("Amplitude")
plt.title("Quantum Operator Acting on an Eigenstate")
plt.axhline(0, linewidth=0.8)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()
