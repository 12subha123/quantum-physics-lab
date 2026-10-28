from dataclasses import dataclass


FERMION_ANTIFERMION_PAIRS = {
    "electron": "positron",
    "muon": "antimuon",
    "tau": "antitau",
    "up": "anti-up",
    "down": "anti-down",
    "strange": "anti-strange",
    "charm": "anti-charm",
    "top": "anti-top",
    "bottom": "anti-bottom",
}

FERMIONS = set(FERMION_ANTIFERMION_PAIRS)
ANTIFERMIONS = set(FERMION_ANTIFERMION_PAIRS.values())
PHOTONS = {"photon"}


@dataclass(frozen=True)
class PhysicalVertexValidation:
    valid: bool
    diagram_id: str
    process: str
    topology: str
    checked_vertices: int
    errors: tuple[str, ...]


def _normalise(name: str) -> str:
    return str(name).strip().lower().replace("_", "-")


def _is_fermion(name: str) -> bool:
    return _normalise(name) in FERMIONS


def _is_antifermion(name: str) -> bool:
    return _normalise(name) in ANTIFERMIONS


def _is_photon(name: str) -> bool:
    return _normalise(name) in PHOTONS


def _base_fermion(name: str) -> str | None:
    name = _normalise(name)

    if name in FERMIONS:
        return name

    for fermion, antifermion in FERMION_ANTIFERMION_PAIRS.items():
        if name == antifermion:
            return fermion

    return None


def _external_particle(leg) -> str:
    if isinstance(leg, dict):
        return _normalise(leg.get("particle", ""))

    return _normalise(getattr(leg, "particle", ""))


def _internal_particle(line) -> str:
    if isinstance(line, dict):
        return _normalise(line.get("particle", ""))

    return _normalise(getattr(line, "particle", ""))


def _connected_particles(diagram, vertex) -> list[str]:
    if isinstance(vertex, dict):
        external_ids = tuple(vertex.get("external_legs", ()))
        internal_ids = tuple(vertex.get("internal_lines", ()))
    else:
        external_ids = tuple(getattr(vertex, "external_legs", ()))
        internal_ids = tuple(getattr(vertex, "internal_lines", ()))

    external_by_id = {}

    for leg in getattr(diagram, "external_legs", ()):
        leg_id = (
            leg.get("leg_id", "")
            if isinstance(leg, dict)
            else getattr(leg, "leg_id", "")
        )
        external_by_id[leg_id] = _external_particle(leg)

    internal_by_id = {}

    for line in getattr(diagram, "internal_lines", ()):
        line_id = (
            line.get("line_id", "")
            if isinstance(line, dict)
            else getattr(line, "line_id", "")
        )
        internal_by_id[line_id] = _internal_particle(line)

    particles = []

    for leg_id in external_ids:
        if leg_id in external_by_id:
            particles.append(external_by_id[leg_id])

    for line_id in internal_ids:
        if line_id in internal_by_id:
            particles.append(internal_by_id[line_id])

    return particles


def _validate_qed_vertex(
    vertex_particles: list[str],
    vertex_id: str,
) -> list[str]:
    """
    Validate local QED field content.

    A QED vertex has:
        photon + charged fermion line + charged fermion line.

    The two fermionic fields may represent:

    1. fermion + corresponding antifermion
       Example: electron + positron + photon

    2. fermion-line continuation
       Example: muon + muon + photon

    3. antifermion-line continuation
       Example: antimuon + antimuon + photon

    The distinction between incoming/outgoing particle and
    antiparticle is handled later by explicit fermion-flow/
    arrow-direction validation.
    """

    errors = []

    if len(vertex_particles) != 3:
        errors.append(
            f"{vertex_id}: QED vertex must contain exactly "
            f"three connected fields."
        )
        return errors

    photons = [
        particle
        for particle in vertex_particles
        if _is_photon(particle)
    ]

    fermion_fields = [
        particle
        for particle in vertex_particles
        if _is_fermion(particle) or _is_antifermion(particle)
    ]

    if len(photons) != 1:
        errors.append(
            f"{vertex_id}: QED vertex requires exactly one photon."
        )

    if len(fermion_fields) != 2:
        errors.append(
            f"{vertex_id}: QED vertex requires exactly two "
            f"charged-fermion fields."
        )
        return errors

    first_base = _base_fermion(fermion_fields[0])
    second_base = _base_fermion(fermion_fields[1])

    if first_base is None or second_base is None:
        errors.append(
            f"{vertex_id}: unsupported charged-fermion field."
        )
        return errors

    if first_base != second_base:
        errors.append(
            f"{vertex_id}: fermion-line flavor mismatch: "
            f"{fermion_fields[0]}, {fermion_fields[1]}."
        )

    return errors


