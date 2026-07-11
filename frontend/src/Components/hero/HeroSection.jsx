import { forwardRef } from 'react';
import { motion } from 'framer-motion';
import AllocationFlow from './AllocationFlow.jsx';
import Button from '../common/Button.jsx';

const fadeUp = {
  hidden: { opacity: 0, y: 14 },
  visible: (delay = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, delay, ease: [0.16, 1, 0.3, 1] },
  }),
};

/**
 * Asymmetric two-column hero, ~45/55 left/right on desktop, stacking
 * to one column on mobile (copy first, flow visual second). Everything
 * — including both CTAs — fits inside 100vh; no scroll indicator,
 * because the brief requires the CTA visible without scrolling.
 */
const HeroSection = forwardRef(function HeroSection(_, ref) {
  const handleBeginAnalysis = () => {
    document.dispatchEvent(new CustomEvent('carne:begin-analysis'));
  };

  const handleViewFlow = () => {
    document.getElementById('decision-flow')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  return (
    <section
      ref={ref}
      data-section="hero"
      className="relative flex min-h-screen w-full items-center bg-transparent py-16 lg:py-0"
    >
      <div className="relative z-20 grid w-full grid-cols-1 items-center gap-14 px-6 sm:px-12 lg:grid-cols-12 lg:gap-8 lg:px-20">
        <div className="lg:col-span-5">
          <motion.div initial="hidden" animate="visible" custom={0} variants={fadeUp}>
            <span className="font-mono text-[0.68rem] uppercase tracking-[0.22em] text-faint">
              Fund Onboarding · Operations
            </span>
          </motion.div>

          <motion.h1
            initial="hidden"
            animate="visible"
            custom={0.08}
            variants={fadeUp}
            className="mt-5 font-display text-[2.5rem] font-medium leading-[1.05] tracking-tight text-ink sm:text-[2.9rem] lg:text-[3.1rem]"
          >
            Carne
            <br />
            Compass
          </motion.h1>

          <motion.p
            initial="hidden"
            animate="visible"
            custom={0.18}
            variants={fadeUp}
            className="mt-3 font-mono text-[0.72rem] uppercase tracking-[0.26em] text-azure"
          >
            Intelligent Allocation Engine
          </motion.p>

          <motion.p
            initial="hidden"
            animate="visible"
            custom={0.3}
            variants={fadeUp}
            className="mt-7 max-w-md text-balance text-[1.15rem] font-medium leading-snug text-ink/90"
          >
            Turn complex fund onboarding decisions into explainable analyst allocations in
            seconds.
          </motion.p>

          <motion.p
            initial="hidden"
            animate="visible"
            custom={0.4}
            variants={fadeUp}
            className="mt-4 max-w-md text-[0.92rem] leading-relaxed text-muted"
          >
            Predict complexity, estimate effort, identify SLA risk, and recommend the right
            analyst using live workload, skills, availability, and blocker data.
          </motion.p>

          <motion.div
            initial="hidden"
            animate="visible"
            custom={0.52}
            variants={fadeUp}
            className="mt-9 flex flex-wrap items-center gap-3"
          >
            <Button onClick={handleBeginAnalysis}>Begin Analysis</Button>
            <Button onClick={handleViewFlow} variant="secondary" icon={null}>
              View Decision Flow
            </Button>
          </motion.div>
        </div>

        <div id="decision-flow" className="flex justify-center lg:col-span-7 lg:justify-end">
          <AllocationFlow />
        </div>
      </div>
    </section>
  );
});

export default HeroSection;
