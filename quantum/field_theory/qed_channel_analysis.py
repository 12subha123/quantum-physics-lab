import math


ALPHA_EM = 1.0 / 137.035999084
E_CHARGE = math.sqrt(4.0 * math.pi * ALPHA_EM)


def _validate(process, sqrt_s, theta):
    allowed = {
        "electron_muon_annihilation",
        "bhabha",
        "moller",
    }

    if process not in allowed:
        raise ValueError(
            "Unsupported QED process. Supported processes are: "
            "electron_muon_annihilation, bhabha, moller."
        )

    if sqrt_s <= 0:
        raise ValueError("Center-of-mass energy must be positive.")

    if theta <= 0 or theta >= math.pi:
        raise ValueError(
            "Scattering angle must be strictly between 0 and pi radians."
        )


def _mandelstam(sqrt_s, theta):
    s = sqrt_s ** 2

    half_angle = theta / 2.0
    cos_half = math.cos(half_angle)
    sin_half = math.sin(half_angle)

    t = -s * sin_half ** 2
    u = -s * cos_half ** 2

    return s, t, u


def analyze_qed_channels(
    process,
    sqrt_s=10.0,
    scattering_angle=math.pi / 2.0,
):
    _validate(
        process,
        sqrt_s,
        scattering_angle,
    )

    s, t, u = _mandelstam(
        sqrt_s,
        scattering_angle,
    )

    e = E_CHARGE
    e4 = e ** 4

    if process == "electron_muon_annihilation":
        ms_squared = 2.0 * e4 * (
            (u ** 2 + t ** 2) / s ** 2
        )

        mt_squared = 0.0
        mu_squared = 0.0
        interference = 0.0

        total_squared = ms_squared

        channels = {
            "s": {
                "amplitude": "M_s",
                "squared": ms_squared,
                "description": (
                    "s-channel virtual-photon annihilation"
                ),
            }
        }

    elif process == "bhabha":
        ms_squared = 2.0 * e4 * (
            (u ** 2 + t ** 2) / s ** 2
        )

        mt_squared = 2.0 * e4 * (
            (u ** 2 + s ** 2) / t ** 2
        )

        interference = 4.0 * e4 * (
            u ** 2 / (s * t)
        )

        mu_squared = 0.0
        total_squared = (
            ms_squared
            + mt_squared
            + interference
        )

        channels = {
            "s": {
                "amplitude": "M_s",
                "squared": ms_squared,
                "description": (
                    "s-channel annihilation contribution"
                ),
            },
            "t": {
                "amplitude": "M_t",
                "squared": mt_squared,
                "description": (
                    "t-channel photon-exchange contribution"
                ),
            },
        }

    elif process == "moller":
        mt_squared = 2.0 * e4 * (
            (s ** 2 + u ** 2) / t ** 2
        )

        mu_squared = 2.0 * e4 * (
            (s ** 2 + t ** 2) / u ** 2
        )

        interference = 4.0 * e4 * (
            s ** 2 / (t * u)
        )

        ms_squared = 0.0

        total_squared = (
            mt_squared
            + mu_squared
            + interference
        )

        channels = {
            "t": {
                "amplitude": "M_t",
                "squared": mt_squared,
                "description": (
                    "t-channel photon exchange"
                ),
            },
            "u": {
                "amplitude": "M_u",
                "squared": mu_squared,
                "description": (
                    "u-channel exchange from identical-fermion crossing"
                ),
            },
        }

    return {
        "success": True,
        "model": (
            "Tree-level QED channel decomposition "
            "with spin-summed, initial-spin-averaged amplitudes"
        ),
        "process": process,
        "units": "Natural units: hbar = c = 1",
        "kinematics": {
            "sqrt_s": sqrt_s,
            "theta_radians": scattering_angle,
            "theta_degrees": math.degrees(scattering_angle),
            "s": s,
            "t": t,
            "u": u,
        },
        "coupling": {
            "alpha_em": ALPHA_EM,
            "electric_charge": e,
        },
        "channels": channels,
        "channel_squared_amplitudes": {
            "s": ms_squared,
            "t": mt_squared,
            "u": mu_squared,
        },
        "interference": {
            "value": interference,
            "present": abs(interference) > 0.0,
        },
        "total": {
            "squared_amplitude": total_squared,
            "formula": (
                "|M_total|^2 = sum(|M_i|^2) + "
                "interference terms"
            ),
        },
        "scientific_scope": [
            "Tree-level QED only.",
            "Massless external-particle approximation.",
            "Spin-summed and initial-spin-averaged result.",
            "No loop corrections.",
            "No renormalization.",
            "No radiative corrections.",
            "This is an educational perturbative calculation.",
        ],
    }
