const API_BASE_URL = "http://127.0.0.1:8000";

export async function analyzeMultiQubit(
  amplitudesReal,
  amplitudesImag = null
) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/multiqubit`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        amplitudes_real: amplitudesReal,
        amplitudes_imag: amplitudesImag,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Multi-qubit analysis failed."
    );
  }

  return data;
}
