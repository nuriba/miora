import { Link } from 'react-router-dom';
import { LucideIcon } from 'lucide-react';

interface Props {
  title: string;
  value: string | number;
  icon: LucideIcon;
  color: string;
  link: string;
}

const StatsCard: React.FC<Props> = ({ title, value, icon: Icon, color, link }) => {
  return (
    <Link
      to={link}
      className="card hover:shadow-xl transition-all group"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm">{title}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
        <div className={`${color} p-3 rounded-full text-white group-hover:scale-110 transition-transform`}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
    </Link>
  );
};

export default StatsCard; 