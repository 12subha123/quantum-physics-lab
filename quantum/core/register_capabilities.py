from quantum.core.capability_registry import (
    PhysicsCapability,
    registry,
)


def register_quantum_capabilities():
    registry.register(
        PhysicsCapability(
            name="quantum_tunneling",
            description=(
                "Simulate quantum tunneling through a potential barrier "
                "and visualize wavefunctions and probability behavior."
            ),
            category="quantum_mechanics",
            handler="quantum.visualization.tunneling_plot",
        )
    )

    registry.register(
        PhysicsCapability(
            name="harmonic_oscillator",
            description=(
                "Calculate and visualize quantum harmonic oscillator "
                "energy levels, wavefunctions, and probability densities."
            ),
            category="quantum_mechanics",
            handler="quantum.visualization.harmonic_oscillator",
        )
    )

    registry.register(
        PhysicsCapability(
            name="superposition",
            description=(
                "Simulate quantum superposition and measurement "
                "probabilities for quantum states."
            ),
            category="quantum_mechanics",
            handler="quantum.visualization.superposition",
        )
    )

    registry.register(
        PhysicsCapability(
            name="operators_eigenstates",
            description=(
                "Demonstrate quantum operators, eigenstates, "
                "and eigenvalue equations."
            ),
            category="quantum_mechanics",
            handler="quantum.visualization.operators_eigenstates",
        )
    )

    registry.register(
        PhysicsCapability(
            name="bloch_sphere",
            description=(
                "Visualize spin-1/2 quantum states using the Bloch sphere."
            ),
            category="quantum_mechanics",
            handler="quantum.visualization.bloch_sphere",
        )
    )

    registry.register(
        PhysicsCapability(
            name="interactive_bloch_sphere",
            description=(
                "Interactively explore qubit states by changing "
                "theta and phi on the Bloch sphere."
            ),
            category="quantum_mechanics",
            handler="quantum.visualization.interactive_bloch_sphere",
        )
    )

    registry.register(
        PhysicsCapability(
            name="quantum_gates",
            description=(
                "Simulate fundamental quantum gates including "
                "X, Y, Z, H, S, and T."
            ),
            category="quantum_computing",
            handler="quantum.computing.quantum_gates",
        )
    )


if __name__ == "__main__":
    register_quantum_capabilities()

    print("Quantum capabilities registered:")
    print()

    for capability in registry.list_capabilities():
        print(
            f"- {capability.name} "
            f"[{capability.category}]"
        )
