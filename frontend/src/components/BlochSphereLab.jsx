import { useState } from "react";

import {
  calculateBlochSphere,
} from "../services/blochSphereApi";

import BlochSphere3D from "./BlochSphere3D";


function BlochSphereLab() {
  const [theta, setTheta] = useState(90);
  const [phi, setPhi] = useState(0);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  async function handleCalculate(event) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      const data = await calculateBlochSphere({
        theta_degrees: Number(theta),
        phi_degrees: Number(phi),
      });

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }


  function formatNumber(value) {
    return Number(value).toFixed(6);
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

        <h1>Spin-1/2 & Bloch Sphere</h1>

        <p className="lab-description">
          Explore the quantum state of a spin-1/2
          particle using the Bloch-sphere
          representation.
        </p>
      </header>


      <section className="lab-card">
        <h2>Quantum State Controls</h2>

        <form onSubmit={handleCalculate}>

          <div className="parameter-grid">

            <label>
              Theta (θ): {theta}°

              <input
                type="range"
                min="0"
                max="180"
                step="1"
                value={theta}
                onChange={(event) =>
                  setTheta(event.target.value)
                }
              />

              <input
                type="number"
                min="0"
                max="180"
                step="1"
                value={theta}
                onChange={(event) =>
                  setTheta(event.target.value)
                }
              />
            </label>


            <label>
              Phi (φ): {phi}°

              <input
                type="range"
                min="0"
                max="360"
                step="1"
                value={phi}
                onChange={(event) =>
                  setPhi(event.target.value)
                }
              />

              <input
                type="number"
                min="0"
                max="360"
                step="1"
                value={phi}
                onChange={(event) =>
                  setPhi(event.target.value)
                }
              />
            </label>

          </div>


          <button
            type="submit"
            className="calculate-button"
            disabled={loading}
          >
            {loading
              ? "Calculating..."
              : "Calculate Quantum State"}
          </button>

        </form>
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

            <h2>3D Bloch Sphere</h2>

            <BlochSphere3D
              x={result.bloch_coordinates.x}
              y={result.bloch_coordinates.y}
              z={result.bloch_coordinates.z}
            />

            <p className="bloch-coordinate-text">
              Bloch vector:
              {" "}
              (
              {formatNumber(
                result.bloch_coordinates.x
              )}
              ,{" "}
              {formatNumber(
                result.bloch_coordinates.y
              )}
              ,{" "}
              {formatNumber(
                result.bloch_coordinates.z
              )}
              )
            </p>

          </section>


          <section className="lab-card">

            <h2>Bloch Coordinates</h2>

            <div className="results-grid">

              <div className="result-item">
                <span>X</span>
                <strong>
                  {formatNumber(
                    result.bloch_coordinates.x
                  )}
                </strong>
              </div>

              <div className="result-item">
                <span>Y</span>
                <strong>
                  {formatNumber(
                    result.bloch_coordinates.y
                  )}
                </strong>
              </div>

              <div className="result-item">
                <span>Z</span>
                <strong>
                  {formatNumber(
                    result.bloch_coordinates.z
                  )}
                </strong>
              </div>

            </div>

          </section>


          <section className="lab-card">

            <h2>Quantum State</h2>

            <div className="explanation-box">

              <p className="equation">
                |ψ⟩ = α|0⟩ + β|1⟩
              </p>

              <p>
                α ={" "}
                <strong>
                  {formatComplex(
                    result.quantum_state.alpha
                  )}
                </strong>
              </p>

              <p>
                β ={" "}
                <strong>
                  {formatComplex(
                    result.quantum_state.beta
                  )}
                </strong>
              </p>

            </div>

          </section>


          <section className="lab-card">

            <h2>Measurement Probabilities</h2>

            <div className="results-grid">

              <div className="result-item">
                <span>P(0)</span>
                <strong>
                  {(
                    result
                      .measurement_probabilities
                      .zero * 100
                  ).toFixed(2)}
                  %
                </strong>
              </div>

              <div className="result-item">
                <span>P(1)</span>
                <strong>
                  {(
                    result
                      .measurement_probabilities
                      .one * 100
                  ).toFixed(2)}
                  %
                </strong>
              </div>

            </div>

          </section>


          <section className="lab-card">

            <h2>Physical Interpretation</h2>

            <div className="explanation-box">

              <p>
                A pure spin-1/2 quantum state is
                represented by a point on the
                surface of the Bloch sphere.
              </p>

              <p>
                θ controls the polar angle,
                while φ controls the azimuthal
                angle.
              </p>

              <p>
                The Bloch vector is
                {" "}
                (
                {formatNumber(
                  result.bloch_coordinates.x
                )}
                ,{" "}
                {formatNumber(
                  result.bloch_coordinates.y
                )}
                ,{" "}
                {formatNumber(
                  result.bloch_coordinates.z
                )}
                ).
              </p>

            </div>

          </section>

        </>
      )}

    </main>
  );
}


export default BlochSphereLab;
