import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Float, MeshDistortMaterial, Sparkles } from '@react-three/drei';

/**
 * The Floating AI Core.
 *
 * A distorted glass icosahedron with an emissive inner light, orbited by
 * a thin tilted ring and a close sparkle halo. Reads as "a system arriving
 * at a decision" rather than a decorative 3D toy — kept singular and slow.
 */
function CoreRing({ radius = 2.05, tilt = 1.1, speed = 0.15, color = '#6C8EFF' }) {
  const ringRef = useRef(null);

  useFrame((_, delta) => {
    if (!ringRef.current) return;
    ringRef.current.rotation.z += delta * speed;
  });

  return (
    <group rotation={[tilt, 0, 0]}>
      <mesh ref={ringRef}>
        <torusGeometry args={[radius, 0.006, 16, 128]} />
        <meshBasicMaterial color={color} transparent opacity={0.45} />
      </mesh>
    </group>
  );
}

function InnerLight() {
  const lightRef = useRef(null);

  useFrame(({ clock }) => {
    if (!lightRef.current) return;
    const t = clock.getElapsedTime();
    lightRef.current.intensity = 3.2 + Math.sin(t * 1.4) * 0.9;
  });

  return <pointLight ref={lightRef} color="#B98CFF" intensity={3.2} distance={6} decay={2} />;
}

export default function AICore() {
  const coreRef = useRef(null);

  useFrame((_, delta) => {
    if (!coreRef.current) return;
    coreRef.current.rotation.y += delta * 0.12;
    coreRef.current.rotation.x += delta * 0.03;
  });

  return (
    <group>
      <ambientLight intensity={0.25} />
      <directionalLight position={[4, 5, 3]} intensity={0.6} color="#F5F6FA" />

      <Float speed={1.4} rotationIntensity={0.3} floatIntensity={0.9}>
        <group>
          <InnerLight />

          <mesh ref={coreRef}>
            <icosahedronGeometry args={[1.35, 4]} />
            <MeshDistortMaterial
              color="#0B0D14"
              emissive="#3548A8"
              emissiveIntensity={0.35}
              roughness={0.15}
              metalness={0.4}
              distort={0.32}
              speed={1.1}
              transparent
              opacity={0.94}
            />
          </mesh>

          <mesh>
            <icosahedronGeometry args={[1.36, 4]} />
            <meshBasicMaterial
              color="#8FA4FF"
              wireframe
              transparent
              opacity={0.08}
            />
          </mesh>

          <CoreRing radius={2.05} tilt={1.05} speed={0.12} color="#6C8EFF" />
          <CoreRing radius={2.35} tilt={-0.6} speed={-0.08} color="#B98CFF" />

          <Sparkles
            count={40}
            scale={4.2}
            size={2}
            speed={0.25}
            opacity={0.5}
            color="#C7D2FF"
          />
        </group>
      </Float>
    </group>
  );
}
