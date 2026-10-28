const API_BASE_URL = "http://127.0.0.1:8000";

export async function analyzeDecoherence(
  densityMatrix,
  time,
  decoherenceRate
) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/decoherence`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        density_matrix: densityMatrix,
        time,
        decoherence_rate: decoherenceRate,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Decoherence calculation failed."
    );
  }

  return data;
}

export async function simulateDecoherence(
  densityMatrix,
  timeStart,
  timeEnd,
  steps,
  decoherenceRate
) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/decoherence/simulation`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        density_matrix: densityMatrix,
        time_start: timeStart,
        time_end: timeEnd,
        steps,
        decoherence_rate: decoherenceRate,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Decoherence simulation failed."
    );
  }

  return data;
}