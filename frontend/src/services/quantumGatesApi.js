const API_BASE_URL = "http://127.0.0.1:8000";

export async function getQuantumStates() {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/gates/states`
  );

  if (!response.ok) {
    throw new Error("Failed to load quantum states.");
  }

  return response.json();
}

export async function getQuantumGates() {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/gates`
  );

  if (!response.ok) {
    throw new Error("Failed to load quantum gates.");
  }

  return response.json();
}

export async function applyQuantumGate(payload) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/gates`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Quantum gate calculation failed."
    );
  }

  return data;
}
