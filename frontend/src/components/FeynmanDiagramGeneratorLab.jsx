import { useMemo, useState } from "react";
import { generateFeynmanDiagrams } from "../services/feynmanDiagramGeneratorApi";
import { generateTopologies } from "../services/topologyApi";
import { calculateQEDAmplitude } from "../services/qedAmplitudeApi";
import { analyzeQEDChannels } from "../services/qedChannelAnalysisApi";
import { calculateQCDAngularObservable } from "../services/qcdAngularObservableApi";

const API_BASE_URL = "http://127.0.0.1:8000";

const PARTICLES = [
  { id: "electron", label: "electron (e⁻)", theory: "Lepton" },
  { id: "positron", label: "positron (e⁺)", theory: "Lepton" },
  { id: "muon", label: "muon (μ⁻)", theory: "Lepton" },
  { id: "antimuon", label: "antimuon (μ⁺)", theory: "Lepton" },
  { id: "tau", label: "tau (τ⁻)", theory: "Lepton" },
  { id: "antitau", label: "antitau (τ⁺)", theory: "Lepton" },
  { id: "electron_neutrino", label: "electron neutrino (νe)", theory: "Lepton" },
  { id: "electron_antineutrino", label: "electron antineutrino (ν̄e)", theory: "Lepton" },
  { id: "muon_neutrino", label: "muon neutrino (νμ)", theory: "Lepton" },
  { id: "muon_antineutrino", label: "muon antineutrino (ν̄μ)", theory: "Lepton" },
  { id: "tau_neutrino", label: "tau neutrino (ντ)", theory: "Lepton" },
  { id: "tau_antineutrino", label: "tau antineutrino (ν̄τ)", theory: "Lepton" },

  { id: "up", label: "up quark (u)", theory: "Quark" },
  { id: "anti_up", label: "anti-up quark (ū)", theory: "Quark" },
  { id: "down", label: "down quark (d)", theory: "Quark" },
  { id: "anti_down", label: "anti-down quark (d̄)", theory: "Quark" },
  { id: "strange", label: "strange quark (s)", theory: "Quark" },
  { id: "anti_strange", label: "anti-strange quark (s̄)", theory: "Quark" },
  { id: "charm", label: "charm quark (c)", theory: "Quark" },
  { id: "anti_charm", label: "anti-charm quark (c̄)", theory: "Quark" },
  { id: "bottom", label: "bottom quark (b)", theory: "Quark" },
  { id: "anti_bottom", label: "anti-bottom quark (b̄)", theory: "Quark" },
  { id: "top", label: "top quark (t)", theory: "Quark" },
  { id: "anti_top", label: "anti-top quark (t̄)", theory: "Quark" },

  { id: "photon", label: "photon (γ)", theory: "Gauge boson" },
  { id: "gluon", label: "gluon (g)", theory: "Gauge boson" },
  { id: "w+", label: "W⁺", theory: "Gauge boson" },
  { id: "w-", label: "W⁻", theory: "Gauge boson" },
  { id: "z", label: "Z⁰", theory: "Gauge boson" },
  { id: "higgs", label: "Higgs (H)", theory: "Scalar" },
  { id: "scalar", label: "generic scalar (φ)", theory: "Scalar" },

  { id: "proton", label: "proton (p)", theory: "Composite" },
  { id: "antiproton", label: "antiproton (p̄)", theory: "Composite" },
  { id: "neutron", label: "neutron (n)", theory: "Composite" },
  { id: "antineutron", label: "antineutron (n̄)", theory: "Composite" },
];

const PRESETS = [
  {
    name: "e⁻ e⁺ → μ⁻ μ⁺",
    initial: ["electron", "positron"],
    final: ["muon", "antimuon"],
  },
  {
    name: "Bhabha scattering",
    initial: ["electron", "positron"],
    final: ["electron", "positron"],
  },
  {
    name: "Møller scattering",
    initial: ["electron", "electron"],
    final: ["electron", "electron"],
  },
  {
    name: "u ū → g g",
    initial: ["up", "anti_up"],
    final: ["gluon", "gluon"],
  },
  {
    name: "e⁻ e⁺ → μ⁻ μ⁺ γ",
    initial: ["electron", "positron"],
    final: ["muon", "antimuon", "photon"],
  },
  {
    name: "e⁻ → e⁻ γ",
    initial: ["electron"],
    final: ["electron", "photon"],
  },
];

const THEORY_COLORS = {
  QED: "#38bdf8",
  QCD: "#f97316",
  Electroweak: "#a78bfa",
  "Scalar phi4": "#4ade80",
};

function particleLabel(id) {
  return PARTICLES.find((p) => p.id === id)?.label || id;
}

