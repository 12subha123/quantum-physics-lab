const API_BASE_URL = "http://127.0.0.1:8000";

export async function analyzeQEDChannels(data) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/qed-channel-analysis`,
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
      payload.detail || "QED channel analysis failed."
    );
  }

  return payload;
}
