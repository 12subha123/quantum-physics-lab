const API_BASE_URL = "http://127.0.0.1:8000";

export async function calculateQEDAmplitude(data) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/qed-amplitude`,
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
      payload.detail || "QED amplitude calculation failed."
    );
  }

  return payload;
}

export async function calculateQEDAngularScan(data) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/qed-amplitude/scan`,
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
      payload.detail || "QED angular scan failed."
    );
  }

  return payload;
}
