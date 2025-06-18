import { motion } from 'framer-motion';
import { Clock, Shirt, Star } from 'lucide-react';

const activities = [
  {
    id: 1,
    type: 'try_on',
    title: 'Tried on Blue Denim Jacket',
    time: '2 hours ago',
    icon: Shirt,
  },
  {
    id: 2,
    type: 'outfit',
    title: 'Saved "Weekend Casual" outfit',
    time: '5 hours ago',
    icon: Star,
  },
  {
    id: 3,
    type: 'garment',
    title: 'Added White Cotton Shirt',
    time: 'Yesterday',
    icon: Shirt,
  },
];

const RecentActivity = () => {
  return (
    <div className="card">
      <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>
      <div className="space-y-4">
        {activities.map((activity, index) => (
          <motion.div
            key={activity.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="flex items-center space-x-4"
          >
            <div className="bg-purple-100 p-2 rounded-lg">
              <activity.icon className="h-5 w-5 text-purple-600" />
            </div>
            <div className="flex-1">
              <p className="font-medium">{activity.title}</p>
              <p className="text-sm text-gray-500 flex items-center mt-1">
                <Clock className="h-3 w-3 mr-1" />
                {activity.time}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default RecentActivity; 