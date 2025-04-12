import React, { RefObject } from 'react';

interface CoverLetterOutputProps {
  coverLetter: string;
  editableCoverLetter: string;
  isLoading: boolean;
  copyNotification: boolean;
  downloadNotification: boolean;
  coverLetterRef: RefObject<HTMLTextAreaElement>;
  handleCoverLetterEdit: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  handleCopyToClipboard: () => void;
  handleDownloadPDF: () => void;
}

const CoverLetterOutput: React.FC<CoverLetterOutputProps> = ({
  coverLetter,
  editableCoverLetter,
  isLoading,
  copyNotification,
  downloadNotification,
  coverLetterRef,
  handleCoverLetterEdit,
  handleCopyToClipboard,
  handleDownloadPDF
}) => {
  return (
    <div className="flex flex-col h-full">
      <div className="mb-3 flex justify-between items-center">
        <h2 className="text-lg font-medium text-gray-800">Generated Cover Letter</h2>
        <div className="flex items-center">
          {copyNotification && (
            <span className="text-green-600 mr-2 text-sm">Copied!</span>
          )}
          {downloadNotification && (
            <span className="text-green-600 mr-2 text-sm">Downloaded!</span>
          )}
          {coverLetter && (
            <div className="flex space-x-2">
              <button
                onClick={handleCopyToClipboard}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded-md text-sm flex items-center"
              >
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z"></path>
                  <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z"></path>
                </svg>
                Copy
              </button>
              <button
                onClick={handleDownloadPDF}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-1.5 rounded-md text-sm flex items-center"
              >
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                  <path fillRule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v3.586l-1.293-1.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V8z" clipRule="evenodd"></path>
                </svg>
                Download PDF
              </button>
            </div>
          )}
        </div>
      </div>
      <div className="border rounded-md p-6 bg-white shadow-sm flex flex-col flex-grow">
        {isLoading ? (
          <div className="flex flex-col justify-center items-center h-full">
            <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-blue-500 mb-4"></div>
            <p className="text-gray-600">Generating your cover letter...</p>
          </div>
        ) : coverLetter ? (
          <textarea
            ref={coverLetterRef}
            className="whitespace-pre-wrap text-gray-800 overflow-y-auto w-full h-full p-0 border-0 focus:ring-0 focus:outline-none resize-none editable-cover-letter"
            value={editableCoverLetter}
            onChange={handleCoverLetterEdit}
            spellCheck
          ></textarea>
        ) : (
          <div className="text-gray-400 flex justify-center items-center h-full">
            <p>Your generated cover letter will appear here</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CoverLetterOutput; 