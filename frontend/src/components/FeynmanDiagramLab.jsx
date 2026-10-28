import { useState } from "react";
import { calculateFeynmanRules } from "../services/feynmanRulesApi";

export default function FeynmanDiagramLab() {
  const [lambda, setLambda] = useState("1");
  const [result, setResult] = useState(null);
  const [selected, setSelected] = useState("diagram");
  const [error, setError] = useState("");

  async function calculate() {
    try {
      setError("");

      const value = Number(lambda);

      if (!Number.isFinite(value) || value < 0) {
        throw new Error("Lambda must be a non-negative number.");
      }

      const data = await calculateFeynmanRules({
        lambda_coupling: value,
      });

      setResult(data);
      setSelected("vertex");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h2>Interactive Feynman Diagram Lab</h2>

      <p>
        Tree-level four-scalar scattering in real scalar phi^4
        theory.
      </p>

      <p>
        Process: phi + phi → phi + phi
      </p>

      <div>
        <label>
          Coupling lambda{" "}
          <input
            type="number"
            min="0"
            step="0.1"
            value={lambda}
            onChange={(event) => setLambda(event.target.value)}
          />
        </label>
      </div>

      <button onClick={calculate}>
        Calculate Amplitude
      </button>

      {error && <p>{error}</p>}

      <div
        style={{
          marginTop: "20px",
          border: "1px solid #888",
          padding: "12px",
          borderRadius: "8px",
        }}
      >
        <svg
          viewBox="0 0 800 430"
          width="100%"
          role="img"
          aria-label="Four scalar particle Feynman contact diagram"
        >
          <line
            x1="80"
            y1="110"
            x2="400"
            y2="215"
            stroke="currentColor"
            strokeWidth="5"
          />

          <line
            x1="80"
            y1="320"
            x2="400"
            y2="215"
            stroke="currentColor"
            strokeWidth="5"
          />

          <line
            x1="400"
            y1="215"
            x2="720"
            y2="110"
            stroke="currentColor"
            strokeWidth="5"
          />

          <line
            x1="400"
            y1="215"
            x2="720"
            y2="320"
            stroke="currentColor"
            strokeWidth="5"
          />

          <polygon
            points="175,135 160,130 165,145"
            fill="currentColor"
          />

          <polygon
            points="175,295 160,290 165,305"
            fill="currentColor"
          />

          <polygon
            points="625,135 640,130 635,145"
            fill="currentColor"
          />

          <polygon
            points="625,295 640,290 635,305"
            fill="currentColor"
          />

          <circle
            cx="400"
            cy="215"
            r="22"
            fill="none"
            stroke="currentColor"
            strokeWidth="5"
            onClick={() => setSelected("vertex")}
            style={{ cursor: "pointer" }}
          />

          <text
            x="65"
            y="90"
            fontSize="24"
          >
            p₁
          </text>

          <text
            x="65"
            y="355"
            fontSize="24"
          >
            p₂
          </text>

          <text
            x="700"
            y="90"
            fontSize="24"
          >
            p₃
          </text>

          <text
            x="700"
            y="355"
            fontSize="24"
          >
            p₄
          </text>

          <text
            x="365"
            y="175"
            fontSize="24"
          >
            φ⁴
          </text>

          <text
            x="330"
            y="405"
            fontSize="22"
          >
            φ + φ → φ + φ
          </text>
        </svg>
      </div>

      <div
        style={{
          display: "flex",
          gap: "8px",
          marginTop: "12px",
          flexWrap: "wrap",
        }}
      >
        <button
          onClick={() => setSelected("diagram")}
        >
          Diagram
        </button>

        <button
          onClick={() => setSelected("vertex")}
        >
          Vertex Rule
        </button>

        <button
          onClick={() => setSelected("amplitude")}
        >
          Amplitude
        </button>
      </div>

      {selected === "diagram" && (
        <div>
          <h3>Diagram Topology</h3>
          <p>
            One four-point interaction vertex connects four
            external scalar legs.
          </p>
          <p>
            Internal propagators: 0
          </p>
          <p>
            Vertices: 1
          </p>
          <p>
            External legs: 4
          </p>
        </div>
      )}

      {selected === "vertex" && (
        <div>
          <h3>Feynman Vertex</h3>
          <p>
            Interaction:
            {" "}
            L_int = -lambda/4! * phi⁴
          </p>

          <p>
            Rule:
            {" "}
            -i lambda
          </p>

          {result && (
            <>
              <p>
                Real part:{" "}
                {result.vertex.vertex_factor.real.toFixed(6)}
              </p>

              <p>
                Imaginary part:{" "}
                {result.vertex.vertex_factor.imaginary.toFixed(6)}
              </p>

              <p>
                Magnitude:{" "}
                {result.vertex.vertex_factor.magnitude.toFixed(6)}
              </p>
            </>
          )}
        </div>
      )}

      {selected === "amplitude" && (
        <div>
          <h3>Tree-Level Amplitude</h3>

          <p>
            Process:
            {" "}
            phi + phi → phi + phi
          </p>

          {result ? (
            <>
              <p>
                M = {result.tree_level_scattering.amplitude_formula}
              </p>

              <p>
                Tree-level diagrams:
                {" "}
                {result.tree_level_scattering.diagrams.length}
              </p>
            </>
          ) : (
            <p>
              Calculate the amplitude to load the backend result.
            </p>
          )}
        </div>
      )}

      <h3>Physics Note</h3>

      <p>
        This diagram represents the lowest-order contact
        interaction in real scalar phi^4 theory. It is a
        tree-level perturbative diagram; loop corrections are
        not included yet.
      </p>
    </div>
  );
}
