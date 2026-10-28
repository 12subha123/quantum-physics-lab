import { useState } from "react";
import { calculateQCDAngularObservable } from "../services/qcdAngularObservableApi";

export default function QCDAngularObservableLab() {
  const [sqrtS, setSqrtS] = useState(10.0);
  const [alphaS, setAlphaS] = useState(0.118);
  const [angularCut, setAngularCut] = useState(0.1);
  const [points, setPoints] = useState(100);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function calculate() {
    setLoading(true);
    setError("");

    try {
      const data = await calculateQCDAngularObservable({
        sqrt_s: Number(sqrtS),
        alpha_s: Number(alphaS),
        angular_cut: Number(angularCut),
        points: Number(points),
      });

      setResult(data);
    } catch (err) {
      setResult(null);
      setError(err.message || "QCD calculation failed.");
    } finally {
      setLoading(false);
    }
  }

  const chartPoints = result?.points || [];

  const width = 760;
  const height = 360;
  const padding = 55;

  const values = chartPoints.map(
    (point) => point.differential_cross_section
  );

  const maxY = Math.max(...values, 1e-30);

  const path = chartPoints
    .map((point, index) => {
      const x =
        padding +
        (index / Math.max(chartPoints.length - 1, 1)) *
          (width - 2 * padding);

      const y =
        height -
        padding -
        (point.differential_cross_section / maxY) *
          (height - 2 * padding);

      return `${index === 0 ? "M" : "L"} ${x} ${y}`;
    })
    .join(" ");

  return (
    <section className="experiment-container">
      <h2>QCD Angular Observable Lab</h2>

      <p>
        Tree-level massless QCD calculation for
        <strong> q + anti-q → g + g </strong>
        with an explicit angular cut.
      </p>

      <div className="experiment-grid">
        <label>
          √s
          <input
            type="number"
            min="0.01"
            step="0.1"
            value={sqrtS}
            onChange={(event) => setSqrtS(event.target.value)}
          />
        </label>

        <label>
          αₛ
          <input
            type="number"
            min="0.0001"
            step="0.001"
            value={alphaS}
            onChange={(event) => setAlphaS(event.target.value)}
          />
        </label>

        <label>
          Angular cut
          <input
            type="number"
            min="0.0001"
            max="1.56"
            step="0.01"
            value={angularCut}
            onChange={(event) => setAngularCut(event.target.value)}
          />
        </label>

        <label>
          Angular points
          <input
            type="number"
            min="2"
            max="2000"
            step="1"
            value={points}
            onChange={(event) => setPoints(event.target.value)}
          />
        </label>
      </div>

      <button onClick={calculate} disabled={loading}>
        {loading ? "Calculating..." : "Calculate QCD Observable"}
      </button>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {result && (
        <>
          <div className="results-grid">
            <div>
              <strong>Status</strong>
              <span>{result.valid ? "Valid" : "Invalid"}</span>
            </div>

            <div>
              <strong>√s</strong>
              <span>{result.sqrt_s}</span>
            </div>

            <div>
              <strong>αₛ</strong>
              <span>{result.alpha_s}</span>
            </div>

            <div>
              <strong>Angular points</strong>
              <span>{result.point_count}</span>
            </div>

            <div>
              <strong>Total cross section</strong>
              <span>
                {result.total_cross_section !== null
                  ? result.total_cross_section.toExponential(6)
                  : "N/A"}
              </span>
            </div>
          </div>

          <div className="qcd-chart-container">
            <h3>dσ/dΩ vs scattering angle</h3>

            <svg
              viewBox={`0 0 ${width} ${height}`}
              width="100%"
              role="img"
              aria-label="QCD differential cross section versus scattering angle"
            >
              <line
                x1={padding}
                y1={height - padding}
                x2={width - padding}
                y2={height - padding}
                stroke="currentColor"
              />

              <line
                x1={padding}
                y1={padding}
                x2={padding}
                y2={height - padding}
                stroke="currentColor"
              />

              <path
                d={path}
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
              />

              <text x={width / 2} y={height - 12} textAnchor="middle">
                θ (radians)
              </text>

              <text
                x="16"
                y={height / 2}
                textAnchor="middle"
                transform={`rotate(-90 16 ${height / 2})`}
              >
                dσ/dΩ
              </text>

              <text x={padding} y={height - padding + 22}>
                {chartPoints.length
                  ? chartPoints[0].theta.toFixed(2)
                  : "0"}
              </text>

              <text
                x={width - padding}
                y={height - padding + 22}
                textAnchor="end"
              >
                {chartPoints.length
                  ? chartPoints[chartPoints.length - 1].theta.toFixed(2)
                  : "π"}
              </text>

              <text x={padding - 8} y={padding - 8} textAnchor="end">
                {maxY.toExponential(2)}
              </text>
            </svg>
          </div>

          <div className="physics-note">
            <strong>Scientific scope:</strong>{" "}
            {result.scientific_scope}
          </div>
        </>
      )}
    </section>
  );
}
