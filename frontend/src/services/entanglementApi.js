const API_BASE_URL = "http://127.0.0.1:8000";

export async function getBellStates() {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/entanglement/states`
  );

  if (!response.ok) {
    throw new Error("Failed to load Bell states.");
  }

  return response.json();
}

export async function analyzeEntanglement(stateName) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/entanglement`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        state_name: stateName,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Entanglement analysis failed."
    );
  }

  return data;
}
