const API_BASE_URL = "http://127.0.0.1:8000";

async function postFeynmanRules(path, data) {
  const response = await fetch(
    `${API_BASE_URL}${path}`,
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
      payload.detail || "Feynman-rule calculation failed."
    );
  }

  return payload;
}

export async function calculateFeynmanRules(data) {
  return postFeynmanRules(
    "/api/quantum/field-theory/feynman-rules",
    data
  );
}

export async function calculatePhi4Vertex(data) {
  return postFeynmanRules(
    "/api/quantum/field-theory/feynman-rules/vertex",
    data
  );
}

export async function calculatePhi4Scattering(data) {
  return postFeynmanRules(
    "/api/quantum/field-theory/feynman-rules/scattering",
    data
  );
}
