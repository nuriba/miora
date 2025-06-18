import { motion } from 'framer-motion';
import { Heart, MessageSquare, UserPlus, ShoppingBag } from 'lucide-react';

const ActivityFeed = () => {
  const activities = [
    {
      id: '1',
      type: 'like',
      user: 'Sarah Johnson',
      action: 'liked your outfit',
      outfit: 'Casual Friday',
      time: '2 hours ago',
      icon: Heart,
      iconColor: 'text-red-500',
    },
    {
      id: '2',
      type: 'comment',
      user: 'Mike Chen',
      action: 'commented on',
      outfit: 'Business Meeting',
      time: '5 hours ago',
      icon: MessageSquare,
      iconColor: 'text-blue-500',
    },
    {
      id: '3',
      type: 'follow',
      user: 'Emma Davis',
      action: 'started following you',
      time: '1 day ago',
      icon: UserPlus,
      iconColor: 'text-green-500',
    },
    {
      id: '4',
      type: 'purchase',
      user: 'You',
      action: 'purchased an item from',
      outfit: 'Summer Collection',
      time: '3 days ago',
      icon: ShoppingBag,
      iconColor: 'text-purple-500',
    },
  ];
  
  return (
    <div className="space-y-4">
      {activities.map((activity, index) => (
        <motion.div
          key={activity.id}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
        >
          <div className={`p-2 bg-white rounded-full ${activity.iconColor}`}>
            <activity.icon className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <p className="text-gray-900">
              <span className="font-semibold">{activity.user}</span>{' '}
              {activity.action}{' '}
              {activity.outfit && (
                <span className="font-semibold text-purple-600">
                  {activity.outfit}
                </span>
              )}
            </p>
            <p className="text-sm text-gray-500 mt-1">{activity.time}</p>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default ActivityFeed;