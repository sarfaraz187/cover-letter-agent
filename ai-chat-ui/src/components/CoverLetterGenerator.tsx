import React, { useState, useEffect } from 'react';
import { generateCoverLetter, fetchCvData } from '../services/api';

const CoverLetterGenerator: React.FC = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [position, setPosition] = useState('');
  const [aboutCompany, setAboutCompany] = useState('');
  const [cvContent, setCvContent] = useState('');
  const [coverLetter, setCoverLetter] = useState('');
  const [editableCoverLetter, setEditableCoverLetter] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isCvLoading, setIsCvLoading] = useState(true);
  const [error, setError] = useState('');
  const [cvError, setCvError] = useState('');
  const [copyNotification, setCopyNotification] = useState(false);

  // Load CV data on component mount
  useEffect(() => {
    const loadCvData = async () => {
      setIsCvLoading(true);
      setCvError('');
      
      try {
        const data = await fetchCvData();
        setCvContent(data);
        console.log('CV data loaded successfully');
      } catch (err) {
        console.error('CV loading error:', err);
        setCvError(err instanceof Error ? err.message : 'Failed to load CV data');
      } finally {
        setIsCvLoading(false);
      }
    };

    loadCvData();
  }, []);

  // Update editable cover letter when the AI generates a new one
  useEffect(() => {
    if (coverLetter) {
      setEditableCoverLetter(coverLetter);
    }
  }, [coverLetter]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!jobDescription.trim() || !position.trim() || !companyName.trim()) {
      setError('Please provide job description, position, and company name');
      return;
    }
    
    if (!cvContent) {
      setError('CV data is not available. Please refresh the page or contact support.');
      return;
    }
    
    setIsLoading(true);
    setError('');
    
    try {
      // Combine data for API request
      const formattedJobDescription = `
Position: ${position}
Company: ${companyName}
About Company: ${aboutCompany}
Job Description: ${jobDescription}
      `;
      
      const result = await generateCoverLetter(formattedJobDescription, cvContent);
      setCoverLetter(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(editableCoverLetter);
    setCopyNotification(true);
    setTimeout(() => {
      setCopyNotification(false);
    }, 2000);
  };

  // Handle editable cover letter changes
  const handleCoverLetterEdit = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setEditableCoverLetter(e.target.value);
  };

  // Display CV loading status at the top if there's an error
  const renderCvStatus = () => {
    if (cvError) {
      return (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p className="font-bold">CV Loading Error</p>
          <p>{cvError}</p>
          <p className="mt-2">Please ensure your CV file (mohammed_sarfaraz_cv.pdf) is in the root directory of the server.</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="flex flex-col h-full max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold mb-5 text-gray-800">AI Cover Letter Agent</h1>
      
      {renderCvStatus()}
      
      <div className="grid grid-cols-1 md:grid-cols-10 gap-6 mb-2 min-h-[600px]">
        <div className="md:col-span-4 flex flex-col">
          <form onSubmit={handleSubmit} className="space-y-3 bg-white p-6 rounded-lg shadow-sm flex flex-col h-full">
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Position
                </label>
                <input 
                  type="text"
                  className="w-full p-2 border rounded-md text-gray-800"
                  value={position}
                  onChange={(e) => setPosition(e.target.value)}
                  placeholder="e.g. Software Engineer"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-700">
                  Company Name
                </label>
                <input 
                  type="text"
                  className="w-full p-2 border rounded-md text-gray-800"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  placeholder="e.g. Google, Amazon"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-700">
                About Company (Optional)
              </label>
              <textarea 
                className="w-full p-2 border rounded-md text-gray-800 min-h-[180px]"
                value={aboutCompany}
                onChange={(e) => setAboutCompany(e.target.value)}
                placeholder="Brief description of the company, culture, and mission..."
              />
            </div>
            
            <div className="flex-grow">
              <label className="block text-sm font-medium mb-2 text-gray-700">
                Job Description
              </label>
              <textarea 
                className="w-full p-2 border rounded-md text-gray-800  min-h-[200px]"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."              
              />
            </div>
            
            {error && <p className="text-red-500 mt-2">{error}</p>}
            
            <button
              type="submit"
              disabled={isLoading || isCvLoading || !cvContent}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-md disabled:bg-blue-400 mt-8"
            >
              {isLoading ? 'Generating...' : (isCvLoading ? 'Loading CV...' : 'Generate Cover Letter')}
            </button>
          </form>
        </div>
        
        <div className="md:col-span-6 flex flex-col">
          <div className="mb-3 flex justify-between items-center">
            <h2 className="text-lg font-medium text-gray-800">Generated Cover Letter</h2>
            <div className="flex items-center">
              {copyNotification && (
                <span className="text-green-600 mr-2 text-sm">Copied!</span>
              )}
              {coverLetter && (
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
      </div>
    </div>
  );
};

export default CoverLetterGenerator; 