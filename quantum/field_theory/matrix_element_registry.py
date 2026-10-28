from dataclasses import dataclass
from typing import Any, Callable


MatrixElementEvaluator = Callable[..., Any]


@dataclass(frozen=True)
class MatrixElementProcess:
    process_id: str
    name: str
    theory: str
    evaluator: MatrixElementEvaluator | None
    status: str
    scientific_scope: str


_REGISTRY: dict[str, MatrixElementProcess] = {}


def register_matrix_element_process(
    process_id: str,
    name: str,
    theory: str,
    evaluator: MatrixElementEvaluator | None,
    status: str,
    scientific_scope: str,
) -> None:
    process_id = process_id.strip()

    if not process_id:
        raise ValueError("process_id cannot be empty.")

    if process_id in _REGISTRY:
        raise ValueError(
            f"Matrix-element process already registered: {process_id}"
        )

    _REGISTRY[process_id] = MatrixElementProcess(
        process_id=process_id,
        name=name,
        theory=theory,
        evaluator=evaluator,
        status=status,
        scientific_scope=scientific_scope,
    )


def get_matrix_element_process(
    process_id: str,
) -> MatrixElementProcess:
    try:
        return _REGISTRY[process_id]
    except KeyError as exc:
        raise ValueError(
            f"Unknown matrix-element process: {process_id}"
        ) from exc


def list_matrix_element_processes() -> tuple[MatrixElementProcess, ...]:
    return tuple(_REGISTRY.values())


def evaluate_matrix_element(
    process_id: str,
    *args,
    **kwargs,
) -> Any:
    process = get_matrix_element_process(process_id)

    if process.evaluator is None:
        raise ValueError(
            f"No numerical matrix-element evaluator is registered "
            f"for process: {process_id}"
        )

    return process.evaluator(*args, **kwargs)


def matrix_element_registry_summary() -> dict:
    processes = list_matrix_element_processes()

    by_theory: dict[str, int] = {}
    by_status: dict[str, int] = {}

    for process in processes:
        by_theory[process.theory] = (
            by_theory.get(process.theory, 0) + 1
        )
        by_status[process.status] = (
            by_status.get(process.status, 0) + 1
        )

    return {
        "success": True,
        "process_count": len(processes),
        "processes": [
            {
                "process_id": process.process_id,
                "name": process.name,
                "theory": process.theory,
                "status": process.status,
                "evaluator_available": process.evaluator is not None,
            }
            for process in processes
        ],
        "by_theory": by_theory,
        "by_status": by_status,
    }
