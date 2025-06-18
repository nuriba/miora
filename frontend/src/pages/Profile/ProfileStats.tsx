import { motion } from 'framer-motion';
import { Users, Shirt, Star, TrendingUp } from 'lucide-react';

const ProfileStats = () => {
  const stats = [
    {
      label: 'Avatars Created',
      value: '3',
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      label: 'Garments',
      value: '24',
      icon: Shirt,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      label: 'Outfits Saved',
      value: '12',
      icon: Star,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
    },
    {
      label: 'Try-On Sessions',
      value: '48',
      icon: TrendingUp,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
  ];
  
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
      {stats.map((stat, index) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="bg-white rounded-xl p-6 text-center shadow-lg"
        >
          <div className={`${stat.bgColor} w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3`}>
            <stat.icon className={`h-6 w-6 ${stat.color}`} />
          </div>
          <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
          <p className="text-sm text-gray-600">{stat.label}</p>
        </motion.div>
      ))}
    </div>
  );
};

export default ProfileStats;