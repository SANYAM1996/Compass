import { useMemo, useRef } from "react";
import { useFrame } from "@react-three/fiber";

function generateSpherePositions(count, radius) {
  const positions = new Float32Array(count * 3);

  for (let index = 0; index < count; index += 1) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    const distance = radius * (0.65 + Math.random() * 0.35);

    positions[index * 3] =
      distance * Math.sin(phi) * Math.cos(theta);

    positions[index * 3 + 1] =
      distance * Math.sin(phi) * Math.sin(theta);

    positions[index * 3 + 2] =
      distance * Math.cos(phi);
  }

  return positions;
}

export default function Particles({
  count = 600,
  radius = 4.5,
}) {
  const pointsRef = useRef();

  const positions = useMemo(
    () => generateSpherePositions(count, radius),
    [count, radius],
  );

  useFrame((_, delta) => {
    if (!pointsRef.current) {
      return;
    }

    pointsRef.current.rotation.y += delta * 0.015;
    pointsRef.current.rotation.x += delta * 0.005;
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          array={positions}
          count={positions.length / 3}
          itemSize={3}
        />
      </bufferGeometry>

      <pointsMaterial
        size={0.025}
        color="#8FA4FF"
        transparent
        opacity={0.65}
        depthWrite={false}
      />
    </points>
  );
}