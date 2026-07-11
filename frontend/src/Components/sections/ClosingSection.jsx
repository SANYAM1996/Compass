import { forwardRef } from 'react';
import { motion } from 'framer-motion';
import SectionLabel from '../common/SectionLabel.jsx';
import Button from '../common/Button.jsx';

const fadeUp = {
  hidden: { opacity: 0, y: 16 },
  visible: (delay = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.8, delay, ease: [0.16, 1, 0.3, 1] },
  }),
};

/**
 * Third beat of the story: the Core has receded to a quiet presence
 * behind the left negative space, content lands right-weighted this
 * time to keep the page's rhythm from feeling like a template repeat
 * of the hero.
 */
const ClosingSection = forwardRef(function ClosingSection(_, ref) {
  const handleBeginAnalysis = () => {
    document.dispatchEvent(new CustomEvent('carne:begin-analysis'));
  };

  return (
    <section
      ref={ref}
      data-section="decision"
      className="relative flex min-h-screen w-full flex-col justify-between bg-transparent"
    >
      <div className="reading-plane-right absolute inset-y-0 right-0 w-full sm:w-3/5" />

      <div className="relative z-20 flex flex-1 items-center justify-end px-6 sm:px-12 lg:px-20">
        <div className="w-full text-right sm:w-3/5 lg:w-1/2">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.6 }}
            custom={0}
            variants={fadeUp}
            className="flex justify-end"
          >
            <SectionLabel index={3} label="Decision" />
          </motion.div>

          <motion.h2
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.6 }}
            custom={0.15}
            variants={fadeUp}
            className="mt-7 ml-auto max-w-xl font-display text-4xl font-medium leading-[1.05] text-ink sm:text-5xl lg:text-6xl"
          >
            Operational intelligence, ready when the fund is.
          </motion.h2>

          <motion.p
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.6 }}
            custom={0.3}
            variants={fadeUp}
            className="mt-6 ml-auto max-w-md text-base leading-relaxed text-muted"
          >
            Carne Compass sits on your existing onboarding pipeline — no migration, no
            re-platforming. It starts reasoning the moment documents arrive.
          </motion.p>

          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.6 }}
            custom={0.45}
            variants={fadeUp}
            className="mt-10 flex justify-end"
          >
            <Button onClick={handleBeginAnalysis}>Begin Analysis</Button>
          </motion.div>
        </div>
      </div>

      <footer className="relative z-20 flex flex-col gap-4 border-t border-hairline px-6 py-8 font-mono text-[0.65rem] uppercase tracking-[0.2em] text-faint sm:flex-row sm:items-center sm:justify-between sm:px-12 lg:px-20">
        <span>Carne Compass — Intelligent Allocation Engine</span>
        <span className="flex items-center gap-2">
          <span className="h-1.5 w-1.5 rounded-full bg-azure" />
          System Operational
        </span>
      </footer>
    </section>
  );
});

export default ClosingSection;
