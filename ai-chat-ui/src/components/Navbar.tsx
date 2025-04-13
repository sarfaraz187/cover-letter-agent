import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
  const { isAuthenticated, loginWithRedirect, logout, user, isLoading, error } = useAuth0();

  const handleLogin = async () => {
    try {
      console.log('Initiating login flow...');
      await loginWithRedirect({
        appState: {
          returnTo: window.location.pathname
        }
      });
    } catch (err) {
      console.error('Login error:', err);
    }
  };

  const handleLogout = () => {
    logout({ 
      logoutParams: { 
        returnTo: window.location.origin
      }
    });
  };

  if (error) {
    console.error('Auth0 error:', error);
  }

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Link to="/" className="flex items-center">
            <img 
              src="https://msarfaraz.blob.core.windows.net/portfolio-assets/mohammed.svg" 
              alt="Logo" 
              className="h-12 w-auto mr-2" 
            />
          </Link>
        </div>
        
        <div className="flex items-center space-x-4">
          {isLoading ? (
            <div className="px-4 py-2">Loading...</div>
          ) : isAuthenticated ? (
            <>
              <div className="flex items-center mr-4">
                {user?.picture && (
                  <img 
                    src={user.picture} 
                    alt="Profile" 
                    className="h-8 w-8 rounded-full mr-2"
                  />
                )}
                <span className="hidden md:inline">{user?.name}</span>
              </div>
              <Link 
                to="/generator" 
                className="px-4 py-2 border border-white text-white rounded hover:bg-white hover:text-gray-800 transition duration-200"
              >
                Cover Letter Generator
              </Link>
              <button
                onClick={handleLogout}
                className="px-4 py-2 border border-red-400 text-red-400 rounded hover:bg-red-500 hover:text-white hover:border-red-500 transition duration-200"
              >
                Log Out
              </button>
            </>
          ) : (
            <button
              onClick={handleLogin}
              className="px-4 py-2 border border-white text-white rounded hover:bg-white hover:text-gray-800 transition duration-200"
            >
              Log In
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar; 