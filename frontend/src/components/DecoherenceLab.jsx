import React, { useState } from "react";

import {
  analyzeDecoherence,
  simulateDecoherence,
} from "../services/decoherenceApi";

function DecoherenceLab() {
  const [time, setTime] = useState("1");
  const [decoherenceRate, setDecoherenceRate] =
    useState("1");

  const [result, setResult] = useState(null);
  const [simulation, setSimulation] =
    useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const densityMatrix = [
    [0.5, 0.5],
    [0.5, 0.5],
  ];

  const formatNumber = (value) =>
    Number(value).toFixed(6);

  async function handleCalculate() {
    setLoading(true);
    setError("");

    try {
      const calculatedTime = Number(time);
      const calculatedRate =
        Number(decoherenceRate);

      if (
        !Number.isFinite(calculatedTime) ||
        calculatedTime < 0
      ) {
        throw new Error(
          "Time must be a non-negative number."
        );
      }

      if (
        !Number.isFinite(calculatedRate) ||
        calculatedRate < 0
      ) {
        throw new Error(
          "Decoherence rate must be a non-negative number."
        );
      }

      const calculated = await analyzeDecoherence(
        densityMatrix,
        calculatedTime,
        calculatedRate
      );

      const simulated =
        await simulateDecoherence(
          densityMatrix,
          0,
          calculatedTime,
          100,
          calculatedRate
        );

      setResult(calculated);
      setSimulation(simulated);
    } catch (err) {
      setError(
        err.message ||
          "Decoherence calculation failed."
      );
      setResult(null);
      setSimulation(null);
    } finally {
      setLoading(false);
    }
  }

  const chartPoints =
    simulation &&
    simulation.times.length > 1
      ? simulation.times
          .map((currentTime, index) => {
            const x =
              60 +
              (index /
                (simulation.times.length - 1)) *
                700;

            const value =
              simulation.coherence_factors[index];

            const y =
              320 -
              value * 280;

            return `${x},${y}`;
          })
          .join(" ")
      : "";

  return (
    <div className="lab-card">
      <h2>Decoherence Laboratory</h2>

      <p>
        Study how environmental dephasing reduces
        quantum coherence and changes the purity and
        entropy of a quantum state.
      </p>

      <div className="control-group">
        <label>
          Time
          <input
            type="number"
            min="0"
            step="0.1"
            value={time}
            onChange={(event) =>
              setTime(event.target.value)
            }
          />
        </label>

        <label>
          Decoherence rate γ
          <input
            type="number"
            min="0"
            step="0.1"
            value={decoherenceRate}
            onChange={(event) =>
              setDecoherenceRate(
                event.target.value
              )
            }
          />
        </label>

        <button
          onClick={handleCalculate}
          disabled={loading}
        >
          {loading
            ? "Calculating..."
            : "Calculate Decoherence"}
        </button>
      </div>

      <div className="result-card">
        <h3>Initial Density Matrix</h3>

        <div className="matrix-display">
          <div className="matrix-row">
            <span className="matrix-cell">
              0.500000
            </span>

            <span className="matrix-cell">
              0.500000
            </span>
          </div>

          <div className="matrix-row">
            <span className="matrix-cell">
              0.500000
            </span>

            <span className="matrix-cell">
              0.500000
            </span>
          </div>
        </div>
      </div>

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      {result && (
        <>
          <div className="result-grid">
            <div className="result-card">
              <h3>Coherence Factor</h3>
              <p>
                {formatNumber(
                  result.coherence_factor
                )}
              </p>
            </div>

            <div className="result-card">
              <h3>Purity</h3>
              <p>
                {formatNumber(result.purity)}
              </p>
            </div>

            <div className="result-card">
              <h3>Von Neumann Entropy</h3>
              <p>
                {formatNumber(
                  result.von_neumann_entropy
                )}
              </p>
            </div>
          </div>

          <div className="result-card">
            <h3>Decohered Density Matrix</h3>

            <div className="matrix-display">
              {result.density_matrix.map(
                (row, rowIndex) => (
                  <div
                    className="matrix-row"
                    key={rowIndex}
                  >
                    {row.map(
                      (value, columnIndex) => (
                        <span
                          className="matrix-cell"
                          key={columnIndex}
                        >
                          {formatNumber(
                            value.real
                          )}
                          {Math.abs(
                            value.imag
                          ) > 1e-10
                            ? ` ${
                                value.imag >= 0
                                  ? "+"
                                  : ""
                              }${formatNumber(
                                value.imag
                              )}i`
                            : ""}
                        </span>
                      )
                    )}
                  </div>
                )
              )}
            </div>
          </div>

          {simulation && (
            <div className="result-card">
              <h3>Coherence Decay</h3>

              <svg
                viewBox="0 0 820 360"
                width="100%"
                height="360"
              >
                <line
                  x1="60"
                  y1="320"
                  x2="760"
                  y2="320"
                  stroke="#888"
                  strokeWidth="2"
                />

                <line
                  x1="60"
                  y1="40"
                  x2="60"
                  y2="320"
                  stroke="#888"
                  strokeWidth="2"
                />

                <polyline
                  points={chartPoints}
                  fill="none"
                  stroke="#2563eb"
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />

                <text
                  x="410"
                  y="350"
                  textAnchor="middle"
                >
                  Time
                </text>

                <text
                  x="20"
                  y="180"
                  textAnchor="middle"
                  transform="rotate(-90 20 180)"
                >
                  Coherence
                </text>
              </svg>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default DecoherenceLab;