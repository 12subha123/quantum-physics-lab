import { useState } from "react";
import { useQFTProcessAnalysis } from "../hooks/useQFTProcessAnalysis";
import QFTAnalysisSummary from "./QFTAnalysisSummary";
import UnifiedFeynmanDiagram from "./UnifiedFeynmanDiagram";

const PRESETS = {
  "e-e+ -> mu-mu+": {
    incoming: ["e-", "e+"],
    outgoing: ["mu-", "mu+"],
  },
  "Bhabha scattering": {
    incoming: ["e-", "e+"],
    outgoing: ["e-", "e+"],
  },
  "Moller scattering": {
    incoming: ["e-", "e-"],
    outgoing: ["e-", "e-"],
  },
  "u-ubar -> gg": {
    incoming: ["u", "anti-up"],
    outgoing: ["g", "g"],
  },
};

export default function UnifiedQFTProcessLab() {
  const [preset, setPreset] = useState("e-e+ -> mu-mu+");

  const {
    analysis,
    loading,
    error,
    analyze,
  } = useQFTProcessAnalysis();

  const runAnalysis = async () => {
    const process = PRESETS[preset];

    await analyze({
      incoming: process.incoming,
      outgoing: process.outgoing,
      maxVertices: 4,
    });
  };

  return (
    <div>
      <section
        style={{
          marginBottom: "20px",
          padding: "16px",
          border: "1px solid #334155",
          borderRadius: "12px",
        }}
      >
        <h2>Unified Quantum Field Theory Laboratory</h2>

        <label>
          Process{" "}
          <select
            value={preset}
            onChange={(event) => setPreset(event.target.value)}
          >
            {Object.keys(PRESETS).map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </select>
        </label>

        <button
          type="button"
          onClick={runAnalysis}
          disabled={loading}
          style={{
            marginLeft: "12px",
            padding: "8px 14px",
          }}
        >
          {loading ? "Analyzing..." : "Analyze Process"}
        </button>

        {error && (
          <p style={{ color: "#f87171" }}>
            {error}
          </p>
        )}
      </section>

      <UnifiedFeynmanDiagram analysis={analysis} />

      <QFTAnalysisSummary analysis={analysis} />
    </div>
  );
}

