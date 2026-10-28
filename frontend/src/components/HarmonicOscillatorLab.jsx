import { useState } from "react";
import { calculateHarmonicOscillator } from "../services/harmonicOscillatorApi";

function HarmonicOscillatorLab() {
  const [mass, setMass] = useState("1.0");
  const [omega, setOmega] = useState("1.0");
  const [numStates, setNumStates] = useState("5");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleCalculate(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await calculateHarmonicOscillator({
        hbar: 1.0,
        mass: Number(mass),
        omega: Number(omega),
        x_min: -5.0,
        x_max: 5.0,
        points: 1000,
        num_states: Number(numStates),
      });

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function createPath(values, xValues, xScale, yScale, yOffset = 0) {
    if (!values || values.length === 0) {
      return "";
    }

    return values
      .map((value, index) => {
        const x = xScale(xValues[index]);
        const y = yScale(value + yOffset);

        return `${index === 0 ? "M" : "L"} ${x} ${y}`;
      })
      .join(" ");
  }

  function OscillatorGraph() {
    if (!result) {
      return null;
    }

    const width = 900;
    const height = 500;

    const paddingLeft = 65;
    const paddingRight = 25;
    const paddingTop = 25;
    const paddingBottom = 55;

    const plotWidth =
      width - paddingLeft - paddingRight;

    const plotHeight =
      height - paddingTop - paddingBottom;

    const xValues = result.position;
    const potential = result.potential;
    const energies = result.energy_levels;

    const maxEnergy =
      Math.max(...energies) * 1.35;

    const maxPotential =
      Math.max(...potential);

    const yMax = Math.max(
      maxEnergy,
      maxPotential
    );

    const xMin = result.simulation_parameters.x_min;
    const xMax = result.simulation_parameters.x_max;

    const xScale = (x) =>
      paddingLeft +
      ((x - xMin) / (xMax - xMin)) *
        plotWidth;

    const yScale = (y) =>
      paddingTop +
      plotHeight -
      (y / yMax) * plotHeight;

    const potentialPath = createPath(
      potential,
      xValues,
      xScale,
      yScale
    );

    return (
      <div className="oscillator-graph-container">
        <svg
          className="oscillator-graph"
          viewBox={`0 0 ${width} ${height}`}
          role="img"
          aria-label="Quantum harmonic oscillator energy levels and wavefunctions"
        >
          <line
            x1={paddingLeft}
            y1={paddingTop}
            x2={paddingLeft}
            y2={height - paddingBottom}
            stroke="#17202a"
            strokeWidth="1.5"
          />

          <line
            x1={paddingLeft}
            y1={height - paddingBottom}
            x2={width - paddingRight}
            y2={height - paddingBottom}
            stroke="#17202a"
            strokeWidth="1.5"
          />

          <path
            d={potentialPath}
            fill="none"
            stroke="#17202a"
            strokeWidth="2.5"
          />

          {energies.map((energyValue, index) => {
            const y = yScale(energyValue);

            const wavefunction =
              result.wavefunctions[index];

            const probability =
              result.probability_densities[index];

            const waveScale =
              yMax * 0.16;

            const wavePath = createPath(
              wavefunction.map(
                (value) =>
                  value * waveScale
              ),
              xValues,
              xScale,
              yScale,
              energyValue
            );

            const probabilityPath =
              createPath(
                probability.map(
                  (value) =>
                    value * waveScale
                ),
                xValues,
                xScale,
                yScale,
                energyValue
              );

            return (
              <g key={index}>
                <line
                  x1={paddingLeft}
                  y1={y}
                  x2={width - paddingRight}
                  y2={y}
                  stroke="#7b8794"
                  strokeWidth="1"
                  strokeDasharray="6 5"
                />

                <path
                  d={wavePath}
                  fill="none"
                  stroke="#17202a"
                  strokeWidth="1.8"
                />

                <path
                  d={probabilityPath}
                  fill="none"
                  stroke="#6c757d"
                  strokeWidth="1.4"
                />

                <text
                  x={paddingLeft - 10}
                  y={y + 4}
                  textAnchor="end"
                  fontSize="13"
                  fill="#17202a"
                >
                  n={index}
                </text>
              </g>
            );
          })}

          <text
            x={width / 2}
            y={height - 12}
            textAnchor="middle"
            fontSize="14"
          >
            Position x
          </text>

          <text
            x="18"
            y={height / 2}
            textAnchor="middle"
            fontSize="14"
            transform={`rotate(-90 18 ${height / 2})`}
          >
            Energy / Wavefunction
          </text>
        </svg>

        <div className="oscillator-legend">
          <span>
            <strong>Solid curve:</strong> harmonic potential
          </span>

          <span>
            <strong>Dashed lines:</strong> energy levels
          </span>

          <span>
            <strong>Wave curves:</strong> quantum states
          </span>

          <span>
            <strong>Probability curves:</strong> |psi|^2
          </span>
        </div>
      </div>
    );
  }

  return (
    <main className="lab-container">
      <header className="lab-header">
        <p className="lab-label">
          QUANTUM PHYSICS LABORATORY
        </p>

        <h1>Quantum Harmonic Oscillator</h1>

        <p className="lab-description">
          Explore quantized energy levels and the
          corresponding wavefunctions of a quantum
          harmonic oscillator.
        </p>
      </header>

      <section className="lab-card">
        <h2>Simulation Parameters</h2>

        <form onSubmit={handleCalculate}>
          <div className="parameter-grid">
            <label>
              Mass
              <input
                type="number"
                step="any"
                min="0.000001"
                value={mass}
                onChange={(event) =>
                  setMass(event.target.value)
                }
              />
            </label>

            <label>
              Angular Frequency
              <input
                type="number"
                step="any"
                min="0.000001"
                value={omega}
                onChange={(event) =>
                  setOmega(event.target.value)
                }
              />
            </label>

            <label>
              Number of States
              <input
                type="number"
                min="1"
                max="10"
                value={numStates}
                onChange={(event) =>
                  setNumStates(event.target.value)
                }
              />
            </label>
          </div>

          <button
            type="submit"
            className="calculate-button"
            disabled={loading}
          >
            {loading
              ? "Calculating..."
              : "Run Simulation"}
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
            <h2>Energy Levels & Wavefunctions</h2>

            <OscillatorGraph />
          </section>

          <section className="lab-card">
            <h2>Energy Levels</h2>

            <div className="results-grid">
              {result.energy_levels.map(
                (energyValue, index) => (
                  <div
                    className="result-item"
                    key={index}
                  >
                    <span>
                      Quantum number n = {index}
                    </span>

                    <strong>
                      {Number(
                        energyValue
                      ).toFixed(6)}
                    </strong>

                    <small>
                      E<sub>n</sub>
                    </small>
                  </div>
                )
              )}
            </div>
          </section>

          <section className="lab-card">
            <h2>Physics Model</h2>

            <div className="equation-block">
              <h3>Energy Quantization</h3>

              <p className="equation">
                E<sub>n</sub> = hbar omega (n + 1/2)
              </p>

              <p>
                The quantum harmonic oscillator has
                discrete energy levels. The lowest
                possible state still contains non-zero
                ground-state energy.
              </p>
            </div>

            <div className="equation-block">
              <h3>Simulation Parameters</h3>

              <div className="substitution">
                <p>
                  <strong>Mass:</strong>{" "}
                  {result.simulation_parameters.mass}
                </p>

                <p>
                  <strong>Angular frequency:</strong>{" "}
                  {result.simulation_parameters.omega}
                </p>

                <p>
                  <strong>Number of states:</strong>{" "}
                  {result.simulation_parameters.num_states}
                </p>

                <p>
                  <strong>Position range:</strong>{" "}
                  {result.simulation_parameters.x_min}
                  {" to "}
                  {result.simulation_parameters.x_max}
                </p>

                <p>
                  <strong>Spatial points:</strong>{" "}
                  {result.simulation_parameters.points}
                </p>
              </div>
            </div>

            <div className="explanation-box">
              <h3>Physical Interpretation</h3>

              <p>
                Increasing the angular frequency
                increases the spacing between adjacent
                energy levels. Increasing the mass changes
                the spatial width of the oscillator
                wavefunctions.
              </p>
            </div>
          </section>
        </>
      )}
    </main>
  );
}

export default HarmonicOscillatorLab;
