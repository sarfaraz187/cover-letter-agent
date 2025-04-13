import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => {
  const { isAuthenticated, loginWithRedirect, isLoading } = useAuth0();

  const handleLogin = async () => {
    try {
      console.log('Initiating login flow from homepage...');
      await loginWithRedirect({
        appState: {
          returnTo: "/generator"
        }
      });
    } catch (err) {
      console.error('Login error from homepage:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            AI Cover Letter Generator
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Create professional, tailored cover letters in seconds using AI technology
            that adapts to your resume and the job description.
          </p>
          
          <div className="mb-12">
            {isLoading ? (
              <div className="px-6 py-3 bg-gray-300 text-gray-700 rounded-lg text-lg font-medium inline-block">
                Loading...
              </div>
            ) : isAuthenticated ? (
              <Link 
                to="/generator" 
                className="px-6 py-3 border-2 border-gray-800 text-gray-800 rounded-lg text-lg font-medium hover:bg-gray-800 hover:text-white transition duration-300 shadow-lg"
              >
                Go to Cover Letter Generator
              </Link>
            ) : (
              <button 
                onClick={handleLogin}
                className="px-6 py-3 border-2 border-gray-800 text-gray-800 rounded-lg text-lg font-medium hover:bg-gray-800 hover:text-white transition duration-300 shadow-lg"
              >
                Log In to Get Started
              </button>
            )}
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-4xl mb-4">
                <i className="fas fa-bolt"></i>
              </div>
              <h3 className="text-xl font-semibold mb-2">Fast & Effortless</h3>
              <p className="text-gray-600">
                Generate a professional cover letter in seconds, not hours.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-4xl mb-4">
                <i className="fas fa-fingerprint"></i>
              </div>
              <h3 className="text-xl font-semibold mb-2">Personalized</h3>
              <p className="text-gray-600">
                Each cover letter is tailored to your resume and the job description.
              </p>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-blue-600 text-4xl mb-4">
                <i className="fas fa-file-alt"></i>
              </div>
              <h3 className="text-xl font-semibold mb-2">Professional Results</h3>
              <p className="text-gray-600">
                Get polished, ready-to-send cover letters that make you stand out.
              </p>
            </div>
          </div>
          
          <div className="bg-white p-8 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-4">How It Works</h2>
            <ol className="text-left space-y-4">
              <li className="flex items-start">
                <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-1 flex-shrink-0">1</span>
                <span>Log in with your account</span>
              </li>
              <li className="flex items-start">
                <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-1 flex-shrink-0">2</span>
                <span>Enter the job description and position details</span>
              </li>
              <li className="flex items-start">
                <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-1 flex-shrink-0">3</span>
                <span>Our AI analyzes your resume and creates a tailored cover letter</span>
              </li>
              <li className="flex items-start">
                <span className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-1 flex-shrink-0">4</span>
                <span>Edit your cover letter if needed and download the final result</span>
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 