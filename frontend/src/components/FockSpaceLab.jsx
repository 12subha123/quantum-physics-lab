import { useMemo, useState } from "react";
import { calculateFockSpace } from "../services/fockSpaceApi";

export default function FockSpaceLab() {
  const [mass, setMass] = useState("1");
  const [modes, setModes] = useState("8");
  const [boxLength, setBoxLength] = useState("20");
  const [occupations, setOccupations] = useState(
    "0,0,1,0,0,0,0,0"
  );
  const [operator, setOperator] = useState("creation");
  const [operatorMode, setOperatorMode] = useState("0");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const modeCount = Number(modes);

  const parsedOccupations = useMemo(() => {
    if (occupations.trim() === "") {
      return [];
    }

    return occupations
      .split(",")
      .map((value) => value.trim())
      .map((value) => Number(value));
  }, [occupations]);

  function updateModes(value) {
    setModes(value);

    const count = Number(value);

    if (!Number.isInteger(count) || count < 1 || count > 32) {
      return;
    }

    const current = occupations
      .split(",")
      .map((value) => value.trim())
      .filter((value) => value !== "");

    const next = Array.from(
      { length: count },
      (_, index) => current[index] ?? "0"
    );

    setOccupations(next.join(","));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setResult(null);

    if (
      !Number.isInteger(modeCount) ||
      modeCount < 1 ||
      modeCount > 32
    ) {
      setError("Number of modes must be between 1 and 32.");
      return;
    }

    if (parsedOccupations.length !== modeCount) {
      setError(
        "Enter exactly " +
          modeCount +
          " non-negative integer occupation numbers."
      );
      return;
    }

    if (
      parsedOccupations.some(
        (value) =>
          !Number.isInteger(value) || value < 0
      )
    ) {
      setError(
        "Occupation numbers must be non-negative integers."
      );
      return;
    }

    const selectedMode = Number(operatorMode);

    if (
      !Number.isInteger(selectedMode) ||
      selectedMode < 0 ||
      selectedMode >= modeCount
    ) {
      setError(
        "Operator mode must be between 0 and " +
          (modeCount - 1) +
          "."
      );
      return;
    }

    try {
      const data = await calculateFockSpace({
        mass: Number(mass),
        modes: modeCount,
        box_length: Number(boxLength),
        occupation_numbers: parsedOccupations,
        operator: operator,
        operator_mode: selectedMode,
      });

      setResult(data);
    } catch (err) {
      setError(
        err.message || "Fock space calculation failed."
      );
    }
  }

  return (
    <div className="lab-card">
      <h2>Fock Space &amp; Particle States</h2>

      <p>
        Explore finite-mode bosonic Fock states,
        occupation numbers, creation and annihilation
        operators, particle number, and energy.
      </p>

      <p>
        <strong>Model:</strong> Finite-mode educational
        approximation to the Fock space of a real scalar
        field.
      </p>

      <form onSubmit={handleSubmit}>
        <div className="input-grid">
          <label>
            Mass
            <input
              type="number"
              min="0"
              step="0.1"
              value={mass}
              onChange={(event) =>
                setMass(event.target.value)
              }
            />
          </label>

          <label>
            Number of modes
            <input
              type="number"
              min="1"
              max="32"
              step="1"
              value={modes}
              onChange={(event) =>
                updateModes(event.target.value)
              }
            />
          </label>

          <label>
            Box length
            <input
              type="number"
              min="0.01"
              step="0.1"
              value={boxLength}
              onChange={(event) =>
                setBoxLength(event.target.value)
              }
            />
          </label>

          <label>
            Operator
            <select
              value={operator}
              onChange={(event) =>
                setOperator(event.target.value)
              }
            >
              <option value="creation">
                Creation a†
              </option>

              <option value="annihilation">
                Annihilation a
              </option>
            </select>
          </label>

          <label>
            Operator mode
            <input
              type="number"
              min="0"
              max={Math.max(0, modeCount - 1)}
              step="1"
              value={operatorMode}
              onChange={(event) =>
                setOperatorMode(event.target.value)
              }
            />
          </label>
        </div>

        <label>
          Occupation numbers
          <input
            type="text"
            value={occupations}
            onChange={(event) =>
              setOccupations(event.target.value)
            }
            placeholder="0,0,1,0,0,0,0,0"
          />
        </label>

        <button type="submit">
          Analyze Fock State
        </button>
      </form>

      {error && (
        <p style={{ color: "crimson" }}>
          {error}
        </p>
      )}

      {result && (
        <div>
          <hr />

          <h3>Fock State</h3>

          <p>
            <strong>Ket:</strong>{" "}
            {result.fock_state.ket}
          </p>

          <p>
            <strong>Total particles:</strong>{" "}
            {result.fock_state.total_particle_number}
          </p>

          <p>
            <strong>Occupied modes:</strong>{" "}
            {result.fock_state.occupied_modes.length > 0
              ? result.fock_state.occupied_modes.join(", ")
              : "None — vacuum state"}
          </p>

          <h3>Energy</h3>

          <p>
            Vacuum energy:{" "}
            {result.energies.vacuum_energy.toFixed(6)}
          </p>

          <p>
            Excitation energy:{" "}
            {result.energies.excitation_energy.toFixed(6)}
          </p>

          <p>
            Total energy:{" "}
            {result.energies.total_energy.toFixed(6)}
          </p>

          {result.operator_action && (
            <>
              <h3>Operator Action</h3>

              <p>
                <strong>Operator:</strong>{" "}
                {result.operator_action.operator}
              </p>

              <p>
                <strong>Mode:</strong>{" "}
                {result.operator_action.mode}
              </p>

              <p>
                <strong>Coefficient:</strong>{" "}
                {result.operator_action.coefficient.toFixed(6)}
              </p>

              <p>
                <strong>Input:</strong>{" "}
                {result.operator_action.input_ket}
              </p>

              <p>
                <strong>Output:</strong>{" "}
                {result.operator_action.output_ket}
              </p>
            </>
          )}

          <h3>Mode Spectrum</h3>

          <div style={{ overflowX: "auto" }}>
            <table>
              <thead>
                <tr>
                  <th>Mode</th>
                  <th>Momentum</th>
                  <th>Frequency</th>
                  <th>Occupation</th>
                  <th>Particle Energy</th>
                  <th>Total Mode Energy</th>
                </tr>
              </thead>

              <tbody>
                {result.modes_data.map((mode) => (
                  <tr key={mode.mode}>
                    <td>{mode.mode}</td>
                    <td>
                      {mode.momentum.toFixed(5)}
                    </td>
                    <td>
                      {mode.frequency.toFixed(5)}
                    </td>
                    <td>
                      {mode.occupation_number}
                    </td>
                    <td>
                      {mode.particle_energy.toFixed(5)}
                    </td>
                    <td>
                      {mode.total_mode_energy.toFixed(5)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <h3>Operator Rules</h3>

          <p>
            {result.operator_rules.annihilation}
          </p>

          <p>
            {result.operator_rules.creation}
          </p>

          <p>
            {result.operator_rules.commutator}
          </p>

          <h3>Physical Interpretation</h3>

          <ul>
            {result.interpretation.map(
              (item, index) => (
                <li key={index}>{item}</li>
              )
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
