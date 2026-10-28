import math


# SI constants
HBAR = 1.054571817e-34      # Reduced Planck constant (J·s)
ELECTRON_VOLT = 1.602176634e-19  # 1 eV in joules


def joules_to_ev(energy_joules):
    """Convert energy from joules to electronvolts."""
    return energy_joules / ELECTRON_VOLT


def ev_to_joules(energy_ev):
    """Convert energy from electronvolts to joules."""
    return energy_ev * ELECTRON_VOLT
