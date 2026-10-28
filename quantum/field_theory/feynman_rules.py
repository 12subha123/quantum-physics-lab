import cmath
import math


def phi4_vertex(lam):
    """
    Four-scalar vertex for real scalar phi^4 theory.

    L_int = -lambda / 4! * phi^4

    Feynman vertex factor:
        -i * lambda
    """
    if lam < 0:
        raise ValueError("Lambda must be non-negative.")

    vertex = complex(0.0, -lam)

    return {
        "type": "phi4_four_scalar_vertex",
        "coupling": lam,
        "vertex_factor": {
            "real": vertex.real,
            "imaginary": vertex.imag,
            "magnitude": abs(vertex),
            "phase": cmath.phase(vertex),
        },
        "formula": "-i lambda",
        "interaction_lagrangian": "-lambda/4! * phi^4",
        "number_of_external_legs": 4,
        "particle_type": "real scalar",
    }


def phi4_tree_level_2_to_2(lam):
    """
    Educational tree-level 2 -> 2 scattering in phi^4 theory.

    At lowest order there is one contact vertex, so
        M = -i lambda.
    """
    vertex = phi4_vertex(lam)

    return {
        "success": True,
        "model": "Real scalar phi^4 theory",
        "approximation": "Tree level",
        "process": "phi + phi -> phi + phi",
        "interaction": {
            "lagrangian": "-lambda/4! * phi^4",
            "coupling": lam,
        },
        "diagrams": [
            {
                "name": "contact",
                "vertices": 1,
                "internal_propagators": 0,
                "external_legs": 4,
            }
        ],
        "amplitude": vertex["vertex_factor"],
        "amplitude_formula": "M = -i lambda",
        "interpretation": [
            "The lowest-order 2-to-2 process is a single four-point contact interaction.",
            "There are four external scalar legs attached to one phi^4 vertex.",
            "At tree level the invariant amplitude is -i lambda.",
            "Loop corrections, renormalization, and higher-order diagrams are not included.",
        ],
    }


def interaction_summary(lam=1.0):
    if lam < 0:
        raise ValueError("Lambda must be non-negative.")

    vertex = phi4_vertex(lam)
    scattering = phi4_tree_level_2_to_2(lam)

    return {
        "success": True,
        "model": "Real scalar phi^4 quantum field theory",
        "units": "Natural units: hbar = c = 1",
        "interaction_lagrangian": "-lambda/4! * phi^4",
        "coupling_constant": lam,
        "vertex": vertex,
        "tree_level_scattering": scattering,
        "feynman_rule": {
            "vertex": "Four scalar lines meet at one vertex.",
            "factor": "-i lambda",
        },
        "limitations": [
            "Educational perturbative implementation.",
            "Tree-level calculations only.",
            "No loop integrals or renormalization.",
            "No momentum-conserving delta function is evaluated numerically here.",
            "This module is not a replacement for a research-grade symbolic QFT package.",
        ],
    }
