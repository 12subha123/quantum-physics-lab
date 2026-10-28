import { useCallback, useState } from "react";
import { analyzeQFTProcess } from "../services/qftAnalysisApi";

export function useQFTProcessAnalysis() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyze = useCallback(
    async ({
      incoming,
      outgoing,
      maxVertices = 4,
    }) => {
      setLoading(true);
      setError("");

      try {
        const result = await analyzeQFTProcess({
          incoming,
          outgoing,
          maxVertices,
        });

        setAnalysis(result);
        return result;
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : "Unknown QFT analysis error.";

        setError(message);
        setAnalysis(null);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  const reset = useCallback(() => {
    setAnalysis(null);
    setError("");
    setLoading(false);
  }, []);

  return {
    analysis,
    loading,
    error,
    analyze,
    reset,
  };
}
