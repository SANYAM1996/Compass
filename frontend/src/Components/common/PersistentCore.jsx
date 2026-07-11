import { forwardRef, Suspense, memo } from 'react';
import { Canvas } from '@react-three/fiber';
import AICore from '../hero/AICore.jsx';
import Particles from '../hero/Particles.jsx';

/**
 * The AI Core is mounted exactly once for the whole page. It never
 * remounts between sections — instead, GSAP tweens this wrapper's CSS
 * transform (translate/scale) as the visitor scrolls, so the same object
 * drifts, recedes, and returns. That continuity is what sells "the system
 * is still reasoning" rather than "a new component loaded."
 *
 * Positioned via CSS transform only (never layout properties) to stay
 * on the compositor thread — no layout thrash during scroll.
 */
const PersistentCore = forwardRef(function PersistentCore(_, ref) {
  return (
    <div
      ref={ref}
      className="pointer-events-none fixed inset-0 z-10 will-change-transform"
      aria-hidden="true"
    >
      <Canvas
        camera={{ position: [0, 0, 7.2], fov: 40 }}
        dpr={[1, 1.75]}
        gl={{ antialias: true, alpha: true }}
      >
        <Suspense fallback={null}>
          <AICore />
          <Particles count={620} radius={7} />
        </Suspense>
      </Canvas>
    </div>
  );
});

export default memo(PersistentCore);
