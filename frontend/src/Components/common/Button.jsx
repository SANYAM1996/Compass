import { forwardRef } from 'react';
import { ArrowRight } from 'lucide-react';

/**
 * Rectangular with a slight radius, not a pill — pill CTAs are the
 * default "AI startup" tell. `icon` defaults to an arrow on primary;
 * pass `icon={null}` explicitly to omit it (used for the secondary CTA).
 */
const Button = forwardRef(function Button(
  { children, onClick, icon: Icon = ArrowRight, variant = 'primary', className = '', ...props },
  ref
) {
  const base =
    'group relative inline-flex items-center gap-2.5 rounded-[6px] px-6 py-3 text-sm font-medium tracking-wide transition-colors duration-200 focus-visible:outline-offset-4';

  const variants = {
    primary: 'bg-ink text-void hover:bg-white',
    secondary: 'border border-hairline text-ink hover:border-azure/60 hover:bg-white/[0.02]',
  };

  return (
    <button
      ref={ref}
      onClick={onClick}
      className={`${base} ${variants[variant]} ${className}`}
      {...props}
    >
      <span>{children}</span>
      {Icon && (
        <Icon
          size={15}
          strokeWidth={2.25}
          className="transition-transform duration-200 group-hover:translate-x-0.5"
        />
      )}
    </button>
  );
});

export default Button;