def _validate_internal_line_continuity(diagram) -> list[str]:
    errors = []

    vertices = getattr(diagram, "vertices", ())
    internal_lines = getattr(diagram, "internal_lines", ())

    vertex_by_id = {}

    for vertex in vertices:
        vertex_id = (
            vertex.get("vertex_id", "")
            if isinstance(vertex, dict)
            else getattr(vertex, "vertex_id", "")
        )
        vertex_by_id[vertex_id] = vertex

    for line in internal_lines:
        if isinstance(line, dict):
            line_id = line.get("line_id", "")
            particle = _normalise(line.get("particle", ""))
            from_vertex = line.get("from_vertex", "")
            to_vertex = line.get("to_vertex", "")
        else:
            line_id = getattr(line, "line_id", "")
            particle = _normalise(getattr(line, "particle", ""))
            from_vertex = getattr(line, "from_vertex", "")
            to_vertex = getattr(line, "to_vertex", "")

        if from_vertex not in vertex_by_id:
            errors.append(
                f"{line_id}: missing source vertex {from_vertex}."
            )
            continue

        if to_vertex not in vertex_by_id:
            errors.append(
                f"{line_id}: missing destination vertex {to_vertex}."
            )
            continue

        from_particles = _connected_particles(
            diagram,
            vertex_by_id[from_vertex],
        )

        to_particles = _connected_particles(
            diagram,
            vertex_by_id[to_vertex],
        )

        if _is_photon(particle):
            if not any(_is_photon(p) for p in from_particles):
                errors.append(
                    f"{line_id}: internal photon is not connected "
                    f"to a photon field at {from_vertex}."
                )

            if not any(_is_photon(p) for p in to_particles):
                errors.append(
                    f"{line_id}: internal photon is not connected "
                    f"to a photon field at {to_vertex}."
                )

            continue

        base_particle = _base_fermion(particle)

        if base_particle is None:
            errors.append(
                f"{line_id}: unsupported internal particle "
                f"'{particle}'."
            )
            continue

        from_bases = {
            _base_fermion(p)
            for p in from_particles
            if _is_fermion(p) or _is_antifermion(p)
        }

        to_bases = {
            _base_fermion(p)
            for p in to_particles
            if _is_fermion(p) or _is_antifermion(p)
        }

        if base_particle not in from_bases:
            errors.append(
                f"{line_id}: fermion flavor '{base_particle}' "
                f"is absent at {from_vertex}."
            )

        if base_particle not in to_bases:
            errors.append(
                f"{line_id}: fermion flavor '{base_particle}' "
                f"is absent at {to_vertex}."
            )

    return errors


def validate_physical_vertices(diagram) -> PhysicalVertexValidation:
    diagram_id = getattr(diagram, "diagram_id", "")
    process = getattr(diagram, "process", "")
    topology = getattr(diagram, "topology", "")
    vertices = getattr(diagram, "vertices", ())

    errors = []

    for vertex in vertices:
        vertex_id = (
            vertex.get("vertex_id", "")
            if isinstance(vertex, dict)
            else getattr(vertex, "vertex_id", "")
        )

        interaction = (
            vertex.get("interaction", "")
            if isinstance(vertex, dict)
            else getattr(vertex, "interaction", "")
        )

        particles = _connected_particles(diagram, vertex)

        if interaction == "qed_fermion_photon":
            errors.extend(
                _validate_qed_vertex(
                    particles,
                    vertex_id,
                )
            )

    errors.extend(
        _validate_internal_line_continuity(diagram)
    )

    return PhysicalVertexValidation(
        valid=not errors,
        diagram_id=diagram_id,
        process=process,
        topology=topology,
        checked_vertices=len(vertices),
        errors=tuple(errors),
    )


def validate_diagrams(diagrams) -> list[PhysicalVertexValidation]:
    return [
        validate_physical_vertices(diagram)
        for diagram in diagrams
    ]


def physical_vertex_validation_summary(diagrams) -> dict:
    validations = validate_diagrams(diagrams)

    valid_count = sum(
        1
        for validation in validations
        if validation.valid
    )

    invalid_count = len(validations) - valid_count

    return {
        "valid": invalid_count == 0,
        "valid_count": valid_count,
        "invalid_count": invalid_count,
        "validations": [
            {
                "valid": validation.valid,
                "diagram_id": validation.diagram_id,
                "process": validation.process,
                "topology": validation.topology,
                "checked_vertices": validation.checked_vertices,
                "errors": list(validation.errors),
            }
            for validation in validations
        ],
        "scientific_scope": (
            "Local QED field-content validation. "
            "Checks photon connectivity, charged-fermion "
            "flavor continuity, and internal-line continuity. "
            "Explicit fermion-arrow orientation, momentum "
            "conservation, spinor algebra, gauge invariance, "
            "loops, and renormalization are handled by later "
            "validation and amplitude layers."
        ),
    }
