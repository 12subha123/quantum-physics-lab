from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from api.fock_space import router as fock_space_router
from api.scattering_simulation import router as scattering_simulation_router
from api.propagator import router as propagator_router
from api.feynman_rules import router as feynman_rules_router
from api.feynman_diagram_generator import router as feynman_diagram_generator_router
from api.qed_amplitude import router as qed_amplitude_router
from api.qed_channel_analysis import router as qed_channel_analysis_router
from api.qft_process_analysis_router import router as qft_process_analysis_router
from api.path_integral import router as path_integral_router
from api.standard_model_vertices import router as standard_model_vertices_router
from api.vertex_matching import router as vertex_matching_router
from api.topology_engine import router as topology_engine_router
from api.quantum_gates import router as quantum_gates_router
from api.entanglement import router as entanglement_router
from api.field_theory import router as field_theory_router
from api.dirac import router as dirac_router
from api.relativistic_comparison import router as relativistic_comparison_router
from api.canonical_quantization import router as canonical_quantization_router
from api.multiqubit import router as multiqubit_router
from api.harmonic_oscillator import router as harmonic_oscillator_router
from api.superposition import router as superposition_router
from api.operators_eigenstates import router as operators_eigenstates_router
from api.bloch_sphere import router as bloch_sphere_router
from api.time_evolution import router as time_evolution_router
from api.time_evolution_simulation import router as time_evolution_simulation_router
from api.density_matrix import router as density_matrix_router
from api.decoherence import router as decoherence_router
from api.measurement import router as measurement_router

from quantum.core.execution_engine import QuantumExecutionEngine


BASE_DIR = Path(__file__).resolve().parent.parent
VISUALIZATION_DIR = BASE_DIR / "quantum" / "visualization" / "outputs"
VISUALIZATION_DIR.mkdir(parents=True, exist_ok=True)


app = FastAPI(
    title="Quantum Physics Laboratory API",
    description="Interactive computational physics API for quantum mechanics simulations.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/visualizations",
    StaticFiles(directory=VISUALIZATION_DIR),
    name="visualizations",
)


execution_engine = QuantumExecutionEngine()


class TunnelingRequest(BaseModel):
    particle_energy_ev: float = Field(
        ...,
        gt=0,
        description="Particle energy in electron-volts.",
    )
    barrier_height_ev: float = Field(
        ...,
        gt=0,
        description="Potential barrier height in electron-volts.",
    )
    barrier_width_nm: float = Field(
        ...,
        gt=0,
        description="Potential barrier width in nanometers.",
    )
    particle_mass_kg: Optional[float] = Field(
        default=None,
        gt=0,
        description="Particle mass in kilograms. Defaults to electron mass.",
    )
    create_visualization: bool = Field(
        default=True,
        description="Whether to generate the tunneling visualization.",
    )


@app.get("/")
def root():
    return {
        "name": "Quantum Physics Laboratory API",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "quantum-physics-laboratory",
    }


@app.post("/api/quantum/tunneling")
def calculate_tunneling(request: TunnelingRequest):
    if request.barrier_height_ev <= request.particle_energy_ev:
        raise HTTPException(
            status_code=400,
            detail=(
                "Barrier height must be greater than particle energy "
                "for this tunneling model."
            ),
        )

    try:
        result = execution_engine.execute(
            question="What is quantum tunneling?",
            particle_energy_ev=request.particle_energy_ev,
            barrier_height_ev=request.barrier_height_ev,
            barrier_width_nm=request.barrier_width_nm,
            particle_mass_kg=request.particle_mass_kg,
            create_visualization=request.create_visualization,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Quantum calculation failed: {exc}",
        ) from exc

    if not result.success:
        raise HTTPException(
            status_code=400,
            detail=result.message,
        )

    visualization_path = result.data["visualization_path"]

    visualization_url = None

    if visualization_path:
        visualization_filename = Path(visualization_path).name
        visualization_url = "/visualizations/" + visualization_filename

    return {
        "success": True,
        "capability": result.capability,
        "message": result.message,
        "simulation_parameters": result.data["simulation_parameters"],
        "results": result.data["results"],
        "visualization_path": visualization_path,
        "visualization_url": visualization_url,
    }


# Core quantum mechanics routers
app.include_router(harmonic_oscillator_router)
app.include_router(superposition_router)
app.include_router(operators_eigenstates_router)
app.include_router(bloch_sphere_router)
app.include_router(quantum_gates_router)
app.include_router(entanglement_router)
app.include_router(multiqubit_router)
app.include_router(time_evolution_router)
app.include_router(time_evolution_simulation_router)
app.include_router(density_matrix_router)
app.include_router(decoherence_router)
app.include_router(measurement_router)


# Quantum field theory routers
app.include_router(field_theory_router)
app.include_router(dirac_router)
app.include_router(relativistic_comparison_router)
app.include_router(canonical_quantization_router)
app.include_router(fock_space_router)
app.include_router(propagator_router)
app.include_router(feynman_rules_router)
app.include_router(feynman_diagram_generator_router)
app.include_router(qed_amplitude_router)
app.include_router(qed_channel_analysis_router)
app.include_router(path_integral_router)
app.include_router(standard_model_vertices_router)
app.include_router(vertex_matching_router)
app.include_router(topology_engine_router)
from api.qcd_angular_observable import router as qcd_angular_observable_router
app.include_router(scattering_simulation_router)
app.include_router(qcd_angular_observable_router)
app.include_router(qft_process_analysis_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )

from api.qcd_angular_observable import router as qcd_angular_observable_router
from api.qft_process_analysis_router import router as qft_process_analysis_router



from api.qft_process_analysis_router import router as qft_process_analysis_router


