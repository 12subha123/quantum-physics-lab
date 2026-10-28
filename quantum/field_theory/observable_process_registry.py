from dataclasses import dataclass
from typing import Callable


MatrixElementEvaluator = Callable[[float, float, float, float], float]


@dataclass(frozen=True)
class ObservableProcess:
    process_id: str
    name: str
    theory: str
    initial_particles: tuple[str, ...]
    final_particles: tuple[str, ...]
    matrix_element_evaluator: MatrixElementEvaluator | None
    observable_type: str
    status: str
    scientific_scope: str


def _qed_ee_to_mumu(
    s: float,
    t: float,
    u: float,
    coupling: float,
) -> float:
    return 2.0 * coupling**4 * (u**2 + t**2) / s**2


def _build_default_registry() -> dict[str, ObservableProcess]:
    return {
        "qed_electron_muon_annihilation": ObservableProcess(
            process_id="qed_electron_muon_annihilation",
            name="e- + e+ -> mu- + mu+",
            theory="QED",
            initial_particles=("electron", "positron"),
            final_particles=("muon", "antimuon"),
            matrix_element_evaluator=None,
            observable_type="2_to_2_cross_section",
            status="registered",
            scientific_scope=(
                "Tree-level QED regression process. "
                "Numerical matrix-element evaluation remains "
                "available through the dedicated QED engine."
            ),
        ),
        "qcd_quark_antiquark_to_gluons": ObservableProcess(
            process_id="qcd_quark_antiquark_to_gluons",
            name="q + anti-q -> g + g",
            theory="QCD",
            initial_particles=("up", "anti-up"),
            final_particles=("gluon", "gluon"),
            matrix_element_evaluator=None,
            observable_type="2_to_2_cross_section",
            status="topology_ready",
            scientific_scope=(
                "QCD process registry entry. Full color/spin-summed "
                "matrix element is not yet implemented."
            ),
        ),
        "electroweak_fermion_scattering": ObservableProcess(
            process_id="electroweak_fermion_scattering",
            name="fermion scattering",
            theory="Electroweak",
            initial_particles=("electron", "positron"),
            final_particles=("electron", "positron"),
            matrix_element_evaluator=None,
            observable_type="2_to_2_cross_section",
            status="topology_ready",
            scientific_scope=(
                "Electroweak registry entry. Full massive "
                "spinor matrix element is not yet implemented."
            ),
        ),
        "higgs_fermion_yukawa": ObservableProcess(
            process_id="higgs_fermion_yukawa",
            name="Higgs-fermion Yukawa interaction",
            theory="Electroweak",
            initial_particles=("fermion", "antifermion"),
            final_particles=("higgs",),
            matrix_element_evaluator=None,
            observable_type="decay_rate",
            status="vertex_ready",
            scientific_scope=(
                "Higgs Yukawa registry entry. Numerical decay "
                "amplitude is not yet implemented."
            ),
        ),
        "phi4_2_to_2": ObservableProcess(
            process_id="phi4_2_to_2",
            name="scalar phi4 2 -> 2 scattering",
            theory="Scalar phi4",
            initial_particles=("scalar", "scalar"),
            final_particles=("scalar", "scalar"),
            matrix_element_evaluator=None,
            observable_type="2_to_2_cross_section",
            status="vertex_ready",
            scientific_scope=(
                "Tree-level phi4 registry entry. Numerical "
                "observable evaluation will be connected to the "
                "existing phi4 Feynman-rule engine."
            ),
        ),
    }


_PROCESS_REGISTRY = _build_default_registry()


def list_observable_processes() -> tuple[ObservableProcess, ...]:
    return tuple(_PROCESS_REGISTRY.values())


def get_observable_process(process_id: str) -> ObservableProcess:
    try:
        return _PROCESS_REGISTRY[process_id]
    except KeyError as exc:
        raise ValueError(
            f"Unknown observable process: {process_id}"
        ) from exc


def register_observable_process(process: ObservableProcess) -> None:
    if not process.process_id.strip():
        raise ValueError("process_id cannot be empty.")

    if process.process_id in _PROCESS_REGISTRY:
        raise ValueError(
            f"Observable process already registered: {process.process_id}"
        )

    _PROCESS_REGISTRY[process.process_id] = process


def observable_process_summary() -> dict:
    processes = list_observable_processes()

    by_theory: dict[str, int] = {}
    by_status: dict[str, int] = {}

    for process in processes:
        by_theory[process.theory] = by_theory.get(process.theory, 0) + 1
        by_status[process.status] = by_status.get(process.status, 0) + 1

    return {
        "success": True,
        "process_count": len(processes),
        "processes": [
            {
                "process_id": process.process_id,
                "name": process.name,
                "theory": process.theory,
                "initial_particles": list(process.initial_particles),
                "final_particles": list(process.final_particles),
                "observable_type": process.observable_type,
                "status": process.status,
            }
            for process in processes
        ],
        "by_theory": by_theory,
        "by_status": by_status,
        "scientific_scope": (
            "Universal process registry architecture for numerical "
            "cross sections and decay rates. Registry membership does "
            "not imply that a complete numerical matrix element exists."
        ),
    }
