const API_BASE_URL = "http://127.0.0.1:8000";

export async function calculateDirac(momentum, mass) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/dirac`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        momentum: Number(momentum),
        mass: Number(mass),
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Dirac calculation failed."
    );
  }

  return data;
}

export async function simulateDirac(parameters) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/dirac/simulation`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        mass: Number(parameters.mass),
        amplitude: Number(parameters.amplitude),
        width: Number(parameters.width),
        momentum: Number(parameters.momentum),
        domain_length: Number(parameters.domain_length),
        duration: Number(parameters.duration),
        points: Number(parameters.points),
        frames: Number(parameters.frames),
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Dirac simulation failed."
    );
  }

  return data;
}
