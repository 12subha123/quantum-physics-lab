from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(frozen=True)
class Particle:
    name: str
    symbol: str
    antiparticle: str
    category: str
    mass_gev: float
    electric_charge: float
    spin: float
    color_charge: str
    is_elementary: bool
    composition: Optional[str] = None


PARTICLES = {
    "electron": Particle(
        name="Electron",
        symbol="e-",
        antiparticle="positron",
        category="lepton",
        mass_gev=0.000510999,
        electric_charge=-1.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=True,
    ),
    "positron": Particle(
        name="Positron",
        symbol="e+",
        antiparticle="electron",
        category="lepton",
        mass_gev=0.000510999,
        electric_charge=1.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=True,
    ),
    "muon": Particle(
        name="Muon",
        symbol="mu-",
        antiparticle="antimuon",
        category="lepton",
        mass_gev=0.105658,
        electric_charge=-1.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=True,
    ),
    "antimuon": Particle(
        name="Antimuon",
        symbol="mu+",
        antiparticle="muon",
        category="lepton",
        mass_gev=0.105658,
        electric_charge=1.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=True,
    ),
    "tau": Particle(
        name="Tau",
        symbol="tau-",
        antiparticle="antitau",
        category="lepton",
        mass_gev=1.77686,
        electric_charge=-1.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=True,
    ),
    "antitau": Particle(
        name="Antitau",
        symbol="tau+",
        antiparticle="tau",
        category="lepton",
        mass_gev=1.77686,
        electric_charge=1.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=True,
    ),
    "electron_neutrino": Particle(
        name="Electron neutrino",
        symbol="nu_e",
        antiparticle="electron_antineutrino",
        category="neutrino",
        mass_gev=0.0,
        electric_charge=0.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=True,
    ),
    "electron_antineutrino": Particle(
        name="Electron antineutrino",
        symbol="anti-nu_e",
        antiparticle="electron_neutrino",
        category="neutrino",
        mass_gev=0.0,
        electric_charge=0.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=True,
    ),
    "up_quark": Particle(
        name="Up quark",
        symbol="u",
        antiparticle="anti_up_quark",
        category="quark",
        mass_gev=0.0022,
        electric_charge=2.0 / 3.0,
        spin=0.5,
        color_charge="triplet",
        is_elementary=True,
    ),
    "anti_up_quark": Particle(
        name="Anti-up quark",
        symbol="u_bar",
        antiparticle="up_quark",
        category="quark",
        mass_gev=0.0022,
        electric_charge=-2.0 / 3.0,
        spin=0.5,
        color_charge="antitriplet",
        is_elementary=True,
    ),
    "down_quark": Particle(
        name="Down quark",
        symbol="d",
        antiparticle="anti_down_quark",
        category="quark",
        mass_gev=0.0047,
        electric_charge=-1.0 / 3.0,
        spin=0.5,
        color_charge="triplet",
        is_elementary=True,
    ),
    "anti_down_quark": Particle(
        name="Anti-down quark",
        symbol="d_bar",
        antiparticle="down_quark",
        category="quark",
        mass_gev=0.0047,
        electric_charge=1.0 / 3.0,
        spin=0.5,
        color_charge="antitriplet",
        is_elementary=True,
    ),
    "strange_quark": Particle(
        name="Strange quark",
        symbol="s",
        antiparticle="anti_strange_quark",
        category="quark",
        mass_gev=0.096,
        electric_charge=-1.0 / 3.0,
        spin=0.5,
        color_charge="triplet",
        is_elementary=True,
    ),
    "anti_strange_quark": Particle(
        name="Anti-strange quark",
        symbol="s_bar",
        antiparticle="strange_quark",
        category="quark",
        mass_gev=0.096,
        electric_charge=1.0 / 3.0,
        spin=0.5,
        color_charge="antitriplet",
        is_elementary=True,
    ),
    "photon": Particle(
        name="Photon",
        symbol="gamma",
        antiparticle="photon",
        category="gauge_boson",
        mass_gev=0.0,
        electric_charge=0.0,
        spin=1.0,
        color_charge="singlet",
        is_elementary=True,
    ),
    "gluon": Particle(
        name="Gluon",
        symbol="g",
        antiparticle="gluon",
        category="gauge_boson",
        mass_gev=0.0,
        electric_charge=0.0,
        spin=1.0,
        color_charge="octet",
        is_elementary=True,
    ),
    "w_plus": Particle(
        name="W boson",
        symbol="W+",
        antiparticle="w_minus",
        category="gauge_boson",
        mass_gev=80.377,
        electric_charge=1.0,
        spin=1.0,
        color_charge="singlet",
        is_elementary=True,
    ),
    "w_minus": Particle(
        name="W boson",
        symbol="W-",
        antiparticle="w_plus",
        category="gauge_boson",
        mass_gev=80.377,
        electric_charge=-1.0,
        spin=1.0,
        color_charge="singlet",
        is_elementary=True,
    ),
    "z_boson": Particle(
        name="Z boson",
        symbol="Z",
        antiparticle="z_boson",
        category="gauge_boson",
        mass_gev=91.1876,
        electric_charge=0.0,
        spin=1.0,
        color_charge="singlet",
        is_elementary=True,
    ),
    "higgs": Particle(
        name="Higgs boson",
        symbol="H",
        antiparticle="higgs",
        category="scalar_boson",
        mass_gev=125.25,
        electric_charge=0.0,
        spin=0.0,
        color_charge="singlet",
        is_elementary=True,
    ),
    "proton": Particle(
        name="Proton",
        symbol="p",
        antiparticle="antiproton",
        category="baryon",
        mass_gev=0.938272,
        electric_charge=1.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=False,
        composition="uud",
    ),
    "neutron": Particle(
        name="Neutron",
        symbol="n",
        antiparticle="antineutron",
        category="baryon",
        mass_gev=0.939565,
        electric_charge=0.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=False,
        composition="udd",
    ),
    "antiproton": Particle(
        name="Antiproton",
        symbol="p_bar",
        antiparticle="proton",
        category="baryon",
        mass_gev=0.938272,
        electric_charge=-1.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=False,
        composition="anti-u anti-u anti-d",
    ),
    "antineutron": Particle(
        name="Antineutron",
        symbol="n_bar",
        antiparticle="neutron",
        category="baryon",
        mass_gev=0.939565,
        electric_charge=0.0,
        spin=0.5,
        color_charge="singlet",
        is_elementary=False,
        composition="anti-u anti-d anti-d",
    ),
}


