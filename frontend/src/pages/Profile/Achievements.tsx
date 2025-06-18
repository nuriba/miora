import { motion } from 'framer-motion';
import { Trophy, Star, Zap, Target } from 'lucide-react';

const Achievements = () => {
  const achievements = [
    {
      id: '1',
      title: 'Fashion Pioneer',
      description: 'Created your first avatar',
      icon: Star,
      color: 'bg-yellow-500',
      unlocked: true,
      date: '2024-01-15',
    },
    {
      id: '2',
      title: 'Wardrobe Master',
      description: 'Added 25 garments to your wardrobe',
      icon: Trophy,
      color: 'bg-purple-500',
      unlocked: true,
      date: '2024-02-20',
    },
    {
      id: '3',
      title: 'Trendsetter',
      description: 'Get 100 likes on a single outfit',
      icon: Zap,
      color: 'bg-pink-500',
      unlocked: false,
      progress: 75,
    },
    {
      id: '4',
      title: 'Perfect Fit',
      description: '10 try-ons with 90%+ fit score',
      icon: Target,
      color: 'bg-green-500',
      unlocked: false,
      progress: 60,
    },
  ];
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {achievements.map((achievement, index) => (
        <motion.div
          key={achievement.id}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: index * 0.1 }}
          className={`p-6 rounded-xl ${
            achievement.unlocked
              ? 'bg-white shadow-lg'
              : 'bg-gray-50 border-2 border-gray-200 border-dashed'
          }`}
        >
          <div className="flex items-start space-x-4">
            <div
              className={`p-3 rounded-full ${
                achievement.unlocked
                  ? achievement.color
                  : 'bg-gray-300'
              } text-white`}
            >
              <achievement.icon className="h-6 w-6" />
            </div>
            <div className="flex-1">
              <h3 className={`font-semibold text-lg ${
                achievement.unlocked ? 'text-gray-900' : 'text-gray-500'
              }`}>
                {achievement.title}
              </h3>
              <p className={`text-sm mt-1 ${
                achievement.unlocked ? 'text-gray-600' : 'text-gray-400'
              }`}>
                {achievement.description}
              </p>
              {achievement.unlocked ? (
                <p className="text-xs text-gray-500 mt-2">
                  Unlocked on {new Date(achievement.date!).toLocaleDateString()}
                </p>
              ) : (
                <div className="mt-3">
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>Progress</span>
                    <span>{achievement.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-purple-600 h-2 rounded-full transition-all"
                      style={{ width: `${achievement.progress}%` }}
                    />
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default Achievements;