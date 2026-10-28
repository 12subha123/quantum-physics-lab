const API_BASE_URL = "http://127.0.0.1:8000";

export async function analyzeQFTProcess({
  incoming,
  outgoing,
  maxVertices = 4,
}) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/analyze-process`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        incoming,
        outgoing,
        max_vertices: maxVertices,
      }),
    },
  );

  if (!response.ok) {
    let detail = `QFT analysis failed (${response.status})`;

    try {
      const error = await response.json();

      if (error?.detail) {
        detail = error.detail;
      }
    } catch {
      // Keep the HTTP status message.
    }

    throw new Error(detail);
  }

  return response.json();
}
