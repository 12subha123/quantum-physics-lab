const API_BASE_URL = "http://127.0.0.1:8000";

export async function calculateSuperposition(
  parameters
) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/superposition`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(parameters),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Quantum superposition calculation failed."
    );
  }

  return data;
}
