import { useEffect, useRef, useState } from "react";

import {
  calculateDirac,
  simulateDirac,
} from "../services/diracApi";

function drawDiracField(canvas, result, frameIndex) {
  if (!canvas || !result) {
    return;
  }

  const context = canvas.getContext("2d");

  if (!context) {
    return;
  }

  const width = canvas.width;
  const height = canvas.height;

  context.clearRect(0, 0, width, height);

  const padding = {
    left: 55,
    right: 20,
    top: 30,
    bottom: 45,
  };

  const plotWidth =
    width - padding.left - padding.right;

  const plotHeight =
    height - padding.top - padding.bottom;

  const x = result.x;
  const density =
    result.probability_density[frameIndex];

  const upper =
    result.upper_component_density[frameIndex];

  const lower =
    result.lower_component_density[frameIndex];

  const xMin = x[0];
  const xMax = x[x.length - 1];

  let maxValue = 0;

  for (const frame of result.probability_density) {
    for (const value of frame) {
      maxValue = Math.max(maxValue, value);
    }
  }

  maxValue = Math.max(maxValue, 1e-9) * 1.15;

  const mapX = (value) =>
    padding.left +
    ((value - xMin) / (xMax - xMin)) *
      plotWidth;

  const mapY = (value) =>
    padding.top +
    (1 - value / maxValue) *
      plotHeight;

  context.font = "13px Arial";
  context.fillStyle = "#333";

  context.strokeStyle = "#aaa";
  context.lineWidth = 1;

  context.beginPath();
  context.moveTo(
    padding.left,
    height - padding.bottom
  );
  context.lineTo(
    width - padding.right,
    height - padding.bottom
  );
  context.stroke();

  function drawCurve(values, lineColor, lineWidth) {
    context.beginPath();

    for (let i = 0; i < x.length; i += 1) {
      const px = mapX(x[i]);
      const py = mapY(values[i]);

      if (i === 0) {
        context.moveTo(px, py);
      } else {
        context.lineTo(px, py);
      }
    }

    context.strokeStyle = lineColor;
    context.lineWidth = lineWidth;
    context.stroke();
  }

  drawCurve(
    density,
    "#2563eb",
    3
  );

  drawCurve(
    upper,
    "#16a34a",
    1.5
  );

  drawCurve(
    lower,
    "#dc2626",
    1.5
  );

  context.fillStyle = "#333";
  context.font = "bold 14px Arial";

  context.fillText(
    "Dirac probability density |ψ|²",
    padding.left,
    18
  );

  context.font = "12px Arial";

  context.fillText(
    "Total density",
    padding.left,
    32
  );

  context.fillStyle = "#16a34a";
  context.fillText(
    "Upper component",
    padding.left + 110,
    32
  );

  context.fillStyle = "#dc2626";
  context.fillText(
    "Lower component",
    padding.left + 235,
    32
  );

  context.fillStyle = "#333";

  context.fillText(
    `x = ${xMin.toFixed(1)}`,
    padding.left,
    height - 15
  );

  context.fillText(
    `x = ${xMax.toFixed(1)}`,
    width - 75,
    height - 15
  );

  context.fillText(
    maxValue.toFixed(3),
    8,
    padding.top + 5
  );

  context.fillText(
    "0",
    25,
    height - padding.bottom + 4
  );
}

