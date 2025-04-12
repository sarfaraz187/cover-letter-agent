import React from 'react';

interface CvErrorAlertProps {
  error: string;
}

const CvErrorAlert: React.FC<CvErrorAlertProps> = ({ error }) => {
  if (!error) return null;
  
  return (
    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      <p className="font-bold">CV Loading Error</p>
      <p>{error}</p>
      <p className="mt-2">Please ensure your CV file (mohammed_sarfaraz_cv.pdf) is in the root directory of the server.</p>
    </div>
  );
};

export default CvErrorAlert; 