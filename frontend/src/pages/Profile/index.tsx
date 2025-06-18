import { useState } from 'react';
import ProfileHeader from './ProfileHeader.tsx';
import ProfileStats from './ProfileStats.tsx';
import ProfileTabs from './ProfileTabs.tsx';
import EditProfileModal from './EditProfileModal.tsx';
import { useAuthStore } from '../../store/authStore';

const Profile = () => {
  const { user } = useAuthStore();
  const [showEditModal, setShowEditModal] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Profile Header */}
      <ProfileHeader 
        user={user} 
        onEdit={() => setShowEditModal(true)} 
      />
      
      {/* Stats Section */}
      <ProfileStats />
      
      {/* Profile Content Tabs */}
      <ProfileTabs activeTab={activeTab} onTabChange={setActiveTab} />
      
      {/* Edit Profile Modal */}
      {showEditModal && (
        <EditProfileModal onClose={() => setShowEditModal(false)} />
      )}
    </div>
  );
};

export default Profile;