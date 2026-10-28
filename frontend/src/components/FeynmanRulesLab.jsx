import { useState } from "react";
import {
  calculateFeynmanRules,
  calculatePhi4Scattering,
} from "../services/feynmanRulesApi";

export default function FeynmanRulesLab() {
  const [lambda, setLambda] = useState("1");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function calculate() {
    try {
      setError("");

      const data = {
        lambda_coupling: Number(lambda),
      };

      const rules = await calculateFeynmanRules(data);
      const scattering = await calculatePhi4Scattering(data);

      setResult({
        rules,
        scattering,
      });
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h2>Feynman Rules Lab</h2>

      <p>
        Real scalar phi^4 interaction at tree level.
      </p>

      <p>
        L_int = -lambda/4! * phi^4
      </p>

      <label>
        Coupling lambda
        <input
          type="number"
          min="0"
          step="0.1"
          value={lambda}
          onChange={(e) => setLambda(e.target.value)}
        />
      </label>

      <button onClick={calculate}>
        Calculate Feynman Rules
      </button>

      {error && <p>{error}</p>}

      {result && (
        <div>
          <h3>Four-Scalar Vertex</h3>

          <p>
            Vertex factor:{" "}
            {result.rules.vertex.formula}
          </p>

          <p>
            Real part:{" "}
            {result.rules.vertex.vertex_factor.real.toFixed(6)}
          </p>

          <p>
            Imaginary part:{" "}
            {result.rules.vertex.vertex_factor.imaginary.toFixed(6)}
          </p>

          <p>
            Magnitude:{" "}
            {result.rules.vertex.vertex_factor.magnitude.toFixed(6)}
          </p>

          <h3>Tree-Level Scattering</h3>

          <p>
            Process:{" "}
            {result.scattering.process}
          </p>

          <p>
            Amplitude:{" "}
            {result.scattering.amplitude_formula}
          </p>

          <p>
            Diagrams at this order:{" "}
            {result.scattering.diagrams.length}
          </p>

          <h3>Physical Interpretation</h3>

          <ul>
            {result.rules.tree_level_scattering.interpretation.map(
              (item) => (
                <li key={item}>{item}</li>
              )
            )}
          </ul>

          <h3>Approximation</h3>

          <ul>
            {result.rules.limitations.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
