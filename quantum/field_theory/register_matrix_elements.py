from quantum.field_theory.matrix_element_registry import (
    register_matrix_element_process,
)
from quantum.field_theory.matrix_element import (
    electron_muon_annihilation,
)
from quantum.field_theory.qcd_matrix_element import (
    qcd_qqbar_to_gg_matrix_element,
)


def register_default_matrix_elements() -> None:
    register_matrix_element_process(
        process_id="qed_electron_muon_annihilation",
        name="e- + e+ -> mu- + mu+",
        theory="QED",
        evaluator=electron_muon_annihilation,
        status="implemented",
        scientific_scope=(
            "Tree-level massless QED. "
            "Spin-summed and initial-spin-averaged."
        ),
    )

    register_matrix_element_process(
        process_id="qcd_quark_antiquark_to_gluons",
        name="q + anti-q -> g + g",
        theory="QCD",
        evaluator=qcd_qqbar_to_gg_matrix_element,
        status="implemented",
        scientific_scope=(
            "Tree-level massless QCD. "
            "Spin-averaged and color-averaged initial state. "
            "No loop corrections or hadronization."
        ),
    )


register_default_matrix_elements()
