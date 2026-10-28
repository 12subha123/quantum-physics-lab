import { useEffect, useState } from "react";
import {
  getQuantumStates,
  getQuantumGates,
  applyQuantumGate,
} from "../services/quantumGatesApi";
import BlochSphere3D from "./BlochSphere3D";

function formatComplex(value) {
  const real = Number(value?.real ?? 0);
  const imag = Number(value?.imag ?? 0);

  if (Math.abs(imag) < 1e-10) {
    return real.toFixed(4);
  }

  if (Math.abs(real) < 1e-10) {
    return `${imag.toFixed(4)}i`;
  }

  return `${real.toFixed(4)} ${imag >= 0 ? "+" : "-"} ${Math.abs(imag).toFixed(4)}i`;
}

export default function QuantumGatesLab() {
  const [states, setStates] = useState(null);
  const [gates, setGates] = useState(null);
  const [stateName, setStateName] = useState("ket0");
  const [gate, setGate] = useState("H");
  const [customMode, setCustomMode] = useState(false);
  const [realInput, setRealInput] = useState("1");
  const [imagInput, setImagInput] = useState("0");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadOptions() {
      try {
        const [stateData, gateData] = await Promise.all([
          getQuantumStates(),
          getQuantumGates(),
        ]);

        setStates(stateData);
        setGates(gateData);
      } catch (err) {
        setError(err.message);
      }
    }

    loadOptions();
  }, []);

  async function runGate() {
    setLoading(true);
    setError("");

    try {
      let payload;

      if (customMode) {
        const real = realInput.split(",").map((value) => Number(value.trim()));
        const imag = imagInput.split(",").map((value) => Number(value.trim()));

        if (
          real.length !== imag.length ||
          real.some((value) => Number.isNaN(value)) ||
          imag.some((value) => Number.isNaN(value))
        ) {
          throw new Error(
            "Real and imaginary amplitudes must have the same number of valid values."
          );
        }

        payload = {
          amplitudes_real: real,
          amplitudes_imag: imag,
          gate,
        };
      } else {
        payload = {
          state_name: stateName,
          gate,
        };
      }

      const data = await applyQuantumGate(payload);
      setResult(data);
    } catch (err) {
      setError(err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  if (!states || !gates) {
    return (
      <section className="lab-section">
        <h2>Quantum Gates Laboratory</h2>
        <p>Loading quantum computing engine...</p>
        {error && <p className="error-message">{error}</p>}
      </section>
    );
  }

  return (
    <section id="quantum-gates-lab" className="lab-section">
      <div className="lab-header">
        <h2>Quantum Gates Laboratory</h2>
        <p>
          Explore quantum states, apply quantum gates, and observe how
          complex amplitudes and measurement probabilities change.
        </p>
      </div>

      <div className="quantum-gates-layout">
        <div className="lab-card">
          <h3>Input State</h3>

          <label className="lab-label">
            State type
            <select
              value={customMode ? "custom" : "standard"}
              onChange={(event) => {
                const value = event.target.value;
                setCustomMode(value === "custom");
                setResult(null);
                setError("");
              }}
            >
              <option value="standard">Standard quantum state</option>
              <option value="custom">Custom complex state</option>
            </select>
          </label>

          {!customMode ? (
            <>
              <label className="lab-label">
                Single-qubit states
                <select
                  value={stateName}
                  onChange={(event) => {
                    setStateName(event.target.value);
                    setResult(null);
                  }}
                >
                  {states.single_qubit_states.map((state) => (
                    <option key={state} value={state}>
                      {state}
                    </option>
                  ))}
                </select>
              </label>

              <label className="lab-label">
                Two-qubit computational states
                <select
                  value={stateName}
                  onChange={(event) => {
                    setStateName(event.target.value);
                    setResult(null);
                  }}
                >
                  {states.two_qubit_states.map((state) => (
                    <option key={state} value={state}>
                      {state}
                    </option>
                  ))}
                </select>
              </label>

              <label className="lab-label">
                Bell states
                <select
                  value={stateName}
                  onChange={(event) => {
                    setStateName(event.target.value);
                    setResult(null);
                  }}
                >
                  {states.bell_states.map((state) => (
                    <option key={state} value={state}>
                      {state}
                    </option>
                  ))}
                </select>
              </label>
            </>
          ) : (
            <>
              <label className="lab-label">
                Real amplitudes
                <input
                  type="text"
                  value={realInput}
                  onChange={(event) => setRealInput(event.target.value)}
                  placeholder="Example: 1, 0, 1, 0"
                />
              </label>

              <label className="lab-label">
                Imaginary amplitudes
                <input
                  type="text"
                  value={imagInput}
                  onChange={(event) => setImagInput(event.target.value)}
                  placeholder="Example: 0, 1, 0, -1"
                />
              </label>

              <p className="lab-hint">
                Enter matching comma-separated real and imaginary
                amplitudes. The engine automatically normalizes the state.
              </p>
            </>
          )}
        </div>

        <div className="lab-card">
          <h3>Quantum Gate</h3>

          <label className="lab-label">
            Gate
            <select
              value={gate}
              onChange={(event) => {
                setGate(event.target.value);
                setResult(null);
              }}
            >
              <optgroup label="Single-qubit gates">
                {gates.single_qubit_gates.map((gateName) => (
                  <option key={gateName} value={gateName}>
                    {gateName}
                  </option>
                ))}
              </optgroup>

              <optgroup label="Two-qubit gates">
                {gates.two_qubit_gates.map((gateName) => (
                  <option key={gateName} value={gateName}>
                    {gateName}
                  </option>
                ))}
              </optgroup>
            </select>
          </label>

          <button
            className="primary-button"
            onClick={runGate}
            disabled={loading}
          >
            {loading ? "Calculating..." : "Apply Quantum Gate"}
          </button>

          {error && <p className="error-message">{error}</p>}
        </div>
      </div>

      {result && (
        <div className="lab-card quantum-result-card">
          <h3>Calculation Result</h3>

          <div className="quantum-result-summary">
            <div>
              <span>Gate</span>
              <strong>{result.gate}</strong>
            </div>

            <div>
              <span>State dimension</span>
              <strong>{result.dimension}</strong>
            </div>
          </div>

          <div className="quantum-state-columns">
            <div>
              <h4>Input State</h4>

              <div className="amplitude-list">
                {result.input_state.map((amplitude, index) => (
                  <div className="amplitude-row" key={index}>
                    <span>
                      |{index
                        .toString(2)
                        .padStart(
                          Math.log2(result.dimension),
                          "0"
                        )}?
                    </span>

                    <strong>
                      {formatComplex(amplitude)}
                    </strong>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4>Output State</h4>

              <div className="amplitude-list">
                {result.output_state.map((amplitude, index) => (
                  <div className="amplitude-row" key={index}>
                    <span>
                      |{index
                        .toString(2)
                        .padStart(
                          Math.log2(result.dimension),
                          "0"
                        )}?
                    </span>

                    <strong>
                      {formatComplex(amplitude)}
                    </strong>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <p>
  Bloch data:{" "}
  {result.bloch_coordinates
    ? "AVAILABLE"
    : "NOT AVAILABLE"}
</p>
          {result.bloch_coordinates && (
  <div className="quantum-bloch-result">
    <h4>Bloch Sphere</h4>

    <BlochSphere3D
      theta={result.bloch_coordinates.theta}
      phi={result.bloch_coordinates.phi}
    />

    <div className="bloch-coordinate-summary">
      <div>
        <span>X</span>
        <strong>
          {result.bloch_coordinates.x.toFixed(4)}
        </strong>
      </div>

      <div>
        <span>Y</span>
        <strong>
          {result.bloch_coordinates.y.toFixed(4)}
        </strong>
      </div>

      <div>
        <span>Z</span>
        <strong>
          {result.bloch_coordinates.z.toFixed(4)}
        </strong>
      </div>

      <div>
        <span>θ</span>
        <strong>
          {result.bloch_coordinates.theta_degrees.toFixed(2)}°
        </strong>
      </div>

      <div>
        <span>φ</span>
        <strong>
          {result.bloch_coordinates.phi_degrees.toFixed(2)}°
        </strong>
      </div>
    </div>
  </div>
)}

          <h4>Measurement Probabilities</h4>

          <div className="probability-list">
            {Object.entries(result.probabilities).map(
              ([basisState, probability]) => (
                <div
                  className="probability-row"
                  key={basisState}
                >
                  <span>|{basisState}?</span>

                  <strong>
                    {(probability * 100).toFixed(2)}%
                  </strong>
                </div>
              )
            )}
          </div>
        </div>
      )}
    </section>
  );
}
