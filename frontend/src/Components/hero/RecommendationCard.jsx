import { useEffect, useState } from 'react';
import { motion, useMotionValue, animate } from 'framer-motion';

const SKILLS = ['AML', 'UCITS', 'Regulatory'];

/**
 * The single point the whole flow builds toward. Deliberately breaks
 * the row pattern used by StatusNode: it's a bordered card, not a line
 * item, with a violet-tinted border — the only place violet appears
 * on the page. The suitability score counts up once on mount rather
 * than appearing as a static number, so it reads as computed, not typed.
 */
export default function RecommendationCard({ delay = 0 }) {
  const [displayScore, setDisplayScore] = useState(0);
  const score = useMotionValue(0);

  useEffect(() => {
    const controls = animate(score, 82, {
      duration: 1.1,
      delay: delay + 0.3,
      ease: [0.16, 1, 0.3, 1],
      onUpdate: (v) => setDisplayScore(Math.round(v)),
    });
    return () => controls.stop();
  }, [score, delay]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.8 }}
      transition={{ duration: 0.5, delay, ease: [0.16, 1, 0.3, 1] }}
      className="ml-8 mt-4 rounded-[6px] border border-violet/40 bg-violet/[0.05] px-5 py-4"
    >
      <div className="flex items-center justify-between gap-2">
        <span className="font-mono text-[0.68rem] uppercase tracking-[0.14em] text-violet">
          Recommended Allocation
        </span>
        <span className="h-1.5 w-1.5 rounded-full bg-status-clear" />
      </div>

      <div className="mt-3 flex items-end justify-between gap-4">
        <div>
          <div className="font-display text-xl font-medium leading-tight text-ink">
            Brian O&rsquo;Sullivan
          </div>
          <div className="mt-2 flex flex-wrap gap-1.5">
            {SKILLS.map((skill) => (
              <span
                key={skill}
                className="rounded-[3px] border border-hairline px-1.5 py-0.5 font-mono text-[0.6rem] uppercase tracking-wide text-muted"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>

        <div className="text-right">
          <div className="font-display text-2xl font-medium leading-none text-ink tabular-nums">
            {displayScore}%
          </div>
          <div className="mt-1 font-mono text-[0.62rem] uppercase tracking-[0.14em] text-muted">
            Suitability
          </div>
        </div>
      </div>
    </motion.div>
  );
}
