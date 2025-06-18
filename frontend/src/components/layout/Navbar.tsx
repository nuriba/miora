import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Bell, Menu } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

const Navbar = () => {
  const location = useLocation();
  const { user, logout } = useAuthStore();
  
  const navigation = [
    { name: 'Try-On Studio', href: '/try-on' },
    { name: 'My Wardrobe', href: '/wardrobe' },
    { name: 'Community', href: '/community' },
    { name: 'Trending', href: '/trending' },
  ];
  
  const isActive = (path: string) => location.pathname === path;
  
  return (
    <nav className="fixed top-0 left-0 right-0 bg-white/95 backdrop-blur-md border-b border-gray-200 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <Link to="/dashboard" className="text-3xl font-bold gradient-text">
            Miora
          </Link>
          
          {/* Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`relative font-medium transition ${
                  isActive(item.href)
                    ? 'text-purple-600'
                    : 'text-gray-700 hover:text-purple-600'
                }`}
              >
                {item.name}
                {isActive(item.href) && (
                  <motion.div
                    layoutId="navbar-indicator"
                    className="absolute -bottom-1 left-0 right-0 h-0.5 bg-purple-600"
                  />
                )}
              </Link>
            ))}
          </div>
          
          {/* User Menu */}
          <div className="flex items-center space-x-4">
            <button className="p-2 text-gray-600 hover:text-purple-600 transition">
              <Bell className="h-5 w-5" />
            </button>
            
            <div className="relative group">
              <button className="flex items-center space-x-2">
                <div className="w-10 h-10 bg-gradient-primary rounded-full flex items-center justify-center text-white font-semibold">
                  {user?.email?.[0].toUpperCase()}
                </div>
              </button>
              
              {/* Dropdown */}
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                <Link
                  to="/profile"
                  className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Profile
                </Link>
                <Link
                  to="/settings"
                  className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Settings
                </Link>
                <hr className="my-1" />
                <button
                  onClick={logout}
                  className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Sign Out
                </button>
              </div>
            </div>
            
            <button className="md:hidden p-2 text-gray-600">
              <Menu className="h-6 w-6" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;