import { useState } from "react";
import { runPathIntegral } from "../services/pathIntegralApi";

const DEFAULTS = {
  mass: 1.0,
  coupling: 1.0,
  lattice_points: 32,
  lattice_spacing: 0.25,
  sweeps: 2000,
  thermalization: 500,
  step_size: 1.0,
  seed: 1234,
};

function formatNumber(value, digits = 6) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "—";
  }

  return Number(value).toFixed(digits);
}

export default function PathIntegralLab() {
  const [parameters, setParameters] = useState(DEFAULTS);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function updateParameter(name, value) {
    setParameters((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function handleRun(event) {
    event.preventDefault();

    if (parameters.thermalization >= parameters.sweeps) {
      setError("Thermalization must be smaller than total sweeps.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const payload = await runPathIntegral({
        mass: Number(parameters.mass),
        coupling: Number(parameters.coupling),
        lattice_points: Number(parameters.lattice_points),
        lattice_spacing: Number(parameters.lattice_spacing),
        sweeps: Number(parameters.sweeps),
        thermalization: Number(parameters.thermalization),
        step_size: Number(parameters.step_size),
        seed: Number(parameters.seed),
      });

      setResult(payload);
    } catch (err) {
      setError(err.message || "Path integral simulation failed.");
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setParameters(DEFAULTS);
    setResult(null);
    setError("");
  }

  const observables = result?.observables || {};
  const monteCarlo = result?.monte_carlo || {};
  const pathIntegral = result?.path_integral || {};
  const finalField = result?.final_field || [];
  const measurements = result?.measurements || [];

  return (
    <section className="experiment-container">
      <h2>Feynman Path Integral Laboratory</h2>

      <p>
        Explore a Euclidean 0+1D scalar φ⁴ path integral using
        Metropolis Monte Carlo sampling.
      </p>

      <form onSubmit={handleRun}>
        <div className="control-grid">
          <label>
            Mass m
            <input
              type="number"
              step="0.1"
              min="0"
              value={parameters.mass}
              onChange={(event) =>
                updateParameter("mass", event.target.value)
              }
            />
          </label>

          <label>
            Coupling λ
            <input
              type="number"
              step="0.1"
              min="0"
              value={parameters.coupling}
              onChange={(event) =>
                updateParameter("coupling", event.target.value)
              }
            />
          </label>

          <label>
            Lattice points
            <input
              type="number"
              min="4"
              max="512"
              value={parameters.lattice_points}
              onChange={(event) =>
                updateParameter("lattice_points", event.target.value)
              }
            />
          </label>

          <label>
            Lattice spacing
            <input
              type="number"
              step="0.01"
              min="0.001"
              value={parameters.lattice_spacing}
              onChange={(event) =>
                updateParameter("lattice_spacing", event.target.value)
              }
            />
          </label>

          <label>
            Monte Carlo sweeps
            <input
              type="number"
              min="1"
              max="100000"
              value={parameters.sweeps}
              onChange={(event) =>
                updateParameter("sweeps", event.target.value)
              }
            />
          </label>

          <label>
            Thermalization
            <input
              type="number"
              min="0"
              value={parameters.thermalization}
              onChange={(event) =>
                updateParameter("thermalization", event.target.value)
              }
            />
          </label>

          <label>
            Step size
            <input
              type="number"
              step="0.1"
              min="0.001"
              value={parameters.step_size}
              onChange={(event) =>
                updateParameter("step_size", event.target.value)
              }
            />
          </label>

          <label>
            Random seed
            <input
              type="number"
              value={parameters.seed}
              onChange={(event) =>
                updateParameter("seed", event.target.value)
              }
            />
          </label>
        </div>

        <div className="button-row">
          <button type="submit" disabled={loading}>
            {loading ? "Running Monte Carlo..." : "Run Path Integral"}
          </button>

          <button type="button" onClick={handleReset}>
            Reset
          </button>
        </div>
      </form>

      {error && (
        <p style={{ color: "#b91c1c", marginTop: "1rem" }}>
          {error}
        </p>
      )}

      {result && (
        <div style={{ marginTop: "1.5rem" }}>
          <h3>Simulation Result</h3>

          <div className="result-grid">
            <div>
              <strong>Model</strong>
              <p>{result.model || "Euclidean φ⁴ theory"}</p>
            </div>

            <div>
              <strong>Mean action</strong>
              <p>{formatNumber(observables.mean_action)}</p>
            </div>

            <div>
              <strong>⟨φ⟩</strong>
              <p>{formatNumber(observables.mean_phi)}</p>
            </div>

            <div>
              <strong>⟨φ²⟩</strong>
              <p>{formatNumber(observables.mean_phi_squared)}</p>
            </div>

            <div>
              <strong>⟨φ⁴⟩</strong>
              <p>{formatNumber(observables.mean_phi_fourth)}</p>
            </div>

            <div>
              <strong>Acceptance rate</strong>
              <p>
                {formatNumber(
                  Number(monteCarlo.acceptance_rate) * 100,
                  2
                )}
                %
              </p>
            </div>

            <div>
              <strong>Measurements</strong>
              <p>{monteCarlo.measurement_count ?? "—"}</p>
            </div>

            <div>
              <strong>Accepted / attempted</strong>
              <p>
                {monteCarlo.accepted ?? "—"} /{" "}
                {monteCarlo.attempted ?? "—"}
              </p>
            </div>
          </div>

          <h3 style={{ marginTop: "1.5rem" }}>
            Path Integral
          </h3>

          <div className="physics-result">
            <p>
              <strong>Formal expression:</strong>{" "}
              {pathIntegral.formal_expression || "Z = ∫ Dφ e⁻ˢᴱ"}
            </p>

            <p>
              <strong>Weight:</strong>{" "}
              {pathIntegral.weight || "exp(-S_E)"}
            </p>

            <p>
              <strong>Euclidean action:</strong>{" "}
              {pathIntegral.action || "S_E[φ]"}
            </p>
          </div>

          <h3 style={{ marginTop: "1.5rem" }}>
            Final Euclidean Field Configuration
          </h3>

          <div
            style={{
              overflowX: "auto",
              padding: "0.75rem",
              border: "1px solid #ddd",
              borderRadius: "8px",
              fontFamily: "monospace",
              fontSize: "0.85rem",
            }}
          >
            {finalField.length
              ? finalField.map((value, index) => (
                  <span key={index}>
                    φ[{index}]={formatNumber(value, 4)}
                    {index < finalField.length - 1 ? "   " : ""}
                  </span>
                ))
              : "No final field returned."}
          </div>

          {measurements.length > 0 && (
            <>
              <h3 style={{ marginTop: "1.5rem" }}>
                Monte Carlo Measurements
              </h3>

              <div
                style={{
                  maxHeight: "300px",
                  overflowY: "auto",
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                }}
              >
                <table style={{ width: "100%" }}>
                  <thead>
                    <tr>
                      <th>Sweep</th>
                      <th>Action</th>
                      <th>⟨φ²⟩</th>
                    </tr>
                  </thead>

                  <tbody>
                    {measurements.map((measurement, index) => (
                      <tr key={index}>
                        <td>
                          {measurement.sweep ??
                            measurement.step ??
                            index}
                        </td>
                        <td>
                          {formatNumber(
                            measurement.action
                          )}
                        </td>
                        <td>
                          {formatNumber(
                            measurement.mean_phi_squared
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}

          <p
            style={{
              marginTop: "1.5rem",
              fontSize: "0.9rem",
              opacity: 0.8,
            }}
          >
            Educational finite-lattice Euclidean path-integral
            simulation. This is not a continuum-limit,
            renormalized, or full Minkowski QFT calculation.
          </p>
        </div>
      )}
    </section>
  );
}