export default function DiracLab() {
  const canvasRef = useRef(null);

  const [mass, setMass] = useState("1.0");
  const [momentum, setMomentum] = useState("2.0");
  const [amplitude, setAmplitude] = useState("1.0");
  const [width, setWidth] = useState("1.5");
  const [domainLength, setDomainLength] =
    useState("20");
  const [duration, setDuration] =
    useState("8");
  const [points, setPoints] =
    useState("256");
  const [frames, setFrames] =
    useState("100");

  const [summary, setSummary] =
    useState(null);

  const [result, setResult] =
    useState(null);

  const [currentFrame, setCurrentFrame] =
    useState(0);

  const [playing, setPlaying] =
    useState(false);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  useEffect(() => {
    if (!result) {
      return;
    }

    drawDiracField(
      canvasRef.current,
      result,
      currentFrame
    );
  }, [result, currentFrame]);

  useEffect(() => {
    if (!playing || !result) {
      return undefined;
    }

    const timer = setInterval(() => {
      setCurrentFrame((previous) => {
        const last =
          result.probability_density.length - 1;

        if (previous >= last) {
          setPlaying(false);
          return 0;
        }

        return previous + 1;
      });
    }, 70);

    return () => clearInterval(timer);
  }, [playing, result]);

  async function handleSummary() {
    setLoading(true);
    setError("");

    try {
      const data = await calculateDirac(
        momentum,
        mass
      );

      setSummary(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Dirac calculation failed."
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleSimulation() {
    setLoading(true);
    setError("");
    setPlaying(false);

    try {
      const data = await simulateDirac({
        mass,
        momentum,
        amplitude,
        width,
        domain_length: domainLength,
        duration,
        points,
        frames,
      });

      setResult(data);
      setCurrentFrame(0);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Dirac simulation failed."
      );
    } finally {
      setLoading(false);
    }
  }

  const activeTime =
    result?.times?.[currentFrame] ?? 0;

  const normDrift =
    result?.diagnostics?.relative_norm_drift ?? 0;

  return (
    <div className="experiment-card">
      <h2>Dirac Field Laboratory</h2>

      <p>
        Explore relativistic fermions through the
        Dirac equation and numerically evolve a
        localized free-fermion wave packet.
      </p>

      <p>
        <strong>Model:</strong> 1+1D free Dirac
        equation in natural units (ℏ = c = 1).
      </p>

      <hr />

      <h3>Relativistic Energy Spectrum</h3>

      <div className="control-grid">
        <label>
          Momentum
          <input
            type="number"
            step="0.1"
            value={momentum}
            onChange={(event) =>
              setMomentum(event.target.value)
            }
          />
        </label>

        <label>
          Mass
          <input
            type="number"
            step="0.1"
            min="0"
            value={mass}
            onChange={(event) =>
              setMass(event.target.value)
            }
          />
        </label>
      </div>

      <button
        type="button"
        onClick={handleSummary}
        disabled={loading}
      >
        Calculate Dirac Spectrum
      </button>

      {summary && (
        <div className="result-card">
          <p>
            <strong>Positive energy:</strong>{" "}
            {summary.positive_energy.toFixed(6)}
          </p>

          <p>
            <strong>Negative energy:</strong>{" "}
            {summary.negative_energy.toFixed(6)}
          </p>

          <p>
            <strong>Eigenvalue error:</strong>{" "}
            {summary.eigenvalue_error.toExponential(3)}
          </p>

          <p>
            <strong>Validation:</strong>{" "}
            {summary.validation_passed
              ? "Passed"
              : "Failed"}
          </p>

          <code>
            {summary.dispersion_relation}
          </code>
        </div>
      )}

      <hr />

      <h3>Numerical Dirac Wave Packet</h3>

      <div className="control-grid">
        <label>
          Mass
          <input
            type="number"
            step="0.1"
            min="0"
            value={mass}
            onChange={(event) =>
              setMass(event.target.value)
            }
          />
        </label>

        <label>
          Momentum
          <input
            type="number"
            step="0.1"
            value={momentum}
            onChange={(event) =>
              setMomentum(event.target.value)
            }
          />
        </label>

        <label>
          Amplitude
          <input
            type="number"
            step="0.1"
            min="0.01"
            value={amplitude}
            onChange={(event) =>
              setAmplitude(event.target.value)
            }
          />
        </label>

        <label>
          Width
          <input
            type="number"
            step="0.1"
            min="0.1"
            value={width}
            onChange={(event) =>
              setWidth(event.target.value)
            }
          />
        </label>

        <label>
          Domain Length
          <input
            type="number"
            step="1"
            min="2"
            value={domainLength}
            onChange={(event) =>
              setDomainLength(event.target.value)
            }
          />
        </label>

        <label>
          Duration
          <input
            type="number"
            step="0.5"
            min="0.1"
            value={duration}
            onChange={(event) =>
              setDuration(event.target.value)
            }
          />
        </label>

        <label>
          Spatial Points
          <input
            type="number"
            step="16"
            min="64"
            max="512"
            value={points}
            onChange={(event) =>
              setPoints(event.target.value)
            }
          />
        </label>

        <label>
          Animation Frames
          <input
            type="number"
            step="10"
            min="20"
            max="160"
            value={frames}
            onChange={(event) =>
              setFrames(event.target.value)
            }
          />
        </label>
      </div>

      <button
        type="button"
        onClick={handleSimulation}
        disabled={loading}
      >
        {loading
          ? "Running Dirac Simulation..."
          : "Run Numerical Dirac Simulation"}
      </button>

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      {result && (
        <div className="result-card">
          <h3>Live Relativistic Wave Packet</h3>

          <canvas
            ref={canvasRef}
            width={900}
            height={380}
            style={{
              width: "100%",
              maxWidth: "900px",
              display: "block",
              margin: "0 auto",
              border: "1px solid #ddd",
              borderRadius: "8px",
              background: "#fafafa",
            }}
          />

          <div className="simulation-controls">
            <button
              type="button"
              onClick={() =>
                setPlaying((value) => !value)
              }
            >
              {playing ? "Pause" : "Play"}
            </button>

            <input
              type="range"
              min="0"
              max={
                result.probability_density.length - 1
              }
              value={currentFrame}
              onChange={(event) => {
                setPlaying(false);
                setCurrentFrame(
                  Number(event.target.value)
                );
              }}
            />
          </div>

          <p>
            <strong>Simulation time:</strong>{" "}
            {activeTime.toFixed(3)}
          </p>

          <p>
            <strong>Norm drift:</strong>{" "}
            {(normDrift * 100).toExponential(3)}%
          </p>

          <p>
            <strong>Initial ⟨x⟩:</strong>{" "}
            {result.diagnostics.initial_expectation_x.toFixed(
              4
            )}
            {" · "}
            <strong>Final ⟨x⟩:</strong>{" "}
            {result.diagnostics.final_expectation_x.toFixed(
              4
            )}
          </p>

          <p>
            The blue curve is the total probability
            density |ψ|². The green and red curves show
            the two Dirac spinor-component densities.
          </p>

          <p>
            <strong>Scientific note:</strong> this is a
            numerical free-fermion Dirac simulation. It
            does not yet include electromagnetic
            interactions, particle creation, or the full
            quantum field-theoretic Standard Model.
          </p>
        </div>
      )}
    </div>
  );
}
