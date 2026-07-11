import { forwardRef } from 'react';
import SectionLabel from '../common/SectionLabel.jsx';

const STEPS = [
  {
    label: 'Ingest',
    heading: 'Every mandate, reconciled on arrival.',
    body: 'Fund documents, mandates, and historical allocations are parsed and cross-checked the moment they land — no manual staging queue.',
  },
  {
    label: 'Reason',
    heading: 'Constraints weighed, not just checked.',
    body: 'Exposure limits, precedent, and jurisdictional rules are evaluated together, so a decision accounts for what actually matters together, not one rule at a time.',
  },
  {
    label: 'Decide',
    heading: 'A ranked allocation, with its reasoning attached.',
    body: 'The output is never a black box — every recommendation carries the trail of constraints and precedent that produced it.',
  },
];

/**
 * Pinned for three scroll-lengths. Step visibility and the persistent
 * Core's on-screen position are both driven by the same GSAP timeline
 * in HomePage — this component only renders the DOM the timeline reads.
 * Panels alternate sides across steps so the eye keeps re-orienting,
 * the way a real reasoning process shifts focus rather than sitting still.
 */
const ReasoningSection = forwardRef(function ReasoningSection({ panelRefs, indexRef }, ref) {
  return (
    <section
      ref={ref}
      data-section="reasoning"
      className="relative h-screen w-full overflow-hidden bg-transparent"
    >
      <div className="absolute left-6 top-10 z-20 sm:left-12 lg:left-20">
        <SectionLabel index={2} label="Reasoning" />
      </div>

      <div
        ref={indexRef}
        className="absolute right-6 top-10 z-20 font-mono text-[0.68rem] uppercase tracking-[0.28em] text-faint sm:right-12 lg:right-20"
      >
        Step 01 / 03
      </div>

      {STEPS.map((step, i) => {
        const alignRight = i % 2 === 1;
        return (
          <div
            key={step.label}
            ref={(el) => (panelRefs.current[i] = el)}
            className={`absolute inset-0 z-20 flex items-center opacity-0 ${
              alignRight ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`reading-plane relative w-full px-6 py-16 sm:w-3/5 sm:px-12 lg:px-20 ${
                alignRight ? 'reading-plane-right text-right' : 'text-left'
              }`}
            >
              <div className={`max-w-lg ${alignRight ? 'ml-auto' : ''}`}>
                <span className="font-mono text-xs uppercase tracking-[0.3em] text-azure/90">
                  {String(i + 1).padStart(2, '0')} — {step.label}
                </span>
                <h3 className="mt-5 font-display text-3xl font-medium leading-tight text-ink sm:text-4xl lg:text-5xl">
                  {step.heading}
                </h3>
                <p className={`mt-5 max-w-md text-base leading-relaxed text-muted ${alignRight ? 'ml-auto' : ''}`}>
                  {step.body}
                </p>
              </div>
            </div>
          </div>
        );
      })}
    </section>
  );
});

export default ReasoningSection;
