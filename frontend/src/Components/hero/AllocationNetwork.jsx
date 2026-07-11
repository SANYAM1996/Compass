import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import gsap from 'gsap';
import StatusNode from './StatusNode.jsx';

/**
 * Node coordinates are percentages of the container box, and the SVG
 * connector overlay uses a matching 0-100 viewBox — so nodes and lines
 * stay perfectly aligned at any container size with zero DOM measurement.
 */
const NODES = {
  case: { x: 10, y: 50 },
  aml: { x: 37, y: 15 },
  kyc: { x: 37, y: 39 },
  complexity: { x: 37, y: 63 },
  sla: { x: 37, y: 87 },
  match: { x: 68, y: 51 },
  allocation: { x: 91, y: 51 },
};

const EDGES = [
  ['case', 'aml'],
  ['case', 'kyc'],
  ['case', 'complexity'],
  ['case', 'sla'],
  ['aml', 'match'],
  ['kyc', 'match'],
  ['complexity', 'match'],
  ['sla', 'match'],
  ['match', 'allocation'],
];

const CANDIDATES = [
  { name: 'A. Reyes', confidence: '94%' },
  { name: 'M. Okonkwo', confidence: '91%' },
];

function edgePath(from, to) {
  const a = NODES[from];
  const b = NODES[to];
  const midX = (a.x + b.x) / 2;
  return `M ${a.x} ${a.y} C ${midX} ${a.y}, ${midX} ${b.y}, ${b.x} ${b.y}`;
}

function Connector({ from, to, delay, urgent = false }) {
  const pathRef = useRef(null);

  useEffect(() => {
    if (!urgent || !pathRef.current) return undefined;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return undefined;

    // A slow traveling dash on the SLA-risk path only — this is the one
    // connector where "still counting down" is meaningful information,
    // not ambient decoration. Starts after the draw-in reveal finishes.
    const el = pathRef.current;
    el.style.strokeDasharray = '2 3';

    const tween = gsap.fromTo(
      el,
      { strokeDashoffset: 0 },
      {
        strokeDashoffset: -20,
        duration: 3.5,
        ease: 'none',
        repeat: -1,
        delay: delay + 1.2,
      }
    );

    return () => tween.kill();
  }, [urgent, delay]);

  return (
    <motion.path
      ref={pathRef}
      d={edgePath(from, to)}
      fill="none"
      stroke="currentColor"
      strokeWidth="0.28"
      vectorEffect="non-scaling-stroke"
      className={urgent ? 'text-status-risk/50' : 'text-hairline'}
      initial={{ pathLength: 0, opacity: 0 }}
      whileInView={{ pathLength: 1, opacity: 1 }}
      viewport={{ once: true, amount: 0.4 }}
      transition={{ pathLength: { duration: 1.4, delay, ease: 'easeInOut' }, opacity: { duration: 0.3, delay } }}
    />
  );
}

function AnalystRoster() {
  const analysts = [
    { name: 'A. Reyes', load: 62 },
    { name: 'M. Okonkwo', load: 48 },
    { name: 'J. Lindqvist', load: 85 },
  ];

  return (
    <div className="space-y-2">
      {analysts.map((a) => (
        <div key={a.name} className="flex items-center gap-2">
          <span className="w-[72px] shrink-0 truncate font-mono text-[0.62rem] text-muted">
            {a.name}
          </span>
          <div className="h-[3px] flex-1 overflow-hidden rounded-full bg-white/[0.06]">
            <div
              className={`h-full rounded-full ${a.load > 75 ? 'bg-status-risk' : 'bg-azure'}`}
              style={{ width: `${a.load}%` }}
            />
          </div>
          <span className="w-7 shrink-0 text-right font-mono text-[0.6rem] text-faint">
            {a.load}%
          </span>
        </div>
      ))}
    </div>
  );
}

/**
 * Cycles the recommended analyst every few seconds — the one place the
 * brief asked for a visible "recommendation updates" behavior. Subtle
 * crossfade, several seconds apart; never a spinner, never continuous.
 */
function RecommendationValue() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setIndex((i) => (i + 1) % CANDIDATES.length);
    }, 5200);
    return () => clearInterval(id);
  }, []);

  const current = CANDIDATES[index];

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={current.name}
        initial={{ opacity: 0, y: 4 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -4 }}
        transition={{ duration: 0.4 }}
      >
        <div className="font-display text-[0.95rem] font-medium leading-tight text-ink">
          {current.name}
        </div>
        <div className="mt-0.5 font-mono text-[0.62rem] tracking-wide text-status-clear">
          {current.confidence} confidence
        </div>
      </motion.div>
    </AnimatePresence>
  );
}

export default function AllocationNetwork() {
  return (
    <div className="relative aspect-[6/5] w-full max-w-[640px]">
      <svg
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
        className="absolute inset-0 h-full w-full"
      >
        {EDGES.map(([from, to], i) => (
          <Connector
            key={`${from}-${to}`}
            from={from}
            to={to}
            delay={0.15 + i * 0.08}
            urgent={from === 'sla' || to === 'sla'}
          />
        ))}
      </svg>

      <StatusNode
        style={{ left: `${NODES.case.x}%`, top: `${NODES.case.y}%` }}
        label="Case"
        value="New Fund Case"
        sublabel="Received 09:14"
        status="neutral"
        pulse
        delay={0}
        width="w-[150px] sm:w-[170px]"
      />

      <StatusNode
        style={{ left: `${NODES.aml.x}%`, top: `${NODES.aml.y}%` }}
        label="AML"
        value="Cleared"
        sublabel="0 flags"
        status="clear"
        delay={0.35}
      />

      <StatusNode
        style={{ left: `${NODES.kyc.x}%`, top: `${NODES.kyc.y}%` }}
        label="KYC"
        value="Pending docs"
        sublabel="2 outstanding"
        status="pending"
        delay={0.45}
      />

      <StatusNode
        style={{ left: `${NODES.complexity.x}%`, top: `${NODES.complexity.y}%` }}
        label="Complexity"
        value="High"
        sublabel="Multi-jurisdiction"
        status="pending"
        delay={0.55}
      />

      <StatusNode
        style={{ left: `${NODES.sla.x}%`, top: `${NODES.sla.y}%` }}
        label="SLA risk"
        value="42%"
        sublabel="6h to breach"
        status="risk"
        pulse
        delay={0.65}
      />

      <StatusNode
        style={{ left: `${NODES.match.x}%`, top: `${NODES.match.y}%` }}
        label="Analyst match"
        status="neutral"
        delay={0.9}
        width="w-[186px] sm:w-[208px]"
      >
        <AnalystRoster />
      </StatusNode>

      <StatusNode
        style={{ left: `${NODES.allocation.x}%`, top: `${NODES.allocation.y}%` }}
        label="Recommendation"
        status="clear"
        highlighted
        pulse
        delay={1.15}
        width="w-[164px] sm:w-[182px]"
      >
        <RecommendationValue />
      </StatusNode>
    </div>
  );
}
