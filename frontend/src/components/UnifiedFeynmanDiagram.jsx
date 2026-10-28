import { useMemo, useState } from "react";

function particleLabel(particle) {
  const labels = {
    electron: "e⁻",
    positron: "e⁺",
    muon: "μ⁻",
    antimuon: "μ⁺",
    photon: "γ",
    gluon: "g",
    z: "Z",
    W: "W",
    "W+": "W⁺",
    "W-": "W⁻",
    Higgs: "H",
    up: "u",
    "anti-up": "ū",
    down: "d",
    "anti-down": "d̄",
  };

  return labels[particle] || particle;
}

function statusClass(status) {
  if (status === "ALLOWED") return "allowed";
  if (status === "FORBIDDEN") return "forbidden";
  return "undecidable";
}

export default function UnifiedFeynmanDiagram({ analysis }) {
  const candidates = analysis?.topology_results ?? [];
  const [selectedIndex, setSelectedIndex] = useState(0);

  const selected = candidates[selectedIndex] ?? null;
  const graph = selected?.graph ?? null;

  const layout = useMemo(() => {
    if (!graph) return null;

    const vertices = graph.vertices ?? [];
    const attachments = graph.external_attachments ?? [];
    const propagators = graph.internal_propagators ?? [];

    const vertexCount = Math.max(vertices.length, 1);
    const width = 760;
    const height = 440;

    const vertexPositions = {};

    vertices.forEach((vertex, index) => {
      const x =
        vertexCount === 1
          ? width / 2
          : 210 + (index * (width - 420)) / (vertexCount - 1);

      vertexPositions[vertex.instance_id] = {
        x,
        y: height / 2,
      };
    });

    const groupedAttachments = {};

    attachments.forEach((attachment) => {
      const list =
        groupedAttachments[attachment.vertex_instance] ??
        [];

      list.push(attachment);
      groupedAttachments[attachment.vertex_instance] = list;
    });

    const externalLines = [];

    Object.entries(groupedAttachments).forEach(
      ([vertexId, legs]) => {
        const vertex = vertexPositions[vertexId];
        if (!vertex) return;

        legs.forEach((leg, index) => {
          const isIncoming = leg.role === "incoming";

          const verticalOffset =
            (index - (legs.length - 1) / 2) * 42;

          const endX = isIncoming ? 55 : width - 55;
          const endY = vertex.y + verticalOffset;

          externalLines.push({
            ...leg,
            x1: vertex.x,
            y1: vertex.y + verticalOffset,
            x2: endX,
            y2: endY,
          });
        });
      },
    );

    const internalLines = propagators
      .map((line) => {
        const a = vertexPositions[line.vertex_a];
        const b = vertexPositions[line.vertex_b];

        if (!a || !b) return null;

        return {
          ...line,
          x1: a.x,
          y1: a.y,
          x2: b.x,
          y2: b.y,
        };
      })
      .filter(Boolean);

    return {
      width,
      height,
      vertexPositions,
      externalLines,
      internalLines,
    };
  }, [graph]);

  if (!analysis) {
    return (
      <section className="qft-diagram-panel">
        <h2>Unified Feynman Diagram</h2>
        <p>Run a QFT process analysis to generate diagrams.</p>
      </section>
    );
  }

  if (!candidates.length) {
    return (
      <section className="qft-diagram-panel">
        <h2>Unified Feynman Diagram</h2>
        <p>No topology candidates were discovered.</p>
      </section>
    );
  }

  return (
    <section className="qft-diagram-panel">
      <h2>Unified Feynman Diagram</h2>

      <div className="qft-topology-selector">
        {candidates.map((candidate, index) => (
          <button
            key={candidate.candidate_id}
            type="button"
            onClick={() => setSelectedIndex(index)}
            className={
              index === selectedIndex
                ? "qft-topology-button active"
                : "qft-topology-button"
            }
          >
            {candidate.topology}-channel #{index + 1}
          </button>
        ))}
      </div>

      {selected && (
        <div className="qft-diagram-meta">
          <strong>
            {selected.process}
          </strong>

          <span className={`qft-status ${statusClass(selected.status)}`}>
            {selected.status}
          </span>

          <span>
            Theory: {graph?.theory ?? "standard_model"}
          </span>
        </div>
      )}

      {selected?.reasons?.length > 0 && (
        <div className="qft-diagram-reasons">
          {selected.reasons.map((reason, index) => (
            <div key={index}>{reason}</div>
          ))}
        </div>
      )}

      {layout && graph && (
        <div className="qft-diagram-canvas">
          <svg
            viewBox={`0 0 ${layout.width} ${layout.height}`}
            width="100%"
            role="img"
            aria-label={`Feynman diagram for ${selected.process}`}
          >
            <defs>
              <marker
                id="fermion-arrow"
                markerWidth="8"
                markerHeight="8"
                refX="7"
                refY="4"
                orient="auto"
              >
                <path d="M0,0 L8,4 L0,8 Z" />
              </marker>
            </defs>

            {layout.externalLines.map((line) => (
              <g key={`external-${line.leg_id}`}>
                <line
                  x1={line.x1}
                  y1={line.y1}
                  x2={line.x2}
                  y2={line.y2}
                  stroke="currentColor"
                  strokeWidth="3"
                  markerEnd={
                    line.physical_particle === "electron" ||
                    line.physical_particle === "muon" ||
                    line.physical_particle === "up" ||
                    line.physical_particle === "down"
                      ? "url(#fermion-arrow)"
                      : undefined
                  }
                />

                <text
                  x={
                    line.role === "incoming"
                      ? line.x2 + 8
                      : line.x2 - 8
                  }
                  y={line.y2 - 8}
                  textAnchor={
                    line.role === "incoming"
                      ? "start"
                      : "end"
                  }
                  fontSize="18"
                  fill="currentColor"
                >
                  {particleLabel(line.physical_particle)}
                </text>
              </g>
            ))}

            {layout.internalLines.map((line) => (
              <g key={line.line_id}>
                <line
                  x1={line.x1}
                  y1={line.y1}
                  x2={line.x2}
                  y2={line.y2}
                  stroke="currentColor"
                  strokeWidth="3"
                  strokeDasharray={
                    line.particle === "photon"
                      ? "10 8"
                      : line.particle === "gluon"
                        ? "3 6"
                        : undefined
                  }
                />

                <text
                  x={(line.x1 + line.x2) / 2}
                  y={(line.y1 + line.y2) / 2 - 12}
                  textAnchor="middle"
                  fontSize="18"
                  fill="currentColor"
                >
                  {particleLabel(line.particle)}
                </text>
              </g>
            ))}

            {Object.entries(layout.vertexPositions).map(
              ([vertexId, position]) => {
                const vertex = graph.vertices.find(
                  (item) => item.instance_id === vertexId,
                );

                return (
                  <g key={vertexId}>
                    <circle
                      cx={position.x}
                      cy={position.y}
                      r="9"
                      fill="currentColor"
                    />

                    <text
                      x={position.x}
                      y={position.y + 34}
                      textAnchor="middle"
                      fontSize="13"
                      fill="currentColor"
                    >
                      {vertex?.catalog_vertex_id ?? "vertex"}
                    </text>
                  </g>
                );
              },
            )}
          </svg>
        </div>
      )}
    </section>
  );
}
