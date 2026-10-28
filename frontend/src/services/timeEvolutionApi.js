const API_BASE_URL = "http://127.0.0.1:8000";

export async function analyzeTimeEvolution(
  stateReal,
  stateImag,
  hamiltonianReal,
  hamiltonianImag,
  time,
  hbar = 1.0
) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/time-evolution`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        state_real: stateReal,
        state_imag: stateImag,
        hamiltonian_real: hamiltonianReal,
        hamiltonian_imag: hamiltonianImag,
        time,
        hbar,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Quantum time-evolution analysis failed."
    );
  }

  return data;
}
