const API_BASE_URL = "http://127.0.0.1:8000";

export async function analyzePureDensityMatrix(
  stateReal,
  stateImag
) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/density-matrix/pure`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        state_real: stateReal,
        state_imag: stateImag,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Pure-state density matrix calculation failed."
    );
  }

  return data;
}


export async function analyzeMixedDensityMatrix(
  statesReal,
  statesImag,
  probabilities
) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/density-matrix/mixed`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        states_real: statesReal,
        states_imag: statesImag,
        probabilities,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Mixed-state density matrix calculation failed."
    );
  }

  return data;
}