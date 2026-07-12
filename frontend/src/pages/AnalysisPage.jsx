import { useState } from "react";
import { analyseCase } from "../services/api.js";

const demoCase = {
  client_name: "Apollo",
  client_segment: "High Profile",
  fund_type: "UCITS",
  domicile: "Ireland",
  aml_status: "Pending",
  kyc_status: "Completed",
  risk_rating: "High",
  client_priority: "Critical",
  latest_blocker_type: "AML Delay",
  strategic_client: true,
  num_sub_funds: 12,
  num_share_classes: 18,
  num_jurisdictions: 4,
  num_delegates: 5,
  missing_documents: 7,
  sla_days: 10,
  regulatory_review_required: 1,
  blocker_count: 2,
};

export default function AnalysisPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyse() {
    try {
      setLoading(true);
      setError("");

      const response = await analyseCase(demoCase);
      setResult(response);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
        err.message ||
        "Analysis failed",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#05060a] px-6 py-16 text-white">
      <div className="mx-auto max-w-5xl">
        <h1 className="text-4xl font-semibold">
          Carne Compass Analysis
        </h1>

        <p className="mt-3 text-slate-400">
          Test the live FastAPI connection using the Apollo demo case.
        </p>

        <button
          type="button"
          onClick={handleAnalyse}
          disabled={loading}
          className="mt-8 rounded-lg bg-blue-500 px-6 py-3 font-medium text-white disabled:opacity-50"
        >
          {loading ? "Analysing..." : "Run Live Analysis"}
        </button>

        {error && (
          <div className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-red-300">
            {error}
          </div>
        )}

        {result && (
          <section className="mt-10 grid gap-4 md:grid-cols-2">
            <div className="rounded-xl border border-white/10 bg-white/5 p-6">
              <p className="text-sm text-slate-400">
                Complexity
              </p>
              <p className="mt-2 text-3xl font-semibold">
                {result.predicted_complexity}
              </p>
              <p className="mt-2 text-slate-400">
                Confidence: {result.prediction_confidence}%
              </p>
            </div>

            <div className="rounded-xl border border-white/10 bg-white/5 p-6">
              <p className="text-sm text-slate-400">
                Estimated Effort
              </p>
              <p className="mt-2 text-3xl font-semibold">
                {result.estimated_effort.estimated_effort_hours}
              </p>
              <p className="mt-2 text-slate-400">
                person-hours
              </p>
            </div>

            <div className="rounded-xl border border-white/10 bg-white/5 p-6 md:col-span-2">
              <p className="text-sm text-slate-400">
                Recommended Analyst
              </p>

              <p className="mt-2 text-3xl font-semibold">
                {result.recommended_analyst?.analyst_name}
              </p>

              <p className="mt-2 text-slate-400">
                Suitability:{" "}
                {result.recommended_analyst?.suitability_score}%
              </p>

              <p className="mt-1 text-slate-400">
                Eligibility:{" "}
                {result.recommended_analyst?.eligibility_status}
              </p>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}