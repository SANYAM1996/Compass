import { memo } from 'react';

/**
 * Layered ambient gradients that sit behind the R3F canvas.
 * Pure CSS/SVG — kept off the WebGL thread for performance.
 */
function GradientBackground() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
      <div className="absolute inset-0 bg-void" />
      <div className="absolute inset-0 bg-void-radial" />

      <div
        className="absolute -top-1/4 left-1/2 h-[60vw] w-[60vw] -translate-x-1/2 rounded-full opacity-30 blur-3xl animate-drift"
        style={{
          background:
            'radial-gradient(circle, rgba(108,142,255,0.35) 0%, rgba(108,142,255,0) 65%)',
        }}
      />
      <div
        className="absolute bottom-[-20%] right-[-10%] h-[45vw] w-[45vw] rounded-full opacity-25 blur-3xl animate-drift"
        style={{
          background:
            'radial-gradient(circle, rgba(185,140,255,0.35) 0%, rgba(185,140,255,0) 65%)',
          animationDelay: '-8s',
        }}
      />

      <div
        className="absolute inset-0 opacity-[0.04]"
        style={{
          backgroundImage:
            'linear-gradient(rgba(255,255,255,0.6) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.6) 1px, transparent 1px)',
          backgroundSize: '64px 64px',
          maskImage: 'radial-gradient(ellipse at 50% 40%, black 0%, transparent 70%)',
          WebkitMaskImage: 'radial-gradient(ellipse at 50% 40%, black 0%, transparent 70%)',
        }}
      />

      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-void" />
    </div>
  );
}

export default memo(GradientBackground);
