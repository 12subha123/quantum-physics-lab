from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from quantum.core.query_engine import QuantumQueryEngine
from quantum.engine.solver.tunneling_solver import (
    calculate_tunneling_probability,
)
from quantum.visualization.tunneling_visualization import (
    plot_tunneling,
)


@dataclass
class PhysicsExecutionResult:
    capability: str
    success: bool
    message: str
    data: Any = None


class QuantumExecutionEngine:
    def __init__(self):
        self.query_engine = QuantumQueryEngine()

    def execute(
        self,
        question: str,
        particle_energy_ev: float = 2.0,
        barrier_height_ev: float = 5.0,
        barrier_width_nm: float = 0.5,
        particle_mass_kg: Optional[float] = None,
        create_visualization: bool = True,
    ) -> PhysicsExecutionResult:

        capabilities = self.query_engine.find_capabilities(question)

        if not capabilities:
            return PhysicsExecutionResult(
                capability="unknown",
                success=False,
                message="No suitable quantum physics capability was found.",
            )

        capability = capabilities[0]

        if capability.name == "quantum_tunneling":
            return self._execute_tunneling(
                particle_energy_ev=particle_energy_ev,
                barrier_height_ev=barrier_height_ev,
                barrier_width_nm=barrier_width_nm,
                particle_mass_kg=particle_mass_kg,
                create_visualization=create_visualization,
            )

        return PhysicsExecutionResult(
            capability=capability.name,
            success=False,
            message=(
                f"The capability '{capability.name}' is registered "
                "but its execution handler is not implemented yet."
            ),
        )

    def _execute_tunneling(
        self,
        particle_energy_ev: float,
        barrier_height_ev: float,
        barrier_width_nm: float,
        particle_mass_kg: Optional[float],
        create_visualization: bool,
    ) -> PhysicsExecutionResult:

        if particle_mass_kg is None:
            result = calculate_tunneling_probability(
                particle_energy_ev=particle_energy_ev,
                barrier_height_ev=barrier_height_ev,
                barrier_width_nm=barrier_width_nm,
            )
        else:
            result = calculate_tunneling_probability(
                particle_energy_ev=particle_energy_ev,
                barrier_height_ev=barrier_height_ev,
                barrier_width_nm=barrier_width_nm,
                particle_mass_kg=particle_mass_kg,
            )

        visualization_path = None

        if create_visualization:
            base_dir = Path(__file__).resolve().parent.parent.parent

            output_dir = (
                base_dir
                / "quantum"
                / "visualization"
                / "outputs"
            )

            output_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            visualization_path = (
                output_dir / "tunneling_simulation.png"
            )

            plot_tunneling(
                particle_energy_ev=particle_energy_ev,
                barrier_height_ev=barrier_height_ev,
                barrier_width_nm=barrier_width_nm,
                output_path=visualization_path,
            )

        data = {
            "simulation_parameters": {
                "particle_energy_ev": result.particle_energy_ev,
                "barrier_height_ev": result.barrier_height_ev,
                "barrier_width_nm": result.barrier_width_nm,
                "particle_mass_kg": result.particle_mass_kg,
            },
            "results": {
                "kappa_per_meter": result.kappa_per_meter,
                "transmission_probability": (
                    result.transmission_probability
                ),
                "reflection_probability": (
                    result.reflection_probability
                ),
                "transmission_percentage": (
                    result.transmission_percentage
                ),
                "reflection_percentage": (
                    result.reflection_percentage
                ),
            },
            "visualization_path": (
                str(visualization_path)
                if visualization_path
                else None
            ),
        }

        return PhysicsExecutionResult(
            capability="quantum_tunneling",
            success=True,
            message=(
                "Quantum tunneling calculation completed "
                "successfully."
            ),
            data=data,
        )


execution_engine = QuantumExecutionEngine()


if __name__ == "__main__":
    print("Quantum Execution Engine")
    print("========================")
    print()

    result = execution_engine.execute(
        question="What is quantum tunneling?",
        particle_energy_ev=2.0,
        barrier_height_ev=5.0,
        barrier_width_nm=0.5,
        create_visualization=True,
    )

    print(f"Capability: {result.capability}")
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    print()

    if result.success:
        print("Simulation parameters:")

        for key, value in result.data[
            "simulation_parameters"
        ].items():
            print(f"  {key}: {value}")

        print()
        print("Results:")

        for key, value in result.data["results"].items():
            print(f"  {key}: {value}")

        print()
        print(
            "Visualization path:",
            result.data["visualization_path"],
        )
