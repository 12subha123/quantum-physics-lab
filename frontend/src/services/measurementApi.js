const API_BASE_URL = "http://127.0.0.1:8000";

export async function performMeasurement(
  stateReal,
  stateImag,
  shots,
  seed
) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/measurement`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        state_real: stateReal,
        state_imag: stateImag,
        shots,
        seed,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Quantum measurement failed."
    );
  }

  return data;
}