import math


ALPHA_EM = 1.0 / 137.035999084
E_CHARGE = math.sqrt(4.0 * math.pi * ALPHA_EM)


def _validate(process, sqrt_s, scattering_angle):
    supported = {
        "electron_muon_annihilation",
        "bhabha",
        "moller",
    }

    if process not in supported:
        raise ValueError(
            "Unsupported process. Use electron_muon_annihilation, "
            "bhabha, or moller."
        )

    if sqrt_s <= 0:
        raise ValueError("Center-of-mass energy must be positive.")

    if scattering_angle <= 0 or scattering_angle >= math.pi:
        raise ValueError(
            "Scattering angle must be strictly between 0 and pi radians."
        )


def _mandelstam_massless(sqrt_s, theta):
    s = sqrt_s ** 2
    half = theta / 2.0

    # Massless 2 -> 2 center-of-mass kinematics.
    t = -0.5 * s * (1.0 - math.cos(theta))
    u = -0.5 * s * (1.0 + math.cos(theta))

    return s, t, u


def _qed_coupling():
    return E_CHARGE


def _annihilation_amplitude_squared(s, t, u):
    e = _qed_coupling()

    # Spin-averaged tree-level massless QED result:
    #
    # |M|^2 = 2 e^4 (u^2 + t^2) / s^2
    return 2.0 * e**4 * (u**2 + t**2) / s**2


def _bhabha_amplitude_squared(s, t, u):
    e = _qed_coupling()

    # Spin-averaged tree-level massless QED result:
    #
    # |M|^2 =
    # 2 e^4 [
    #   (u^2+t^2)/s^2
    #   + (u^2+s^2)/t^2
    #   + 2u^2/(s t)
    # ]
    #
    # The final term is the s/t interference contribution.
    s_channel = (u**2 + t**2) / s**2
    t_channel = (u**2 + s**2) / t**2
    interference = 2.0 * u**2 / (s * t)

    return {
        "s_channel": 2.0 * e**4 * s_channel,
        "t_channel": 2.0 * e**4 * t_channel,
        "interference": 2.0 * e**4 * interference,
        "total": 2.0 * e**4 * (
            s_channel + t_channel + interference
        ),
    }


def _moller_amplitude_squared(s, t, u):
    e = _qed_coupling()

    # Spin-averaged tree-level massless QED result:
    #
    # |M|^2 =
    # 2 e^4 [
    #   (s^2+u^2)/t^2
    #   + (s^2+t^2)/u^2
    #   + 2s^2/(t u)
    # ]
    #
    # The final term is the t/u interference contribution.
    t_channel = (s**2 + u**2) / t**2
    u_channel = (s**2 + t**2) / u**2
    interference = 2.0 * s**2 / (t * u)

    return {
        "t_channel": 2.0 * e**4 * t_channel,
        "u_channel": 2.0 * e**4 * u_channel,
        "interference": 2.0 * e**4 * interference,
        "total": 2.0 * e**4 * (
            t_channel + u_channel + interference
        ),
    }


def _cross_section(
    amplitude_squared,
    s,
    identical_final_state=False,
):
    # Massless 2 -> 2 CM relation:
    #
    # d sigma/d Omega = |M|^2 / (64 pi^2 s)
    #
    # Include 1/2 for identical final-state particles.
    factor = 0.5 if identical_final_state else 1.0

    differential = (
        factor * amplitude_squared /
        (64.0 * math.pi**2 * s)
    )

    return differential


