import { forwardRef } from 'react';
import { motion } from 'framer-motion';

/**
 * Forwarded ref so the parent (HeroSection) can hand this element to a
 * GSAP ScrollTrigger tween without prop-drilling animation logic here.
 */
const ScrollIndicator = forwardRef(function ScrollIndicator(_, ref) {
  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 1.6, duration: 0.8 }}
      className="absolute bottom-10 left-1/2 flex -translate-x-1/2 flex-col items-center gap-3"
    >
      <span className="font-mono text-[0.65rem] uppercase tracking-[0.3em] text-muted">
        Scroll
      </span>
      <div className="flex h-8 w-5 justify-center rounded-full border border-hairline p-1">
        <span className="h-1.5 w-1.5 rounded-full bg-azure animate-scroll-dot" />
      </div>
    </motion.div>
  );
});

export default ScrollIndicator;
