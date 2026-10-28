import { useEffect, useRef, useState } from "react";

import {
  calculateKleinGordon,
  simulateKleinGordon,
} from "../services/fieldTheoryApi";

function drawField(canvas, result, frameIndex) {
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
  const field = result.field[frameIndex];

  if (!x || !field || x.length !== field.length) {
    return;
  }

  const xMin = x[0];
  const xMax = x[x.length - 1];

  let maxAbs = 0;

  for (const frame of result.field) {
    for (const value of frame) {
      maxAbs = Math.max(maxAbs, Math.abs(value));
    }
  }

  maxAbs = Math.max(maxAbs, 1e-9) * 1.1;

  const mapX = (value) =>
    padding.left +
    ((value - xMin) / (xMax - xMin)) *
      plotWidth;

  const mapY = (value) =>
    padding.top +
    (0.5 - value / (2 * maxAbs)) *
      plotHeight;

  context.font = "13px Arial";
  context.fillStyle = "#333";
  context.strokeStyle = "#777";
  context.lineWidth = 1;

  context.beginPath();
  context.moveTo(
    padding.left,
    mapY(0)
  );
  context.lineTo(
    width - padding.right,
    mapY(0)
  );
  context.stroke();

  context.beginPath();
  context.moveTo(
    mapX(0),
    padding.top
  );
  context.lineTo(
    mapX(0),
    height - padding.bottom
  );
  context.stroke();

  context.beginPath();

  for (let i = 0; i < x.length; i += 1) {
    const px = mapX(x[i]);
    const py = mapY(field[i]);

    if (i === 0) {
      context.moveTo(px, py);
    } else {
      context.lineTo(px, py);
    }
  }

  context.strokeStyle = "#2563eb";
  context.lineWidth = 2.5;
  context.stroke();

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
    `+${maxAbs.toFixed(2)}`,
    8,
    padding.top + 5
  );

  context.fillText(
    "0",
    25,
    mapY(0) + 4
  );

  context.fillText(
    `-${maxAbs.toFixed(2)}`,
    5,
    height - padding.bottom
  );

  context.font = "bold 14px Arial";

  context.fillText(
    "Klein–Gordon field φ(x,t)",
    padding.left,
    18
  );
}

export default function KleinGordonLab() {
  const canvasRef = useRef(null);

  const [mass, setMass] = useState("1.0");
  const [amplitude, setAmplitude] = useState("1.0");
  const [width, setWidth] = useState("1.5");
  const [wavenumber, setWavenumber] = useState("2.0");
  const [domainLength, setDomainLength] = useState("20");
  const [duration, setDuration] = useState("8");
  const [points, setPoints] = useState("201");
  const [frames, setFrames] = useState("100");

  const [equationResult, setEquationResult] =
    useState(null);

  const [simulationResult, setSimulationResult] =
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
    if (!simulationResult) {
      return;
    }

    drawField(
      canvasRef.current,
      simulationResult,
      currentFrame
    );
  }, [simulationResult, currentFrame]);

  useEffect(() => {
    if (!playing || !simulationResult) {
      return undefined;
    }

    const timer = setInterval(() => {
      setCurrentFrame((previous) => {
        const last =
          simulationResult.field.length - 1;

        if (previous >= last) {
          setPlaying(false);
          return 0;
        }

        return previous + 1;
      });
    }, 70);

    return () => clearInterval(timer);
  }, [playing, simulationResult]);

  async function handleCalculate() {
    setLoading(true);
    setError("");

    try {
      const result =
        await calculateKleinGordon(mass);

      setEquationResult(result);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Klein-Gordon calculation failed."
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
      const result =
        await simulateKleinGordon({
          mass,
          amplitude,
          width,
          wavenumber,
          domain_length: domainLength,
          duration,
          points,
          frames,
        });

      setSimulationResult(result);
      setCurrentFrame(0);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Klein-Gordon simulation failed."
      );
    } finally {
      setLoading(false);
    }
  }

  const activeTime =
    simulationResult?.times?.[currentFrame] ?? 0;

  const diagnostics =
    simulationResult?.diagnostics;

  const energyDrift =
    diagnostics?.discrete_energy_relative_drift;

  return (
    <div className="experiment-card">
      <h2>Klein–Gordon Field Laboratory</h2>

      <p>
        Symbolically derive the Klein–Gordon equation
        and numerically evolve a scalar field in 1+1
        dimensions.
      </p>

      <p>
        <strong>Model:</strong> educational finite-difference
        simulation in natural units (ℏ = c = 1).
      </p>

      <hr />

      <h3>Symbolic Field Equation</h3>

      <div className="control-group">
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
        onClick={handleCalculate}
        disabled={loading}
      >
        {loading
          ? "Calculating..."
          : "Calculate Field Equation"}
      </button>

      {equationResult && (
        <div className="result-card">
          <p>
            <strong>Equation:</strong>
          </p>

          <code>
            {equationResult.equation}
          </code>
        </div>
      )}

      <hr />

      <h3>Numerical Field Simulation</h3>

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
          Wavenumber
          <input
            type="number"
            step="0.1"
            min="0"
            value={wavenumber}
            onChange={(event) =>
              setWavenumber(event.target.value)
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
            step="10"
            min="51"
            max="401"
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
          ? "Running Numerical Simulation..."
          : "Run Numerical Field Simulation"}
      </button>

      {error && (
        <p className="error-message">
          {error}
        </p>
      )}

      {simulationResult && (
        <div className="result-card">
          <h3>Live Numerical Field</h3>

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
                simulationResult.field.length - 1
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
            <strong>Spatial points:</strong>{" "}
            {simulationResult.parameters.points}
            {" · "}
            <strong>Frames:</strong>{" "}
            {simulationResult.parameters.frames}
          </p>

          <p>
            <strong>Time step:</strong>{" "}
            {simulationResult.parameters.time_step.toFixed(
              5
            )}
            {" · "}
            <strong>Spatial step:</strong>{" "}
            {simulationResult.parameters.spatial_step.toFixed(
              5
            )}
          </p>

          {diagnostics && (
            <div>
              <p>
                <strong>Initial maximum |φ|:</strong>{" "}
                {diagnostics.initial_max_abs_field.toFixed(
                  6
                )}
              </p>

              <p>
                <strong>Final maximum |φ|:</strong>{" "}
                {diagnostics.final_max_abs_field.toFixed(
                  6
                )}
              </p>

              <p>
                <strong>Discrete energy drift:</strong>{" "}
                {(energyDrift * 100).toFixed(4)}%
              </p>
            </div>
          )}

          <p>
            <strong>Interpretation:</strong> the curve is
            the numerically calculated scalar field
            φ(x,t). Moving the animation forward shows
            the actual finite-difference evolution rather
            than a pre-generated illustration.
          </p>
        </div>
      )}
    </div>
  );
}
