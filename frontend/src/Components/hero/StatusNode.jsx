import { motion } from 'framer-motion';

const DOT_COLOR = {
  neutral: 'bg-faint border-faint',
  active: 'bg-azure border-azure',
  complete: 'bg-status-clear border-status-clear',
  pending: 'bg-status-pending border-status-pending',
  risk: 'bg-status-risk border-status-risk',
};

/**
 * One row in the decision-flow timeline (AllocationFlow). Renders a
 * hairline rail segment above/below a status dot, plus a label/value
 * pair on a single line — closer to a terminal log than a diagram.
 *
 * The rail is split into a top half and a bottom half so each segment
 * can draw in independently as the row scrolls into view, staggered
 * by `delay`. `isFirst`/`isLast` trim the rail at the ends of the flow.
 */
export default function StatusNode({
  label,
  value,
  status = 'neutral',
  active = false,
  delay = 0,
  isFirst = false,
  isLast = false,
}) {
  return (
    <div className="flex items-stretch gap-4">
      <div className="relative flex w-4 shrink-0 justify-center">
        {!isFirst && (
          <motion.span
            className="absolute top-0 h-1/2 w-px bg-hairline"
            style={{ transformOrigin: 'top' }}
            initial={{ scaleY: 0 }}
            whileInView={{ scaleY: 1 }}
            viewport={{ once: true, amount: 0.9 }}
            transition={{ duration: 0.35, delay, ease: 'easeOut' }}
          />
        )}
        {!isLast && (
          <motion.span
            className="absolute bottom-0 h-1/2 w-px bg-hairline"
            style={{ transformOrigin: 'top' }}
            initial={{ scaleY: 0 }}
            whileInView={{ scaleY: 1 }}
            viewport={{ once: true, amount: 0.9 }}
            transition={{ duration: 0.35, delay: delay + 0.08, ease: 'easeOut' }}
          />
        )}

        <span
          className={`absolute top-1/2 h-2.5 w-2.5 -translate-y-1/2 rounded-full border ${DOT_COLOR[status]}`}
        >
          {active && (
            <motion.span
              className={`absolute inset-0 rounded-full ${DOT_COLOR[status]}`}
              initial={{ scale: 1, opacity: 0.6 }}
              animate={{ scale: [1, 2.1, 1], opacity: [0.5, 0, 0.5] }}
              transition={{ duration: 1.3, repeat: 2, ease: 'easeOut', delay: delay + 0.4 }}
            />
          )}
        </span>
      </div>

      <div className="flex flex-1 items-baseline justify-between gap-4 border-b border-hairline/40 py-3.5">
        <span className="font-mono text-[0.68rem] uppercase tracking-[0.14em] text-muted">
          {label}
        </span>
        <span className="text-right font-mono text-[0.82rem] text-ink">{value}</span>
      </div>
    </div>
  );
}
