import { useState } from "react";
import { analyzeMultiQubit } from "../services/multiqubitApi";

export default function MultiQubitLab() {
  const [amplitudes, setAmplitudes] = useState(
    "0,0,0,0,0,1,0,0"
  );

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function runAnalysis() {
    setLoading(true);
    setError("");

    try {
      const values = amplitudes
        .split(",")
        .map((value) => value.trim())
        .filter((value) => value !== "")
        .map(Number);

      if (
        values.length === 0 ||
        values.some((value) => !Number.isFinite(value))
      ) {
        throw new Error(
          "Enter valid numerical amplitudes separated by commas."
        );
      }

      const data = await analyzeMultiQubit(values);

      setResult(data);
    } catch (err) {
      setResult(null);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section
      id="multiqubit-lab"
      className="lab-section"
    >
      <div className="lab-header">
        <h2>Multi-Qubit State Laboratory</h2>

        <p>
          Construct and analyze multi-qubit quantum
          state vectors and their computational-basis
          measurement probabilities.
        </p>
      </div>

      <div className="lab-card">
        <h3>Quantum State Input</h3>

        <label className="lab-label">
          Real amplitudes

          <textarea
            value={amplitudes}
            onChange={(event) =>
              setAmplitudes(event.target.value)
            }
            rows={4}
            placeholder="Example: 0,0,0,0,0,1,0,0"
          />
        </label>

        <p className="input-help">
          Enter amplitudes separated by commas.
          The number of amplitudes must be a power
          of two.
        </p>

        <button
          className="primary-button"
          onClick={runAnalysis}
          disabled={loading}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Quantum State"}
        </button>

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}
      </div>

      {result && (
        <div className="lab-card quantum-result-card">
          <h3>State Analysis</h3>

          <div className="quantum-result-summary">
            <div>
              <span>Qubits</span>
              <strong>{result.qubits}</strong>
            </div>

            <div>
              <span>Dimension</span>
              <strong>{result.dimension}</strong>
            </div>
          </div>

          <div className="quantum-state-columns">
            <div>
              <h4>Normalized State</h4>

              <div className="amplitude-list">
                {result.state.map(
                  (amplitude, index) => {
                    const basisState =
                      index
                        .toString(2)
                        .padStart(
                          result.qubits,
                          "0"
                        );

                    const real =
                      Number(amplitude.real);

                    const imag =
                      Number(amplitude.imag);

                    let value;

                    if (
                      Math.abs(imag) < 1e-10
                    ) {
                      value = real.toFixed(4);
                    } else if (
                      Math.abs(real) < 1e-10
                    ) {
                      value =
                        `${imag.toFixed(4)}i`;
                    } else {
                      value =
                        `${real.toFixed(4)} ${
                          imag >= 0
                            ? "+"
                            : "-"
                        } ${Math.abs(
                          imag
                        ).toFixed(4)}i`;
                    }

                    return (
                      <div
                        className="amplitude-row"
                        key={index}
                      >
                        <span>
                          |{basisState}⟩
                        </span>

                        <strong>
                          {value}
                        </strong>
                      </div>
                    );
                  }
                )}
              </div>
            </div>

            <div>
              <h4>
                Measurement Probabilities
              </h4>

              <div className="probability-list">
                {Object.entries(
                  result.probabilities
                ).map(
                  ([
                    basisState,
                    probability,
                  ]) => (
                    <div
                      className="probability-row"
                      key={basisState}
                    >
                      <span>
                        |{basisState}⟩
                      </span>

                      <strong>
                        {(
                          probability * 100
                        ).toFixed(2)}
                        %
                      </strong>
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
