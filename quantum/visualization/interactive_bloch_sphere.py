import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Initial state
theta_initial = np.pi / 3
phi_initial = np.pi / 4

# Bloch sphere coordinates
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 50)

sphere_x = np.outer(np.cos(u), np.sin(v))
sphere_y = np.outer(np.sin(u), np.sin(v))
sphere_z = np.outer(np.ones_like(u), np.cos(v))

fig = plt.figure(figsize=(10, 9))
ax = fig.add_subplot(111, projection="3d")

plt.subplots_adjust(bottom=0.22)

# Sphere
ax.plot_surface(
    sphere_x,
    sphere_y,
    sphere_z,
    alpha=0.15,
    linewidth=0
)

# Axes
ax.plot([-1, 1], [0, 0], [0, 0], linewidth=1)
ax.plot([0, 0], [-1, 1], [0, 0], linewidth=1)
ax.plot([0, 0], [0, 0], [-1, 1], linewidth=1)

# State vector
theta = theta_initial
phi = phi_initial

state_x = np.sin(theta) * np.cos(phi)
state_y = np.sin(theta) * np.sin(phi)
state_z = np.cos(theta)

vector = ax.quiver(
    0,
    0,
    0,
    state_x,
    state_y,
    state_z,
    linewidth=3
)

ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_zlim(-1.2, 1.2)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.set_title("Interactive Qubit Bloch Sphere")

# Sliders
theta_axis = plt.axes([0.18, 0.10, 0.65, 0.03])
phi_axis = plt.axes([0.18, 0.05, 0.65, 0.03])

theta_slider = Slider(
    theta_axis,
    "Theta",
    0,
    np.pi,
    valinit=theta_initial
)

phi_slider = Slider(
    phi_axis,
    "Phi",
    0,
    2 * np.pi,
    valinit=phi_initial
)


def update(_):
    global vector

    theta = theta_slider.val
    phi = phi_slider.val

    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    # Remove old vector
    vector.remove()

    # Draw updated vector
    vector = ax.quiver(
        0,
        0,
        0,
        x,
        y,
        z,
        linewidth=3
    )

    # Measurement probabilities
    p0 = np.cos(theta / 2) ** 2
    p1 = np.sin(theta / 2) ** 2

    ax.set_title(
        f"Interactive Bloch Sphere\n"
        f"P(0) = {p0:.3f}    P(1) = {p1:.3f}"
    )

    fig.canvas.draw_idle()


theta_slider.on_changed(update)
phi_slider.on_changed(update)

plt.show()
