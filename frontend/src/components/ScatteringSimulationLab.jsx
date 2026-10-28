import { useEffect, useMemo, useState } from "react";
import { simulatePhi4Scattering } from "../services/scatteringSimulationApi";

export default function ScatteringSimulationLab() {
  const [mass, setMass] = useState("1");
  const [sqrtS, setSqrtS] = useState("5");
  const [lambda, setLambda] = useState("1");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [running, setRunning] = useState(false);
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    if (!result) {
      return undefined;
    }

    let frame;
    const start = performance.now();

    const animate = (time) => {
      setPhase(((time - start) / 1800) % 1);
      frame = requestAnimationFrame(animate);
    };

    frame = requestAnimationFrame(animate);

    return () => cancelAnimationFrame(frame);
  }, [result]);

  async function runSimulation() {
    try {
      setError("");
      setRunning(true);

      const payload = {
        mass: Number(mass),
        sqrt_s: Number(sqrtS),
        lambda_coupling: Number(lambda),
        angular_points: 73,
      };

      const data = await simulatePhi4Scattering(payload);
      setResult(data);
    } catch (err) {
      setError(err.message || "Scattering simulation failed.");
      setResult(null);
    } finally {
      setRunning(false);
    }
  }

  const plot = useMemo(() => {
    if (!result) {
      return null;
    }

    const points = result.angular_distribution;

    const width = 820;
    const height = 330;
    const left = 75;
    const right = 30;
    const top = 30;
    const bottom = 55;

    const maxValue = Math.max(
      ...points.map(
        (point) => point.differential_cross_section
      ),
      1e-30
    );

    const plotWidth = width - left - right;
    const plotHeight = height - top - bottom;

    const path = points
      .map((point, index) => {
        const x =
          left +
          (index / (points.length - 1)) * plotWidth;

        const y =
          top +
          (1 -
            point.differential_cross_section /
              maxValue) *
            plotHeight;

        return `${index === 0 ? "M" : "L"} ${x} ${y}`;
      })
      .join(" ");

    return {
      width,
      height,
      left,
      right,
      top,
      bottom,
      plotWidth,
      plotHeight,
      path,
      maxValue,
    };
  }, [result]);

  const event = useMemo(() => {
    const progress = phase;

    const incoming = Math.min(progress / 0.45, 1);
    const outgoing = Math.max(
      0,
      Math.min((progress - 0.45) / 0.55, 1)
    );

    return {
      incoming,
      outgoing,
    };
  }, [phase]);

  const threshold =
    Number(sqrtS) < 2 * Number(mass);

  return (
    <div
      style={{
        maxWidth: "1100px",
        margin: "0 auto",
        padding: "20px",
      }}
    >
      <h2>f4 Scattering Simulation Lab</h2>

      <p>
        Explore tree-level scalar scattering:
        {" "}
        <strong>f + f ? f + f</strong>
      </p>

      <p>
        This laboratory calculates the scattering amplitude and
        cross section from the f4 interaction rather than merely
        displaying a Feynman diagram.
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(210px, 1fr))",
          gap: "14px",
          marginTop: "20px",
        }}
      >
        <label>
          Scalar mass m
          <input
            type="number"
            min="0"
            step="0.1"
            value={mass}
            onChange={(event) =>
              setMass(event.target.value)
            }
            style={{
              width: "100%",
              marginTop: "6px",
              padding: "8px",
            }}
          />
        </label>

        <label>
          Center-of-mass energy vs
          <input
            type="number"
            min="0.01"
            step="0.1"
            value={sqrtS}
            onChange={(event) =>
              setSqrtS(event.target.value)
            }
            style={{
              width: "100%",
              marginTop: "6px",
              padding: "8px",
            }}
          />
        </label>

        <label>
          Coupling ?
          <input
            type="number"
            min="0"
            step="0.1"
            value={lambda}
            onChange={(event) =>
              setLambda(event.target.value)
            }
            style={{
              width: "100%",
              marginTop: "6px",
              padding: "8px",
            }}
          />
        </label>
      </div>

      {threshold && (
        <p
          style={{
            marginTop: "15px",
            padding: "12px",
            border: "1px solid currentColor",
          }}
        >
          Threshold condition: vs must be at least 2m for
          two-particle scattering.
        </p>
      )}

      <button
        onClick={runSimulation}
        disabled={running || threshold}
        style={{
          marginTop: "18px",
          padding: "10px 18px",
          cursor:
            running || threshold
              ? "not-allowed"
              : "pointer",
        }}
      >
        {running
          ? "Calculating..."
          : "Run Scattering Simulation"}
      </button>

      {error && (
        <p style={{ marginTop: "15px" }}>
          {error}
        </p>
      )}

      {result && (
        <>
          <section style={{ marginTop: "28px" }}>
            <h3>1. Scattering Event</h3>

            <p>
              The animation represents the calculated
              two-particle collision at the tree-level
              f4 contact vertex.
            </p>

            <svg
              viewBox="0 0 900 420"
              width="100%"
              role="img"
              aria-label="Animated phi four scattering event"
              style={{
                border: "1px solid currentColor",
                maxHeight: "430px",
              }}
            >
              <line
                x1="70"
                y1="120"
                x2="450"
                y2="210"
                stroke="currentColor"
                strokeWidth="4"
                opacity="0.25"
              />

              <line
                x1="70"
                y1="300"
                x2="450"
                y2="210"
                stroke="currentColor"
                strokeWidth="4"
                opacity="0.25"
              />

              <line
                x1="450"
                y1="210"
                x2="830"
                y2="120"
                stroke="currentColor"
                strokeWidth="4"
                opacity="0.25"
              />

              <line
                x1="450"
                y1="210"
                x2="830"
                y2="300"
                stroke="currentColor"
                strokeWidth="4"
                opacity="0.25"
              />

              <circle
                cx="450"
                cy="210"
                r="26"
                fill="none"
                stroke="currentColor"
                strokeWidth="4"
              />

              <circle
                cx={
                  70 +
                  380 * event.incoming
                }
                cy={
                  120 +
                  90 * event.incoming
                }
                r="12"
                fill="currentColor"
              />

              <circle
                cx={
                  70 +
                  380 * event.incoming
                }
                cy={
                  300 -
                  90 * event.incoming
                }
                r="12"
                fill="currentColor"
              />

              <circle
                cx={
                  450 +
                  380 * event.outgoing
                }
                cy={
                  210 -
                  90 * event.outgoing
                }
                r="12"
                fill="currentColor"
              />

              <circle
                cx={
                  450 +
                  380 * event.outgoing
                }
                cy={
                  210 +
                  90 * event.outgoing
                }
                r="12"
                fill="currentColor"
              />

              <text x="55" y="90" fontSize="24">
                p1
              </text>

              <text x="55" y="335" fontSize="24">
                p2
              </text>

              <text x="805" y="90" fontSize="24">
                p3
              </text>

              <text x="805" y="335" fontSize="24">
                p4
              </text>

              <text
                x="420"
                y="165"
                fontSize="24"
              >
                -i?
              </text>

              <text
                x="390"
                y="375"
                fontSize="18"
              >
                Tree-level contact interaction
              </text>
            </svg>
          </section>

          <section style={{ marginTop: "28px" }}>
            <h3>2. Collision Kinematics</h3>

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit, minmax(190px, 1fr))",
                gap: "12px",
              }}
            >
              <Metric
                label="vs"
                value={result.kinematics.center_of_mass_energy.toFixed(
                  4
                )}
              />

              <Metric
                label="Incoming momentum"
                value={result.kinematics.incoming_momentum.toFixed(
                  4
                )}
              />

              <Metric
                label="Outgoing momentum"
                value={result.kinematics.outgoing_momentum.toFixed(
                  4
                )}
              />

              <Metric
                label="Threshold"
                value={result.kinematics.threshold_energy.toFixed(
                  4
                )}
              />
            </div>
          </section>

          <section style={{ marginTop: "28px" }}>
            <h3>3. Scattering Amplitude</h3>

            <div
              style={{
                padding: "18px",
                border: "1px solid currentColor",
              }}
            >
              <p>
                <strong>Tree-level Feynman rule:</strong>
              </p>

              <p
                style={{
                  fontSize: "24px",
                  fontFamily: "serif",
                }}
              >
                M = -i?
              </p>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns:
                    "repeat(auto-fit, minmax(190px, 1fr))",
                  gap: "12px",
                }}
              >
                <Metric
                  label="Re(M)"
                  value={result.amplitude.real.toFixed(6)}
                />

                <Metric
                  label="Im(M)"
                  value={result.amplitude.imaginary.toFixed(
                    6
                  )}
                />

                <Metric
                  label="|M|"
                  value={result.amplitude.magnitude.toFixed(
                    6
                  )}
                />

                <Metric
                  label="|M|²"
                  value={result.amplitude.squared_magnitude.toFixed(
                    6
                  )}
                />
              </div>
            </div>
          </section>

          <section style={{ marginTop: "28px" }}>
            <h3>4. Differential Cross Section</h3>

            <p>
              For this tree-level identical-scalar process,
              the amplitude is independent of the scattering
              angle. Therefore the angular distribution is
              isotropic.
            </p>

            <svg
              viewBox={`0 0 ${plot.width} ${plot.height}`}
              width="100%"
              role="img"
              aria-label="Differential cross section versus scattering angle"
              style={{
                border: "1px solid currentColor",
              }}
            >
              <line
                x1={plot.left}
                y1={
                  plot.height -
                  plot.bottom
                }
                x2={
                  plot.width -
                  plot.right
                }
                y2={
                  plot.height -
                  plot.bottom
                }
                stroke="currentColor"
                strokeWidth="2"
              />

              <line
                x1={plot.left}
                y1={plot.top}
                x2={plot.left}
                y2={
                  plot.height -
                  plot.bottom
                }
                stroke="currentColor"
                strokeWidth="2"
              />

              <path
                d={plot.path}
                fill="none"
                stroke="currentColor"
                strokeWidth="4"
              />

              <text
                x={plot.left - 8}
                y={plot.height - 15}
                fontSize="17"
              >
                0°
              </text>

              <text
                x={plot.width / 2 - 15}
                y={plot.height - 15}
                fontSize="17"
              >
                90°
              </text>

              <text
                x={plot.width - 58}
                y={plot.height - 15}
                fontSize="17"
              >
                180°
              </text>

              <text
                x="10"
                y="22"
                fontSize="17"
              >
                ds/dO
              </text>

              <text
                x={plot.width / 2 - 90}
                y={plot.height - 2}
                fontSize="17"
              >
                Scattering angle ?
              </text>
            </svg>

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit, minmax(220px, 1fr))",
                gap: "12px",
                marginTop: "15px",
              }}
            >
              <Metric
                label="ds/dO"
                value={result.cross_section.differential_value.toExponential(
                  6
                )}
              />

              <Metric
                label="Total s"
                value={result.cross_section.total_value.toExponential(
                  6
                )}
              />
            </div>
          </section>

          <section style={{ marginTop: "28px" }}>
            <h3>5. What the Simulation Means</h3>

            <div
              style={{
                display: "grid",
                gap: "10px",
              }}
            >
              {result.interpretation.map(
                (item, index) => (
                  <p key={index}>
                    • {item}
                  </p>
                )
              )}
            </div>
          </section>

          <section style={{ marginTop: "28px" }}>
            <h3>6. Physics Pipeline</h3>

            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: "8px",
                alignItems: "center",
              }}
            >
              <Step label="f4 interaction" />
              <Arrow />
              <Step label="Feynman rule" />
              <Arrow />
              <Step label="M = -i?" />
              <Arrow />
              <Step label="|M|²" />
              <Arrow />
              <Step label="ds/dO" />
              <Arrow />
              <Step label="s" />
            </div>
          </section>
        </>
      )}
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div
      style={{
        padding: "14px",
        border: "1px solid currentColor",
      }}
    >
      <div
        style={{
          fontSize: "13px",
          opacity: 0.7,
        }}
      >
        {label}
      </div>

      <div
        style={{
          fontSize: "21px",
          fontWeight: "600",
          marginTop: "5px",
        }}
      >
        {value}
      </div>
    </div>
  );
}

function Step({ label }) {
  return (
    <div
      style={{
        padding: "9px 12px",
        border: "1px solid currentColor",
      }}
    >
      {label}
    </div>
  );
}

function Arrow() {
  return <span aria-hidden="true">?</span>;
}
