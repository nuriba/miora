import { Suspense, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, PerspectiveCamera } from '@react-three/drei';
import { RotateCcw, Camera, Maximize2, Download } from 'lucide-react';
import Avatar3D from './Avatar3D';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { useAvatarStore } from '../../store/avatarStore';
import { useGarmentStore } from '../../store/garmentStore';

const Viewport3D = () => {
  const controlsRef = useRef<any>();
  const { activeAvatar } = useAvatarStore();
  const { selectedGarments } = useGarmentStore();
  
  const handleReset = () => {
    if (controlsRef.current) {
      controlsRef.current.reset();
    }
  };
  
  return (
    <div className="h-full w-full relative">
      <Canvas shadows>
        <PerspectiveCamera makeDefault position={[0, 1, 5]} />
        <OrbitControls
          ref={controlsRef}
          enablePan={false}
          minDistance={3}
          maxDistance={10}
          minPolarAngle={Math.PI / 4}
          maxPolarAngle={Math.PI / 1.5}
        />
        
        <ambientLight intensity={0.5} />
        <directionalLight
          position={[10, 10, 5]}
          intensity={1}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        
        <Suspense fallback={null}>
          <Avatar3D avatar={activeAvatar} selectedGarments={selectedGarments} />
          <Environment preset="city" />
        </Suspense>
        
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1, 0]} receiveShadow>
          <planeGeometry args={[10, 10]} />
          <shadowMaterial opacity={0.3} />
        </mesh>
      </Canvas>
      
      {/* Loading Overlay */}
      <Suspense fallback={<LoadingSpinner />}>
        {/* Controls */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex gap-4 bg-white/90 backdrop-blur-md rounded-full p-2 shadow-lg">
          <button
            onClick={handleReset}
            className="p-3 rounded-full bg-gradient-primary text-white hover:opacity-90 transition"
            title="Reset View"
          >
            <RotateCcw className="h-5 w-5" />
          </button>
          <button
            className="p-3 rounded-full bg-gradient-primary text-white hover:opacity-90 transition"
            title="Change Camera"
          >
            <Camera className="h-5 w-5" />
          </button>
          <button
            className="p-3 rounded-full bg-gradient-primary text-white hover:opacity-90 transition"
            title="Fullscreen"
          >
            <Maximize2 className="h-5 w-5" />
          </button>
          <button
            className="p-3 rounded-full bg-gradient-primary text-white hover:opacity-90 transition"
            title="Download Image"
          >
            <Download className="h-5 w-5" />
          </button>
        </div>
      </Suspense>
    </div>
  );
};

export default Viewport3D;