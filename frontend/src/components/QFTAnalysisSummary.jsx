export default function QFTAnalysisSummary({ analysis }) {
  if (!analysis) {
    return null;
  }

  return (
    <section
      style={{
        marginTop: "24px",
        padding: "16px",
        border: "1px solid #334155",
        borderRadius: "12px",
        background: "#0f172a",
        color: "#e2e8f0",
      }}
    >
      <h3 style={{ marginTop: 0 }}>
        Unified QFT Process Analysis
      </h3>

      <p>
        <strong>Process:</strong>{" "}
        {analysis.process}
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(140px, 1fr))",
          gap: "10px",
          marginTop: "12px",
        }}
      >
        <div>
          <strong>Candidates</strong>
          <div>{analysis.candidate_count}</div>
        </div>

        <div>
          <strong>Allowed</strong>
          <div>{analysis.allowed_count}</div>
        </div>

        <div>
          <strong>Forbidden</strong>
          <div>{analysis.forbidden_count}</div>
        </div>

        <div>
          <strong>Undecidable</strong>
          <div>{analysis.undecidable_count}</div>
        </div>
      </div>

      <p style={{ marginBottom: 0 }}>
        <strong>Overall status:</strong>{" "}
        {analysis.status}
      </p>

      {analysis.topology_results?.length > 0 && (
        <div style={{ marginTop: "16px" }}>
          <strong>Discovered topologies</strong>

          <div style={{ marginTop: "8px" }}>
            {analysis.topology_results.map((candidate) => (
              <div
                key={candidate.candidate_id}
                style={{
                  padding: "10px",
                  marginBottom: "8px",
                  border: "1px solid #475569",
                  borderRadius: "8px",
                }}
              >
                <div>
                  <strong>
                    {candidate.topology}
                  </strong>
                </div>

                <div>
                  Status: {candidate.status}
                </div>

                {candidate.reasons?.length > 0 && (
                  <ul>
                    {candidate.reasons.map((reason, index) => (
                      <li key={index}>{reason}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
