import numpy as np
import matplotlib.pyplot as plt

# Qubit state parameters
theta = np.pi / 3
phi = np.pi / 4

# Bloch-sphere coordinates
x_state = np.sin(theta) * np.cos(phi)
y_state = np.sin(theta) * np.sin(phi)
z_state = np.cos(theta)

# Create sphere
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 50)

x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones_like(u), np.cos(v))

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111, projection="3d")

# Bloch sphere
ax.plot_surface(
    x,
    y,
    z,
    alpha=0.15,
    linewidth=0
)

# Coordinate axes
ax.plot([-1, 1], [0, 0], [0, 0], linewidth=1)
ax.plot([0, 0], [-1, 1], [0, 0], linewidth=1)
ax.plot([0, 0], [0, 0], [-1, 1], linewidth=1)

# State vector
ax.quiver(
    0,
    0,
    0,
    x_state,
    y_state,
    z_state,
    linewidth=3
)

# Labels
ax.text(1.1, 0, 0, "X")
ax.text(0, 1.1, 0, "Y")
ax.text(0, 0, 1.1, "|0>")
ax.text(0, 0, -1.1, "|1>")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.set_title(
    r"Bloch Sphere: "
    r"$|\psi\rangle = "
    r"\cos(\theta/2)|0\rangle + "
    r"e^{i\phi}\sin(\theta/2)|1\rangle$"
)

ax.set_box_aspect([1, 1, 1])

plt.tight_layout()
plt.show()

print("Spin-1/2 Bloch Sphere")
print("---------------------")
print(f"Theta: {theta:.4f} rad")
print(f"Phi:   {phi:.4f} rad")
print()
print("Bloch vector:")
print(f"X = {x_state:.4f}")
print(f"Y = {y_state:.4f}")
print(f"Z = {z_state:.4f}")
