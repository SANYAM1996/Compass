import HeroSection from '../components/hero/HeroSection.jsx';

/**
 * Landing page. Background is two Tailwind utility classes (bg-grid,
 * bg-vignette — defined in styles/index.css) rather than a dedicated
 * component; a single faint grid plus a vignette doesn't warrant its
 * own file, and keeps the import graph honest.
 */
export default function HomePage() {
  return (
    <main className="relative min-h-screen w-full bg-void">
      <div className="bg-grid pointer-events-none fixed inset-0 z-0 opacity-[0.04]" aria-hidden="true" />
      <div className="bg-vignette pointer-events-none fixed inset-0 z-0" aria-hidden="true" />
      <HeroSection />
    </main>
  );
}