function particleSymbol(id) {
  const symbols = {
    electron: "e⁻",
    positron: "e⁺",
    muon: "μ⁻",
    antimuon: "μ⁺",
    tau: "τ⁻",
    antitau: "τ⁺",
    electron_neutrino: "νe",
    electron_antineutrino: "ν̄e",
    muon_neutrino: "νμ",
    muon_antineutrino: "ν̄μ",
    tau_neutrino: "ντ",
    tau_antineutrino: "ν̄τ",
    up: "u",
    anti_up: "ū",
    down: "d",
    anti_down: "d̄",
    strange: "s",
    anti_strange: "s̄",
    charm: "c",
    anti_charm: "c̄",
    bottom: "b",
    anti_bottom: "b̄",
    top: "t",
    anti_top: "t̄",
    photon: "γ",
    gluon: "g",
    "w+": "W⁺",
    "w-": "W⁻",
    z: "Z",
    higgs: "H",
    scalar: "φ",
    proton: "p",
    antiproton: "p̄",
    neutron: "n",
    antineutron: "n̄",
  };

  return symbols[id] || id;
}

function processText(initial, final) {
  return `${initial.map(particleSymbol).join(" + ")} → ${final
    .map(particleSymbol)
    .join(" + ")}`;
}

function DiagramSVG({ diagram }) {
  const width = 760;
  const height = 330;

  const lines = diagram?.lines || [];
  const vertices = diagram?.vertices || [];
  const topology = diagram?.topology || "tree-level";

  const external = lines.filter(
    (line) =>
      line.role === "incoming" ||
      line.role === "outgoing" ||
      line.role === "initial" ||
      line.role === "final"
  );

  const internal = lines.filter(
    (line) =>
      line.role === "internal" ||
      line.field_type === "internal" ||
      line.direction === "internal"
  );

  const incoming = external.filter(
    (line) =>
      line.role === "incoming" ||
      line.role === "initial"
  );

  const outgoing = external.filter(
    (line) =>
      line.role === "outgoing" ||
      line.role === "final"
  );

  const vertexPositions =
    vertices.length === 0
      ? [{ x: width / 2, y: height / 2 }]
      : vertices.map((_, index) => ({
          x:
            vertices.length === 1
              ? width / 2
              : 250 + (index * 260) / Math.max(vertices.length - 1, 1),
          y: height / 2,
        }));

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      width="100%"
      role="img"
      aria-label={`Feynman diagram ${diagram?.process || ""}`}
      style={{
        background: "#07111f",
        borderRadius: 14,
        border: "1px solid #1e293b",
      }}
    >
      <text
        x="20"
        y="28"
        fill="#e2e8f0"
        fontSize="17"
        fontWeight="700"
      >
        {diagram?.theory || "Tree-level"} · {topology}
      </text>

      {incoming.map((line, index) => {
        const y = 95 + index * 105;
        const vertex = vertexPositions[0];

        return (
          <g key={`in-${line.line_id || index}`}>
            <line
              x1="55"
              y1={y}
              x2={vertex.x}
              y2={vertex.y}
              stroke="#cbd5e1"
              strokeWidth="3"
            />
            <polygon
              points={`${vertex.x - 12},${vertex.y - 7} ${vertex.x},${vertex.y} ${vertex.x - 12},${vertex.y + 7}`}
              fill="#cbd5e1"
            />
            <text x="55" y={y - 12} fill="#f8fafc" fontSize="16">
              {particleSymbol(line.particle)}
            </text>
            <text x="55" y={y + 25} fill="#94a3b8" fontSize="12">
              {line.momentum || `p${index + 1}`}
            </text>
          </g>
        );
      })}

      {outgoing.map((line, index) => {
        const y = 95 + index * 105;
        const vertex = vertexPositions[vertexPositions.length - 1];

        return (
          <g key={`out-${line.line_id || index}`}>
            <line
              x1={vertex.x}
              y1={vertex.y}
              x2={width - 55}
              y2={y}
              stroke="#cbd5e1"
              strokeWidth="3"
            />
            <polygon
              points={`${width - 43},${y - 7} ${width - 55},${y} ${width - 43},${y + 7}`}
              fill="#cbd5e1"
            />
            <text
              x={width - 130}
              y={y - 12}
              fill="#f8fafc"
              fontSize="16"
            >
              {particleSymbol(line.particle)}
            </text>
            <text
              x={width - 130}
              y={y + 25}
              fill="#94a3b8"
              fontSize="12"
            >
              {line.momentum || `p${index + 3}`}
            </text>
          </g>
        );
      })}

      {internal.map((line, index) => {
        const y = height / 2 + (index - (internal.length - 1) / 2) * 42;

        const x1 = vertexPositions[0]?.x || 250;
        const x2 =
          vertexPositions[vertexPositions.length - 1]?.x || 510;

        const isFermion = [
          "electron",
          "positron",
          "muon",
          "antimuon",
          "tau",
          "antitau",
          "up",
          "anti_up",
          "down",
          "anti_down",
          "strange",
          "anti_strange",
          "charm",
          "anti_charm",
          "bottom",
          "anti_bottom",
          "top",
          "anti_top",
        ].includes(line.particle);

        return (
          <g key={`internal-${line.line_id || index}`}>
            <line
              x1={x1}
              y1={y}
              x2={x2}
              y2={y}
              stroke={isFermion ? "#f8fafc" : "#94a3b8"}
              strokeWidth="3"
              strokeDasharray={isFermion ? undefined : "10 7"}
            />

            {isFermion && (
              <polygon
                points={`${(x1 + x2) / 2 + 9},${y - 6} ${
                  (x1 + x2) / 2 + 20
                },${y} ${(x1 + x2) / 2 + 9},${y + 6}`}
                fill="#f8fafc"
              />
            )}

            <text
              x={(x1 + x2) / 2}
              y={y - 12}
              textAnchor="middle"
              fill="#f8fafc"
              fontSize="15"
            >
              {particleSymbol(line.particle)}
            </text>

            <text
              x={(x1 + x2) / 2}
              y={y + 25}
              textAnchor="middle"
              fill="#94a3b8"
              fontSize="12"
            >
              {line.momentum || `q${index + 1}`}
            </text>
          </g>
        );
      })}

      {vertexPositions.map((position, index) => (
        <g key={`vertex-${index}`}>
          <circle
            cx={position.x}
            cy={position.y}
            r="9"
            fill="#f8fafc"
          />
          <text
            x={position.x}
            y={position.y + 32}
            textAnchor="middle"
            fill="#94a3b8"
            fontSize="12"
          >
            V{index + 1}
          </text>
        </g>
      ))}
    </svg>
  );
}

