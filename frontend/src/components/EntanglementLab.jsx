import { useEffect, useState } from "react";
import {
  getBellStates,
  analyzeEntanglement,
} from "../services/entanglementApi";

function formatComplex(value) {
  const real = Number(value?.real ?? 0);
  const imag = Number(value?.imag ?? 0);

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

export default function EntanglementLab() {
  const [states, setStates] = useState([]);
  const [stateName, setStateName] = useState("phi_plus");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadStates() {
      try {
        const data = await getBellStates();
        setStates(data.states || []);
      } catch (err) {
        setError(err.message);
      }
    }

    loadStates();
  }, []);

  async function runAnalysis() {
    setLoading(true);
    setError("");

    try {
      const data = await analyzeEntanglement(stateName);
      setResult(data);
    } catch (err) {
      setError(err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section
      id="entanglement-lab"
      className="lab-section"
    >
      <div className="lab-header">
        <h2>Quantum Entanglement Laboratory</h2>

        <p>
          Explore Bell states and investigate quantum
          entanglement using measurement probabilities,
          reduced density matrices, and state purity.
        </p>
      </div>

      <div className="lab-card">
        <h3>Bell State Experiment</h3>

        <label className="lab-label">
          Bell state

          <select
            value={stateName}
            onChange={(event) => {
              setStateName(event.target.value);
              setResult(null);
              setError("");
            }}
          >
            {states.map((state) => (
              <option
                key={state.name}
                value={state.name}
              >
                {state.label} — {state.name}
              </option>
            ))}
          </select>
        </label>

        <button
          className="primary-button"
          onClick={runAnalysis}
          disabled={loading || states.length === 0}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Entanglement"}
        </button>

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}
      </div>

      {result && (
        <div className="lab-card quantum-result-card">
          <h3>Entanglement Analysis</h3>

          <div className="quantum-result-summary">
            <div>
              <span>Bell state</span>
              <strong>{result.label}</strong>
            </div>

            <div>
              <span>Dimension</span>
              <strong>{result.dimension}</strong>
            </div>

            <div>
              <span>Entangled</span>
              <strong>
                {result.is_entangled
                  ? "Yes"
                  : "No"}
              </strong>
            </div>

            <div>
              <span>Purity</span>
              <strong>
                {result.reduced_state_purity.toFixed(4)}
              </strong>
            </div>
          </div>

          <div className="quantum-state-columns">
            <div>
              <h4>State Amplitudes</h4>

              <div className="amplitude-list">
                {result.state.map(
                  (amplitude, index) => (
                    <div
                      className="amplitude-row"
                      key={index}
                    >
                      <span>
                        |
                        {index
                          .toString(2)
                          .padStart(2, "0")}
                        ⟩
                      </span>

                      <strong>
                        {formatComplex(amplitude)}
                      </strong>
                    </div>
                  )
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

          <h4>
            Reduced Density Matrix
          </h4>

          <div className="density-matrix">
            {result.reduced_density_matrix.map(
              (row, rowIndex) => (
                <div
                  className="density-row"
                  key={rowIndex}
                >
                  {row.map(
                    (value, columnIndex) => (
                      <span
                        className="density-cell"
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

          <div className="lab-explanation">
            <h4>Physical Interpretation</h4>

            <p>
              The reduced state purity is
              approximately 0.5 for a maximally
              entangled Bell pair. A pure single
              qubit state has purity 1, while the
              reduced state of one qubit from a
              maximally entangled pair is mixed.
            </p>

            <p>
              Therefore, the reduced-state analysis
              provides evidence that the two qubits
              cannot be described independently.
            </p>
          </div>
        </div>
      )}
    </section>
  );
}
