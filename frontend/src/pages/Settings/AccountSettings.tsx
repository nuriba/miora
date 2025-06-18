import { useState } from 'react';
import { Mail, Key, Smartphone, Trash2 } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import toast from 'react-hot-toast';

const AccountSettings = () => {
  const { user } = useAuthStore();
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  
  const handleChangePassword = () => {
    // Handle password change
    toast.success('Password change email sent!');
  };
  
  const handleDeleteAccount = () => {
    // Handle account deletion
    toast.error('Account deletion is not available in demo');
    setShowDeleteConfirm(false);
  };
  
  return (
    <div className="space-y-6">
      {/* Account Information */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Account Information</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email Address
            </label>
            <div className="flex items-center space-x-3">
              <Mail className="h-5 w-5 text-gray-400" />
              <input
                type="email"
                value={user?.email || ''}
                disabled
                className="flex-1 border-gray-300 rounded-lg bg-gray-50"
              />
            </div>
            <p className="mt-1 text-sm text-gray-500">
              Your email cannot be changed
            </p>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Account Type
            </label>
            <div className="inline-flex items-center px-3 py-1 rounded-full bg-purple-100 text-purple-600 text-sm font-medium">
              Free Plan
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Member Since
            </label>
            <p className="text-gray-900">
              {new Date(user?.created_at || '').toLocaleDateString('en-US', {
                month: 'long',
                day: 'numeric',
                year: 'numeric',
              })}
            </p>
          </div>
        </div>
      </div>
      
      {/* Password & Security */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-6">Password & Security</h2>
        
        <div className="space-y-4">
          <div>
            <button
              onClick={handleChangePassword}
              className="flex items-center space-x-3 text-purple-600 hover:text-purple-700 font-medium"
            >
              <Key className="h-5 w-5" />
              <span>Change Password</span>
            </button>
            <p className="mt-1 text-sm text-gray-500 ml-8">
              We'll send you an email with instructions
            </p>
          </div>
          
          <div className="pt-4 border-t">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Smartphone className="h-5 w-5 text-gray-400" />
                <div>
                  <p className="font-medium">Two-Factor Authentication</p>
                  <p className="text-sm text-gray-500">
                    Add an extra layer of security to your account
                  </p>
                </div>
              </div>
              <button className="btn btn-secondary text-sm">
                Enable
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Danger Zone */}
      <div className="bg-red-50 border border-red-200 rounded-xl p-6">
        <h2 className="text-xl font-semibold text-red-900 mb-4">Danger Zone</h2>
        
        <div className="space-y-4">
          <div>
            <p className="text-red-700 mb-3">
              Once you delete your account, there is no going back. Please be certain.
            </p>
            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
            >
              <Trash2 className="h-4 w-4" />
              <span>Delete Account</span>
            </button>
          </div>
        </div>
      </div>
      
      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl p-6 max-w-md w-full">
            <h3 className="text-lg font-semibold mb-4">Delete Account?</h3>
            <p className="text-gray-600 mb-6">
              This action cannot be undone. All your data will be permanently deleted.
            </p>
            <div className="flex space-x-4">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="flex-1 btn btn-secondary"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteAccount}
                className="flex-1 btn bg-red-600 text-white hover:bg-red-700"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AccountSettings;