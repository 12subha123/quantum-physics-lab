import { useState } from "react";

import {
  calculateOperatorEigenstates,
  calculateCustomOperator,
} from "../services/operatorsEigenstatesApi";


function OperatorsEigenstatesLab() {
  const [mode, setMode] = useState("preset");
  const [operator, setOperator] = useState("pauli_z");

  const [matrix, setMatrix] = useState({
    a: "2",
    b: "1",
    c: "1",
    d: "2",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  async function handleCalculate(event) {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      let data;

      if (mode === "preset") {
        data = await calculateOperatorEigenstates(
          operator
        );
      } else {
        data = await calculateCustomOperator({
          a: Number(matrix.a),
          b: Number(matrix.b),
          c: Number(matrix.c),
          d: Number(matrix.d),
        });
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  function updateMatrix(name, value) {
    setMatrix((previous) => ({
      ...previous,
      [name]: value,
    }));
  }


  function formatComplex(value) {
    const real = Number(value.real);
    const imag = Number(value.imag);

    if (
      Math.abs(real) < 1e-10 &&
      Math.abs(imag) < 1e-10
    ) {
      return "0";
    }

    if (Math.abs(imag) < 1e-10) {
      return real.toFixed(6);
    }

    if (Math.abs(real) < 1e-10) {
      return `${imag.toFixed(6)}i`;
    }

    const sign = imag >= 0 ? "+" : "-";

    return (
      `${real.toFixed(6)} ` +
      `${sign} ` +
      `${Math.abs(imag).toFixed(6)}i`
    );
  }


  return (
    <main className="lab-container">
      <header className="lab-header">
        <p className="lab-label">
          QUANTUM PHYSICS LABORATORY
        </p>

        <h1>Operators & Eigenstates</h1>

        <p className="lab-description">
          Build or select a quantum operator and
          calculate its eigenvalues and eigenstates.
        </p>
      </header>


      <section className="lab-card">
        <h2>Operator Laboratory</h2>

        <div className="operator-mode-buttons">
          <button
            type="button"
            className={
              mode === "preset"
                ? "mode-button active"
                : "mode-button"
            }
            onClick={() => {
              setMode("preset");
              setResult(null);
              setError("");
            }}
          >
            Pauli Operators
          </button>

          <button
            type="button"
            className={
              mode === "custom"
                ? "mode-button active"
                : "mode-button"
            }
            onClick={() => {
              setMode("custom");
              setResult(null);
              setError("");
            }}
          >
            Custom Operator
          </button>
        </div>


        {mode === "preset" && (
          <form onSubmit={handleCalculate}>
            <div className="parameter-grid">
              <label>
                Quantum Operator

                <select
                  value={operator}
                  onChange={(event) =>
                    setOperator(
                      event.target.value
                    )
                  }
                >
                  <option value="pauli_x">
                    Pauli-X
                  </option>

                  <option value="pauli_y">
                    Pauli-Y
                  </option>

                  <option value="pauli_z">
                    Pauli-Z
                  </option>
                </select>
              </label>
            </div>

            <button
              type="submit"
              className="calculate-button"
              disabled={loading}
            >
              {loading
                ? "Calculating..."
                : "Calculate Eigenstates"}
            </button>
          </form>
        )}


        {mode === "custom" && (
          <form onSubmit={handleCalculate}>
            <p className="operator-input-description">
              Enter the four elements of a real 2×2
              quantum operator.
            </p>

            <div className="custom-matrix-input">
              <div>
                <label>
                  a

                  <input
                    type="number"
                    step="any"
                    value={matrix.a}
                    onChange={(event) =>
                      updateMatrix(
                        "a",
                        event.target.value
                      )
                    }
                    required
                  />
                </label>

                <label>
                  b

                  <input
                    type="number"
                    step="any"
                    value={matrix.b}
                    onChange={(event) =>
                      updateMatrix(
                        "b",
                        event.target.value
                      )
                    }
                    required
                  />
                </label>
              </div>

              <div>
                <label>
                  c

                  <input
                    type="number"
                    step="any"
                    value={matrix.c}
                    onChange={(event) =>
                      updateMatrix(
                        "c",
                        event.target.value
                      )
                    }
                    required
                  />
                </label>

                <label>
                  d

                  <input
                    type="number"
                    step="any"
                    value={matrix.d}
                    onChange={(event) =>
                      updateMatrix(
                        "d",
                        event.target.value
                      )
                    }
                    required
                  />
                </label>
              </div>
            </div>

            <p className="equation">
              A = [
              {" "}
              {matrix.a || "0"}
              {" "}
              {matrix.b || "0"}
              {" "}
              ;{" "}
              {matrix.c || "0"}
              {" "}
              {matrix.d || "0"}
              {" "}
              ]
            </p>

            <button
              type="submit"
              className="calculate-button"
              disabled={loading}
            >
              {loading
                ? "Calculating..."
                : "Calculate Custom Operator"}
            </button>
          </form>
        )}
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
            <h2>Operator Matrix</h2>

            <div className="matrix-display">
              {result.matrix.map(
                (row, rowIndex) => (
                  <div
                    className="matrix-row"
                    key={rowIndex}
                  >
                    {row.map(
                      (value, columnIndex) => (
                        <span
                          className="matrix-value"
                          key={columnIndex}
                        >
                          {formatComplex(value)}
                        </span>
                      )
                    )}
                  </div>
                )
              )}
            </div>
          </section>


          <section className="lab-card">
            <h2>Eigenvalues</h2>

            <div className="results-grid">
              {result.eigenvalues.map(
                (value, index) => (
                  <div
                    className="result-item"
                    key={index}
                  >
                    <span>
                      Eigenvalue {index + 1}
                    </span>

                    <strong>
                      {formatComplex(value)}
                    </strong>

                    <small>
                      λ
                    </small>
                  </div>
                )
              )}
            </div>
          </section>


          <section className="lab-card">
            <h2>Eigenstates</h2>

            <div className="eigenstate-list">
              {result.eigenvectors.map(
                (vector, index) => (
                  <div
                    className="eigenstate-card"
                    key={index}
                  >
                    <h3>
                      Eigenstate {index + 1}
                    </h3>

                    <p className="equation">
                      |ψ⟩ = [
                      {" "}
                      {formatComplex(
                        vector[0]
                      )}
                      {" , "}
                      {formatComplex(
                        vector[1]
                      )}
                      {" "}
                      ]
                    </p>

                    <p>
                      Corresponding eigenvalue:
                      {" "}
                      <strong>
                        {formatComplex(
                          result.eigenvalues[
                            index
                          ]
                        )}
                      </strong>
                    </p>
                  </div>
                )
              )}
            </div>
          </section>


          <section className="lab-card">
            <h2>
              Eigenvalue Equation Verification
            </h2>

            <div className="results-grid">
              {result.verification.map(
                (item, index) => (
                  <div
                    className="result-item"
                    key={index}
                  >
                    <span>
                      Eigenstate {index + 1}
                    </span>

                    <strong>
                      {item.verified
                        ? "Verified"
                        : "Failed"}
                    </strong>

                    <small>
                      Residual:{" "}
                      {Number(
                        item.residual
                      ).toExponential(3)}
                    </small>
                  </div>
                )
              )}
            </div>

            <div className="explanation-box">
              <p>
                The eigenvalue equation is:
              </p>

              <p className="equation">
                A|ψ⟩ = λ|ψ⟩
              </p>

              <p>
                The residual measures the numerical
                difference between the two sides of
                the eigenvalue equation. A value close
                to zero indicates that the calculated
                eigenstate satisfies the equation.
              </p>
            </div>
          </section>


          <section className="lab-card">
            <h2>Physical Interpretation</h2>

            <div className="explanation-box">
              <p>
                A quantum operator represents a
                measurable physical quantity or a
                transformation of a quantum state.
              </p>

              <p>
                An eigenstate is a quantum state for
                which measuring the corresponding
                observable produces a definite
                eigenvalue.
              </p>

              <p>
                You can use the Pauli operators as
                standard quantum-mechanics examples,
                or construct your own 2×2 operator and
                investigate its mathematical properties.
              </p>
            </div>
          </section>
        </>
      )}
    </main>
  );
}


export default OperatorsEigenstatesLab;
