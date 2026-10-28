import { useState } from "react";
import {
  calculatePropagator,
  calculatePropagatorScan,
} from "../services/propagatorApi";

export default function PropagatorLab() {
  const [mass, setMass] = useState("1");
  const [energy, setEnergy] = useState("2");
  const [momentum, setMomentum] = useState("1");
  const [epsilon, setEpsilon] = useState("0.001");

  const [result, setResult] = useState(null);
  const [scan, setScan] = useState(null);
  const [error, setError] = useState("");

  async function calculate() {
    try {
      setError("");
      const data = await calculatePropagator({
        mass: Number(mass),
        energy: Number(energy),
        momentum: Number(momentum),
        epsilon: Number(epsilon),
      });
      setResult(data);

      const scanData = await calculatePropagatorScan({
        mass: Number(mass),
        momentum: Number(momentum),
        epsilon: Number(epsilon),
        points: 101,
        energy_min: 0,
        energy_max: 4,
      });
      setScan(scanData);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h2>Free Scalar Feynman Propagator</h2>

      <p>
        Momentum-space propagator for a free scalar field.
        This is an educational perturbative-QFT implementation.
      </p>

      <p>
        D_F(p) = i / (p² - m² + iε)
      </p>

      <div>
        <label>
          Mass
          <input
            type="number"
            step="0.1"
            value={mass}
            onChange={(e) => setMass(e.target.value)}
          />
        </label>

        <label>
          Energy
          <input
            type="number"
            step="0.1"
            value={energy}
            onChange={(e) => setEnergy(e.target.value)}
          />
        </label>

        <label>
          Momentum
          <input
            type="number"
            step="0.1"
            value={momentum}
            onChange={(e) => setMomentum(e.target.value)}
          />
        </label>

        <label>
          Epsilon
          <input
            type="number"
            step="0.0001"
            value={epsilon}
            onChange={(e) => setEpsilon(e.target.value)}
          />
        </label>
      </div>

      <button onClick={calculate}>
        Calculate Propagator
      </button>

      {error && <p>{error}</p>}

      {result && (
        <div>
          <h3>Propagator Result</h3>

          <p>
            p² = {result.kinematics.p_squared.toFixed(6)}
          </p>

          <p>
            m² = {result.kinematics.mass_squared.toFixed(6)}
          </p>

          <p>
            On shell:{" "}
            {result.kinematics.on_shell_condition
              ? "YES"
              : "NO"}
          </p>

          <p>
            Real part:{" "}
            {result.propagator.real.toFixed(8)}
          </p>

          <p>
            Imaginary part:{" "}
            {result.propagator.imaginary.toFixed(8)}
          </p>

          <p>
            Magnitude:{" "}
            {result.propagator.magnitude.toFixed(8)}
          </p>

          <p>
            Phase:{" "}
            {result.propagator.phase.toFixed(8)}
          </p>
        </div>
      )}

      {scan && (
        <div>
          <h3>Energy Scan</h3>

          <p>
            The scan contains {scan.data.length} energy
            points and shows the propagator approaching its
            mass-shell enhancement.
          </p>

          <table>
            <thead>
              <tr>
                <th>Energy</th>
                <th>Real</th>
                <th>Imaginary</th>
                <th>Magnitude</th>
              </tr>
            </thead>

            <tbody>
              {scan.data
                .filter((_, index) => index % 10 === 0)
                .map((point) => (
                  <tr key={point.energy}>
                    <td>{point.energy.toFixed(3)}</td>
                    <td>{point.real.toFixed(6)}</td>
                    <td>{point.imaginary.toFixed(6)}</td>
                    <td>{point.magnitude.toFixed(6)}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}

      <h3>Physical Interpretation</h3>

      <ul>
        <li>
          The propagator is the basic free-field building
          block used in perturbative QFT.
        </li>
        <li>
          The enhancement occurs near p² = m², the
          relativistic mass shell.
        </li>
        <li>
          The iε prescription specifies how the poles are
          treated.
        </li>
        <li>
          The next stages will use propagators to construct
          Feynman rules and scattering amplitudes.
        </li>
      </ul>
    </div>
  );
}
