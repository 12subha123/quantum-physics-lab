import sympy as sp


def euler_lagrange_equation(
    lagrangian,
    field,
    coordinates,
):
    """
    Calculate the Euler-Lagrange equation for a classical field.

    For a field phi(x):
        dL/dphi - d_mu[dL/d(d_mu phi)] = 0

    coordinates should contain the spacetime coordinates,
    for example [t, x, y, z].
    """

    lagrangian = sp.sympify(lagrangian)
    field = sp.sympify(field)

    equation = sp.diff(lagrangian, field)

    for coordinate in coordinates:
        derivative = sp.diff(
            lagrangian,
            sp.diff(field, coordinate),
        )

        equation -= sp.diff(
            derivative,
            coordinate,
        )

    return sp.simplify(equation)


def scalar_field_lagrangian(
    field,
    mass,
    kinetic_coefficient=sp.Rational(1, 2),
    mass_coefficient=sp.Rational(1, 2),
):
    """
    Construct the Lagrangian density for a real scalar field
    in a simplified 1+1-dimensional representation:

        L = 1/2 (d_t phi)^2
            - 1/2 (d_x phi)^2
            - 1/2 m^2 phi^2

    This is an educational field-theory representation.
    """

    field = sp.sympify(field)
    mass = sp.sympify(mass)

    time_derivative = sp.Derivative(field, sp.Symbol("t"))
    space_derivative = sp.Derivative(field, sp.Symbol("x"))

    return sp.expand(
        kinetic_coefficient * time_derivative**2
        - kinetic_coefficient * space_derivative**2
        - mass_coefficient * mass**2 * field**2
    )


def klein_gordon_equation(
    field,
    mass,
    time_symbol=None,
    space_symbol=None,
):
    """
    Return the symbolic Klein-Gordon equation in 1+1 dimensions:

        d²phi/dt² - d²phi/dx² + m² phi = 0
    """

    field = sp.sympify(field)
    mass = sp.sympify(mass)

    if time_symbol is None:
        time_symbol = sp.Symbol("t")

    if space_symbol is None:
        space_symbol = sp.Symbol("x")

    equation = (
        sp.diff(field, time_symbol, 2)
        - sp.diff(field, space_symbol, 2)
        + mass**2 * field
    )

    return sp.simplify(equation)