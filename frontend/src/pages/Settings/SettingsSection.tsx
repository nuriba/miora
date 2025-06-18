import { ReactNode } from 'react';

interface Props {
  title: string;
  description?: string;
  children: ReactNode;
}

const SettingsSection: React.FC<Props> = ({ title, description, children }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="mb-6">
        <h2 className="text-xl font-semibold">{title}</h2>
        {description && (
          <p className="text-gray-600 mt-1">{description}</p>
        )}
      </div>
      {children}
    </div>
  );
};

export default SettingsSection;