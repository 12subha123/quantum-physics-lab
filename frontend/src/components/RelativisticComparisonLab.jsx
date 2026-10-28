import { useEffect, useRef, useState } from "react";
import { runRelativisticComparison } from "../services/relativisticComparisonApi";


function drawCurve(
  canvas,
  x,
  values,
  title,
  yLabel,
  time,
) {
  if (!canvas || !x?.length || !values?.length) {
    return;
  }

  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;

  ctx.clearRect(0, 0, width, height);

  const margin = {
    left: 55,
    right: 20,
    top: 38,
    bottom: 35,
  };

  const plotWidth =
    width - margin.left - margin.right;
  const plotHeight =
    height - margin.top - margin.bottom;

  ctx.strokeStyle = "#94a3b8";
  ctx.lineWidth = 1;

  for (let i = 0; i <= 4; i += 1) {
    const y =
      margin.top +
      (plotHeight * i) / 4;

    ctx.beginPath();
    ctx.moveTo(margin.left, y);
    ctx.lineTo(width - margin.right, y);
    ctx.stroke();
  }

  let min = Math.min(...values);
  let max = Math.max(...values);

  if (min === max) {
    min -= 1;
    max += 1;
  }

  const padding = (max - min) * 0.08;
  min -= padding;
  max += padding;

  ctx.beginPath();

  values.forEach((value, index) => {
    const px =
      margin.left +
      (index / (values.length - 1)) * plotWidth;

    const py =
      margin.top +
      ((max - value) / (max - min)) * plotHeight;

    if (index === 0) {
      ctx.moveTo(px, py);
    } else {
      ctx.lineTo(px, py);
    }
  });

  ctx.strokeStyle = "#2563eb";
  ctx.lineWidth = 2;
  ctx.stroke();

  ctx.fillStyle = "#111827";
  ctx.font = "bold 15px sans-serif";
  ctx.fillText(title, margin.left, 20);

  ctx.font = "12px sans-serif";
  ctx.fillText(
    `${yLabel} ? t = ${Number(time).toFixed(2)}`,
    margin.left,
    height - 10,
  );

  ctx.fillText(
    `max ${max.toFixed(3)}`,
    width - 105,
    20,
  );
}


