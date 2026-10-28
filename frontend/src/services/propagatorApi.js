const API_BASE_URL = "http://127.0.0.1:8000";

export async function calculatePropagator(data) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/propagator`,
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
      payload.detail || "Propagator calculation failed."
    );
  }

  return payload;
}

export async function calculatePropagatorScan(data) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/propagator/scan`,
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
      payload.detail || "Propagator scan failed."
    );
  }

  return payload;
}
