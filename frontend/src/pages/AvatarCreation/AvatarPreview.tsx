import { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import { useAvatar } from '../../hooks/useAvatar';
import LoadingSpinner from '../../components/common/LoadingSpinner';

interface Props {
  avatarId: string | null;
}

const AvatarPreview: React.FC<Props> = ({ avatarId }) => {
  const { data: avatar, isLoading } = useAvatar(avatarId || '');
  
  if (!avatarId) {
    return (
      <div className="card h-full flex items-center justify-center">
        <div className="text-center text-gray-500">
          <div className="w-32 h-32 bg-gray-200 rounded-full mx-auto mb-4" />
          <p>Select an avatar to preview</p>
        </div>
      </div>
    );
  }
  
  if (isLoading) {
    return (
      <div className="card h-full flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }
  
  return (
    <div className="card h-full">
      <h3 className="text-lg font-semibold mb-4">Avatar Preview</h3>
      
      <div className="aspect-[3/4] bg-gradient-to-br from-purple-100 to-pink-100 rounded-lg mb-4">
        <Canvas>
          <OrbitControls enablePan={false} />
          <ambientLight intensity={0.5} />
          <directionalLight position={[10, 10, 5]} intensity={1} />
          <Suspense fallback={null}>
            {/* Avatar 3D model would go here */}
            <mesh>
              <capsuleGeometry args={[0.5, 1.5, 4, 8]} />
              <meshStandardMaterial color="#9333ea" />
            </mesh>
          </Suspense>
          <Environment preset="city" />
        </Canvas>
      </div>
      
      {avatar && (
        <div className="space-y-3">
          <h4 className="font-medium">Measurements</h4>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span className="text-gray-500">Height:</span>
              <p className="font-medium">{avatar.height} cm</p>
            </div>
            <div>
              <span className="text-gray-500">Weight:</span>
              <p className="font-medium">{avatar.weight || 'N/A'} kg</p>
            </div>
            <div>
              <span className="text-gray-500">Chest:</span>
              <p className="font-medium">{avatar.chest} cm</p>
            </div>
            <div>
              <span className="text-gray-500">Waist:</span>
              <p className="font-medium">{avatar.waist} cm</p>
            </div>
            <div>
              <span className="text-gray-500">Hips:</span>
              <p className="font-medium">{avatar.hips} cm</p>
            </div>
            <div>
              <span className="text-gray-500">Body Type:</span>
              <p className="font-medium capitalize">{avatar.body_type}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AvatarPreview;