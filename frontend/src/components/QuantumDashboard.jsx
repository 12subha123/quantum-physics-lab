import React from "react";

import TunnelingLab from "./TunnelingLab";
import HarmonicOscillatorLab from "./HarmonicOscillatorLab";
import SuperpositionLab from "./SuperpositionLab";
import OperatorsEigenstatesLab from "./OperatorsEigenstatesLab";
import BlochSphereLab from "./BlochSphereLab";
import QuantumGatesLab from "./QuantumGatesLab";
import EntanglementLab from "./EntanglementLab";
import MultiQubitLab from "./MultiQubitLab";
import TimeEvolutionLab from "./TimeEvolutionLab";
import DensityMatrixLab from "./DensityMatrixLab";
import DecoherenceLab from "./DecoherenceLab";
import MeasurementLab from "./MeasurementLab";

function QuantumDashboard() {
  const experiments = [
    {
      id: "tunneling",
      title: "Quantum Tunneling",
      category: "Quantum Foundations",
      description:
        "Explore tunneling probability through a potential barrier.",
      status: "Physics Ready",
    },
    {
      id: "harmonic-oscillator",
      title: "Quantum Harmonic Oscillator",
      category: "Quantum Foundations",
      description:
        "Explore quantized energy levels and harmonic oscillator wavefunctions.",
      status: "Physics Ready",
    },
    {
      id: "superposition",
      title: "Superposition & Measurement",
      category: "Quantum Foundations",
      description:
        "Study quantum superposition and measurement probabilities.",
      status: "Physics Ready",
    },
    {
      id: "operators-eigenstates",
      title: "Operators & Eigenstates",
      category: "Quantum Foundations",
      description:
        "Analyze quantum operators, eigenvalues, and eigenstates.",
      status: "Physics Ready",
    },
    {
      id: "bloch-sphere",
      title: "Bloch Sphere",
      category: "Quantum Computing",
      description:
        "Visualize single-qubit states on the Bloch sphere.",
      status: "Physics Ready",
    },
    {
      id: "quantum-gates",
      title: "Quantum Gates",
      category: "Quantum Computing",
      description:
        "Experiment with fundamental quantum gates and qubit states.",
      status: "Physics Ready",
    },
    {
      id: "entanglement",
      title: "Bell-State Entanglement",
      category: "Quantum Computing",
      description:
        "Analyze entanglement, reduced states, and Bell states.",
      status: "Physics Ready",
    },
    {
      id: "multiqubit",
      title: "Multi-Qubit States",
      category: "Quantum Computing",
      description:
        "Work with multi-qubit state vectors and measurement probabilities.",
      status: "Physics Ready",
    },
    {
      id: "time-evolution",
      title: "Hamiltonian Time Evolution",
      category: "Quantum Dynamics",
      description:
        "Simulate quantum-state evolution under a time-independent Hamiltonian.",
      status: "Physics Ready",
    },
    {
      id: "density-matrix",
      title: "Density Matrices",
      category: "Quantum Foundations",
      description:
        "Analyze pure and mixed quantum states using density matrices.",
      status: "Physics Ready",
    },
    {
      id: "decoherence",
      title: "Quantum Decoherence",
      category: "Open Quantum Systems",
      description:
        "Study how environmental noise destroys quantum coherence.",
      status: "Physics Ready",
    },
    {
      id: "measurement",
      title: "Quantum Measurement",
      category: "Quantum Measurement",
      description:
        "Prepare quantum states and simulate repeated measurements using the Born rule.",
      status: "Physics Ready",
    },
    {
      id: "qft",
      title: "Quantum Field Theory",
      category: "Quantum Field Theory",
      description:
        "Explore relativistic scalar fields and the Klein–Gordon equation.",
      status: "Physics Ready",
    },
  ];

  return (
    <div className="quantum-dashboard">
      <header className="dashboard-header">
        <h1>Quantum Physics Laboratory</h1>

        <p>
          Interactive computational experiments for exploring quantum
          mechanics, quantum information, and quantum field theory.
        </p>
      </header>

      <section className="experiment-grid">
        {experiments.map((experiment) => (
          <button
            key={experiment.id}
            className="experiment-card"
            onClick={() => {
              const section = document.getElementById(
                `${experiment.id}-lab`
              );

              if (section) {
                section.scrollIntoView({
                  behavior: "smooth",
                  block: "start",
                });
              }
            }}
          >
            <div className="experiment-card-header">
              <h2>{experiment.title}</h2>

              <span className="experiment-status">
                {experiment.status}
              </span>
            </div>

            <p className="experiment-category">
              {experiment.category}
            </p>

            <p className="experiment-description">
              {experiment.description}
            </p>

            <span className="experiment-action">
              Open Laboratory →
            </span>
          </button>
        ))}
      </section>

      <main className="experiment-sections">
        <section
          id="tunneling-lab"
          className="experiment-container"
        >
          <TunnelingLab />
        </section>

        <section
          id="harmonic-oscillator-lab"
          className="experiment-container"
        >
          <HarmonicOscillatorLab />
        </section>

        <section
          id="superposition-lab"
          className="experiment-container"
        >
          <SuperpositionLab />
        </section>

        <section
          id="operators-eigenstates-lab"
          className="experiment-container"
        >
          <OperatorsEigenstatesLab />
        </section>

        <section
          id="bloch-sphere-lab"
          className="experiment-container"
        >
          <BlochSphereLab />
        </section>

        <section
          id="quantum-gates-lab"
          className="experiment-container"
        >
          <QuantumGatesLab />
        </section>

        <section
          id="entanglement-lab"
          className="experiment-container"
        >
          <EntanglementLab />
        </section>

        <section
          id="multiqubit-lab"
          className="experiment-container"
        >
          <MultiQubitLab />
        </section>

        <section
          id="time-evolution-lab"
          className="experiment-container"
        >
          <TimeEvolutionLab />
        </section>

        <section
          id="density-matrix-lab"
          className="experiment-container"
        >
          <DensityMatrixLab />
        </section>

        <section
          id="decoherence-lab"
          className="experiment-container"
        >
          <DecoherenceLab />
        </section>

        <section
          id="measurement-lab"
          className="experiment-container"
        >
          <MeasurementLab />
        </section>

        <section
          id="qft-lab"
          className="experiment-container"
        >
        </section>
      </main>
    </div>
  );
}

export default QuantumDashboard;
