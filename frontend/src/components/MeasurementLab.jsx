import React, { useState } from "react";

import { performMeasurement } from "../services/measurementApi";

function MeasurementLab() {
  const [stateReal, setStateReal] = useState(
    "0.7071067812, 0.7071067812"
  );

  const [stateImag, setStateImag] = useState(
    "0, 0"
  );

  const [shots, setShots] = useState("100");

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const parseVector = (value) => {
    return value
      .split(",")
      .map((item) => Number(item.trim()));
  };

  const formatNumber = (value) =>
    Number(value).toFixed(6);

  async function handleMeasure() {
    setLoading(true);
    setError("");

    try {
      const real = parseVector(stateReal);
      const imag = parseVector(stateImag);
      const calculatedShots = Number(shots);

      if (
        real.some((value) => !Number.isFinite(value))
      ) {
        throw new Error(
          "Real amplitudes must contain valid numbers."
        );
      }

      if (
        imag.some((value) => !Number.isFinite(value))
      ) {
        throw new Error(
          "Imaginary amplitudes must contain valid numbers."
        );
      }

      if (real.length !== imag.length) {
        throw new Error(
          "Real and imaginary vectors must have the same length."
        );
      }

      if (
        !Number.isInteger(calculatedShots) ||
        calculatedShots < 1
      ) {
        throw new Error(
          "Shots must be a positive integer."
        );
      }

      const measurement =
        await performMeasurement(
          real,
          imag,
          calculatedShots,
          42
        );

      setResult(measurement);
    } catch (err) {
      setResult(null);
      setError(
        err.message ||
          "Quantum measurement failed."
      );
    } finally {
      setLoading(false);
    }
  }

  const probabilities =
    result?.measurement_probabilities || {};

  const counts =
    result?.measurement?.counts || {};

  return (
    <div className="lab-card">
      <h2>Quantum Measurement Laboratory</h2>

      <p>
        Explore the Born rule by preparing a quantum
        state and repeatedly measuring it in the
        computational basis.
      </p>

      <div className="control-group">
        <label>
          Real amplitudes
          <input
            type="text"
            value={stateReal}
            onChange={(event) =>
              setStateReal(event.target.value)
            }
            placeholder="0.7071, 0.7071"
          />
        </label>

        <label>
          Imaginary amplitudes
          <input
            type="text"
            value={stateImag}
            onChange={(event) =>
              setStateImag(event.target.value)
            }
            placeholder="0, 0"
          />
        </label>

        <label>
          Measurement shots
          <input
            type="number"
            min="1"
            step="1"
            value={shots}
            onChange={(event) =>
              setShots(event.target.value)
            }
          />
        </label>

        <button
          onClick={handleMeasure}
          disabled={loading}
        >
          {loading
            ? "Measuring..."
            : "Measure Quantum State"}
        </button>
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
              <h3>Qubits</h3>
              <p>{result.qubits}</p>
            </div>

            <div className="result-card">
              <h3>Dimension</h3>
              <p>{result.dimension}</p>
            </div>

            <div className="result-card">
              <h3>Normalization</h3>
              <p>
                {formatNumber(
                  result.normalization
                )}
              </p>
            </div>

            <div className="result-card">
              <h3>Total Shots</h3>
              <p>
                {result.measurement.shots}
              </p>
            </div>
          </div>

          <div className="result-card">
            <h3>Theoretical Probabilities</h3>

            {Object.entries(probabilities).map(
              ([state, probability]) => (
                <div
                  className="result-row"
                  key={state}
                >
                  <strong>
                    |{state}⟩
                  </strong>

                  <span>
                    {formatNumber(
                      probability
                    )}
                  </span>

                  <span>
                    {(probability * 100).toFixed(
                      2
                    )}
                    %
                  </span>
                </div>
              )
            )}
          </div>

          <div className="result-card">
            <h3>Observed Measurement Counts</h3>

            {Object.entries(counts).map(
              ([state, count]) => {
                const total =
                  result.measurement.shots;

                const percentage =
                  total > 0
                    ? (count / total) * 100
                    : 0;

                return (
                  <div
                    className="result-row"
                    key={state}
                  >
                    <strong>
                      |{state}⟩
                    </strong>

                    <span>
                      {count} measurements
                    </span>

                    <span>
                      {percentage.toFixed(2)}%
                    </span>
                  </div>
                );
              }
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default MeasurementLab;