import { Link } from 'react-router-dom';
import { Camera, Upload, Sparkles, Users } from 'lucide-react';

interface Props {
  /**
   * Layout orientation – default is grid (horizontal). When set to "vertical" the
   * actions will be stacked one per row (useful for side-column layouts).
   */
  orientation?: 'horizontal' | 'vertical';
}

const QuickActions: React.FC<Props> = ({ orientation = 'horizontal' }) => {
  const actions = [
    {
      label: 'Create Avatar',
      icon: Camera,
      link: '/avatars',
      color: 'bg-blue-500',
    },
    {
      label: 'Add Garment',
      icon: Upload,
      link: '/wardrobe',
      color: 'bg-green-500',
    },
    {
      label: 'Virtual Try-On',
      icon: Sparkles,
      link: '/try-on',
      color: 'bg-purple-500',
    },
    {
      label: 'Community',
      icon: Users,
      link: '/community',
      color: 'bg-pink-500',
    },
  ];
  
  const containerClass =
    orientation === 'vertical'
      ? 'flex flex-col gap-4'
      : 'grid grid-cols-4 gap-4';

  return (
    <div className={containerClass}>
      {actions.map((action) => (
        <Link
          key={action.label}
          to={action.link}
          aria-label={action.label}
          className="group"
        >
          <div
            className={`${action.color} w-14 h-14 rounded-lg flex items-center justify-center text-white group-hover:scale-110 transition-transform`}
          >
            <action.icon className="h-6 w-6" />
          </div>
        </Link>
      ))}
    </div>
  );
};

export default QuickActions; 