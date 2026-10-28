import { useState } from "react";
import { calculateSuperposition } from "../services/superpositionApi";

function SuperpositionLab() {
  const [alphaReal, setAlphaReal] = useState("0.70710678");
  const [alphaImag, setAlphaImag] = useState("0");

  const [betaReal, setBetaReal] = useState("0.70710678");
  const [betaImag, setBetaImag] = useState("0");

  const [shots, setShots] = useState("1000");

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleCalculate(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await calculateSuperposition({
        alpha_real: Number(alphaReal),
        alpha_imag: Number(alphaImag),
        beta_real: Number(betaReal),
        beta_imag: Number(betaImag),
        shots: Number(shots),
      });

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function probabilityPercent(value) {
    return `${(value * 100).toFixed(2)}%`;
  }

  function ProbabilityChart() {
    if (!result) {
      return null;
    }

    const width = 760;
    const height = 430;

    const paddingLeft = 70;
    const paddingRight = 35;
    const paddingTop = 35;
    const paddingBottom = 70;

    const chartWidth =
      width - paddingLeft - paddingRight;

    const chartHeight =
      height - paddingTop - paddingBottom;

    const labels = ["|0>", "|1>"];

    const theoretical = [
      result.probabilities.zero,
      result.probabilities.one,
    ];

    const observed = [
      result.measurement.observed_probability_zero,
      result.measurement.observed_probability_one,
    ];

    const groupWidth = chartWidth / labels.length;
    const barWidth = 70;
    const gap = 18;

    function yScale(value) {
      return (
        paddingTop +
        chartHeight -
        value * chartHeight
      );
    }

    return (
      <div className="probability-chart-container">
        <svg
          className="probability-chart"
          viewBox={`0 0 ${width} ${height}`}
          role="img"
          aria-label="Theoretical and observed quantum measurement probabilities"
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

          {[0, 0.25, 0.5, 0.75, 1].map(
            (value) => {
              const y = yScale(value);

              return (
                <g key={value}>
                  <line
                    x1={paddingLeft}
                    y1={y}
                    x2={width - paddingRight}
                    y2={y}
                    stroke="#dfe4e8"
                    strokeWidth="1"
                  />

                  <text
                    x={paddingLeft - 10}
                    y={y + 4}
                    textAnchor="end"
                    fontSize="12"
                    fill="#626d78"
                  >
                    {Math.round(value * 100)}%
                  </text>
                </g>
              );
            }
          )}

          {labels.map((label, index) => {
            const center =
              paddingLeft +
              groupWidth * index +
              groupWidth / 2;

            const theoreticalX =
              center -
              barWidth -
              gap / 2;

            const observedX =
              center +
              gap / 2;

            const theoreticalY =
              yScale(theoretical[index]);

            const observedY =
              yScale(observed[index]);

            const baseline =
              height - paddingBottom;

            return (
              <g key={label}>
                <rect
                  x={theoreticalX}
                  y={theoreticalY}
                  width={barWidth}
                  height={baseline - theoreticalY}
                  fill="#17202a"
                  rx="6"
                />

                <rect
                  x={observedX}
                  y={observedY}
                  width={barWidth}
                  height={baseline - observedY}
                  fill="#6c757d"
                  rx="6"
                />

                <text
                  x={center}
                  y={height - 35}
                  textAnchor="middle"
                  fontSize="15"
                  fontWeight="600"
                  fill="#17202a"
                >
                  {label}
                </text>

                <text
                  x={theoreticalX + barWidth / 2}
                  y={theoreticalY - 10}
                  textAnchor="middle"
                  fontSize="12"
                  fill="#17202a"
                >
                  {(theoretical[index] * 100).toFixed(1)}%
                </text>

                <text
                  x={observedX + barWidth / 2}
                  y={observedY - 10}
                  textAnchor="middle"
                  fontSize="12"
                  fill="#626d78"
                >
                  {(observed[index] * 100).toFixed(1)}%
                </text>
              </g>
            );
          })}

          <text
            x={width / 2}
            y="20"
            textAnchor="middle"
            fontSize="16"
            fontWeight="600"
            fill="#17202a"
          >
            Measurement Probability
          </text>

          <rect
            x={paddingLeft}
            y={height - 18}
            width="14"
            height="14"
            rx="3"
            fill="#17202a"
          />

          <text
            x={paddingLeft + 22}
            y={height - 6}
            fontSize="12"
            fill="#626d78"
          >
            Theoretical
          </text>

          <rect
            x={paddingLeft + 115}
            y={height - 18}
            width="14"
            height="14"
            rx="3"
            fill="#6c757d"
          />

          <text
            x={paddingLeft + 137}
            y={height - 6}
            fontSize="12"
            fill="#626d78"
          >
            Observed
          </text>
        </svg>
      </div>
    );
  }

  return (
    <main className="lab-container">
      <header className="lab-header">
        <p className="lab-label">
          QUANTUM PHYSICS LABORATORY
        </p>

        <h1>Quantum Superposition & Measurement</h1>

        <p className="lab-description">
          Explore how a qubit can exist in a superposition
          of quantum states and how measurement produces
          probabilistic outcomes.
        </p>
      </header>

      <section className="lab-card">
        <h2>Quantum State</h2>

        <p>
          The qubit is represented as:
        </p>

        <p className="equation">
          |psi&gt; = alpha |0&gt; + beta |1&gt;
        </p>

        <form onSubmit={handleCalculate}>
          <div className="parameter-grid">
            <label>
              Re(alpha)
              <input
                type="number"
                step="any"
                value={alphaReal}
                onChange={(event) =>
                  setAlphaReal(event.target.value)
                }
              />
            </label>

            <label>
              Im(alpha)
              <input
                type="number"
                step="any"
                value={alphaImag}
                onChange={(event) =>
                  setAlphaImag(event.target.value)
                }
              />
            </label>

            <label>
              Re(beta)
              <input
                type="number"
                step="any"
                value={betaReal}
                onChange={(event) =>
                  setBetaReal(event.target.value)
                }
              />
            </label>

            <label>
              Im(beta)
              <input
                type="number"
                step="any"
                value={betaImag}
                onChange={(event) =>
                  setBetaImag(event.target.value)
                }
              />
            </label>

            <label>
              Measurement Shots
              <input
                type="number"
                min="1"
                max="100000"
                value={shots}
                onChange={(event) =>
                  setShots(event.target.value)
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
              : "Measure Qubit"}
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
            <h2>Quantum State</h2>

            <div className="equation-block">
              <p className="equation">
                |psi&gt; = (
                {result.state.alpha_real.toFixed(6)}
                {" + "}
                {result.state.alpha_imag.toFixed(6)}
                i)|0&gt;
                {" + "}
                (
                {result.state.beta_real.toFixed(6)}
                {" + "}
                {result.state.beta_imag.toFixed(6)}
                i)|1&gt;
              </p>

              <p>
                The state has been normalized so that the
                total measurement probability is equal to 1.
              </p>
            </div>
          </section>

          <section className="lab-card">
            <h2>Measurement Probabilities</h2>

            <div className="results-grid">
              <div className="result-item">
                <span>P(0)</span>

                <strong>
                  {probabilityPercent(
                    result.probabilities.zero
                  )}
                </strong>

                <small>
                  Probability of measuring |0&gt;
                </small>
              </div>

              <div className="result-item">
                <span>P(1)</span>

                <strong>
                  {probabilityPercent(
                    result.probabilities.one
                  )}
                </strong>

                <small>
                  Probability of measuring |1&gt;
                </small>
              </div>
            </div>
          </section>

          <section className="lab-card">
            <h2>Theoretical vs Observed</h2>

            <ProbabilityChart />
          </section>

          <section className="lab-card">
            <h2>Measurement Results</h2>

            <div className="measurement-bars">
              <div className="measurement-row">
                <div className="measurement-label">
                  <span>|0&gt;</span>
                  <strong>
                    {result.measurement.zero_count}
                  </strong>
                </div>

                <div className="measurement-track">
                  <div
                    className="measurement-fill"
                    style={{
                      width: `${result.measurement
                        .observed_probability_zero * 100}%`,
                    }}
                  />
                </div>
              </div>

              <div className="measurement-row">
                <div className="measurement-label">
                  <span>|1&gt;</span>
                  <strong>
                    {result.measurement.one_count}
                  </strong>
                </div>

                <div className="measurement-track">
                  <div
                    className="measurement-fill"
                    style={{
                      width: `${result.measurement
                        .observed_probability_one * 100}%`,
                    }}
                  />
                </div>
              </div>
            </div>

            <p className="model-note">
              Each measurement run is sampled randomly
              according to the theoretical quantum
              probabilities.
            </p>
          </section>

          <section className="lab-card">
            <h2>Physical Interpretation</h2>

            <div className="explanation-box">
              <p>
                Before measurement, the qubit is described
                by a superposition of |0&gt; and |1&gt;.
              </p>

              <p>
                When the qubit is measured in the
                computational basis, the result is either
                |0&gt; or |1&gt;. The probabilities are
                determined by the squared magnitudes of the
                corresponding amplitudes.
              </p>

              <p>
                Repeating the experiment produces different
                observed frequencies, while the theoretical
                probabilities remain fixed for the same
                quantum state.
              </p>

              <p>
                Increasing the number of measurement shots
                makes the observed frequencies statistically
                converge toward the theoretical probabilities.
              </p>
            </div>
          </section>
        </>
      )}
    </main>
  );
}

export default SuperpositionLab;