function Section({ title, children }) {
  return (
    <section
      style={{
        marginTop: 18,
        padding: 18,
        background: "#0b1627",
        border: "1px solid #1e293b",
        borderRadius: 14,
      }}
    >
      <h3
        style={{
          margin: "0 0 14px",
          color: "#f8fafc",
          fontSize: 18,
        }}
      >
        {title}
      </h3>
      {children}
    </section>
  );
}

function ChipList({ values, onRemove }) {
  if (!values.length) {
    return (
      <span style={{ color: "#64748b", fontSize: 13 }}>
        None selected
      </span>
    );
  }

  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
      {values.map((value, index) => (
        <button
          key={`${value}-${index}`}
          type="button"
          onClick={() => onRemove(index)}
          style={{
            border: "1px solid #334155",
            background: "#111c2e",
            color: "#e2e8f0",
            borderRadius: 999,
            padding: "7px 10px",
            cursor: "pointer",
          }}
          title="Remove particle"
        >
          {particleSymbol(value)} ×
        </button>
      ))}
    </div>
  );
}

export default function FeynmanDiagramGeneratorLab() {
  const [initialParticles, setInitialParticles] = useState([
    "electron",
    "positron",
  ]);

  const [finalParticles, setFinalParticles] = useState([
    "muon",
    "antimuon",
  ]);

  const [selectedParticle, setSelectedParticle] = useState("electron");
  const [targetSide, setTargetSide] = useState("initial");

  const [vertices, setVertices] = useState([]);
  const [vertexSummary, setVertexSummary] = useState(null);
  const [topologyData, setTopologyData] = useState(null);
  const [diagramData, setDiagramData] = useState(null);
  const [selectedDiagram, setSelectedDiagram] = useState(null);
  const [qedAmplitude, setQEDAmplitude] = useState(null);
  const [qedChannels, setQEDChannels] = useState(null);
  const [qcdObservable, setQCDObservable] = useState(null);

  const [sqrtS, setSqrtS] = useState(10);
  const [alphaS, setAlphaS] = useState(0.118);
  const [angularCut, setAngularCut] = useState(0.1);
  const [angularPoints, setAngularPoints] = useState(80);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const process = useMemo(
    () => processText(initialParticles, finalParticles),
    [initialParticles, finalParticles]
  );

  const selectedTheory = useMemo(() => {
    const ids = [...initialParticles, ...finalParticles];

    if (ids.some((id) => ["gluon", "up", "anti_up", "down", "anti_down", "strange", "anti_strange", "charm", "anti_charm", "bottom", "anti_bottom", "top", "anti_top"].includes(id))) {
      return "QCD / mixed";
    }

    if (ids.some((id) => ["w+", "w-", "z", "higgs", "electron_neutrino", "electron_antineutrino", "muon_neutrino", "muon_antineutrino", "tau_neutrino", "tau_antineutrino"].includes(id))) {
      return "Electroweak / mixed";
    }

    if (ids.includes("scalar")) {
      return "Scalar phi4";
    }

    return "QED";
  }, [initialParticles, finalParticles]);

  function addParticle() {
    if (targetSide === "initial") {
      setInitialParticles((current) => [...current, selectedParticle]);
    } else {
      setFinalParticles((current) => [...current, selectedParticle]);
    }
  }

  function removeInitial(index) {
    setInitialParticles((current) =>
      current.filter((_, i) => i !== index)
    );
  }

  function removeFinal(index) {
    setFinalParticles((current) =>
      current.filter((_, i) => i !== index)
    );
  }

  function applyPreset(preset) {
    setInitialParticles(preset.initial);
    setFinalParticles(preset.final);
    setVertices([]);
    setVertexSummary(null);
    setTopologyData(null);
    setDiagramData(null);
    setSelectedDiagram(null);
    setQEDAmplitude(null);
    setQEDChannels(null);
    setQCDObservable(null);
    setError("");
  }

  async function discoverInteractions() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/quantum/field-theory/standard-model/match-process-vertices`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            initial_particles: initialParticles,
            final_particles: finalParticles,
          }),
        }
      );

      const payload = await response.json();

      if (!response.ok) {
        throw new Error(
          Array.isArray(payload.detail)
            ? payload.detail.join(", ")
            : payload.detail || "Vertex matching failed."
        );
      }

      setVertices(payload.vertices || []);
      setVertexSummary(payload);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function runLaboratory() {
    if (!initialParticles.length || !finalParticles.length) {
      setError("Select at least one incoming and one outgoing particle.");
      return;
    }

    setLoading(true);
    setError("");

    setQEDAmplitude(null);
    setQEDChannels(null);
    setQCDObservable(null);

    try {
      const [vertexResponse, topologyResponse, diagramResponse] =
        await Promise.all([
          fetch(
            `${API_BASE_URL}/api/quantum/field-theory/standard-model/match-process-vertices`,
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                initial_particles: initialParticles,
                final_particles: finalParticles,
              }),
            }
          ),
          generateTopologies({
            initial_particles: initialParticles,
            final_particles: finalParticles,
          }),
          generateFeynmanDiagrams({
            initial_particles: initialParticles,
            final_particles: finalParticles,
          }),
        ]);

      const vertexPayload = await vertexResponse.json();

      if (!vertexResponse.ok) {
        throw new Error(
          Array.isArray(vertexPayload.detail)
            ? vertexPayload.detail.join(", ")
            : vertexPayload.detail || "Vertex discovery failed."
        );
      }

      setVertices(vertexPayload.vertices || []);
      setVertexSummary(vertexPayload);

      setTopologyData(topologyResponse);
      setDiagramData(diagramResponse);
      setSelectedDiagram(
        diagramResponse?.diagrams?.[0] ||
          diagramResponse?.candidates?.[0] ||
          null
      );

      const isQED =
        initialParticles.length === 2 &&
        finalParticles.length === 2 &&
        ["electron", "positron", "muon", "antimuon", "tau", "antitau"].every(
          (p) => true
        ) &&
        initialParticles.every((p) =>
          ["electron", "positron", "muon", "antimuon", "tau", "antitau"].includes(p)
        ) &&
        finalParticles.every((p) =>
          ["electron", "positron", "muon", "antimuon", "tau", "antitau"].includes(p)
        );

      if (isQED) {
        try {
          const amplitude = await calculateQEDAmplitude({
            process: process.includes("μ")
              ? "electron_muon_annihilation"
              : "electron_muon_annihilation",
            sqrt_s: Number(sqrtS),
            scattering_angle: Math.PI / 2,
          });

          setQEDAmplitude(amplitude);
        } catch {
          setQEDAmplitude(null);
        }

        try {
          const channelProcess =
            process === "e⁻ + e⁺ → e⁻ + e⁺"
              ? "bhabha"
              : process === "e⁻ + e⁻ → e⁻ + e⁻"
                ? "moller"
                : "electron_muon_annihilation";

          const channels = await analyzeQEDChannels({
            process: channelProcess,
            sqrt_s: Number(sqrtS),
            scattering_angle: Math.PI / 2,
          });

          setQEDChannels(channels);
        } catch {
          setQEDChannels(null);
        }
      }

      const isQQbarGG =
        initialParticles.length === 2 &&
        initialParticles[0] === "up" &&
        initialParticles[1] === "anti_up" &&
        finalParticles.length === 2 &&
        finalParticles[0] === "gluon" &&
        finalParticles[1] === "gluon";

      if (isQQbarGG) {
        try {
          const qcd = await calculateQCDAngularObservable({
            sqrt_s: Number(sqrtS),
            alpha_s: Number(alphaS),
            angular_cut: Number(angularCut),
            points: Number(angularPoints),
          });

          setQCDObservable(qcd);
        } catch {
          setQCDObservable(null);
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const diagrams =
    diagramData?.diagrams ||
    diagramData?.candidates ||
    diagramData?.assignments ||
    [];

  const topologyCandidates =
    topologyData?.candidates ||
    topologyData?.topologies ||
    [];

  return (
    <div
      style={{
        color: "#e2e8f0",
        background: "#020617",
        padding: 20,
        borderRadius: 18,
      }}
    >
      <div style={{ marginBottom: 20 }}>
        <h2
          style={{
            margin: 0,
            fontSize: 27,
            color: "#f8fafc",
          }}
        >
          Universal Feynman Interaction Laboratory
        </h2>

        <p
          style={{
            marginTop: 8,
            color: "#94a3b8",
            lineHeight: 1.6,
          }}
        >
          Particle process → Standard Model interaction discovery →
          tree-level topologies → Feynman diagrams → vertices →
          propagators → flow → Feynman rules → amplitudes →
          numerical observables.
        </p>
      </div>

      <Section title="1. Particle Process">
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: 8,
            marginBottom: 14,
          }}
        >
          {PRESETS.map((preset) => (
            <button
              key={preset.name}
              type="button"
              onClick={() => applyPreset(preset)}
              style={{
                padding: "8px 11px",
                borderRadius: 8,
                border: "1px solid #334155",
                background: "#111827",
                color: "#e2e8f0",
                cursor: "pointer",
              }}
            >
              {preset.name}
            </button>
          ))}
        </div>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
            gap: 14,
          }}
        >
          <div>
            <label>Particle</label>
            <select
              value={selectedParticle}
              onChange={(event) =>
                setSelectedParticle(event.target.value)
              }
              style={{
                width: "100%",
                marginTop: 6,
                padding: 10,
                background: "#111827",
                color: "#f8fafc",
                border: "1px solid #334155",
                borderRadius: 8,
              }}
            >
              {PARTICLES.map((particle) => (
                <option key={particle.id} value={particle.id}>
                  {particle.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label>Target side</label>
            <select
              value={targetSide}
              onChange={(event) => setTargetSide(event.target.value)}
              style={{
                width: "100%",
                marginTop: 6,
                padding: 10,
                background: "#111827",
                color: "#f8fafc",
                border: "1px solid #334155",
                borderRadius: 8,
              }}
            >
              <option value="initial">Incoming</option>
              <option value="final">Outgoing</option>
            </select>
          </div>

          <div style={{ display: "flex", alignItems: "end" }}>
            <button
              type="button"
              onClick={addParticle}
              style={{
                width: "100%",
                padding: 10,
                borderRadius: 8,
                border: "1px solid #38bdf8",
                background: "#0c4a6e",
                color: "#f8fafc",
                cursor: "pointer",
              }}
            >
              Add particle
            </button>
          </div>
        </div>

        <div style={{ marginTop: 16 }}>
          <div style={{ marginBottom: 7, color: "#94a3b8" }}>
            Incoming
          </div>
          <ChipList
            values={initialParticles}
            onRemove={removeInitial}
          />
        </div>

        <div style={{ marginTop: 16 }}>
          <div style={{ marginBottom: 7, color: "#94a3b8" }}>
            Outgoing
          </div>
          <ChipList
            values={finalParticles}
            onRemove={removeFinal}
          />
        </div>

        <div
          style={{
            marginTop: 16,
            padding: 13,
            borderRadius: 10,
            background: "#111827",
            color: "#f8fafc",
            fontSize: 17,
            fontWeight: 600,
          }}
        >
          {process}
        </div>

        <div
          style={{
            marginTop: 8,
            color: "#94a3b8",
            fontSize: 13,
          }}
        >
          Detected theory family: {selectedTheory}
        </div>

        <div style={{ display: "flex", gap: 10, marginTop: 16 }}>
          <button
            type="button"
            onClick={discoverInteractions}
            disabled={loading}
            style={{
              padding: "10px 15px",
              borderRadius: 8,
              border: "1px solid #64748b",
              background: "#1e293b",
              color: "#f8fafc",
              cursor: "pointer",
            }}
          >
            Discover interactions
          </button>

          <button
            type="button"
            onClick={runLaboratory}
            disabled={loading}
            style={{
              padding: "10px 18px",
              borderRadius: 8,
              border: "1px solid #4ade80",
              background: "#14532d",
              color: "#f8fafc",
              cursor: "pointer",
              fontWeight: 700,
            }}
          >
            {loading ? "Running laboratory..." : "Run complete analysis"}
          </button>
        </div>

        {error && (
          <div
            style={{
              marginTop: 14,
              padding: 12,
              background: "#450a0a",
              border: "1px solid #7f1d1d",
              borderRadius: 8,
              color: "#fecaca",
            }}
          >
            {error}
          </div>
        )}
      </Section>

      <Section title="2. Standard Model Interaction Discovery">
        {!vertexSummary ? (
          <p style={{ color: "#64748b" }}>
            Run interaction discovery to query the Standard Model
            vertex matcher.
          </p>
        ) : (
          <>
            <div style={{ marginBottom: 12 }}>
              Matching vertices:{" "}
              <strong>{vertexSummary.vertex_count || 0}</strong>
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit,minmax(250px,1fr))",
                gap: 10,
              }}
            >
              {vertices.map((vertex, index) => (
                <div
                  key={`${vertex.id || vertex.vertex_id || index}`}
                  style={{
                    padding: 13,
                    borderRadius: 10,
                    border: "1px solid #334155",
                    background: "#111827",
                  }}
                >
                  <div
                    style={{
                      fontWeight: 700,
                      color:
                        THEORY_COLORS[vertex.theory] || "#e2e8f0",
                    }}
                  >
                    {vertex.id || vertex.vertex_id || `Vertex ${index + 1}`}
                  </div>

                  <div style={{ marginTop: 6, color: "#cbd5e1" }}>
                    {vertex.name ||
                      vertex.interaction ||
                      vertex.description ||
                      "Standard Model interaction vertex"}
                  </div>

                  <div
                    style={{
                      marginTop: 6,
                      fontSize: 12,
                      color: "#94a3b8",
                    }}
                  >
                    {vertex.theory || "Standard Model"}
                  </div>
                </div>
              ))}
            </div>

            {!vertices.length && (
              <div style={{ color: "#fbbf24" }}>
                No matching vertex was found for this complete process.
                This does not by itself prove that the process is
                physically forbidden; the topology layer must also be
                considered.
              </div>
            )}
          </>
        )}
      </Section>

      <Section title="3. Tree-Level Topologies">
        {!topologyData ? (
          <p style={{ color: "#64748b" }}>
            Run the complete analysis to generate topology candidates.
          </p>
        ) : (
          <>
            <div style={{ marginBottom: 12 }}>
              Candidate topologies:{" "}
              <strong>{topologyCandidates.length}</strong>
            </div>

            <div
              style={{
                display: "grid",
                gap: 9,
              }}
            >
              {topologyCandidates.map((candidate, index) => (
                <div
                  key={candidate.topology || candidate.diagram_id || index}
                  style={{
                    padding: 12,
                    background: "#111827",
                    border: "1px solid #334155",
                    borderRadius: 9,
                  }}
                >
                  <strong>
                    {candidate.channel ||
                      candidate.topology ||
                      `Topology ${index + 1}`}
                  </strong>

                  {candidate.internal_particle && (
                    <span style={{ color: "#94a3b8", marginLeft: 10 }}>
                      internal: {particleSymbol(candidate.internal_particle)}
                    </span>
                  )}
                </div>
              ))}
            </div>

            {!topologyCandidates.length && (
              <div style={{ color: "#fbbf24" }}>
                The general topology interface accepted this process,
                but no topology generator is currently implemented for
                this specific particle combination.
              </div>
            )}
          </>
        )}
      </Section>

      <Section title="4. Feynman Diagram Visualization">
        {!diagrams.length ? (
          <div style={{ color: "#94a3b8" }}>
            No diagram was returned by the current diagram generator.
            Unsupported processes remain visible as explicit
            “not yet supported” states rather than being replaced by a
            fake diagram.
          </div>
        ) : (
          <>
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                gap: 8,
                marginBottom: 14,
              }}
            >
              {diagrams.map((diagram, index) => (
                <button
                  key={diagram.diagram_id || index}
                  type="button"
                  onClick={() => setSelectedDiagram(diagram)}
                  style={{
                    padding: "8px 11px",
                    borderRadius: 8,
                    border: "1px solid #334155",
                    background:
                      selectedDiagram === diagram
                        ? "#1e3a5f"
                        : "#111827",
                    color: "#f8fafc",
                    cursor: "pointer",
                  }}
                >
                  {diagram.channel ||
                    diagram.topology ||
                    diagram.diagram_id ||
                    `Diagram ${index + 1}`}
                </button>
              ))}
            </div>

            {selectedDiagram && (
              <>
                <DiagramSVG diagram={selectedDiagram} />

                <div
                  style={{
                    marginTop: 12,
                    padding: 12,
                    background: "#111827",
                    borderRadius: 9,
                    color: "#cbd5e1",
                  }}
                >
                  <strong>{selectedDiagram.process}</strong>
                  <br />
                  Theory: {selectedDiagram.theory || "—"}
                  <br />
                  Topology: {selectedDiagram.topology || "—"}
                  <br />
                  Internal particle:{" "}
                  {selectedDiagram.internal_particle
                    ? particleSymbol(selectedDiagram.internal_particle)
                    : "none"}
                </div>
              </>
            )}
          </>
        )}
      </Section>

      <Section title="5. Vertices, Propagators & Flow">
        {selectedDiagram ? (
          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit,minmax(250px,1fr))",
              gap: 12,
            }}
          >
            <div
              style={{
                padding: 13,
                background: "#111827",
                borderRadius: 10,
              }}
            >
              <h4>Vertices</h4>
              {(selectedDiagram.vertices || []).map(
                (vertex, index) => (
                  <div
                    key={vertex.vertex_id || index}
                    style={{
                      marginTop: 9,
                      padding: 9,
                      borderLeft: "3px solid #38bdf8",
                    }}
                  >
                    <strong>
                      {vertex.vertex_id || `V${index + 1}`}
                    </strong>
                    <br />
                    {vertex.interaction || "interaction"}
                    <br />
                    <span style={{ color: "#94a3b8" }}>
                      {vertex.factor || "factor unavailable"}
                    </span>
                  </div>
                )
              )}
            </div>

            <div
              style={{
                padding: 13,
                background: "#111827",
                borderRadius: 10,
              }}
            >
              <h4>Internal propagators</h4>
              {(selectedDiagram.internal_lines || []).map(
                (line, index) => (
                  <div
                    key={line.line_id || index}
                    style={{
                      marginTop: 9,
                      padding: 9,
                      borderLeft: "3px solid #f97316",
                    }}
                  >
                    <strong>
                      {line.line_id || `q${index + 1}`}
                    </strong>
                    <br />
                    {particleSymbol(line.particle)}
                    <br />
                    <span style={{ color: "#94a3b8" }}>
                      momentum: {line.momentum || "symbolic"}
                    </span>
                  </div>
                )
              )}

              {!selectedDiagram.internal_lines?.length && (
                <span style={{ color: "#64748b" }}>
                  No internal propagator.
                </span>
              )}
            </div>

            <div
              style={{
                padding: 13,
                background: "#111827",
                borderRadius: 10,
              }}
            >
              <h4>External flow</h4>
              {(selectedDiagram.lines || []).map(
                (line, index) => (
                  <div
                    key={line.line_id || index}
                    style={{
                      marginTop: 7,
                      color: "#cbd5e1",
                    }}
                  >
                    {line.role || line.direction || "external"}:{" "}
                    {particleSymbol(line.particle)}
                    {line.momentum
                      ? ` (${line.momentum})`
                      : ""}
                  </div>
                )
              )}
            </div>
          </div>
        ) : (
          <p style={{ color: "#64748b" }}>
            Generate a diagram to inspect its graph structure.
          </p>
        )}
      </Section>

      <Section title="6. Feynman Rules & Symbolic Amplitude">
        {selectedDiagram ? (
          <>
            {(selectedDiagram.vertices || []).map(
              (vertex, index) => (
                <div
                  key={vertex.vertex_id || index}
                  style={{
                    padding: 12,
                    marginBottom: 8,
                    background: "#111827",
                    borderRadius: 9,
                  }}
                >
                  <strong>
                    {vertex.vertex_id || `Vertex ${index + 1}`}
                  </strong>
                  <div style={{ marginTop: 5 }}>
                    {vertex.interaction || "interaction"}
                  </div>
                  <div
                    style={{
                      marginTop: 5,
                      fontFamily: "monospace",
                      color: "#67e8f9",
                    }}
                  >
                    {vertex.factor || "rule unavailable"}
                  </div>
                </div>
              )
            )}

            <div
              style={{
                marginTop: 14,
                padding: 14,
                background: "#020617",
                border: "1px solid #334155",
                borderRadius: 9,
                fontFamily: "monospace",
                overflowX: "auto",
              }}
            >
              {selectedDiagram.amplitude_structure ||
                selectedDiagram.amplitude_expression ||
                "Symbolic amplitude structure will be assembled by the amplitude layer."}
            </div>
          </>
        ) : (
          <p style={{ color: "#64748b" }}>
            Select a generated diagram to inspect its rules.
          </p>
        )}
      </Section>

      <Section title="7. Numerical Observables">
        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit,minmax(160px,1fr))",
            gap: 10,
            marginBottom: 14,
          }}
        >
          <label>
            √s
            <input
              type="number"
              min="0.001"
              step="0.1"
              value={sqrtS}
              onChange={(event) =>
                setSqrtS(event.target.value)
              }
              style={{
                width: "100%",
                marginTop: 5,
                padding: 9,
                background: "#111827",
                color: "#f8fafc",
                border: "1px solid #334155",
                borderRadius: 8,
              }}
            />
          </label>

          <label>
            αs
            <input
              type="number"
              min="0.001"
              step="0.001"
              value={alphaS}
              onChange={(event) =>
                setAlphaS(event.target.value)
              }
              style={{
                width: "100%",
                marginTop: 5,
                padding: 9,
                background: "#111827",
                color: "#f8fafc",
                border: "1px solid #334155",
                borderRadius: 8,
              }}
            />
          </label>

          <label>
            Angular cut
            <input
              type="number"
              min="0.001"
              max="1.5"
              step="0.01"
              value={angularCut}
              onChange={(event) =>
                setAngularCut(event.target.value)
              }
              style={{
                width: "100%",
                marginTop: 5,
                padding: 9,
                background: "#111827",
                color: "#f8fafc",
                border: "1px solid #334155",
                borderRadius: 8,
              }}
            />
          </label>

          <label>
            Angular points
            <input
              type="number"
              min="10"
              max="2000"
              step="10"
              value={angularPoints}
              onChange={(event) =>
                setAngularPoints(event.target.value)
              }
              style={{
                width: "100%",
                marginTop: 5,
                padding: 9,
                background: "#111827",
                color: "#f8fafc",
                border: "1px solid #334155",
                borderRadius: 8,
              }}
            />
          </label>
        </div>

        {qedAmplitude && (
          <div
            style={{
              padding: 13,
              background: "#082f49",
              border: "1px solid #0369a1",
              borderRadius: 10,
              marginBottom: 10,
            }}
          >
            <strong>QED matrix element</strong>
            <div style={{ marginTop: 7, fontFamily: "monospace" }}>
              |M|² = {qedAmplitude.ms_squared}
            </div>
          </div>
        )}

        {qedChannels && (
          <div
            style={{
              padding: 13,
              background: "#172554",
              border: "1px solid #3730a3",
              borderRadius: 10,
              marginBottom: 10,
            }}
          >
            <strong>QED channel analysis</strong>
            <div
              style={{
                marginTop: 7,
                fontFamily: "monospace",
                whiteSpace: "pre-wrap",
              }}
            >
              {JSON.stringify(qedChannels, null, 2)}
            </div>
          </div>
        )}

        {qcdObservable && (
          <div
            style={{
              padding: 13,
              background: "#431407",
              border: "1px solid #c2410c",
              borderRadius: 10,
            }}
          >
            <strong>QCD angular observable</strong>
            <div style={{ marginTop: 7 }}>
              Total cross section:{" "}
              {qcdObservable.total_cross_section}
            </div>
            <div
              style={{
                marginTop: 5,
                color: "#fed7aa",
                fontSize: 13,
              }}
            >
              LO massless QCD result with explicit angular cut.
            </div>
          </div>
        )}

        {!qedAmplitude && !qcdObservable && (
          <div
            style={{
              padding: 13,
              background: "#111827",
              borderRadius: 10,
              color: "#94a3b8",
            }}
          >
            Numerical evaluation is currently process-dependent.
            The laboratory intentionally does not invent a numerical
            result for interactions whose matrix-element evaluator has
            not yet been implemented.
          </div>
        )}
      </Section>

      <Section title="8. Scientific Scope">
        <ul
          style={{
            color: "#94a3b8",
            lineHeight: 1.7,
            paddingLeft: 20,
          }}
        >
          <li>
            Tree-level perturbative Standard Model interaction
            discovery is the target architecture.
          </li>
          <li>
            Diagram generation is currently implemented for a subset
            of QED charged-lepton processes.
          </li>
          <li>
            The topology engine accepts general N→M process structure,
            while individual topology builders are still being
            expanded.
          </li>
          <li>
            QCD includes symbolic q q̄ → g g amplitudes and a
            leading-order angular observable with an explicit cut.
          </li>
          <li>
            Lorentz algebra, Dirac traces, spin sums and color algebra
            are separate calculation layers.
          </li>
          <li>
            Loop corrections, renormalization, gauge fixing,
            hadronization and detector physics are outside the current
            educational tree-level scope.
          </li>
        </ul>
      </Section>
    </div>
  );
}
