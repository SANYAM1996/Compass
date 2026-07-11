/**
 * Structural label used across the three narrative sections. Justified
 * here (unlike decorative 01/02/03 markers) because Signal → Reasoning →
 * Decision is a real, ordered pipeline — the numbering carries information
 * about where in the process the visitor is.
 */
export default function SectionLabel({ index, total = 3, label }) {
  return (
    <div className="flex items-center gap-3 font-mono text-[0.68rem] uppercase tracking-[0.28em] text-faint">
      <span className="text-azure/80">
        {String(index).padStart(2, '0')}
      </span>
      <span className="h-px w-8 bg-hairline" />
      <span>{label}</span>
      <span className="text-faint/60">
        / {String(total).padStart(2, '0')}
      </span>
    </div>
  );
}
