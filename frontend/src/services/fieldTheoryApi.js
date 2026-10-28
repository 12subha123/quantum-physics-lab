const API_BASE_URL = "http://127.0.0.1:8000";

export async function calculateKleinGordon(mass) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/klein-gordon`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        mass: Number(mass),
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : "Klein-Gordon calculation failed."
    );
  }

  return data;
}

export async function simulateKleinGordon(parameters) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/field-theory/klein-gordon/simulation`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        mass: Number(parameters.mass),
        amplitude: Number(parameters.amplitude),
        width: Number(parameters.width),
        wavenumber: Number(parameters.wavenumber),
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
        : "Klein-Gordon simulation failed."
    );
  }

  return data;
}
