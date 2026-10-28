import React, { useState } from "react";
import {
  analyzePureDensityMatrix,
  analyzeMixedDensityMatrix,
} from "../services/densityMatrixApi";

export default function DensityMatrixLab() {
  const [mode, setMode] = useState("pure");

  const [pureState, setPureState] = useState(
    "0.7071067812, 0.7071067812"
  );

  const [pureImag, setPureImag] = useState(
    "0, 0"
  );

  const [mixedStateA, setMixedStateA] = useState(
    "1, 0"
  );

  const [mixedStateB, setMixedStateB] = useState(
    "0, 1"
  );

  const [mixedProbabilityA, setMixedProbabilityA] =
    useState("0.5");

  const [mixedProbabilityB, setMixedProbabilityB] =
    useState("0.5");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function parseVector(value) {
    return value
      .split(",")
      .map((item) => Number(item.trim()));
  }

  async function handleCalculate() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      if (mode === "pure") {
        const real = parseVector(pureState);
        const imag = parseVector(pureImag);

        if (real.some((value) => !Number.isFinite(value))) {
          throw new Error(
            "Pure-state real amplitudes must be valid numbers."
          );
        }

        if (imag.some((value) => !Number.isFinite(value))) {
          throw new Error(
            "Pure-state imaginary amplitudes must be valid numbers."
          );
        }

        if (real.length !== imag.length) {
          throw new Error(
            "Real and imaginary amplitudes must have the same length."
          );
        }

        const data = await analyzePureDensityMatrix(
          real,
          imag
        );

        setResult(data);
      } else {
        const stateA = parseVector(mixedStateA);
        const stateB = parseVector(mixedStateB);

        const probabilityA = Number(
          mixedProbabilityA
        );

        const probabilityB = Number(
          mixedProbabilityB
        );

        if (
          stateA.some(
            (value) => !Number.isFinite(value)
          ) ||
          stateB.some(
            (value) => !Number.isFinite(value)
          )
        ) {
          throw new Error(
            "Mixed-state amplitudes must be valid numbers."
          );
        }

        if (
          !Number.isFinite(probabilityA) ||
          !Number.isFinite(probabilityB)
        ) {
          throw new Error(
            "Mixed-state probabilities must be valid numbers."
          );
        }

        if (stateA.length !== stateB.length) {
          throw new Error(
            "Mixed states must have the same dimension."
          );
        }

        const data =
          await analyzeMixedDensityMatrix(
            [stateA, stateB],
            [
              new Array(stateA.length).fill(0),
              new Array(stateB.length).fill(0),
            ],
            [probabilityA, probabilityB]
          );

        setResult(data);
      }
    } catch (err) {
      setError(
        err.message ||
          "Density-matrix calculation failed."
      );
    } finally {
      setLoading(false);
    }
  }

  function formatComplex(value) {
    const real = Number(value.real);
    const imag = Number(value.imag);

    if (Math.abs(imag) < 1e-10) {
      return real.toFixed(4);
    }

    if (Math.abs(real) < 1e-10) {
      return `${imag.toFixed(4)}i`;
    }

    return `${real.toFixed(4)} ${
      imag >= 0 ? "+" : "-"
    } ${Math.abs(imag).toFixed(4)}i`;
  }

  return (
    <div className="lab-card">
      <h2>Density Matrices & Mixed States</h2>

      <p>
        Represent pure and mixed quantum states using
        density matrices and calculate trace, purity,
        entropy, eigenvalues, and measurement
        probabilities.
      </p>

      <div className="control-group">
        <label>State Type</label>

        <select
          value={mode}
          onChange={(event) => {
            setMode(event.target.value);
            setResult(null);
            setError("");
          }}
        >
          <option value="pure">
            Pure State
          </option>

          <option value="mixed">
            Mixed State
          </option>
        </select>
      </div>

      {mode === "pure" && (
        <>
          <div className="control-group">
            <label>
              Real amplitudes
            </label>

            <input
              value={pureState}
              onChange={(event) =>
                setPureState(event.target.value)
              }
              placeholder="Example: 0.7071, 0.7071"
            />
          </div>

          <div className="control-group">
            <label>
              Imaginary amplitudes
            </label>

            <input
              value={pureImag}
              onChange={(event) =>
                setPureImag(event.target.value)
              }
              placeholder="Example: 0, 0"
            />
          </div>
        </>
      )}

      {mode === "mixed" && (
        <>
          <div className="control-group">
            <label>
              State 1 amplitudes
            </label>

            <input
              value={mixedStateA}
              onChange={(event) =>
                setMixedStateA(event.target.value)
              }
              placeholder="Example: 1, 0"
            />
          </div>

          <div className="control-group">
            <label>
              State 1 probability
            </label>

            <input
              type="number"
              step="0.1"
              value={mixedProbabilityA}
              onChange={(event) =>
                setMixedProbabilityA(
                  event.target.value
                )
              }
            />
          </div>

          <div className="control-group">
            <label>
              State 2 amplitudes
            </label>

            <input
              value={mixedStateB}
              onChange={(event) =>
                setMixedStateB(event.target.value)
              }
              placeholder="Example: 0, 1"
            />
          </div>

          <div className="control-group">
            <label>
              State 2 probability
            </label>

            <input
              type="number"
              step="0.1"
              value={mixedProbabilityB}
              onChange={(event) =>
                setMixedProbabilityB(
                  event.target.value
                )
              }
            />
          </div>
        </>
      )}

      <button
        type="button"
        onClick={handleCalculate}
        disabled={loading}
      >
        {loading
          ? "Calculating..."
          : "Calculate Density Matrix"}
      </button>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {result && (
        <div className="result-card">
          <h3>Density Matrix Results</h3>

          <div className="result-grid">
            <div>
              <strong>Qubits</strong>
              <span>{result.qubits}</span>
            </div>

            <div>
              <strong>Dimension</strong>
              <span>{result.dimension}</span>
            </div>

            <div>
              <strong>Trace</strong>
              <span>
                {result.trace.toFixed(6)}
              </span>
            </div>

            <div>
              <strong>Purity</strong>
              <span>
                {result.purity.toFixed(6)}
              </span>
            </div>

            <div>
              <strong>Von Neumann Entropy</strong>
              <span>
                {result.von_neumann_entropy.toFixed(
                  6
                )}
              </span>
            </div>
          </div>

          <h4>Density Matrix</h4>

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
                        {formatComplex(value)}
                      </span>
                    )
                  )}
                </div>
              )
            )}
          </div>

          <h4>Eigenvalues</h4>

          <div className="probability-list">
            {result.eigenvalues.map(
              (value, index) => (
                <div
                  key={index}
                  className="probability-row"
                >
                  <span>
                    λ{index}
                  </span>

                  <strong>
                    {value.toFixed(6)}
                  </strong>
                </div>
              )
            )}
          </div>

          <h4>
            Measurement Probabilities
          </h4>

          <div className="probability-list">
            {Object.entries(
              result.measurement_probabilities
            ).map(([state, probability]) => (
              <div
                key={state}
                className="probability-row"
              >
                <span>
                  |{state}⟩
                </span>

                <strong>
                  {(probability * 100).toFixed(
                    2
                  )}
                  %
                </strong>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}