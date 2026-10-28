const API_BASE = "http://127.0.0.1:8000";

export async function runRelativisticComparison(parameters) {
  const response = await fetch(
    `${API_BASE}/api/quantum/field-theory/relativistic-comparison`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(parameters),
    },
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Relativistic comparison failed.",
    );
  }

  return data;
}
