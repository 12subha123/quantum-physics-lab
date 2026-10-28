const API_BASE_URL = "http://127.0.0.1:8000";

export async function calculateFockSpace(data) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/fock-space`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  );

  const payload = await response.json();

  if (!response.ok) {
    throw new Error(
      payload.detail || "Fock space calculation failed."
    );
  }

  return payload;
}
