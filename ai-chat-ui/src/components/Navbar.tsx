import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
  const { isAuthenticated, loginWithRedirect, logout, user } = useAuth0();

  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Link to="/" className="flex items-center">
            <span className="text-xl font-bold">Cover Letter Generator</span>
          </Link>
        </div>
        
        <div className="flex items-center space-x-4">
          {isAuthenticated ? (
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
              <Link to="/generator" className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700 transition">
                Cover Letter Generator
              </Link>
              <button
                onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
                className="px-4 py-2 bg-red-600 rounded hover:bg-red-700 transition"
              >
                Log Out
              </button>
            </>
          ) : (
            <button
              onClick={() => loginWithRedirect()}
              className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700 transition"
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