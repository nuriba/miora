import { ContactShadows } from '@react-three/drei';
import { Avatar } from '../../api/types';

interface Props {
  avatar: Avatar | null;
  selectedGarments?: any[];
}

const Avatar3D: React.FC<Props> = ({ avatar, selectedGarments = [] }) => {
  if (!avatar) return null;

  const GarmentOverlay = ({ garment, position }: { garment: any; position: [number, number, number] }) => (
    <mesh position={position}>
      <boxGeometry args={[1.1, 0.8, 0.1]} />
      <meshStandardMaterial
        color={garment.color || '#ec4899'}
        transparent
        opacity={0.8}
      />
    </mesh>
  );

  return (
    <group>
      {/* Basic avatar representation */}
      <mesh position={[0, 0, 0]}>
        <capsuleGeometry args={[0.5, 1.5, 4, 8]} />
        <meshStandardMaterial color="#9333ea" />
      </mesh>

      {/* Head */}
      <mesh position={[0, 1.2, 0]}>
        <sphereGeometry args={[0.3, 16, 16]} />
        <meshStandardMaterial color="#f3e8ff" />
      </mesh>

      {/* Arms */}
      <mesh position={[-0.7, 0.5, 0]}>
        <capsuleGeometry args={[0.15, 0.8, 4, 8]} />
        <meshStandardMaterial color="#9333ea" />
      </mesh>
      <mesh position={[0.7, 0.5, 0]}>
        <capsuleGeometry args={[0.15, 0.8, 4, 8]} />
        <meshStandardMaterial color="#9333ea" />
      </mesh>

      {/* Legs */}
      <mesh position={[-0.25, -1.2, 0]}>
        <capsuleGeometry args={[0.2, 1.0, 4, 8]} />
        <meshStandardMaterial color="#7c3aed" />
      </mesh>
      <mesh position={[0.25, -1.2, 0]}>
        <capsuleGeometry args={[0.2, 1.0, 4, 8]} />
        <meshStandardMaterial color="#7c3aed" />
      </mesh>

      {/* Render selected garments */}
      {selectedGarments.map((garment, index) => (
        <GarmentOverlay
          key={garment.id || index}
          garment={garment}
          position={[0, 0.2 - index * 0.1, 0.1]}
        />
      ))}

      {/* Shadow */}
      <ContactShadows position={[0, -2, 0]} opacity={0.4} scale={3} blur={2} />
    </group>
  );
};

export default Avatar3D; 