def calculate_qed_amplitude(
    process,
    sqrt_s=10.0,
    scattering_angle=math.pi / 2.0,
):
    _validate(
        process=process,
        sqrt_s=sqrt_s,
        scattering_angle=scattering_angle,
    )

    s, t, u = _mandelstam_massless(
        sqrt_s=sqrt_s,
        theta=scattering_angle,
    )

    if process == "electron_muon_annihilation":
        total_squared = _annihilation_amplitude_squared(
            s=s,
            t=t,
            u=u,
        )

        differential = _cross_section(
            amplitude_squared=total_squared,
            s=s,
            identical_final_state=False,
        )

        channels = {
            "s": {
                "diagram": "s-channel photon exchange",
                "amplitude_structure": "M_s ∝ 1/s",
                "spin_averaged_squared": total_squared,
            }
        }

        interference = 0.0

        process_label = (
            "e⁻ + e⁺ → μ⁻ + μ⁺"
        )

    elif process == "bhabha":
        values = _bhabha_amplitude_squared(
            s=s,
            t=t,
            u=u,
        )

        total_squared = values["total"]

        differential = _cross_section(
            amplitude_squared=total_squared,
            s=s,
            identical_final_state=False,
        )

        channels = {
            "s": {
                "diagram": "s-channel photon exchange",
                "amplitude_structure": "M_s ∝ 1/s",
                "spin_averaged_squared": values["s_channel"],
            },
            "t": {
                "diagram": "t-channel photon exchange",
                "amplitude_structure": "M_t ∝ 1/t",
                "spin_averaged_squared": values["t_channel"],
            },
        }

        interference = values["interference"]

        process_label = (
            "e⁻ + e⁺ → e⁻ + e⁺"
        )

    else:
        values = _moller_amplitude_squared(
            s=s,
            t=t,
            u=u,
        )

        total_squared = values["total"]

        differential = _cross_section(
            amplitude_squared=total_squared,
            s=s,
            identical_final_state=True,
        )

        channels = {
            "t": {
                "diagram": "t-channel photon exchange",
                "amplitude_structure": "M_t ∝ 1/t",
                "spin_averaged_squared": values["t_channel"],
            },
            "u": {
                "diagram": "u-channel photon exchange",
                "amplitude_structure": "M_u ∝ 1/u",
                "spin_averaged_squared": values["u_channel"],
            },
        }

        interference = values["interference"]

        process_label = (
            "e⁻ + e⁻ → e⁻ + e⁻"
        )

    return {
        "success": True,
        "model": (
            "Tree-level massless QED, spin-summed and "
            "initial-spin averaged"
        ),
        "process": process_label,
        "process_key": process,
        "coupling": {
            "alpha_em": ALPHA_EM,
            "electric_charge": E_CHARGE,
        },
        "kinematics": {
            "sqrt_s": sqrt_s,
            "s": s,
            "t": t,
            "u": u,
            "scattering_angle_radians": scattering_angle,
            "scattering_angle_degrees": (
                math.degrees(scattering_angle)
            ),
        },
        "diagrams": channels,
        "amplitude": {
            "interference_contribution": interference,
            "spin_averaged_total_squared": total_squared,
            "interpretation": (
                "The total result contains the contributions "
                "from all generated tree-level diagrams and "
                "their interference."
            ),
        },
        "cross_section": {
            "differential_cross_section": differential,
            "formula": (
                "dσ/dΩ = |M|²/(64π²s), with a 1/2 "
                "identical-final-state factor for Møller scattering."
            ),
        },
        "limitations": [
            "Tree-level QED only.",
            "Massless kinematic approximation.",
            "Spin-summed and initial-spin averaged result.",
            "No loop corrections.",
            "No renormalization.",
            "No full helicity-amplitude construction yet.",
            "No soft/collinear radiation corrections.",
            "Cross sections are expressed in natural units.",
        ],
    }


def calculate_qed_angular_scan(
    process,
    sqrt_s=10.0,
    points=91,
):
    if points < 8 or points > 721:
        raise ValueError("Points must be between 8 and 721.")

    theta_min = math.pi / (points * 10.0)
    theta_max = math.pi - theta_min

    data = []

    for index in range(points):
        theta = theta_min + (
            theta_max - theta_min
        ) * index / (points - 1)

        result = calculate_qed_amplitude(
            process=process,
            sqrt_s=sqrt_s,
            scattering_angle=theta,
        )

        cross_section = result["cross_section"]

        differential_value = cross_section.get(
            "differential_value",
            cross_section.get("differential_cross_section"),
        )

        if differential_value is None:
            raise ValueError(
                "QED amplitude result does not contain a differential cross section."
            )

        data.append(
            {
                "theta_radians": theta,
                "theta_degrees": math.degrees(theta),
                "differential_cross_section": differential_value,
            }
        )

    return {
        "success": True,
        "process": process,
        "sqrt_s": sqrt_s,
        "points": points,
        "angular_distribution": data,
        "note": (
            "Exact 0? and 180? endpoints are excluded because "
            "massless tree-level QED expressions can become singular."
        ),
    }
