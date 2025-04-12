import React from 'react';

interface FormSectionProps {
  position: string;
  companyName: string;
  aboutCompany: string;
  jobDescription: string;
  error: string;
  isLoading: boolean;
  isCvLoading: boolean;
  setPosition: (value: string) => void;
  setCompanyName: (value: string) => void;
  setAboutCompany: (value: string) => void;
  setJobDescription: (value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
}

const FormSection: React.FC<FormSectionProps> = ({
  position,
  companyName,
  aboutCompany,
  jobDescription,
  error,
  isLoading,
  isCvLoading,
  setPosition,
  setCompanyName,
  setAboutCompany,
  setJobDescription,
  onSubmit
}) => {
  return (
    <form onSubmit={onSubmit} className="space-y-3 bg-white p-6 rounded-lg shadow-sm flex flex-col h-full">
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
          className="w-full p-2 border rounded-md text-gray-800 min-h-[200px]"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the job description here..."              
        />
      </div>
      
      {error && <p className="text-red-500 mt-2">{error}</p>}
      
      <button
        type="submit"
        disabled={isLoading || isCvLoading}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-md disabled:bg-blue-400 mt-8"
      >
        {isLoading ? 'Generating...' : (isCvLoading ? 'Loading CV...' : 'Generate Cover Letter')}
      </button>
    </form>
  );
};

export default FormSection; 