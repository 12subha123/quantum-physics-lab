from dataclasses import dataclass
from math import pi

import quantum.field_theory.register_matrix_elements  # noqa: F401

from quantum.field_theory.matrix_element_registry import (
    evaluate_matrix_element,
)
from quantum.field_theory.observable_process_registry import (
    get_observable_process,
)
from quantum.field_theory.qcd_angular_observables import (
    integrate_qcd_angular_cross_section,
)


@dataclass(frozen=True)
class ObservableEvaluation:
    success: bool
    process_id: str
    process: str
    theory: str
    observable_type: str
    valid: bool
    matrix_element_available: bool
    phase_space_valid: bool
    matrix_element_squared: float | None
    total_cross_section: float | None
    errors: tuple[str, ...]
    scientific_scope: str


def _qed_cross_section(
    ms_squared: float,
    s: float,
) -> float:
    return ms_squared / (16.0 * pi * s)


def evaluate_observable_process(
    process_id: str,
    sqrt_s: float = 10.0,
    alpha_s: float = 0.118,
    angular_cut: float = 0.1,
    angular_points: int = 200,
) -> ObservableEvaluation:

    if sqrt_s <= 0.0:
        return ObservableEvaluation(
            success=True,
            process_id=process_id,
            process="",
            theory="",
            observable_type="",
            valid=False,
            matrix_element_available=False,
            phase_space_valid=False,
            matrix_element_squared=None,
            total_cross_section=None,
            errors=("sqrt_s must be positive.",),
            scientific_scope="",
        )

    process = get_observable_process(process_id)

    if process is None:
        return ObservableEvaluation(
            success=True,
            process_id=process_id,
            process="",
            theory="",
            observable_type="",
            valid=False,
            matrix_element_available=False,
            phase_space_valid=False,
            matrix_element_squared=None,
            total_cross_section=None,
            errors=("Unknown observable process.",),
            scientific_scope="",
        )

    if process.observable_type != "2_to_2_cross_section":
        return ObservableEvaluation(
            success=True,
            process_id=process_id,
            process=process.name,
            theory=process.theory,
            observable_type=process.observable_type,
            valid=False,
            matrix_element_available=False,
            phase_space_valid=False,
            matrix_element_squared=None,
            total_cross_section=None,
            errors=(
                "This observable type is registered but "
                "its numerical evaluator is not yet implemented.",
            ),
            scientific_scope=process.scientific_scope,
        )

    s = sqrt_s * sqrt_s

    # ---------------------------------------------------------
    # QED
    # ---------------------------------------------------------
    if process.theory == "QED":

        t = -0.5 * s
        u = -0.5 * s

        result = evaluate_matrix_element(
            process_id,
            s,
            t,
            u,
        )

        if not getattr(result, "valid", False):
            return ObservableEvaluation(
                success=True,
                process_id=process_id,
                process=process.name,
                theory=process.theory,
                observable_type=process.observable_type,
                valid=False,
                matrix_element_available=True,
                phase_space_valid=True,
                matrix_element_squared=getattr(
                    result,
                    "ms_squared",
                    None,
                ),
                total_cross_section=None,
                errors=getattr(result, "errors", ()),
                scientific_scope=process.scientific_scope,
            )

        ms_squared = result.ms_squared

        if ms_squared is None:
            return ObservableEvaluation(
                success=True,
                process_id=process_id,
                process=process.name,
                theory=process.theory,
                observable_type=process.observable_type,
                valid=False,
                matrix_element_available=True,
                phase_space_valid=True,
                matrix_element_squared=None,
                total_cross_section=None,
                errors=("Matrix element returned no numerical value.",),
                scientific_scope=process.scientific_scope,
            )

        sigma = _qed_cross_section(
            ms_squared,
            s,
        )

        return ObservableEvaluation(
            success=True,
            process_id=process_id,
            process=process.name,
            theory=process.theory,
            observable_type=process.observable_type,
            valid=True,
            matrix_element_available=True,
            phase_space_valid=True,
            matrix_element_squared=ms_squared,
            total_cross_section=sigma,
            errors=(),
            scientific_scope=(
                process.scientific_scope
                + " The current QED total cross section "
                  "uses the existing angle-independent "
                  "regression observable."
            ),
        )

    # ---------------------------------------------------------
    # QCD
    # ---------------------------------------------------------
    if process.theory == "QCD":

        if alpha_s <= 0.0:
            return ObservableEvaluation(
                success=True,
                process_id=process_id,
                process=process.name,
                theory=process.theory,
                observable_type=process.observable_type,
                valid=False,
                matrix_element_available=True,
                phase_space_valid=False,
                matrix_element_squared=None,
                total_cross_section=None,
                errors=("alpha_s must be positive.",),
                scientific_scope=process.scientific_scope,
            )

        angular_result = integrate_qcd_angular_cross_section(
            sqrt_s=sqrt_s,
            alpha_s=alpha_s,
            angular_cut=angular_cut,
            points=angular_points,
        )

        if not angular_result.valid:
            return ObservableEvaluation(
                success=True,
                process_id=process_id,
                process=process.name,
                theory=process.theory,
                observable_type=process.observable_type,
                valid=False,
                matrix_element_available=True,
                phase_space_valid=True,
                matrix_element_squared=None,
                total_cross_section=None,
                errors=angular_result.errors,
                scientific_scope=angular_result.scientific_scope,
            )

        # Evaluate the symmetric point as a representative
        # matrix-element value for the summary.
        central = evaluate_matrix_element(
            process_id,
            s,
            -0.5 * s,
            -0.5 * s,
            alpha_s,
        )

        return ObservableEvaluation(
            success=True,
            process_id=process_id,
            process=process.name,
            theory=process.theory,
            observable_type=process.observable_type,
            valid=True,
            matrix_element_available=True,
            phase_space_valid=True,
            matrix_element_squared=getattr(
                central,
                "ms_squared",
                None,
            ),
            total_cross_section=angular_result.total_cross_section,
            errors=(),
            scientific_scope=(
                angular_result.scientific_scope
                + " The reported total cross section is "
                  "numerically integrated over solid angle "
                  "with the supplied angular cut."
            ),
        )

    # ---------------------------------------------------------
    # Future theories
    # ---------------------------------------------------------

    return ObservableEvaluation(
        success=True,
        process_id=process_id,
        process=process.name,
        theory=process.theory,
        observable_type=process.observable_type,
        valid=False,
        matrix_element_available=False,
        phase_space_valid=False,
        matrix_element_squared=None,
        total_cross_section=None,
        errors=(
            "A numerical matrix-element/observable evaluator "
            "is not yet registered for this theory/process.",
        ),
        scientific_scope=process.scientific_scope,
    )


def observable_evaluation_summary(
    process_id: str,
    sqrt_s: float = 10.0,
    alpha_s: float = 0.118,
    angular_cut: float = 0.1,
    angular_points: int = 200,
) -> dict:

    result = evaluate_observable_process(
        process_id=process_id,
        sqrt_s=sqrt_s,
        alpha_s=alpha_s,
        angular_cut=angular_cut,
        angular_points=angular_points,
    )

    return {
        "success": result.success,
        "process_id": result.process_id,
        "process": result.process,
        "theory": result.theory,
        "observable_type": result.observable_type,
        "valid": result.valid,
        "matrix_element_available": result.matrix_element_available,
        "phase_space_valid": result.phase_space_valid,
        "matrix_element_squared": result.matrix_element_squared,
        "total_cross_section": result.total_cross_section,
        "errors": list(result.errors),
        "scientific_scope": result.scientific_scope,
    }
