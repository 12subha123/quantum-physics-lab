import { useState } from "react";
import { calculateCanonicalQuantization } from "../services/canonicalQuantizationApi";


export default function CanonicalQuantizationLab() {
  const [mass, setMass] = useState(1);
  const [modes, setModes] = useState(8);
  const [boxLength, setBoxLength] = useState(20);
  const [occupations, setOccupations] = useState(
    "0,0,1,0,0,0,0,0",
  );

  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function run() {
    setLoading(true);
    setError("");

    try {
      const values = occupations
        .split(",")
        .map((value) => Number(value.trim()));

      if (
        values.length !== modes ||
        values.some(
          (value) =>
            !Number.isInteger(value) || value < 0,
        )
      ) {
        throw new Error(
          `Enter exactly ${modes} non-negative integer occupation numbers.`,
        );
      }

      const data =
        await calculateCanonicalQuantization({
          mass,
          modes,
          box_length: boxLength,
          occupation_numbers: values,
        });

      setResult(data);
    } catch (err) {
      setError(err.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h2>Canonical Quantization of a Scalar Field</h2>

      <p>
        Quantize a finite set of normal modes of a real
        scalar field and explore creation, annihilation,
        Fock-state occupation, and vacuum energy.
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
            min="0"
            step="0.1"
            value={mass}
            onChange={(e) =>
              setMass(Number(e.target.value))
            }
          />
        </label>

        <label>
          Number of Modes
          <input
            type="number"
            min="1"
            max="32"
            step="1"
            value={modes}
            onChange={(e) =>
              setModes(Number(e.target.value))
            }
          />
        </label>

        <label>
          Box Length
          <input
            type="number"
            min="0.1"
            step="1"
            value={boxLength}
            onChange={(e) =>
              setBoxLength(Number(e.target.value))
            }
          />
        </label>
      </div>

      <label
        style={{
          display: "block",
          marginBottom: 12,
        }}
      >
        Occupation numbers
        <input
          type="text"
          value={occupations}
          onChange={(e) =>
            setOccupations(e.target.value)
          }
          placeholder="0,0,1,0,0,0,0,0"
          style={{
            display: "block",
            width: "100%",
            marginTop: 6,
          }}
        />
      </label>

      <p>
        Each number is the number of quanta in one mode.
        For example, <strong>1</strong> means one quantum
        occupies that mode.
      </p>

      <button onClick={run} disabled={loading}>
        {loading
          ? "Calculating..."
          : "Quantize Scalar Field"}
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
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(180px, 1fr))",
              gap: 12,
              marginTop: 20,
            }}
          >
            <div>
              <strong>Vacuum Energy</strong>
              <p>
                {result.vacuum_energy.toFixed(6)}
              </p>
            </div>

            <div>
              <strong>Excitation Energy</strong>
              <p>
                {result.excitation_energy.toFixed(6)}
              </p>
            </div>

            <div>
              <strong>Total Energy</strong>
              <p>
                {result.total_energy.toFixed(6)}
              </p>
            </div>
          </div>

          <div
            style={{
              marginTop: 20,
              overflowX: "auto",
            }}
          >
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
              }}
            >
              <thead>
                <tr>
                  <th>Mode</th>
                  <th>Momentum</th>
                  <th>?</th>
                  <th>Occupation</th>
                  <th>Excitation Energy</th>
                  <th>Total Mode Energy</th>
                </tr>
              </thead>

              <tbody>
                {result.modes_data.map((mode) => (
                  <tr key={mode.mode}>
                    <td>{mode.mode}</td>
                    <td>
                      {mode.momentum.toFixed(4)}
                    </td>
                    <td>
                      {mode.frequency.toFixed(4)}
                    </td>
                    <td>
                      {mode.occupation_number}
                    </td>
                    <td>
                      {mode.excitation_energy.toFixed(4)}
                    </td>
                    <td>
                      {mode.total_mode_energy.toFixed(4)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div
            style={{
              marginTop: 20,
              padding: 16,
              border: "1px solid #cbd5e1",
              borderRadius: 10,
            }}
          >
            <h3>QFT Structure</h3>

            <p>
              {result.field_operator_structure}
            </p>

            <p>
              {result.hamiltonian_structure}
            </p>

            <p>
              <strong>
                Canonical commutation relation:
              </strong>{" "}
              {result.commutation_relation}
            </p>

            <h4>Interpretation</h4>

            <ul>
              {result.interpretation.map(
                (item, index) => (
                  <li key={index}>{item}</li>
                ),
              )}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}
