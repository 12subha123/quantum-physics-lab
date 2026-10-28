import React, { useState } from "react";
import { analyzeTimeEvolution } from "../services/timeEvolutionApi";
import { simulateTimeEvolution } from "../services/timeEvolutionSimulationApi";

export default function TimeEvolutionLab() {
  const [stateInput, setStateInput] = useState(
    "0.7071067812, 0.7071067812"
  );

  const [hamiltonianInput, setHamiltonianInput] = useState(
    "0.5, 0\n0,-0.5"
  );

  const [time, setTime] = useState("3.141592653589793");
  const [hbar, setHbar] = useState("1");

  const [simulationStart, setSimulationStart] = useState("0");
  const [simulationEnd, setSimulationEnd] = useState(
    "6.283185307179586"
  );
  const [steps, setSteps] = useState("100");

  const [result, setResult] = useState(null);
  const [simulation, setSimulation] = useState(null);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [simulationLoading, setSimulationLoading] =
    useState(false);

  function parseState(value) {
    return value
      .split(",")
      .map((item) => Number(item.trim()));
  }

  function parseMatrix(value) {
    return value
      .trim()
      .split("\n")
      .map((row) =>
        row
          .split(",")
          .map((item) => Number(item.trim()))
      );
  }

  function buildInputs() {
    const stateReal = parseState(stateInput);
    const hamiltonianReal = parseMatrix(hamiltonianInput);

    const stateImag = stateReal.map(() => 0);

    const hamiltonianImag = hamiltonianReal.map((row) =>
      row.map(() => 0)
    );

    return {
      stateReal,
      stateImag,
      hamiltonianReal,
      hamiltonianImag,
    };
  }

  async function handleCalculate() {
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const {
        stateReal,
        stateImag,
        hamiltonianReal,
        hamiltonianImag,
      } = buildInputs();

      const data = await analyzeTimeEvolution(
        stateReal,
        stateImag,
        hamiltonianReal,
        hamiltonianImag,
        Number(time),
        Number(hbar)
      );

      setResult(data);
    } catch (err) {
      setError(
        err.message || "Time-evolution calculation failed."
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleSimulation() {
    setError("");
    setSimulation(null);
    setSimulationLoading(true);

    try {
      const {
        stateReal,
        stateImag,
        hamiltonianReal,
        hamiltonianImag,
      } = buildInputs();

      const data = await simulateTimeEvolution(
        stateReal,
        stateImag,
        hamiltonianReal,
        hamiltonianImag,
        Number(simulationStart),
        Number(simulationEnd),
        Number(steps),
        Number(hbar)
      );

      setSimulation(data);
    } catch (err) {
      setError(
        err.message || "Time-evolution simulation failed."
      );
    } finally {
      setSimulationLoading(false);
    }
  }

  const chartData =
    simulation?.times?.map((timeValue, index) => {
      const probabilityRow =
        simulation.probabilities[index];

      const row = {
        time: Number(timeValue.toFixed(4)),
      };

      Object.entries(probabilityRow).forEach(
        ([state, probability]) => {
          row[`p_${state}`] = probability * 100;
        }
      );

      return row;
    }) || [];

  const probabilityKeys =
    simulation?.probabilities?.[0]
      ? Object.keys(simulation.probabilities[0])
      : [];

  return (
    <section id="time-evolution-lab" className="lab-section">
      <div className="lab-header">
        <h2>Hamiltonian Time Evolution</h2>

        <p>
          Evolve a finite-dimensional quantum state under a
          time-independent Hamiltonian.
        </p>
      </div>

      <div className="lab-card">
        <label className="lab-label">
          Initial state amplitudes
        </label>

        <input
          className="lab-input"
          value={stateInput}
          onChange={(event) =>
            setStateInput(event.target.value)
          }
          placeholder="0.7071, 0.7071"
        />

        <p className="input-help">
          Enter real amplitudes separated by commas.
        </p>

        <label className="lab-label">
          Hamiltonian matrix
        </label>

        <textarea
          className="lab-textarea"
          value={hamiltonianInput}
          onChange={(event) =>
            setHamiltonianInput(event.target.value)
          }
          rows={4}
          placeholder={"0.5, 0\n0, -0.5"}
        />

        <p className="input-help">
          Enter one matrix row per line. Separate values with
          commas.
        </p>

        <div className="input-grid">
          <div>
            <label className="lab-label">
              Single calculation time
            </label>

            <input
              className="lab-input"
              type="number"
              step="any"
              value={time}
              onChange={(event) =>
                setTime(event.target.value)
              }
            />
          </div>

          <div>
            <label className="lab-label">
              ℏ
            </label>

            <input
              className="lab-input"
              type="number"
              step="any"
              min="0.0000000001"
              value={hbar}
              onChange={(event) =>
                setHbar(event.target.value)
              }
            />
          </div>
        </div>

        <button
          className="primary-button"
          onClick={handleCalculate}
          disabled={loading}
        >
          {loading
            ? "Calculating..."
            : "Evolve Quantum State"}
        </button>
      </div>

      <div className="lab-card">
        <h3>Time-Series Simulation</h3>

        <p className="input-help">
          Calculate the measurement probabilities across a
          continuous time interval.
        </p>

        <div className="input-grid">
          <div>
            <label className="lab-label">
              Start time
            </label>

            <input
              className="lab-input"
              type="number"
              step="any"
              value={simulationStart}
              onChange={(event) =>
                setSimulationStart(event.target.value)
              }
            />
          </div>

          <div>
            <label className="lab-label">
              End time
            </label>

            <input
              className="lab-input"
              type="number"
              step="any"
              value={simulationEnd}
              onChange={(event) =>
                setSimulationEnd(event.target.value)
              }
            />
          </div>

          <div>
            <label className="lab-label">
              Steps
            </label>

            <input
              className="lab-input"
              type="number"
              min="2"
              step="1"
              value={steps}
              onChange={(event) =>
                setSteps(event.target.value)
              }
            />
          </div>
        </div>

        <button
          className="primary-button"
          onClick={handleSimulation}
          disabled={simulationLoading}
        >
          {simulationLoading
            ? "Simulating..."
            : "Run Time Simulation"}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {result && (
        <div className="quantum-result-card">
          <h3>Single-Time Result</h3>

          <div className="quantum-result-summary">
            <div>
              <strong>Dimension</strong>
              <span>{result.dimension}</span>
            </div>

            <div>
              <strong>Time</strong>
              <span>{result.time}</span>
            </div>

            <div>
              <strong>ℏ</strong>
              <span>{result.hbar}</span>
            </div>

            <div>
              <strong>Normalization</strong>
              <span>
                {result.normalization.toFixed(6)}
              </span>
            </div>
          </div>

          <div className="quantum-state-columns">
            <div>
              <h3>Initial Probabilities</h3>

              <div className="probability-list">
                {Object.entries(
                  result.initial_probabilities
                ).map(([state, probability]) => (
                  <div
                    className="probability-row"
                    key={`initial-${state}`}
                  >
                    <span>|{state}⟩</span>

                    <strong>
                      {(probability * 100).toFixed(2)}%
                    </strong>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3>Evolved Probabilities</h3>

              <div className="probability-list">
                {Object.entries(
                  result.evolved_probabilities
                ).map(([state, probability]) => (
                  <div
                    className="probability-row"
                    key={`evolved-${state}`}
                  >
                    <span>|{state}⟩</span>

                    <strong>
                      {(probability * 100).toFixed(2)}%
                    </strong>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="quantum-state-columns">
            <div>
              <h3>Initial Energy</h3>

              <p>
                {result.initial_energy.toFixed(8)}
              </p>
            </div>

            <div>
              <h3>Final Energy</h3>

              <p>
                {result.final_energy.toFixed(8)}
              </p>
            </div>
          </div>

          <h3>Evolved State</h3>

          <div className="amplitude-list">
            {result.evolved_state.map(
              (amplitude, index) => (
                <div
                  className="amplitude-row"
                  key={index}
                >
                  <span>|{index}⟩</span>

                  <span>
                    {amplitude.real.toFixed(6)}
                    {amplitude.imag >= 0
                      ? " + "
                      : " - "}
                    {Math.abs(
                      amplitude.imag
                    ).toFixed(6)}
                    i
                  </span>
                </div>
              )
            )}
          </div>
        </div>
      )}

      {simulation && (
        <div className="quantum-result-card">
          <h3>Probability Evolution</h3>

          <div className="quantum-result-summary">
            <div>
              <strong>Qubits</strong>
              <span>{simulation.qubits}</span>
            </div>

            <div>
              <strong>Dimension</strong>
              <span>{simulation.dimension}</span>
            </div>

            <div>
              <strong>Time Points</strong>
              <span>{simulation.times.length}</span>
            </div>

            <div>
              <strong>ℏ</strong>
              <span>{simulation.hbar}</span>
            </div>
          </div>

          <div className="time-evolution-chart">
            <svg
              viewBox="0 0 800 360"
              role="img"
              aria-label="Quantum probability evolution over time"
            >
              {probabilityKeys.map(
                (state, stateIndex) => {
                  const points = chartData
                    .map((row, index) => {
                      const x =
                        chartData.length > 1
                          ? 60 +
                            (index /
                              (chartData.length - 1)) *
                              700
                          : 410;

                      const probability =
                        row[`p_${state}`] ?? 0;

                      const y =
                        320 -
                        (probability / 100) * 280;

                      return `${x},${y}`;
                    })
                    .join(" ");

                  return (
                    <polyline
  points={points}
  fill="none"
  stroke={stateIndex === 0 ? "#2563eb" : "#dc2626"}
  strokeWidth="3"
  strokeLinecap="round"
  strokeLinejoin="round"
/>
                    
                  );
                }
              )}

              <line
                x1="60"
                y1="320"
                x2="760"
                y2="320"
                strokeWidth="2"
              />

              <line
                x1="60"
                y1="40"
                x2="60"
                y2="320"
                strokeWidth="2"
              />
            </svg>
          </div>

          <div className="probability-list">
            {probabilityKeys.map((state) => (
              <div
                className="probability-row"
                key={`simulation-${state}`}
              >
                <span>
                  P(|{state}⟩)
                </span>

                <strong>
                  Time-dependent
                </strong>
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
