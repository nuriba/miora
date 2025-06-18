import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuthStore } from '../../store/authStore';
import { useAvatarStore } from '../../store/avatarStore';
import RecentActivity from './RecentActivity';
import QuickActions from './QuickActions';

const Dashboard = () => {
  const user = useAuthStore((state) => state.user);
  const { activeAvatar, fetchAvatars } = useAvatarStore();
  
  useEffect(() => {
    fetchAvatars();
  }, [fetchAvatars]);
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.email?.split('@')[0]}!
        </h1>
        <p className="mt-1 text-lg text-gray-500">
          Here's what's happening with your virtual wardrobe today.
        </p>
      </div>
      
      {/* Avatar Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="mb-8 flex justify-center"
      >
        <div className="card w-full lg:max-w-3xl flex flex-col items-center justify-center min-h-[260px]">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={activeAvatar?.thumbnail_url || '/default-avatar.png'}
            alt="Avatar"
            className="h-32 w-32 rounded-full object-cover mb-4"
          />
          <h3 className="text-xl font-semibold">
            {activeAvatar?.name || 'Default Avatar'}
          </h3>
        </div>
      </motion.div>

      {/* Quick Actions Horizontal */}
      <div className="mb-8 flex justify-center">
        <QuickActions orientation="horizontal" />
      </div>
      
      {/* Recent Activity */}
      <div className="mt-8">
        <RecentActivity />
      </div>
    </div>
  );
};

export default Dashboard;