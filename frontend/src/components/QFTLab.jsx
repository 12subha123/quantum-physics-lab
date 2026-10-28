import KleinGordonLab from "./KleinGordonLab";
import DiracLab from "./DiracLab";
import RelativisticComparisonLab from "./RelativisticComparisonLab";
import CanonicalQuantizationLab from "./CanonicalQuantizationLab";
import FockSpaceLab from "./FockSpaceLab";
import PropagatorLab from "./PropagatorLab";
import FeynmanRulesLab from "./FeynmanRulesLab";
import FeynmanDiagramLab from "./FeynmanDiagramLab";
import FeynmanDiagramGeneratorLab from "./FeynmanDiagramGeneratorLab";
import QCDAngularObservableLab from "./QCDAngularObservableLab";
import ScatteringSimulationLab from "./ScatteringSimulationLab";
import PathIntegralLab from "./PathIntegralLab";

export default function QFTLab() {
  return (
    <>
      <section
        id="klein-gordon-lab"
        className="experiment-container"
      >
        <KleinGordonLab />
      </section>

      <section
        id="dirac-lab"
        className="experiment-container"
      >
        <DiracLab />
      </section>

      <section
        id="relativistic-comparison-lab"
        className="experiment-container"
      >
        <RelativisticComparisonLab />
      </section>

      <section
        id="canonical-quantization-lab"
        className="experiment-container"
      >
        <CanonicalQuantizationLab />
      </section>

      <section
        id="fock-space-lab"
        className="experiment-container"
      >
        <FockSpaceLab />
      </section>

      <section
        id="propagator-lab"
        className="experiment-container"
      >
        <PropagatorLab />
      </section>

      <section
        id="feynman-rules-lab"
        className="experiment-container"
      >
        <FeynmanRulesLab />
      </section>

      <section
        id="feynman-diagram-lab"
        className="experiment-container"
      >
        <FeynmanDiagramLab />
      </section>

      <section
        id="universal-feynman-diagram-lab"
        className="experiment-container"
      >
        <FeynmanDiagramGeneratorLab />
      </section>
      <section
        id="qcd-angular-observable-lab"
        className="experiment-container"
      >
        <QCDAngularObservableLab />
      </section>

      <section
        id="path-integral-lab"
        className="experiment-container"
      >
        <PathIntegralLab />
      </section>

      <section
        id="scattering-simulation-lab"
        className="experiment-container"
      >
        <ScatteringSimulationLab />
      </section>
    </>
  );
}


