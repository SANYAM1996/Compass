import { useState } from "react";
import { analyseCase } from "../services/api.js";

const initialCase = {
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

const fieldClass =
  "mt-2 w-full rounded-lg border border-white/10 bg-white/5 px-3 py-2.5 text-white outline-none transition focus:border-blue-400/60";

const labelClass = "text-sm text-slate-400";

function SelectField({
  label,
  name,
  value,
  options,
  onChange,
}) {
  return (
    <label>
      <span className={labelClass}>{label}</span>

      <select
        name={name}
        value={value}
        onChange={onChange}
        className={fieldClass}
      >
        {options.map((option) => (
          <option
            key={option}
            value={option}
            className="bg-slate-950"
          >
            {option}
          </option>
        ))}
      </select>
    </label>
  );
}

function NumberField({
  label,
  name,
  value,
  min = 0,
  max,
  onChange,
}) {
  return (
    <label>
      <span className={labelClass}>{label}</span>

      <input
        type="number"
        name={name}
        value={value}
        min={min}
        max={max}
        onChange={onChange}
        className={fieldClass}
      />
    </label>
  );
}

export default function AnalysisPage() {
  const [caseData, setCaseData] = useState(initialCase);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value, type, checked } = event.target;

    setCaseData((current) => ({
      ...current,
      [name]:
        type === "checkbox"
          ? checked
          : type === "number"
            ? Number(value)
            : value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await analyseCase(caseData);
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
    <main className="min-h-screen bg-[#05060a] px-5 py-10 text-white">
      <div className="mx-auto max-w-7xl">
        <header className="mb-10">
          <p className="text-xs uppercase tracking-[0.3em] text-blue-300">
            Intelligent Allocation Engine
          </p>

          <h1 className="mt-3 text-4xl font-semibold">
            Carne Compass Analysis
          </h1>

          <p className="mt-3 max-w-2xl text-slate-400">
            Enter the onboarding case details. The system will
            predict complexity, estimate effort, and rank the most
            suitable analysts.
          </p>
        </header>

        <div className="grid gap-8 xl:grid-cols-[1fr_1.15fr]">
          <form
            onSubmit={handleSubmit}
            className="rounded-2xl border border-white/10 bg-white/[0.03] p-6"
          >
            <h2 className="text-xl font-medium">
              Onboarding case
            </h2>

            <div className="mt-6 grid gap-5 sm:grid-cols-2">
              <label>
                <span className={labelClass}>Client name</span>

                <input
                  type="text"
                  name="client_name"
                  value={caseData.client_name}
                  onChange={handleChange}
                  className={fieldClass}
                  required
                />
              </label>

              <SelectField
                label="Client segment"
                name="client_segment"
                value={caseData.client_segment}
                onChange={handleChange}
                options={[
                  "High Profile",
                  "Institutional",
                  "Small / Emerging",
                ]}
              />

              <SelectField
                label="Fund type"
                name="fund_type"
                value={caseData.fund_type}
                onChange={handleChange}
                options={[
                  "UCITS",
                  "AIF",
                  "Hedge Fund",
                  "Private Equity",
                  "Real Estate",
                  "Money Market",
                ]}
              />

              <SelectField
                label="Domicile"
                name="domicile"
                value={caseData.domicile}
                onChange={handleChange}
                options={[
                  "Ireland",
                  "Luxembourg",
                  "UK",
                  "Cayman Islands",
                  "Malta",
                ]}
              />

              <SelectField
                label="AML status"
                name="aml_status"
                value={caseData.aml_status}
                onChange={handleChange}
                options={[
                  "Completed",
                  "In Progress",
                  "Pending",
                  "Blocked",
                ]}
              />

              <SelectField
                label="KYC status"
                name="kyc_status"
                value={caseData.kyc_status}
                onChange={handleChange}
                options={[
                  "Completed",
                  "In Progress",
                  "Pending",
                  "Failed",
                ]}
              />

              <SelectField
                label="Risk rating"
                name="risk_rating"
                value={caseData.risk_rating}
                onChange={handleChange}
                options={[
                  "Low",
                  "Medium",
                  "High",
                ]}
              />

              <SelectField
                label="Client priority"
                name="client_priority"
                value={caseData.client_priority}
                onChange={handleChange}
                options={[
                  "Low",
                  "Normal",
                  "High",
                  "Critical",
                ]}
              />

              <SelectField
                label="Latest blocker"
                name="latest_blocker_type"
                value={caseData.latest_blocker_type}
                onChange={handleChange}
                options={[
                  "None",
                  "AML Delay",
                  "KYC Issue",
                  "Missing Documents",
                  "Regulatory Review",
                  "Analyst Unavailable",
                  "Client Dependency",
                ]}
              />

              <NumberField
                label="SLA days"
                name="sla_days"
                value={caseData.sla_days}
                min={1}
                max={365}
                onChange={handleChange}
              />

              <NumberField
                label="Sub-funds"
                name="num_sub_funds"
                value={caseData.num_sub_funds}
                min={1}
                max={100}
                onChange={handleChange}
              />

              <NumberField
                label="Share classes"
                name="num_share_classes"
                value={caseData.num_share_classes}
                min={1}
                max={200}
                onChange={handleChange}
              />

              <NumberField
                label="Jurisdictions"
                name="num_jurisdictions"
                value={caseData.num_jurisdictions}
                min={1}
                max={20}
                onChange={handleChange}
              />

              <NumberField
                label="Delegates"
                name="num_delegates"
                value={caseData.num_delegates}
                min={0}
                max={50}
                onChange={handleChange}
              />

              <NumberField
                label="Missing documents"
                name="missing_documents"
                value={caseData.missing_documents}
                min={0}
                max={100}
                onChange={handleChange}
              />

              <NumberField
                label="Blocker count"
                name="blocker_count"
                value={caseData.blocker_count}
                min={0}
                max={20}
                onChange={handleChange}
              />

              <label className="flex items-center gap-3 rounded-lg border border-white/10 bg-white/5 px-4 py-3">
                <input
                  type="checkbox"
                  name="strategic_client"
                  checked={caseData.strategic_client}
                  onChange={handleChange}
                  className="h-4 w-4"
                />

                <span className="text-sm text-slate-300">
                  Strategic client
                </span>
              </label>

              <label className="flex items-center gap-3 rounded-lg border border-white/10 bg-white/5 px-4 py-3">
                <input
                  type="checkbox"
                  checked={
                    caseData.regulatory_review_required === 1
                  }
                  onChange={(event) =>
                    setCaseData((current) => ({
                      ...current,
                      regulatory_review_required:
                        event.target.checked ? 1 : 0,
                    }))
                  }
                  className="h-4 w-4"
                />

                <span className="text-sm text-slate-300">
                  Regulatory review required
                </span>
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-7 w-full rounded-lg bg-blue-500 px-6 py-3 font-medium transition hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading
                ? "Analysing case..."
                : "Analyse and Recommend"}
            </button>

            {error && (
              <div className="mt-5 rounded-lg border border-red-500/30 bg-red-500/10 p-4 text-red-300">
                {error}
              </div>
            )}
          </form>

          <section>
            {!result && !loading && (
              <div className="flex min-h-[420px] items-center justify-center rounded-2xl border border-dashed border-white/10 bg-white/[0.02] p-10 text-center">
                <div>
                  <p className="text-lg text-slate-300">
                    No analysis yet
                  </p>

                  <p className="mt-2 text-sm text-slate-500">
                    Complete the case details and run the analysis.
                  </p>
                </div>
              </div>
            )}

            {loading && (
              <div className="flex min-h-[420px] items-center justify-center rounded-2xl border border-white/10 bg-white/[0.03]">
                <div className="text-center">
                  <div className="mx-auto h-10 w-10 animate-spin rounded-full border-2 border-white/20 border-t-blue-400" />

                  <p className="mt-5 text-slate-300">
                    Evaluating complexity, effort and analyst fit...
                  </p>
                </div>
              </div>
            )}

            {result && (
              <ResultsPanel result={result} />
            )}
          </section>
        </div>
      </div>
    </main>
  );
}

function ResultsPanel({ result }) {
  const recommendation = result.recommended_analyst;

  return (
    <div className="space-y-5">
      <div className="grid gap-4 sm:grid-cols-3">
        <MetricCard
          label="Complexity"
          value={result.predicted_complexity}
          detail={`${result.prediction_confidence}% confidence`}
        />

        <MetricCard
          label="Estimated effort"
          value={
            result.estimated_effort.estimated_effort_hours
          }
          detail="person-hours"
        />

        <MetricCard
          label="Effort band"
          value={result.estimated_effort.effort_band}
          detail={`${result.estimated_effort.estimated_effort_days} analyst-days`}
        />
      </div>

      <div className="rounded-2xl border border-blue-400/20 bg-blue-400/[0.06] p-6">
        <p className="text-xs uppercase tracking-[0.2em] text-blue-300">
          Recommended analyst
        </p>

        <div className="mt-4 flex flex-wrap items-start justify-between gap-4">
          <div>
            <h2 className="text-3xl font-semibold">
              {recommendation?.analyst_name}
            </h2>

            <p className="mt-2 text-slate-400">
              {recommendation?.seniority} ·{" "}
              {recommendation?.team}
            </p>
          </div>

          <div className="text-right">
            <p className="text-4xl font-semibold">
              {recommendation?.suitability_score}%
            </p>

            <p className="text-xs uppercase tracking-wider text-slate-500">
              suitability
            </p>
          </div>
        </div>

        <div className="mt-5 flex flex-wrap gap-2">
          {recommendation?.matched_skills
            ?.split(",")
            .filter(Boolean)
            .map((skill) => (
              <span
                key={skill}
                className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-slate-300"
              >
                {skill.trim()}
              </span>
            ))}
        </div>

        <div className="mt-5 grid gap-3 sm:grid-cols-3">
          <SmallMetric
            label="Workload"
            value={`${recommendation?.current_workload_pct}%`}
          />

          <SmallMetric
            label="Eligibility"
            value={recommendation?.eligibility_status}
          />

          <SmallMetric
            label="Quality"
            value={`${recommendation?.quality_score}/10`}
          />
        </div>

        <div className="mt-6">
          <p className="text-sm font-medium">
            Why this analyst?
          </p>

          <ul className="mt-3 space-y-2 text-sm text-slate-400">
            {recommendation?.reasons?.map((reason) => (
              <li key={reason}>• {reason}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-6">
        <h3 className="text-lg font-medium">
          Ranked alternatives
        </h3>

        <div className="mt-4 space-y-3">
          {result.top_recommendations.map(
            (analyst, index) => (
              <div
                key={analyst.analyst_id}
                className="grid gap-3 rounded-xl border border-white/10 bg-white/[0.02] p-4 sm:grid-cols-[40px_1fr_auto]"
              >
                <div className="text-slate-500">
                  #{index + 1}
                </div>

                <div>
                  <p className="font-medium">
                    {analyst.analyst_name}
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    {analyst.seniority} · {analyst.team}
                  </p>

                  {analyst.missing_mandatory_skills && (
                    <p className="mt-2 text-xs text-amber-300">
                      Missing:{" "}
                      {analyst.missing_mandatory_skills}
                    </p>
                  )}
                </div>

                <div className="text-right">
                  <p className="text-xl font-semibold">
                    {analyst.suitability_score}%
                  </p>

                  <p className="text-xs text-slate-500">
                    {analyst.eligibility_status}
                  </p>
                </div>
              </div>
            ),
          )}
        </div>
      </div>
    </div>
  );
}

function MetricCard({ label, value, detail }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/[0.03] p-5">
      <p className="text-sm text-slate-400">
        {label}
      </p>

      <p className="mt-2 text-2xl font-semibold">
        {value}
      </p>

      <p className="mt-1 text-sm text-slate-500">
        {detail}
      </p>
    </div>
  );
}

function SmallMetric({ label, value }) {
  return (
    <div className="rounded-lg border border-white/10 bg-black/20 p-3">
      <p className="text-xs text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-sm font-medium">
        {value}
      </p>
    </div>
  );
}