export default function RelativisticComparisonLab() {
  const [mass, setMass] = useState(1);
  const [momentum, setMomentum] = useState(2);
  const [amplitude, setAmplitude] = useState(1);
  const [width, setWidth] = useState(1.5);
  const [domainLength, setDomainLength] = useState(20);
  const [duration, setDuration] = useState(8);
  const [points, setPoints] = useState(128);
  const [frames, setFrames] = useState(80);

  const [result, setResult] = useState(null);
  const [frame, setFrame] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const kgCanvas = useRef(null);
  const diracCanvas = useRef(null);

  useEffect(() => {
    if (!playing || !result) {
      return undefined;
    }

    const timer = setInterval(() => {
      setFrame((current) => {
        const last =
          result.shared_parameters.frames - 1;

        if (current >= last) {
          setPlaying(false);
          return 0;
        }

        return current + 1;
      });
    }, 80);

    return () => clearInterval(timer);
  }, [playing, result]);

  useEffect(() => {
    if (!result) {
      return;
    }

    const index = Math.min(
      frame,
      result.klein_gordon.field.length - 1,
    );

    drawCurve(
      kgCanvas.current,
      result.klein_gordon.x,
      result.klein_gordon.field[index],
      "Klein?Gordon scalar field",
      "Field amplitude",
      result.klein_gordon.times[index],
    );

    drawCurve(
      diracCanvas.current,
      result.dirac.x,
      result.dirac.probability_density[index],
      "Dirac fermion probability density",
      "Probability density",
      result.dirac.times[index],
    );
  }, [result, frame]);

  async function run() {
    setLoading(true);
    setError("");
    setPlaying(false);

    try {
      const data = await runRelativisticComparison({
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
      setFrame(0);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h2>Relativistic Quantum Mechanics Comparison</h2>

      <p>
        Compare the relativistic Klein?Gordon scalar field
        with the Dirac spin-1/2 fermion model using matched
        physical parameters.
      </p>

      <p>
        <strong>Natural units:</strong> ? = c = 1
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(180px, 1fr))",
          gap: 12,
          marginBottom: 16,
        }}
      >
        <label>
          Mass
          <input
            type="number"
            step="0.1"
            value={mass}
            onChange={(e) => setMass(Number(e.target.value))}
          />
        </label>

        <label>
          Momentum
          <input
            type="number"
            step="0.1"
            value={momentum}
            onChange={(e) =>
              setMomentum(Number(e.target.value))
            }
          />
        </label>

        <label>
          Amplitude
          <input
            type="number"
            step="0.1"
            value={amplitude}
            onChange={(e) =>
              setAmplitude(Number(e.target.value))
            }
          />
        </label>

        <label>
          Width
          <input
            type="number"
            step="0.1"
            value={width}
            onChange={(e) =>
              setWidth(Number(e.target.value))
            }
          />
        </label>

        <label>
          Domain Length
          <input
            type="number"
            step="1"
            value={domainLength}
            onChange={(e) =>
              setDomainLength(Number(e.target.value))
            }
          />
        </label>

        <label>
          Duration
          <input
            type="number"
            step="1"
            value={duration}
            onChange={(e) =>
              setDuration(Number(e.target.value))
            }
          />
        </label>

        <label>
          Spatial Points
          <input
            type="number"
            step="16"
            min="64"
            max="256"
            value={points}
            onChange={(e) =>
              setPoints(Number(e.target.value))
            }
          />
        </label>

        <label>
          Animation Frames
          <input
            type="number"
            step="10"
            min="20"
            max="120"
            value={frames}
            onChange={(e) =>
              setFrames(Number(e.target.value))
            }
          />
        </label>
      </div>

      <button onClick={run} disabled={loading}>
        {loading
          ? "Running comparison..."
          : "Run Relativistic Comparison"}
      </button>

      {error && (
        <p style={{ color: "crimson" }}>
          {error}
        </p>
      )}

      {result && (
        <>
          <div
            style={{
              marginTop: 20,
              padding: 16,
              border: "1px solid #cbd5e1",
              borderRadius: 10,
            }}
          >
            <h3>Relativistic Kinematics</h3>

            <p>
              Energy:{" "}
              <strong>
                {result.relativistic_kinematics.energy.toFixed(6)}
              </strong>
            </p>

            <p>
              Rest energy:{" "}
              <strong>
                {result.relativistic_kinematics.rest_energy.toFixed(6)}
              </strong>
            </p>

            <p>
              Group velocity:{" "}
              <strong>
                {result.relativistic_kinematics.group_velocity.toFixed(6)}
              </strong>
            </p>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(320px, 1fr))",
              gap: 16,
              marginTop: 20,
            }}
          >
            <canvas
              ref={kgCanvas}
              width={600}
              height={300}
              style={{
                width: "100%",
                border: "1px solid #cbd5e1",
                borderRadius: 10,
              }}
            />

            <canvas
              ref={diracCanvas}
              width={600}
              height={300}
              style={{
                width: "100%",
                border: "1px solid #cbd5e1",
                borderRadius: 10,
              }}
            />
          </div>

          <div style={{ marginTop: 16 }}>
            <button
              onClick={() =>
                setPlaying((current) => !current)
              }
            >
              {playing ? "Pause" : "Play"}
            </button>

            <input
              type="range"
              min="0"
              max={result.shared_parameters.frames - 1}
              value={frame}
              onChange={(e) => {
                setPlaying(false);
                setFrame(Number(e.target.value));
              }}
              style={{
                width: "100%",
                marginTop: 10,
              }}
            />
          </div>

          <div
            style={{
              marginTop: 20,
              padding: 16,
              border: "1px solid #cbd5e1",
              borderRadius: 10,
            }}
          >
            <h3>Scientific Interpretation</h3>

            <ul>
              {result.comparison_notes.map(
                (note, index) => (
                  <li key={index}>{note}</li>
                ),
              )}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}
