import { useState } from "react";
import { calculateTunneling } from "../services/quantumApi";

function TunnelingLab() {
  const [energy, setEnergy] = useState("2.0");
  const [barrierHeight, setBarrierHeight] = useState("5.0");
  const [barrierWidth, setBarrierWidth] = useState("0.5");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleCalculate(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await calculateTunneling({
        particle_energy_ev: Number(energy),
        barrier_height_ev: Number(barrierHeight),
        barrier_width_nm: Number(barrierWidth),
        create_visualization: true,
      });

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function formatScientific(value) {
    return Number(value).toExponential(6);
  }

  function getExplanation() {
    if (!result) {
      return "";
    }

    const transmission =
      result.results.transmission_probability;

    if (transmission < 0.001) {
      return (
        "The particle has a very small probability of " +
        "tunneling through the barrier. The barrier is higher " +
        "than the particle energy, and the exponential " +
        "dependence makes transmission strongly suppressed."
      );
    }

    if (transmission < 0.1) {
      return (
        "The particle has a measurable but relatively small " +
        "probability of tunneling through the barrier."
      );
    }

    return (
      "The particle has a relatively large tunneling probability " +
      "for the selected barrier parameters."
    );
  }

  return (
    <main className="lab-container">
      <header className="lab-header">
        <p className="lab-label">
          QUANTUM PHYSICS LABORATORY
        </p>

        <h1>Quantum Tunneling</h1>

        <p className="lab-description">
          Explore how a quantum particle can pass through a
          potential barrier even when its classical energy is
          insufficient to overcome it.
        </p>
      </header>

      <section className="lab-card">
        <h2>Simulation Parameters</h2>

        <form onSubmit={handleCalculate}>
          <div className="parameter-grid">
            <label>
              Particle
              <input
                type="text"
                value="Electron"
                disabled
              />
            </label>

            <label>
              Particle Energy (eV)
              <input
                type="number"
                step="any"
                min="0.000001"
                value={energy}
                onChange={(event) =>
                  setEnergy(event.target.value)
                }
              />
            </label>

            <label>
              Barrier Height (eV)
              <input
                type="number"
                step="any"
                min="0.000001"
                value={barrierHeight}
                onChange={(event) =>
                  setBarrierHeight(event.target.value)
                }
              />
            </label>

            <label>
              Barrier Width (nm)
              <input
                type="number"
                step="any"
                min="0.000001"
                value={barrierWidth}
                onChange={(event) =>
                  setBarrierWidth(event.target.value)
                }
              />
            </label>
          </div>

          <button
            type="submit"
            className="calculate-button"
            disabled={loading}
          >
            {loading ? "Calculating..." : "Calculate"}
          </button>
        </form>
      </section>

      {error && (
        <section className="error-card">
          <strong>Calculation error</strong>
          <p>{error}</p>
        </section>
      )}

      {result && (
        <>
          <section className="lab-card">
            <h2>Simulation Results</h2>

            <div className="results-grid">
              <div className="result-item">
                <span>Kappa</span>
                <strong>
                  {formatScientific(
                    result.results.kappa_per_meter
                  )}
                </strong>
                <small>1/m</small>
              </div>

              <div className="result-item">
                <span>Transmission Probability</span>
                <strong>
                  {formatScientific(
                    result.results.transmission_probability
                  )}
                </strong>
              </div>

              <div className="result-item">
                <span>Transmission</span>
                <strong>
                  {result.results.transmission_percentage.toFixed(
                    6
                  )}
                  %
                </strong>
              </div>

              <div className="result-item">
                <span>Reflection Probability</span>
                <strong>
                  {formatScientific(
                    result.results.reflection_probability
                  )}
                </strong>
              </div>

              <div className="result-item">
                <span>Reflection</span>
                <strong>
                  {result.results.reflection_percentage.toFixed(
                    6
                  )}
                  %
                </strong>
              </div>
            </div>
          </section>

          <section className="lab-card">
            <h2>Physics Calculation</h2>

            <div className="equation-block">
              <h3>Tunneling Probability</h3>

              <p className="equation">
                T approximately equals exp(-2 Kappa a)
              </p>

              <p>
                For a rectangular barrier with particle energy
                below the barrier height, the tunneling
                probability decreases exponentially with the
                barrier width.
              </p>
            </div>

            <div className="equation-block">
              <h3>Decay Constant</h3>

              <p className="equation">
                Kappa = sqrt(2m(V0 - E)) / hbar
              </p>

              <div className="substitution">
                <p>
                  <strong>Particle mass:</strong>{" "}
                  {Number(
                    result.simulation_parameters.particle_mass_kg
                  ).toExponential(6)}{" "}
                  kg
                </p>

                <p>
                  <strong>Particle energy:</strong>{" "}
                  {result.simulation_parameters.particle_energy_ev}{" "}
                  eV
                </p>

                <p>
                  <strong>Barrier height:</strong>{" "}
                  {result.simulation_parameters.barrier_height_ev}{" "}
                  eV
                </p>

                <p>
                  <strong>Barrier width:</strong>{" "}
                  {result.simulation_parameters.barrier_width_nm}{" "}
                  nm
                </p>

                <p>
                  <strong>Calculated Kappa:</strong>{" "}
                  {formatScientific(
                    result.results.kappa_per_meter
                  )}{" "}
                  1/m
                </p>
              </div>
            </div>

            <div className="explanation-box">
              <h3>Physical Interpretation</h3>

              <p>{getExplanation()}</p>

              <p>
                Increasing the barrier width or increasing the
                barrier height generally suppresses tunneling,
                while increasing the particle energy brings it
                closer to the top of the barrier and increases
                the tunneling probability in this model.
              </p>
            </div>

            <p className="model-note">
              <strong>Model note:</strong> The current solver
              uses the exponential rectangular-barrier
              approximation. It is an educational approximation
              rather than the exact finite-barrier scattering
              solution.
            </p>
          </section>

          {result.visualization_url && (
            <section className="lab-card">
              <h2>Simulation Visualization</h2>

              <img
                className="simulation-image"
                src={`http://127.0.0.1:8000${result.visualization_url}`}
                alt="Quantum tunneling simulation"
              />
            </section>
          )}
        </>
      )}
    </main>
  );
}

export default TunnelingLab;
