import AvatarSidebar from './AvatarSidebar';
import Viewport3D from './Viewport3D';
import FitAnalysisPanel from './FitAnalysisPanel';
import { useAvatarStore } from '../../store/avatarStore';
import { useGarmentStore } from '../../store/garmentStore';

const VirtualTryOn = () => {
  const { activeAvatar } = useAvatarStore();
  const { selectedGarments } = useGarmentStore();
  
  return (
    <div className="h-[calc(100vh-5rem)] flex bg-gradient-primary">
      {/* Left Sidebar - Avatar & Wardrobe */}
      <AvatarSidebar />
      
      {/* Center - 3D Viewport */}
      <div className="flex-1 relative">
        <Viewport3D />
      </div>
      
      {/* Right Panel - Fit Analysis */}
      <FitAnalysisPanel 
        selectedGarments={selectedGarments}
        avatar={activeAvatar}
      />
    </div>
  );
};

export default VirtualTryOn;