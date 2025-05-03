import React from 'react';

interface ErrorAlertProps {
  error: string;
}

const ErrorAlert: React.FC<ErrorAlertProps> = ({ error }) => {
  if (!error) return null;
  
  return (
    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p className="font-bold">Failed to get a positive API response</p>
      <p>{error}</p>
      <p className="mt-2">Please ensure your backend is running.</p>
    </div>
  );
};

export default ErrorAlert; 