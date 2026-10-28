const API_BASE_URL = "http://127.0.0.1:8000";

export async function calculateOperatorEigenstates(
  operator
) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/operators-eigenstates`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        operator,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Operator eigenstate calculation failed."
    );
  }

  return data;
}


export async function calculateCustomOperator(
  parameters
) {
  const response = await fetch(
    `${API_BASE_URL}/api/quantum/operators-eigenstates/custom`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(parameters),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Custom operator calculation failed."
    );
  }

  return data;
}
