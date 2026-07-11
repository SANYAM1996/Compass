import StatusNode from './StatusNode.jsx';
import RecommendationCard from './RecommendationCard.jsx';

/**
 * A single vertical pipeline, not a branching diagram — matches the
 * real sequence a fund onboarding case moves through. Each row is a
 * StatusNode; the final step is a RecommendationCard, which is the one
 * point allowed to break the row pattern, since it's the answer the
 * flow was building toward.
 */
const STEPS = [
  { label: 'New Fund Case', value: 'Case #FC-2291', status: 'neutral' },
  { label: 'AML Check', value: 'Pending', status: 'pending' },
  { label: 'KYC Check', value: 'Completed', status: 'complete' },
  { label: 'Complexity Score', value: 'High', status: 'pending' },
  { label: 'SLA Risk', value: '10 days remaining', status: 'risk' },
  { label: 'Analyst Matching', value: 'Workload 64%', status: 'active', active: true },
];

export default function AllocationFlow() {
  return (
    <div className="w-full max-w-[420px]">
      {STEPS.map((step, i) => (
        <StatusNode
          key={step.label}
          label={step.label}
          value={step.value}
          status={step.status}
          active={Boolean(step.active)}
          delay={0.1 + i * 0.08}
          isFirst={i === 0}
          isLast={false}
        />
      ))}

      <RecommendationCard delay={0.1 + STEPS.length * 0.08} />
    </div>
  );
}
