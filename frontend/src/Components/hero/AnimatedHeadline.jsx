import { motion } from 'framer-motion';

const container = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.09,
      delayChildren: 0.15,
    },
  },
};

const word = {
  hidden: { y: '110%', opacity: 0 },
  visible: {
    y: '0%',
    opacity: 1,
    transition: { duration: 0.9, ease: [0.16, 1, 0.3, 1] },
  },
};

/**
 * Splits a line into words and reveals each with a clipped rise —
 * avoids the generic "fade + blur" headline entrance.
 */
function AnimatedLine({ text, className = '' }) {
  const words = text.split(' ');

  return (
    <span className={`block overflow-hidden ${className}`}>
      <motion.span variants={container} initial="hidden" animate="visible" className="inline-block">
        {words.map((w, i) => (
          <span key={`${w}-${i}`} className="inline-block overflow-hidden pr-[0.28em] align-top">
            <motion.span variants={word} className="inline-block">
              {w}
            </motion.span>
          </span>
        ))}
      </motion.span>
    </span>
  );
}

export default function AnimatedHeadline() {
  return (
    <h1 className="font-display font-medium leading-[0.98] tracking-tight text-5xl sm:text-6xl md:text-7xl lg:text-[5.5rem]">
      <AnimatedLine text="Carne Compass" className="text-ink" />
      <AnimatedLine text="Intelligent Allocation Engine" className="text-gradient" />
    </h1>
  );
}