@dataclass(frozen=True)
class Interaction:
    name: str
    theory: str
    vertex: tuple[str, ...]
    mediator: str
    order: str
    description: str


INTERACTIONS = [
    Interaction(
        name="QED fermion-photon vertex",
        theory="QED",
        vertex=("charged_fermion", "charged_fermion", "photon"),
        mediator="photon",
        order="e",
        description="Electromagnetic interaction between a charged fermion and a photon.",
    ),
    Interaction(
        name="QCD quark-gluon vertex",
        theory="QCD",
        vertex=("quark", "quark", "gluon"),
        mediator="gluon",
        order="g_s",
        description="Strong interaction between a quark and a gluon.",
    ),
    Interaction(
        name="QCD three-gluon vertex",
        theory="QCD",
        vertex=("gluon", "gluon", "gluon"),
        mediator="gluon",
        order="g_s",
        description="Non-Abelian three-gluon self interaction.",
    ),
    Interaction(
        name="QCD four-gluon vertex",
        theory="QCD",
        vertex=("gluon", "gluon", "gluon", "gluon"),
        mediator="gluon",
        order="g_s^2",
        description="Non-Abelian four-gluon interaction.",
    ),
    Interaction(
        name="Charged weak vertex",
        theory="Electroweak",
        vertex=("fermion", "fermion", "W"),
        mediator="W",
        order="g",
        description="Charged-current weak interaction.",
    ),
    Interaction(
        name="Neutral weak vertex",
        theory="Electroweak",
        vertex=("fermion", "fermion", "Z"),
        mediator="Z",
        order="g",
        description="Neutral-current weak interaction.",
    ),
    Interaction(
        name="Higgs-fermion Yukawa vertex",
        theory="Electroweak",
        vertex=("fermion", "fermion", "Higgs"),
        mediator="Higgs",
        order="y_f",
        description="Fermion-Higgs Yukawa interaction.",
    ),
    Interaction(
        name="Scalar phi4 vertex",
        theory="Scalar QFT",
        vertex=("scalar", "scalar", "scalar", "scalar"),
        mediator="none",
        order="lambda",
        description="Four-scalar contact interaction retained as the first educational QFT model.",
    ),
]


def get_particle(name: str) -> Particle:
    try:
        return PARTICLES[name]
    except KeyError as exc:
        raise ValueError(f"Unknown particle: {name}") from exc


def list_particles(category: Optional[str] = None) -> list[dict]:
    particles = PARTICLES.values()

    if category is not None:
        particles = [
            particle
            for particle in particles
            if particle.category == category
        ]

    return [asdict(particle) for particle in particles]


def list_interactions(theory: Optional[str] = None) -> list[dict]:
    interactions = INTERACTIONS

    if theory is not None:
        interactions = [
            interaction
            for interaction in interactions
            if interaction.theory.lower() == theory.lower()
        ]

    return [asdict(interaction) for interaction in interactions]


def particle_summary() -> dict:
    return {
        "particle_count": len(PARTICLES),
        "interaction_count": len(INTERACTIONS),
        "categories": sorted(
            {particle.category for particle in PARTICLES.values()}
        ),
        "theories": sorted(
            {interaction.theory for interaction in INTERACTIONS}
        ),
    }
