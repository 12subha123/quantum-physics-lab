const API_BASE_URL = "http://127.0.0.1:8000";

export async function calculateQCDAngularObservable(data) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/qcd/angular-observable`,
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
      Array.isArray(payload.detail)
        ? payload.detail.join(", ")
        : payload.detail || "QCD angular observable calculation failed."
    );
  }

  return payload;
}
